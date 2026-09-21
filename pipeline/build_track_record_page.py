#!/usr/bin/env python3
"""Regenerate docs/track-record.html from docs/track-record.json.
The page is the public, bilingual rendering of the ledger — every directional ticket
published in the daily report, resolved mechanically on daily closes. Nothing filtered.
Run after every ledger update (the daily forex-report pipeline does this)."""
import json, os, re, sys

DOCS = os.path.join(os.path.dirname(__file__), "..", "docs")
LEDGER = os.path.join(DOCS, "track-record.json")
OUT = os.path.join(DOCS, "track-record.html")

with open(LEDGER, encoding="utf-8") as f:
    L = json.load(f)

watching, opened, closed = L.get("watching", []), L.get("open", []), L.get("closed", [])
updated = L["meta"].get("lastUpdated", "")

def num(v):
    if v is None:
        return "—"
    s = ("%.5f" % float(v)).rstrip("0").rstrip(".")
    return s

def arrow(direction):
    return "▲ long" if direction == "long" else "▼ short"

resolved = [t for t in closed if t.get("outcome") in ("target", "stop", "expired")]
revoked = [t for t in closed if t.get("outcome") == "revoked"]
n_target = sum(1 for t in resolved if t["outcome"] == "target")
n_stop = sum(1 for t in resolved if t["outcome"] == "stop")
n_expired = sum(1 for t in resolved if t["outcome"] == "expired")
net_r = sum(t["realizedR"] for t in resolved if t.get("realizedR") is not None)
avg_r = (net_r / len(resolved)) if resolved else None

OUTCOME_EN = {"target": "Target hit", "stop": "Stop hit", "expired": "Expired (10 sessions)", "revoked": "Revoked before trigger"}
OUTCOME_PT = {"target": "Alvo atingido", "stop": "Stop atingido", "expired": "Expirou (10 pregões)", "revoked": "Revogado antes do gatilho"}

def ticket_row(t, kind):
    if kind == "watching":
        status_en, status_pt = "Watching for trigger", "Aguardando gatilho"
        exit_en = exit_pt = "—"
        rr_en = rr_pt = "—"
    elif kind == "open":
        status_en, status_pt = "Open (triggered %s)" % t.get("entryDate", "—"), "Aberto (gatilho em %s)" % t.get("entryDate", "—")
        exit_en = exit_pt = "—"
        rr_en = rr_pt = "—"
    else:
        o = t["outcome"]
        status_en, status_pt = "%s (%s)" % (OUTCOME_EN[o], t.get("exitDate", "—")), "%s (%s)" % (OUTCOME_PT[o], t.get("exitDate", "—"))
        exit_en = exit_pt = "—"
        rr_en = rr_pt = ("%+.2fR" % t["realizedR"]) if t.get("realizedR") is not None else "—"
    return ("              <tr><td>%s</td><td>%s</td><td>%s / %s</td><td>%s</td><td>%s</td><td>%s</td><td>1:%s</td><td>%s</td><td>%s</td></tr>\n"
            "<tr class='tr-pt' style='display:none;'><td>%s</td><td>%s</td><td>%s / %s</td><td>%s</td><td>%s</td><td>%s</td><td>1:%s</td><td>%s</td><td>%s</td></tr>") % (
        t["pair"], t.get("reportDate", "—"), arrow(t["direction"]), t.get("setup", "—"),
        num(t.get("entry")), num(t.get("stop")), num(t.get("target")), num(t.get("plannedR", 0)) if t.get("plannedR") else "—", status_en, exit_en if kind != "closed" else rr_en,
        t["pair"], t.get("reportDate", "—"), arrow(t["direction"]), t.get("setup", "—"),
        num(t.get("entry")), num(t.get("stop")), num(t.get("target")), num(t.get("plannedR", 0)) if t.get("plannedR") else "—", status_pt, exit_pt if kind != "closed" else rr_pt,
    )

def notes_block(tickets, en_label, pt_label):
    if not tickets:
        return ""
    items = "".join("<li><b>%s</b> (%s): %s</li>" % (t["pair"], t.get("reportDate", "—"), t.get("note", "")) for t in tickets)
    return ('<div class="tr-notes"><div class="lang-en"><h3>%s</h3><ul>%s</ul></div>'
            '<div class="lang-pt" style="display:none;"><h3>%s</h3><ul>%s</ul></div></div>') % (en_label, items, pt_label, items)

HEAD_EN = ("           <thead><tr><th>Pair</th><th>Published</th><th>Direction / setup</th><th>Entry</th><th>Stop</th><th>Target</th><th>Planned R/R</th><th>Status</th><th>Result</th></tr></thead>")
HEAD_PT = ("           <thead class='tr-pt' style='display:none;'><tr><th>Par</th><th>Publicado</th><th>Direção / setup</th><th>Entrada</th><th>Stop</th><th>Alvo</th><th>R/R planejado</th><th>Status</th><th>Resultado</th></tr></thead>")

def table(tickets, kind):
    if not tickets:
        return ('<p class="lang-en">No tickets in this state right now.</p><p class="lang-pt" style="display:none;">Nenhum ticket neste estado no momento.</p>')
    rows = "\n".join(ticket_row(t, kind) for t in tickets)
    return '<div class="table-wrap"><table>\n%s\n%s\n<tbody>\n%s\n</tbody>\n</table></div>' % (HEAD_EN, HEAD_PT, rows)

# PT rows are rendered hidden by the page's language toggle
PAGE = """<!DOCTYPE html>
<html lang="en" data-title-pt="Registro de Desempenho - Forex Report">
<head>
    <link rel="icon" type="image/png" href="favicon-96x96.png" sizes="96x96" />
    <link rel="shortcut icon" href="favicon.ico" />
    <link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png" />
    <meta name="apple-mobile-web-app-title" content="Forex Report" />
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Track Record - Forex Ticket Performance - Forex Report</title>
    <meta name="description" content="The public performance ledger of Forex Report: every directional ticket published in the daily analysis, resolved mechanically on daily closes. Wins, losses and revoked setups — nothing filtered.">

    <link rel="canonical" href="https://newsforextrading.com/track-record.html">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="Forex Report">
    <meta property="og:title" content="Track Record - Forex Ticket Performance - Forex Report">
    <meta property="og:description" content="Every directional ticket published in the daily analysis, resolved mechanically on daily closes. Nothing filtered.">
    <meta property="og:url" content="https://newsforextrading.com/track-record.html">
    <meta property="og:image" content="https://newsforextrading.com/web-app-manifest-512x512.png">
    <meta property="og:locale" content="en_US">
    <meta property="og:locale:alternate" content="pt_BR">
    <meta name="twitter:card" content="summary">

    <!-- Google AdSense — personalization gated by cookie consent (consent.js) -->
    <script>
        try { if (localStorage.getItem('forexCookieConsent') === 'declined') (window.adsbygoogle = window.adsbygoogle || []).requestNonPersonalizedAds = 1; } catch (e) {}
    </script>
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4617266720439769"
     crossorigin="anonymous"></script>
    <script src="consent.js" defer></script>
    <script src="lang.js" defer></script>

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800&family=Hanken+Grotesk:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
    <style>
        .ledger-container { max-width: 1080px; margin: 0 auto; padding: 0 1.5rem 2rem 1.5rem; }
        .ledger-container table { width: 100%; border-collapse: collapse; margin: 1rem 0; font-size: 0.88rem; }
        .ledger-container th, .ledger-container td { border: 1px solid var(--border-color); padding: 0.55rem 0.6rem; text-align: left; vertical-align: top; }
        .ledger-container th { background-color: var(--bg-light); color: var(--color-primary); font-weight: 600; white-space: nowrap; }
        .ledger-container td { font-family: var(--font-mono); white-space: nowrap; }
        .ledger-container td:nth-child(2), .ledger-container td:nth-child(8), .ledger-container td:nth-child(9) { font-family: var(--font-body); }
        .ledger-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 0.8rem; margin: 1.5rem 0; }
        .stat-card { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 10px; padding: 0.9rem 1rem; }
        .stat-num { font-family: var(--font-mono); font-size: 1.45rem; font-weight: 600; color: var(--text-primary); }
        .stat-lab { font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.04em; color: var(--text-muted); }
        .tr-notes h3 { font-size: 1rem; color: var(--color-primary); margin: 1.2rem 0 0.4rem 0; }
        .tr-notes ul { margin-left: 1.2rem; }
        .tr-notes li { font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 0.5rem; line-height: 1.55; }
        .ledger-method { background: var(--bg-light); border-left: 4px solid var(--color-primary); border-radius: 4px; padding: 1rem 1.2rem; margin: 1.25rem 0; font-size: 0.9rem; color: var(--text-secondary); line-height: 1.65; }
        /* Wide ledgers scroll inside .table-wrap (style.css) on phones */
    </style>
</head>
<body>
    <header class="site-header">
        <div class="container header-content">
            <a href="index.html" class="brand-logo">FOREX<span>REPORT</span></a>
            <nav class="header-nav">
                <a href="index.html" class="nav-link" id="navHome">Dashboard</a>
                <a href="news.html" class="nav-link" id="navNews">News</a>
                <a href="guides/index.html" class="nav-link" id="navGuides">Education</a>
                <a href="about.html" class="nav-link" id="navAbout">About Us</a>
                <a href="contact.html" class="nav-link" id="navContact">Contact</a>
            </nav>
            <div class="header-actions">
                <div class="lang-selector-wrapper">
                    <select class="lang-select" id="langSelect" aria-label="Language Selector">
                        <option value="en">EN</option>
                        <option value="pt">PT</option>
                    </select>
                    <svg class="lang-select-arrow" viewBox="0 0 20 20">
                        <path d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" />
                    </svg>
                </div>
            </div>
        </div>
    </header>

    <main class="container-wide">
        <div class="ledger-container">
            <div style="margin-top: 1.5rem; margin-bottom: 0.5rem; font-size: 0.85rem; color: var(--text-muted);">
                <a href="index.html" style="color: var(--text-muted);">Home</a> &gt; <span class="lang-en">Track Record</span><span class="lang-pt" style="display:none;">Registro de Desempenho</span>
            </div>

            <h1 style="margin-bottom: 0.5rem;">
                <span class="lang-en">Performance Track Record</span>
                <span class="lang-pt" style="display:none;">Registro de Desempenho</span>
            </h1>
            <p style="font-size: 1.05rem; color: var(--text-secondary); max-width: 760px;">
                <span class="lang-en">Every directional ticket published in the daily report since 17/08/2026, tracked after the fact and resolved mechanically on daily closes. Wins, losses, expiries and revoked setups all stay on the page — this ledger exists so you can judge the methodology on evidence, not on claims. Last update: __UPDATED__.</span>
                <span class="lang-pt" style="display:none;">Todo ticket direcional publicado no relatório diário desde 17/08/2026, acompanhado depois dos fatos e resolvido mecanicamente por fechamentos diários. Acertos, perdas, expirações e setups revogados permanecem na página — este registro existe para que você julgue a metodologia pela evidência, e não por promessas. Última atualização: __UPDATED__.</span>
            </p>

            <div class="ledger-method">
                <div class="lang-en"><b>Resolution rules.</b> Triggers and resolutions are close-based (ECB/Frankfurter reference rates). A daily close at/beyond the target closes the ticket at that level; a close at/beyond the stop closes it at −1R; ten sessions after entry with neither level crossed expire the ticket at the 10th-session close (realized R = (exit − entry)/(entry − stop) for longs, mirrored for shorts). A setup withdrawn by a later report before its trigger fired is marked <i>revoked</i> and counts as no trade. One watching ticket per pair at a time.</div>
                <div class="lang-pt" style="display:none;"><b>Regras de resolução.</b> Gatilhos e resoluções são por fechamento (taxas de referência BCE/Frankfurter). Um fechamento diário no alvo ou além fecha o ticket naquele nível; um fechamento no stop ou além fecha em −1R; dez pregões após a entrada sem cruzar nenhum nível expiram o ticket no fechamento do 10º pregão (R realizado = (saída − entrada)/(entrada − stop) para compras, espelhado para vendas). Um setup retirado por relatório posterior antes do gatilho é marcado como <i>revogado</i> e não conta como operação. Apenas um ticket em observação por par por vez.</div>
            </div>

            <div class="ledger-stats">
                <div class="stat-card"><div class="stat-num">__N_WATCH__</div><div class="stat-lab"><span class="lang-en">Watching</span><span class="lang-pt" style="display:none;">Em observação</span></div></div>
                <div class="stat-card"><div class="stat-num">__N_OPEN__</div><div class="stat-lab"><span class="lang-en">Open</span><span class="lang-pt" style="display:none;">Abertos</span></div></div>
                <div class="stat-card"><div class="stat-num">__N_RESOLVED__</div><div class="stat-lab"><span class="lang-en">Resolved</span><span class="lang-pt" style="display:none;">Resolvidos</span></div></div>
                <div class="stat-card"><div class="stat-num">__N_REVOKED__</div><div class="stat-lab"><span class="lang-en">Revoked</span><span class="lang-pt" style="display:none;">Revogados</span></div></div>
                <div class="stat-card"><div class="stat-num">__NET_R__</div><div class="stat-lab"><span class="lang-en">Net realized (R)</span><span class="lang-pt" style="display:none;">R líquido (R)</span></div></div>
            </div>
            <p style="font-size: 0.85rem; color: var(--text-muted);">
                <span class="lang-en">Resolved detail: __N_TARGET__ target &middot; __N_STOP__ stop &middot; __N_EXPIRED__ expired &middot; average __AVG_R__R per resolved ticket. Small sample so far — the ledger grows one report at a time. Past performance does not guarantee future results.</span>
                <span class="lang-pt" style="display:none;">Detalhe dos resolvidos: __N_TARGET__ alvo &middot; __N_STOP__ stop &middot; __N_EXPIRED__ expirados &middot; média de __AVG_R__R por ticket resolvido. Amostra pequena até agora — o registro cresce um relatório por vez. Desempenho passado não garante resultados futuros.</span>
            </p>

            <section class="report-section" style="margin-top: 2rem;">
                <h2 class="section-title"><span class="lang-en">Watching — awaiting trigger</span><span class="lang-pt" style="display:none;">Em observação — aguardando gatilho</span></h2>
__TABLE_WATCHING__
__NOTES_WATCHING__
            </section>

            <section class="report-section" style="margin-top: 2rem;">
                <h2 class="section-title"><span class="lang-en">Open — triggered, still running</span><span class="lang-pt" style="display:none;">Abertos — gatilho disparado, em andamento</span></h2>
__TABLE_OPEN__
__NOTES_OPEN__
            </section>

            <section class="report-section" style="margin-top: 2rem;">
                <h2 class="section-title"><span class="lang-en">Closed — resolved or revoked</span><span class="lang-pt" style="display:none;">Fechados — resolvidos ou revogados</span></h2>
__TABLE_CLOSED__
__NOTES_CLOSED__
            </section>

            <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 1.5rem;">
                <span class="lang-en">Desk notes are reproduced in their original wording (English). The methodology behind every ticket is documented in <a href="guides/our-methodology.html">Our Methodology</a>; the risk rules in <a href="guides/risk-management.html">Risk Management</a>.</span>
                <span class="lang-pt" style="display:none;">As notas da mesa são reproduzidas no original (inglês). A metodologia por trás de cada ticket está documentada em <a href="guides/our-methodology.html">Nossa Metodologia</a>; as regras de risco em <a href="guides/risk-management.html">Gestão de Risco</a>.</span>
            </p>
        </div>

        <!-- Ad Space — after the ledger content -->
        <ins class="adsbygoogle" style="display:block; text-align:center; margin: 2rem 0;" data-ad-layout="in-article" data-ad-format="fluid" data-ad-client="ca-pub-4617266720439769" data-ad-slot="8549246934"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
    </main>

    <footer class="site-footer">
        <div class="container">
            <p class="footer-disclaimer">Disclaimer: Forex trading involves significant risk. Leverage can work against you. Past results do not guarantee future performance. Content is purely educational and does not constitute financial advice.</p>
            <div class="footer-links">
                <a href="about.html" class="footer-link">About Us</a>
                <a href="contact.html" class="footer-link">Contact</a>
                <a href="disclaimer.html" class="footer-link">Legal Disclaimer</a>
                <a href="privacy.html" class="footer-link">Privacy Policy</a>
                <a href="terms.html" class="footer-link">Terms of Service</a>
                <a href="track-record.html" class="footer-link">Track Record</a>
                <a href="guides/index.html" class="footer-link">Education</a>
            </div>
            <p class="footer-copyright">&copy; 2026 Forex Report. All rights reserved.</p>
        </div>
    </footer>

    <!-- Language switcher + cookie consent are shared, deferred (see <head>) -->
</body>
</html>
"""

html = PAGE
html = html.replace("__UPDATED__", updated)
html = html.replace("__N_WATCH__", str(len(watching)))
html = html.replace("__N_OPEN__", str(len(opened)))
html = html.replace("__N_RESOLVED__", str(len(resolved)))
html = html.replace("__N_REVOKED__", str(len(revoked)))
html = html.replace("__N_TARGET__", str(n_target))
html = html.replace("__N_STOP__", str(n_stop))
html = html.replace("__N_EXPIRED__", str(n_expired))
html = html.replace("__NET_R__", "%+.2f" % net_r)
html = html.replace("__AVG_R__", ("%+.2f" % avg_r) if avg_r is not None else "0.00")
html = html.replace("__TABLE_WATCHING__", table(watching, "watching"))
html = html.replace("__TABLE_OPEN__", table(opened, "open"))
html = html.replace("__TABLE_CLOSED__", table(closed, "closed"))
html = html.replace("__NOTES_WATCHING__", notes_block(watching, "Desk notes", "Notas da mesa (original)"))
html = html.replace("__NOTES_OPEN__", notes_block(opened, "Desk notes", "Notas da mesa (original)"))
html = html.replace("__NOTES_CLOSED__", notes_block(closed, "Desk notes", "Notas da mesa (original)"))

assert "__" not in re.sub(r"__\w+__", "", html) or not re.search(r"__[A-Z_]+__", html), "unreplaced placeholder"
assert html.count("<ins") == 1 and html.count("adsbygoogle || []).push({});") == 1, "ad pattern broken"
assert "consent.js" in html and "requestNonPersonalizedAds" in html, "consent pattern broken"
assert "lang.js" in html and "data-title-pt" in html, "lang.js pattern broken"
assert html.count('<div class="table-wrap">') == html.count("<table"), "table wrap broken"

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)
print("OK track-record.html: %d watching / %d open / %d closed (%d resolved, %d revoked) · net %.2fR · updated %s"
      % (len(watching), len(opened), len(closed), len(resolved), len(revoked), net_r, updated))
