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
                                    <div class="range-gauge-track"><div class="range-gauge-marker" style="left: {{GAUGE}}%;"></div></div>
                                    <div class="range-gauge-labels"><span>S</span><span>R</span></div>
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
                </section>

                <!-- Section 3: Strategic Verdict & Setup -->
                <section class="report-section">
                    <h3 class="section-title">
                        <span class="lang-en">3. Strategic Verdict & Trade Setup</span>
                        <span class="lang-pt" style="display:none;">3. Veredito Estratégico & Sugestão de Operação</span>
                    </h3>

                    <div class="verdict-card verdict-{{VERDICT}}">
                        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1rem; border-bottom: 1px solid rgba(0,0,0,0.05); padding-bottom: 0.75rem;">
                            <span class="verdict-badge {{VERDICT}}" style="margin-bottom: 0;">
                                <span class="lang-en">{{REC_EN}}</span>
                                <span class="lang-pt" style="display:none;">{{REC_PT}}</span>
                            </span>
                            <div style="display: flex; align-items: center; gap: 0.4rem;">
                                <span style="font-size: 0.8rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">
                                    <span class="lang-en">Risk/Reward Ratio</span>
                                    <span class="lang-pt" style="display:none;">Relação Risco/Retorno</span>
                                </span>
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

                        <!-- Interactive R&R Visual Bar -->
                        <div class="ratio-bar-wrapper" style="margin-top: 1.25rem;">
                            <div class="ratio-bar-label">
                                <span style="font-weight:700;">
                                    <span class="lang-en">RISK / REWARD SYMMETRY</span>
                                    <span class="lang-pt" style="display:none;">SIMETRIA RISCO / RETORNO</span>
                                </span>
                                <span>{{RR}}</span>
                            </div>
                            <div class="ratio-bar-container">
                                <div class="ratio-bar-fill" style="width: {{RRVAL}}%;"></div>
                            </div>
                        </div>

                        <div class="tech-box-label" style="margin-top: 1.25rem; margin-bottom: 0.25rem;">
                            <span class="lang-en">Final Justification</span>
                            <span class="lang-pt" style="display:none;">Justificativa Final</span>
                        </div>
                        <div class="section-content lang-en" style="font-size: 0.9rem; font-style: italic;">{{JUST_EN}}</div>
                        <div class="section-content lang-pt" style="display:none; font-size: 0.9rem; font-style: italic;">{{JUST_PT}}</div>
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

    mapping = {
        "PAIR": pair,
        "QUOTE": d["quote"],
        "BIAS_CLASS": bias_class,
        "BIAS_EN": bias_en,
        "BIAS_PT": bias_pt,
        "GAUGE": gauge,
        "VERDICT": verdict,
        "RR": d["en"]["rr"],
        "RRVAL": str(d["en"]["rrValue"]),
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
    assert "02/08/2026" not in new_article, f"{fname}: old timestamp 02/08/2026 in new article"
    assert "fechamento diário de 31/07" not in new_article and "31/07 daily close" not in new_article, f"{fname}: stale closing-date phrase"
    assert "03/08/2026" in new_article, f"{fname}: today's date 03/08/2026 missing from new article"

    with open(path, "w", encoding="utf-8") as f:
        f.write(html_new)
    print(f"OK {fname}: bias={bias_class} verdict={verdict} gauge={gauge}% rrBar={d['en']['rrValue']}% rr={d['en']['rr']}")

print("\nAll 6 static pages regenerated from forexData.")
