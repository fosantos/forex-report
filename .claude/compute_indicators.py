import urllib.request, json, sys, statistics
from datetime import date, datetime

# Fetch daily series from 2024-08-01 through the last completed D1 bar.
# Primary source: MetaTrader 5 terminal (D1 closes). Fallback: Frankfurter/ECB API.
START = date(2024, 8, 1)

MT5_SYMBOLS = {
    'EUR/USD': 'EURUSD',
    'USD/JPY': 'USDJPY',
    'AUD/USD': 'AUDUSD',
    'GBP/USD': 'GBPUSD',
    'EUR/JPY': 'EURJPY',
    'GBP/JPY': 'GBPJPY',
}

def fetch_from_mt5():
    import MetaTrader5 as mt5
    if not mt5.initialize():
        raise RuntimeError(f'MT5 initialize failed: {mt5.last_error()}')
    try:
        today = datetime.now().date()
        series, dates, quotes = {}, [], {}
        for pair, sym in MT5_SYMBOLS.items():
            rates = mt5.copy_rates_range(sym, mt5.TIMEFRAME_D1, datetime.combine(START, datetime.min.time()),
                                         datetime.combine(today, datetime.min.time()))
            if rates is None or len(rates) == 0:
                raise RuntimeError(f'MT5 copy_rates_range failed for {sym}: {mt5.last_error()}')
            # Drop the still-forming D1 candle: indicators are close-based on completed sessions
            bars = [r for r in rates if datetime.fromtimestamp(r['time']).date() < today]
            if pair == 'EUR/USD':
                dates = [datetime.fromtimestamp(r['time']).date().isoformat() for r in bars]
            series[pair] = [float(r['close']) for r in bars]
            tick = mt5.symbol_info_tick(sym)
            quotes[pair] = (tick.bid + tick.ask) / 2 if tick else None
    finally:
        mt5.shutdown()
    return dates, series, quotes

def fetch_from_frankfurter():
    req = urllib.request.Request(
        f"https://frankfurter.app/{START.isoformat()}..{date.today().isoformat()}?from=USD&to=EUR,JPY,GBP,AUD",
        headers={'User-Agent': 'Mozilla/5.0 (forex-report)'}
    )
    resp = urllib.request.urlopen(req, timeout=60)
    data = json.load(resp)
    dates = sorted(data['rates'].keys())
    pairs_def = {
        'EUR/USD': lambda r: 1.0 / r['EUR'],
        'USD/JPY': lambda r: r['JPY'],
        'AUD/USD': lambda r: 1.0 / r['AUD'],
        'GBP/USD': lambda r: 1.0 / r['GBP'],
        'EUR/JPY': lambda r: r['JPY'] / r['EUR'],
        'GBP/JPY': lambda r: r['JPY'] / r['GBP'],
    }
    series = {pair: [fn(data['rates'][d]) for d in dates] for pair, fn in pairs_def.items()}
    return dates, series, {}

try:
    dates, series, live_quotes = fetch_from_mt5()
    source = 'MetaTrader 5 terminal (D1 closes)'
except Exception as e:
    print(f'MT5 fetch failed ({e}); falling back to Frankfurter/ECB API', file=sys.stderr)
    dates, series, live_quotes = fetch_from_frankfurter()
    source = 'Frankfurter/ECB daily reference rates'

print(f'Data source: {source}')
print(f'Total trading days: {len(dates)}')
print(f'First date: {dates[0]}')
print(f'Last date: {dates[-1]}')
if live_quotes:
    print('Live MT5 mid quotes:')
    for pair, q in live_quotes.items():
        print(f'  {pair}: {q:.5f}' if q is not None else f'  {pair}: n/a')

def sma(closes, n):
    if len(closes) < n:
        return None
    return sum(closes[-n:]) / n

def sigma20(closes):
    """Std-dev of the last 20 daily % changes -> (pct, price distance)."""
    if len(closes) < 21:
        return None, None
    rets = [(closes[i] / closes[i-1] - 1.0) * 100 for i in range(len(closes)-20, len(closes))]
    sd_pct = statistics.stdev(rets)
    return sd_pct, sd_pct / 100.0 * closes[-1]

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
results = {}
for pair, closes in series.items():
    last = closes[-1]
    prev = closes[-2]
    daily_pct = (last - prev) / prev * 100
    sma50 = sma(closes, 50)
    sma200 = sma(closes, 200)

    # Volatility: sigma20 (close-to-close), also in pips
    sd_pct, sd_dist = sigma20(closes)
    pip = 0.01 if '/JPY' in pair else 0.0001
    sd_pips = sd_dist / pip

    # Donchian channels on closes (forward trigger reference: includes the last close)
    don10_hi, don10_lo = max(closes[-10:]), min(closes[-10:])
    don20_hi, don20_lo = max(closes[-20:]), min(closes[-20:])

    # 9-month swing: ~ last 195 trading days.
    window = closes[-195:]
    swing_high_idx = window.index(max(window))
    swing_low_idx = window.index(min(window))
    swing_high = max(window)
    swing_low = min(window)
    high_first = swing_high_idx < swing_low_idx

    fibs = fib_levels(swing_high, swing_low)

    # Bias by SMA alignment (rule 2 of the forex-report agent)
    if last > sma200 and sma50 > sma200:
        alignment = 'BULL-ALIGNED'
    elif last < sma200 and sma50 < sma200:
        alignment = 'BEAR-ALIGNED'
    else:
        alignment = 'MIXED (default WAIT unless a confirmed breakout resolves it)'

    print(f'\n--- {pair} ---')
    print(f'  Last close ({dates[-1]}): {last:.5f}')
    print(f'  Prev close ({dates[-2]}): {prev:.5f}')
    print(f'  Daily % change: {daily_pct:+.3f}%')
    print(f'  SMA50:  {sma50:.5f}')
    print(f'  SMA200: {sma200:.5f}')
    print(f'  Price vs SMA50: {"above" if last>sma50 else "below"}')
    print(f'  Price vs SMA200: {"above" if last>sma200 else "below"}')
    print(f'  Bias (alignment): {alignment}')
    print(f'  sigma20: {sd_pct:.3f}% = {sd_dist:.5f} = {sd_pips:.0f} pips  -> stop floor 1.5s = {1.5*sd_pips:.0f} pips, 2.5s = {2.5*sd_pips:.0f} pips')
    print(f'  Donchian 10d hi/lo (breakout trigger): {don10_hi:.5f} / {don10_lo:.5f}')
    print(f'  Donchian 20d hi/lo (anchor): {don20_hi:.5f} / {don20_lo:.5f}')
    print(f'  9-mo window swing high: {swing_high:.5f} (idx {swing_high_idx} of {len(window)})')
    print(f'  9-mo window swing low:  {swing_low:.5f} (idx {swing_low_idx} of {len(window)})')
    print(f'  High-first (downtrend leg): {high_first}')
    print(f'  Fibonacci (from {swing_low:.5f} to {swing_high:.5f}) — confluence only:')
    for k, v in fibs.items():
        print(f'    {k}: {v:.5f}')
    results[pair] = dict(last=last, prev=prev, daily_pct=daily_pct, sma50=sma50, sma200=sma200,
                         sigma20_pct=sd_pct, sigma20_dist=sd_dist, sigma20_pips=sd_pips,
                         don10_hi=don10_hi, don10_lo=don10_lo, don20_hi=don20_hi, don20_lo=don20_lo,
                         swing_high=swing_high, swing_low=swing_low, fibs=fibs,
                         alignment=alignment, swing_high_idx=swing_high_idx, swing_low_idx=swing_low_idx)

# Print last 10 closes per pair
print('\n' + '='*70)
print('LAST 10 DAILY CLOSES PER PAIR:')
for pair, closes in series.items():
    print(f'\n{pair}:')
    for d, c in zip(dates[-10:], closes[-10:]):
        print(f'  {d}: {c:.5f}')

# Emit machine-readable JSON for downstream
print('\n' + '='*70)
print('RESULTS_JSON_START')
print(json.dumps({'source': source, 'dates': dates, 'n_sessions': len(dates), 'live_quotes': live_quotes, 'results': results}, default=str))
print('RESULTS_JSON_END')
