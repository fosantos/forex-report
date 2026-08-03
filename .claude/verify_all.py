#!/usr/bin/env python3
"""Comprehensive verification of both representations against the rules."""
import json, re, sys

INDEX = r"C:/Projetos/forex-report/docs/index.html"
DOCS = r"C:/Projetos/forex-report/docs"
PAGE = {
    "EUR/USD": "eur-usd.html", "USD/JPY": "usd-jpy.html", "AUD/USD": "aud-usd.html",
    "GBP/USD": "gbp-usd.html", "EUR/JPY": "eur-jpy.html", "GBP/JPY": "gbp-jpy.html",
}
errors = []

with open(INDEX, encoding="utf-8") as f:
    idx = f.read()
s = idx.find("const forexData = {"); s2 = idx.find("{", s)
e = idx.find("\n};", s) + len("\n};")
data = json.loads(idx[s2:e][:-1].rstrip())

def parse_level(str_):
    m = re.sub(r",(\d)", r".\1", str(str_))
    m = re.search(r"-?\d+\.?\d*", m)
    return float(m.group(0)) if m else None

def verdict_class(rec):
    if "WAIT" in rec: return "wait"
    if "SELL" in rec: return "sell"
    return "buy"

# ---- 1. index.html checks ----
# timestamps
if idx.count("03/08/2026 13:30 UTC") != 3:
    errors.append(f"index.html: expected 3 timestamps, found {idx.count('03/08/2026 13:30 UTC')}")
if "02/08/2026" in idx:
    errors.append("index.html: stale 02/08/2026 present")
# ticker changes present
for pair, pct in [("EUR/USD","+0.44%"),("USD/JPY","-2.22%"),("AUD/USD","-0.16%"),
                  ("GBP/USD","+0.36%"),("EUR/JPY","-1.80%"),("GBP/JPY","-1.87%")]:
    if f'"{pair}": "{pct}"' not in idx:
        errors.append(f"index.html ticker: {pair} {pct} missing")
# pair order
order = list(data.keys())
if order != list(PAGE.keys()):
    errors.append(f"index.html: pair order {order}")
# rrValue = round(R*25)
for pair, d in data.items():
    rr = d["en"]["rr"]; rv = d["en"]["rrValue"]
    R = float(re.match(r"1:([0-9.]+)", rr).group(1))
    if round(R*25) != rv:
        errors.append(f"{pair}: rrValue {rv} != round({R}*25)={round(R*25)}")
    if R < 2:
        errors.append(f"{pair}: R/R {rr} below 1:2 gate")

print("== index.html checks done ==")

# ---- 2. static page checks ----
for pair, fname in PAGE.items():
    d = data[pair]
    path = DOCS + "\\" + fname
    with open(path, encoding="utf-8") as f:
        html = f.read()
    # structural integrity
    if html.count("<article ") != 1:
        errors.append(f"{fname}: {html.count('<article ')} articles")
    if "</article>" not in html:
        errors.append(f"{fname}: no </article>")
    if "</footer>" not in html or "</body>" not in html:
        errors.append(f"{fname}: footer/body missing")
    if "compliance-container" not in html:
        errors.append(f"{fname}: educational section missing")
    if "03/08/2026" not in html:
        errors.append(f"{fname}: today date missing")
    if "02/08/2026" in html:
        errors.append(f"{fname}: stale 02/08/2026")
    # quote
    if f"<strong>{d['quote']}</strong>" not in html:
        errors.append(f"{fname}: quote {d['quote']} not found in <strong>")
    # bias class on article
    if f'class="report-container bias-{d["biasType"]}"' not in html:
        errors.append(f"{fname}: report-container bias-{d['biasType']} missing")
    # verdict class
    vc = verdict_class(d["en"]["recommendation"])
    if f"verdict-card verdict-{vc}" not in html:
        errors.append(f"{fname}: verdict-card verdict-{vc} missing")
    if f'verdict-badge {vc}"' not in html:
        errors.append(f"{fname}: verdict-badge {vc} missing")
    # rr-seal and ratio bar
    if d["en"]["rr"] not in html:
        errors.append(f"{fname}: rr {d['en']['rr']} missing")
    # rr-seal appears at least once; ratio-bar-fill width
    if f"width: {d['en']['rrValue']}%;" not in html:
        errors.append(f"{fname}: ratio-bar-fill width {d['en']['rrValue']}% missing")
    # gauge
    q = parse_level(d["quote"]); sup = parse_level(d["en"]["support"]); res = parse_level(d["en"]["resistance"])
    pct = max(0, min(100, (q - sup) / (res - sup) * 100))
    g = round(pct)
    if f"left: {g}%;" not in html:
        errors.append(f"{fname}: gauge left:{g}% missing (computed {pct:.2f})")
    # lang presence: each dynamic value should appear (en is visible, pt hidden)
    for lang in ["en", "pt"]:
        for fld in ["fundamental","trend","support","resistance","priceAction","trigger","stop","target","justification"]:
            val = d[lang][fld]
            if val not in html:
                errors.append(f"{fname}: {lang}.{fld} value not found in page")
    # recommendation strings (both langs)
    if d["en"]["recommendation"] not in html:
        errors.append(f"{fname}: EN recommendation missing")
    if d["pt"]["recommendation"] not in html:
        errors.append(f"{fname}: PT recommendation missing")
    # bias badge text
    bias_txt = {"bear":("BEARISH","BAIXA"),"bull":("BULLISH","ALTA")}[d["biasType"]]
    if f"{pair} - {bias_txt[0]}" not in html:
        errors.append(f"{fname}: EN bias badge text missing")
    if f"{pair} - {bias_txt[1]}" not in html:
        errors.append(f"{fname}: PT bias badge text missing")
    print(f"  {fname}: OK (bias={d['biasType']} verdict={vc} gauge={g}% rrBar={d['en']['rrValue']}%)")

print("\n== static page checks done ==")
if errors:
    print(f"\nFAILED with {len(errors)} error(s):")
    for er in errors:
        print("  -", er)
    sys.exit(1)
print("\nALL CHECKS PASSED: both representations in sync, all rules satisfied.")
