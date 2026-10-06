#!/usr/bin/env python3
"""06/10/2026 edition — news wire refresh: prepends 4 desk-wire items (both representations:
newsData.items in index.html + static cards in news.html), updates the wire hero (kicker,
dateline, sub-line) and the week-ahead calendar strip (FOMC minutes 07/10, US CPI ≈13/10 with
shutdown delay risk, Fed-ECB-BoJ cluster 27-30/10, BoE 05/11). Grounded in the 06/10 forexData
narrative only. Aborts on any structural mismatch."""
import io

IDX = r"C:/Projetos/forex-report/docs/index.html"
NEWS = r"C:/Projetos/forex-report/docs/news.html"
TS = "06/10/2026 23:00 UTC"

# ---------------- JS items (newsData, index.html) ----------------
JS_ITEMS = '''                {
                    date: "06/10/2026",
                    category: "flow",
                    impact: "high",
                    pairs: ["EUR/USD"],
                    pt: {
                        headline: "O livro cobra a sequência: corredor do EUR/USD encerra no alvo com +1,27R no fechamento de 01/10 e a venda rearma uma prateleira abaixo da mínima de 9 meses",
                        summary: "O fechamento de 01/10 (1.1298) cruzou o alvo 1.1350 do corredor de continuação disparado em 23/09 (edição de 19/09 — entrada 1.1411, stop 1.1500) e encerrou o ticket em +1,27R (113 pips sobre os 89 pips de risco), o segundo alvo do ledger público — e o capítulo não parou: o fechamento de 05/10 (1.1204) cravou a mínima de 9 meses antes do repique de terça (+0,58%, para 1.1269; quarto fechamento semanal de queda seguido). A mesa rearma uma casa abaixo: venda no repique da prateleira virada 1.1340-1.1370 (o piso de setembro entregue + o redondo 1.1350 + a Fib 78,6% 1.1369), stop 1.1412 (62 pips, sobre a máxima de 10 pregões 1.1411), alvo 1.1200 — o redondo sob a mínima — a 1:2,42, válida até 09/10. O ticket de repique de 28/09 (prateleira 1.1455-1.1500) expirou sem imprimir e foi revogado.",
                        take: "O shutdown suspendeu os dados, não o fluxo: quatro semanas de fechamento semanal de queda com o dólar dominante mesmo com o ISM fraco. A regra não persegue mínima fresca a 65 pips de distância — o próximo ticket só existe se o repique entregar o fechamento na prateleira virada."
                    },
                    en: {
                        headline: "The book collects the sequence: the EUR/USD continuation runner closes at target for +1.27R at the Oct-1 close and the short re-arms one shelf above the 9-month low",
                        summary: "The Oct-1 close (1.1298) crossed the 1.1350 target of the continuation runner triggered on Sep 23 (Sep-19 edition — entry 1.1411, stop 1.1500) and closed the ticket at +1.27R (113 pips over the 89-pip risk), the public ledger's second target — and the chapter did not stop: the Oct-5 close (1.1204) pinned the 9-month low before Tuesday's bounce (+0.58%, to 1.1269; a fourth straight weekly down close). The desk re-arms one shelf below: a short on the pullback to the flipped 1.1340-1.1370 shelf (the handed-back September floor + the 1.1350 round + the 78.6% Fib 1.1369), stop 1.1412 (62 pips, over the 10-day high 1.1411), target 1.1200 — the round under the low — at 1:2.42, valid through Oct 9. The Sep-28 pullback ticket (1.1455-1.1500 shelf) expired unprinted and was revoked.",
                        take: "The shutdown suspended the data, not the flow: four weekly down closes with the dollar dominant even through the weak ISM. The rule does not chase a fresh low from 65 pips away — the next ticket only exists if the pullback delivers the close on the flipped shelf."
                    }
                },
                {
                    date: "06/10/2026",
                    category: "macro",
                    impact: "high",
                    pairs: ["EUR/USD", "GBP/USD", "AUD/USD"],
                    pt: {
                        headline: "Shutdown suspende NFP e CPI desde 01/10 — e o dólar domina mesmo assim: ISM services fraco não compra pausa, EUR/USD abaixo de 1,1200",
                        summary: "O apagão fiscal chegou onde dói: com o shutdown do governo dos EUA desde 01/10, claims, NFP e CPI ficam suspensos — e o CPI de setembro (≈13/10) corre risco de atraso. O fluxo não pediu licença: na semana o dólar varreu o tabuleiro e o fechamento de 05/10 do EUR/USD (1.1204, mínima de 9 meses) veio mesmo com o ISM services de setembro mais fraco que o esperado (05/10, com pressão de preços subindo) — o diferencial (Fed a 3,75-4,00% com mais uma alta sinalizada) segue mandando mais que o dado. A terça devolveu o repique (EUR/USD +0,58%, GBP/USD +0,39%, AUD/USD +0,31%) e a ata do FOMC de quarta (07/10) é o próximo texto na mesa — com o cluster Fed-BCE-BoJ chegando em 27-30/10.",
                        take: "Filtro de eventos sem CPI é filtro cego: com o dado sob risco de atraso, a janela de 24h se apega ao que resta — a ata do FOMC (07/10) e os discursos. A mesa segue negociando fechamentos, não promessas de calendário."
                    },
                    en: {
                        headline: "Shutdown suspends NFP and CPI since Oct 1 — and the dollar dominates anyway: a weak ISM services buys no pause, EUR/USD under 1.1200",
                        summary: "The fiscal blackout hit where it hurts: with the US government shutdown running since Oct 1, claims, NFP and CPI stay suspended — and September's CPI (≈Oct 13) runs delay risk. The flow asked for no license: the dollar swept the board on the week and EUR/USD's Oct-5 close (1.1204, a 9-month low) arrived even through September's weaker-than-expected ISM services (Oct 5, with price pressures mounting) — the differential (Fed at 3.75-4.00% with one more hike signaled) still commands more than the print. Tuesday returned the bounce (EUR/USD +0.58%, GBP/USD +0.39%, AUD/USD +0.31%) and Wednesday's FOMC minutes (Oct 7) are the desk's next text — with the Fed-ECB-BoJ cluster arriving Oct 27-30.",
                        take: "An event filter without CPI is a blind filter: with the print under delay risk, the 24h window clings to what remains — the FOMC minutes (Oct 7) and the speeches. The desk keeps trading closes, not calendar promises."
                    }
                },
                {
                    date: "06/10/2026",
                    category: "cb",
                    impact: "high",
                    pairs: ["AUD/USD"],
                    pt: {
                        headline: "RBA entrega a alta unânime a 4,60% — e a “esperança” de Bullock entrega a SMA200: aussie vira neutro com o teto virado 0.7027-0.7032",
                        summary: "A decisão veio como o consenso pedia (29/09): alta unânime de 25 pb para 4,60%, com comunicado hawkish — mas a frase de Bullock esperando que as quatro altas já entregadas bastem para baixar a inflação tirou o próximo passo do preço: o par mal se mexeu no anúncio e o fechamento de 30/09 (0.6968) entregou a SMA200 (0.7027), com o alinhamento de alta que sobrevivia por 7 pips. A leitura vira NEUTRA (fechamento sob a SMA200, SMA50 0.7092 acima dela) e o mapa trava entre o teto virado 0.7027-0.7032 (SMA200 + Fib 38,2%) e a mínima de 10/20 pregões (0.6939), com a Fib 50% (0.6962) segurando a segunda e devolvendo o repique de terça (+0,31%). O motor commodity segue de pé (CPI a 3,5%, WTI ~US$ 83) e o árbitro chega com o CPI do Q3 no fim de outubro (≈28/10).",
                        take: "Alta unânime vendida no comunicado e devolvida na conferência: o mercado ouviu “esperança” onde o board dizia vigilância. Sem rompimento confirmado na faixa 0.6939-0.7032 não há ticket — o CPI do Q3 decide se a RBA de novembro devolve o diferencial ao aussie."
                    },
                    en: {
                        headline: "RBA delivers the unanimous hike to 4.60% — and Bullock's “hope” hands over the SMA200: the aussie turns neutral under the flipped 0.7027-0.7032 ceiling",
                        summary: "The decision came as consensus wanted it (Sep 29): a unanimous 25-bp hike to 4.60%, with hawkish statement language — but Bullock's line hoping the four hikes already delivered would be enough to bring inflation down took the next step out of the price: the pair barely moved on the announcement and the Sep-30 close (0.6968) handed over the SMA200 (0.7027), taking the bull alignment that had survived by 7 pips. The read turns NEUTRAL (close under the SMA200, 50-day 0.7092 above it) and the map locks between the flipped 0.7027-0.7032 ceiling (SMA200 + 38.2% Fib) and the 10/20-day low (0.6939), with the 50% Fib (0.6962) holding Monday and returning Tuesday's bounce (+0.31%). The commodity engine still stands (CPI at 3.5%, WTI ~$83) and the arbiter arrives with Q3 CPI late October (≈Oct 28).",
                        take: "A unanimous hike sold in the statement and returned at the press conference: the market heard “hope” where the board said vigilance. Without a confirmed breakout in the 0.6939-0.7032 range there is no ticket — the Q3 CPI decides whether November's RBA gives the differential back to the aussie."
                    }
                },
                {
                    date: "06/10/2026",
                    category: "cb",
                    impact: "med",
                    pairs: ["USD/JPY", "EUR/JPY", "GBP/JPY"],
                    pt: {
                        headline: "As médias cruzam para baixo nos cruzamentos — e o preço encosta nos clusters: USD/JPY a 38 pips do teto que cortou o rali, GBP/JPY na Fib 78,6%",
                        summary: "A semana devolveu a devolução do iene: +0,77% no USD/JPY (para 158,09, a 38 pips do cluster Fib 50% + SMA200 158.27-158.47 que cortou o rali em 24/09) e +0,87% no GBP/JPY (209,89, a 3 pips da Fib 78,6% 209,85) — e o estrutural virou: a SMA50 passou sob a SMA200 nos dois pares, formalizando a leitura de baixa. O EUR/JPY cravou a mínima de 9 meses em 02/10 (176,98) e rejeitou em dois pregões (178,15). Mas formalizar não é operar: com o MoF na janela (rate checks + intervenção conjunta de julho), os pisos de 2,5σ20 (203/195/214 pips) mantêm os três pares em AGUARDAR — e o fim de outubro chega carregado: Fed em 27-28/10, 48h antes do BoJ (29-30/10, pausa esperada).",
                        take: "Cruzamento de médias com o preço encostado no cluster é o pior terreno para ticket: o piso de intervenção reprova os dois lados. O Fed decidindo 48h antes do BoJ é o roteiro do diferencial que manda — a mesa espera o cluster ceder ou a σ20 comprimir."
                    },
                    en: {
                        headline: "The averages cross bearish on the yen crosses — with price leaning on the clusters: USD/JPY 38 pips under the ceiling that cut the rip, GBP/JPY on the 78.6% Fib",
                        summary: "The week returned the yen's giveback: +0.77% on USD/JPY (to 158.09, 38 pips under the 50% Fib + SMA200 cluster 158.27-158.47 that cut the rip on Sep 24) and +0.87% on GBP/JPY (209.89, 3 pips off the 78.6% Fib 209.85) — and the structural flipped: the 50-day slipped under the SMA200 on both pairs, formalizing the bearish read. EUR/JPY pinned its 9-month low on Oct 2 (176.98) and rejected it in two sessions (178.15). But formalizing is not trading: with the MoF inside the window (rate checks + the July joint intervention), the 2.5-sigma20 floors (203/195/214 pips) keep all three pairs on WAIT — and late October arrives loaded: the Fed on Oct 27-28, 48h before the BoJ (Oct 29-30, a pause expected).",
                        take: "An averages cross with price leaning on the cluster is the worst ground for a ticket: the intervention floor rejects both sides. The Fed deciding 48h before the BoJ is the script of the differential that commands — the desk waits for the cluster to give way or sigma20 to compress."
                    }
                },
'''

# ---------------- HTML cards (news.html) ----------------
IMPACT_LABEL = {"high": ("High Impact", "Impacto Alto"), "med": ("Medium Impact", "Impacto Médio"), "low": ("Low Impact", "Impacto Baixo")}

def card2(num, cat_en, cat_pt, impact, date, title_en, title_pt, sum_en, sum_pt, take_en, take_pt, pairs):
    chips = "\n".join('                        <a href="%s.html" class="pair-link-chip">%s</a>' % (p.lower().replace("/", "-"), p) for p in pairs)
    return '''                <!-- News 06/10 %s: %s -->
                <article class="news-card">
                    <div class="news-card-top">
                        <span class="news-cat"><span class="lang-en">%s</span><span class="lang-pt" style="display:none;">%s</span></span>
                        <span class="impact-badge %s"><span class="lang-en">%s</span><span class="lang-pt" style="display:none;">%s</span></span>
                        <span class="news-date">%s</span>
                    </div>
                    <h2 class="news-title">
                        <span class="lang-en">%s</span>
                        <span class="lang-pt" style="display:none;">%s</span>
                    </h2>
                    <p class="news-summary">
                        <span class="lang-en">%s</span>
                        <span class="lang-pt" style="display:none;">%s</span>
                    </p>
                    <div class="news-take">
                        <span class="take-tag"><span class="lang-en">Desk take</span><span class="lang-pt" style="display:none;">Leitura da mesa</span></span>
                        <span class="lang-en">%s</span>
                        <span class="lang-pt" style="display:none;">%s</span>
                    </div>
                    <div class="news-pairs">
                        <span class="np-label"><span class="lang-en">Watch</span><span class="lang-pt" style="display:none;">Acompanhar</span></span>
%s
                    </div>
                </article>

''' % (num, title_en[:60], cat_en, cat_pt, impact, IMPACT_LABEL[impact][0], IMPACT_LABEL[impact][1], date,
       title_en, title_pt, sum_en, sum_pt, take_en, take_pt, chips)

# ---- index.html: prepend items to newsData (idempotent) ----
h = io.open(IDX, encoding="utf-8").read()
if h.count('date: "06/10/2026"') == 4:
    print("index.html: 4 newsData items already present, skipping")
else:
    marker = "        const newsData = {"
    i = h.find(marker)
    assert i != -1, "newsData not found"
    assert h.count('date: "06/10/2026"') == 0, "unexpected partial insertion"
    j = h.find("items: [", i)
    assert j != -1
    insert_at = j + len("items: [")
    h2 = h[:insert_at] + "\n\n" + JS_ITEMS.rstrip() + h[insert_at:]
    assert h2.count('date: "06/10/2026"') == 4
    io.open(IDX, "w", encoding="utf-8", newline="").write(h2)
    print("index.html: 4 newsData items prepended")

# ---- news.html ----
n = io.open(NEWS, encoding="utf-8").read()

def sub_once(s, old, new, label):
    assert s.count(old) == 1, (label, s.count(old))
    return s.replace(old, new)

n = sub_once(n, "Wire updated: 28/09/2026 22:15 UTC", "Wire updated: " + TS, "dateline EN")
n = sub_once(n, "Telégrafo atualizado em: 28/09/2026 22:15 UTC", "Telégrafo atualizado em: " + TS, "dateline PT")
n = sub_once(n,
    '<span class="cd-kicker"><span class="lang-en">Market Wire · Central Bank Week</span><span class="lang-pt" style="display:none;">Telégrafo da Mesa · Semana de Bancos Centrais</span></span>',
    '<span class="cd-kicker"><span class="lang-en">Market Wire · The Data-Vacuum Week</span><span class="lang-pt" style="display:none;">Telégrafo da Mesa · Semana do Vazio de Dados</span></span>',
    "kicker")
n = sub_once(n,
    '<span><span class="lang-en">6 pairs · 4 central banks in 8 days</span><span class="lang-pt" style="display:none;">6 pares · 4 bancos centrais em 8 dias</span></span>',
    '<span><span class="lang-en">6 pairs · Fed-ECB-BoJ inside 72h (27-30/10)</span><span class="lang-pt" style="display:none;">6 pares · Fed-BCE-BoJ em 72h (27-30/10)</span></span>',
    "hero sub-line")

old_cal = '''                <div class="cal-cell">
                    <span class="cal-date">28/09-02/10</span>
                    <span class="cal-event"><span class="lang-en">RBA week — two pullback tickets armed</span><span class="lang-pt" style="display:none;">Semana da RBA — dois tickets de repique armados</span></span>
                    <div class="cal-meta"><span class="cal-impact low" aria-hidden="true"></span><span class="cal-cur">FX</span></div>
                </div>
                <div class="cal-cell">
                    <span class="cal-date">29/09</span>
                    <span class="cal-event"><span class="lang-en">RBA decision</span><span class="lang-pt" style="display:none;">Decisão da RBA</span></span>
                    <div class="cal-meta"><span class="cal-impact med" aria-hidden="true"></span><span class="cal-cur">AUD</span></div>
                </div>
                <div class="cal-cell">
                    <span class="cal-date">≈13/10</span>
                    <span class="cal-event"><span class="lang-en">US CPI (Sep)</span><span class="lang-pt" style="display:none;">CPI dos EUA (set)</span></span>
                    <div class="cal-meta"><span class="cal-impact high" aria-hidden="true"></span><span class="cal-cur">USD</span></div>
                </div>'''
new_cal = '''                <div class="cal-cell">
                    <span class="cal-date">07/10</span>
                    <span class="cal-event"><span class="lang-en">FOMC minutes (Sep meeting)</span><span class="lang-pt" style="display:none;">Ata do FOMC (reunião de set)</span></span>
                    <div class="cal-meta"><span class="cal-impact low" aria-hidden="true"></span><span class="cal-cur">USD</span></div>
                </div>
                <div class="cal-cell">
                    <span class="cal-date">≈13/10</span>
                    <span class="cal-event"><span class="lang-en">US &amp; UK CPI (Sep) — delay risk</span><span class="lang-pt" style="display:none;">CPI EUA &amp; Reino Unido (set) — risco de atraso</span></span>
                    <div class="cal-meta"><span class="cal-impact high" aria-hidden="true"></span><span class="cal-cur">USD·GBP</span></div>
                </div>
                <div class="cal-cell">
                    <span class="cal-date">27-30/10</span>
                    <span class="cal-event"><span class="lang-en">Fed, ECB &amp; BoJ inside 72h</span><span class="lang-pt" style="display:none;">Fed, BCE e BoJ em 72h</span></span>
                    <div class="cal-meta"><span class="cal-impact high" aria-hidden="true"></span><span class="cal-cur">FX</span></div>
                </div>'''
n = sub_once(n, old_cal, new_cal, "calendar strip")

html_cards = "".join([
    card2("A", "Market Flow", "Fluxo &amp; Mercado", "high", "06/10/2026",
        "The book collects the sequence: the EUR/USD continuation runner closes at target for +1.27R at the Oct-1 close and the short re-arms one shelf above the 9-month low",
        "O livro cobra a sequência: corredor do EUR/USD encerra no alvo com +1,27R no fechamento de 01/10 e a venda rearma uma prateleira abaixo da mínima de 9 meses",
        "The Oct-1 close (1.1298) crossed the 1.1350 target of the continuation runner triggered on Sep 23 (Sep-19 edition — entry 1.1411, stop 1.1500) and closed the ticket at +1.27R (113 pips over the 89-pip risk), the public ledger's second target — and the chapter did not stop: the Oct-5 close (1.1204) pinned the 9-month low before Tuesday's bounce (+0.58%, to 1.1269; a fourth straight weekly down close). The desk re-arms one shelf below: a short on the pullback to the flipped 1.1340-1.1370 shelf (the handed-back September floor + the 1.1350 round + the 78.6% Fib 1.1369), stop 1.1412 (62 pips, over the 10-day high 1.1411), target 1.1200 — the round under the low — at 1:2.42, valid through Oct 9. The Sep-28 pullback ticket (1.1455-1.1500 shelf) expired unprinted and was revoked.",
        "O fechamento de 01/10 (1.1298) cruzou o alvo 1.1350 do corredor de continuação disparado em 23/09 (edição de 19/09 — entrada 1.1411, stop 1.1500) e encerrou o ticket em +1,27R (113 pips sobre os 89 pips de risco), o segundo alvo do ledger público — e o capítulo não parou: o fechamento de 05/10 (1.1204) cravou a mínima de 9 meses antes do repique de terça (+0,58%, para 1.1269; quarto fechamento semanal de queda seguido). A mesa rearma uma casa abaixo: venda no repique da prateleira virada 1.1340-1.1370 (o piso de setembro entregue + o redondo 1.1350 + a Fib 78,6% 1.1369), stop 1.1412 (62 pips, sobre a máxima de 10 pregões 1.1411), alvo 1.1200 — o redondo sob a mínima — a 1:2,42, válida até 09/10. O ticket de repique de 28/09 (prateleira 1.1455-1.1500) expirou sem imprimir e foi revogado.",
        "The shutdown suspended the data, not the flow: four weekly down closes with the dollar dominant even through the weak ISM. The rule does not chase a fresh low from 65 pips away — the next ticket only exists if the pullback delivers the close on the flipped shelf.",
        "O shutdown suspendeu os dados, não o fluxo: quatro semanas de fechamento semanal de queda com o dólar dominante mesmo com o ISM fraco. A regra não persegue mínima fresca a 65 pips de distância — o próximo ticket só existe se o repique entregar o fechamento na prateleira virada.",
        ["EUR/USD"]),
    card2("B", "Macro Data", "Dados Macro", "high", "06/10/2026",
        "Shutdown suspends NFP and CPI since Oct 1 — and the dollar dominates anyway: a weak ISM services buys no pause, EUR/USD under 1.1200",
        "Shutdown suspende NFP e CPI desde 01/10 — e o dólar domina mesmo assim: ISM services fraco não compra pausa, EUR/USD abaixo de 1,1200",
        "The fiscal blackout hit where it hurts: with the US government shutdown running since Oct 1, claims, NFP and CPI stay suspended — and September's CPI (≈Oct 13) runs delay risk. The flow asked for no license: the dollar swept the board on the week and EUR/USD's Oct-5 close (1.1204, a 9-month low) arrived even through September's weaker-than-expected ISM services (Oct 5, with price pressures mounting) — the differential (Fed at 3.75-4.00% with one more hike signaled) still commands more than the print. Tuesday returned the bounce (EUR/USD +0.58%, GBP/USD +0.39%, AUD/USD +0.31%) and Wednesday's FOMC minutes (Oct 7) are the desk's next text — with the Fed-ECB-BoJ cluster arriving Oct 27-30.",
        "O apagão fiscal chegou onde dói: com o shutdown do governo dos EUA desde 01/10, claims, NFP e CPI ficam suspensos — e o CPI de setembro (≈13/10) corre risco de atraso. O fluxo não pediu licença: na semana o dólar varreu o tabuleiro e o fechamento de 05/10 do EUR/USD (1.1204, mínima de 9 meses) veio mesmo com o ISM services de setembro mais fraco que o esperado (05/10, com pressão de preços subindo) — o diferencial (Fed a 3,75-4,00% com mais uma alta sinalizada) segue mandando mais que o dado. A terça devolveu o repique (EUR/USD +0,58%, GBP/USD +0,39%, AUD/USD +0,31%) e a ata do FOMC de quarta (07/10) é o próximo texto na mesa — com o cluster Fed-BCE-BoJ chegando em 27-30/10.",
        "An event filter without CPI is a blind filter: with the print under delay risk, the 24h window clings to what remains — the FOMC minutes (Oct 7) and the speeches. The desk keeps trading closes, not calendar promises.",
        "Filtro de eventos sem CPI é filtro cego: com o dado sob risco de atraso, a janela de 24h se apega ao que resta — a ata do FOMC (07/10) e os discursos. A mesa segue negociando fechamentos, não promessas de calendário.",
        ["EUR/USD", "GBP/USD", "AUD/USD"]),
    card2("C", "Central Banks", "Bancos Centrais", "high", "06/10/2026",
        "RBA delivers the unanimous hike to 4.60% — and Bullock's “hope” hands over the SMA200: the aussie turns neutral under the flipped 0.7027-0.7032 ceiling",
        "RBA entrega a alta unânime a 4,60% — e a “esperança” de Bullock entrega a SMA200: aussie vira neutro com o teto virado 0.7027-0.7032",
        "The decision came as consensus wanted it (Sep 29): a unanimous 25-bp hike to 4.60%, with hawkish statement language — but Bullock's line hoping the four hikes already delivered would be enough to bring inflation down took the next step out of the price: the pair barely moved on the announcement and the Sep-30 close (0.6968) handed over the SMA200 (0.7027), taking the bull alignment that had survived by 7 pips. The read turns NEUTRAL (close under the SMA200, 50-day 0.7092 above it) and the map locks between the flipped 0.7027-0.7032 ceiling (SMA200 + 38.2% Fib) and the 10/20-day low (0.6939), with the 50% Fib (0.6962) holding Monday and returning Tuesday's bounce (+0.31%). The commodity engine still stands (CPI at 3.5%, WTI ~$83) and the arbiter arrives with Q3 CPI late October (≈Oct 28).",
        "A decisão veio como o consenso pedia (29/09): alta unânime de 25 pb para 4,60%, com comunicado hawkish — mas a frase de Bullock esperando que as quatro altas já entregadas bastem para baixar a inflação tirou o próximo passo do preço: o par mal se mexeu no anúncio e o fechamento de 30/09 (0.6968) entregou a SMA200 (0.7027), com o alinhamento de alta que sobrevivia por 7 pips. A leitura vira NEUTRA (fechamento sob a SMA200, SMA50 0.7092 acima dela) e o mapa trava entre o teto virado 0.7027-0.7032 (SMA200 + Fib 38,2%) e a mínima de 10/20 pregões (0.6939), com a Fib 50% (0.6962) segurando a segunda e devolvendo o repique de terça (+0,31%). O motor commodity segue de pé (CPI a 3,5%, WTI ~US$ 83) e o árbitro chega com o CPI do Q3 no fim de outubro (≈28/10).",
        "A unanimous hike sold in the statement and returned at the press conference: the market heard “hope” where the board said vigilance. Without a confirmed breakout in the 0.6939-0.7032 range there is no ticket — the Q3 CPI decides whether November's RBA gives the differential back to the aussie.",
        "Alta unânime vendida no comunicado e devolvida na conferência: o mercado ouviu “esperança” onde o board dizia vigilância. Sem rompimento confirmado na faixa 0.6939-0.7032 não há ticket — o CPI do Q3 decide se a RBA de novembro devolve o diferencial ao aussie.",
        ["AUD/USD"]),
    card2("D", "Central Banks", "Bancos Centrais", "med", "06/10/2026",
        "The averages cross bearish on the yen crosses — with price leaning on the clusters: USD/JPY 38 pips under the ceiling that cut the rip, GBP/JPY on the 78.6% Fib",
        "As médias cruzam para baixo nos cruzamentos — e o preço encosta nos clusters: USD/JPY a 38 pips do teto que cortou o rali, GBP/JPY na Fib 78,6%",
        "The week returned the yen's giveback: +0.77% on USD/JPY (to 158.09, 38 pips under the 50% Fib + SMA200 cluster 158.27-158.47 that cut the rip on Sep 24) and +0.87% on GBP/JPY (209.89, 3 pips off the 78.6% Fib 209.85) — and the structural flipped: the 50-day slipped under the SMA200 on both pairs, formalizing the bearish read. EUR/JPY pinned its 9-month low on Oct 2 (176.98) and rejected it in two sessions (178.15). But formalizing is not trading: with the MoF inside the window (rate checks + the July joint intervention), the 2.5-sigma20 floors (203/195/214 pips) keep all three pairs on WAIT — and late October arrives loaded: the Fed on Oct 27-28, 48h before the BoJ (Oct 29-30, a pause expected).",
        "A semana devolveu a devolução do iene: +0,77% no USD/JPY (para 158,09, a 38 pips do cluster Fib 50% + SMA200 158.27-158.47 que cortou o rali em 24/09) e +0,87% no GBP/JPY (209,89, a 3 pips da Fib 78,6% 209,85) — e o estrutural virou: a SMA50 passou sob a SMA200 nos dois pares, formalizando a leitura de baixa. O EUR/JPY cravou a mínima de 9 meses em 02/10 (176,98) e rejeitou em dois pregões (178,15). Mas formalizar não é operar: com o MoF na janela (rate checks + intervenção conjunta de julho), os pisos de 2,5σ20 (203/195/214 pips) mantêm os três pares em AGUARDAR — e o fim de outubro chega carregado: Fed em 27-28/10, 48h antes do BoJ (29-30/10, pausa esperada).",
        "An averages cross with price leaning on the cluster is the worst ground for a ticket: the intervention floor rejects both sides. The Fed deciding 48h before the BoJ is the script of the differential that commands — the desk waits for the cluster to give way or sigma20 to compress.",
        "Cruzamento de médias com o preço encostado no cluster é o pior terreno para ticket: o piso de intervenção reprova os dois lados. O Fed decidindo 48h antes do BoJ é o roteiro do diferencial que manda — a mesa espera o cluster ceder ou a σ20 comprimir.",
        ["USD/JPY", "EUR/JPY", "GBP/JPY"]),
])

grid_marker = '            <div class="news-grid">'
k = n.find(grid_marker)
assert k != -1, "news-grid not found"
insert_at = k + len(grid_marker)
n = n[:insert_at] + "\n" + html_cards + n[insert_at:]
io.open(NEWS, "w", encoding="utf-8", newline="").write(n)
assert n.count('class="news-date">06/10/2026<') == 4
print("news.html: 4 cards prepended, hero + calendar updated ->", TS)
