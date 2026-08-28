#!/usr/bin/env python3
"""Comprehensive verification of both representations against the rules."""
import json, re, sys

INDEX = r"C:/Projetos/forex-report/docs/index.html"
DOCS = r"C:/Projetos/forex-report/docs"
PAGE = {
    "EUR/USD": "eur-usd.html", "USD/JPY": "usd-jpy.html", "AUD/USD": "aud-usd.html",
    "GBP/USD": "gbp-usd.html", "EUR/JPY": "eur-jpy.html", "GBP/JPY": "gbp-jpy.html",
}
TODAY_TS = "28/08/2026 22:05 UTC"
TODAY_DATE = "28/08/2026"
STALE_DATES = ["24/08/2026", "20/08/2026", "19/08/2026", "18/08/2026", "17/08/2026", "14/08/2026", "13/08/2026", "11/08/2026", "03/08/2026", "02/08/2026"]
TICKER = [("EUR/USD","-0.02%"),("USD/JPY","+0.18%"),("AUD/USD","+0.07%"),
          ("GBP/USD","+0.01%"),("EUR/JPY","+0.16%"),("GBP/JPY","+0.19%")]
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
    if "WAIT" in rec or "AGUARDAR" in rec: return "wait"
    if "SELL" in rec or "VENDA" in rec: return "sell"
    return "buy"

# ---- 1. index.html checks ----
if idx.count(TODAY_TS) != 3:
    errors.append(f"index.html: expected 3 timestamps '{TODAY_TS}', found {idx.count(TODAY_TS)}")
for stale in STALE_DATES:
    # stale dates may legitimately appear inside macro narrative (e.g. "July 29") only as DD/MM;
    # only flag a stale date if it appears with the year-suffix that marks a report session date
    if stale in idx:
        errors.append(f"index.html: stale session date {stale} present")
for pair, pct in TICKER:
    if f'"{pair}": "{pct}"' not in idx:
        errors.append(f"index.html ticker: {pair} {pct} missing")
order = list(data.keys())
if order != list(PAGE.keys()):
    errors.append(f"index.html: pair order {order}")
for pair, d in data.items():
    rr = d["en"]["rr"]; rv = d["en"]["rrValue"]
    if rr == "N/A":
        if rv != 0:
            errors.append(f"{pair}: N/A but rrValue={rv}")
        if "WAIT" not in d["en"]["recommendation"]:
            errors.append(f"{pair}: N/A but recommendation not WAIT")
        continue
    mobj = re.match(r"1:([0-9.]+)", rr)
    if not mobj:
        errors.append(f"{pair}: bad rr {rr}")
        continue
    R = float(mobj.group(1))
    if round(R*25) != rv:
        errors.append(f"{pair}: rrValue {rv} != round({R}*25)={round(R*25)}")
    if R < 2:
        errors.append(f"{pair}: R/R {rr} below 1:2 gate")
    # PT/EN rr + rrValue must match
    if d["pt"]["rr"] != rr or d["pt"]["rrValue"] != rv:
        errors.append(f"{pair}: PT/EN rr mismatch")
    # bias consistency
    expected_bias = {"bull":"ALTA","bear":"BAIXA","neutral":"NEUTRO"}[d["biasType"]]
    if d["bias"] != expected_bias:
        errors.append(f"{pair}: bias {d['bias']} != {expected_bias} for biasType {d['biasType']}")
    # risk-suffix rule: every directional stop carries the fixed sizing note
    if "WAIT" not in d["en"]["recommendation"]:
        if not d["en"]["stop"].endswith("· suggested risk ≤ 1% per trade."):
            errors.append(f"{pair}: EN stop missing '· suggested risk ≤ 1% per trade.' suffix")
        if not d["pt"]["stop"].endswith("· risco sugerido ≤ 1% por operação."):
            errors.append(f"{pair}: PT stop missing '· risco sugerido ≤ 1% por operação.' suffix")

# recommendation i18n helper keys must include the short-breakout pair
if '"VENDA (SHORT) NO ROMPIMENTO": "SELL (SHORT) ON BREAKOUT"' not in idx:
    errors.append("index.html: EN i18n dict missing VENDA (SHORT) NO ROMPIMENTO key")
if '"VENDA (SHORT) NO ROMPIMENTO": "VENDA (SHORT) NO ROMPIMENTO"' not in idx:
    errors.append("index.html: PT i18n dict missing VENDA (SHORT) NO ROMPIMENTO key")

print("== index.html checks done ==")

# ---- 2. static page checks ----
for pair, fname in PAGE.items():
    d = data[pair]
    path = DOCS + "\\" + fname
    with open(path, encoding="utf-8") as f:
        html = f.read()
    if html.count("<article ") != 1:
        errors.append(f"{fname}: {html.count('<article ')} articles")
    if "</article>" not in html:
        errors.append(f"{fname}: no </article>")
    if "</footer>" not in html or "</body>" not in html:
        errors.append(f"{fname}: footer/body missing")
    if "compliance-container" not in html:
        errors.append(f"{fname}: educational section missing")
    if TODAY_DATE not in html:
        errors.append(f"{fname}: today date {TODAY_DATE} missing")
    for stale in ["19/08/2026", "18/08/2026", "17/08/2026", "14/08/2026", "13/08/2026"]:
        if stale in html:
            errors.append(f"{fname}: stale session date {stale}")
    if f"<strong>{d['quote']}</strong>" not in html:
        errors.append(f"{fname}: quote {d['quote']} not found in <strong>")
    if f'class="report-container bias-{d["biasType"]}"' not in html:
        errors.append(f"{fname}: report-container bias-{d['biasType']} missing")
    vc = verdict_class(d["en"]["recommendation"])
    if f"trade-ticket verdict-{vc}" not in html:
        errors.append(f"{fname}: trade-ticket verdict-{vc} missing")
    if f'verdict-badge {vc}"' not in html:
        errors.append(f"{fname}: verdict-badge {vc} missing")
    if d["en"]["rr"] not in html:
        errors.append(f"{fname}: rr {d['en']['rr']} missing")
    # Research-Desk design renders R/R via conviction score (score/10), derived from rr; not a width bar
    if d["en"]["rr"] == "N/A":
        if "0/10" not in html:
            errors.append(f"{fname}: N/A conviction score 0/10 missing")
    else:
        R = float(re.match(r"1:([0-9.]+)", d["en"]["rr"]).group(1))
        score = round(min(10, max(3, R * 3)))
        if f"{score}/10" not in html:
            errors.append(f"{fname}: conviction score {score}/10 missing (R={R})")
    q = parse_level(d["quote"]); sup = parse_level(d["en"]["support"]); res = parse_level(d["en"]["resistance"])
    if sup is not None and res is not None and res != sup:
        pct = max(0, min(100, (q - sup) / (res - sup) * 100))
        g = round(pct)
        if f"left: {g}%;" not in html:
            errors.append(f"{fname}: gauge left:{g}% missing (computed {pct:.2f})")
    for lang in ["en", "pt"]:
        for fld in ["fundamental","trend","support","resistance","priceAction","trigger","stop","target","justification"]:
            val = d[lang][fld]
            if val not in html:
                errors.append(f"{fname}: {lang}.{fld} value not found in page")
    if d["en"]["recommendation"] not in html:
        errors.append(f"{fname}: EN recommendation missing")
    if d["pt"]["recommendation"] not in html:
        errors.append(f"{fname}: PT recommendation missing")
    bias_txt = {"bear":("BEARISH","BAIXA"),"bull":("BULLISH","ALTA"),"neutral":("NEUTRAL","NEUTRO")}[d["biasType"]]
    if f"{pair} - {bias_txt[0]}" not in html:
        errors.append(f"{fname}: EN bias badge text missing")
    if f"{pair} - {bias_txt[1]}" not in html:
        errors.append(f"{fname}: PT bias badge text missing")
    print(f"  {fname}: OK (bias={d['biasType']} verdict={vc} gauge={g if (sup and res and res!=sup) else 'N/A'}% rrBar={d['en']['rrValue']}%)")

print("\n== static page checks done ==")

# ---- 3. track-record ledger checks ----
LEDGER = DOCS + "\\track-record.json"
try:
    with open(LEDGER, encoding="utf-8") as f:
        ledger = json.load(f)
    for key in ("meta", "watching", "open", "closed"):
        if key not in ledger:
            errors.append(f"track-record.json: missing '{key}' section")
    seen_pairs = []
    for t in ledger.get("watching", []):
        for fld in ("pair", "reportDate", "direction", "stop", "target", "plannedR", "triggerRule"):
            if fld not in t:
                errors.append(f"track-record.json watching: missing '{fld}' in {t.get('pair', '?')}")
        if t.get("pair") not in PAGE:
            errors.append(f"track-record.json: unknown pair {t.get('pair')}")
        elif t["pair"] in seen_pairs:
            errors.append(f"track-record.json: more than one watching ticket for {t['pair']}")
        seen_pairs.append(t.get("pair"))
    for t in ledger.get("open", []):
        for fld in ("pair", "reportDate", "direction", "entry", "entryDate", "stop", "target", "plannedR"):
            if fld not in t:
                errors.append(f"track-record.json open: missing '{fld}' in {t.get('pair', '?')}")
    for t in ledger.get("closed", []):
        for fld in ("pair", "direction", "entry", "entryDate", "exit", "exitDate", "outcome", "realizedR"):
            if fld not in t:
                errors.append(f"track-record.json closed: missing '{fld}' in {t.get('pair', '?')}")
    print("== track-record ledger checks done ==")
except FileNotFoundError:
    errors.append("track-record.json not found")
except json.JSONDecodeError as ex:
    errors.append(f"track-record.json: invalid JSON: {ex}")

if errors:
    print(f"\nFAILED with {len(errors)} error(s):")
    for er in errors:
        print("  -", er)
    sys.exit(1)
print("\nALL CHECKS PASSED: both representations in sync, all rules satisfied.")
