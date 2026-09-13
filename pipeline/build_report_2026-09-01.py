#!/usr/bin/env python3
"""01/09/2026 daily report build. Data basis: Frankfurter/ECB, 511 sessions
01/09/2024-01/09/2026 (indicators_2026-09-01.json).
Post-Jackson-Hole repricing: ~57% Fed September-hike odds, DXY ~99.5, USD/JPY
broke the 10-day high into 160.16 (JGB 30y at highs), EUR/USD lost 1.1625/1.1629
by close on Monday 31/08 (1.1596) and printed 1.1590 — the SMA alignment flipped
BEARISH (close < SMA200 1.1629, SMA50 1.1491 < SMA200). NFP lands Friday 04/09
(>24h away — no event-window block today). JPY intervention window ages out
~03/09 (2.5-sigma20 floor still active on JPY pairs).
Verdicts: 3 directional (first since 28/08), 3 WAIT:
- EUR/USD BAIXA: SELL (SHORT) ON PULLBACK — zone 1.1625-1.1632 (former breakout
  floor + SMA200); entry ref 1.1620, stop 1.1665 (45p >= 1.5s20 42p), target
  1.1515 (20-day low), R/R 1:2.33.
- USD/JPY ALTA: WAIT — D10 breakout printed (160.16 > 159.73) but stop under the
  SMA200 (158.25) vs the 163.91 cap yields ~1:1.9 — gate fails; reassess ~03/09.
- AUD/USD ALTA: BUY (LONG) ON PULLBACK — zone 0.7000-0.7019 (round/SMA50);
  entry ref 0.7010, stop 0.6950 (60p >= 1.5s20 39p), target 0.7195 (20-day
  high), R/R 1:3.08.
- GBP/USD NEUTRAL: SMA50 (1.3429) slipped under SMA200 (1.3432) — alignment
  neutral again; WAIT.
- EUR/JPY ALTA: WAIT — pullback stop under the SMA200 (52p) fails the 2.5s20
  floor (95p); breakout to 187.73 yields ~1:1.5.
- GBP/JPY ALTA: BUY (LONG) ON PULLBACK — zone 215.66-215.98 (D10 low/SMA50);
  entry ref 215.75, stop 214.10 (165p >= 2.5s20 115p), target 219.10 (9-mo
  high 219.14 region), R/R 1:2.03.
Ledger: both legacy open tickets EXPIRED on 31/08 (10th session, no level
crossed) — GBP/JPY +0.17R (exit 216.24), GBP/USD -0.29R (exit 1.3539, executed
on eToro virtual). Three new watching tickets appended."""
import json, re, sys

DOCS = r"C:/Projetos/forex-report/docs"
IDX = DOCS + "/index.html"
TS = "01/09/2026 18:04 UTC"
OLD_TS = "28/08/2026 22:05 UTC"
PAGE = {
    "EUR/USD": "eur-usd.html", "USD/JPY": "usd-jpy.html", "AUD/USD": "aud-usd.html",
    "GBP/USD": "gbp-usd.html", "EUR/JPY": "eur-jpy.html", "GBP/JPY": "gbp-jpy.html",
}

A = {}
A["EUR/USD"] = dict(
    quote="1.1590", bias="BAIXA", biasType="bear",
    pt=dict(
        fundamental="O EUR/USD opera em 1,1590 no fechamento diário de 01/09/2026 (referência BCE), estável (-0,05%) — mas o regime virou: na segunda (31/08) o par perdeu por fechamento o piso 1.1625 e a SMA200 (1.1629), fechando 1.1596, e hoje consolidou sob os dois níveis. O alinhamento agora é de BAIXA (fechamento < SMA200 1.1629 e SMA50 1.1491 < SMA200) — a primeira leitura bearish desde o rompimento de 20/08, invalidada aquela resolução de alta. A reprecificação pós-Jackson Hole segue: ~57% de probabilidade de ALTA do Fed em setembro, DXY ~99,5; NFP sexta (04/09) é o árbitro do diferencial. A σ20 segue comprimida (28 pips). Indicadores (SMA 50/200, σ20, Donchian e Fibonacci) calculados da série diária BCE/Frankfurter (511 pregões, 01/09/2024 a 01/09/2026).",
        trend="Fechamento sob a SMA200 (1.1629) com SMA50 (1.1491) também abaixo — alinhamento de baixa; o antigo piso do rompimento (1.1625) vira resistência com a Fib 50% (1.1657) acima, e a mínima de 20 pregões (1.1515) abaixo.",
        support="1.1576 (mínima de 10 pregões) / 1.1582 (Fib 61,8%), com a mínima de 20 pregões (1.1515) e o redondo 1.1500 abaixo.",
        resistance="1.1625 (piso do rompimento devolvido) / 1.1629 (SMA200), com a Fib 50% (1.1657) acima.",
        priceAction="Setup de venda na retração: o preço precisa primeiro recuperar a zona 1.1625-1.1632 (piso devolvido + SMA200); o gatilho é fechamento diário abaixo do fechamento anterior sob o midpoint da zona (1.1629). Alvo 1.1515 (mínima de 20 pregões); a mínima de 10 dias (1.1576) é o degrau intermediário menor. Nota de evento: NFP sexta (04/09) — se o gatilho só disparar na quinta, reavaliar após o evento.",
        recommendation="VENDA (SHORT) NA RETRAÇÃO",
        trigger="Retração à zona 1.1625-1.1632 seguida de fechamento diário abaixo do fechamento anterior, sob o midpoint 1.1629 — entrada de referência 1.1620. Se o gatilho disparar dentro da janela de 24h do NFP (quinta), reavaliar após o evento.",
        stop="1.1665 (acima da Fib 50% 1.1657 e do redondo 1.1650; 45 pips ≥ 1,5σ20 de 42 pips) · risco sugerido ≤ 1% por operação.",
        target="1.1515 (mínima de 20 pregões, junto ao redondo 1.1500).",
        rr="1:2.33", rrValue=58,
        justification="A perda de 1.1625/1.1629 por fechamento não é ruído — devolveu o par ao alinhamento de baixa com a SMA50 já sob a SMA200 e o dólar reprecificando alta de juros. Vender na retração à zona devolvida (e não no rompimento) paga 1:2.33 com stop estruturalmente protegido pelos níveis que invalidam a tese; perseguir o preço sob 1.1590 pagaria menos e com stop pior.",
    ),
    en=dict(
        fundamental="EUR/USD trades at 1.1590 on the 01/09/2026 daily close (ECB reference), flat (-0.05%) — but the regime flipped: on Monday (Aug 31) the pair lost by close the 1.1625 floor and the 200-day SMA (1.1629), closing 1.1596, and today consolidated under both. The alignment is now BEARISH (close < SMA200 1.1629 and SMA50 1.1491 < SMA200) — the first bearish read since the Aug 20 breakout, whose bullish resolution is invalidated. The post-Jackson-Hole repricing continues: ~57% probability of a Fed September hike, DXY ~99.5; Friday's NFP (Sep 4) arbitrates the differential. Sigma20 stays compressed (28 pips). Indicators (SMA 50/200, sigma20, Donchian, Fibonacci) computed from the ECB/Frankfurter daily series (511 sessions, 01/09/2024 to 01/09/2026).",
        trend="Close under the 200-day SMA (1.1629) with the 50-day (1.1491) also below — bearish alignment; the former breakout floor (1.1625) turns resistance with the 50% Fib (1.1657) above, and the 20-day low (1.1515) beneath.",
        support="1.1576 (10-day low) / 1.1582 (61.8% Fib), with the 20-day low (1.1515) and the 1.1500 round beneath.",
        resistance="1.1625 (breakout floor handed back) / 1.1629 (200-day SMA), with the 50% Fib (1.1657) above.",
        priceAction="Sell-the-pullback setup: price must first recover the 1.1625-1.1632 zone (handed-back floor + 200-day SMA); the trigger is a daily close below the previous close under the zone midpoint (1.1629). Target 1.1515 (20-day low); the 10-day low (1.1576) is the minor intermediate step. Event note: NFP Friday (Sep 4) — if the trigger only fires Thursday, reassess after the event.",
        recommendation="SELL (SHORT) ON PULLBACK",
        trigger="Pullback into the 1.1625-1.1632 zone followed by a daily close below the previous close, under the 1.1629 midpoint — entry reference 1.1620. If the trigger fires inside the NFP 24h window (Thursday), reassess after the event.",
        stop="1.1665 (above the 50% Fib 1.1657 and the 1.1650 round; 45 pips >= the 42-pip 1.5-sigma20 floor) · suggested risk ≤ 1% per trade.",
        target="1.1515 (20-day low, by the 1.1500 round).",
        rr="1:2.33", rrValue=58,
        justification="Losing 1.1625/1.1629 by close is not noise — it returned the pair to the bearish alignment with the 50-day already under the 200-day and the dollar repricing rate hikes. Selling the pullback into the handed-back zone (rather than the breakdown) pays 1:2.33 with a stop structurally protected by the very levels that invalidate the thesis; chasing under 1.1590 would pay less with a worse stop.",
    ))

A["USD/JPY"] = dict(
    quote="160.16", bias="ALTA", biasType="bull",
    pt=dict(
        fundamental="O USD/JPY opera em 160,16 no fechamento diário de 01/09/2026 (referência BCE), subindo +0,27% e imprimindo o rompimento D10: o fechamento superou a máxima de 10 pregões (159,73) com os yields dos JGBs de 30 anos em máximas e o dólar forte (~57% de chance de alta do Fed em setembro, DXY ~99,5). O alinhamento segue de alta (SMA50 160,84 > SMA200 158,40) e a Fib 38,2% (159,60) foi reconquistada e respeitada. Mas a aritmética segue travada: com stop estrutural sob a SMA200 (158,25), o teto da máxima de 9 meses (163,91) entrega ~1:1,9 — o gate falha; e a janela de intervenção (piso 2,5σ20 ≈ 80 pips, σ20 comprimida a 32) segue ativa até ~03/09, com NFP na sexta (04/09) como evento seguinte. Indicadores calculados da série diária BCE/Frankfurter (511 pregões, 01/09/2024 a 01/09/2026).",
        trend="Acima da SMA200 (158,40) e sob a SMA50 (160,84) — alinhamento de alta; rompimento D10 confirmado (160,16 > 159,73), com a confluência SMA50 / Fib 23,6% (160,84-161,25) como teto imediato e a máxima de 9 meses (163,91) acima.",
        support="159,60 (Fib 38,2% reconquistada), com a máxima de 10 pregões (159,73) devolvida a degrau e a SMA200 (158,40) abaixo.",
        resistance="160,84 (SMA50) / 161,25 (Fib 23,6%), com a máxima de 9 meses (163,91) acima.",
        priceAction="Sem entrada — o rompimento imprimiu, mas o R/R não fecha: stop sob a SMA200 (158,25, ~191 pips do fecho) contra o teto 163,91 entrega ~1:1,9; stop mais curto falha o piso de intervenção de 2,5σ20. Reavaliar após ~03/09 (expiração da janela) ou em fechamento dentro da zona 158,25-158,70 com σ20 comprimida; NFP sexta pode redefinir o diferencial.",
        recommendation="AGUARDAR OUTRO GATILHO",
        trigger="Nenhum — rompimento D10 impresso mas R/R ~1:1,9 com stop estrutural. Reavaliar após ~03/09 (fim da janela de intervenção) ou em fechamento dentro da zona 158,25-158,70 com compressão de σ20.",
        stop="N/A (sem operação).",
        target="N/A (sem operação).",
        rr="N/A", rrValue=0,
        justification="O desenho de alta avançou — rompimento D10, Fib 38,2% reconquistada, σ20 na menor leitura da fase — mas o gate continua: mesmo mirando a máxima de 9 meses, o stop estrutural sob a SMA200 trava o R/R em ~1:1,9, e a janela de intervenção ainda impõe o piso de 2,5σ20 até ~03/09. Disciplina: deixar o rompimento correr sem nós e reavaliar na quinta.",
    ),
    en=dict(
        fundamental="USD/JPY trades at 160.16 on the 01/09/2026 daily close (ECB reference), up +0.27% and printing the D10 breakout: the close took out the 10-day high (159.73) with 30-year JGB yields at highs and the dollar firm (~57% Fed September-hike odds, DXY ~99.5). The alignment stays bullish (50-day 160.84 > 200-day 158.40) and the 38.2% Fib (159.60) was reclaimed and respected. But the arithmetic stays locked: with a structural stop under the SMA200 (158.25), the 9-month-high cap (163.91) yields ~1:1.9 — the gate fails; and the intervention window (2.5-sigma20 floor ~= 80 pips, sigma20 compressed to 32) stays active until ~Sep 3, with NFP on Friday (Sep 4) the next event. Indicators computed from the ECB/Frankfurter daily series (511 sessions, 01/09/2024 to 01/09/2026).",
        trend="Above the 200-day SMA (158.40) and under the 50-day (160.84) — bull alignment; D10 breakout confirmed (160.16 > 159.73), with the 50-day / 23.6% Fib confluence (160.84-161.25) as the immediate cap and the 9-month high (163.91) above.",
        support="159.60 (reclaimed 38.2% Fib), with the 10-day high (159.73) handed back as a step and the 200-day SMA (158.40) beneath.",
        resistance="160.84 (50-day SMA) / 161.25 (23.6% Fib), with the 9-month high (163.91) above.",
        priceAction="No entry — the breakout printed, but the R/R doesn't close: a stop under the SMA200 (158.25, ~191 pips from the close) against the 163.91 cap yields ~1:1.9; a shorter stop fails the 2.5-sigma20 intervention floor. Reassess after ~Sep 3 (window expiry) or on a close inside the 158.25-158.70 zone with compressed sigma20; Friday's NFP can redefine the differential.",
        recommendation="WAIT FOR ANOTHER TRIGGER",
        trigger="None — D10 breakout printed but R/R ~1:1.9 with a structural stop. Reassess after ~Sep 3 (intervention window ends) or on a close inside the 158.25-158.70 zone with sigma20 compression.",
        stop="N/A (no trade).",
        target="N/A (no trade).",
        rr="N/A", rrValue=0,
        justification="The bull blueprint advanced — D10 breakout, 38.2% Fib reclaimed, sigma20 at the phase's tightest — but the gate holds: even targeting the 9-month high, the structural stop under the SMA200 locks R/R at ~1:1.9, and the intervention window still imposes the 2.5-sigma20 floor until ~Sep 3. Discipline: let the breakout run without us and reassess Thursday.",
    ))

A["AUD/USD"] = dict(
    quote="0.7141", bias="ALTA", biasType="bull",
    pt=dict(
        fundamental="O AUD/USD opera em 0,7141 no fechamento diário de 01/09/2026 (referência BCE), caindo -0,29% — a retração do topo 0,7195 finalmente engatilhou: dois fechamentos em queda devolveram o redondo 0,7200 e miram a zona de compra 0.7000-0.7019 (redondo / SMA50), ainda intocada. O alinhamento segue de alta (SMA50 0,7019 > SMA200 0,6962) e o par assenta 122 pips acima da zona. A RBA segue a 4,35%; WTI ~US$ 83 e o dólar forte pós-Jackson Hole (~57% de chance de alta do Fed) pesam no curto prazo — a retração é o preço de entrada, não a invalidação. NFP sexta (04/09): gatilho disparado antes da quinta opera normal; dentro da janela, reavaliar após o evento. Indicadores calculados da série diária BCE/Frankfurter (511 pregões, 01/09/2024 a 01/09/2026).",
        trend="Acima das SMA50 (0,7019) e SMA200 (0,6962) — alinhamento de alta; a retração devolveu o redondo 0,7200 e a máxima de 20 pregões (0,7195) à condição de resistência, com a máxima de 9 meses (0,7257) acima.",
        support="0.7076 (mínima de 10 pregões), com a zona de compra 0.7000-0.7019 (redondo / SMA50) abaixo.",
        resistance="0.7195 (máxima de 20 pregões), com o redondo 0,7200 no caminho e a máxima de 9 meses (0,7257) acima.",
        priceAction="Setup de compra na retração: aguardar fechamento diário dentro da zona 0.7000-0.7019 seguido de fechamento de alta acima do midpoint (0.7010) — entrada de referência 0.7010, stop sob a SMA200/redondo (0.6950), alvo 0.7195 (máxima de 20 pregões), com 0.7257 como extensão. A mínima de 10 dias (0.7076) é o degrau intermediário, já devolvido ao campo de alta.",
        recommendation="COMPRA (LONG) NA RETRAÇÃO",
        trigger="Fechamento diário dentro da zona 0.7000-0.7019 (redondo / SMA50) seguido de fechamento acima do fechamento anterior e do midpoint 0.7010 — entrada de referência 0.7010. Dentro da janela de 24h do NFP, reavaliar após o evento.",
        stop="0.6950 (sob a SMA200 0.6962 e o redondo 0.6950; 60 pips ≥ 1,5σ20 de 39 pips) · risco sugerido ≤ 1% por operação.",
        target="0.7195 (máxima de 20 pregões; extensão 0.7257, máxima de 9 meses).",
        rr="1:3.08", rrValue=77,
        justification="A zona intocada é o gatilho que o relatório espera desde 21/08 — a retração de dois dias finalmente encaminha o preço para ela com o alinhamento de alta intacto. Comprar o redondo/SMA50 paga 1:3.08 até a máxima de 20 pregões com stop estrutural sob a SMA200; perseguir o topo pagava 1:1,4. A θ agora é do lado de quem espera.",
    ),
    en=dict(
        fundamental="AUD/USD trades at 0.7141 on the 01/09/2026 daily close (ECB reference), down -0.29% — the pullback from the 0.7195 top finally engaged: two lower closes handed back the 0.7200 round and aim at the 0.7000-0.7019 buying zone (round / 50-day SMA), still untouched. The alignment stays bullish (50-day 0.7019 > 200-day 0.6962) and the pair sits 122 pips above the zone. RBA stays at 4.35%; WTI ~$83 and the strong post-Jackson-Hole dollar (~57% Fed hike odds) weigh short-term — the pullback is the entry price, not the invalidation. NFP Friday (Sep 4): a trigger fired before Thursday trades normally; inside the window, reassess after the event. Indicators computed from the ECB/Frankfurter daily series (511 sessions, 01/09/2024 to 01/09/2026).",
        trend="Above the 50-day (0.7019) and 200-day (0.6962) SMAs — bull alignment; the pullback returned the 0.7200 round and the 20-day high (0.7195) to resistance, with the 9-month high (0.7257) above.",
        support="0.7076 (10-day low), with the 0.7000-0.7019 buying zone (round / 50-day SMA) beneath.",
        resistance="0.7195 (20-day high), with the 0.7200 round in the path and the 9-month high (0.7257) above.",
        priceAction="Buy-the-pullback setup: wait for a daily close inside the 0.7000-0.7019 zone followed by a higher close above the midpoint (0.7010) — entry reference 0.7010, stop under the SMA200/round (0.6950), target 0.7195 (20-day high), with 0.7257 as extension. The 10-day low (0.7076) is the intermediate step, already handed back to the bull field.",
        recommendation="BUY (LONG) ON PULLBACK",
        trigger="Daily close inside the 0.7000-0.7019 zone (round / 50-day SMA) followed by a close above the previous close and the 0.7010 midpoint — entry reference 0.7010. Inside the NFP 24h window, reassess after the event.",
        stop="0.6950 (under the 200-day SMA 0.6962 and the 0.6950 round; 60 pips >= the 39-pip 1.5-sigma20 floor) · suggested risk ≤ 1% per trade.",
        target="0.7195 (20-day high; extension 0.7257, the 9-month high).",
        rr="1:3.08", rrValue=77,
        justification="The untouched zone is the trigger this report has awaited since Aug 21 — the two-day pullback finally steers price toward it with the bull alignment intact. Buying the round/50-day pays 1:3.08 to the 20-day high with a structural stop under the 200-day SMA; chasing the top paid 1:1.4. The edge now sits with whoever waits.",
    ))

A["GBP/USD"] = dict(
    quote="1.3531", bias="NEUTRO", biasType="neutral",
    pt=dict(
        fundamental="O GBP/USD opera em 1,3531 no fechamento diário de 01/09/2026 (referência BCE), estável (-0,06%) e consolidando sob a Fib devolvida: a SMA50 (1.3429) escorregou sob a SMA200 (1.3432) e o alinhamento voltou a NEUTRO — o regime misto que o rompimento de 20/08 havia resolvido para a alta. Ledger: o ticket de 17/08 (executado no eToro virtual a 1.35258) expirou por tempo na segunda (31/08, 10ª sessão) com fechamento 1.3539 — R realizado -0.29. Warsh hawkish via dólar segue contra o GBP; BoE a 3,75% (6-3, próxima reunião 17/09); NFP sexta (04/09). Indicadores calculados da série diária BCE/Frankfurter (511 pregões, 01/09/2024 a 01/09/2026).",
        trend="Preço acima das SMA50 (1.3429) e SMA200 (1.3432), mas com SMA50 sob a SMA200 — alinhamento neutro; fechamentos sob a Fib 23,6% (1.3644) devolvida, com a máxima de 20 pregões (1.3656) acima e a mínima de 20 pregões (1.3446) abaixo.",
        support="1.3446 (mínima de 20 pregões), com a confluência SMA50/SMA200 (1.3429-1.3432) e o redondo 1.3400 abaixo.",
        resistance="1.3644 (Fib 23,6% devolvida), com a máxima de 20 pregões (1.3656) e a de 9 meses (1.3817) acima.",
        priceAction="Sem gatilho — alinhamento neutro exige critério de rompimento: (a) fechamento sob a confluência 1.3429-1.3432 abre 1.3346-1.3260 (Fib 61,8% / mínima de 9 meses) e reorienta o viés para baixa; (b) reconquista por fechamento acima de 1.3656 devolve a leitura de alta. Até lá, sem entrada.",
        recommendation="AGUARDAR OUTRO GATILHO",
        trigger="Nenhum — alinhamento neutro. Assistir a perda da confluência 1.3429-1.3432 ou a reconquista de 1.3656 para definir o próximo setup.",
        stop="N/A (sem operação).",
        target="N/A (sem operação).",
        rr="N/A", rrValue=0,
        justification="O cruzamento de médias virou (SMA50 sob a SMA200) e a resolução de alta de 20/08 está formalmente desfeita — sem alinhamento, qualquer entrada seria aposta, não setup. O ticket legado expirou perto do flat (-0.29R) e o campo agora é decidido entre a confluência 1.3429-1.3432 e a reconquista de 1.3656.",
    ),
    en=dict(
        fundamental="GBP/USD trades at 1.3531 on the 01/09/2026 daily close (ECB reference), flat (-0.06%) and consolidating under the handed-back Fib: the 50-day SMA (1.3429) slipped under the 200-day (1.3432) and the alignment returned to NEUTRAL — the mixed regime the Aug 20 breakout had resolved bullish. Ledger: the Aug 17 ticket (executed on eToro virtual at 1.35258) expired on time Monday (Aug 31, 10th session) with a 1.3539 close — realized R -0.29. Hawkish-Warsh dollar pressure stays against GBP; BoE at 3.75% (6-3, next meeting Sep 17); NFP Friday (Sep 4). Indicators computed from the ECB/Frankfurter daily series (511 sessions, 01/09/2024 to 01/09/2026).",
        trend="Price above the 50-day (1.3429) and 200-day (1.3432) SMAs, but with the 50-day under the 200-day — neutral alignment; closes under the handed-back 23.6% Fib (1.3644), with the 20-day high (1.3656) above and the 20-day low (1.3446) beneath.",
        support="1.3446 (20-day low), with the 50/200-day SMA confluence (1.3429-1.3432) and the 1.3400 round beneath.",
        resistance="1.3644 (23.6% Fib handed back), with the 20-day high (1.3656) and the 9-month high (1.3817) above.",
        priceAction="No trigger — neutral alignment demands a breakout criterion: (a) a close under the 1.3429-1.3432 confluence opens 1.3346-1.3260 (61.8% Fib / 9-month low) and reorients the bias bearish; (b) a reclaim close above 1.3656 restores the bullish read. Until then, no entry.",
        recommendation="WAIT FOR ANOTHER TRIGGER",
        trigger="None — neutral alignment. Watch the loss of the 1.3429-1.3432 confluence or the reclaim of 1.3656 to define the next setup.",
        stop="N/A (no trade).",
        target="N/A (no trade).",
        rr="N/A", rrValue=0,
        justification="The moving-average cross flipped (50-day under the 200-day) and the Aug 20 bullish resolution is formally undone — without alignment, any entry would be a bet, not a setup. The legacy ticket expired near flat (-0.29R) and the field is now decided between the 1.3429-1.3432 confluence and the 1.3656 reclaim.",
    ))

A["EUR/JPY"] = dict(
    quote="185.63", bias="ALTA", biasType="bull",
    pt=dict(
        fundamental="O EUR/JPY opera em 185,63 no fechamento diário de 01/09/2026 (referência BCE), subindo +0,22% e dançando sob a máxima de 10 pregões (185,91): o alinhamento segue pleno de alta (SMA50 184,80 > SMA200 184,18) e a σ20 comprimiu a 38 pips — mas a janela de intervenção (ativa até ~03/09) mantém o piso 2,5σ20 (≈95 pips): uma retração à zona 184,62-184,80 (mínima D10 / SMA50) exige stop sob a SMA200 (184,18, ~52-60 pips da entrada) — falha o piso; e o rompimento acima de 185,91 contra o teto da máxima de 9 meses (187,73) entrega ~1:1,5 com stop aprovado. O keynote hawkish de Warsh sustenta o diferencial BCE-BoJ (e o risco de jawboning do MoF). Indicadores calculados da série diária BCE/Frankfurter (511 pregões, 01/09/2024 a 01/09/2026).",
        trend="Acima das SMA50 (184,80) e SMA200 (184,18) — alinhamento de alta pleno; fechamento colado sob a máxima de 10/20 pregões (185,91), com a Fib 23,6% (185,97) e a máxima de 9 meses (187,73) acima.",
        support="184.80 (SMA50) / 184.62 (mínima de 10 pregões), com a SMA200 (184.18) e a Fib 50% (184,14) abaixo.",
        resistance="185.91 (máximas de 10/20 pregões) / 185.97 (Fib 23,6%), com a máxima de 9 meses (187,73) acima.",
        priceAction="Sem entrada — o piso de intervenção (2,5σ20 ≈ 95 pips) reprova o stop da retração (~52-60 pips) e o rompimento entrega ~1:1,5. Reavaliar após ~03/09 (expiração da janela): com a σ20 a 38 pips, a aritmética do gate pode virar na quinta.",
        recommendation="AGUARDAR OUTRO GATILHO",
        trigger="Nenhum — piso de intervenção ativo até ~03/09 reprova o setup de retração e o rompimento entrega ~1:1,5. Reavaliar após a expiração da janela ou em retração profunda à zona 183,13-184,14 (Fib 61,8-50%).",
        stop="N/A (sem operação).",
        target="N/A (sem operação).",
        rr="N/A", rrValue=0,
        justification="A compressão de volatilidade (87 → 38 pips desde 28/08) aproximou o gate, mas a janela de intervenção ainda impõe 95 pips de piso contra um stop estrutural de ~52-60 — e o teto de 187,73 não paga o rompimento. A estrutura segue de alta e a quinta (~03/09) pode destravar a aritmética; até lá, sem operação.",
    ),
    en=dict(
        fundamental="EUR/JPY trades at 185.63 on the 01/09/2026 daily close (ECB reference), up +0.22% and dancing under the 10-day high (185.91): the alignment stays fully bullish (50-day 184.80 > 200-day 184.18) and sigma20 compressed to 38 pips — but the intervention window (active until ~Sep 3) holds the 2.5-sigma20 floor (~=95 pips): a pullback to the 184.62-184.80 zone (D10 low / 50-day SMA) requires a stop under the 200-day (184.18, ~52-60 pips from entry) — it fails the floor; and the breakout above 185.91 against the 9-month-high cap (187.73) yields ~1:1.5 with an approved stop. Warsh's hawkish keynote sustains the ECB-BoJ differential (and the MoF's jawboning risk). Indicators computed from the ECB/Frankfurter daily series (511 sessions, 01/09/2024 to 01/09/2026).",
        trend="Above the 50-day (184.80) and 200-day (184.18) SMAs — full bull alignment; close glued under the 10/20-day high (185.91), with the 23.6% Fib (185.97) and the 9-month high (187.73) above.",
        support="184.80 (50-day SMA) / 184.62 (10-day low), with the 200-day SMA (184.18) and the 50% Fib (184.14) beneath.",
        resistance="185.91 (10/20-day highs) / 185.97 (23.6% Fib), with the 9-month high (187.73) above.",
        priceAction="No entry — the intervention floor (2.5-sigma20 ~= 95 pips) rejects the pullback stop (~52-60 pips) and the breakout yields ~1:1.5. Reassess after ~Sep 3 (window expiry): with sigma20 at 38 pips, the gate's arithmetic may flip on Thursday.",
        recommendation="WAIT FOR ANOTHER TRIGGER",
        trigger="None — intervention floor active until ~Sep 3 rejects the pullback setup and the breakout yields ~1:1.5. Reassess after the window expires or on a deep pullback to the 183.13-184.14 zone (61.8-50% Fib).",
        stop="N/A (no trade).",
        target="N/A (no trade).",
        rr="N/A", rrValue=0,
        justification="The volatility compression (87 → 38 pips since Aug 28) brought the gate closer, but the intervention window still imposes a 95-pip floor against a ~52-60-pip structural stop — and the 187.73 cap doesn't pay for the breakout. The structure stays bullish and Thursday (~Sep 3) may unlock the arithmetic; until then, no trade.",
    ))

A["GBP/JPY"] = dict(
    quote="216.71", bias="ALTA", biasType="bull",
    pt=dict(
        fundamental="O GBP/JPY opera em 216,71 no fechamento diário de 01/09/2026 (referência BCE), subindo +0,21%. Ledger: o ticket de 14/08 (entrada 215,90, stop 213,90, alvo 219,00) expirou por tempo na segunda (31/08, 10ª sessão) com fechamento 216,24 — R realizado +0.17, a colheita ficando a ~1,2% do alvo. A estrutura segue de alta plena (SMA50 215,98 > SMA200 212,75) e o piso de intervenção 2,5σ20 agora é ≈115 pips (σ20 comprimida a 46) — a aritmética que travava adições afrouxou: uma retração à zona 215.66-215.98 (mínima D10 / SMA50) com stop sob a Fib 61,8% (214,14) passa no gate e paga 1:2.03 contra o topo de 9 meses (219,14). Janela de intervenção expira ~03/09; BoJ em setembro é o próximo foco institucional. Indicadores calculados da série diária BCE/Frankfurter (511 pregões, 01/09/2024 a 01/09/2026).",
        trend="Acima das SMA50 (215,98) e SMA200 (212,75) — alinhamento de alta pleno; fechamento sob a máxima de 10/20 pregões (217,07), com a máxima de 9 meses (219,14) acima.",
        support="215.98 (SMA50) / 215.66 (mínima de 10 pregões), com a Fib 61,8% (214,14) e a de 38,2% (211,33) abaixo.",
        resistance="217.07 (máximas de 10/20 pregões), com a máxima de 9 meses (219,14) acima.",
        priceAction="Setup de compra na retração: aguardar fechamento diário dentro da zona 215.66-215.98 (mínima D10 / SMA50) seguido de fechamento de alta — entrada de referência 215.75, stop 214.10 (sob a Fib 61,8%), alvo 219.10 (região da máxima de 9 meses). A perda por fechamento da Fib 61,8% (214,14) invalida o setup.",
        recommendation="COMPRA (LONG) NA RETRAÇÃO",
        trigger="Fechamento diário dentro da zona 215.66-215.98 (mínima D10 / SMA50) seguido de fechamento acima do fechamento anterior — entrada de referência 215.75. Reavaliar se o disparo ocorrer após ~03/09 com a janela de intervenção expirada (o piso afrouxa para 1,5σ20).",
        stop="214.10 (sob a Fib 61,8% 214.14; 165 pips ≥ 2,5σ20 de 115 pips) · risco sugerido ≤ 1% por operação.",
        target="219.10 (região da máxima de 9 meses 219.14).",
        rr="1:2.03", rrValue=51,
        justification="O ticket legado expirou a 1,2% do alvo e a estrutura não mudou — o que mudou é a aritmética: com a σ20 comprimida a 46 pips, o piso de intervenção caiu de ~265 para ~115 pips e a zona D10/SMA50 finalmente comporta um stop estrutural aprovado com R/R de 1:2.03. Comprar a retração à zona, não o topo de 217.",
    ),
    en=dict(
        fundamental="GBP/JPY trades at 216.71 on the 01/09/2026 daily close (ECB reference), up +0.21%. Ledger: the Aug 14 ticket (entry 215.90, stop 213.90, target 219.00) expired on time Monday (Aug 31, 10th session) with a 216.24 close — realized R +0.17, the harvest stopping ~1.2% shy of target. The structure stays fully bullish (50-day 215.98 > 200-day 212.75) and the 2.5-sigma20 intervention floor is now ~=115 pips (sigma20 compressed to 46) — the arithmetic that blocked adds has loosened: a pullback to the 215.66-215.98 zone (D10 low / 50-day SMA) with a stop under the 61.8% Fib (214.14) passes the gate and pays 1:2.03 against the 9-month top (219.14). Intervention window expires ~Sep 3; the BoJ's September meeting is the next institutional focus. Indicators computed from the ECB/Frankfurter daily series (511 sessions, 01/09/2024 to 01/09/2026).",
        trend="Above the 50-day (215.98) and 200-day (212.75) SMAs — full bull alignment; close under the 10/20-day high (217.07), with the 9-month high (219.14) above.",
        support="215.98 (50-day SMA) / 215.66 (10-day low), with the 61.8% Fib (214.14) and the 38.2% (211.33) beneath.",
        resistance="217.07 (10/20-day highs), with the 9-month high (219.14) above.",
        priceAction="Buy-the-pullback setup: wait for a daily close inside the 215.66-215.98 zone (D10 low / 50-day SMA) followed by a higher close — entry reference 215.75, stop 214.10 (under the 61.8% Fib), target 219.10 (9-month-high region). A close below the 61.8% Fib (214.14) invalidates the setup.",
        recommendation="BUY (LONG) ON PULLBACK",
        trigger="Daily close inside the 215.66-215.98 zone (D10 low / 50-day SMA) followed by a close above the previous close — entry reference 215.75. Reassess if the fire comes after ~Sep 3 with the intervention window expired (the floor loosens to 1.5-sigma20).",
        stop="214.10 (under the 61.8% Fib 214.14; 165 pips >= the 115-pip 2.5-sigma20 floor) · suggested risk ≤ 1% per trade.",
        target="219.10 (9-month-high region, 219.14).",
        rr="1:2.03", rrValue=51,
        justification="The legacy ticket expired 1.2% from target and the structure didn't change — what changed is the arithmetic: with sigma20 compressed to 46 pips, the intervention floor fell from ~265 to ~115 pips and the D10/50-day zone finally fits an approved structural stop at 1:2.03 R/R. Buy the pullback into the zone, not the 217 top.",
    ))

# ---------------- helpers ----------------
def rep(text, old, new, where, n=1):
    c = text.count(old)
    if c != n:
        sys.exit(f"ERROR [{where}]: expected {n} occurrence(s), found {c}: {old[:80]}...")
    return text.replace(old, new)

# ---------------- index.html ----------------
with open(IDX, encoding="utf-8") as f:
    idx = f.read()
s = idx.find("        const forexData = {")
if s == -1:
    sys.exit("ERROR: forexData block not found")
e = idx.find("\n};", s) + len("\n};")
old_block = idx[s:e]
old_data = json.loads(old_block[old_block.find("{"):-1].rstrip())

def field(v):
    return json.dumps(v, ensure_ascii=False)
lines = ['        const forexData = {']
for i, pair in enumerate(["EUR/USD", "USD/JPY", "AUD/USD", "GBP/USD", "EUR/JPY", "GBP/JPY"]):
    d = A[pair]
    comma = "," if i < 5 else ""
    lines.append(f'          "{pair}": {{')
    lines.append(f'                    "quote": {field(d["quote"])},')
    lines.append(f'                    "bias": {field(d["bias"])},')
    lines.append(f'                    "biasType": {field(d["biasType"])},')
    for lang in ("pt", "en"):
        lines.append(f'                    "{lang}": {{')
        flds = ["fundamental", "trend", "support", "resistance", "priceAction",
                "recommendation", "trigger", "stop", "target", "rr", "rrValue", "justification"]
        for j, fl in enumerate(flds):
            cm = "," if j < len(flds) - 1 else ""
            lines.append(f'                              "{fl}": {field(d[lang][fl])}{cm}')
        cm = "," if lang == "pt" else ""
        lines.append(f'                    }}{cm}')
    lines.append(f'          }}{comma}')
lines.append("};")
new_block = "\n".join(lines)

s2 = idx.find("        const forexData = {")
e2 = idx.find("\n};", s2) + len("\n};")
idx = idx[:s2] + new_block + idx[e2:]

m = re.search(r'(id="generationTime"[^>]*>Reports generated on: )[^<]*(</p>)', idx)
if not m:
    sys.exit("ERROR: generationTime not found")
idx = idx[:m.start()] + m.group(1) + TS + m.group(2) + idx[m.end():]
if idx.count(OLD_TS) != 2:
    sys.exit(f"ERROR: expected 2 old timestamps, found {idx.count(OLD_TS)}")
idx = idx.replace(OLD_TS, TS)

old_changes = '''        const dailyChanges = {
            "EUR/USD": "-0.02%",
            "USD/JPY": "+0.18%",
            "AUD/USD": "+0.07%",
            "GBP/USD": "+0.01%",
            "EUR/JPY": "+0.16%",
            "GBP/JPY": "+0.19%"
        };'''
new_changes = '''        const dailyChanges = {
            "EUR/USD": "-0.05%",
            "USD/JPY": "+0.27%",
            "AUD/USD": "-0.29%",
            "GBP/USD": "-0.06%",
            "EUR/JPY": "+0.22%",
            "GBP/JPY": "+0.21%"
        };'''
idx = rep(idx, old_changes, new_changes, "ticker")
old_be = 'dataBasis: "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 530 daily sessions (01/08/2024–28/08/2026).",'
new_be = 'dataBasis: "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 511 daily sessions (01/09/2024–01/09/2026).",'
old_bp = 'dataBasis: "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, sigma20 e Donchian calculados · 530 pregões (01/08/2024 a 28/08/2026).",'
new_bp = 'dataBasis: "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, sigma20 e Donchian calculados · 511 pregões (01/09/2024 a 01/09/2026).",'
idx = rep(idx, old_be, new_be, "dataBasis EN")
idx = rep(idx, old_bp, new_bp, "dataBasis PT")

with open(IDX, "w", encoding="utf-8") as f:
    f.write(idx)
print("OK: index.html")

# ---------------- static pages ----------------
GAUGE = {"EUR/USD": 29, "USD/JPY": 45, "AUD/USD": 55, "GBP/USD": 43, "EUR/JPY": 75, "GBP/JPY": 67}
OLD_GAUGE = {"EUR/USD": 50, "USD/JPY": 51, "AUD/USD": 30, "GBP/USD": 16, "EUR/JPY": 39, "GBP/JPY": 31}

BLUF = {
 "EUR/USD": [('<span class="bluf-action wait">WAIT</span> — pullback under the 1.1657 Fib toward the 200-day; Jackson Hole reaction due Monday</span>',
              '<span class="bluf-action sell">SELL</span> — regime flipped bearish; short the pullback into 1.1625-1.1632, target 1.1515</span>'),
             ('<span class="bluf-action wait">AGUARDAR</span> — retração sob a Fib 1.1657 rumo à SMA200; reação de Jackson Hole sai segunda</span>',
              '<span class="bluf-action sell">VENDA</span> — regime virou de baixa; vender a retração a 1.1625-1.1632, alvo 1.1515</span>')],
 "USD/JPY": [('<span class="bluf-action wait">WAIT</span> — pressing the 10-day high (159.70); intervention floor until ~03/09</span>',
              '<span class="bluf-action wait">WAIT</span> — D10 breakout into 160.16 printed; R/R to 163.91 still fails (~1:1.9)</span>'),
             ('<span class="bluf-action wait">AGUARDAR</span> — pressionando a máxima de 10 dias (159,70); piso de intervenção até ~03/09</span>',
              '<span class="bluf-action wait">AGUARDAR</span> — rompimento D10 em 160,16 impresso; R/R rumo a 163,91 segue falhando (~1:1,9)</span>')],
 "AUD/USD": [('<span class="bluf-action wait">WAIT</span> — breakout extended; 0.7200/0.7257 caps; zone pullback still the trigger</span>',
              '<span class="bluf-action buy">BUY</span> — pullback engaged; buy the 0.7000-0.7019 zone, target 0.7195 (R/R 1:3.08)</span>'),
             ('<span class="bluf-action wait">AGUARDAR</span> — rompimento estendido; tetos 0.7200/0.7257; retração à zona segue sendo o gatilho</span>',
              '<span class="bluf-action buy">COMPRA</span> — retração engatilhada; comprar a zona 0.7000-0.7019, alvo 0.7195 (R/R 1:3,08)</span>')],
 "GBP/USD": [('<span class="bluf-action wait">WAIT</span> — deep pullback toward 1.3538; position +24 pips; expiry check Monday</span>',
              '<span class="bluf-action wait">WAIT</span> — 50-day slipped under the 200-day: neutral again; 1.3429-1.3432 vs 1.3656</span>'),
             ('<span class="bluf-action wait">AGUARDAR</span> — retração profunda rumo a 1.3538; posição +24 pips; checagem de expiração segunda</span>',
              '<span class="bluf-action wait">AGUARDAR</span> — SMA50 escorregou sob a SMA200: neutro de novo; 1.3429-1.3432 vs 1.3656</span>')],
 "EUR/JPY": [('<span class="bluf-action wait">WAIT</span> — fresh 10-day highs against the intervention wall (~1:0.8)</span>',
              '<span class="bluf-action wait">WAIT</span> — under 185.91; intervention floor still rejects the pullback stop</span>'),
             ('<span class="bluf-action wait">AGUARDAR</span> — novas máximas de 10 dias contra o muro de intervenção (~1:0,8)</span>',
              '<span class="bluf-action wait">AGUARDAR</span> — sob 185,91; piso de intervenção segue rejeitando o stop da retração</span>')],
 "GBP/JPY": [('<span class="bluf-action wait">WAIT</span> — position +99 pips; expiry check Monday; floor until ~03/09</span>',
              '<span class="bluf-action buy">BUY</span> — legacy ticket expired +0.17R; buy the 215.66-215.98 zone, target 219.10</span>'),
             ('<span class="bluf-action wait">AGUARDAR</span> — posição +99 pips; checagem de expiração segunda; piso até ~03/09</span>',
              '<span class="bluf-action buy">COMPRA</span> — ticket legado expirou +0,17R; comprar a zona 215.66-215.98, alvo 219.10</span>')],
}

NEXT_EVENT = {
 "EUR/USD": ("Jackson Hole reaction", "NFP Friday 04/09",
             "Reação de Jackson Hole", "NFP sexta 04/09"),
 "USD/JPY": ("BoJ Sep meeting &amp; MoF", "MoF window ~03/09 · NFP 04/09",
             "BoJ em setembro e MoF", "Janela MoF ~03/09 · NFP 04/09"),
 "AUD/USD": ("China data &amp; JH reaction", "NFP Friday 04/09",
             "Dados da China e reação do JH", "NFP sexta 04/09"),
 "GBP/USD": ("Jackson Hole reaction", "NFP Friday 04/09",
             "Reação de Jackson Hole", "NFP sexta 04/09"),
 "EUR/JPY": ("BoJ September meeting", "MoF window ~03/09",
             "Reunião do BoJ em setembro", "Janela MoF ~03/09"),
 "GBP/JPY": ("BoJ September meeting", "MoF window ~03/09",
             "Reunião de setembro do BoJ", "Janela MoF ~03/09"),
}

GAUGE_LABELS = {
 "EUR/USD": ("1.1643", "1.1590", [("l", "1.1629", "1.1515"), ("r", "1.1657", "1.1632")]),
 "USD/JPY": ("159.68", "160.16", []),  # rgv-l 158.27 / rgv-r 161.02 unchanged
 "AUD/USD": ("0.7195", "0.7141", [("l", "0.7168", "0.7019")]),  # rgv-r 0.7257 unchanged
 "GBP/USD": ("1.3583", "1.3531", [("l", "1.3538", "1.3432")]),  # rgv-r 1.3656 unchanged
 "EUR/JPY": ("185.91", "185.63", []),  # rgv-l 184.77 / rgv-r 187.73 unchanged
 "GBP/JPY": ("216.89", "216.71", []),  # rgv-l 215.87 / rgv-r 219.14 unchanged
}

# bias/verdict class + label swaps; conviction + rr-seal on directional pages
BIAS_SWAP = {
 "EUR/USD": ("bull", "bear", "BULLISH", "BEARISH", "ALTA", "BAIXA"),
 "GBP/USD": ("bull", "neutral", "BULLISH", "NEUTRAL", "ALTA", "NEUTRO"),
}
VERDICT_SWAP = {
 "EUR/USD": ("wait", "sell", "WAIT FOR ANOTHER TRIGGER", "SELL (SHORT) ON PULLBACK",
             "AGUARDAR OUTRO GATILHO", "VENDA (SHORT) NA RETRAÇÃO"),
 "AUD/USD": ("wait", "buy", "WAIT FOR ANOTHER TRIGGER", "BUY (LONG) ON PULLBACK",
             "AGUARDAR OUTRO GATILHO", "COMPRA (LONG) NA RETRAÇÃO"),
 "GBP/JPY": ("wait", "buy", "WAIT FOR ANOTHER TRIGGER", "BUY (LONG) ON PULLBACK",
             "AGUARDAR OUTRO GATILHO", "COMPRA (LONG) NA RETRAÇÃO"),
}
CONVICTION = {"EUR/USD": ("0/10", "7/10"), "AUD/USD": ("0/10", "9/10"), "GBP/JPY": ("0/10", "6/10")}
RR_SEAL = {"EUR/USD": "1:2.33", "AUD/USD": "1:3.08", "GBP/JPY": "1:2.03"}

for pair, fname in PAGE.items():
    path = f"{DOCS}/{fname}"
    with open(path, encoding="utf-8") as f:
        h = f.read()
    od, nd = old_data[pair], A[pair]
    # 1) BLUF inner text
    for old, new in BLUF[pair]:
        h = rep(h, old, new, f"{fname} BLUF")
    # 2) bias classes/labels
    if pair in BIAS_SWAP:
        ob, nb, oen_b, nen_b, opt_b, npt_b = BIAS_SWAP[pair]
        h = rep(h, f'<article class="report-container bias-{ob}"', f'<article class="report-container bias-{nb}"', f"{fname} article bias")
        h = rep(h, f'<div class="bias-badge bias-{ob}">', f'<div class="bias-badge bias-{nb}">', f"{fname} bias badge")
        h = rep(h, f'>{pair} - {oen_b}</span>', f'>{pair} - {nen_b}</span>', f"{fname} bias EN")
        h = rep(h, f'>{pair} - {opt_b}</span>', f'>{pair} - {npt_b}</span>', f"{fname} bias PT")
    # 3) verdict class + badge text
    if pair in VERDICT_SWAP:
        ov, nv, oen_v, nen_v, opt_v, npt_v = VERDICT_SWAP[pair]
        h = rep(h, f'<div class="trade-ticket verdict-{ov}">', f'<div class="trade-ticket verdict-{nv}">', f"{fname} ticket verdict")
        h = rep(h, f'<span class="verdict-badge {ov}">', f'<span class="verdict-badge {nv}">', f"{fname} verdict badge")
        h = rep(h, f'<span class="lang-en">{oen_v}</span>', f'<span class="lang-en">{nen_v}</span>', f"{fname} verdict EN")
        h = rep(h, f'<span class="lang-pt" style="display:none;">{opt_v}</span>', f'<span class="lang-pt" style="display:none;">{npt_v}</span>', f"{fname} verdict PT")
    # 4) fields (recommendation on swapped pairs already handled by the badge text)
    for lang in ("pt", "en"):
        skip_rec = pair in VERDICT_SWAP
        skip_st = False
        # stop/target cards share the identical old "N/A" text — replace in order
        if od[lang]["stop"] == od[lang]["target"] and (nd[lang]["stop"] != od[lang]["stop"] or nd[lang]["target"] != od[lang]["target"]):
            skip_st = True
            for fl in ("stop", "target"):
                oldv = od[lang][fl]
                i = h.find(oldv)
                if i == -1:
                    sys.exit(f"ERROR [{fname} {lang}.{fl}]: not found")
                h = h[:i] + nd[lang][fl] + h[i + len(oldv):]
        flds = ["fundamental", "trend", "support", "resistance", "priceAction",
                "trigger", "justification"]
        if not skip_st:
            flds += ["stop", "target"]
        if not skip_rec:
            flds.append("recommendation")
        for fl in flds:
            oldv, newv = od[lang][fl], nd[lang][fl]
            if oldv == newv:
                continue
            h = rep(h, oldv, newv, f"{fname} {lang}.{fl}", 1)
    # 5) rr-seal + conviction
    if pair in RR_SEAL:
        h = rep(h, '<span class="rr-seal">N/A</span>', f'<span class="rr-seal">{RR_SEAL[pair]}</span>', f"{fname} rr-seal")
        oc, nc = CONVICTION[pair]
        h = rep(h, f'>{oc} &middot;', f'>{nc} &middot;', f"{fname} conviction")
    # 6) quote strong
    h = rep(h, f'<strong>{od["quote"]}</strong>', f'<strong>{nd["quote"]}</strong>', f"{fname} quote strong")
    # 7) gauge position (now + marker)
    h = rep(h, f'left: {OLD_GAUGE[pair]}%', f'left: {GAUGE[pair]}%', f"{fname} gauge", 2)
    old_now, new_now, rgv_swaps = GAUGE_LABELS[pair]
    h = rep(h, f'>{old_now}</div>', f'>{new_now}</div>', f"{fname} gauge now-label")
    for side, old_rgv, new_rgv in rgv_swaps:
        h = rep(h, f'<span class="rgv-{side}">{old_rgv}</span>', f'<span class="rgv-{side}">{new_rgv}</span>', f"{fname} rgv-{side}")
    # 8) next-event line
    oen, nen, opt_, npt = NEXT_EVENT[pair]
    h = rep(h, f'<span class="lang-en">{oen}</span>', f'<span class="lang-en">{nen}</span>', f"{fname} next-event EN")
    h = rep(h, f'<span class="lang-pt" style="display:none;">{opt_}</span>', f'<span class="lang-pt" style="display:none;">{npt}</span>', f"{fname} next-event PT")
    # 9) ticket serial date
    h = rep(h, '<span class="ts-date">14·08·26</span>', '<span class="ts-date">01·09·26</span>', f"{fname} ts-date")
    with open(path, "w", encoding="utf-8") as f:
        f.write(h)
    print(f"OK: {fname} ({pair})")

# pages' data-basis lines + chip refreshes
for fname in PAGE.values():
    p = f"{DOCS}/{fname}"
    with open(p, encoding="utf-8") as f:
        h = f.read()
    oen = "ECB/Frankfurter reference rates · SMA50/200, sigma20 &amp; Donchian computed · 530 daily sessions (01/08/2024–28/08/2026)."
    nen = "ECB/Frankfurter reference rates · SMA50/200, sigma20 &amp; Donchian computed · 511 daily sessions (01/09/2024–01/09/2026)."
    opt = "taxas de referência BCE/Frankfurter · SMA50/200, sigma20 e Donchian calculados · 530 pregões (01/08/2024 a 28/08/2026)."
    npt = "taxas de referência BCE/Frankfurter · SMA50/200, sigma20 e Donchian calculados · 511 pregões (01/09/2024 a 01/09/2026)."
    h = rep(h, oen, nen, f"{fname} basis EN")
    h = rep(h, opt, npt, f"{fname} basis PT")
    if fname == "eur-usd.html":
        h = rep(h, '<span class="macro-chip lang-en">Warsh hawkish JH</span>', '<span class="macro-chip lang-en">Fed Sep hike ~57%</span>', f"{fname} chip EN 1")
        h = rep(h, '<span class="macro-chip lang-pt" style="display:none;">Warsh hawkish (JH)</span>', '<span class="macro-chip lang-pt" style="display:none;">Alta Fed set ~57%</span>', f"{fname} chip PT 1")
    with open(p, "w", encoding="utf-8") as f:
        f.write(h)
print("OK: 6 pages data-basis + chips")

# ---------------- track-record ledger ----------------
LED = DOCS + "/track-record.json"
led = json.load(open(LED, encoding="utf-8"))
led["meta"]["lastUpdated"] = "01/09/2026"
open_tickets = [t for t in led.get("open", [])]
for t in open_tickets:
    t["outcome"] = "expired"
    t["exitDate"] = "31/08/2026"
    if t["pair"] == "GBP/JPY":
        t["exit"] = 216.24
        t["realizedR"] = round((216.24 - 215.90) / (215.90 - 213.90), 2)  # +0.17
        t["note"] = "legacy 14/08 ticket: expired on time at the 10th session (31/08 close 216.24, +34 pips; neither 219.00 nor 213.90 close-crossed)"
    else:
        t["exit"] = 1.3539
        t["realizedR"] = round((1.3539 - 1.3559) / (1.3559 - 1.3490), 2)  # -0.29
        t["note"] = "17/08 ticket (eToro virtual fill 1.35258): expired on time at the 10th session (31/08 close 1.3539; neither 1.3800 nor 1.3490 close-crossed)"
    led.setdefault("closed", []).append(t)
led["open"] = []
led["watching"] = [
    {
        "pair": "EUR/USD", "reportDate": "01/09/2026", "direction": "short", "setup": "pullback",
        "entry": 1.1620, "stop": 1.1665, "target": 1.1515, "plannedR": 2.33,
        "triggerRule": "daily close inside 1.1625-1.1632 (handed-back floor + SMA200) followed by a close below the previous close under the 1.1629 midpoint; skip if inside the NFP 24h window (reassess after 04/09)",
        "note": "regime flipped bearish on 31/08 (close < SMA200, SMA50 < SMA200)"
    },
    {
        "pair": "AUD/USD", "reportDate": "01/09/2026", "direction": "long", "setup": "pullback",
        "entry": 0.7010, "stop": 0.6950, "target": 0.7195, "plannedR": 3.08,
        "triggerRule": "daily close inside 0.7000-0.7019 (round + 50-day SMA) followed by a close above the previous close and the 0.7010 midpoint; skip if inside the NFP 24h window",
        "note": "zone awaited since 21/08; two-day pullback from the 0.7195 top engages it"
    },
    {
        "pair": "GBP/JPY", "reportDate": "01/09/2026", "direction": "long", "setup": "pullback",
        "entry": 215.75, "stop": 214.10, "target": 219.10, "plannedR": 2.03,
        "triggerRule": "daily close inside 215.66-215.98 (D10 low + 50-day SMA) followed by a close above the previous close",
        "note": "2.5-sigma20 floor now ~115 pips (sigma20 46): first JPY-pair setup passing the intervention gate"
    },
]
with open(LED, "w", encoding="utf-8") as f:
    json.dump(led, f, ensure_ascii=False, indent=2)
print("OK: track-record.json (2 expired: GBP/JPY +0.17R, GBP/USD -0.29R; 3 new watching)")

print("\nDONE: run verify_all.py next.")
