#!/usr/bin/env python3
"""Daily regeneration for the 19/09/2026 edition — ECB/Frankfurter basis
(the logged-in MT5 terminal still returns no FX data; compute_indicators fell back).
Basis: ECB/Frankfurter reference rates, 545 sessions 01/08/2024-18/09/2026 (last close: 18/09/2026).
Saturday desk edition reviewing the central-bank week. Fed HIKED 25bp to 3.75-4.00% on 16/09
(unanimous, first hike in ~3 years, Warsh "inflation is too high", one more possible in 2026,
Dow -600). BoE held 3.75% on 17/09 (6-3, three hike dissents to 4%). BoJ hiked 25bp to 1.25% on
17-18/09 in a 7-2 vote whose dissent clouds further hikes — yen slid, Japan ran FX rate checks.
Closes: EUR/USD -0.18% to 1.1460 (4th down close, fresh 10/20-day low under the 78.6% Fib):
the 14/09 breakout short TRIGGERED at the 15/09 close (1.15389 < 1.1551, inside its own
post-FOMC reassessment clause) -> moves to OPEN (+1.29R toward 1.1440); new continuation ticket:
short a close < 1.1460, entry 1.1459, stop 1.1500 (41p >= 37p floor), target 1.1350 (109p, over
the 9-month low 1.1340), 1:2.66, valid through the 23/09 close. USD/JPY +1.41% to 157.89 — 10-day
high close reclaiming every September close: bear regime dead -> NEUTRAL (still under SMA200
158.36/SMA50 159.14), WAIT (2.5sigma floor 281p, MoF rate checks). GBP/USD -0.24% to 1.3344 —
7th down close, the 61.8% Fib 1.3411 invalidation printed 17/09: bias flips BULL->BEAR, but the
78.6%+round cluster at 1.3300/1.3301 pays ~1:1.1 and blocks the 1:2 path -> WAIT. AUD/USD +0.09%
to 0.7120: bull alignment intact, the broken 0.7141-0.7162 zone still blocks -> WAIT (RBA 29/09).
EUR/JPY +1.23% to 180.94: death cross stands but the rip closed at a 10-day high; floor 270p ->
WAIT. GBP/JPY +1.17% to 210.69: reclaim of 209.85/210.57 kills the bear read -> NEUTRAL, floor
340p -> WAIT. Verdicts: EUR/USD SELL breakout; the other five WAIT.
Also prepends 4 wire items (Fed/BoJ/BoE/book-flow) to the news digest + news.html, updates the
week-ahead calendar strip, and patches verify_all.py to the new stamp/ticker/stale dates.
Aborts on any structural mismatch."""
import re, json, sys
from datetime import datetime, timezone

DOCS = r"C:/Projetos/forex-report/docs"
TS_DATE = "19/09/2026"
now = datetime.now(timezone.utc)
TS = TS_DATE + " " + now.strftime("%H:%M") + " UTC"
OLD_TS = "14/09/2026 22:22 UTC"

BASIS_EN_AMP = "ECB/Frankfurter reference rates · SMA50/200, sigma20 &amp; Donchian computed · 545 daily sessions (01/08/2024–18/09/2026)."
BASIS_PT = "taxas de referência BCE/Frankfurter · SMA50/200, σ20 e Donchian calculados · 545 pregões (01/08/2024 a 18/09/2026)."

def rep(text, old, new, label, count=1):
    n = text.count(old)
    if n != count:
        print(f"FAIL [{label}]: expected {count} occurrence(s), found {n}")
        sys.exit(1)
    return text.replace(old, new)

def resub(text, pat, new, label, count=1, flags=re.DOTALL):
    out, n = re.subn(pat, new, text, flags=flags)
    if n != count:
        print(f"FAIL [{label}]: expected {count} match(es), found {n}")
        sys.exit(1)
    return out

# =====================================================================
# 1. forexData block (index.html)
# =====================================================================
FD = {
  "EUR/USD": {
    "quote": "1.1460", "bias": "BAIXA", "biasType": "bear",
    "pt": {
      "fundamental": "O EUR/USD fechou em 1,1460 na sessão de sexta 18/09/2026 (taxa de referência BCE/Frankfurter; edição de sábado 19/09 da mesa — o terminal MT5 logado segue sem retornar dados de FX), caindo -0,18% — quarta queda consecutiva, semana de -0,79%. A semana entregou o roteiro hawkish por completo: o FOMC subiu 25 pb para 3,75-4,00% em 16/09 (unânime, primeiro aumento em cerca de três anos, com Warsh dizendo que a inflação está alta demais e sinalizando mais uma alta ainda em 2026; Dow -600 pontos) contra um BCE parado em 2,50% desde 10/09 — o diferencial só se abre a favor do dólar. O livro já está posicionado: o curto de rompimento da edição de 14/09 disparou no fechamento de 15/09 (1,1539 sob a mínima de 1,1551, dentro da própria cláusula de reavaliação pós-FOMC) e roda a +1,29R rumo ao alvo 1.1440, stop 1.1600. O fechamento de sexta ainda varreu a Fib 78,6% (1,1476) e cravou nova mínima de 10/20 pregões — o mapa rearma a continuação uma casa abaixo. Alinhamento plenamente de baixa (fechamento sob a SMA200 1,1628, SMA50 1,1536 abaixo dela), com o preço 76 pips sob a SMA50. Indicadores (SMA 50/200, σ20, Donchian e Fibonacci) calculados da série diária BCE/Frankfurter (545 pregões, 01/08/2024 a 18/09/2026).",
      "trend": "Fechamento sob a SMA200 (1,1628) com a SMA50 (1,1536) abaixo dela — alinhamento de baixa pleno e o rompimento se aprofundando: quarta queda consecutiva, mínima sucessiva de 10/20 pregões (1,1460) e a Fib 78,6% (1,1476) varrida na sexta; a SMA50 (1,1536) virou o teto estrutural distante.",
      "support": "1.1460 é o próprio fechamento — mínima de 10/20 pregões —, com o redondo 1.1400 abaixo e a mínima de 9 meses (1.1340) como andar de baixo.",
      "resistance": "1.1500 (redondo sobre a Fib 78,6% devolvida, 1.1476), com o fechamento quebrado de 17/09 (1.1481) e a Fib 61,8% (1.1582) acima.",
      "priceAction": "Setup de continuação (o mapa rearma uma casa abaixo, com o corredor entregue): o gatilho é o próximo fechamento diário sob 1.1460 (entrada de referência 1.1459), stop 1.1500 (41 pips sobre o redondo e a Fib 78,6% devolvida; ≥ piso 1,5σ20 de ~37 pips), alvo 1.1350 (109 pips, imediatamente sobre a mínima de 9 meses 1.1340), cruzando apenas o redondo 1.1400. Fechamento de volta sobre 1.1500 cancela o mapa. O corredor da mesa (entrada no fechamento de 15/09 a 1,1539, stop 1.1600, alvo 1.1440) segue rodando — agora a +1,29R.",
      "recommendation": "VENDA (SHORT) NO ROMPIMENTO",
      "trigger": "Fechamento diário abaixo da mínima de 10 pregões 1.1460 — entrada de referência 1.1459. Válido até o fechamento de 23/09; sem evento de primeira linha na janela (próximo CPI dos EUA ≈13/10).",
      "stop": "1.1500 (sobre o redondo 1.1500 e a Fib 78,6% devolvida 1.1476; 41 pips ≥ piso 1,5σ20 de ~37 pips) · risco sugerido ≤ 1% por operação.",
      "target": "1.1350 (109 pips, imediatamente sobre a mínima de 9 meses 1.1340), com apenas o redondo 1.1400 no caminho.",
      "rr": "1:2.66", "rrValue": 66,
      "justification": "A semana entregou o comitê e o preço na mesma direção: alta unânime do Fed com sinalização de mais uma, BCE parado — e o corredor aberto no fechamento de 15/09 já paga +1,29R com o stop 1.1600 intacto. A regra não fica satisfeita com menos: a continuação exige seu próprio fechamento confirmatório sob 1,1460, paga 1:2,66 (109 pips contra 41) com stop estrutural sobre o redondo e a Fib devolvida, e mira a mínima de 9 meses com caminho limpo — só o redondo 1.1400. É posição adicional, não substituta do corredor — e só dispara se o preço entregar o fechamento."
    },
    "en": {
      "fundamental": "EUR/USD closed at 1.1460 in the Friday 18/09/2026 session (ECB/Frankfurter reference rate; Saturday 19/09 desk edition — the logged-in MT5 terminal still returns no FX data), down -0.18% — a fourth straight down close and a -0.79% week. The week delivered the hawkish script in full: the FOMC raised 25 bp to 3.75-4.00% on Sep 16 (unanimous, the first hike in about three years, with Warsh saying inflation is too high and signaling one more hike still this year; Dow -600 points) against an ECB frozen at 2.50% since Sep 10 — the differential only opens in the dollar's favor. The book is already positioned: the Sep-14 edition's breakout short triggered at the Sep-15 close (1.1539 under the 1.1551 low, inside its own post-FOMC reassessment clause) and runs at +1.29R toward the 1.1440 target, stop 1.1600. Friday's close also swept the 78.6% Fib (1.1476) and printed a fresh 10/20-day low — the map re-arms the continuation one shelf lower. Fully bearish alignment (close under the SMA200 1.1628, 50-day 1.1536 below it), price 76 pips under the 50-day. Indicators (SMA 50/200, sigma20, Donchian and Fibonacci) computed from the ECB/Frankfurter daily series (545 sessions, 01/08/2024 to 18/09/2026).",
      "trend": "Close under the 200-day SMA (1.1628) with the 50-day (1.1536) below it — full bear alignment and the breakdown deepening: a fourth straight down close, a fresh 10/20-day low (1.1460) and the 78.6% Fib (1.1476) swept on Friday; the 50-day SMA (1.1536) is now the distant structural ceiling.",
      "support": "1.1460 is the close itself — the 10/20-day low —, with the 1.1400 round beneath and the 9-month low (1.1340) as the lower floor.",
      "resistance": "1.1500 (the round over the handed-back 78.6% Fib, 1.1476), with the broken Sep-17 close (1.1481) and the 61.8% Fib (1.1582) above.",
      "priceAction": "Continuation setup (the book re-arms one shelf lower, with the runner delivered): the trigger is the next daily close under 1.1460 (entry reference 1.1459), stop 1.1500 (41 pips over the round and the handed-back 78.6% Fib; >= the ~37-pip 1.5-sigma20 floor), target 1.1350 (109 pips, just above the 9-month low 1.1340), crossing only the 1.1400 round. A close back over 1.1500 cancels the map. The desk's runner (entered at the Sep-15 close 1.1539, stop 1.1600, target 1.1440) keeps working — now at +1.29R.",
      "recommendation": "SELL (SHORT) ON BREAKOUT",
      "trigger": "Daily close under the 10-day low 1.1460 — entry reference 1.1459. Valid through the Sep 23 close; no top-tier event inside the window (next US CPI ≈Oct 13).",
      "stop": "1.1500 (over the 1.1500 round and the handed-back 78.6% Fib 1.1476; 41 pips >= the ~37-pip 1.5-sigma20 floor) · suggested risk ≤ 1% per trade.",
      "target": "1.1350 (109 pips, just above the 9-month low 1.1340), with only the 1.1400 round on the way.",
      "rr": "1:2.66", "rrValue": 66,
      "justification": "The week delivered the committee and the price in the same direction: a unanimous Fed hike with one more signaled, the ECB frozen — and the runner opened at the Sep-15 close already pays +1.29R with the 1.1600 stop untouched. The rule does not settle for less: the continuation demands its own confirming close under 1.1460, pays 1:2.66 (109 pips against 41) with a structural stop over the round and the handed-back Fib, and aims at the 9-month low over a clean path — only the 1.1400 round. It is an additive position, not a substitute for the runner — and it only fires if price delivers the close."
    }
  },
  "USD/JPY": {
    "quote": "157.89", "bias": "NEUTRO", "biasType": "neutral",
    "pt": {
      "fundamental": "O USD/JPY fechou em 157,89 na sessão de sexta 18/09/2026 (taxa de referência BCE/Frankfurter; edição de sábado 19/09), subindo +1,41% — o maior movimento dos seis pares e um fechamento em máxima de 10 pregões: o repique virou rompimento de verdade e varreu todos os fechamentos de setembro, incluindo a mínima quebrada de 03/09 (156.01). O motor foi o BoJ: alta de 25 pb para 1,25% (máxima de 31 anos) em votação 7-2 — a dissidência nubla os próximos passos, o mercado duvida de mais altas e o iene caiu; para completar, o Japão fez checagens de taxa (rate checks) no mercado cambial — o MoF está de plantão. Com o Fed a 3,75-4,00% e sinalizando mais uma alta em 2026, o diferencial segue a favor do dólar. Mas o mapa de baixa morreu: a leitura vira NEUTRA (fechamento ainda sob a SMA200 158,36 e a SMA50 159,14, que segue acima dela) e a geometria segue bloqueada — σ20 a 112 pips faz o piso de intervenção 2,5σ20 valer 281 pips: uma compra em 157,90 exigiria stop a ~154,90 (sob o redondo 155,00) e alvo a ~600 pips, encostando na máxima de 9 meses (163.91) e cruzando SMA200, SMA50, a máxima de 20 pregões (160.16) e as Fibs no caminho. Indicadores calculados da série diária BCE/Frankfurter (545 pregões, 01/08/2024 a 18/09/2026).",
      "trend": "O rompimento de baixa de setembro foi totalmente recuperado — fechamento acima de todos os fechamentos do mês, em máxima de 10 pregões —, mas o preço segue sob a SMA200 (158,36) e a SMA50 (159,14): alinhamento misto resolvido para NEUTRO, com o cluster Fib 50% + SMA200 (158,27-158,36) como teto imediato.",
      "support": "153.27 (mínima de 10/20 pregões), com a mínima de 9 meses (152.63) e o redondo 152.50 abaixo — 155.04 (Fib 78,6% + redondo) é a primeira defesa.",
      "resistance": "158.36 (SMA200 + Fib 50% 158,27 — cluster), com a Fib 38,2% (159,60), a SMA50 (159,14) e a máxima de 20 pregões (160.16) acima.",
      "priceAction": "Sem entrada — o piso de intervenção (2,5σ20 = 281 pips) reprova a compra: exigiria stop a ~154,90 e alvo a ~600 pips cruzando a escada SMA200/SMA50/Donchian 160,16 até encostar na máxima de 9 meses; a venda não tem estrutura depois de um fechamento em máxima de 10 pregões — e com o MoF fazendo rate checks, ficar na frente do interveniente é caro nos dois lados. Rearmar: fechamento sobre o cluster 158,27-158,36 com a Donchian 20 (160,16) cedendo e a σ20 comprimindo, ou rompimento falho de volta sob 155,69. Próximo BoJ no fim de outubro.",
      "recommendation": "AGUARDAR OUTRO GATILHO",
      "trigger": "Nenhum — o piso de intervenção (2,5σ20 = 281 pips) reprova a compra em máxima de 10 pregões e a venda não tem estrutura sob a escada das médias. Assistir ao cluster 158,27-158,36 e ao MoF; próximo BoJ no fim de outubro.",
      "stop": "N/A (sem operação).",
      "target": "N/A (sem operação).",
      "rr": "N/A", "rrValue": 0,
      "justification": "O BoJ entregou a alta e o mercado cuspiu o iene: 7-2 com dissidência é alta sem credibilidade — e o MoF respondeu com rate checks. O rompimento de baixa de setembro morreu recuperado e a leitura vira neutra, mas o relatório não paga para descobrir se a checagem vira intervenção nem para comprar iene fraco: com o piso de 281 pips, nenhuma geometria fecha 1:2 com caminho limpo. Neutro e fora, assistindo ao cluster da SMA200."
    },
    "en": {
      "fundamental": "USD/JPY closed at 157.89 in the Friday 18/09/2026 session (ECB/Frankfurter reference rate; Saturday 19/09 desk edition), up +1.41% — the biggest move of the six pairs and a 10-day high close: the bounce became a real breakout and swept every September close, including the broken Sep-3 low (156.01). The engine was the BoJ: a 25-bp hike to 1.25% (a 31-year high) in a 7-2 vote — the dissent clouds the next steps, the market doubts further hikes and the yen fell; to top it off, Japan ran rate checks in the FX market — the MoF is on watch. With the Fed at 3.75-4.00% and signaling one more hike this year, the differential stays in the dollar's favor. But the bear map is dead: the read turns NEUTRAL (close still under the SMA200 158.36 and the 50-day 159.14, which stays above it) and the geometry stays blocked — sigma20 at 112 pips puts the 2.5-sigma20 intervention floor at 281 pips: a long from 157.90 would need a stop at ~154.90 (under the 155.00 round) and a ~600-pip target, brushing the 9-month high (163.91) and crossing the SMA200, the SMA50, the 20-day high (160.16) and the Fibs on the way. Indicators computed from the ECB/Frankfurter daily series (545 sessions, 01/08/2024 to 18/09/2026).",
      "trend": "September's bear breakdown was fully reclaimed — a close above every September close, at a 10-day high —, but price stays under the SMA200 (158.36) and the 50-day (159.14): mixed alignment resolved to NEUTRAL, with the 50% Fib + SMA200 cluster (158.27-158.36) as the immediate ceiling.",
      "support": "153.27 (the 10/20-day low), with the 9-month low (152.63) and the 152.50 round beneath — 155.04 (78.6% Fib + round) is the first defense.",
      "resistance": "158.36 (SMA200 + 50% Fib 158.27 — a cluster), with the 38.2% Fib (159.60), the 50-day SMA (159.14) and the 20-day high (160.16) above.",
      "priceAction": "No entry — the intervention floor (2.5-sigma20 = 281 pips) rejects the long: it would demand a stop at ~154.90 and a ~600-pip target crossing the SMA200/SMA50/Donchian 160.16 ladder up to the 9-month high; a short has no structure after a 10-day high close — and with the MoF running rate checks, standing in front of the intervenor is expensive on both sides. Re-arm: a close over the 158.27-158.36 cluster with the 20-day Donchian (160.16) giving way and sigma20 compressing, or a failed breakout back under 155.69. Next BoJ late October.",
      "recommendation": "WAIT FOR ANOTHER TRIGGER",
      "trigger": "None — the intervention floor (2.5-sigma20 = 281 pips) rejects a long at a 10-day high and a short has no structure under the averages' ladder. Watch the 158.27-158.36 cluster and the MoF; next BoJ late October.",
      "stop": "N/A (no trade).",
      "target": "N/A (no trade).",
      "rr": "N/A", "rrValue": 0,
      "justification": "The BoJ delivered the hike and the market spat out the yen: 7-2 with dissent is a hike without credibility — and the MoF answered with rate checks. September's bear breakdown died reclaimed and the read turns neutral, but the report does not pay to find out whether the check becomes intervention, nor to buy weak yen: with the 281-pip floor, no geometry closes 1:2 over a clean path. Neutral and out, watching the SMA200 cluster."
    }
  },
  "AUD/USD": {
    "quote": "0.7120", "bias": "ALTA", "biasType": "bull",
    "pt": {
      "fundamental": "O AUD/USD fechou em 0,7120 na sessão de sexta 18/09/2026 (taxa de referência BCE/Frankfurter; edição de sábado 19/09), subindo +0,09% — o primeiro fechamento positivo em quatro pregões, parado a 6 pips da mínima de 10/20 pregões (0,7114, cravada na quinta). O Fed entregue (3,75-4,00%, com mais uma alta sinalizada para 2026) aperta o diferencial contra uma RBA parada a 4,35% — mas o motor aussie segue de pé: CPI australiano a 3,5%, WTI ~US$ 83 e bancos projetando 4,60% em novembro, com a reunião da RBA em 29/09 como o próximo árbitro. O alinhamento de alta segue intacto (SMA50 0,7084 > SMA200 0,7005; preço acima das duas) e a aritmética segue reprovada: da prateleira reprecificada 0.7084-0.7114 (SMA50 + Fib 23,6% 0,7102 + mínima de 10/20 pregões) com stop 0.7059 (49 pips ≥ piso 1,5σ20 de ~33 pips), a zona quebrada 0.7141-0.7162 paga ~1:1,5 e o único alvo de 1:2+ (0.7195-0.7204) segue além dela — obstáculo intermediário de primeira ordem, o mesmo veredito de 14/09. Indicadores calculados da série diária BCE/Frankfurter (545 pregões, 01/08/2024 a 18/09/2026).",
      "trend": "Acima das SMA50 (0,7084) e SMA200 (0,7005) — alinhamento de alta pleno; a sequência de três quedas travou sobre a mínima de 10/20 pregões (0,7114), com a Fib 23,6% (0,7102) e a SMA50 como prateleira.",
      "support": "0.7102 (Fib 23,6%), com a mínima de 10/20 pregões (0.7114) no piso imediato e a SMA50 (0.7084) logo abaixo.",
      "resistance": "0.7141 (piso quebrado da zona 0.7141-0.7162), com o nível entregue (0.7195-0.7204) e a máxima de 10/20 pregões (0.7225) acima.",
      "priceAction": "Sem entrada — o prêmio segue sob o portão: da prateleira 0.7084-0.7114 com stop 0.7059, a zona quebrada 0.7141-0.7162 paga ~1:1,5 e o único 1:2+ (0.7195-0.7204) segue além dela — obstáculo de primeira ordem no caminho. Rearmar: base sobre a prateleira com fechamento de volta sobre 0.7162, ou a RBA (29/09) reprecificando os alvos.",
      "recommendation": "AGUARDAR OUTRO GATILHO",
      "trigger": "Nenhum — o alvo estrutural mais próximo paga ~1:1,5 e o único acima de 1:2 (0.7195-0.7204) segue além da zona quebrada 0.7141-0.7162; a RBA (29/09) é o próximo árbitro.",
      "stop": "N/A (sem operação).",
      "target": "N/A (sem operação).",
      "rr": "N/A", "rrValue": 0,
      "justification": "O par fez o mínimo: travou a queda sobre a mínima de quinta sem entregar nem base nem quebra — e o portão de 1:2 segue fechado pela zona quebrada no caminho, como em 14/09. O diferencial apertou com o Fed entregue, o que reforça esperar a RBA: banco que projeta 4,60% em novembro não precisa ser antecipado por um ticket de 1:1,5. A vantagem segue com quem espera — e com a prateleira provando base."
    },
    "en": {
      "fundamental": "AUD/USD closed at 0.7120 in the Friday 18/09/2026 session (ECB/Frankfurter reference rate; Saturday 19/09 desk edition), up +0.09% — the first positive close in four sessions, sitting 6 pips above the 10/20-day low (0.7114, printed Thursday). The delivered Fed (3.75-4.00%, one more hike signaled for 2026) squeezes the differential against an RBA on hold at 4.35% — but the aussie engine stands: Australian CPI at 3.5%, WTI ~$83 and banks projecting 4.60% by November, with the RBA's Sep-29 meeting the next arbiter. The bull alignment stays intact (50-day 0.7084 > 200-day 0.7005; price above both) and the arithmetic stays rejected: from the re-priced 0.7084-0.7114 shelf (50-day + 23.6% Fib 0.7102 + the 10/20-day low) with a stop at 0.7059 (49 pips >= the ~33-pip 1.5-sigma20 floor), the broken 0.7141-0.7162 zone pays ~1:1.5 and the only 1:2+ target (0.7195-0.7204) still sits beyond it — a first-order intermediate block, the same verdict as Sep 14. Indicators computed from the ECB/Frankfurter daily series (545 sessions, 01/08/2024 to 18/09/2026).",
      "trend": "Above the 50-day (0.7084) and 200-day (0.7005) SMAs — full bull alignment; the three-session slide stalled on the 10/20-day low (0.7114), with the 23.6% Fib (0.7102) and the 50-day as the shelf.",
      "support": "0.7102 (23.6% Fib), with the 10/20-day low (0.7114) at the immediate floor and the 50-day SMA (0.7084) just beneath.",
      "resistance": "0.7141 (the broken floor of the 0.7141-0.7162 zone), with the handed-back level (0.7195-0.7204) and the 10/20-day high (0.7225) above.",
      "priceAction": "No entry — the premium stays under the gate: from the 0.7084-0.7114 shelf with a stop at 0.7059, the broken 0.7141-0.7162 zone pays ~1:1.5 and the only 1:2+ target (0.7195-0.7204) still sits beyond it — a first-order block on the way. Re-arm: a base over the shelf with a close back over 0.7162, or the RBA (Sep 29) re-pricing the targets.",
      "recommendation": "WAIT FOR ANOTHER TRIGGER",
      "trigger": "None — the nearest structural target pays ~1:1.5 and the only 1:2+ target (0.7195-0.7204) still sits beyond the broken 0.7141-0.7162 zone; the RBA (Sep 29) is the next arbiter.",
      "stop": "N/A (no trade).",
      "target": "N/A (no trade).",
      "rr": "N/A", "rrValue": 0,
      "justification": "The pair did the minimum: stalled the slide on Thursday's low while delivering neither a base nor a break — and the 1:2 gate stays shut by the broken zone on the way, as on Sep 14. The differential narrowed with the Fed delivered, which reinforces waiting for the RBA: a bank projected to reach 4.60% by November does not need to be front-run by a 1:1.5 ticket. The edge stays with whoever waits — and with the shelf proving a base."
    }
  },
  "GBP/USD": {
    "quote": "1.3344", "bias": "BAIXA", "biasType": "bear",
    "pt": {
      "fundamental": "O GBP/USD fechou em 1,3344 na sessão de sexta 18/09/2026 (taxa de referência BCE/Frankfurter; edição de sábado 19/09), caindo -0,24% — sétima queda consecutiva e semana de -1,11%. O BoE segurou os juros em 3,75% na quinta (17/09) em votação 6-3 — três dissidências por alta a 4%, tom hawkish —, mas o Fed entregue na véspera (3,75-4,00%, unânime, mais uma alta sinalizada) comprou o xadrez: o diferencial virou contra a libra e o preço entregou a invalidação que a edição de 14/09 marcava — o fechamento de 17/09 (1,3377) varreu a Fib 61,8% (1,3411) e a sexta cravou mínimas de 10/20 pregões. O viés vira BAIXA: o alinhamento formal segue misto (fechamento sob a SMA200 1,3451, SMA50 1,3480 acima dela), mas o rompimento confirmado resolve o misto para baixo — o mesmo critério aplicado ao USD/JPY em 07/09. A geometria, porém, reprova a entrada: da quebra (entrada 1.3343) com stop 1.3390 (47 pips ≥ piso 1,5σ20 de ~41 pips), o alvo estrutural mais próximo — o cluster Fib 78,6% + redondo (1.3300/1.3301) — paga ~1:1,1, e o caminho até o 1:2 (≤1.3249) atravessa o cluster: bloqueio de primeira ordem. Próximos árbitros: CPI do Reino Unido ≈13/10 e BoE em 05/11. Indicadores calculados da série diária BCE/Frankfurter (545 pregões, 01/08/2024 a 18/09/2026).",
      "trend": "Sétima queda consecutiva sob a SMA200 (1,3451) e sob a SMA50 (1,3480) — alinhamento formal misto, mas o rompimento confirmado das mínimas de 10/20 pregões (1,3344) com a Fib 61,8% (1,3411) varrida resolve a leitura para baixa: viés BAIXA.",
      "support": "1.3344 é o próprio fechamento — mínima de 10/20 pregões —, com o cluster Fib 78,6% + redondo (1.3300/1.3301) e o redondo 1.3250 abaixo; a mínima de 9 meses (1.3160) é o andar de baixo.",
      "resistance": "1.3411 (Fib 61,8% — a invalidez virada teto), com o fechamento quebrado de 17/09 (1.3377) e a confluência SMA200/SMA50 (1.3451-1.3480) acima.",
      "priceAction": "Sem entrada — a quebra existe, o prêmio não: de 1.3343 com stop 1.3390, o cluster 1.3300/1.3301 paga ~1:1,1 e esticar até o 1:2 (≤1.3249) atravessa o cluster de primeira ordem. Rearmar: fechamento sob 1.3300 (cluster varrido) reprecifica a venda para a mínima de 9 meses (1.3160); recuperação sobre 1.3411 devolve o mapa de alta. CPI do Reino Unido ≈13/10 e BoE em 05/11 arbitram.",
      "recommendation": "AGUARDAR OUTRO GATILHO",
      "trigger": "Nenhum — o cluster Fib 78,6% + redondo (1.3300/1.3301) bloqueia o caminho do 1:2 e o alvo mais próximo paga ~1:1,1; reavaliar em fechamento sob 1.3300 ou sobre 1.3411.",
      "stop": "N/A (sem operação).",
      "target": "N/A (sem operação).",
      "rr": "N/A", "rrValue": 0,
      "justification": "O viés virou, a entrada não veio: sete quedas seguidas entregaram a invalidez da estrutura de alta, mas o primeiro andar de suporte está perto demais — 43 pips abaixo do fechamento — para pagar 1:2 com stop aprovado no piso de volatilidade. O BoE hawkish em 6-3 é o detalhe que proíbe perseguição cega: se o CPI britânico esquentar, o cluster 1.3300 pode ser o piso do recuo, não o trampolim. A mesa espera o cluster ceder por fechamento — aí sim, com âncora na mínima de 9 meses."
    },
    "en": {
      "fundamental": "GBP/USD closed at 1.3344 in the Friday 18/09/2026 session (ECB/Frankfurter reference rate; Saturday 19/09 desk edition), down -0.24% — a seventh straight down close and a -1.11% week. The BoE held rates at 3.75% on Thursday (Sep 17) in a 6-3 vote — three dissents for a hike to 4%, a hawkish tone — but the delivered Fed the day before (3.75-4.00%, unanimous, one more hike signaled) won the chessboard: the differential turned against sterling and price delivered the invalidation the Sep-14 edition had marked — the Sep-17 close (1.3377) swept the 61.8% Fib (1.3411) and Friday printed fresh 10/20-day lows. The bias flips BEARISH: the formal alignment stays mixed (close under the SMA200 1.3451, 50-day 1.3480 above it), but the confirmed breakdown resolves the mix downward — the same criterion applied to USD/JPY on Sep 7. The geometry, though, rejects the entry: from the break (entry 1.3343) with a stop at 1.3390 (47 pips >= the ~41-pip 1.5-sigma20 floor), the nearest structural target — the 78.6% Fib + round cluster (1.3300/1.3301) — pays ~1:1.1, and the path to 1:2 (<=1.3249) crosses the cluster: a first-order block. Next arbiters: UK CPI ≈Oct 13 and the BoE on Nov 5. Indicators computed from the ECB/Frankfurter daily series (545 sessions, 01/08/2024 to 18/09/2026).",
      "trend": "A seventh straight down close under the SMA200 (1.3451) and the 50-day (1.3480) — formally mixed alignment, but the confirmed breakdown of the 10/20-day lows (1.3344) with the 61.8% Fib (1.3411) swept resolves the read bearish: BEAR bias.",
      "support": "1.3344 is the close itself — the 10/20-day low —, with the 78.6% Fib + round cluster (1.3300/1.3301) and the 1.3250 round beneath; the 9-month low (1.3160) is the lower floor.",
      "resistance": "1.3411 (61.8% Fib — the invalidation turned ceiling), with the broken Sep-17 close (1.3377) and the SMA200/SMA50 confluence (1.3451-1.3480) above.",
      "priceAction": "No entry — the break exists, the premium does not: from 1.3343 with a stop at 1.3390, the 1.3300/1.3301 cluster pays ~1:1.1 and stretching to 1:2 (<=1.3249) crosses the first-order cluster. Re-arm: a close under 1.3300 (the cluster swept) re-prices the short toward the 9-month low (1.3160); a reclaim over 1.3411 hands back the bull map. UK CPI ≈Oct 13 and the BoE on Nov 5 arbitrate.",
      "recommendation": "WAIT FOR ANOTHER TRIGGER",
      "trigger": "None — the 78.6% Fib + round cluster (1.3300/1.3301) blocks the 1:2 path and the nearest target pays ~1:1.1; reassess on a close under 1.3300 or over 1.3411.",
      "stop": "N/A (no trade).",
      "target": "N/A (no trade).",
      "rr": "N/A", "rrValue": 0,
      "justification": "The bias turned, the entry did not come: seven straight down closes delivered the bull structure's invalidation, but the first support shelf sits too close — 43 pips under the close — to pay 1:2 with a stop cleared by the volatility floor. A hawkish 6-3 BoE is the detail that forbids blind chasing: if UK CPI runs hot, the 1.3300 cluster may be the retreat's floor, not its springboard. The desk waits for the cluster to give way by close — then, and only then, with an anchor at the 9-month low."
    }
  },
  "EUR/JPY": {
    "quote": "180.94", "bias": "BAIXA", "biasType": "bear",
    "pt": {
      "fundamental": "O EUR/JPY fechou em 180,94 na sessão de sexta 18/09/2026 (taxa de referência BCE/Frankfurter; edição de sábado 19/09), subindo +1,23% — fechamento em máxima de 10 pregões no rastro do BoJ: alta de 25 pb para 1,25% em votação 7-2 cuja dissidência nubla os próximos passos — o mercado duvida de mais altas, o iene foi ao chão e o MoF respondeu com rate checks no cambial. O repique varreu a Fib 78,6% (180,49), o redondo 180,00 e a sequência de mínimas de 9 meses (178,59 → 178,52) — mas o cruzamento de baixa segue de pé: SMA50 183,55 sob a SMA200 184,12 e o preço sob as duas — alinhamento formalmente de baixa. A geometria segue bloqueada: σ20 a 108 pips faz o piso de intervenção 2,5σ20 valer 270 pips — uma venda exigiria alvo a ~540 pips (175,5x), território sem estrutura além dos redondos 178,00/177,50; e vender um fechamento em máxima de 10 pregões é perseguir. Indicadores calculados da série diária BCE/Frankfurter (545 pregões, 01/08/2024 a 18/09/2026).",
      "trend": "Fechamento sob a SMA200 (184,12) e sob a SMA50 (183,55), com a SMA50 sob a SMA200 (cruzamento de baixa de 14/09) — leitura de baixa formal, agora com um repique violento: máxima de 10 pregões (180,94) sobre a Fib 78,6% devolvida (180,49).",
      "support": "180.49 (Fib 78,6% devolvida) / redondo 180.00, com a mínima de 9 meses (178.52) e os redondos 178.00/177.50 abaixo.",
      "resistance": "182.04 (Fib 61,8%), com a SMA50 (183.55), a SMA200 (184.12) e a máxima de 20 pregões (185.91) acima.",
      "priceAction": "Sem entrada — direção formalmente de baixa, timing impossível: o piso de intervenção (2,5σ20 = 270 pips) manda procurar âncora a ~540 pips e não há; vender máxima de 10 pregões é perseguir o rastro do BoJ, e comprar contra o cruzamento de baixa com o MoF de plantão é aposta dupla. Rearmar: compressão da σ20 com fechamento de volta sob 179.85, ou reteste estruturado do cluster 182.04-183.55.",
      "recommendation": "AGUARDAR OUTRO GATILHO",
      "trigger": "Nenhum — o piso de intervenção (2,5σ20 = 270 pips) reprova a venda e a compra contradiz o cruzamento de baixa; assistir à reação no cluster 182.04-183.55 e ao MoF (próximo BoJ no fim de outubro).",
      "stop": "N/A (sem operação).",
      "target": "N/A (sem operação).",
      "rr": "N/A", "rrValue": 0,
      "justification": "O BoJ deu a alta e tirou a credibilidade da próxima — o pior combo para quem precisa de iene forte. O cruzamento de baixa segue no painel, mas o repique entregou máxima de 10 pregões e o piso de 270 pips não negocia: sem âncora a ~540 pips, sem ticket. Fora do mercado até o repique mostrar exaustão por fechamento ou a σ20 comprimir."
    },
    "en": {
      "fundamental": "EUR/JPY closed at 180.94 in the Friday 18/09/2026 session (ECB/Frankfurter reference rate; Saturday 19/09 desk edition), up +1.23% — a 10-day high close in the BoJ's wake: a 25-bp hike to 1.25% in a 7-2 vote whose dissent clouds the next steps — the market doubts further hikes, the yen hit the floor and the MoF answered with FX rate checks. The rip swept the 78.6% Fib (180.49), the 180.00 round and the sequence of 9-month lows (178.59 → 178.52) — but the bearish cross stands: 50-day 183.55 under the 200-day 184.12 with price under both — a formally bearish alignment. The geometry stays blocked: sigma20 at 108 pips puts the 2.5-sigma20 intervention floor at 270 pips — a short would need a target ~540 pips lower (175.5x), territory with no structure beyond the 178.00/177.50 rounds; and shorting a 10-day high close is chasing. Indicators computed from the ECB/Frankfurter daily series (545 sessions, 01/08/2024 to 18/09/2026).",
      "trend": "Close under the SMA200 (184.12) and the 50-day (183.55), with the 50-day under the 200-day (the Sep-14 bearish cross) — a formally bearish read, now with a violent rip: a 10-day high (180.94) over the handed-back 78.6% Fib (180.49).",
      "support": "180.49 (handed-back 78.6% Fib) / the 180.00 round, with the 9-month low (178.52) and the 178.00/177.50 rounds beneath.",
      "resistance": "182.04 (61.8% Fib), with the 50-day SMA (183.55), the SMA200 (184.12) and the 20-day high (185.91) above.",
      "priceAction": "No entry — formally bearish direction, impossible timing: the intervention floor (2.5-sigma20 = 270 pips) demands an anchor ~540 pips away and there is none; shorting a 10-day high is chasing the BoJ's wake, and buying against the bearish cross with the MoF on watch is a double bet. Re-arm: sigma20 compression with a close back under 179.85, or a structured retest of the 182.04-183.55 cluster.",
      "recommendation": "WAIT FOR ANOTHER TRIGGER",
      "trigger": "None — the intervention floor (2.5-sigma20 = 270 pips) rejects the short and a long contradicts the bearish cross; watch the reaction at the 182.04-183.55 cluster and the MoF (next BoJ late October).",
      "stop": "N/A (no trade).",
      "target": "N/A (no trade).",
      "rr": "N/A", "rrValue": 0,
      "justification": "The BoJ delivered the hike and took the credibility out of the next one — the worst combo for anyone needing a strong yen. The bearish cross stays on the board, but the rip printed a 10-day high and the 270-pip floor does not negotiate: no anchor ~540 pips down, no ticket. Out of the market until the rip shows exhaustion by close or sigma20 compresses."
    }
  },
  "GBP/JPY": {
    "quote": "210.69", "bias": "NEUTRO", "biasType": "neutral",
    "pt": {
      "fundamental": "O GBP/JPY fechou em 210,69 na sessão de sexta 18/09/2026 (taxa de referência BCE/Frankfurter; edição de sábado 19/09), subindo +1,17% — fechamento em máxima de 10 pregões que varreu a Fib 78,6% (209,85), o redondo 210,00 e a mínima quebrada de 03/09 (210.57): o regime de baixa de setembro morreu recuperado e a leitura vira NEUTRA (fechamento ainda sob a SMA200 213,00 e a SMA50 214,50, que segue acima dela). O motor é o mesmo dos outros cruzamentos: BoJ 7-2 para 1,25% com dissidência e dúvida sobre a próxima, iene ao chão, MoF em rate checks — com o agravante do BoE hawkish em 6-3 (3,75%, três votos por 4%): o carry reabre a favor do cruzamento. Geometria bloqueada: σ20 a 136 pips faz o piso 2,5σ20 valer 340 pips — uma compra exigiria stop a ~207,2 (sob a mínima de 9 meses 207.32) e alvo a ~680 pips, cruzando a escada Fib/SMA (211.84, 213.00-213.23, 214.50-63, 216.35) até o 217.5. Indicadores calculados da série diária BCE/Frankfurter (545 pregões, 01/08/2024 a 18/09/2026).",
      "trend": "O rompimento de baixa de setembro foi recuperado por fechamento (210,57 devolvido) — a leitura vira NEUTRA: preço sob a SMA200 (213,00) e a SMA50 (214,50), com a escada 61,8% (211,84) → SMA200 (213,00) + Fib 50% (213,23) → SMA50 (214,50) + Fib 38,2% (214,63) como teto múltiplo.",
      "support": "209.85 (Fib 78,6% devolvida) / redondo 209.00, com a mínima de 10/20 pregões (207.91) e a de 9 meses (207.32) abaixo.",
      "resistance": "211.84 (Fib 61,8%), com a SMA200 (213.00) + Fib 50% (213.23), a SMA50 (214.50) + Fib 38,2% (214.63) e a máxima de 20 pregões (217.07) acima.",
      "priceAction": "Sem entrada — o piso de intervenção (2,5σ20 = 340 pips) reprova a compra (stop a ~207,2 sob a mínima de 9 meses, alvo cruzando a escada inteira) e a venda não tem estrutura depois do regime de baixa morrer recuperado. Rearmar: compressão da σ20 ou reteste estruturado de 209.85-210.57.",
      "recommendation": "AGUARDAR OUTRO GATILHO",
      "trigger": "Nenhum — o piso de intervenção (2,5σ20 = 340 pips) reprova qualquer geometria; assistir à reação na escada 211.84-214.63 e ao MoF.",
      "stop": "N/A (sem operação).",
      "target": "N/A (sem operação).",
      "rr": "N/A", "rrValue": 0,
      "justification": "O cruzamento mais caro do livro ficou mais caro ainda: BoJ duvidoso joga o iene para baixo e BoE hawkish sustenta a libra — o carry reabre, e justamente por isso o MoF está de plantão com rate checks. Com o piso a 340 pips, a única geometria de compra atravessa quatro níveis de primeira ordem até o alvo. Neutro e fora — a recuperação matou o mapa de baixa, o piso mata o de alta."
    },
    "en": {
      "fundamental": "GBP/JPY closed at 210.69 in the Friday 18/09/2026 session (ECB/Frankfurter reference rate; Saturday 19/09 desk edition), up +1.17% — a 10-day high close that swept the 78.6% Fib (209.85), the 210.00 round and the broken Sep-3 low (210.57): September's bear regime died reclaimed and the read turns NEUTRAL (close still under the SMA200 213.00 and the 50-day 214.50, which stays above it). The engine is the same as the other crosses: a 7-2 BoJ to 1.25% with dissent and doubt about the next step, yen on the floor, MoF running rate checks — with the aggravation of a hawkish 6-3 BoE (3.75%, three votes for 4%): the carry re-opens in the cross's favor. Geometry blocked: sigma20 at 136 pips puts the 2.5-sigma20 floor at 340 pips — a long would need a stop at ~207.2 (under the 9-month low 207.32) and a ~680-pip target, crossing the Fib/SMA ladder (211.84, 213.00-213.23, 214.50-63, 216.35) all the way to 217.5. Indicators computed from the ECB/Frankfurter daily series (545 sessions, 01/08/2024 to 18/09/2026).",
      "trend": "September's bear breakdown was reclaimed by close (210.57 handed back) — the read turns NEUTRAL: price under the SMA200 (213.00) and the 50-day (214.50), with the 61.8% Fib (211.84) → SMA200 (213.00) + 50% Fib (213.23) → 50-day (214.50) + 38.2% Fib (214.63) ladder as a multiple ceiling.",
      "support": "209.85 (handed-back 78.6% Fib) / the 209.00 round, with the 10/20-day low (207.91) and the 9-month low (207.32) beneath.",
      "resistance": "211.84 (61.8% Fib), with the SMA200 (213.00) + 50% Fib (213.23), the 50-day (214.50) + 38.2% Fib (214.63) and the 20-day high (217.07) above.",
      "priceAction": "No entry — the intervention floor (2.5-sigma20 = 340 pips) rejects the long (a stop at ~207.2 under the 9-month low, a target crossing the whole ladder) and a short has no structure after the bear regime died reclaimed. Re-arm: sigma20 compression or a structured retest of 209.85-210.57.",
      "recommendation": "WAIT FOR ANOTHER TRIGGER",
      "trigger": "None — the intervention floor (2.5-sigma20 = 340 pips) rejects any geometry; watch the reaction on the 211.84-214.63 ladder and the MoF.",
      "stop": "N/A (no trade).",
      "target": "N/A (no trade).",
      "rr": "N/A", "rrValue": 0,
      "justification": "The book's priciest cross got pricier still: a doubted BoJ floors the yen and a hawkish BoE holds sterling — the carry re-opens, and precisely because of it the MoF is on watch with rate checks. With the floor at 340 pips, the only long geometry crosses four first-order levels to reach its target. Neutral and out — the reclaim killed the bear map, the floor kills the bull one."
    }
  }
}

fd_json = json.dumps(FD, ensure_ascii=False, indent=8)

P = DOCS + "/index.html"
html = open(P, encoding="utf-8").read()

html, n = re.subn(r"        const forexData = \{.*?\n\};",
                  "        const forexData = " + fd_json + ";", html, count=1, flags=re.DOTALL)
if n != 1:
    print("FAIL: forexData block"); sys.exit(1)

html = rep(html, "Reports generated on: " + OLD_TS, "Reports generated on: " + TS, "ts en badge+i18n", count=2)
html = rep(html, 'generatedAt: "Relatórios gerados em: ' + OLD_TS + '"', 'generatedAt: "Relatórios gerados em: ' + TS + '"', "ts pt i18n")
html = rep(html, 'dataBasis: "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 541 daily sessions (01/08/2024–14/09/2026).",',
                 'dataBasis: "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 545 daily sessions (01/08/2024–18/09/2026).",', "basis en")
html = rep(html, 'dataBasis: "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, σ20 e Donchian calculados · 541 pregões (01/08/2024 a 14/09/2026).",',
                 'dataBasis: "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, σ20 e Donchian calculados · 545 pregões (01/08/2024 a 18/09/2026).",', "basis pt")

html, n = re.subn(
    r"        const dailyChanges = \{.*?\n        \};",
    '''        const dailyChanges = {
            "EUR/USD": "-0.18%",
            "USD/JPY": "+1.41%",
            "AUD/USD": "+0.09%",
            "GBP/USD": "-0.24%",
            "EUR/JPY": "+1.23%",
            "GBP/JPY": "+1.17%"
        };''', html, count=1, flags=re.DOTALL)
if n != 1:
    print("FAIL: dailyChanges"); sys.exit(1)

html, n = re.subn(
    r"        const macroDrivers = \{.*?\n        \};",
    '''        const macroDrivers = {
            "EUR/USD": {
                en: ["Fed hiked to 3.75-4.00%", "Runner short +1.29R", "New short < 1.1460"],
                pt: ["Fed subiu a 3,75-4,00%", "Curta rodando +1,29R", "Nova venda < 1,1460"]
            },
            "USD/JPY": {
                en: ["BoJ 1.25% by 7-2", "MoF rate checks", "2.5σ floor 281p"],
                pt: ["BoJ 1,25% por 7-2", "MoF em checagem", "Piso 2,5σ 281p"]
            },
            "AUD/USD": {
                en: ["Bull alignment intact", "0.7141-0.7162 caps", "RBA Sep 29"],
                pt: ["Alinhamento de alta intacto", "Zona 0,7141-0,7162 capa", "RBA 29/09"]
            },
            "GBP/USD": {
                en: ["61.8% Fib swept", "Bias flips to bear", "BoE 5/11"],
                pt: ["Fib 61,8% varrida", "Viés vira baixa", "BoE 5/11"]
            },
            "EUR/JPY": {
                en: ["Death cross stands", "10-day high rip", "2.5σ floor 270p"],
                pt: ["Cruzamento de baixa segue", "Repique máx. 10 preg.", "Piso 2,5σ 270p"]
            },
            "GBP/JPY": {
                en: ["Bear regime reclaimed", "Read flips neutral", "2.5σ floor 340p"],
                pt: ["Regime de baixa recuperado", "Leitura vira neutra", "Piso 2,5σ 340p"]
            }
        };''', html, count=1, flags=re.DOTALL)
if n != 1:
    print("FAIL: macroDrivers"); sys.exit(1)

# ---- news wire digest (newsData): update stamp + prepend the 19/09 items ----
html = rep(html, 'updated: "' + OLD_TS + '",', 'updated: "' + TS + '",', "newsData.updated")

NEWS_ITEMS = '''                {
                    date: "19/09/2026",
                    category: "cb",
                    impact: "high",
                    pairs: ["EUR/USD", "AUD/USD", "GBP/USD"],
                    pt: {
                        headline: "Fed entrega a alta unânime para 3,75-4,00% e sinaliza mais uma ainda em 2026; dólar varre o tabuleiro",
                        summary: "O FOMC de 15-16/09 fechou a semana dos bancos centrais: alta unânime de 25 pb para 3,75-4,00% — a primeira em cerca de três anos —, com o presidente Warsh dizendo que a inflação está alta demais e sinalizando mais uma alta ainda em 2026; o Dow caiu mais de 600 pontos na sequência. Contra um BCE parado em 2,50% e um BoE que só segurou os juros (3,75%, 6-3), o diferencial virou matéria-prima do dólar: o EUR/USD fechou a semana em 1,1460 (quarta queda seguida, mínima de 10/20 pregões) com o corredor de venda da mesa rodando a +1,29R rumo a 1.1440 — e um novo ticket de continuação armado sob 1.1460 (stop 1.1500, alvo 1.1350, 1:2,66); o AUD/USD travou a queda sobre 0,7114 e segue em AGUARDAR até a RBA (29/09).",
                        take: "O livro entrou na semana curto do EUR/USD no fechamento de 15/09 — e o comitê confirmou o mapa em vez de desmenti-lo: alta entregue, sinalização de mais uma, o dólar cobrou dos dois lados do Atlântico. A mesa não persegue: a continuação exige seu próprio fechamento sob 1,1460."
                    },
                    en: {
                        headline: "Fed delivers a unanimous hike to 3.75-4.00% and signals one more this year; the dollar sweeps the board",
                        summary: "The Sep 15-16 FOMC closed the central-bank week: a unanimous 25-bp hike to 3.75-4.00% — the first in about three years — with Chair Warsh saying inflation is too high and signaling one more hike still this year; the Dow fell more than 600 points in the follow-through. Against an ECB frozen at 2.50% and a BoE that merely held (3.75%, 6-3), the differential became the dollar's raw material: EUR/USD closed the week at 1.1460 (a fourth straight down close, a fresh 10/20-day low) with the desk's short runner working at +1.29R toward 1.1440 — and a new continuation ticket armed under 1.1460 (stop 1.1500, target 1.1350, 1:2.66); AUD/USD stalled the slide at 0.7114 and stays on WAIT until the RBA (Sep 29).",
                        take: "The book entered the week short EUR/USD from the Sep-15 close — and the committee confirmed the map instead of refuting it: hike delivered, one more signaled, the dollar collected on both sides of the Atlantic. The desk does not chase: the continuation demands its own close under 1.1460."
                    }
                },
                {
                    date: "19/09/2026",
                    category: "cb",
                    impact: "high",
                    pairs: ["USD/JPY", "EUR/JPY", "GBP/JPY"],
                    pt: {
                        headline: "BoJ sobe a 1,25% por 7-2 e a dissidência derruba o iene: máximas de 10 pregões nos três cruzamentos e o MoF faz rate checks",
                        summary: "O BoJ entregou os 25 pb (1,25%, máxima de 31 anos) em 17-18/09, mas a votação 7-2 com dissidência e sinais mistos nublou a próxima alta — o mercado duvida do compromisso e o iene foi o pior do tabuleiro: USD/JPY +1,41% na sexta para 157,89 (fechamento em máxima de 10 pregões, recuperando todos os fechamentos de setembro, incluindo a mínima quebrada de 03/09, 156.01), EUR/JPY 180,94 (+1,23%) e GBP/JPY 210,69 (+1,17%), ambos em máximas de 10 pregões. Para completar, o Japão fez checagens de taxa no mercado cambial — o MoF em alerta máximo desde a intervenção conjunta de julho. Os pisos de 2,5σ20 (281/270/340 pips) mantêm os três pares em AGUARDAR: os rompimentos de baixa de setembro morreram recuperados (leitura neutra no USD/JPY e no GBP/JPY), mas nenhuma geometria fecha 1:2 com caminho limpo na frente do interveniente.",
                        take: "Alta sem credibilidade é o pior resultado para uma moeda: o BoJ pagou 25 pb e o mercado cobrou de volta em iene — com o MoF fazendo rate checks, a mesa não fica do lado de dentro da sala de máquinas. Os três cruzamentos viram neutros ou travados; o próximo BoJ só no fim de outubro."
                    },
                    en: {
                        headline: "BoJ hikes to 1.25% by 7-2 and the dissent floors the yen: 10-day high closes across all three crosses as the MoF runs rate checks",
                        summary: "The BoJ delivered the 25 bp (1.25%, a 31-year high) on Sep 17-18, but the 7-2 vote with dissent and mixed signals clouded the next hike — the market doubts the commitment and the yen was the board's worst: USD/JPY +1.41% Friday to 157.89 (a 10-day high close, reclaiming every September close including the broken Sep-3 low, 156.01), EUR/JPY 180.94 (+1.23%) and GBP/JPY 210.69 (+1.17%), both at 10-day highs. To top it off, Japan ran rate checks in the FX market — the MoF on maximum alert since the July joint intervention. The 2.5-sigma20 floors (281/270/340 pips) keep all three pairs on WAIT: September's bear breakdowns died reclaimed (a neutral read on USD/JPY and GBP/JPY), but no geometry closes 1:2 over a clean path in front of the intervenor.",
                        take: "A hike without credibility is the worst outcome for a currency: the BoJ paid 25 bp and the market took it back in yen — with the MoF running rate checks, the desk does not stand inside the machine room. All three crosses turn neutral or blocked; the next BoJ only in late October."
                    }
                },
                {
                    date: "19/09/2026",
                    category: "cb",
                    impact: "med",
                    pairs: ["GBP/USD"],
                    pt: {
                        headline: "BoE segura 3,75% em 6-3 com três votos por alta — hawkish, mas o Fed entregue comprou o xadrez e o cable entrega a invalidez",
                        summary: "O BoE manteve os juros em 3,75% na quinta (17/09) em votação 6-3 — as três dissidências pediram alta a 4%, e o tom seguiu apertando segundo a imprensa. Não bastou: 24h depois do Fed entregar 3,75-4,00% com mais uma alta sinalizada, o diferencial virou contra a libra e o preço mandou o recado — sétima queda consecutiva do cable, fechamento em 1,3344, com o fechamento de 17/09 varrendo a Fib 61,8% (1,3411) que a edição de 14/09 marcava como invalidez da estrutura de alta. O viés vira baixa, mas a mesa não persegue: o cluster Fib 78,6% + redondo (1.3300/1.3301) paga ~1:1,1 da quebra e bloqueia o caminho do 1:2 — rearmar em fechamento sob 1.3300 (alvo reprecificado na mínima de 9 meses, 1.3160) ou recuperação sobre 1.3411. Próximos árbitros: CPI do Reino Unido ≈13/10 e BoE em 05/11.",
                        take: "Hold hawkish contra hike entregue é derrota por seleção: o BoE subiu o tom e mesmo assim perdeu o diferencial para o Fed — o cable pagou com a estrutura de alta. A mesa virou o viés, manteve a disciplina: nada de vender dentro do cluster; o ticket só existe se o 1.3300 ceder por fechamento."
                    },
                    en: {
                        headline: "BoE holds 3.75% at 6-3 with three hike votes — hawkish, but the delivered Fed won the chessboard and cable hands over the invalidation",
                        summary: "The BoE kept rates at 3.75% on Thursday (Sep 17) in a 6-3 vote — the three dissents called for a hike to 4%, and the tone kept tightening per the press. It was not enough: 24h after the Fed delivered 3.75-4.00% with one more hike signaled, the differential turned against sterling and price sent the message — cable's seventh straight down close at 1.3344, with the Sep-17 close sweeping the 61.8% Fib (1.3411) the Sep-14 edition had marked as the bull structure's invalidation. The bias turns bear, but the desk does not chase: the 78.6% Fib + round cluster (1.3300/1.3301) pays ~1:1.1 from the break and blocks the 1:2 path — re-arm on a close under 1.3300 (target re-priced to the 9-month low, 1.3160) or a reclaim over 1.3411. Next arbiters: UK CPI ≈Oct 13 and the BoE on Nov 5.",
                        take: "A hawkish hold against a delivered hike is a loss by selection: the BoE raised its tone and still lost the differential to the Fed — cable paid with the bull structure. The desk flipped the bias and kept the discipline: no selling inside the cluster; the ticket only exists if 1.3300 gives way by close."
                    }
                },
                {
                    date: "19/09/2026",
                    category: "flow",
                    impact: "high",
                    pairs: ["EUR/USD"],
                    pt: {
                        headline: "O livro na semana dos bancos centrais: corredor de venda disparado no fechamento de 15/09 roda a +1,29R; três vieses viram",
                        summary: "Semana de três decisões, um disparo e três vieses novos. O curto de rompimento do EUR/USD (armado na edição de 14/09) disparou no fechamento de 15/09 (1,1539 sob a mínima de 1,1551, dentro da própria cláusula de reavaliação pós-FOMC — o comitê confirmou) e roda a +1,29R rumo ao alvo 1.1440 com o stop 1.1600 intacto; a mesa rearma a continuação: fechamento sob 1.1460, stop 1.1500, alvo 1.1350 (1:2,66). No tabuleiro: GBP/USD vira de alta para baixa (invalidez entregue), USD/JPY e GBP/JPY viram de baixa para neutros (os rompimentos de setembro recuperados por fechamento), EUR/JPY segue baixa travado no piso de intervenção e AUD/USD segue alta travado na zona quebrada 0.7141-0.7162 — cinco dos seis pares em AGUARDAR, o dólar na frente.",
                        take: "O relatório terminou a semana com o que buscou ao entrá-la: um corredor rodando na direção do macro e cinco mapas travados por geometria — pisos de intervenção nos cruzamentos, cluster de primeira ordem no cable, zona quebrada no aussie. Disciplina paga; o próximo teste é a RBA (29/09)."
                    },
                    en: {
                        headline: "The book in the central-bank week: the short runner triggered at the Sep-15 close works at +1.29R; three biases flip",
                        summary: "A week of three decisions, one trigger and three new biases. The EUR/USD breakout short (armed in the Sep-14 edition) fired at the Sep-15 close (1.1539 under the 1.1551 low, inside its own post-FOMC reassessment clause — the committee confirmed) and runs at +1.29R toward the 1.1440 target with the 1.1600 stop intact; the desk re-arms the continuation: a close under 1.1460, stop 1.1500, target 1.1350 (1:2.66). On the board: GBP/USD flips bull to bear (the invalidation delivered), USD/JPY and GBP/JPY flip bear to neutral (September's breakdowns reclaimed by close), EUR/JPY stays bear blocked at the intervention floor and AUD/USD stays bull blocked at the broken 0.7141-0.7162 zone — five of six pairs on WAIT, the dollar in front.",
                        take: "The report ended the week with what it sought entering it: one runner working in the macro's direction and five maps blocked by geometry — intervention floors on the crosses, a first-order cluster on cable, a broken zone on the aussie. Discipline pays; the next test is the RBA (Sep 29)."
                    }
                },
'''
html = rep(html, '            items: [\n                {\n                    date: "14/09/2026"',
            "            items: [\n" + NEWS_ITEMS + "                {\n                    date: \"14/09/2026\"", "newsData item prepend")

open(P, "w", encoding="utf-8").write(html)
print(f"OK: index.html (forexData, 3 timestamps, basis, ticker, macroDrivers, news digest) — stamp {TS}")

# =====================================================================
# 2. Static pages
# =====================================================================
PAGE = {"EUR/USD": "eur-usd.html", "USD/JPY": "usd-jpy.html", "AUD/USD": "aud-usd.html",
        "GBP/USD": "gbp-usd.html", "EUR/JPY": "eur-jpy.html", "GBP/JPY": "gbp-jpy.html"}

def update_page(pair, fname, d, gauge_pct, sup_txt, res_txt, chips, next_ev, tier, tier_cls, bar_on, badge, badge_cls):
    p = f"{DOCS}/{fname}"
    h = open(p, encoding="utf-8").read()
    tag = fname
    # quote
    h = resub(h, r"(<h2 class=\"pair-name\">" + re.escape(pair) + r"</h2>.*?<strong>)[\d.]+(</strong>)",
              r"\g<1>" + d["quote"] + r"\g<2>", f"{tag} quote")
    # data basis + macro chips + next event + ts-date + rr-seal
    h = resub(h, r"<div class=\"data-basis\">.*?</div>",
              '<div class="data-basis"><span class="db-tag"><span class="lang-en">Basis</span><span class="lang-pt" style="display:none;">Base</span>:</span> <span class="lang-en">' + BASIS_EN_AMP + '</span><span class="lang-pt" style="display:none;">' + BASIS_PT + "</span></div>",
              f"{tag} basis")
    h = resub(h, r"<div class=\"macro-chips\">.*?</div>", chips, f"{tag} macro-chips")
    h = resub(h, r"<div class=\"next-event\">.*?</div>", next_ev, f"{tag} next-event")
    h = rep(h, '<span class="ts-date">14·09·26</span>', '<span class="ts-date">19·09·26</span>', f"{tag} ts-date")
    h = resub(h, r"<span class=\"rr-seal\">[^<]+</span>", '<span class="rr-seal">' + d["pt"]["rr"] + "</span>", f"{tag} rr-seal")
    # BLUF
    h = resub(h, r"<span class=\"lang-en\"><span class=\"bluf-action \w+\">\w+</span>[^<]*</span>",
              d["_bluf_en"], f"{tag} bluf en")
    h = resub(h, r"<span class=\"lang-pt\" style=\"display:none;\"><span class=\"bluf-action \w+\">\w+</span>[^<]*</span>",
              d["_bluf_pt"], f"{tag} bluf pt")
    # conviction tier + bar
    h = resub(h, r"<span class=\"conv-tier[^\"]*\">\d+/10 &middot; <span class=\"lang-en\">\w+</span><span class=\"lang-pt\" style=\"display:none;\">\w+</span></span>",
              f'<span class="conv-tier {tier_cls}">{tier} &middot; <span class="lang-en">' + d["_tier_en"] + '</span><span class="lang-pt" style="display:none;">' + d["_tier_pt"] + "</span></span>",
              f"{tag} tier")
    h = resub(h, r"<div class=\"conv-bar\">.*?</div>",
              '<div class="conv-bar">' + "".join('<i class="on"></i>' for _ in range(bar_on)) + "".join("<i></i>" for _ in range(10 - bar_on)) + "</div>",
              f"{tag} bar")
    # fundamental
    h = resub(h, r"<div class=\"section-content lang-en\">.*?</div>",
              '<div class="section-content lang-en">' + d["en"]["fundamental"] + "</div>", f"{tag} fundamental en")
    h = resub(h, r"<div class=\"section-content lang-pt\" style=\"display:none;\">.*?</div>",
              '<div class="section-content lang-pt\" style=\"display:none;\">' + d["pt"]["fundamental"] + "</div>", f"{tag} fundamental pt")
    # trend
    h = resub(h, r"<div class=\"tech-box-value lang-en\">.*?</div>",
              '<div class="tech-box-value lang-en">' + d["en"]["trend"] + "</div>", f"{tag} trend en")
    h = resub(h, r"<div class=\"tech-box-value lang-pt\" style=\"display:none;\">.*?</div>",
              '<div class="tech-box-value lang-pt" style="display:none;">' + d["pt"]["trend"] + "</div>", f"{tag} trend pt")
    # support / resistance strongs (ordered: support first, resistance second)
    strongs_en = re.findall(r"<strong class=\"lang-en\">[^<]*</strong>", h)
    strongs_pt = re.findall(r"<strong class=\"lang-pt\" style=\"display:none;\">[^<]*</strong>", h)
    if len(strongs_en) != 2 or len(strongs_pt) != 2:
        print(f"FAIL [{tag} strongs]: en={len(strongs_en)} pt={len(strongs_pt)}"); sys.exit(1)
    h = h.replace(strongs_en[0], '<strong class="lang-en">' + d["en"]["support"] + "</strong>", 1)
    h = h.replace(strongs_en[1], '<strong class="lang-en">' + d["en"]["resistance"] + "</strong>", 1)
    h = h.replace(strongs_pt[0], '<strong class="lang-pt" style="display:none;">' + d["pt"]["support"] + "</strong>", 1)
    h = h.replace(strongs_pt[1], '<strong class="lang-pt" style="display:none;">' + d["pt"]["resistance"] + "</strong>", 1)
    # gauge
    h = resub(h, r"(<div class=\"range-gauge-now\" style=\"left: )\d+%(;\">)[\d.]+(</div>)",
              r"\g<1>" + gauge_pct + r"%\g<2>" + d["quote"] + r"\g<3>", f"{tag} gauge now")
    h = resub(h, r"(<div class=\"range-gauge-marker\" style=\"left: )\d+%(;\"></div>)",
              r"\g<1>" + gauge_pct + r"%\g<2>", f"{tag} gauge marker")
    h = resub(h, r"<span class=\"rgv-l\">[\d.]+</span>", '<span class="rgv-l">' + sup_txt + "</span>", f"{tag} rgv-l")
    h = resub(h, r"<span class=\"rgv-r\">[\d.]+</span>", '<span class="rgv-r">' + res_txt + "</span>", f"{tag} rgv-r")
    # price action
    h = resub(h, r"<div class=\"section-content lang-en\" style=\"font-size: 0\.9rem;\">.*?</div>",
              '<div class="section-content lang-en" style="font-size: 0.9rem;">' + d["en"]["priceAction"] + "</div>", f"{tag} pa en")
    h = resub(h, r"<div class=\"section-content lang-pt\" style=\"display:none; font-size: 0\.9rem;\">.*?</div>",
              '<div class="section-content lang-pt" style="display:none; font-size: 0.9rem;">' + d["pt"]["priceAction"] + "</div>", f"{tag} pa pt")
    # verdict badge (class + labels) + ticket class — set the class per today's verdict
    if badge:
        h = resub(h, r"<span class=\"verdict-badge \w+\">\s*<span class=\"lang-en\">[^<]*</span>\s*<span class=\"lang-pt\" style=\"display:none;\">[^<]*</span>\s*</span>",
                  badge, f"{tag} verdict badge")
    for old_cls, new_cls in badge_cls:
        h = rep(h, f'class="trade-ticket verdict-{old_cls}"', f'class="trade-ticket verdict-{new_cls}"', f"{tag} ticket cls")
    # trigger / stop / target (ordered)
    vals_en = re.findall(r"<div class=\"setup-card-value lang-en\">.*?</div>", h)
    vals_pt = re.findall(r"<div class=\"setup-card-value lang-pt\" style=\"display:none;\">.*?</div>", h)
    if len(vals_en) != 3 or len(vals_pt) != 3:
        print(f"FAIL [{tag} card values]: en={len(vals_en)} pt={len(vals_pt)}"); sys.exit(1)
    for i, k in enumerate(("trigger", "stop", "target")):
        h = h.replace(vals_en[i], '<div class="setup-card-value lang-en">' + d["en"][k] + "</div>", 1)
        h = h.replace(vals_pt[i], '<div class="setup-card-value lang-pt" style="display:none;">' + d["pt"][k] + "</div>", 1)
    # justification
    h = resub(h, r"<div class=\"section-content lang-en\" style=\"font-size: 0\.9rem; font-style: italic;\">.*?</div>",
              '<div class="section-content lang-en" style="font-size: 0.9rem; font-style: italic;">' + d["en"]["justification"] + "</div>", f"{tag} just en")
    h = resub(h, r"<div class=\"section-content lang-pt\" style=\"display:none; font-size: 0\.9rem; font-style: italic;\">.*?</div>",
              '<div class="section-content lang-pt" style="display:none; font-size: 0.9rem; font-style: italic;">' + d["pt"]["justification"] + "</div>", f"{tag} just pt")
    # bias swap (container + badge class + badge texts) when the alignment changed today
    if pair in BIAS_SWAP:
        old_b, new_b, old_en, new_en, old_pt, new_pt = BIAS_SWAP[pair]
        h = rep(h, f'class="report-container bias-{old_b}"', f'class="report-container bias-{new_b}"', f"{tag} container")
        h = rep(h, f'bias-badge bias-{old_b}"', f'bias-badge bias-{new_b}"', f"{tag} badge cls")
        h = rep(h, f'<span class="lang-en">{old_en}</span>', f'<span class="lang-en">{new_en}</span>', f"{tag} badge en")
        h = rep(h, f'<span class="lang-pt" style="display:none;">{old_pt}</span>', f'<span class="lang-pt" style="display:none;">{new_pt}</span>', f"{tag} badge pt")
    open(p, "w", encoding="utf-8").write(h)
    print(f"OK: {fname}")

NEXT_EV = {
    "EUR/USD": '<div class="next-event"><span class="ne-tag"><span class="lang-en">Next focus</span><span class="lang-pt" style="display:none;">Próximo foco</span></span> <span class="lang-en">US CPI ≈13/10 · FOMC ≈28/10</span><span class="lang-pt" style="display:none;">CPI EUA ≈13/10 · FOMC ≈28/10</span></div>',
    "USD/JPY": '<div class="next-event"><span class="ne-tag"><span class="lang-en">Next focus</span><span class="lang-pt" style="display:none;">Próximo foco</span></span> <span class="lang-en">MoF intervention watch</span><span class="lang-pt" style="display:none;">MoF em alerta de intervenção</span></div>',
    "AUD/USD": '<div class="next-event"><span class="ne-tag"><span class="lang-en">Next focus</span><span class="lang-pt" style="display:none;">Próximo foco</span></span> <span class="lang-en">RBA 29/09</span><span class="lang-pt" style="display:none;">RBA 29/09</span></div>',
    "GBP/USD": '<div class="next-event"><span class="ne-tag"><span class="lang-en">Next focus</span><span class="lang-pt" style="display:none;">Próximo foco</span></span> <span class="lang-en">UK CPI ≈13/10 · BoE 5/11</span><span class="lang-pt" style="display:none;">CPI UK ≈13/10 · BoE 5/11</span></div>',
    "EUR/JPY": '<div class="next-event"><span class="ne-tag"><span class="lang-en">Next focus</span><span class="lang-pt" style="display:none;">Próximo foco</span></span> <span class="lang-en">MoF intervention watch</span><span class="lang-pt" style="display:none;">MoF em alerta de intervenção</span></div>',
    "GBP/JPY": '<div class="next-event"><span class="ne-tag"><span class="lang-en">Next focus</span><span class="lang-pt" style="display:none;">Próximo foco</span></span> <span class="lang-en">MoF watch · BoE 5/11</span><span class="lang-pt" style="display:none;">MoF em alerta · BoE 5/11</span></div>',
}

FD["EUR/USD"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action sell">SELL</span> — the runner short (entered at the Sep-15 close 1.1539) works +1.29R toward 1.1440; continuation ticket: short a close under 1.1460, stop 1.1500, target 1.1350 (1:2.66)</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action sell">VENDA</span> — a curta correndo (entrada no fechamento de 15/09, 1,1539) trabalha +1,29R rumo a 1,1440; ticket de continuação: vender um fechamento sob 1,1460, stop 1,1500, alvo 1,1350 (1:2,66)</span>',
    "_tier_en": "High", "_tier_pt": "Alta",
})
FD["USD/JPY"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — the BoJ\'s 7-2 hike (dissent, doubts on more) floored the yen and the MoF ran rate checks; the 10-day-high close ends the bear read but the 281-pip intervention floor blocks every geometry</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — a alta do BoJ por 7-2 (dissidência, dúvidas sobre a próxima) derrubou o iene e o MoF fez checagens cambiais; o fechamento em máxima de 10 pregões encerra a leitura de baixa, mas o piso de intervenção de 281 pips bloqueia qualquer geometria</span>',
    "_tier_en": "Moderate", "_tier_pt": "Moderada",
})
FD["AUD/USD"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — bull alignment intact at 0.7120, stalled over the 10/20-day low 0.7114; the broken 0.7141-0.7162 zone still caps the shelf\'s premium under 1:2 — the RBA (Sep 29) is the re-arm event</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — alinhamento de alta intacto em 0,7120, travado sobre a mínima de 10/20 pregões 0,7114; a zona quebrada 0,7141-0,7162 segue capando o prêmio da prateleira sob 1:2 — a RBA (29/09) é o evento de rearme</span>',
    "_tier_en": "Moderate", "_tier_pt": "Moderada",
})
FD["GBP/USD"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — the week swept the 61.8% Fib (1.3411) and the 10/20-day lows; the bias flips bear, but the 1.3300/1.3301 cluster caps the first leg at ~1:1.1 — re-arm under 1.3300</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — a semana varreu a Fib 61,8% (1,3411) e as mínimas de 10/20 pregões; o viés vira baixa, mas o cluster 1,3300/1,3301 capa a primeira perna em ~1:1,1 — rearmar sob 1,3300</span>',
    "_tier_en": "Moderate", "_tier_pt": "Moderada",
})
FD["EUR/JPY"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — the death cross stands, but the BoJ-disappointment rip closed at a 10-day high (180.94) over the handed-back 78.6% Fib; the 270-pip intervention floor rejects every geometry</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — o cruzamento de baixa segue, mas o repique pós-BoJ fechou em máxima de 10 pregões (180,94) sobre a Fib 78,6% devolvida; o piso de intervenção de 270 pips rejeita qualquer geometria</span>',
    "_tier_en": "Moderate", "_tier_pt": "Moderada",
})
FD["GBP/JPY"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — the reclaim of 209.85/210.57 ends September\'s bear read (neutral now); the 340-pip intervention floor rejects every geometry up the Fib/SMA ladder</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — a recuperação de 209,85/210,57 encerra o regime de baixa de setembro (neutro agora); o piso de intervenção de 340 pips rejeita qualquer geometria na escada Fib/SMA</span>',
    "_tier_en": "Moderate", "_tier_pt": "Moderada",
})

# bias flips today: USD/JPY bear->neutral (September breakdown reclaimed by close);
# GBP/USD bull->bear (61.8% Fib invalidation printed); GBP/JPY bear->neutral (reclaim of 209.85/210.57)
BIAS_SWAP = {
    "USD/JPY": ("bear", "neutral", "USD/JPY - BEARISH", "USD/JPY - NEUTRAL", "USD/JPY - BAIXA", "USD/JPY - NEUTRO"),
    "GBP/USD": ("bull", "bear", "GBP/USD - BULLISH", "GBP/USD - BEARISH", "GBP/USD - ALTA", "GBP/USD - BAIXA"),
    "GBP/JPY": ("bear", "neutral", "GBP/JPY - BEARISH", "GBP/JPY - NEUTRAL", "GBP/JPY - BAIXA", "GBP/JPY - NEUTRO"),
}

def chips_div(items):
    return '<div class="macro-chips">' + "".join(
        f'<span class="macro-chip lang-en">{en}</span><span class="macro-chip lang-pt" style="display:none;">{pt}</span>'
        for en, pt in items) + "</div>"

CHIPS = {
    "EUR/USD": chips_div([("Fed 3.75-4.00%", "Fed 3,75-4,00%"),
                          ("One more hike in 2026", "Mais uma alta em 2026"),
                          ("ECB on hold 2.50%", "BCE parada em 2,50%")]),
    "USD/JPY": chips_div([("BoJ 1.25% · 7-2", "BoJ 1,25% · 7-2"),
                          ("MoF rate checks", "MoF em checagem"),
                          ("Fed–BoJ gap", "Diferencial Fed–BoJ")]),
    "AUD/USD": chips_div([("RBA 4.35% · Sep 29", "RBA 4,35% · 29/09"),
                          ("Fed 3.75-4.00%", "Fed 3,75-4,00%"),
                          ("Zone 0.7141 caps", "Zona 0,7141 capa")]),
    "GBP/USD": chips_div([("BoE 3.75% 6-3 hold", "BoE 3,75% 6-3 manteve"),
                          ("Fed out-hawks BoE", "Fed supera o BoE"),
                          ("CPI UK 2.9%", "IPC UK 2,9%")]),
    "EUR/JPY": chips_div([("BoJ 1.25% · 7-2", "BoJ 1,25% · 7-2"),
                          ("Death cross stands", "Cruzamento de baixa segue"),
                          ("MoF rate checks", "MoF em checagem")]),
    "GBP/JPY": chips_div([("BoJ 1.25% · 7-2", "BoJ 1,25% · 7-2"),
                          ("MoF rate checks", "MoF em checagem"),
                          ("BoE–BoJ gap", "Diferencial BoE–BoJ")]),
}

# gauge percent computed from the support/resistance leading numbers vs quote
GAUGE = {"EUR/USD": ("0", "1.1460", "1.1500"), "USD/JPY": ("91", "153.27", "158.36"),
         "AUD/USD": ("46", "0.7102", "0.7141"), "GBP/USD": ("0", "1.3344", "1.3411"),
         "EUR/JPY": ("29", "180.49", "182.04"), "GBP/JPY": ("42", "209.85", "211.84")}
# conviction score = round(R*3) clamped to [3,10]; 0 for WAIT pairs
TIER = {"EUR/USD": ("8/10", "", 8), "USD/JPY": ("0/10", "t-mod", 0),
        "AUD/USD": ("0/10", "t-mod", 0), "GBP/USD": ("0/10", "t-mod", 0),
        "EUR/JPY": ("0/10", "t-mod", 0), "GBP/JPY": ("0/10", "t-mod", 0)}

# no verdict-badge flips today: EUR/USD stays sell-breakout, the other five stay WAIT
BADGE = {}

for pair, fname in PAGE.items():
    g = GAUGE[pair]; t = TIER[pair]
    badge, cls_swaps = BADGE.get(pair, (None, []))
    update_page(pair, fname, FD[pair], g[0], g[1], g[2], CHIPS[pair], NEXT_EV[pair],
                t[0], t[1], t[2], badge, cls_swaps)

# =====================================================================
# 3. track-record ledger
# =====================================================================
LED = DOCS + "/track-record.json"
led = json.load(open(LED, encoding="utf-8"))
led["meta"]["lastUpdated"] = TS_DATE

# Resolve the live ticket: the 14/09 EUR/USD breakout short TRIGGERED — the 15/09 close
# (1.15389) printed under the 10-day low 1.1551, inside the FOMC window per the ticket's own
# clause (reassess after the event: the Fed hiked to 3.75-4.00% on 16/09 and the 16/09 close
# 1.15370 held under the entry — the reassessment confirms). Neither target 1.1440 nor stop
# 1.1600 was close-crossed through 18/09 (close 1.14600) -> OPEN, running +1.29R.
watching = led["watching"]
assert len(watching) == 1 and watching[0]["pair"] == "EUR/USD" and watching[0]["reportDate"] == "14/09/2026"
t = watching[0]
t["entry"] = 1.15389
t["entryDate"] = "15/09/2026"
t["note"] = ("triggered at the 15/09 close (1.15389, under the 10-day low 1.1551) inside the FOMC window per the "
             "ticket's own clause; the post-event reassessment confirmed it — the Fed hiked to 3.75-4.00% (16/09) and "
             "the 16/09 close (1.15370) held under the entry; running +1.29R at the 18/09 close (1.14600) toward "
             "1.1440, the 1.1600 stop never threatened (10-session expiry: 29/09)")
led["open"] = [t]
led["watching"] = []

# Append: EUR/USD continuation short breakout — fresh 10/20-day low under the handed-back Fib.
led["watching"].append({
    "pair": "EUR/USD",
    "reportDate": TS_DATE,
    "direction": "short",
    "setup": "breakout",
    "entry": 1.1459,
    "stop": 1.15,
    "target": 1.135,
    "plannedR": 2.66,
    "triggerRule": "daily close under the 10-day Donchian low 1.1460 (entry reference 1.1459); valid through the 23/09 close",
    "note": ("continuation breakdown: the 18/09 close (1.1460, -0.18%) is a fresh 10/20-day low under the handed-back "
             "78.6% Fib (1.1476); stop 41 pips over the 1.1500 round + the handed-back Fib (>= the ~37-pip 1.5-sigma20 "
             "floor); target 1.1350 just above the 9-month low (1.1340), path crossing only the 1.1400 round; additive "
             "to the open runner from the 14/09 ticket (entered at the 15/09 close 1.1539, stop 1.1600, target 1.1440)")
})
assert len(led["watching"]) == 1
assert len([t for t in led["watching"] if t["pair"] == "EUR/USD"]) == 1

with open(LED, "w", encoding="utf-8") as f:
    json.dump(led, f, ensure_ascii=False, indent=2)
print("OK: track-record.json (14/09 short moved watching->open at 1.15389, continuation short appended)")

# =====================================================================
# 4. news.html — hero dateline + calendar strip + new wire cards + basis note
# =====================================================================
NP = DOCS + "/news.html"
nh = open(NP, encoding="utf-8").read()
nh = rep(nh, '<span class="lang-en">Wire updated: ' + OLD_TS + '</span>', '<span class="lang-en">Wire updated: ' + TS + '</span>', "news hero en")
nh = rep(nh, '<span class="lang-pt" style="display:none;">Telégrafo atualizado em: ' + OLD_TS + '</span>', '<span class="lang-pt" style="display:none;">Telégrafo atualizado em: ' + TS + '</span>', "news hero pt")
nh = rep(nh, "numbers and dates reflect the report's data basis of 14/09/2026", "numbers and dates reflect the report's data basis of 19/09/2026", "news note en")
nh = rep(nh, "refletem a base de dados do relatório de 14/09/2026", "refletem a base de dados do relatório de 19/09/2026", "news note pt")

# week-ahead calendar: the central-bank week is delivered — the post-decision slate
nh, n = re.subn(r"<div class=\"cal-grid\">.*?</section>", '''<div class="cal-grid">
                <div class="cal-cell">
                    <span class="cal-date">21-25/09</span>
                    <span class="cal-event"><span class="lang-en">Quiet week — tickets run on closes</span><span class="lang-pt" style="display:none;">Semana muda — os tickets rodam nos fechamentos</span></span>
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
                </div>
                <div class="cal-cell">
                    <span class="cal-date">05/11</span>
                    <span class="cal-event"><span class="lang-en">BoE decision</span><span class="lang-pt" style="display:none;">Decisão do BoE</span></span>
                    <div class="cal-meta"><span class="cal-impact high" aria-hidden="true"></span><span class="cal-cur">GBP</span></div>
                </div>
            </div>
        </section>''', nh, count=1, flags=re.DOTALL)
if n != 1:
    print("FAIL: calendar strip"); sys.exit(1)

def news_card(comment, cat_en, cat_pt, impact_en, impact_pt, impact_cls, date, headline_en, headline_pt, summary_en, summary_pt, take_en, take_pt, pairs):
    chips = "\n".join(f'                        <a href="{PAGE[p]}" class="pair-link-chip">{p}</a>' for p in pairs)
    return f'''                <!-- {comment} -->
                <article class="news-card">
                    <div class="news-card-top">
                        <span class="news-cat"><span class="lang-en">{cat_en}</span><span class="lang-pt" style="display:none;">{cat_pt}</span></span>
                        <span class="impact-badge {impact_cls}"><span class="lang-en">{impact_en}</span><span class="lang-pt" style="display:none;">{impact_pt}</span></span>
                        <span class="news-date">{date}</span>
                    </div>
                    <h2 class="news-title">
                        <span class="lang-en">{headline_en}</span>
                        <span class="lang-pt" style="display:none;">{headline_pt}</span>
                    </h2>
                    <p class="news-summary">
                        <span class="lang-en">{summary_en}</span>
                        <span class="lang-pt" style="display:none;">{summary_pt}</span>
                    </p>
                    <div class="news-take">
                        <span class="take-tag"><span class="lang-en">Desk take</span><span class="lang-pt" style="display:none;">Leitura da mesa</span></span>
                        <span class="lang-en">{take_en}</span>
                        <span class="lang-pt" style="display:none;">{take_pt}</span>
                    </div>
                    <div class="news-pairs">
                        <span class="np-label"><span class="lang-en">Watch</span><span class="lang-pt" style="display:none;">Acompanhar</span></span>
{chips}
                    </div>
                </article>

'''

NEWS_CARDS = (
    news_card("News 0: Fed delivers the unanimous hike — dollar sweeps the board",
              "Central Banks", "Bancos Centrais", "High Impact", "Impacto Alto", "high", "19/09/2026",
              "Fed delivers a unanimous hike to 3.75-4.00% and signals one more this year; the dollar sweeps the board",
              "Fed entrega a alta unânime para 3,75-4,00% e sinaliza mais uma ainda em 2026; dólar varre o tabuleiro",
              "The Sep 15-16 FOMC closed the central-bank week: a unanimous 25-bp hike to 3.75-4.00% — the first in about three years — with Chair Warsh saying inflation is too high and signaling one more hike still this year; the Dow fell more than 600 points in the follow-through. Against an ECB frozen at 2.50% and a BoE that merely held (3.75%, 6-3), the differential became the dollar's raw material: EUR/USD closed the week at 1.1460 (a fourth straight down close, a fresh 10/20-day low) with the desk's short runner working at +1.29R toward 1.1440 — and a new continuation ticket armed under 1.1460 (stop 1.1500, target 1.1350, 1:2.66); AUD/USD stalled the slide at 0.7114 and stays on WAIT until the RBA (Sep 29).",
              "O FOMC de 15-16/09 fechou a semana dos bancos centrais: alta unânime de 25 pb para 3,75-4,00% — a primeira em cerca de três anos —, com o presidente Warsh dizendo que a inflação está alta demais e sinalizando mais uma alta ainda em 2026; o Dow caiu mais de 600 pontos na sequência. Contra um BCE parado em 2,50% e um BoE que só segurou os juros (3,75%, 6-3), o diferencial virou matéria-prima do dólar: o EUR/USD fechou a semana em 1,1460 (quarta queda seguida, mínima de 10/20 pregões) com o corredor de venda da mesa rodando a +1,29R rumo a 1.1440 — e um novo ticket de continuação armado sob 1.1460 (stop 1.1500, alvo 1.1350, 1:2,66); o AUD/USD travou a queda sobre 0,7114 e segue em AGUARDAR até a RBA (29/09).",
              "The book entered the week short EUR/USD from the Sep-15 close — and the committee confirmed the map instead of refuting it: hike delivered, one more signaled, the dollar collected on both sides of the Atlantic. The desk does not chase: the continuation demands its own close under 1.1460.",
              "O livro entrou na semana curto do EUR/USD no fechamento de 15/09 — e o comitê confirmou o mapa em vez de desmenti-lo: alta entregue, sinalização de mais uma, o dólar cobrou dos dois lados do Atlântico. A mesa não persegue: a continuação exige seu próprio fechamento sob 1,1460.",
              ["EUR/USD", "AUD/USD", "GBP/USD"]) +
    news_card("News 1: BoJ 7-2 dissent floors the yen — MoF rate checks",
              "Central Banks", "Bancos Centrais", "High Impact", "Impacto Alto", "high", "19/09/2026",
              "BoJ hikes to 1.25% by 7-2 and the dissent floors the yen: 10-day high closes across all three crosses as the MoF runs rate checks",
              "BoJ sobe a 1,25% por 7-2 e a dissidência derruba o iene: máximas de 10 pregões nos três cruzamentos e o MoF faz rate checks",
              "The BoJ delivered the 25 bp (1.25%, a 31-year high) on Sep 17-18, but the 7-2 vote with dissent and mixed signals clouded the next hike — the market doubts the commitment and the yen was the board's worst: USD/JPY +1.41% Friday to 157.89 (a 10-day high close, reclaiming every September close including the broken Sep-3 low, 156.01), EUR/JPY 180.94 (+1.23%) and GBP/JPY 210.69 (+1.17%), both at 10-day highs. To top it off, Japan ran rate checks in the FX market — the MoF on maximum alert since the July joint intervention. The 2.5-sigma20 floors (281/270/340 pips) keep all three pairs on WAIT: September's bear breakdowns died reclaimed (a neutral read on USD/JPY and GBP/JPY), but no geometry closes 1:2 over a clean path in front of the intervenor.",
              "O BoJ entregou os 25 pb (1,25%, máxima de 31 anos) em 17-18/09, mas a votação 7-2 com dissidência e sinais mistos nublou a próxima alta — o mercado duvida do compromisso e o iene foi o pior do tabuleiro: USD/JPY +1,41% na sexta para 157,89 (fechamento em máxima de 10 pregões, recuperando todos os fechamentos de setembro, incluindo a mínima quebrada de 03/09, 156.01), EUR/JPY 180,94 (+1,23%) e GBP/JPY 210,69 (+1,17%), ambos em máximas de 10 pregões. Para completar, o Japão fez checagens de taxa no mercado cambial — o MoF em alerta máximo desde a intervenção conjunta de julho. Os pisos de 2,5σ20 (281/270/340 pips) mantêm os três pares em AGUARDAR: os rompimentos de baixa de setembro morreram recuperados (leitura neutra no USD/JPY e no GBP/JPY), mas nenhuma geometria fecha 1:2 com caminho limpo na frente do interveniente.",
              "A hike without credibility is the worst outcome for a currency: the BoJ paid 25 bp and the market took it back in yen — with the MoF running rate checks, the desk does not stand inside the machine room. All three crosses turn neutral or blocked; the next BoJ only in late October.",
              "Alta sem credibilidade é o pior resultado para uma moeda: o BoJ pagou 25 pb e o mercado cobrou de volta em iene — com o MoF fazendo rate checks, a mesa não fica do lado de dentro da sala de máquinas. Os três cruzamentos viram neutros ou travados; o próximo BoJ só no fim de outubro.",
              ["USD/JPY", "EUR/JPY", "GBP/JPY"]) +
    news_card("News 2: BoE hawkish hold is not enough — cable delivers the invalidation",
              "Central Banks", "Bancos Centrais", "Medium Impact", "Impacto Médio", "med", "19/09/2026",
              "BoE holds 3.75% at 6-3 with three hike votes — hawkish, but the delivered Fed won the chessboard and cable hands over the invalidation",
              "BoE segura 3,75% em 6-3 com três votos por alta — hawkish, mas o Fed entregue comprou o xadrez e o cable entrega a invalidez",
              "The BoE kept rates at 3.75% on Thursday (Sep 17) in a 6-3 vote — the three dissents called for a hike to 4%, and the tone kept tightening per the press. It was not enough: 24h after the Fed delivered 3.75-4.00% with one more hike signaled, the differential turned against sterling and price sent the message — cable's seventh straight down close at 1.3344, with the Sep-17 close sweeping the 61.8% Fib (1.3411) the Sep-14 edition had marked as the bull structure's invalidation. The bias turns bear, but the desk does not chase: the 78.6% Fib + round cluster (1.3300/1.3301) pays ~1:1.1 from the break and blocks the 1:2 path — re-arm on a close under 1.3300 (target re-priced to the 9-month low, 1.3160) or a reclaim over 1.3411. Next arbiters: UK CPI ≈Oct 13 and the BoE on Nov 5.",
              "O BoE manteve os juros em 3,75% na quinta (17/09) em votação 6-3 — as três dissidências pediram alta a 4%, e o tom seguiu apertando segundo a imprensa. Não bastou: 24h depois do Fed entregar 3,75-4,00% com mais uma alta sinalizada, o diferencial virou contra a libra e o preço mandou o recado — sétima queda consecutiva do cable, fechamento em 1,3344, com o fechamento de 17/09 varrendo a Fib 61,8% (1,3411) que a edição de 14/09 marcava como invalidez da estrutura de alta. O viés vira baixa, mas a mesa não persegue: o cluster Fib 78,6% + redondo (1.3300/1.3301) paga ~1:1,1 da quebra e bloqueia o caminho do 1:2 — rearmar em fechamento sob 1.3300 (alvo reprecificado na mínima de 9 meses, 1.3160) ou recuperação sobre 1.3411. Próximos árbitros: CPI do Reino Unido ≈13/10 e BoE em 05/11.",
              "A hawkish hold against a delivered hike is a loss by selection: the BoE raised its tone and still lost the differential to the Fed — cable paid with the bull structure. The desk flipped the bias and kept the discipline: no selling inside the cluster; the ticket only exists if 1.3300 gives way by close.",
              "Hold hawkish contra hike entregue é derrota por seleção: o BoE subiu o tom e mesmo assim perdeu o diferencial para o Fed — o cable pagou com a estrutura de alta. A mesa virou o viés, manteve a disciplina: nada de vender dentro do cluster; o ticket só existe se o 1.3300 ceder por fechamento.",
              ["GBP/USD"]) +
    news_card("News 3: the book in the central-bank week — runner at +1.29R, three biases flip",
              "Market Flow", "Fluxo de Mercado", "High Impact", "Impacto Alto", "high", "19/09/2026",
              "The book in the central-bank week: the short runner triggered at the Sep-15 close works at +1.29R; three biases flip",
              "O livro na semana dos bancos centrais: corredor de venda disparado no fechamento de 15/09 roda a +1,29R; três vieses viram",
              "A week of three decisions, one trigger and three new biases. The EUR/USD breakout short (armed in the Sep-14 edition) fired at the Sep-15 close (1.1539 under the 1.1551 low, inside its own post-FOMC reassessment clause — the committee confirmed) and runs at +1.29R toward the 1.1440 target with the 1.1600 stop intact; the desk re-arms the continuation: a close under 1.1460, stop 1.1500, target 1.1350 (1:2.66). On the board: GBP/USD flips bull to bear (the invalidation delivered), USD/JPY and GBP/JPY flip bear to neutral (September's breakdowns reclaimed by close), EUR/JPY stays bear blocked at the intervention floor and AUD/USD stays bull blocked at the broken 0.7141-0.7162 zone — five of six pairs on WAIT, the dollar in front.",
              "Semana de três decisões, um disparo e três vieses novos. O curto de rompimento do EUR/USD (armado na edição de 14/09) disparou no fechamento de 15/09 (1,1539 sob a mínima de 1,1551, dentro da própria cláusula de reavaliação pós-FOMC — o comitê confirmou) e roda a +1,29R rumo ao alvo 1.1440 com o stop 1.1600 intacto; a mesa rearma a continuação: fechamento sob 1.1460, stop 1.1500, alvo 1.1350 (1:2,66). No tabuleiro: GBP/USD vira de alta para baixa (invalidez entregue), USD/JPY e GBP/JPY viram de baixa para neutros (os rompimentos de setembro recuperados por fechamento), EUR/JPY segue baixa travado no piso de intervenção e AUD/USD segue alta travado na zona quebrada 0.7141-0.7162 — cinco dos seis pares em AGUARDAR, o dólar na frente.",
              "The report ended the week with what it sought entering it: one runner working in the macro's direction and five maps blocked by geometry — intervention floors on the crosses, a first-order cluster on cable, a broken zone on the aussie. Discipline pays; the next test is the RBA (Sep 29).",
              "O relatório terminou a semana com o que buscou ao entrá-la: um corredor rodando na direção do macro e cinco mapas travados por geometria — pisos de intervenção nos cruzamentos, cluster de primeira ordem no cable, zona quebrada no aussie. Disciplina paga; o próximo teste é a RBA (29/09).",
              ["EUR/USD"])
)

nh = rep(nh, "                <!-- News 0: Dollar opens FOMC week on the front foot — both tickets off the book -->", NEWS_CARDS + "                <!-- News 0: Dollar opens FOMC week on the front foot — both tickets off the book -->", "news card prepend")
open(NP, "w", encoding="utf-8").write(nh)
print("OK: news.html (dateline, calendar strip, 4 new cards, basis note)")

# =====================================================================
# 5. patch verify_all.py to the new edition
# =====================================================================
VP = r"C:/Projetos/forex-report/pipeline/verify_all.py"
v = open(VP, encoding="utf-8").read()
v = rep(v, 'TODAY_TS = "14/09/2026 22:22 UTC"', 'TODAY_TS = "' + TS + '"', "verify TODAY_TS")
v = rep(v, 'TODAY_DATE = "14/09/2026"  # basis session date (report edition: 14/09/2026)', 'TODAY_DATE = "18/09/2026"  # basis session date (report edition: 19/09/2026)', "verify TODAY_DATE")
v = rep(v, '''TICKER = [("EUR/USD","-0.35%"),("USD/JPY","+0.33%"),("AUD/USD","-0.60%"),
          ("GBP/USD","-0.10%"),("EUR/JPY","-0.02%"),("GBP/JPY","+0.23%")]''',
        '''TICKER = [("EUR/USD","-0.18%"),("USD/JPY","+1.41%"),("AUD/USD","+0.09%"),
          ("GBP/USD","-0.24%"),("EUR/JPY","+1.23%"),("GBP/JPY","+1.17%")]''', "verify TICKER")
v = rep(v, 'for stale in ["02/09/2026", "01/09/2026", "19/08/2026", "18/08/2026", "17/08/2026", "14/08/2026", "13/08/2026", "04/09/2026", "07/09/2026", "09/09/2026", "11/09/2026"]:',
        'for stale in ["02/09/2026", "01/09/2026", "19/08/2026", "18/08/2026", "17/08/2026", "14/08/2026", "13/08/2026", "04/09/2026", "07/09/2026", "09/09/2026", "11/09/2026", "14/09/2026"]:', "verify static stale")
open(VP, "w", encoding="utf-8").write(v)
print("OK: verify_all.py patched to the 19/09/2026 edition")

print(f"\nDONE {TS} — run verify_all.py next.")
