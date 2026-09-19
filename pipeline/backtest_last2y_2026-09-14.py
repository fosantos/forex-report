#!/usr/bin/env python3
"""Rolling 2-year window re-validation of the Research Desk canonical swing rules
(Donchian 10 breakout / 10-session expiry / 1.5-sigma20 stop floor / R/R >= 1:2),
run on the same ECB/Frankfurter series and the SAME engine as backtest_strategy.py
(indicators and warm-up identical to the 2000-present canonical run; only the
reporting window changes), per the user request of 14/09/2026: "backtest dos
ultimos 2 anos".

Window: trades ENTERED between 2024-09-14 and 2026-09-14 (both boundaries from the
last available close). Full history is still fetched and simulated so indicator
state, regime and open-position carryover at the window boundary match the
canonical run exactly.

Engine logic mirrored 1:1 from pipeline/backtest_strategy.py (PRIMARY config).
Not modeled (same as canonical): JPY 2.5-sigma intervention floor and the 24h
event filter - live-desk results can differ from this simulation.
Output: console + pipeline/backtest_results_2026-09-14_last2y.txt (via tee).
"""
import urllib.request, json, statistics
from datetime import date

START = '2000-01-01'
END = date.today().isoformat()
WIN_START = '2024-09-14'   # entry-date filter: last 2 years from the last close
PIP = {'EUR/USD': 0.0001, 'USD/JPY': 0.01, 'AUD/USD': 0.0001,
       'GBP/USD': 0.0001, 'EUR/JPY': 0.01, 'GBP/JPY': 0.01}
COST_PIPS = 1.5
FLOOR_SIG = 1.5
RR_MIN = 2.0
WARM = 250
BREAKOUT_N = 10
EXPIRY = 10

req = urllib.request.Request(
    f'https://api.frankfurter.app/{START}..{END}?from=USD&to=EUR,JPY,GBP,AUD',
    headers={'User-Agent': 'Mozilla/5.0 (forex-report)'})
data = json.load(urllib.request.urlopen(req, timeout=180))
dates = sorted(data['rates'].keys())
print(f'Series: {dates[0]} .. {dates[-1]}  ({len(dates)} sessions)')
print(f'Window: entries {WIN_START} .. {dates[-1]}  (last 2 years)\n')

PAIRS = {
    'EUR/USD': lambda r: 1.0 / r['EUR'],
    'USD/JPY': lambda r: r['JPY'],
    'AUD/USD': lambda r: 1.0 / r['AUD'],
    'GBP/USD': lambda r: 1.0 / r['GBP'],
    'EUR/JPY': lambda r: r['JPY'] / r['EUR'],
    'GBP/JPY': lambda r: r['JPY'] / r['GBP'],
}


def run_pair(pair, closes, breakout_n=BREAKOUT_N, expiry=EXPIRY):
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


def outcome(t):
    if t['R'] == t['plannedR']:
        return 'target'
    if t['R'] == -1.0:
        return 'stop'
    return 'expired'


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


series = {p: [fn(data['rates'][d]) for d in dates] for p, fn in PAIRS.items()}
w_start_i = next(i for i, d in enumerate(dates) if d >= WIN_START)
w_end_i = len(dates) - 1

print('=' * 108)
print(f'CONFIG: PRIMARY  Donchian{BREAKOUT_N} / expiry {EXPIRY} (canonical)   |   floor {FLOOR_SIG} x sigma20, '
      f'R/R >= {RR_MIN}, cost {COST_PIPS} pips RT   |   WINDOW: last 2 years (entries {WIN_START}..{dates[-1]})')
print('=' * 108)

all_trades = {}
hdr = f"{'pair':9} {'trades':>6} {'win%':>6} {'avgR':>7} {'totR(net)':>10} {'totR(gross)':>11} {'PF':>6} {'maxDD(R)':>9} {'losestrk':>9}"
print(hdr); print('-' * len(hdr))
for pair, closes in series.items():
    trades, skips = run_pair(pair, closes)
    w = [t for t in trades if dates[t['entry_i']] >= WIN_START]
    all_trades[pair] = w
    s = stats(w)
    bh = (closes[w_end_i] / closes[w_start_i] - 1) * 100
    if s['n']:
        print(f"{pair:9} {s['n']:>6} {s['win']:>6.1f} {s['avg']:>7.3f} {s['total']:>10.1f} {s['gross']:>11.1f} {s['pf']:>6.2f} {s['maxdd']:>9.1f} {s['worst_streak']:>9}")
    else:
        print(f"{pair:9}      0      -       -          -           -      -        -        -")
    print(f"{'':9} (skips in window: R/R-gate {skips['rr_gate']}, no-target {skips['no_target']}; buy&hold 2y {bh:+.1f}%)")

# ---- portfolio (by exit order) ----
flat = sorted((t['exit_i'], t['Rnet'], pair, t) for pair in all_trades for t in all_trades[pair])
cum = 0.0; peak = 0.0; maxdd = 0.0
rs = []
for _, r, _p, _t in flat:
    cum += r; rs.append(r)
    peak = max(peak, cum); maxdd = max(maxdd, peak - cum)
wins = [r for r in rs if r > 0]; losses = [r for r in rs if r <= 0]
p = dict(n=len(rs), win=100 * len(wins) / len(rs), avg=sum(rs) / len(rs), total=sum(rs),
         pf=(sum(wins) / abs(sum(losses))) if losses and sum(losses) != 0 else float('inf'), maxdd=maxdd)
print('-' * len(hdr))
print(f"PORTFOLIO  {p['n']:>6} {p['win']:>6.1f} {p['avg']:>7.3f} {p['total']:>10.1f} {'':>11} {p['pf']:>6.2f} {p['maxdd']:>9.1f}")
mean = sum(rs) / len(rs); sd = statistics.stdev(rs)
print(f"   significance: t-stat vs 0 = {mean / (sd / len(rs) ** 0.5):+.2f}  (mean {mean:+.3f}R, sd {sd:.2f}R, n {len(rs)})")

# ---- outcome + setup breakdown ----
cats = {}
for _, _r, _pr, t in flat:
    cats.setdefault(outcome(t), []).append(t['Rnet'])
for cat in ('target', 'stop', 'expired'):
    if cat in cats:
        v = cats[cat]
        print(f"   {cat:8} n={len(v):>3}  avgR={sum(v)/len(v):+.3f}  total={sum(v):+.1f}")
per_setup = {}
for _, _r, _p, t in flat:
    per_setup.setdefault(t['setup'], []).append(t['Rnet'])
for setup, rs2 in per_setup.items():
    w2 = [r for r in rs2 if r > 0]
    print(f"   {setup:9} n={len(rs2):>3}  win={100*len(w2)/len(rs2):5.1f}%  avgR={sum(rs2)/len(rs2):+.3f}  total={sum(rs2):+.1f}")

# ---- quarterly buckets (by exit) ----
qmap = {}
for ex_i, r, _p, _t in flat:
    y, m = dates[ex_i][:4], int(dates[ex_i][5:7])
    q = f"{y}-Q{(m - 1) // 3 + 1}"
    qmap.setdefault(q, []).append(r)
print('\n   quarterly (by exit):')
for q in sorted(qmap):
    e = qmap[q]
    bar = '#' * max(1, round(sum(e)))
    print(f"     {q}: n={len(e):>2}  total={sum(e):+6.1f}R  avg={sum(e)/len(e):+.3f}  {bar}")

# ---- full trade list ----
print('\n   trade log (entry -> exit, close-based):')
print(f"   {'pair':9} {'dir':6} {'setup':9} {'entry date':11} {'exit date':11} {'outcome':8} {'planR':>6} {'Rnet':>7}")
for ex_i, r, pair, t in flat:
    print(f"   {pair:9} {t['dir']:6} {t['setup']:9} {dates[t['entry_i']]} {dates[ex_i]}  {outcome(t):8} {t['plannedR']:>6.2f} {r:>+7.2f}")

print(f"\nBASELINE COMPARISON (canonical 2000-2026, pipeline/backtest_results_2026-08-17.txt):")
print("   821 trades, +100.8R net, PF 1.31, t +3.24, avg +0.123R/trade, maxDD 14.4R, win 50.2%")
print("   (2y window: JPY 2.5-sigma intervention floor and 24h event filter still NOT modeled)")
