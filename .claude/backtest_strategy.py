#!/usr/bin/env python3
"""Permanent re-validation backtest of the Research Desk swing rules on ECB/Frankfurter
daily closes, close-only, 2000 -> present, 6 pairs. Re-run before adopting any rule change
and compare against the baseline in .claude/backtest_results_2026-08-17.txt.

Canonical (PRIMARY) config since 17/08/2026 rule standardization:
Donchian 10 breakout / 10-session expiry / 1.5-sigma20 stop floor / R/R >= 1:2.
Baseline: portfolio +100.8R net, 821 trades, PF 1.31, t-stat +3.24.

Mechanical translation of the rules (documented approximations):
- Regime: bull = close > SMA200 and SMA50 > SMA200; bear mirrored; else MIXED.
- Pullback entry (trend continuation): in an aligned regime, a close back to/below the
  SMA50 (long) arms the setup; trigger = subsequent close > prev close AND > SMA50
  (short mirrored). This approximates "anchor zone touch + close in trend direction".
- Breakout entry: close beyond the prior N-day extreme (N=10 primary/canonical,
  N=20 variant), allowed in aligned regimes and in MIXED only in the direction of
  the SMA200 side ("breakout resolves the mix"). Approximation: single-close trigger.
- Stop: the FARTHER of (1.5 x sigma20 from entry, trailing 10-day extreme)
  -> "structurally protected" + volatility floor.
- Target: nearest structural level beyond entry among (N-day extreme, 195-day extreme).
  If no level exists beyond entry (e.g. breakout at 9-month highs) -> no trade.
- R/R gate: (target-entry)/(entry-stop) >= 2.0, else skip (WAIT).
- Resolution is CLOSE-based (ledger convention): stop/target on daily close cross;
  EXPIRED after `expiry` sessions with R from the expiry close.
- One position per pair at a time. JPY intervention floor (2.5 sigma) NOT modeled.
- Event filter (24h macro) NOT modeled (no historical calendar in data).
Costs: COST_PIPS round-trip per trade, converted to R via the stop distance.
"""
import urllib.request, json, statistics, sys
from datetime import date

START = '2000-01-01'
END = date.today().isoformat()
PIP = {'EUR/USD': 0.0001, 'USD/JPY': 0.01, 'AUD/USD': 0.0001,
       'GBP/USD': 0.0001, 'EUR/JPY': 0.01, 'GBP/JPY': 0.01}
COST_PIPS = 1.5
FLOOR_SIG = 1.5
RR_MIN = 2.0
WARM = 250

req = urllib.request.Request(
    f'https://api.frankfurter.app/{START}..{END}?from=USD&to=EUR,JPY,GBP,AUD',
    headers={'User-Agent': 'Mozilla/5.0 (forex-report)'})
data = json.load(urllib.request.urlopen(req, timeout=180))
dates = sorted(data['rates'].keys())
print(f'Series: {dates[0]} .. {dates[-1]}  ({len(dates)} sessions)\n')

PAIRS = {
    'EUR/USD': lambda r: 1.0 / r['EUR'],
    'USD/JPY': lambda r: r['JPY'],
    'AUD/USD': lambda r: 1.0 / r['AUD'],
    'GBP/USD': lambda r: 1.0 / r['GBP'],
    'EUR/JPY': lambda r: r['JPY'] / r['EUR'],
    'GBP/JPY': lambda r: r['JPY'] / r['GBP'],
}


def run_pair(pair, closes, breakout_n=20, expiry=10):
    n = len(closes)
    trades = []
    pos = None            # open ticket
    armed = None          # 'long'/'short' pullback armed
    skips = {'rr_gate': 0, 'no_target': 0}
    for i in range(WARM, n):
        c = closes[i]
        # ---- resolve open position (close-based) ----
        if pos:
            if pos['dir'] == 'long':
                if c <= pos['stop']:
                    r = -1.0
                elif c >= pos['target']:
                    r = pos['plannedR']
                elif i - pos['entry_i'] >= expiry:
                    r = (c - pos['entry']) / (pos['entry'] - pos['stop'])
                else:
                    r = None
            else:
                if c >= pos['stop']:
                    r = -1.0
                elif c <= pos['target']:
                    r = pos['plannedR']
                elif i - pos['entry_i'] >= expiry:
                    r = (pos['entry'] - c) / (pos['stop'] - pos['entry'])
                else:
                    r = None
            if r is not None:
                cost_r = COST_PIPS * PIP[pair] / abs(pos['entry'] - pos['stop'])
                trades.append(dict(dir=pos['dir'], setup=pos['setup'], entry_i=pos['entry_i'],
                                   exit_i=i, entry=pos['entry'], exit=c, stop=pos['stop'],
                                   target=pos['target'], plannedR=pos['plannedR'],
                                   R=r, Rnet=r - cost_r))
                pos = None
            continue
        # ---- indicators from data up to and including close i ----
        prev = closes[i - 1]
        sma50 = sum(closes[i - 49:i + 1]) / 50.0
        sma200 = sum(closes[i - 199:i + 1]) / 200.0
        rets = [closes[k] / closes[k - 1] - 1.0 for k in range(i - 19, i + 1)]
        sig = statistics.stdev(rets) * c
        floor = FLOOR_SIG * sig
        don10_lo = min(closes[i - 9:i + 1])   # trailing structural low incl. today
        don10_hi = max(closes[i - 9:i + 1])
        brk_hi = max(closes[i - breakout_n:i])  # breakout reference: prior N excl. today
        brk_lo = min(closes[i - breakout_n:i])
        swing_hi = max(closes[i - 194:i + 1])
        swing_lo = min(closes[i - 194:i + 1])
        bull = c > sma200 and sma50 > sma200
        bear = c < sma200 and sma50 < sma200

        def try_enter(direction, setup):
            nonlocal pos
            if direction == 'long':
                stop = min(c - floor, don10_lo)
                cands = sorted(x for x in (brk_hi, swing_hi) if x > c)
                tgt = cands[0] if cands else None
                if tgt is None:
                    skips['no_target'] += 1
                    return False
                if (tgt - c) / (c - stop) < RR_MIN:
                    skips['rr_gate'] += 1
                    return False
            else:
                stop = max(c + floor, don10_hi)
                cands = sorted((x for x in (brk_lo, swing_lo) if x < c), reverse=True)
                tgt = cands[0] if cands else None
                if tgt is None:
                    skips['no_target'] += 1
                    return False
                if (c - tgt) / (stop - c) < RR_MIN:
                    skips['rr_gate'] += 1
                    return False
            pos = dict(dir=direction, setup=setup, entry_i=i, entry=c, stop=stop,
                       target=tgt, plannedR=round(abs(tgt - c) / abs(c - stop), 3))
            return True

        # ---- pullback (trend continuation) ----
        if bull:
            if armed == 'short':
                armed = None
            if c <= sma50:
                armed = 'long'
            elif armed == 'long' and c > prev and c > sma50:
                if try_enter('long', 'pullback'):
                    armed = None
                    continue
        elif bear:
            if armed == 'long':
                armed = None
            if c >= sma50:
                armed = 'short'
            elif armed == 'short' and c < prev and c < sma50:
                if try_enter('short', 'pullback'):
                    armed = None
                    continue
        else:
            armed = None
        # ---- breakout (may resolve MIXED toward the SMA200 side) ----
        if c > brk_hi and (bull or c > sma200):
            try_enter('long', 'breakout')
        elif c < brk_lo and (bear or c < sma200):
            try_enter('short', 'breakout')
    return trades, skips


def stats(trades):
    if not trades:
        return dict(n=0)
    rs = [t['Rnet'] for t in trades]
    wins = [r for r in rs if r > 0]
    losses = [r for r in rs if r <= 0]
    cum = 0.0
    peak = 0.0
    maxdd = 0.0
    streak = worst = 0
    for r in rs:
        cum += r
        peak = max(peak, cum)
        maxdd = max(maxdd, peak - cum)
        streak = 0 if r > 0 else streak + 1
        worst = max(worst, streak)
    return dict(n=len(rs), win=100 * len(wins) / len(rs),
                avg=sum(rs) / len(rs), total=sum(rs),
                pf=(sum(wins) / abs(sum(losses))) if losses and sum(losses) != 0 else float('inf'),
                gross=sum(t['R'] for t in trades), maxdd=maxdd, worst_streak=worst)


def portfolio(all_trades):
    flat = sorted((t['exit_i'], t['Rnet'], t['setup']) for pair in all_trades for t in all_trades[pair])
    cum = 0.0; peak = 0.0; maxdd = 0.0
    rs = []
    for _, r, _s in flat:
        cum += r; rs.append(r)
        peak = max(peak, cum); maxdd = max(maxdd, peak - cum)
    wins = [r for r in rs if r > 0]; losses = [r for r in rs if r <= 0]
    return dict(n=len(rs), win=100 * len(wins) / len(rs), avg=sum(rs) / len(rs), total=sum(rs),
                pf=(sum(wins) / abs(sum(losses))) if losses and sum(losses) != 0 else float('inf'),
                maxdd=maxdd)


series = {p: [fn(data['rates'][d]) for d in dates] for p, fn in PAIRS.items()}

for label, kw in [('PRIMARY  Donchian10 / expiry 10 (canonical)', dict(breakout_n=10, expiry=10)),
                  ('VARIANT  Donchian20 / expiry 10', dict(breakout_n=20, expiry=10)),
                  ('VARIANT  Donchian20 / expiry 30', dict(breakout_n=20, expiry=30))]:
    print('=' * 100)
    print(f'CONFIG: {label}   |   floor {FLOOR_SIG} x sigma20, R/R >= {RR_MIN}, cost {COST_PIPS} pips RT')
    print('=' * 100)
    all_trades = {}
    hdr = f"{'pair':9} {'trades':>6} {'win%':>6} {'avgR':>7} {'totR(net)':>10} {'totR(gross)':>11} {'PF':>6} {'maxDD(R)':>9} {'losestrk':>9}"
    print(hdr); print('-' * len(hdr))
    for pair, closes in series.items():
        trades, skips = run_pair(pair, closes, **kw)
        all_trades[pair] = trades
        s = stats(trades)
        bh = (closes[-1] / closes[WARM] - 1) * 100
        if s['n']:
            print(f"{pair:9} {s['n']:>6} {s['win']:>6.1f} {s['avg']:>7.3f} {s['total']:>10.1f} {s['gross']:>11.1f} {s['pf']:>6.2f} {s['maxdd']:>9.1f} {s['worst_streak']:>9}")
        else:
            print(f"{pair:9}      0      -       -          -           -      -        -        -")
        print(f"{'':9} (skips: R/R-gate {skips['rr_gate']}, no-target {skips['no_target']}; buy&hold {bh:+.1f}%)")
    p = portfolio(all_trades)
    per_setup = {}
    for pair in all_trades:
        for t in all_trades[pair]:
            per_setup.setdefault(t['setup'], []).append(t['Rnet'])
    print('-' * len(hdr))
    print(f"PORTFOLIO  {p['n']:>6} {p['win']:>6.1f} {p['avg']:>7.3f} {p['total']:>10.1f} {'':>11} {p['pf']:>6.2f} {p['maxdd']:>9.1f}")
    flat = sorted((t['exit_i'], t['Rnet']) for pair in all_trades for t in all_trades[pair])
    rs = [r for _, r in flat]
    mean = sum(rs) / len(rs); sd = statistics.stdev(rs)
    print(f"   significance: t-stat vs 0 = {mean / (sd / len(rs) ** 0.5):+.2f}  (mean {mean:+.3f}R, sd {sd:.2f}R, n {len(rs)})")
    eras = {}
    for i, r in flat:
        y = int(dates[i][:4]); era = f"{y // 5 * 5}-{y // 5 * 5 + 4}"
        eras.setdefault(era, []).append(r)
    for era in sorted(eras):
        e = eras[era]
        print(f"     {era}: n={len(e):>4}  total={sum(e):+7.1f}R  avg={sum(e) / len(e):+.3f}")
    for setup, rs2 in per_setup.items():
        w = [r for r in rs2 if r > 0]
        print(f"   {setup:9} n={len(rs2):>4}  win={100*len(w)/len(rs2):5.1f}%  avgR={sum(rs2)/len(rs2):+.3f}  total={sum(rs2):+.1f}")
    print()
