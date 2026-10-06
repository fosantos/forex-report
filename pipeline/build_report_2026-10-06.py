#!/usr/bin/env python3
"""06/10/2026 edition — replaces forexData + dailyChanges + macroDrivers + the 4 report stamps
in docs/index.html. Data basis: Frankfurter/ECB daily reference rates, 557 sessions 01/08/2024-06/10/2026
(compute_indicators.py run of 06/10/2026; the MT5 terminal still returns no FX data).
Key events of the basis week: EUR/USD runner (19/09 ticket) hit its 1.1350 target at the 01/10 close (+1.27R);
05/10 printed the fresh 9-month low 1.1204; 06/10 bounce +0.58%. US government shutdown since 01/10 (NFP/CPI
suspended); ISM services weak on 05/10 with the dollar dominant anyway; RBA hiked 25bp to 4.60% (unanimous) on
29/09 but Bullock voiced hope the four delivered hikes suffice; averages crossed bearish on USD/JPY and GBP/JPY.
Aborts on any structural mismatch. Validates JSON + key order + rrValue consistency."""
import re, json, sys

PATH = r"C:/Projetos/forex-report/docs/index.html"
TS = "06/10/2026 23:00 UTC"
OLD_TS = "28/09/2026 22:15 UTC"

with open(PATH, encoding="utf-8") as f:
    html = f.read()

NEW_BLOCK = '''        const forexData = {
        "EUR/USD": {
                "quote": "1.1269",
                "bias": "BAIXA",
                "biasType": "bear",
                "pt": {
                        "fundamental": "O EUR/USD fechou em 1,1269 na sessão de terça 06/10/2026 (taxa de referência BCE/Frankfurter; o terminal MT5 logado segue sem retornar dados de FX), subindo +0,58% — repique da mínima de 9 meses (1.1204, cravada na segunda): a semana custou -0,96% com o dólar dominante mesmo com o ISM services fraco (05/10) e o shutdown do governo dos EUA (desde 01/10, com NFP, CPI e claims suspensos) não comprou nenhuma pausa ao fluxo — quarto fechamento semanal de queda seguido. O livro cobrou a sequência: o corredor de continuação da edição de 19/09 encerrou no alvo — o fechamento de 01/10 (1.1298) cruzou o alvo 1.1350 e o ticket bankou +1,27R, o segundo alvo do ledger público. O diferencial segue como matéria-prima do dólar (Fed a 3,75-4,00% com mais uma alta sinalizada contra o BCE parado em 2,50%) e o alinhamento segue de baixa pleno (fechamento sob a SMA200 1,1607, SMA50 1,1522 abaixo dela). A regra pede o repique: venda armada na prateleira virada 1.1340-1.1370. Indicadores (SMA 50/200, σ20, Donchian e Fibonacci) calculados da série diária BCE/Frankfurter (557 pregões, 01/08/2024 a 06/10/2026).",
                        "trend": "Alinhamento de baixa pleno — fechamento sob a SMA200 (1,1607) e a SMA50 (1,1522) abaixo dela — com a mínima de 9 meses (1.1204) cravada na segunda e o repique de terça devolvendo 65 pips: a estrutura segue entregando andares, agora com a prateleira virada 1.1340-1.1370 como teto imediato.",
                        "support": "1.1204 (mínima de 9 meses, cravada na segunda), com o redondo 1.1200 logo abaixo — o piso em formação.",
                        "resistance": "1.1369 (Fib 78,6% + o topo da prateleira virada 1.1340-1.1370), com a máxima de 10 pregões (1.1411) e a SMA50 (1.1522) acima.",
                        "priceAction": "Setup de venda no repique: o gatilho é um fechamento diário dentro da prateleira virada 1.1340-1.1370 (o piso de setembro 1.1340 entregue + o redondo 1.1350 + a Fib 78,6% 1.1369) seguido de fechamento sob o anterior e sob o meio da zona 1.1355 — entrada de referência 1.1350, stop 1.1412 (62 pips sobre o topo da zona e a máxima de 10 pregões 1.1411, ≥ piso 1,5σ20 de ~54 pips), alvo 1.1200 (150 pips, o redondo sob a mínima de 9 meses 1.1204), cruzando apenas o redondo 1.1300. Fechamento de volta sobre 1.1412 cancela o mapa.",
                        "recommendation": "VENDA (SHORT) NA RETRAÇÃO",
                        "trigger": "Fechamento diário dentro da prateleira 1.1340-1.1370 seguido de fechamento sob o anterior e sob o meio da zona 1.1355 — entrada de referência 1.1350. Válido até o fechamento de 09/10; a ata do FOMC (07/10) e o CPI dos EUA ≈13/10 (sujeito a atraso pelo shutdown) ficam fora da janela de 24h.",
                        "stop": "1.1412 (62 pips sobre o topo da zona 1.1369 e a máxima de 10 pregões 1.1411; ≥ piso 1,5σ20 de ~54 pips) · risco sugerido ≤ 1% por operação.",
                        "target": "1.1200 (150 pips, o redondo sob a mínima de 9 meses 1.1204), com apenas o redondo 1.1300 no caminho.",
                        "rr": "1:2.42",
                        "rrValue": 60,
                        "justification": "A semana pagou o corredor e devolveu o mapa: o ticket de 19/09 encerrou no alvo com +1,27R no fechamento de 01/10 e a mínima de 9 meses (1.1204) chegou na segunda — o dólar dominou mesmo com o ISM fraco, e o shutdown só suspendeu os dados, não o fluxo. A regra agora pede o repique: perseguir a 65 pips da mínima fresca é pagar o pior preço do corredor; a prateleira virada 1.1340-1.1370 (piso entregue + redondo + Fib 78,6%) devolve a entrada com stop estrutural de 62 pips aprovado no piso de volatilidade e 1:2,42 até o redondo sob a mínima, cruzando apenas o 1.1300 — e o ticket só existe se o repique entregar o fechamento."
                },
                "en": {
                        "fundamental": "EUR/USD closed at 1.1269 in the Tuesday 06/10/2026 session (ECB/Frankfurter reference rate; the logged-in MT5 terminal still returns no FX data), up +0.58% — a bounce off the 9-month low (1.1204, printed Monday): the week cost -0.96% with the dollar dominant even through the weak ISM services print (Oct 5), and the US government shutdown (since Oct 1, with NFP, CPI and claims suspended) bought the flow no pause — a fourth straight weekly down close. The book collected the sequence: the Sep-19 continuation runner closed at target — the Oct-1 close (1.1298) crossed the 1.1350 target and the ticket banked +1.27R, the public ledger's second target. The differential remains the dollar's raw material (Fed at 3.75-4.00% with one more hike signaled against an ECB frozen at 2.50%) and the alignment stays fully bearish (close under the SMA200 1.1607, 50-day 1.1522 below it). The rule asks for the pullback: a short armed on the flipped 1.1340-1.1370 shelf. Indicators (SMA 50/200, sigma20, Donchian and Fibonacci) computed from the ECB/Frankfurter daily series (557 sessions, 01/08/2024 to 06/10/2026).",
                        "trend": "Full bear alignment — close under the SMA200 (1.1607) with the 50-day (1.1522) below it — and the 9-month low (1.1204) printed Monday, with Tuesday's bounce handing back 65 pips: the structure keeps delivering floors, now with the flipped 1.1340-1.1370 shelf as the immediate ceiling.",
                        "support": "1.1204 (the 9-month low, printed Monday), with the 1.1200 round just beneath — the floor in formation.",
                        "resistance": "1.1369 (the 78.6% Fib + the top of the flipped 1.1340-1.1370 shelf), with the 10-day high (1.1411) and the 50-day SMA (1.1522) above.",
                        "priceAction": "Pullback short setup: the trigger is a daily close inside the flipped 1.1340-1.1370 shelf (the handed-back September floor 1.1340 + the 1.1350 round + the 78.6% Fib 1.1369) followed by a close below the previous close and below the 1.1355 zone midpoint — entry reference 1.1350, stop 1.1412 (62 pips over the zone top and the 10-day high 1.1411, >= the ~54-pip 1.5-sigma20 floor), target 1.1200 (150 pips, the round under the 9-month low 1.1204), crossing only the 1.1300 round. A close back over 1.1412 cancels the map.",
                        "recommendation": "SELL (SHORT) ON PULLBACK",
                        "trigger": "Daily close inside the 1.1340-1.1370 shelf followed by a close below the previous close and below the 1.1355 midpoint — entry reference 1.1350. Valid through the 09/10 close; the FOMC minutes (Oct 7) and US CPI ≈13/10 (delay risk from the shutdown) sit outside the 24h window.",
                        "stop": "1.1412 (62 pips over the 1.1369 zone top and the 10-day high 1.1411; >= the ~54-pip 1.5-sigma20 floor) · suggested risk ≤ 1% per trade.",
                        "target": "1.1200 (150 pips, the round under the 9-month low 1.1204), with only the 1.1300 round on the way.",
                        "rr": "1:2.42",
                        "rrValue": 60,
                        "justification": "The week paid the runner and returned the map: the Sep-19 ticket closed at target for +1.27R at the Oct-1 close and the 9-month low (1.1204) arrived Monday — the dollar dominated even through the weak ISM, and the shutdown only suspended the data, not the flow. The rule now asks for the pullback: chasing 65 pips off the fresh low is paying the runner's worst price; the flipped 1.1340-1.1370 shelf (handed-back floor + round + 78.6% Fib) returns the entry with a 62-pip structural stop cleared by the volatility floor and 1:2.42 to the round under the low, crossing only 1.1300 — and the ticket only exists if the pullback delivers the close."
                }
        },
        "USD/JPY": {
                "quote": "158.09",
                "bias": "BAIXA",
                "biasType": "bear",
                "pt": {
                        "fundamental": "O USD/JPY fechou em 158,09 na sessão de terça 06/10/2026 (taxa de referência BCE/Frankfurter), caindo -0,09% — a devolução foi devolvida: +0,77% na semana trouxe o par de volta à soleira do cluster que cortou o rali em 24/09 (Fib 50% 158,27 + SMA200 158,47, agora a 18 pips acima). A novidade estrutural é o cruzamento: a SMA50 (157,88) passou sob a SMA200 (158,47) e o alinhamento formal virou de baixa — com o preço recuperando a SMA50 mas batendo no teto de primeira ordem. O roteiro segue o mesmo: Fed a 3,75-4,00% pagando o diferencial contra um BoJ a 1,25% cuja alta 7-2 deixou dúvida sobre a próxima (decisão em 29-30/10, pausa esperada), e o MoF na janela de intervenção (rate checks + intervenção conjunta de julho dentro dos 30 dias) — σ20 a 81 pips faz o piso 2,5σ20 valer 203 pips e nenhuma direção fecha 1:2 no meio do canal 156.88-158.85. Indicadores (SMA 50/200, σ20, Donchian e Fibonacci) calculados da série diária BCE/Frankfurter (557 pregões, 01/08/2024 a 06/10/2026).",
                        "trend": "A semana devolveu a devolução: de 156,88 (28/09) a 158,23 (05/10), com o fechamento de terça parando a 18 pips do cluster Fib 50% + SMA200 (158,27-158,47) — e o cruzamento novo (SMA50 157,88 sob a SMA200 158,47) formaliza a leitura de baixa no meio do canal 156.88-158.85.",
                        "support": "157.88 (SMA50, recuperada na semana), com a mínima de 10 pregões (156.88) e o redondo 155.00 abaixo.",
                        "resistance": "158.47 (SMA200 + Fib 50% 158,27 — o cluster que cortou o rali em 24/09), com as máximas de 10/20 pregões (158.85) acima.",
                        "priceAction": "Sem entrada — o piso de intervenção (2,5σ20 = 203 pips) reprova os dois lados no meio do canal: a compra exige stop a ~153,20 (sob a mínima de 20 pregões, 480+ pips do preço) com alvo atravessando o cluster e a escada acima, e a venda no cluster exigiria stop a ~160,45 e alvo a ~154,30, atravessando as Fibs 61,8% (156,94) e 78,6% (155,04). Rearmar: fechamento sob 156.88 (mínima de 10 pregões) abre a geometria de queda rumo à Donchian 20 (153.27) com a σ20 comprimindo; fechamento sobre o cluster 158.27-158.47 reabre o teste das máximas de 10/20 pregões. Próximos árbitros: Fed em 27-28/10 e BoJ em 29-30/10.",
                        "recommendation": "AGUARDAR OUTRO GATILHO",
                        "trigger": "Nenhum — o piso de intervenção (2,5σ20 = 203 pips) reprova qualquer geometria com o preço a 18 pips do cluster Fib 50% + SMA200; assistir ao MoF. Fed em 27-28/10 e BoJ em 29-30/10 como próximos árbitros.",
                        "stop": "N/A (sem operação).",
                        "target": "N/A (sem operação).",
                        "rr": "N/A",
                        "rrValue": 0,
                        "justification": "O cruzamento das médias formalizou a baixa — mas formalizar não é operar: o preço parou a 18 pips do cluster que cortou o rali (158,27-158,47) e o piso de intervenção a 203 pips reprova compra e venda no meio do canal. Com o Fed decidindo 48h antes do BoJ no fim de outubro e o MoF na janela, a mesa fica fora — o cluster decide o próximo capítulo."
                },
                "en": {
                        "fundamental": "USD/JPY closed at 158.09 in the Tuesday 06/10/2026 session (ECB/Frankfurter reference rate), down -0.09% — the giveback was given back: +0.77% on the week returned the pair to the doorstep of the cluster that cut the rip on Sep 24 (50% Fib 158.27 + SMA200 158.47, now 18 pips above). The structural news is the cross: the 50-day (157.88) slipped under the SMA200 (158.47) and the formal alignment turned bearish — with price reclaiming the 50-day but leaning on the first-order ceiling. The script stays the same: the Fed at 3.75-4.00% paying the differential against a BoJ at 1.25% whose 7-2 hike left the next step in doubt (decision on Oct 29-30, a pause expected), and the MoF inside the intervention window (rate checks + the July joint intervention within 30 days) — sigma20 at 81 pips puts the 2.5-sigma20 floor at 203 pips and no direction closes 1:2 mid-channel 156.88-158.85. Indicators (SMA 50/200, sigma20, Donchian and Fibonacci) computed from the ECB/Frankfurter daily series (557 sessions, 01/08/2024 to 06/10/2026).",
                        "trend": "The week returned the giveback: from 156.88 (Sep 28) to 158.23 (Oct 5), with Tuesday's close stopping 18 pips under the 50% Fib + SMA200 cluster (158.27-158.47) — and the fresh cross (50-day 157.88 under the SMA200 158.47) formalizes the bearish read mid-channel 156.88-158.85.",
                        "support": "157.88 (the 50-day SMA, reclaimed on the week), with the 10-day low (156.88) and the 155.00 round beneath.",
                        "resistance": "158.47 (SMA200 + 50% Fib 158.27 — the cluster that cut the Sep-24 rip), with the 10/20-day highs (158.85) above.",
                        "priceAction": "No entry — the intervention floor (2.5-sigma20 = 203 pips) rejects both sides mid-channel: a long needs a stop at ~153.20 (under the 20-day low, 480+ pips from price) with a target crossing the cluster and the ladder above, and a short at the cluster would need a stop at ~160.45 and a target at ~154.30, crossing the 61.8% (156.94) and 78.6% (155.04) Fibs. Re-arm: a close under 156.88 (the 10-day low) opens the breakdown geometry toward the 20-day Donchian (153.27) with sigma20 compressing; a close over the 158.27-158.47 cluster reopens the test of the 10/20-day highs. Next arbiters: the Fed on Oct 27-28 and the BoJ on Oct 29-30.",
                        "recommendation": "WAIT FOR ANOTHER TRIGGER",
                        "trigger": "None — the intervention floor (2.5-sigma20 = 203 pips) rejects any geometry with price 18 pips under the 50% Fib + SMA200 cluster; watch the MoF. The Fed on Oct 27-28 and the BoJ on Oct 29-30 as the next arbiters.",
                        "stop": "N/A (no trade).",
                        "target": "N/A (no trade).",
                        "rr": "N/A",
                        "rrValue": 0,
                        "justification": "The averages' cross formalized the bear — but formalizing is not trading: price stopped 18 pips under the cluster that cut the rip (158.27-158.47) and the 203-pip intervention floor rejects both sides mid-channel. With the Fed deciding 48h before the BoJ in late October and the MoF inside the window, the desk stays out — the cluster decides the next chapter."
                }
        },
        "AUD/USD": {
                "quote": "0.6982",
                "bias": "NEUTRO",
                "biasType": "neutral",
                "pt": {
                        "fundamental": "O AUD/USD fechou em 0,6982 na sessão de terça 06/10/2026 (taxa de referência BCE/Frankfurter), subindo +0,31% — a prateleira que segurava o mapa cedeu: a RBA entregou a alta unânime de 25 pb para 4,60% em 29/09 com comunicado hawkish, mas a “esperança” de Bullock de que as quatro altas já entregadas bastem para baixar a inflação tirou o próximo passo do preço — o par mal se mexeu no anúncio e o fechamento de 30/09 (0,6968) entregou a SMA200 (0,7027), com o alinhamento de alta que sobrevivia por 7 pips. A leitura vira NEUTRA formal (fechamento sob a SMA200 com a SMA50 0,7092 acima dela) e o mapa trava entre o teto virado 0.7027-0.7032 (SMA200 + Fib 38,2%) e a mínima de 10/20 pregões (0.6939) — a Fib 50% (0,6962) segurou a queda na segunda e devolveu o repique. O motor commodity segue de pé (CPI a 3,5%, WTI ~US$ 83 no rastro do conflito com o Irã), mas o momento é do dólar (Fed 3,75-4,00% com mais uma sinalizada). Próximo árbitro: CPI australiano do Q3 no fim de outubro (≈28/10). Indicadores calculados da série diária BCE/Frankfurter (557 pregões, 01/08/2024 a 06/10/2026).",
                        "trend": "Alinhamento virado: fechamento sob a SMA200 (0,7027) com a SMA50 (0,7092) ainda acima dela — leitura NEUTRA, com o teto virado 0.7027-0.7032 bloqueando por cima e a mínima de 10/20 pregões (0.6939) sustentando por baixo, a Fib 50% (0,6962) fazendo o meio.",
                        "support": "0.6962 (Fib 50% do rali de 9 meses — segurou a segunda), com a mínima de 10/20 pregões (0.6939) e a Fib 61,8% (0.6893) abaixo.",
                        "resistance": "0.7032 (SMA200 0,7027 + Fib 38,2% — o teto virado), com a máxima de 10 pregões (0.7067) e a SMA50 (0.7092) acima.",
                        "priceAction": "Sem entrada — alinhamento misto sem rompimento confirmado não gera ticket (regra), e o par está no meio da faixa 0.6939-0.7032. Rearmar nos dois lados: fechamento sobre 0.7032 (recaptura da SMA200 + Fib 38,2%) com segundo fechamento confirmatório reabre o mapa de alta rumo à máxima de 10 pregões (0.7067); fechamento sob 0.6939 (mínima de 10/20 pregões) abre a queda rumo à Fib 61,8% (0.6893) com a σ20 comprimindo. O CPI do Q3 (≈28/10) chega para dizer se a RBA de novembro reabre o diferencial.",
                        "recommendation": "AGUARDAR OUTRO GATILHO",
                        "trigger": "Nenhum — alinhamento neutro sem rompimento confirmado: recaptura de 0.7032 exige segundo fechamento confirmatório (nível maior); fechamento sob 0.6939 abre o mapa de baixo. Próximo árbitro: CPI australiano do Q3 ≈28/10.",
                        "stop": "N/A (sem operação).",
                        "target": "N/A (sem operação).",
                        "rr": "N/A",
                        "rrValue": 0,
                        "justification": "A RBA pagou 25 pb e o mercado cobrou a frase: a “esperança” de Bullock pesou mais que a alta unânime — e o fechamento de 30/09 sob a SMA200 entregou o alinhamento que sobrevivia por 7 pips. Sem rompimento confirmado em nenhum lado da faixa 0.6939-0.7032, a regra manda esperar: o CPI do Q3 (≈28/10) chega para dizer se a RBA de novembro devolve o diferencial ao aussie."
                },
                "en": {
                        "fundamental": "AUD/USD closed at 0.6982 in the Tuesday 06/10/2026 session (ECB/Frankfurter reference rate), up +0.31% — the shelf holding the map gave way: the RBA delivered the unanimous 25-bp hike to 4.60% on Sep 29 with hawkish statement language, but Bullock's “hope” that the four hikes already delivered would be enough to bring inflation down took the next step out of the price — the pair barely moved on the announcement and the Sep-30 close (0.6968) handed over the SMA200 (0.7027), taking the bull alignment that had survived by 7 pips. The read formally turns NEUTRAL (close under the SMA200 with the 50-day 0.7092 above it) and the map locks between the flipped 0.7027-0.7032 ceiling (SMA200 + 38.2% Fib) and the 10/20-day low (0.6939) — the 50% Fib (0.6962) held Monday's slide and returned the bounce. The commodity engine still stands (CPI at 3.5%, WTI ~$83 in the Iran conflict's wake), but the momentum is the dollar's (Fed at 3.75-4.00% with one more signaled). Next arbiter: Australian Q3 CPI late October (≈Oct 28). Indicators computed from the ECB/Frankfurter daily series (557 sessions, 01/08/2024 to 06/10/2026).",
                        "trend": "Alignment flipped: close under the SMA200 (0.7027) with the 50-day (0.7092) still above it — a NEUTRAL read, with the flipped 0.7027-0.7032 ceiling blocking above, the 10/20-day low (0.6939) holding below and the 50% Fib (0.6962) marking the middle.",
                        "support": "0.6962 (50% Fib of the 9-month rally — held Monday), with the 10/20-day low (0.6939) and the 61.8% Fib (0.6893) beneath.",
                        "resistance": "0.7032 (SMA200 0.7027 + 38.2% Fib — the flipped ceiling), with the 10-day high (0.7067) and the 50-day SMA (0.7092) above.",
                        "priceAction": "No entry — a mixed alignment without a confirmed breakout issues no ticket (rule), and the pair sits mid-range 0.6939-0.7032. Re-arm both ways: a close over 0.7032 (SMA200 + 38.2% Fib reclaim) with a second confirming close reopens the bull map toward the 10-day high (0.7067); a close under 0.6939 (the 10/20-day low) opens the drop toward the 61.8% Fib (0.6893) with sigma20 compressing. The Q3 CPI (≈Oct 28) arrives to say whether November's RBA reopens the differential.",
                        "recommendation": "WAIT FOR ANOTHER TRIGGER",
                        "trigger": "None — neutral alignment without a confirmed breakout: a 0.7032 reclaim demands a second confirming close (major level); a close under 0.6939 opens the downside map. Next arbiter: Australian Q3 CPI ≈Oct 28.",
                        "stop": "N/A (no trade).",
                        "target": "N/A (no trade).",
                        "rr": "N/A",
                        "rrValue": 0,
                        "justification": "The RBA paid 25 bp and the market charged the sentence: Bullock's “hope” weighed more than the unanimous hike — and the Sep-30 close under the SMA200 handed over the alignment that had survived by 7 pips. With no confirmed breakout on either side of the 0.6939-0.7032 range, the rule says wait: the Q3 CPI (≈Oct 28) arrives to say whether November's RBA gives the differential back to the aussie."
                }
        },
        "GBP/USD": {
                "quote": "1.3276",
                "bias": "BAIXA",
                "biasType": "bear",
                "pt": {
                        "fundamental": "O GBP/USD fechou em 1,3276 na sessão de terça 06/10/2026 (taxa de referência BCE/Frankfurter), subindo +0,39% — o repique encosta no cluster que manda o mapa: o fechamento de 30/09 (1.3286) parou a 4 pips do piso da zona 1.3290-1.3330 e o gatilho armado em 28/09 expirou no fechamento de 02/10 sem disparar (ticket revogado), mas a estrutura não mudou — fechamento sob a SMA200 (1,3445) e sob a SMA50 (1,3452), viés de baixa pelo rompimento confirmado de 23/09 (fechamento sob o cluster 1.3300/1.3301, nunca recuperado) e diferencial contra a libra (Fed 3,75-4,00% com mais uma sinalizada × BoE parado em 3,75% por 6-3). A zona é rearmada com o stop alargado ao piso de volatilidade expandido (σ20 a 41 pips → piso ~61 pips): stop 1.3372. Próximos árbitros: CPI do Reino Unido ≈13/10 e BoE em 05/11. Indicadores calculados da série diária BCE/Frankfurter (557 pregões, 01/08/2024 a 06/10/2026).",
                        "trend": "Duas altas em três pregões saindo da mínima de 10/20 pregões (1.3201), mas o quadro segue de baixa: fechamento sob a SMA200 (1,3445) e sob a SMA50 (1,3452), com o cluster 1.3300/1.3301 varrido por fechamento em 23/09 e nunca recuperado — o rompimento confirmado resolve o alinhamento misto para baixo.",
                        "support": "1.3201 (mínima de 10/20 pregões), com a mínima de 9 meses (1.3160) e o redondo 1.3150 abaixo.",
                        "resistance": "1.3301 (cluster Fib 78,6% + redondo — o piso virado teto), com o fechamento quebrado de 22/09 (1.3363) e a Fib 61,8% (1.3411) acima.",
                        "priceAction": "Setup de venda no repique (rearmado): o gatilho é um fechamento diário dentro da zona devolvida 1.3290-1.3330 (cluster Fib 78,6% + redondo) seguido de fechamento sob o anterior e sob o meio da zona 1.3310 — entrada de referência 1.3310, stop 1.3372 (62 pips sobre o fechamento quebrado de 22/09, ≥ piso 1,5σ20 expandido de ~61 pips), alvo 1.3170 (140 pips, imediatamente sobre a mínima de 9 meses 1.3160), cruzando apenas o redondo 1.3250. Fechamento de volta sobre 1.3372 cancela o mapa.",
                        "recommendation": "VENDA (SHORT) NA RETRAÇÃO",
                        "trigger": "Fechamento diário dentro da zona 1.3290-1.3330 seguido de fechamento sob o anterior e sob o meio 1.3310 — entrada de referência 1.3310. Válido até o fechamento de 09/10; o CPI do Reino Unido ≈13/10 fica fora da janela de 24h.",
                        "stop": "1.3372 (sobre o fechamento quebrado de 22/09 1.3363; 62 pips ≥ piso 1,5σ20 expandido de ~61 pips) · risco sugerido ≤ 1% por operação.",
                        "target": "1.3170 (140 pips, imediatamente sobre a mínima de 9 meses 1.3160), com apenas o redondo 1.3250 no caminho.",
                        "rr": "1:2.26",
                        "rrValue": 56,
                        "justification": "A zona passou a semana inteira a 4 pips do disparo — o fechamento de 30/09 parou em 1.3286 e o gatilho de 28/09 expirou sem imprimir — mas o mapa não mudou: o diferencial segue contra a libra, o cluster segue virado e o repique de terça traz o preço a 25 pips da zona. Rearmada com o stop alargado ao piso expandido (62 pips), a venda paga 1:2,26 na soleira da mínima de 9 meses — e o BoE hawkish em 6-3 segue proibindo perseguição: o ticket só existe se a zona imprimir o fechamento."
                },
                "en": {
                        "fundamental": "GBP/USD closed at 1.3276 in the Tuesday 06/10/2026 session (ECB/Frankfurter reference rate), up +0.39% — the pullback leans on the cluster that owns the map: the Sep-30 close (1.3286) stopped 4 pips under the 1.3290-1.3330 zone floor and the trigger armed on Sep 28 expired at the Oct-2 close unfired (ticket revoked), but the structure did not change — close under the SMA200 (1.3445) and the 50-day (1.3452), bear bias by the confirmed Sep-23 breakdown (a close under the 1.3300/1.3301 cluster, never reclaimed) and a differential against sterling (Fed 3.75-4.00% with one more signaled vs a BoE parked at 3.75% by 6-3). The zone is re-armed with the stop widened to the expanded volatility floor (sigma20 at 41 pips → ~61-pip floor): stop 1.3372. Next arbiters: UK CPI ≈13/10 and the BoE on 05/11. Indicators computed from the ECB/Frankfurter daily series (557 sessions, 01/08/2024 to 06/10/2026).",
                        "trend": "Two up closes in three sessions off the 10/20-day low (1.3201), but the board stays bearish: close under the SMA200 (1.3445) and the 50-day (1.3452), with the 1.3300/1.3301 cluster swept by the Sep-23 close and never reclaimed — the confirmed breakdown resolves the mixed alignment downward.",
                        "support": "1.3201 (the 10/20-day low), with the 9-month low (1.3160) and the 1.3150 round beneath.",
                        "resistance": "1.3301 (the 78.6% Fib + round cluster — the floor turned ceiling), with the broken Sep-22 close (1.3363) and the 61.8% Fib (1.3411) above.",
                        "priceAction": "Pullback short setup (re-armed): the trigger is a daily close inside the handed-back 1.3290-1.3330 zone (78.6% Fib + round cluster) followed by a close below the previous close and below the 1.3310 zone midpoint — entry reference 1.3310, stop 1.3372 (62 pips over the broken Sep-22 close, >= the expanded ~61-pip 1.5-sigma20 floor), target 1.3170 (140 pips, just above the 9-month low 1.3160), crossing only the 1.3250 round. A close back over 1.3372 cancels the map.",
                        "recommendation": "SELL (SHORT) ON PULLBACK",
                        "trigger": "Daily close inside the 1.3290-1.3330 zone followed by a close below the previous close and below the 1.3310 midpoint — entry reference 1.3310. Valid through the 09/10 close; UK CPI ≈13/10 sits outside the 24h window.",
                        "stop": "1.3372 (over the broken Sep-22 close 1.3363; 62 pips >= the expanded ~61-pip 1.5-sigma20 floor) · suggested risk ≤ 1% per trade.",
                        "target": "1.3170 (140 pips, just above the 9-month low 1.3160), with only the 1.3250 round on the way.",
                        "rr": "1:2.26",
                        "rrValue": 56,
                        "justification": "The zone spent the whole week 4 pips from firing — the Sep-30 close stopped at 1.3286 and the Sep-28 trigger expired unprinted — but the map did not change: the differential stays against sterling, the cluster stays flipped and Tuesday's pullback brings price to 25 pips from the zone. Re-armed with the stop widened to the expanded floor (62 pips), the short pays 1:2.26 on the 9-month low's doorstep — and a hawkish 6-3 BoE still forbids chasing: the ticket only exists if the zone prints the close."
                }
        },
        "EUR/JPY": {
                "quote": "178.15",
                "bias": "BAIXA",
                "biasType": "bear",
                "pt": {
                        "fundamental": "O EUR/JPY fechou em 178,15 na sessão de terça 06/10/2026 (taxa de referência BCE/Frankfurter), subindo +0,49% — rejeição da mínima de 9 meses: o fechamento de 02/10 (176,98) cravou o novo andar e o par devolveu 117 pips em dois pregões. A decomposição segue dupla — euro caindo com o diferencial BCE × Fed (BCE parado em 2,50%, Fed a 3,75-4,00% com mais uma sinalizada) e iene oscilando com a dúvida do BoJ (1,25% em 7-2; próxima decisão 29-30/10, pausa esperada) — e o alinhamento de baixa segue pleno (SMA50 181,91 sob a SMA200 183,91, preço sob as duas). A geometria segue bloqueada: σ20 a 78 pips faz o piso de intervenção 2,5σ20 valer 195 pips (rate checks do MoF + intervenção conjunta de julho na janela de 30 dias) — a venda no repique à Fib 78,6% (179,28) exigiria stop a ~181,50 e alvo a ~175,50, território sem estrutura sob a mínima de 9 meses. Indicadores calculados da série diária BCE/Frankfurter (557 pregões, 01/08/2024 a 06/10/2026).",
                        "trend": "Mínima de 9 meses cravada em 02/10 (176,98) e rejeitada em dois pregões — fechamento sob a SMA200 (183,91) e sob a SMA50 (181,91), com a SMA50 sob a SMA200: alinhamento de baixa pleno, agora com o repique encostando na Fib 78,6% (179,28).",
                        "support": "176.98 (mínima de 9 meses, cravada em 02/10), com o redondo 176.50 abaixo — e a ausência de estrutura sob a mínima: o preço segue fazendo o piso.",
                        "resistance": "179.28 (Fib 78,6% do declínio de 9 meses), com as máximas de 10/20 pregões (180.56/180.94) acima.",
                        "priceAction": "Sem entrada — o piso de intervenção (2,5σ20 = 195 pips) reprova a venda no repique: stop a ~181,50 exigiria alvo a ~175,50, atravessando a mínima de 9 meses rumo a território sem estrutura. Rearmar: repique estruturado às máximas de 10/20 pregões (180.56-180.94) com a σ20 comprimindo abre a venda com âncora; fechamento sob 176.98 segue sem alvo estrutural. Próximo BoJ em 29-30/10 — com o Fed decidindo 48h antes.",
                        "recommendation": "AGUARDAR OUTRO GATILHO",
                        "trigger": "Nenhum — o piso de intervenção (2,5σ20 = 195 pips) reprova qualquer geometria com o preço a 113 pips da mínima de 9 meses; assistir ao MoF. BoJ em 29-30/10 (pausa esperada), com o Fed 48h antes.",
                        "stop": "N/A (sem operação).",
                        "target": "N/A (sem operação).",
                        "rr": "N/A",
                        "rrValue": 0,
                        "justification": "A mínima de 9 meses foi cravada e rejeitada em duas sessões — o roteiro clássico do piso sem estrutura: quem compra não tem âncora acima e quem vende não tem alvo abaixo. Com o piso de intervenção a 195 pips e o BoJ de outubro (29-30/10) precedido pelo Fed em 48h, a mesa fica fora até o repique entregar âncora ou a σ20 comprimir."
                },
                "en": {
                        "fundamental": "EUR/JPY closed at 178.15 in the Tuesday 06/10/2026 session (ECB/Frankfurter reference rate), up +0.49% — a rejection off the 9-month low: the Oct-2 close (176.98) pinned the new floor and the pair handed back 117 pips in two sessions. The decomposition stays double — euro falling on the ECB-Fed differential (ECB frozen at 2.50%, Fed at 3.75-4.00% with one more signaled) and the yen swinging on the BoJ doubt (1.25% by 7-2; next decision Oct 29-30, a pause expected) — and the bear alignment stays full (50-day 181.91 under the SMA200 183.91, price under both). The geometry stays blocked: sigma20 at 78 pips puts the 2.5-sigma20 intervention floor at 195 pips (MoF rate checks + the July joint intervention inside the 30-day window) — a short on the pullback to the 78.6% Fib (179.28) would need a stop at ~181.50 and a target at ~175.50, structure-less territory under the 9-month low. Indicators computed from the ECB/Frankfurter daily series (557 sessions, 01/08/2024 to 06/10/2026).",
                        "trend": "A 9-month low pinned on Oct 2 (176.98) and rejected in two sessions — close under the SMA200 (183.91) and the 50-day (181.91), with the 50-day under the 200-day: full bear alignment, now with the bounce leaning on the 78.6% Fib (179.28).",
                        "support": "176.98 (the 9-month low, pinned Oct 2), with the 176.50 round beneath — and no structure under the low: price keeps printing the floor.",
                        "resistance": "179.28 (78.6% Fib of the 9-month decline), with the 10/20-day highs (180.56/180.94) above.",
                        "priceAction": "No entry — the intervention floor (2.5-sigma20 = 195 pips) rejects the pullback short: a stop at ~181.50 would demand a target at ~175.50, crossing the 9-month low into structure-less territory. Re-arm: a structured pullback to the 10/20-day highs (180.56-180.94) with sigma20 compressing opens the anchored short; a close under 176.98 still has no structural target. Next BoJ Oct 29-30 — with the Fed deciding 48h earlier.",
                        "recommendation": "WAIT FOR ANOTHER TRIGGER",
                        "trigger": "None — the intervention floor (2.5-sigma20 = 195 pips) rejects any geometry with price 113 pips off the 9-month low; watch the MoF. BoJ Oct 29-30 (a pause expected), with the Fed 48h earlier.",
                        "stop": "N/A (no trade).",
                        "target": "N/A (no trade).",
                        "rr": "N/A",
                        "rrValue": 0,
                        "justification": "The 9-month low was pinned and rejected within two sessions — the classic script of a floor without structure: the buyer has no anchor above and the seller no target below. With the intervention floor at 195 pips and October's BoJ (Oct 29-30) preceded by the Fed by 48h, the desk stays out until the pullback delivers an anchor or sigma20 compresses."
                }
        },
        "GBP/JPY": {
                "quote": "209.89",
                "bias": "BAIXA",
                "biasType": "bear",
                "pt": {
                        "fundamental": "O GBP/JPY fechou em 209,89 na sessão de terça 06/10/2026 (taxa de referência BCE/Frankfurter), subindo +0,30% — terceiro fechamento de alta em quatro pregões: o carry BoE hawkish (3,75%, 6-3) × BoJ duvidoso (1,25%, 7-2) voltou a ser montado e o cruzamento encostou na Fib 78,6% (209,85) a 11 pips da máxima de 10 pregões (209,99). A novidade estrutural é o cruzamento: a SMA50 (212,38) passou sob a SMA200 (213,04) e o alinhamento formal virou de baixa — preço sob as duas médias. A geometria segue bloqueada nos dois lados: σ20 a 85 pips faz o piso de intervenção 2,5σ20 valer 214 pips — a venda na Fib exigiria stop a ~212,10 (sobre a Fib 61,8% 211,84 e o redondo 212,00) e alvo a ~205,50, atravessando a mínima de 9 meses (207,32) rumo a território sem estrutura; a compra exige stop sob 207,32 com alvo cruzando a escada Fib/SMA inteira. Indicadores calculados da série diária BCE/Frankfurter (557 pregões, 01/08/2024 a 06/10/2026).",
                        "trend": "Três altas em quatro pregões devolveram o carry — fechamento a 3 pips da Fib 78,6% (209,85) — mas o quadro formal virou de baixa: preço sob a SMA200 (213,04) e sob a SMA50 (212,38), agora com a SMA50 cruzando para baixo.",
                        "support": "208.07 (mínima de 10 pregões), com a mínima de 20 pregões (207.91), a de 9 meses (207.32) e o redondo 207.00 abaixo.",
                        "resistance": "209.99 (máxima de 10 pregões), com a máxima de 20 pregões (210.69) e a escada Fib 61,8% (211.84) → SMA200 + Fib 50% (213.04-213.23) acima.",
                        "priceAction": "Sem entrada — o piso de intervenção (2,5σ20 = 214 pips) reprova os dois lados: a venda na Fib 78,6% (209,85) exige alvo a ~205,50 atravessando a mínima de 9 meses; a compra exige stop sob 207,32 com alvo cruzando a escada inteira. Rearmar: fechamento sobre 210.69 (máxima de 20 pregões) reabre o mapa do carry rumo à escada Fib/SMA; fechamento sob 207.32 com a σ20 comprimindo abre a geometria de queda. Próximos árbitros: Fed em 27-28/10 e BoJ em 29-30/10.",
                        "recommendation": "AGUARDAR OUTRO GATILHO",
                        "trigger": "Nenhum — o piso de intervenção (2,5σ20 = 214 pips) reprova qualquer geometria com o preço encostado na Fib 78,6%; assistir ao MoF.",
                        "stop": "N/A (sem operação).",
                        "target": "N/A (sem operação).",
                        "rr": "N/A",
                        "rrValue": 0,
                        "justification": "O cruzamento mais caro do livro cruzou as médias para baixo justamente quando o carry voltou a ser montado — preço na Fib 78,6% com estruturas formais de baixa: o pior terreno para ticket. Com o piso a 214 pips, nenhuma direção fecha 1:2 sem atravessar primeira ordem: neutro-formal e fora, esperando o Fed (27-28/10) e o BoJ (29-30/10) decidirem o diferencial que manda."
                },
                "en": {
                        "fundamental": "GBP/JPY closed at 209.89 in the Tuesday 06/10/2026 session (ECB/Frankfurter reference rate), up +0.30% — a third up close in four sessions: the hawkish-BoE (3.75%, 6-3) × doubted-BoJ (1.25%, 7-2) carry is being rebuilt and the cross leaned on the 78.6% Fib (209.85), 11 pips under the 10-day high (209.99). The structural news is the cross: the 50-day (212.38) slipped under the SMA200 (213.04) and the formal alignment turned bearish — price under both averages. The geometry stays blocked both ways: sigma20 at 85 pips puts the 2.5-sigma20 intervention floor at 214 pips — a short at the Fib would need a stop at ~212.10 (over the 61.8% Fib 211.84 and the 212.00 round) and a target at ~205.50, crossing the 9-month low (207.32) into structure-less territory; a long needs a stop under 207.32 with a target crossing the whole Fib/SMA ladder. Indicators computed from the ECB/Frankfurter daily series (557 sessions, 01/08/2024 to 06/10/2026).",
                        "trend": "Three up closes in four sessions returned the carry — the close sits 3 pips off the 78.6% Fib (209.85) — but the formal board turned bearish: price under the SMA200 (213.04) and the 50-day (212.38), now with the 50-day crossing below.",
                        "support": "208.07 (the 10-day low), with the 20-day low (207.91), the 9-month low (207.32) and the 207.00 round beneath.",
                        "resistance": "209.99 (the 10-day high), with the 20-day high (210.69) and the 61.8% Fib (211.84) → SMA200 + 50% Fib (213.04-213.23) ladder above.",
                        "priceAction": "No entry — the intervention floor (2.5-sigma20 = 214 pips) rejects both sides: a short at the 78.6% Fib (209.85) needs a target at ~205.50 crossing the 9-month low; a long needs a stop under 207.32 with a target crossing the whole ladder. Re-arm: a close over 210.69 (the 20-day high) reopens the carry map toward the Fib/SMA ladder; a close under 207.32 with sigma20 compressing opens the breakdown geometry. Next arbiters: the Fed on Oct 27-28 and the BoJ on Oct 29-30.",
                        "recommendation": "WAIT FOR ANOTHER TRIGGER",
                        "trigger": "None — the intervention floor (2.5-sigma20 = 214 pips) rejects any geometry with price leaning on the 78.6% Fib; watch the MoF.",
                        "stop": "N/A (no trade).",
                        "target": "N/A (no trade).",
                        "rr": "N/A",
                        "rrValue": 0,
                        "justification": "The book's priciest cross put its averages into a bear cross just as the carry got rebuilt — price on the 78.6% Fib with formal bear structure: the worst ground for a ticket. With the floor at 214 pips, no direction closes 1:2 without crossing first-order structure: formally bear and out, waiting for the Fed (Oct 27-28) and the BoJ (Oct 29-30) to decide the differential that commands."
                }
        }
};'''

NEW_CHANGES = '''        const dailyChanges = {
            "EUR/USD": "+0.58%",
            "USD/JPY": "-0.09%",
            "AUD/USD": "+0.31%",
            "GBP/USD": "+0.39%",
            "EUR/JPY": "+0.49%",
            "GBP/JPY": "+0.30%"
        };'''

NEW_DRIVERS = '''        const macroDrivers = {
            "EUR/USD": {
                en: ["+1.27R banked at 1.1350", "Short on 1.1340-1.1370", "9-mo low 1.1204"],
                pt: ["+1,27R no alvo 1.1350", "Venda no repique 1,1340-1,1370", "Mín. 9 meses 1,1204"]
            },
            "USD/JPY": {
                en: ["50-day crosses under 200-day", "Cluster 158.27-158.47 caps", "2.5σ floor 203p"],
                pt: ["SMA50 cruza sob a SMA200", "Cluster 158,27-158,47 no teto", "Piso 2,5σ 203p"]
            },
            "AUD/USD": {
                en: ["RBA hike, SMA200 lost", "Read turns neutral", "Ceiling 0.7027-0.7032"],
                pt: ["Alta da RBA, SMA200 perdida", "Leitura vira neutra", "Teto 0,7027-0,7032"]
            },
            "GBP/USD": {
                en: ["Short re-armed 1.329-1.333", "Stop widened to σ floor", "9-mo low 1.3160 target"],
                pt: ["Venda rearmada 1,329-1,333", "Stop alargado ao piso σ", "Alvo mín. 9 meses 1,3160"]
            },
            "EUR/JPY": {
                en: ["9-mo low 176.98 rejected", "No structure below", "2.5σ floor 195p"],
                pt: ["Mín. 9 meses 176,98 rejeitada", "Sem estrutura abaixo", "Piso 2,5σ 195p"]
            },
            "GBP/JPY": {
                en: ["Carry back at 78.6% Fib", "Averages cross bearish", "2.5σ floor 214p"],
                pt: ["Carry de volta à Fib 78,6%", "Médias cruzam para baixo", "Piso 2,5σ 214p"]
            }
        };'''

# ---- assertion-checked replacements ----
def replace_span(html, start_marker, end_marker, new, label):
    i = html.find(start_marker)
    assert i != -1, label + ": start marker not found"
    j = html.find(end_marker, i)
    assert j != -1, label + ": end marker not found"
    j += len(end_marker)
    assert html.find(start_marker, j) == -1, label + ": start marker not unique"
    return html[:i] + new + html[j:]

html = replace_span(html, "        const forexData = {", "\n};", NEW_BLOCK, "forexData")
html = replace_span(html, "        const dailyChanges = {", "\n        };", NEW_CHANGES, "dailyChanges")
html = replace_span(html, "        const macroDrivers = {", "\n        };", NEW_DRIVERS, "macroDrivers")

n_ts = html.count(OLD_TS)
assert n_ts == 4, f"expected 4 old stamps, found {n_ts}"
html = html.replace(OLD_TS, TS)

with open(PATH, "w", encoding="utf-8", newline="") as f:
    f.write(html)

# ---- post-write validation ----
with open(PATH, encoding="utf-8") as f:
    idx = f.read()
s = idx.find("const forexData = {"); s2 = idx.find("{", s)
e = idx.find("\n};", s) + len("\n};")
data = json.loads(idx[s2:e][:-1].rstrip())
order = list(data.keys())
assert order == ["EUR/USD", "USD/JPY", "AUD/USD", "GBP/USD", "EUR/JPY", "GBP/JPY"], order
for pair, d in data.items():
    for lang in ("pt", "en"):
        for fld in ("fundamental", "trend", "support", "resistance", "priceAction", "recommendation", "trigger", "stop", "target", "rr", "justification", ):
            assert fld in d[lang], f"{pair}/{lang}: missing {fld}"
        assert d[lang]["rrValue"] == d["en"]["rrValue"]
    rr = d["en"]["rr"]
    if rr == "N/A":
        assert d["en"]["rrValue"] == 0 and "WAIT" in d["en"]["recommendation"], pair
    else:
        R = float(rr[2:])
        assert round(R * 25) == d["en"]["rrValue"], f"{pair}: rrValue {d['en']['rrValue']} != {round(R*25)}"
        assert R >= 2, pair
    assert d["bias"] == {"bull": "ALTA", "bear": "BAIXA", "neutral": "NEUTRO"}[d["biasType"]], pair
assert idx.count(TS) == 4, idx.count(TS)
print("index.html updated: forexData (6 pairs), dailyChanges, macroDrivers, 4 stamps ->", TS)
