import urllib.request, json, sys
from datetime import datetime

req = urllib.request.Request(
    'https://api.frankfurter.app/2024-08-01..2026-08-03?from=USD&to=EUR,JPY,GBP,AUD',
    headers={'User-Agent': 'Mozilla/5.0 (forex-report)'}
)
resp = urllib.request.urlopen(req, timeout=60)
data = json.load(resp)

dates = sorted(data['rates'].keys())
print(f'Total trading days: {len(dates)}')
print(f'First date: {dates[0]}')
print(f'Last date: {dates[-1]}')

# Build per-pair close series
pairs_def = {
    'EUR/USD': lambda r: 1.0 / r['EUR'],
    'USD/JPY': lambda r: r['JPY'],
    'AUD/USD': lambda r: 1.0 / r['AUD'],
    'GBP/USD': lambda r: 1.0 / r['GBP'],
    'EUR/JPY': lambda r: r['JPY'] / r['EUR'],
    'GBP/JPY': lambda r: r['JPY'] / r['GBP'],
}

series = {}
for pair, fn in pairs_def.items():
    closes = [fn(data['rates'][d]) for d in dates]
    series[pair] = closes

def sma(closes, n):
    if len(closes) < n:
        return None
    return sum(closes[-n:]) / n

def fib_levels(swing_high, swing_low):
    diff = swing_high - swing_low
    return {
        '0.0': swing_low,
        '0.236': swing_high - 0.236*diff,
        '0.382': swing_high - 0.382*diff,
        '0.500': swing_high - 0.500*diff,
        '0.618': swing_high - 0.618*diff,
        '0.786': swing_high - 0.786*diff,
        '1.0': swing_high,
    }

print('\n' + '='*70)
for pair, closes in series.items():
    last = closes[-1]
    prev = closes[-2]
    daily_pct = (last - prev) / prev * 100
    sma50 = sma(closes, 50)
    sma200 = sma(closes, 200)

    # 9-month swing: ~ last 195 trading days. Find swing high and low over that window.
    window = closes[-195:]
    # For proper swing high/low identification, look at the full window range
    swing_high_idx = window.index(max(window))
    swing_low_idx = window.index(min(window))
    swing_high = max(window)
    swing_low = min(window)

    # Determine chronological order of swing high and low
    high_first = swing_high_idx < swing_low_idx  # if true, high came before low (downtrend leg)

    fibs = fib_levels(swing_high, swing_low)

    # Bias by 200-SMA
    if last > sma200:
        bias = 'BULLISH (above 200-SMA)'
    else:
        bias = 'BEARISH (below 200-SMA)'

    print(f'\n--- {pair} ---')
    print(f'  Last close ({dates[-1]}): {last:.5f}')
    print(f'  Prev close ({dates[-2]}): {prev:.5f}')
    print(f'  Daily % change: {daily_pct:+.3f}%')
    print(f'  SMA50:  {sma50:.5f}')
    print(f'  SMA200: {sma200:.5f}')
    print(f'  Price vs SMA50: {"above" if last>sma50 else "below"}')
    print(f'  Price vs SMA200: {"above" if last>sma200 else "below"}')
    print(f'  Bias: {bias}')
    print(f'  9-mo window swing high: {swing_high:.5f} (idx {swing_high_idx} of {len(window)})')
    print(f'  9-mo window swing low:  {swing_low:.5f} (idx {swing_low_idx} of {len(window)})')
    print(f'  High-first (downtrend leg): {high_first}')
    print(f'  Fibonacci (from {swing_low:.5f} to {swing_high:.5f}):')
    for k, v in fibs.items():
        print(f'    {k}: {v:.5f}  {"<-- last close near" if abs(v-last)<0.0020*(swing_high-swing_low+0.0001) else ""}')

# Also print last 10 closes for each pair for context
print('\n' + '='*70)
print('LAST 10 DAILY CLOSES PER PAIR:')
for pair, closes in series.items():
    print(f'\n{pair}:')
    for d, c in zip(dates[-10:], closes[-10:]):
        print(f'  {d}: {c:.5f}')
