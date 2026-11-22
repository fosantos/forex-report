#!/usr/bin/env python3
"""MetaTrader 5 HTTP bridge — runs on Windows, next to the MT5 terminal.

The MCP server (server.py) cannot talk to the terminal directly when it runs
in WSL/Linux, so this small bridge runs on Windows (stdlib only, plus the
`MetaTrader5` pip package) and exposes the terminal over authenticated HTTP.

Usage (Windows; the terminal does NOT need to be open beforehand):
    set MT5_BRIDGE_TOKEN=<shared-secret>
    python mt5_bridge.py [--host 127.0.0.1] [--port 8765]

For WSL clients bind --host 0.0.0.0 (the token is mandatory either way).
Set MT5_ENABLE_TRADING=1 on BOTH sides to allow order/position tools.

When terminal64.exe is not running, the bridge launches it automatically and
waits (up to MT5_TERMINAL_TIMEOUT seconds, default 60) for initialize() to
succeed. Point MT5_TERMINAL_PATH at the exe when it is not in the default
install folder; set MT5_NO_AUTOLAUNCH=1 to disable the auto-launch and fail
fast instead.

Protocol: POST /  {"op": "<name>", "params": {...}}
          -> {"ok": true, "data": ...} | {"ok": false, "error": "..."}
Auth: header X-MT5-Token must equal MT5_BRIDGE_TOKEN (constant-time compare).
"""

import argparse
import glob
import hmac
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

TOKEN = os.environ.get("MT5_BRIDGE_TOKEN", "")
TRADING = os.environ.get("MT5_ENABLE_TRADING", "0") == "1"
MAX_RATES = 5000
MAX_ITEMS = 1000


def _env_int(name, default):
    try:
        return max(int(os.environ.get(name, str(default))), 1)
    except ValueError:
        return default


TERMINAL_TIMEOUT = _env_int("MT5_TERMINAL_TIMEOUT", 60)
AUTOLAUNCH = os.environ.get("MT5_NO_AUTOLAUNCH", "0") != "1"

TIMEFRAMES = {}  # filled lazily once MetaTrader5 is imported


class BridgeError(Exception):
    pass


_mt5 = None


def _terminal_candidates():
    """Possible terminal64.exe locations, most explicit first."""
    cands = []
    env_path = os.environ.get("MT5_TERMINAL_PATH", "").strip().strip('"')
    if env_path:
        cands.append(env_path)
    cands.append(r"C:\Program Files\MetaTrader 5\terminal64.exe")
    if os.name == "nt":
        pf86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")
        cands.append(os.path.join(pf86, "MetaTrader 5", "terminal64.exe"))
        # broker-branded installs (e.g. "MetaTrader 5 - XM") sit in siblings
        pf = os.environ.get("ProgramFiles", r"C:\Program Files")
        cands.extend(sorted(glob.glob(os.path.join(pf, "MetaTrader*", "terminal64.exe"))))
    seen, out = set(), []
    for c in cands:
        if c.lower() not in seen:
            seen.add(c.lower())
            out.append(c)
    return out


def _find_terminal():
    for cand in _terminal_candidates():
        if os.path.isfile(cand):
            return cand
    return None


def _terminal_process_running():
    """True when a terminal64.exe process exists (via Windows tasklist)."""
    if os.name != "nt":
        return False
    try:
        out = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq terminal64.exe", "/FO", "CSV", "/NH"],
            capture_output=True, text=True, timeout=15)
    except (OSError, subprocess.SubprocessError):
        return False
    return "terminal64.exe" in out.stdout.lower()


def _launch_terminal(path):
    """Start the terminal detached, so it outlives the bridge process."""
    flags = 0
    if os.name == "nt":
        flags = getattr(subprocess, "DETACHED_PROCESS", 0)
        flags |= getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
    subprocess.Popen([path], stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                     close_fds=True, creationflags=flags)


def _autolaunch_and_wait(m):
    """Launch terminal64.exe when it is down, then poll initialize().

    Returns True once initialize() succeeds. Raises BridgeError when the exe
    cannot be found/started or the wait times out; returns False when
    auto-launch is disabled or the terminal is already running (in which
    case initialize() failed for another reason and the original error
    stands).
    """
    if not AUTOLAUNCH or _terminal_process_running():
        return False
    path = _find_terminal()
    if path is None:
        raise BridgeError(
            "MT5 terminal is not running and terminal64.exe was not found. "
            "Install MetaTrader 5 or set MT5_TERMINAL_PATH to its terminal64.exe."
        )
    try:
        _launch_terminal(path)
    except OSError as e:
        raise BridgeError(
            f"MT5 terminal is not running and launching {path} failed: {e}")
    print(f"bridge: launched {path}, waiting up to "
          f"{TERMINAL_TIMEOUT}s for the terminal...", flush=True)
    deadline = time.time() + TERMINAL_TIMEOUT
    while time.time() < deadline:
        if m.initialize():
            print("bridge: terminal is up.", flush=True)
            return True
        time.sleep(2)
    raise BridgeError(
        f"MT5 terminal was launched but initialize() timed out after "
        f"{TERMINAL_TIMEOUT}s (last error: {m.last_error()}). Log into the "
        "terminal once manually, then retry.")


def mt5():
    """Import + initialize the terminal connection (re-tried while failing).

    When the terminal is not running, it is launched automatically (see
    MT5_TERMINAL_PATH / MT5_TERMINAL_TIMEOUT / MT5_NO_AUTOLAUNCH).
    """
    global _mt5, TIMEFRAMES
    if _mt5 is not None:
        info = _mt5.terminal_info()
        if info is not None:
            return _mt5
        _mt5.shutdown()  # terminal went away; re-init below
        _mt5 = None
    try:
        import MetaTrader5 as m
    except ImportError:
        raise BridgeError(
            "MetaTrader5 package not installed on the bridge host. "
            "On Windows: pip install MetaTrader5 "
            "(the bridge launches terminal64.exe itself when it is down)."
        )
    if not m.initialize() and not _autolaunch_and_wait(m):
        raise BridgeError(
            f"MT5 initialize() failed: {m.last_error()}. "
            "Is terminal64.exe running and logged into a (demo) account?"
        )
    _mt5 = m
    TIMEFRAMES = {
        "M1": m.TIMEFRAME_M1, "M5": m.TIMEFRAME_M5, "M15": m.TIMEFRAME_M15,
        "M30": m.TIMEFRAME_M30, "H1": m.TIMEFRAME_H1, "H4": m.TIMEFRAME_H4,
        "D1": m.TIMEFRAME_D1, "W1": m.TIMEFRAME_W1, "MN1": m.TIMEFRAME_MN1,
    }
    return _mt5


def timeframe(name):
    tf = TIMEFRAMES.get(str(name).upper())
    if tf is None:
        raise BridgeError(f"unknown timeframe {name!r}; use one of {sorted(TIMEFRAMES)}")
    return tf


def to_jsonable(obj):
    if obj is None or isinstance(obj, (bool, int, float, str)):
        return obj
    if hasattr(obj, "_asdict"):  # MT5 namedtuples (checked before tuple: they ARE tuples)
        return to_jsonable(obj._asdict())
    if isinstance(obj, dict):
        return {str(k): to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [to_jsonable(v) for v in obj]
    if hasattr(obj, "dtype") and hasattr(obj, "tolist"):  # numpy arrays/scalars
        return to_jsonable(obj.tolist())
    if isinstance(obj, datetime):
        ts = obj if obj.tzinfo else obj.replace(tzinfo=timezone.utc)
        return ts.astimezone(timezone.utc).isoformat()
    return str(obj)


def epoch_to_iso(epoch):
    return datetime.fromtimestamp(int(epoch), tz=timezone.utc).isoformat()


# ---------------------------------------------------------------- ops ---

def op_status(_p):
    m = mt5()
    t, a = m.terminal_info(), m.account_info()
    if t is None or a is None:
        raise BridgeError(f"terminal/account info unavailable: {m.last_error()}")
    return {"terminal": to_jsonable(t), "account": to_jsonable(a),
            "trading_enabled": TRADING}


def op_tick(p):
    m = mt5()
    symbol = p.get("symbol", "")
    if not m.symbol_select(symbol, True):
        raise BridgeError(f"symbol {symbol!r} not available: {m.last_error()}")
    tick = m.symbol_info_tick(symbol)
    if tick is None:
        raise BridgeError(f"no tick for {symbol!r}: {m.last_error()}")
    d = to_jsonable(tick)
    d["time_iso"] = epoch_to_iso(tick.time)
    return d


def op_rates(p):
    m = mt5()
    symbol = p.get("symbol", "")
    count = min(max(int(p.get("count", 500)), 1), MAX_RATES)
    start_pos = max(int(p.get("start_pos", 0)), 0)
    tf = timeframe(p.get("timeframe", "D1"))
    if not m.symbol_select(symbol, True):
        raise BridgeError(f"symbol {symbol!r} not available: {m.last_error()}")
    rates = m.copy_rates_from_pos(symbol, tf, start_pos, count)
    if rates is None or len(rates) == 0:
        raise BridgeError(f"no rates for {symbol}: {m.last_error()}")
    out = []
    for r in (rates.tolist() if hasattr(rates, "tolist") else rates):
        t, o, h, lo, c, tv, sp, rv = (r[i] if not isinstance(r, dict) else
                                      r[k] for i, k in enumerate(
                                          ("time", "open", "high", "low", "close",
                                           "tick_volume", "spread", "real_volume")))
        out.append({"time": epoch_to_iso(t), "open": o, "high": h, "low": lo,
                    "close": c, "tick_volume": tv, "spread": sp, "real_volume": rv})
    return {"symbol": symbol, "timeframe": str(p.get("timeframe", "D1")).upper(),
            "count": len(out), "rates": out}


def op_symbols(p):
    m = mt5()
    search = str(p.get("search", "") or "*")
    if not search.endswith("*"):
        search += "*"
    syms = m.symbols_get(search) or ()
    out = []
    for s in syms[:MAX_ITEMS]:
        out.append({"name": s.name, "digits": s.digits, "point": s.point,
                    "spread": s.spread, "trade_mode": s.trade_mode,
                    "volume_min": s.volume_min, "volume_max": s.volume_max,
                    "volume_step": s.volume_step,
                    "currency_base": s.currency_base,
                    "currency_profit": s.currency_profit})
    return {"count": len(out), "symbols": out}


def op_positions(p):
    m = mt5()
    symbol = p.get("symbol")
    ticket = p.get("ticket")
    if ticket is not None:
        res = m.positions_get(ticket=int(ticket))
    elif symbol:
        res = m.positions_get(symbol=symbol)
    else:
        res = m.positions_get()
    return {"count": len(res or ()), "positions": to_jsonable(list(res or ()))}


def op_deals(p):
    m = mt5()
    try:
        start = datetime.fromisoformat(str(p["start"]))
        end = datetime.fromisoformat(str(p["end"]))
    except (KeyError, ValueError):
        raise BridgeError("deals needs ISO datetimes 'start' and 'end'")
    deals = m.history_deals_get(start, end) or ()
    return {"count": min(len(deals), MAX_ITEMS),
            "deals": to_jsonable(list(deals[:MAX_ITEMS]))}


ORDER_TYPES = {}  # BUY/SELL/... filled lazily


def order_type(name):
    m = mt5()
    mapping = {"BUY": m.ORDER_TYPE_BUY, "SELL": m.ORDER_TYPE_SELL,
               "BUY_LIMIT": m.ORDER_TYPE_BUY_LIMIT, "SELL_LIMIT": m.ORDER_TYPE_SELL_LIMIT,
               "BUY_STOP": m.ORDER_TYPE_BUY_STOP, "SELL_STOP": m.ORDER_TYPE_SELL_STOP}
    t = mapping.get(str(name).upper())
    if t is None:
        raise BridgeError(f"unknown order type {name!r}; use one of {sorted(mapping)}")
    return t


def send_with_filling_fallback(request):
    """order_send trying IOC -> FOK -> RETURN (retcode 10030 = bad filling)."""
    m = mt5()
    last = None
    for filling in (m.ORDER_FILLING_IOC, m.ORDER_FILLING_FOK, m.ORDER_FILLING_RETURN):
        request["type_filling"] = filling
        last = m.order_send(request)
        if last is None:
            raise BridgeError(f"order_send failed: {m.last_error()}")
        if last.retcode != 10030:  # 10030 = unsupported filling mode
            break
    d = to_jsonable(last)
    d["success"] = last.retcode == m.TRADE_RETCODE_DONE
    return d


def op_order(p):
    m = mt5()
    if not TRADING:
        raise BridgeError("trading disabled on the bridge (set MT5_ENABLE_TRADING=1).")
    symbol = p.get("symbol", "")
    volume = float(p.get("volume", 0))
    if volume <= 0 or volume > 100:
        raise BridgeError(f"volume {volume} out of range (0, 100]")
    if not m.symbol_select(symbol, True):
        raise BridgeError(f"symbol {symbol!r} not available: {m.last_error()}")
    tick = m.symbol_info_tick(symbol)
    if tick is None:
        raise BridgeError(f"no tick for {symbol!r}: {m.last_error()}")
    otype = order_type(p.get("type", "BUY"))
    is_buy = otype in (m.ORDER_TYPE_BUY, m.ORDER_TYPE_BUY_LIMIT, m.ORDER_TYPE_BUY_STOP)
    price = float(p.get("price") or (tick.ask if is_buy else tick.bid))
    request = {"action": m.TRADE_ACTION_DEAL, "symbol": symbol, "volume": volume,
               "type": otype, "price": price,
               "sl": float(p.get("sl", 0.0)), "tp": float(p.get("tp", 0.0)),
               "deviation": int(p.get("deviation", 20)),
               "magic": int(p.get("magic", 0)),
               "comment": str(p.get("comment", "mcp-metatrader")),
               "type_time": m.ORDER_TIME_GTC}
    if otype not in (m.ORDER_TYPE_BUY, m.ORDER_TYPE_SELL):
        request["action"] = m.TRADE_ACTION_PENDING
    return send_with_filling_fallback(request)


def op_close(p):
    m = mt5()
    if not TRADING:
        raise BridgeError("trading disabled on the bridge (set MT5_ENABLE_TRADING=1).")
    ticket = int(p.get("ticket", 0))
    pos = m.positions_get(ticket=ticket)
    if not pos:
        raise BridgeError(f"position #{ticket} not found")
    pos = pos[0]
    tick = m.symbol_info_tick(pos.symbol)
    if tick is None:
        raise BridgeError(f"no tick for {pos.symbol!r}: {m.last_error()}")
    close_buy = pos.type == m.POSITION_TYPE_SELL
    request = {"action": m.TRADE_ACTION_DEAL, "symbol": pos.symbol,
               "volume": pos.volume,
               "type": m.ORDER_TYPE_BUY if close_buy else m.ORDER_TYPE_SELL,
               "position_id": ticket,
               "price": tick.ask if close_buy else tick.bid,
               "deviation": int(p.get("deviation", 20)),
               "magic": int(p.get("magic", 0)),
               "comment": str(p.get("comment", "mcp-metatrader-close")),
               "type_time": m.ORDER_TIME_GTC}
    return send_with_filling_fallback(request)


def op_modify(p):
    m = mt5()
    if not TRADING:
        raise BridgeError("trading disabled on the bridge (set MT5_ENABLE_TRADING=1).")
    ticket = int(p.get("ticket", 0))
    pos = m.positions_get(ticket=ticket)
    if not pos:
        raise BridgeError(f"position #{ticket} not found")
    request = {"action": m.TRADE_ACTION_SLTP, "symbol": pos[0].symbol,
               "position": ticket, "sl": float(p.get("sl", 0.0)),
               "tp": float(p.get("tp", 0.0))}
    res = m.order_send(request)
    if res is None:
        raise BridgeError(f"modify failed: {m.last_error()}")
    d = to_jsonable(res)
    d["success"] = res.retcode == m.TRADE_RETCODE_DONE
    return d


OPS = {"status": op_status, "tick": op_tick, "rates": op_rates,
       "symbols": op_symbols, "positions": op_positions, "deals": op_deals,
       "order": op_order, "close": op_close, "modify": op_modify}


class Handler(BaseHTTPRequestHandler):
    server_version = "mt5-bridge/1.0"

    def log_message(self, fmt, *args):
        sys.stderr.write("bridge: " + fmt % args + "\n")

    def _send(self, code, payload):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        token = self.headers.get("X-MT5-Token", "")
        if not TOKEN or not hmac.compare_digest(token, TOKEN):
            self._send(401, {"ok": False, "error": "bad or missing X-MT5-Token"})
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length) or b"{}")
        except (ValueError, OSError):
            self._send(400, {"ok": False, "error": "invalid JSON body"})
            return
        fn = OPS.get(body.get("op"))
        if fn is None:
            self._send(400, {"ok": False,
                             "error": f"unknown op {body.get('op')!r}; use one of {sorted(OPS)}"})
            return
        try:
            self._send(200, {"ok": True, "data": fn(body.get("params") or {})})
        except BridgeError as e:
            self._send(200, {"ok": False, "error": str(e)})
        except Exception as e:  # never leak a traceback over HTTP
            self._send(500, {"ok": False, "error": f"bridge internal error: {e}"})

    def do_GET(self):
        self._send(404, {"ok": False, "error": "POST JSON to /"})


def main():
    ap = argparse.ArgumentParser(description="MetaTrader 5 HTTP bridge for the MCP server.")
    ap.add_argument("--host", default="127.0.0.1",
                    help="bind address (use 0.0.0.0 for WSL clients)")
    ap.add_argument("--port", type=int, default=8765)
    args = ap.parse_args()
    if not TOKEN:
        sys.exit("refusing to start: set MT5_BRIDGE_TOKEN first (shared secret).")
    try:
        mt5()  # connect now (launching the terminal when needed) for a clear startup error
    except BridgeError as e:
        sys.exit(f"refusing to start: {e}")
    srv = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"mt5-bridge listening on http://{args.host}:{args.port} "
          f"(trading={'on' if TRADING else 'off'}, "
          f"autolaunch={'on' if AUTOLAUNCH else 'off'})", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        if _mt5 is not None:
            _mt5.shutdown()


if __name__ == "__main__":
    main()
