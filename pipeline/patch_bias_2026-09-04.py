#!/usr/bin/env python3
"""Patch for the 04/09/2026 edition: bias-class swaps on the 4 pages whose SMA alignment
changed (USD/JPY bull->neutral, GBP/USD neutral->bull, EUR/JPY bull->neutral, GBP/JPY bull->neutral)
and the AUD/USD conviction score fix (9/10 -> 7/10 per the round(R*3) convention)."""
import sys

DOCS = r"C:/Projetos/forex-report/docs"

def rep(text, old, new, label, count=1):
    n = text.count(old)
    if n != count:
        print(f"FAIL [{label}]: expected {count} occurrence(s), found {n}")
        sys.exit(1)
    return text.replace(old, new)

# pair -> (file, old bias, new bias, old EN text, new EN text, old PT text, new PT text)
SWAPS = [
    ("usd-jpy.html",  "bull",    "neutral", "USD/JPY - BULLISH", "USD/JPY - NEUTRAL", "USD/JPY - ALTA",   "USD/JPY - NEUTRO"),
    ("gbp-usd.html",  "neutral", "bull",    "GBP/USD - NEUTRAL", "GBP/USD - BULLISH", "GBP/USD - NEUTRO", "GBP/USD - ALTA"),
    ("eur-jpy.html",  "bull",    "neutral", "EUR/JPY - BULLISH", "EUR/JPY - NEUTRAL", "EUR/JPY - ALTA",   "EUR/JPY - NEUTRO"),
    ("gbp-jpy.html",  "bull",    "neutral", "GBP/JPY - BULLISH", "GBP/JPY - NEUTRAL", "GBP/JPY - ALTA",   "GBP/JPY - NEUTRO"),
]

for fname, old_b, new_b, old_en, new_en, old_pt, new_pt in SWAPS:
    p = f"{DOCS}/{fname}"
    h = open(p, encoding="utf-8").read()
    h = rep(h, f'class="report-container bias-{old_b}"', f'class="report-container bias-{new_b}"', f"{fname} container")
    h = rep(h, f'bias-badge bias-{old_b}"', f'bias-badge bias-{new_b}"', f"{fname} badge cls")
    h = rep(h, f'<span class="lang-en">{old_en}</span>', f'<span class="lang-en">{new_en}</span>', f"{fname} badge en")
    h = rep(h, f'<span class="lang-pt" style="display:none;">{old_pt}</span>', f'<span class="lang-pt" style="display:none;">{new_pt}</span>', f"{fname} badge pt")
    open(p, "w", encoding="utf-8").write(h)
    print(f"OK: {fname} bias {old_b} -> {new_b}")

# AUD/USD conviction: 9/10 t-high (8 bars) -> 7/10 default (7 bars)
p = f"{DOCS}/aud-usd.html"
h = open(p, encoding="utf-8").read()
h = rep(h, '<span class="conv-tier t-high">9/10', '<span class="conv-tier ">7/10', "aud tier")
h = rep(h, '<div class="conv-bar"><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i></i><i></i></div>',
            '<div class="conv-bar"><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i></i><i></i><i></i></div>', "aud bar")
open(p, "w", encoding="utf-8").write(h)
print("OK: aud-usd.html conviction 9/10 -> 7/10")
