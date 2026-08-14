#!/usr/bin/env python3
"""Regenerate the <article> block in each static pair page from the validated forexData in index.html.
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

# ---- Macro driver chips (author-maintained, mirrors docs/index.html macroDrivers) ----
DRIVERS = {
    "EUR/USD": (["Fed hold 3.50-3.75%", "CPI 3.4%", "ECB 2.25%"], ["Fed 3,50-3,75%", "CPI 3,4%", "BCE 2,25%"]),
    "USD/JPY": (["BoJ 1.00% hawkish", "Intervention fade", "Fed–BoJ gap"], ["BoJ 1,0% hawkish", "Intervenção esvaindo", "Diferencial Fed–BoJ"]),
    "AUD/USD": (["RBA 4.35%", "WTI $82", "Fed dovish"], ["RBA 4,35%", "WTI $82", "Fed dovish"]),
    "GBP/USD": (["BoE 3.75% 6-3", "CPI 2.6%", "Fed dovish"], ["BoE 3,75% 6-3", "IPC 2,6%", "Fed dovish"]),
    "EUR/JPY": (["BoJ 1.00% hawkish", "Intervention fade", "ECB–BoJ gap"], ["BoJ 1,0% hawkish", "Intervenção esvaindo", "Diferencial BCE–BoJ"]),
    "GBP/JPY": (["BoJ 1.00% hawkish", "Intervention fade", "BoE–BoJ gap"], ["BoJ 1,0% hawkish", "Intervenção esvaindo", "Diferencial BoE–BoJ"]),
}

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
                    <div class="data-basis"><span class="db-tag"><span class="lang-en">Basis</span><span class="lang-pt" style="display:none;">Base</span>:</span> <span class="lang-en">ECB/Frankfurter reference rates · SMA50/200 &amp; Fibonacci computed · 520 daily sessions (01/08/2024–14/08/2026).</span><span class="lang-pt" style="display:none;">taxas de referência BCE/Frankfurter · SMA50/200 e Fibonacci calculados · 520 pregões (01/08/2024 a 14/08/2026).</span></div>
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
    assert "14/08/2026" in new_article, f"{fname}: today's date 14/08/2026 missing from new article"

    with open(path, "w", encoding="utf-8") as f:
        f.write(html_new)
    print(f"OK {fname}: bias={bias_class} verdict={verdict} gauge={gauge}% rrBar={d['en']['rrValue']}% rr={d['en']['rr']}")

print("\nAll 6 static pages regenerated from forexData.")
