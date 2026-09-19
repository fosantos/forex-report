#!/usr/bin/env python3
"""Regenerate the <article> block in each static pair page from the validated forexData in index.html,
and refresh the no-JS static fallback report (EUR/USD) inside index.html itself.
Guarantees the static pages match the dashboard representation. Aborts on any structural anomaly."""
import json, re, sys

INDEX = r"C:/Projetos/forex-report/docs/index.html"
DOCS = r"C:/Projetos/forex-report/docs"

PAGE = {
    "EUR/USD": "eur-usd.html",
    "USD/JPY": "usd-jpy.html",
    "AUD/USD": "aud-usd.html",
    "GBP/USD": "gbp-usd.html",
    "EUR/JPY": "eur-jpy.html",
    "GBP/JPY": "gbp-jpy.html",
}
BIAS_TXT = {"bear": ("BEARISH", "BAIXA"), "bull": ("BULLISH", "ALTA"), "neutral": ("NEUTRAL", "NEUTRO")}

# ---- extract forexData JSON from index.html ----
with open(INDEX, encoding="utf-8") as f:
    idx = f.read()
s = idx.find("const forexData = {"); s2 = idx.find("{", s)
e = idx.find("\n};", s) + len("\n};")
data = json.loads(idx[s2:e][:-1].rstrip())

def parse_level(str_):
    m = re.sub(r",(\d)", r".\1", str(str_))
    m = re.search(r"-?\d+\.?\d*", m)
    return float(m.group(0)) if m else None

def verdict_class(rec_en):
    if "WAIT" in rec_en: return "wait"
    if "SELL" in rec_en: return "sell"
    return "buy"

# ---- Macro driver chips — derived from the macroDrivers object in docs/index.html (single source) ----
_mb = re.search(r"const macroDrivers\s*=\s*\{", idx)
assert _mb, "index.html: macroDrivers object not found"
_me = re.search(r"\n\s*\};", idx[_mb.end():])
assert _me, "index.html: macroDrivers closing brace not found"
_mjs = idx[_mb.end() - 1: _mb.end() + _me.end() - 1]
_mjs = re.sub(r"(\w+)\s*:", r'"\1":', _mjs)  # quote bare JS keys for JSON parsing
_macro = json.loads(_mjs)
DRIVERS = {p: (v["en"], v["pt"]) for p, v in _macro.items()}
assert set(DRIVERS) == set(PAGE), "macroDrivers pairs do not match the 6 canonical pairs"

def data_basis(d, lang):
    """Build the data-basis line from the fundamental text itself, so it can never go stale."""
    if lang == "en":
        m = re.search(r"(\d+)\s+sessions,\s*(\d{2}/\d{2}/\d{4})\s+to\s+(\d{2}/\d{2}/\d{4})", d["en"]["fundamental"])
        src = "MetaTrader 5 D1 closes" if "MetaTrader" in d["en"]["fundamental"] else "ECB/Frankfurter reference rates"
        if m:
            return "%s &middot; SMA50/200 &amp; Fibonacci computed &middot; %s daily sessions (%s–%s)." % (src, m.group(1), m.group(2), m.group(3))
        dates = re.findall(r"\d{2}/\d{2}/\d{4}", d["en"]["fundamental"])
        assert dates, "index.html: no session date found in EN fundamental"
        return "%s &middot; SMA50/200 &amp; Fibonacci computed &middot; daily series through %s." % (src, dates[-1])
    m = re.search(r"(\d+)\s+pregões,\s*(\d{2}/\d{2}/\d{4})\s+a\s+(\d{2}/\d{2}/\d{4})", d["pt"]["fundamental"])
    src = "closes D1 do MetaTrader 5" if "MetaTrader" in d["pt"]["fundamental"] else "taxas de referência BCE/Frankfurter"
    if m:
        return "%s &middot; SMA50/200 e Fibonacci calculados &middot; %s pregões (%s a %s)." % (src, m.group(1), m.group(2), m.group(3))
    dates = re.findall(r"\d{2}/\d{2}/\d{4}", d["pt"]["fundamental"])
    assert dates, "index.html: no session date found in PT fundamental"
    return "%s &middot; SMA50/200 e Fibonacci calculados &middot; série diária até %s." % (src, dates[-1])

# ---- Intelligence helpers (conviction, BLUF, level-map SVG) ----
def fmt(v):
    if v is None:
        return "—"
    return ("%.1f" % v) if v >= 100 else ("%.4f" % v)

def conviction(rr):
    if not rr or rr == "N/A":
        return 0, "mod"
    m = re.match(r"1:([0-9.]+)", rr)
    R = float(m.group(1)) if m else 0.0
    score = round(min(10, max(3, R * 3)))
    tier = "high" if score >= 8 else ("good" if score == 7 else "mod")
    return score, tier

def conv_segs_html(score):
    return "".join('<i class="on"></i>' if i <= score else '<i></i>' for i in range(1, 11))

def chips_html(pair):
    en, pt = DRIVERS.get(pair, ([], []))
    out = []
    for e, p in zip(en, pt):
        out.append('<span class="macro-chip lang-en">%s</span><span class="macro-chip lang-pt" style="display:none;">%s</span>' % (e, p))
    return "".join(out)

def bluf_sentence(d, lang):
    det = d["en"]; rec = det["recommendation"].upper()
    entry = parse_level(det["trigger"]); stop = parse_level(det["stop"]); target = parse_level(det["target"])
    is_wait = "WAIT" in rec or "AGUARDAR" in rec
    is_sell = "SELL" in rec or "VENDA" in rec
    cls = "wait" if is_wait else ("sell" if is_sell else "buy")
    if lang == "pt":
        action = "AGUARDAR" if is_wait else ("VENDA" if is_sell else "COMPRA")
    else:
        action = "WAIT" if is_wait else ("SHORT" if is_sell else "LONG")
    if is_wait:
        tail = ""
    else:
        pull = "PULLBACK" in rec or "RETRA" in rec
        if lang == "pt":
            mode = "na retração até" if pull else "no rompimento de"
            tail = '%s <b>%s</b> &middot; stop <b>%s</b> &middot; alvo <b>%s</b> &middot; R/R <b>%s</b>' % (mode, fmt(entry), fmt(stop), fmt(target), det["rr"])
        else:
            mode = "on a pullback to" if pull else "on a breakout to"
            tail = '%s <b>%s</b> &middot; stop <b>%s</b> &middot; target <b>%s</b> &middot; R/R <b>%s</b>' % (mode, fmt(entry), fmt(stop), fmt(target), det["rr"])
    return '<span class="bluf-action %s">%s</span> %s' % (cls, action, tail)

LM_LABELS = {
    "en": {"entry": "Entry", "stop": "Stop", "target": "Target", "support": "Support", "resistance": "Resist", "price": "Price", "head": "Trade level map"},
    "pt": {"entry": "Entrada", "stop": "Stop", "target": "Alvo", "support": "Suporte", "resistance": "Resist.", "price": "Preço", "head": "Mapa de níveis da operação"},
}

def level_map_svg(d, lab):
    det = d["en"]
    price = parse_level(d["quote"]); entry = parse_level(det["trigger"]); stop = parse_level(det["stop"])
    target = parse_level(det["target"]); sup = parse_level(det["support"]); res = parse_level(det["resistance"])
    ticks = [("lm-entry", entry, lab["entry"]), ("lm-stop", stop, lab["stop"]),
             ("lm-target", target, lab["target"]), ("lm-sup", sup, lab["support"]),
             ("lm-res", res, lab["resistance"])]
    ticks = [t for t in ticks if t[1] is not None]
    if price is None or len(ticks) < 2:
        return ""
    vals = [t[1] for t in ticks] + [price]
    lo = min(vals); hi = max(vals)
    if hi == lo:
        hi = lo + 1
    pad = (hi - lo) * 0.06; lo -= pad; hi += pad
    W = 320; M = 16; AX = 50
    xp = lambda p: M + (p - lo) / (hi - lo) * (W - 2 * M)
    sorted_ticks = sorted(ticks, key=lambda t: t[1])
    svg = ['<svg viewBox="0 0 %d 96" role="img" aria-label="%s" text-rendering="geometricPrecision">' % (W, lab["head"])]
    svg.append('<line class="lm-axis" x1="%d" y1="%d" x2="%d" y2="%d"/>' % (M, AX, W - M, AX))
    for i, (cls, val, label) in enumerate(sorted_ticks):
        x = str(round(xp(val)))
        s = -1 if i % 2 == 0 else 1
        svg.append('<line class="lm-tick %s" x1="%s" y1="%d" x2="%s" y2="%d"/>' % (cls, x, AX, x, AX + s * 26))
        svg.append('<text class="lm-label %s" x="%s" y="%d" text-anchor="middle">%s</text>' % (cls, x, AX + s * 33, label))
        svg.append('<text class="lm-val" x="%s" y="%d" text-anchor="middle">%s</text>' % (x, AX + s * 41, fmt(val)))
    px = str(round(xp(price)))
    svg.append('<line class="lm-now-line" x1="%s" y1="10" x2="%s" y2="86"/>' % (px, px))
    svg.append('<polygon class="lm-now-mark" points="%s,15 %.1f,8 %.1f,8"/>' % (px, float(px) - 3.5, float(px) + 3.5))
    svg.append('<text class="lm-label lm-now-mark" x="%s" y="6" text-anchor="middle">%s %s</text>' % (px, lab["price"], fmt(price)))
    svg.append('</svg>')
    return "".join(svg)

ARTICLE_TPL = '''                        <article class="report-container bias-{{BIAS_CLASS}}" style="display: block;">
            <div class="report-header">
                <div class="pair-info">
                    <div class="pair-icon-wrapper">
                        <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                    </div>
                    <div>
                        <h2 class="pair-name">{{PAIR}}</h2>
                        <div class="pair-quote">
                            <span class="lang-en">Current Quote:</span>
                            <span class="lang-pt" style="display:none;">Cotação Atual:</span>
                            <strong>{{QUOTE}}</strong>
                        </div>
                    </div>
                </div>
                <div class="bias-badge bias-{{BIAS_CLASS}}">
                    <span class="lang-en">{{PAIR}} - {{BIAS_EN}}</span>
                    <span class="lang-pt" style="display:none;">{{PAIR}} - {{BIAS_PT}}</span>
                </div>
            </div>

            <div class="report-body">
                <!-- REPORT BRIEF — BLUF + conviction + macro drivers + data basis -->
                <div class="report-brief">
                    <div class="bluf">
                        <span class="bluf-tag"><span class="lang-en">Bottom line</span><span class="lang-pt" style="display:none;">Resumo da operação</span></span>
                        <span class="lang-en">{{BLUF_EN}}</span><span class="lang-pt" style="display:none;">{{BLUF_PT}}</span>
                    </div>
                    <div class="brief-grid">
                        <div class="conviction">
                            <div class="conv-head">
                                <span class="conv-label"><span class="lang-en">Setup conviction (R/R)</span><span class="lang-pt" style="display:none;">Convicção do setup (R/R)</span></span>
                                <span class="conv-tier {{CONV_TIERCLS}}">{{CONV_SCORE}}/10 &middot; <span class="lang-en">{{CONV_TIER_EN}}</span><span class="lang-pt" style="display:none;">{{CONV_TIER_PT}}</span></span>
                            </div>
                            <div class="conv-bar">{{CONV_SEGS}}</div>
                        </div>
                        <div class="macro-block">
                            <div class="macro-head"><span class="lang-en">Macro drivers</span><span class="lang-pt" style="display:none;">Drivers macro</span></div>
                            <div class="macro-chips">{{CHIPS}}</div>
                            <div class="next-event"><span class="ne-tag"><span class="lang-en">Next focus</span><span class="lang-pt" style="display:none;">Próximo foco</span></span> <span class="lang-en">US CPI &amp; Fed speakers</span><span class="lang-pt" style="display:none;">CPI dos EUA &amp; discursos do Fed</span></div>
                        </div>
                    </div>
                    <div class="data-basis"><span class="db-tag"><span class="lang-en">Basis</span><span class="lang-pt" style="display:none;">Base</span>:</span> <span class="lang-en">{{BASIS_EN}}</span><span class="lang-pt" style="display:none;">{{BASIS_PT}}</span></div>
                </div>

                <!-- Section 1: Fundamental -->
                <section class="report-section">
                    <h3 class="section-title">
                        <span class="lang-en">1. Fundamental & Macro Flow</span>
                        <span class="lang-pt" style="display:none;">1. Panorama Fundamentalista & Fluxo Macro</span>
                    </h3>
                    <div class="section-content lang-en">{{FUND_EN}}</div>
                    <div class="section-content lang-pt" style="display:none;">{{FUND_PT}}</div>
                </section>

                <!-- Section 2: Technical -->
                <section class="report-section">
                    <h3 class="section-title">
                        <span class="lang-en">2. Technical Architecture</span>
                        <span class="lang-pt" style="display:none;">2. Arquitetura Técnica (Gráfico Diário/Semanal)</span>
                    </h3>

                    <div class="technical-grid">
                        <div class="tech-box">
                            <div class="tech-box-label">
                                <span class="lang-en">Main Trend</span><span class="trend-arrow" aria-hidden="true"></span>
                                <span class="lang-pt" style="display:none;">Tendência Principal</span>
                            </div>
                            <div class="tech-box-value lang-en">{{TREND_EN}}</div>
                            <div class="tech-box-value lang-pt" style="display:none;">{{TREND_PT}}</div>
                        </div>
                        <div class="tech-box">
                            <div class="tech-box-label">
                                <span class="lang-en">Critical Liquidity Zones</span>
                                <span class="lang-pt" style="display:none;">Zonas de Liquidez Críticas</span>
                            </div>
                            <div class="tech-box-value" style="display: flex; flex-direction: column; gap: 0.4rem;">
                                <div style="font-size: 0.85rem;">
                                    <span style="font-weight: 500; color: var(--text-secondary);">
                                        <span class="lang-en">Nearest Macro Support:</span>
                                        <span class="lang-pt" style="display:none;">Suporte Macro mais próximo:</span>
                                    </span>
                                    <strong class="lang-en">{{SUPP_EN}}</strong>
                                    <strong class="lang-pt" style="display:none;">{{SUPP_PT}}</strong>
                                </div>
                                <div style="font-size: 0.85rem;">
                                    <span style="font-weight: 500; color: var(--text-secondary);">
                                        <span class="lang-en">Nearest Macro Resistance:</span>
                                        <span class="lang-pt" style="display:none;">Resistência Macro mais próxima:</span>
                                    </span>
                                    <strong class="lang-en">{{RES_EN}}</strong>
                                    <strong class="lang-pt" style="display:none;">{{RES_PT}}</strong>
                                </div>
                            </div>
                                <div class="range-gauge" aria-hidden="true">
                                    <div class="range-gauge-track">
                                        <div class="range-gauge-mid"></div>
                                        <div class="range-gauge-now" style="left: {{GAUGE}}%;">{{GAUGE_NOW}}</div>
                                        <div class="range-gauge-marker" style="left: {{GAUGE}}%;"></div>
                                    </div>
                                    <div class="range-gauge-values"><span class="rgv-l">{{GAUGE_SUP}}</span><span class="rgv-r">{{GAUGE_RES}}</span></div>
                                </div>
                        </div>
                    </div>

                    <div class="tech-box" style="margin-top:1rem;">
                        <div class="tech-box-label">
                            <span class="lang-en">Price Action Behavior</span>
                            <span class="lang-pt" style="display:none;">Comportamento do Preço (Price Action)</span>
                        </div>
                        <div class="section-content lang-en" style="font-size: 0.9rem;">{{PA_EN}}</div>
                        <div class="section-content lang-pt" style="display:none; font-size: 0.9rem;">{{PA_PT}}</div>
                    </div>

                    <!-- TRADE LEVEL MAP — schematic of price vs entry/stop/target/S-R -->
                    <div class="level-map">
                        <div class="lm-head"><span class="lang-en">Trade level map</span><span class="lang-pt" style="display:none;">Mapa de níveis da operação</span></div>
                        <div class="lang-en">{{LM_SVG_EN}}</div>
                        <div class="lang-pt" style="display:none;">{{LM_SVG_PT}}</div>
                        <div class="lm-legend">
                            <span><i class="lg-entry"></i><span class="lang-en">Entry</span><span class="lang-pt" style="display:none;">Entrada</span></span>
                            <span><i class="lg-stop"></i><span class="lang-en">Stop</span><span class="lang-pt" style="display:none;">Stop</span></span>
                            <span><i class="lg-target"></i><span class="lang-en">Target</span><span class="lang-pt" style="display:none;">Alvo</span></span>
                            <span><i class="lg-now"></i><span class="lang-en">Price</span><span class="lang-pt" style="display:none;">Preço</span></span>
                        </div>
                    </div>
                </section>

                <!-- Section 3: Strategic Verdict & Setup -->
                <section class="report-section">
                    <h3 class="section-title">
                        <span class="lang-en">3. Strategic Verdict & Trade Setup</span>
                        <span class="lang-pt" style="display:none;">3. Veredito Estratégico & Sugestão de Operação</span>
                    </h3>

                    <!-- TRADE TICKET — the stamped order slip (signature element) -->
                    <div class="trade-ticket verdict-{{VERDICT}}">
                        <div class="ticket-head">
                            <div class="ticket-id">
                                <span class="ticket-serial">TICKET &middot; <span class="ts-pair">{{PAIR}}</span> &middot; <span class="ts-date">{{SERIAL_DATE}}</span></span>
                                <span class="verdict-badge {{VERDICT}}">
                                    <span class="lang-en">{{REC_EN}}</span>
                                    <span class="lang-pt" style="display:none;">{{REC_PT}}</span>
                                </span>
                            </div>
                            <div class="ticket-rr">
                                <span class="rr-label">R : R</span>
                                <span class="rr-seal">{{RR}}</span>
                            </div>
                        </div>

                        <div class="setup-trigger-card">
                            <div class="setup-card-label">
                                <span class="lang-en">Entry Trigger</span>
                                <span class="lang-pt" style="display:none;">Gatilho de Entrada</span>
                            </div>
                            <div class="setup-card-value lang-en">{{TRIG_EN}}</div>
                            <div class="setup-card-value lang-pt" style="display:none;">{{TRIG_PT}}</div>
                        </div>

                        <div class="setup-risk-grid">
                            <div class="risk-card stop-card">
                                <div class="setup-card-label">
                                    <span class="lang-en">Stop Loss (Invalidation)</span>
                                    <span class="lang-pt" style="display:none;">Invalidação Técnica (Stop Loss)</span>
                                </div>
                                <div class="setup-card-value lang-en">{{STOP_EN}}</div>
                                <div class="setup-card-value lang-pt" style="display:none;">{{STOP_PT}}</div>
                            </div>
                            <div class="risk-card target-card">
                                <div class="setup-card-label">
                                    <span class="lang-en">Take Profit (Target)</span>
                                    <span class="lang-pt" style="display:none;">Alvo de Saída (Take Profit)</span>
                                </div>
                                <div class="setup-card-value lang-en">{{TGT_EN}}</div>
                                <div class="setup-card-value lang-pt" style="display:none;">{{TGT_PT}}</div>
                            </div>
                        </div>

                        <div style="margin-top: 1rem;">
                            <div class="tech-box-label">
                                <span class="lang-en">Final Justification</span>
                                <span class="lang-pt" style="display:none;">Justificativa Final</span>
                            </div>
                            <div class="section-content lang-en" style="font-size: 0.9rem; font-style: italic;">{{JUST_EN}}</div>
                            <div class="section-content lang-pt" style="display:none; font-size: 0.9rem; font-style: italic;">{{JUST_PT}}</div>
                        </div>
                    </div>
                </section>
            </div>
        </article>'''

def render(tpl, m):
    out = tpl
    for k, v in m.items():
        out = out.replace("{{" + k + "}}", v)
    return out

for pair, fname in PAGE.items():
    d = data[pair]
    bias_class = d["biasType"]
    bias_en, bias_pt = BIAS_TXT[bias_class]
    q = parse_level(d["quote"]); sup = parse_level(d["en"]["support"]); res = parse_level(d["en"]["resistance"])
    pct = (q - sup) / (res - sup) * 100
    pct = max(0, min(100, pct))
    gauge = str(round(pct))
    verdict = verdict_class(d["en"]["recommendation"])

    score, tier = conviction(d["en"]["rr"])
    tier_en = {"high": "High", "good": "Good", "mod": "Moderate"}[tier]
    tier_pt = {"high": "Alta", "good": "Boa", "mod": "Moderada"}[tier]
    tiercls = "t-high" if tier == "high" else ("t-mod" if tier == "mod" else "")

    _dm = re.search(r"(\d{2})/(\d{2})/(\d{4})", d["en"]["fundamental"])
    serial_date = ("%s·%s·%s" % (_dm.group(1), _dm.group(2), _dm.group(3)[2:])) if _dm else ""

    mapping = {
        "PAIR": pair,
        "SERIAL_DATE": serial_date,
        "QUOTE": d["quote"],
        "BIAS_CLASS": bias_class,
        "BIAS_EN": bias_en,
        "BIAS_PT": bias_pt,
        "GAUGE": gauge,
        "VERDICT": verdict,
        "RR": d["en"]["rr"],
        "RRVAL": str(d["en"]["rrValue"]),
        "BLUF_EN": bluf_sentence(d, "en"),
        "BLUF_PT": bluf_sentence(d, "pt"),
        "CONV_SCORE": str(score),
        "CONV_TIER_EN": tier_en,
        "CONV_TIER_PT": tier_pt,
        "CONV_TIERCLS": tiercls,
        "CONV_SEGS": conv_segs_html(score),
        "CHIPS": chips_html(pair),
        "BASIS_EN": data_basis(d, "en"),
        "BASIS_PT": data_basis(d, "pt"),
        "LM_SVG_EN": level_map_svg(d, LM_LABELS["en"]),
        "LM_SVG_PT": level_map_svg(d, LM_LABELS["pt"]),
        "GAUGE_SUP": fmt(sup),
        "GAUGE_RES": fmt(res),
        "GAUGE_NOW": d["quote"],
        "FUND_EN": d["en"]["fundamental"],
        "FUND_PT": d["pt"]["fundamental"],
        "TREND_EN": d["en"]["trend"],
        "TREND_PT": d["pt"]["trend"],
        "SUPP_EN": d["en"]["support"],
        "SUPP_PT": d["pt"]["support"],
        "RES_EN": d["en"]["resistance"],
        "RES_PT": d["pt"]["resistance"],
        "PA_EN": d["en"]["priceAction"],
        "PA_PT": d["pt"]["priceAction"],
        "REC_EN": d["en"]["recommendation"],
        "REC_PT": d["pt"]["recommendation"],
        "TRIG_EN": d["en"]["trigger"],
        "TRIG_PT": d["pt"]["trigger"],
        "STOP_EN": d["en"]["stop"],
        "STOP_PT": d["pt"]["stop"],
        "TGT_EN": d["en"]["target"],
        "TGT_PT": d["pt"]["target"],
        "JUST_EN": d["en"]["justification"],
        "JUST_PT": d["pt"]["justification"],
    }
    new_article = render(ARTICLE_TPL, mapping)
    # sanity: no leftover placeholders
    assert "{{" not in new_article, f"{pair}: leftover placeholder"

    path = DOCS + "\\" + fname
    with open(path, encoding="utf-8") as f:
        html = f.read()

    # structural assertions on the ORIGINAL page
    assert html.count("<article ") == 1, f"{fname}: expected exactly 1 <article>, found {html.count('<article ')}"
    assert "</footer>" in html and "</body>" in html, f"{fname}: footer/body missing"
    # locate the existing article block (non-greedy to first </article>)
    m = re.search(r"<article class=\"report-container.*?</article>", html, re.DOTALL)
    assert m, f"{fname}: article block not found"
    old_article = m.group(0)

    html_new = html[:m.start()] + new_article + html[m.end():]
    # post-write assertions
    assert html_new.count("<article ") == 1, f"{fname}: article count changed after replace"
    assert "</footer>" in html_new and "</body>" in html_new, f"{fname}: footer/body broken after replace"
    # ensure the evergreen educational block is still present (untouched)
    assert "compliance-container" in html_new, f"{fname}: educational section lost"
    # ensure no stale REPORT date remains (old timestamp / old closing phrase); today's date must be present
    assert "11/08/2026" not in new_article, f"{fname}: old timestamp 11/08/2026 in new article"
    assert "13/08/2026" not in new_article, f"{fname}: old timestamp 13/08/2026 in new article"
    assert "03/08/2026" not in new_article, f"{fname}: old timestamp 03/08/2026 in new article"
    assert "02/08/2026" not in new_article, f"{fname}: old timestamp 02/08/2026 in new article"
    assert "fechamento diário de 31/07" not in new_article and "31/07 daily close" not in new_article, f"{fname}: stale closing-date phrase"
    assert serial_date, f"{fname}: could not extract the session date from the EN fundamental text"

    with open(path, "w", encoding="utf-8") as f:
        f.write(html_new)
    print(f"OK {fname}: bias={bias_class} verdict={verdict} gauge={gauge}% rrBar={d['en']['rrValue']}% rr={d['en']['rr']}")

# ---- Refresh the no-JS static fallback report (default pair EUR/USD) inside index.html ----
# The dashboard re-renders #reportContainer via JS on load; this static block is what crawlers
# and no-JS visitors see, so it must carry the CURRENT default-pair data after every daily run.
FALLBACK_PAIR = "EUR/USD"
fd = data[FALLBACK_PAIR]
f_det = fd["en"]
f_bias = fd["biasType"]
f_bias_txt = BIAS_TXT[f_bias][0]
f_verdict = verdict_class(f_det["recommendation"])
f_q = parse_level(fd["quote"]); f_sup = parse_level(f_det["support"]); f_res = parse_level(f_det["resistance"])
f_gauge = str(round(max(0, min(100, (f_q - f_sup) / (f_res - f_sup) * 100)))) if f_res != f_sup else "50"
_dm = re.search(r"(\d{2})/(\d{2})/(\d{4})", f_det["fundamental"])
f_serial = "TICKET · %s · %s·%s·%s" % (FALLBACK_PAIR, _dm.group(1), _dm.group(2), _dm.group(3)[2:]) if _dm else ""

def _sub1(pattern, repl, name, html, flags=re.DOTALL):
    new, n = re.subn(pattern, repl, html, flags=flags)
    assert n == 1, "index.html fallback: '%s' matched %d times (expected 1)" % (name, n)
    return new

with open(INDEX, encoding="utf-8") as f:
    idx_html = f.read()
m = re.search(r'<article class="report-container[^>]*id="reportContainer".*?</article>', idx_html, re.DOTALL)
assert m, "index.html: static fallback article (#reportContainer) not found"
fb = m.group(0)
fb = _sub1(r'(<article class="report-container bias-)\w+(")', r"\g<1>%s\g<2>" % f_bias, "article bias class", fb)
fb = _sub1(r'id="currentQuoteVal">[^<]*<', lambda _: 'id="currentQuoteVal">%s<' % fd["quote"], "quote", fb)
fb = _sub1(r'<div class="bias-badge bias-\w+">\s*[A-Z]+\s*</div>',
           lambda _: '<div class="bias-badge bias-%s">%s</div>' % (f_bias, f_bias_txt), "header bias badge", fb)
fb = _sub1(r'id="reportFundamental">.*?</div>', lambda _: 'id="reportFundamental">%s</div>' % f_det["fundamental"], "fundamental", fb)
fb = _sub1(r'id="reportTrend">.*?</div>', lambda _: 'id="reportTrend">%s</div>' % f_det["trend"], "trend", fb)
fb = _sub1(r'id="reportSupport">.*?</strong>', lambda _: 'id="reportSupport">%s</strong>' % f_det["support"], "support", fb)
fb = _sub1(r'id="reportResistance">.*?</strong>', lambda _: 'id="reportResistance">%s</strong>' % f_det["resistance"], "resistance", fb)
fb = _sub1(r'id="reportGaugeNow" style="left:\s*\d+(\.\d+)?%;">[^<]*<',
           lambda _: 'id="reportGaugeNow" style="left: %s%%;">%s<' % (f_gauge, fd["quote"]), "gauge now", fb)
fb = _sub1(r'id="reportRangeMarker" style="left:\s*\d+(\.\d+)?%;"',
           lambda _: 'id="reportRangeMarker" style="left: %s%%;"' % f_gauge, "gauge marker", fb)
fb = _sub1(r'id="reportGaugeSup">[^<]*<', lambda _: 'id="reportGaugeSup">%s<' % fmt(f_sup), "gauge sup", fb)
fb = _sub1(r'id="reportGaugeRes">[^<]*<', lambda _: 'id="reportGaugeRes">%s<' % fmt(f_res), "gauge res", fb)
fb = _sub1(r'id="reportPriceAction"[^>]*>.*?</div>', lambda _: 'id="reportPriceAction" style="font-size: 0.9rem;">%s</div>' % f_det["priceAction"], "price action", fb)
fb = _sub1(r'id="ticketSerial">[^<]*<', lambda _: 'id="ticketSerial">%s<' % f_serial, "ticket serial", fb)
fb = _sub1(r'<span class="verdict-badge \w+" id="reportVerdictBadge">.*?</span>',
           lambda _: '<span class="verdict-badge %s" id="reportVerdictBadge">%s</span>' % (f_verdict, f_det["recommendation"]), "verdict badge", fb)
fb = _sub1(r'id="reportRR">[^<]*<', lambda _: 'id="reportRR">%s<' % f_det["rr"], "rr seal", fb)
fb = _sub1(r'id="reportTrigger">.*?</div>', lambda _: 'id="reportTrigger">%s</div>' % f_det["trigger"], "trigger", fb)
fb = _sub1(r'id="reportStop">.*?</div>', lambda _: 'id="reportStop">%s</div>' % f_det["stop"], "stop", fb)
fb = _sub1(r'id="reportTarget">.*?</div>', lambda _: 'id="reportTarget">%s</div>' % f_det["target"], "target", fb)
fb = _sub1(r'id="reportJustification"[^>]*>.*?</div>',
           lambda _: 'id="reportJustification" style="font-size: 0.9rem; font-style: italic;">%s</div>' % f_det["justification"], "justification", fb)
fb = _sub1(r'trade-ticket verdict-\w+" id="verdictCardElement"',
           lambda _: 'trade-ticket verdict-%s" id="verdictCardElement"' % f_verdict, "ticket verdict class", fb)
# post-refresh sanity: the fallback must now carry the current data
for probe, what in [(fd["quote"], "quote"), (f_det["recommendation"], "EN recommendation"), (f_det["rr"], "rr")]:
    assert probe in fb, "index.html fallback: %s missing after refresh" % what

idx_html = idx_html[:m.start()] + fb + idx_html[m.end():]
with open(INDEX, "w", encoding="utf-8") as f:
    f.write(idx_html)
print("OK index.html: no-JS static fallback refreshed for %s (bias=%s verdict=%s gauge=%s%%)" % (FALLBACK_PAIR, f_bias, f_verdict, f_gauge))

print("\nAll 6 static pages + index fallback regenerated from forexData.")
