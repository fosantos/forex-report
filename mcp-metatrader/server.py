#!/usr/bin/env python3
"""MCP server: MetaTrader 5 (via mt5_bridge.py on the Windows host).

Stdio server. Forwards every tool call to the bridge over authenticated HTTP,
so it works from WSL/Linux while the MT5 terminal runs on Windows.

Env:
  MT5_BRIDGE_URL      bridge base URL (default http://127.0.0.1:8765)
  MT5_BRIDGE_TOKEN    shared secret (required; must match the bridge)
  MT5_ENABLE_TRADING  "1" enables order/close/modify tools (default off;
                      the bridge enforces the same flag on its side)
"""

import json
import os
import urllib.error
import urllib.request

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

BRIDGE_URL = os.environ.get("MT5_BRIDGE_URL", "http://127.0.0.1:8765").rstrip("/")
TOKEN = os.environ.get("MT5_BRIDGE_TOKEN", "")
TRADING = os.environ.get("MT5_ENABLE_TRADING", "0") == "1"
TIMEOUT = 30

mcp = MCPServer(
    "metatrader",
    instructions="MetaTrader 5 terminal access: quotes, OHLC history, open "
                 "positions and (when enabled) order placement through the "
                 "mt5_bridge. Never invent prices; every value comes from the "
                 "terminal. Trading tools need MT5_ENABLE_TRADING=1.",
)


_DIRECT_OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def call_bridge(op, params=None):
    if not TOKEN:
        raise ToolError(
            "MT5_BRIDGE_TOKEN is not configured on the MCP server. "
            "Re-register with: muse mcp add metatrader -e MT5_BRIDGE_TOKEN=<secret> …"
        )
    body = json.dumps({"op": op, "params": params or {}}).encode()
    req = urllib.request.Request(
        BRIDGE_URL + "/",
        data=body,
        headers={"Content-Type": "application/json", "X-MT5-Token": TOKEN},
        method="POST",
    )
    try:
        # Direct connection: bridge traffic is LAN/localhost by design and must
        # never go through a web proxy (also avoids hangs on proxied localhost).
        with _DIRECT_OPENER.open(req, timeout=TIMEOUT) as resp:
            payload = json.load(resp)
    except urllib.error.HTTPError as e:
        try:
            detail = json.load(e).get("error", e.reason)
        except ValueError:
            detail = e.reason
        raise ToolError(f"bridge HTTP {e.code}: {detail}")
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        raise ToolError(
            f"MT5 bridge unreachable at {BRIDGE_URL}: {e}. "
            "On Windows, with the terminal running: "
            "set MT5_BRIDGE_TOKEN=<same secret> && python mt5_bridge.py"
        )
    if not payload.get("ok"):
        raise ToolError(str(payload.get("error", "unknown bridge error")))
    return payload["data"]


def dump(data):
    return json.dumps(data, ensure_ascii=False)


def need_trading():
    if not TRADING:
        raise ToolError(
            "trading tools are disabled (MT5_ENABLE_TRADING != 1 on the MCP side). "
            "Re-register with -e MT5_ENABLE_TRADING=1 and restart the bridge with "
            "MT5_ENABLE_TRADING=1 to allow orders."
        )


@mcp.tool()
def mt5_status() -> str:
    """Terminal + trading-account status (connection, balance, equity, margin, currency)."""
    return dump(call_bridge("status"))


@mcp.tool()
def mt5_quote(symbol: str) -> str:
    """Live tick for a symbol: bid, ask, time, spread (e.g. symbol='EURUSD')."""
    return dump(call_bridge("tick", {"symbol": symbol}))


@mcp.tool()
def mt5_rates(symbol: str, timeframe: str = "D1", count: int = 500) -> str:
    """OHLC history: timeframe M1/M5/M15/M30/H1/H4/D1/W1/MN1, count<=5000 (latest last)."""
    return dump(call_bridge("rates", {"symbol": symbol, "timeframe": timeframe,
                                      "count": count}))


@mcp.tool()
def mt5_symbols(search: str = "") -> str:
    """List trade symbols, optionally filtered by prefix (e.g. search='EUR')."""
    return dump(call_bridge("symbols", {"search": search}))


@mcp.tool()
def mt5_positions(symbol: str = "") -> str:
    """Open positions, optionally filtered by symbol. Shows ticket, volume, price, SL/TP, profit."""
    return dump(call_bridge("positions", {"symbol": symbol or None}))


@mcp.tool()
def mt5_deals(start: str, end: str) -> str:
    """Closed-deal history between ISO datetimes (e.g. start='2026-11-01', end='2026-11-20')."""
    return dump(call_bridge("deals", {"start": start, "end": end}))


@mcp.tool()
def mt5_order(symbol: str, side: str, volume: float, order_type: str = "market",
              price: float = 0.0, sl: float = 0.0, tp: float = 0.0,
              deviation: int = 20, magic: int = 0,
              comment: str = "mcp-metatrader") -> str:
    """Place an order (needs MT5_ENABLE_TRADING=1). side=buy|sell; order_type=market|limit|stop
    (price required unless market). sl/tp absolute prices, 0 = none. Returns the fill report."""
    need_trading()
    side, order_type = side.lower(), order_type.lower()
    if side not in ("buy", "sell") or order_type not in ("market", "limit", "stop"):
        raise ToolError("side must be buy|sell and order_type market|limit|stop")
    mt5_type = {"buy": {"market": "BUY", "limit": "BUY_LIMIT", "stop": "BUY_STOP"},
                "sell": {"market": "SELL", "limit": "SELL_LIMIT", "stop": "SELL_STOP"}}[side][order_type]
    if order_type != "market" and price <= 0:
        raise ToolError("price is required for limit/stop orders")
    return dump(call_bridge("order", {"symbol": symbol, "type": mt5_type,
                                      "volume": volume, "price": price, "sl": sl,
                                      "tp": tp, "deviation": deviation,
                                      "magic": magic, "comment": comment}))


@mcp.tool()
def mt5_close_position(ticket: int, deviation: int = 20) -> str:
    """Close a position in full at market (needs MT5_ENABLE_TRADING=1)."""
    need_trading()
    return dump(call_bridge("close", {"ticket": ticket, "deviation": deviation}))


@mcp.tool()
def mt5_modify_position(ticket: int, sl: float, tp: float) -> str:
    """Move SL/TP of an open position, absolute prices (needs MT5_ENABLE_TRADING=1)."""
    need_trading()
    return dump(call_bridge("modify", {"ticket": ticket, "sl": sl, "tp": tp}))


if __name__ == "__main__":
    mcp.run(transport="stdio")
