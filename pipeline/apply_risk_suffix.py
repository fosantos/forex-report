#!/usr/bin/env python3
"""One-shot (17/08/2026): apply the fixed risk-sizing suffix to every directional stop field
(5 pairs x PT/EN, in docs/index.html forexData AND the static pair pages) and add the missing
VENDA (SHORT) NO ROMPIMENTO / SELL (SHORT) ON BREAKOUT keys to both i18n dictionaries.
Aborts on any non-unique or missing match. EUR/JPY is WAIT (N/A stop) — exempt."""
import sys

DOCS = r"C:/Projetos/forex-report/docs"

SUF_PT = " · risco sugerido ≤ 1% por operação."
SUF_EN = " · suggested risk ≤ 1% per trade."

# pair -> (pt_stop, en_stop, static_page)
STOPS = {
    "EUR/USD": ("1,1740 (Acima da Fib 38,2% em 1,1732).", "1.1740 (Above the 38.2% Fib at 1.1732).", "eur-usd.html"),
    "USD/JPY": ("156,80 (Abaixo da Fib 61,8% em 156,94).", "156.80 (Below the 61.8% Fib at 156.94).", "usd-jpy.html"),
    "AUD/USD": ("0,6890 (Abaixo da SMA200 de 0,6925).", "0.6890 (Below the 0.6925 200-day SMA).", "aud-usd.html"),
    "GBP/USD": ("1,3340 (Abaixo da Fib 61,8% em 1,3350).", "1.3340 (Below the 61.8% Fib at 1.3350).", "gbp-usd.html"),
    "GBP/JPY": ("213,90 (Abaixo da Fib 23,6% em 214,83).", "213.90 (Below the 23.6% Fib at 214.83).", "gbp-jpy.html"),
}

def replace_exact(text, old, new, where):
    n = text.count(old)
    if n != 1:
        sys.exit(f"ERROR [{where}]: expected exactly 1 occurrence, found {n}: {old}")
    return text.replace(old, new)

def suffix(stop_old, suf):
    return stop_old[:-1] + suf  # swap final period for suffix + period

# 1) static pages: this pair's 2 stop strings
for pair, (pt_old, en_old, page) in STOPS.items():
    path = DOCS + "/" + page
    with open(path, encoding="utf-8") as f:
        html = f.read()
    html = replace_exact(html, pt_old, suffix(pt_old, SUF_PT), f"{page} {pair} PT stop")
    html = replace_exact(html, en_old, suffix(en_old, SUF_EN), f"{page} {pair} EN stop")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"OK: {page} — {pair} stop suffixes (PT+EN)")

# 2) docs/index.html: all 10 stop strings + 2 i18n keys
idx_path = DOCS + "/index.html"
with open(idx_path, encoding="utf-8") as f:
    idx = f.read()
for pair, (pt_old, en_old, _) in STOPS.items():
    idx = replace_exact(idx, pt_old, suffix(pt_old, SUF_PT), f"index.html {pair} PT stop")
    idx = replace_exact(idx, en_old, suffix(en_old, SUF_EN), f"index.html {pair} EN stop")

key_anchor_en = '"VENDA (SHORT) NA RETRAÇÃO": "SELL (SHORT) ON PULLBACK",'
key_new_en = '"VENDA (SHORT) NO ROMPIMENTO": "SELL (SHORT) ON BREAKOUT",'
key_anchor_pt = '"VENDA (SHORT) NA RETRAÇÃO": "VENDA (SHORT) NA RETRAÇÃO",'
key_new_pt = '"VENDA (SHORT) NO ROMPIMENTO": "VENDA (SHORT) NO ROMPIMENTO",'
idx = replace_exact(idx, key_anchor_en, key_anchor_en + "\n                " + key_new_en, "index.html EN i18n")
idx = replace_exact(idx, key_anchor_pt, key_anchor_pt + "\n                " + key_new_pt, "index.html PT i18n")
with open(idx_path, "w", encoding="utf-8") as f:
    f.write(idx)
print(f"OK: index.html — 10 stop suffixes + 2 i18n keys")

print("DONE: all directional tickets now carry the risk-sizing suffix.")
