#!/usr/bin/env python3
"""19/08/2026 daily report build. Data basis: Frankfurter/ECB, 523 sessions
01/08/2024-19/08/2026 (compute_indicators.py run of 19/08/2026).
No verdict/bias changes vs 18/08 (EUR/USD sell-pullback unchanged; 5x WAIT).
UK CPI (19/08 07:00) passed — GBP event window clear; JPY intervention window
still active until ~03/09. Ledger: no resolutions (both positions between levels;
EUR/USD watching not armed)."""
import json, re, sys, os

DOCS = r"C:/Projetos/forex-report/docs"
IDX = DOCS + "/index.html"
TS = "19/08/2026 20:50 UTC"
OLD_TS = "18/08/2026 20:45 UTC"
PAGE = {
    "EUR/USD": "eur-usd.html", "USD/JPY": "usd-jpy.html", "AUD/USD": "aud-usd.html",
    "GBP/USD": "gbp-usd.html", "EUR/JPY": "eur-jpy.html", "GBP/JPY": "gbp-jpy.html",
}

A = {}
A["EUR/USD"] = dict(
    quote="1.1605", bias="BAIXA", biasType="bear",
    pt=dict(
        fundamental="O EUR/USD opera em 1,1605 no fechamento diário de 19/08/2026 (referência BCE, ~14:15 CET), avançando +0,25% e fechando além da máxima de 10 pregões (1,1593) — porém contra o alinhamento de baixa (SMA50 1,1467 < SMA200 1,1626; preço sob a linha de 200 dias), o que não configura setup da estratégia: o rally agora pressiona a zona decisiva 1,1625-1,1657 (SMA200 / Fib 50%) por baixo, devolvendo o par acima da Fib 61,8% (1,1582). Macro inalterado: Fed dividido (9-3, 3,50-3,75%), CPI dos EUA 3,4%, DXY ~99,8, BCE 2,25%. Indicadores (SMA 50/200, σ20, Donchian e Fibonacci) calculados da série diária BCE/Frankfurter (523 pregões, 01/08/2024 a 19/08/2026). A zona segue o gatilho — agora ao alcance.",
        trend="Abaixo da SMA200 (1,1626) e acima da SMA50 (1,1467), com SMA50 < SMA200 — alinhamento de baixa; o rally pressionou a Fib 61,8% (1,1582) e mira a zona 1,1625-1,1657, a menos de 20 pips do fechamento.",
        support="1,1476 (Fib 78,6%), com a mínima de 9 meses em 1,1340 abaixo.",
        resistance="1,1657 (Fib 50%) em confluência com a SMA200 (1,1625) — a zona de venda; 1,1732 (Fib 38,2%) no topo.",
        priceAction="O rompimento D10 de hoje (1,1605 > 1,1593) é contra-tendência e não é setup; o gatilho válido segue o primeiro fechamento diário abaixo do anterior dentro da zona 1,1625-1,1657, retomando a queda rumo a 1,1476-1,1450 — fechamento acima de 1,1732 invalida o viés de baixa.",
        recommendation="VENDA (SHORT) NA RETRAÇÃO",
        trigger="Primeiro fechamento diário abaixo do fechamento anterior dentro da zona 1,1625-1,1657 (referência de entrada 1,1641, o meio da zona).",
        stop="1,1710 (Acima do número redondo 1,1700 e do piso de 1,5σ20 de 45 pips; invalida a SMA200) · risco sugerido ≤ 1% por operação.",
        target="1,1450 (Logo abaixo da Fib 78,6% em 1,1476).",
        rr="1:2.77", rrValue=69,
        justification="O alinhamento de baixa (SMA50 < SMA200 e preço sob a linha de 200 dias) prevalece sobre o macro de dólar pressionado, e o rally estanca exatamente na confluência Fib 50% / SMA200. Entrada vendida em 1,1641 com stop estrutural de 69 pips (≥ piso de 1,5σ20) e alvo a 191 pips entrega R/R de 1:2.77 rumo a 1,1450 — caminho limpo, sem S/R intermediária relevante.",
    ),
    en=dict(
        fundamental="EUR/USD trades at 1.1605 on the 19/08/2026 daily close (ECB reference, ~14:15 CET), up +0.25% and closing beyond the 10-day high (1.1593) — yet against the bear alignment (SMA50 1.1467 < SMA200 1.1626; price below the 200-day line), which is not a strategy setup: the rally now presses the decisive 1.1625-1.1657 zone (200-day SMA / 50% Fib) from below, putting the pair back above the 61.8% Fib (1.1582). Macro unchanged: divided Fed (9-3, 3.50-3.75%), US CPI 3.4%, DXY ~99.8, ECB 2.25%. Indicators (SMA 50/200, sigma20, Donchian, Fibonacci) computed from the ECB/Frankfurter daily series (523 sessions, 01/08/2024 to 19/08/2026). The zone remains the trigger — now within reach.",
        trend="Below the 200-day SMA (1.1626) and above the 50-day (1.1467), with SMA50 < SMA200 — bear alignment; the rally pressed the 61.8% Fib (1.1582) and targets the 1.1625-1.1657 zone, less than 20 pips from the close.",
        support="1.1476 (78.6% Fib), with the 9-month low of 1.1340 beneath.",
        resistance="1.1657 (50% Fib) in confluence with the 200-day SMA (1.1625) — the selling zone; 1.1732 (38.2% Fib) on top.",
        priceAction="Today's D10 breakout (1.1605 > 1.1593) is counter-trend and not a setup; the valid trigger remains the first daily close below the previous close inside the 1.1625-1.1657 zone, resuming the drop toward 1.1476-1.1450 — a daily close above 1.1732 invalidates the bear bias.",
        recommendation="SELL (SHORT) ON PULLBACK",
        trigger="First daily close below the previous close inside the 1.1625-1.1657 zone (entry reference 1.1641, the zone midpoint).",
        stop="1.1710 (Above the 1.1700 round number and the 1.5-sigma20 floor of 45 pips; invalidates the 200-day SMA) · suggested risk ≤ 1% per trade.",
        target="1.1450 (Just below the 78.6% Fib at 1.1476).",
        rr="1:2.77", rrValue=69,
        justification="The bear alignment (SMA50 < SMA200, price under the 200-day line) outweighs the pressured-USD macro, and the rally stalls exactly at the 50% Fib / 200-day confluence. A short from 1.1641 with a 69-pip structural stop (>= the 1.5-sigma20 floor) and a 191-pip target delivers 1:2.77 R/R toward 1.1450 — a clean path with no relevant intermediate S/R.",
    ))

A["USD/JPY"] = dict(
    quote="159.09", bias="ALTA", biasType="bull",
    pt=dict(
        fundamental="O USD/JPY opera em 159,09 no fechamento diário de 19/08/2026 (referência BCE), recuando -0,38% e devolvendo o rompimento — o fechamento voltou abaixo da Fib 38,2% (159,60) e da máxima de 10 pregões (159,70). O BoJ segue hawkish a 1,0% e o diferencial Fed-BoJ é amplo, com a estrutura de alta intacta acima da SMA200 (158,17); mas a janela de 30 dias da intervenção de início de agosto segue ativa até ~03/09, mantendo o piso de stop em 2,5σ20 (≈268 pips) — que degrada qualquer configuração a R/R <1:2. Indicadores calculados da série diária BCE/Frankfurter (523 pregões, 01/08/2024 a 19/08/2026).",
        trend="Acima da SMA200 (158,17) e abaixo da SMA50 (161,11) — alinhamento de alta; o rompimento D10 foi devolvido (fechamento 159,09 < 159,60) e a retração mira a confluência Fib 50% (158,27) / SMA200 (158,17).",
        support="158,27 (Fib 50%) / 158,17 (SMA200), com a Fib 61,8% (156,94) abaixo; a Fib 38,2% (159,60) foi perdida hoje.",
        resistance="159,60 (Fib 38,2%, perdida hoje), com a confluência SMA50 / Fib 23,6% (161,11-161,25) e a máxima de 9 meses (163,91) acima.",
        priceAction="Sem gatilho: a devolução do rompimento ainda não alcança a zona 158,17-158,27 e o piso de intervenção (2,5σ20 ≈ 268 pips) degrada qualquer entrada a R/R <1:2 — rompimento ~1:1,6, retração ~1:1. Reavaliar após ~03/09 ou em retração à zona com σ20 comprimida.",
        recommendation="AGUARDAR OUTRO GATILHO",
        trigger="Nenhum — piso de intervenção (2,5σ20 ≈ 268 pips) ativo até ~03/09 degrada todo R/R (<1:2). Reavaliar quando a janela expirar ou após retração à zona 158,17-158,27 com compressão de σ20.",
        stop="N/A (sem operação).",
        target="N/A (sem operação).",
        rr="N/A", rrValue=0,
        justification="A devolução do rompimento confirma a leitura de ontem: com o piso de intervenção ativo, nem perseguição nem retração fecham 1:2. O alinhamento de alta acima da SMA200 segue — aguardar a janela envelhecer (~03/09) ou uma retração mais profunda.",
    ),
    en=dict(
        fundamental="USD/JPY trades at 159.09 on the 19/08/2026 daily close (ECB reference), easing -0.38% and handing back the breakout — the close fell back below the 38.2% Fib (159.60) and the 10-day high (159.70). The BoJ remains hawkish at 1.00% and the Fed-BoJ differential is wide, with the bull structure intact above the 200-day SMA (158.17); but the 30-day intervention window stays active until ~Sep 3, holding the stop floor at 2.5-sigma20 (~=268 pips) — which degrades any configuration below 1:2 R/R. Indicators computed from the ECB/Frankfurter daily series (523 sessions, 01/08/2024 to 19/08/2026).",
        trend="Above the 200-day SMA (158.17) and below the 50-day (161.11) — bull alignment; the D10 breakout was handed back (close 159.09 < 159.60) and the pullback targets the 50% Fib (158.27) / 200-day SMA (158.17) confluence.",
        support="158.27 (50% Fib) / 158.17 (200-day SMA), with the 61.8% Fib (156.94) beneath; the 38.2% Fib (159.60) was lost today.",
        resistance="159.60 (38.2% Fib, lost today), with the 50-day SMA / 23.6% Fib confluence (161.11-161.25) and the 9-month high (163.91) above.",
        priceAction="No trigger: the handed-back breakout has not reached the 158.17-158.27 zone and the intervention floor (2.5-sigma20 ~= 268 pips) degrades any entry below 1:2 R/R — breakout ~1:1.6, pullback ~1:1. Reassess after ~Sep 3 or on a pullback to the zone with compressed sigma20.",
        recommendation="WAIT FOR ANOTHER TRIGGER",
        trigger="None — intervention floor (2.5-sigma20 ~= 268 pips) active until ~Sep 3 degrades every R/R (<1:2). Reassess when the window expires or after a pullback to the 158.17-158.27 zone with sigma20 compression.",
        stop="N/A (no trade).",
        target="N/A (no trade).",
        rr="N/A", rrValue=0,
        justification="The handed-back breakout confirms yesterday's read: with the intervention floor active, neither chase nor pullback closes 1:2. The bull alignment above the 200-day remains — wait for the window to age out (~Sep 3) or a deeper pullback.",
    ))

A["AUD/USD"] = dict(
    quote="0.7076", bias="ALTA", biasType="bull",
    pt=dict(
        fundamental="O AUD/USD opera em 0,7076 no fechamento diário de 19/08/2026 (referência BCE), recuando -0,50% e testando a Fib 23,6% (0,7065) — fechou 11 pips acima dela, aproximando a retração da zona de compra 0,6990-0,7065 pela primeira vez desde o rompimento. RBA a 4,35% (11/08), WTI ~US$ 82 e o quadro de dólar pressionado seguem; alinhamento de alta acima das SMA50 (0,6993) e SMA200 (0,6933) dentro do avanço de 0,6445 a 0,7257. Indicadores calculados da série diária BCE/Frankfurter (523 pregões, 01/08/2024 a 19/08/2026).",
        trend="Acima das SMA50 (0,6993) e SMA200 (0,6933) — alinhamento de alta; a retração alcançou a vizinhança da Fib 23,6% (0,7065), com a zona de compra 0,6990-0,7065 logo abaixo e a máxima de 9 meses (0,7257) acima.",
        support="0,7065 (Fib 23,6%, segurando por 11 pips), com a SMA50 (0,6993) abaixo.",
        resistance="0,7257 (máxima de 9 meses do avanço de 0,6445), com o número redondo 0,7200 no caminho.",
        priceAction="Sem gatilho ainda: a retração aproxima a zona 0,6990-0,7065 sem alcançá-la por fechamento. Gatilhos: fechamento dentro da zona (SMA50 / Fib 23,6%, R/R ≥ 3 rumo a 0,7150) ou fechamento decisivo acima de 0,7257, abrindo ar limpo.",
        recommendation="AGUARDAR OUTRO GATILHO",
        trigger="Nenhum — aguardar fechamento dentro da zona 0,6990-0,7065 (SMA50 / Fib 23,6%) ou fechamento decisivo acima de 0,7257.",
        stop="N/A (sem operação).",
        target="N/A (sem operação).",
        rr="N/A", rrValue=0,
        justification="A retração finalmente aproxima a zona de compra — a paciência do gate está prestes a ser recompensada ou invalidada: fechamento na zona arma o longo com R/R ≥ 3; se a zona falhar e o par cair sob a SMA50, o alinhamento enfraquece. Sem operação até um dos dois.",
    ),
    en=dict(
        fundamental="AUD/USD trades at 0.7076 on the 19/08/2026 daily close (ECB reference), easing -0.50% and testing the 23.6% Fib (0.7065) — it closed 11 pips above it, bringing the pullback within reach of the 0.6990-0.7065 buying zone for the first time since the breakout. RBA at 4.35% (Aug 11), WTI ~$82 and the pressured-dollar backdrop persist; bull alignment above the 50-day (0.6993) and 200-day (0.6933) SMAs within the 0.6445 to 0.7257 advance. Indicators computed from the ECB/Frankfurter daily series (523 sessions, 01/08/2024 to 19/08/2026).",
        trend="Above the 50-day (0.6993) and 200-day (0.6933) SMAs — bull alignment; the pullback reached the 23.6% Fib (0.7065) neighborhood, with the 0.6990-0.7065 buying zone just beneath and the 9-month high (0.7257) above.",
        support="0.7065 (23.6% Fib, holding by 11 pips), with the 50-day SMA (0.6993) beneath.",
        resistance="0.7257 (9-month high of the 0.6445 advance), with the 0.7200 round number in the path.",
        priceAction="No trigger yet: the pullback nears the 0.6990-0.7065 zone without reaching it on a close. Triggers: a close inside the zone (50-day SMA / 23.6% Fib, R/R >= 3 toward 0.7150) or a decisive close above 0.7257 opening clean air.",
        recommendation="WAIT FOR ANOTHER TRIGGER",
        trigger="None — wait for a close inside the 0.6990-0.7065 zone (50-day SMA / 23.6% Fib) or a decisive close above 0.7257.",
        stop="N/A (no trade).",
        target="N/A (no trade).",
        rr="N/A", rrValue=0,
        justification="The pullback finally nears the buying zone — the gate's patience is about to be rewarded or invalidated: a close in the zone arms the long at R/R >= 3; if the zone fails and the pair drops under the 50-day SMA, the alignment weakens. No trade until one of the two.",
    ))

A["GBP/USD"] = dict(
    quote="1.3556", bias="NEUTRO", biasType="neutral",
    pt=dict(
        fundamental="O GBP/USD opera em 1,3556 no fechamento diário de 19/08/2026 (referência BCE), avançando +0,22% e parando a 0,3 pip do gatilho: o fechamento ficou sob a máxima de 10 pregões (1,3559), mantendo o regime misto (preço acima das duas médias, SMA50 1,3379 ainda sob a SMA200 1,3411). O CPI do Reino Unido foi divulgado hoje (07:00 London) — a janela de eventos está livre novamente. O ticket de 17/08 segue aberto e próximo do ponto de entrada (stop 1,3490 / alvo 1,3800). Indicadores calculados da série diária BCE/Frankfurter (523 pregões, 01/08/2024 a 19/08/2026).",
        trend="Preço acima das SMA50 (1,3379) e SMA200 (1,3411), com SMA50 ainda abaixo da SMA200 — regime misto: o fechamento de 1,3556 ficou 0,3 pip sob o gatilho de resolução (máxima de 10 dias, 1,3559); a barra de hoje decide o lado.",
        support="1,3500 (número redondo), com a Fib 50% (1,3439) abaixo.",
        resistance="1,3559 (máxima de 10 dias / gatilho de resolução), com a Fib 23,6% (1,3639) e a máxima de 9 meses (1,3817) acima.",
        priceAction="Sem nova entrada: o regime segue misto — um fechamento acima de 1,3559 resolve para alta (abrindo o rompimento D10) e devolve o viés comprado; a perda de 1,3500 pressiona a Fib 50% (1,3439). A posição do ticket de 17/08 segue gerenciada (stop 1,3490 / alvo 1,3800).",
        recommendation="AGUARDAR OUTRO GATILHO",
        trigger="Nenhum — regime misto a 0,3 pip da resolução: fechamento acima de 1,3559 (máxima de 10 dias) resolve para alta; perda de 1,3500 devolve a pressão baixista. Posição existente segue com stop 1,3490 / alvo 1,3800.",
        stop="N/A (sem nova operação).",
        target="N/A (sem nova operação).",
        rr="N/A", rrValue=0,
        justification="O CPI passou e a janela de eventos está livre, mas o fechamento de hoje deixou o regime misto intacto — por 0,3 pip. A disciplina exige o fechamento de resolução acima de 1,3559 (ou a rejeição sob 1,3500) antes de qualquer nova entrada; a posição de 17/08 roda com stop/alvo estruturais.",
    ),
    en=dict(
        fundamental="GBP/USD trades at 1.3556 on the 19/08/2026 daily close (ECB reference), up +0.22% and stopping 0.3 of a pip shy of the trigger: the close held below the 10-day high (1.3559), keeping the regime mixed (price above both SMAs but the 50-day 1.3379 still below the 200-day 1.3411). UK CPI was released this morning (07:00 London) — the event window is clear again. The Aug 17 ticket stays open near its entry (stop 1.3490 / target 1.3800). Indicators computed from the ECB/Frankfurter daily series (523 sessions, 01/08/2024 to 19/08/2026).",
        trend="Price above the 50-day (1.3379) and 200-day (1.3411) SMAs, with the 50-day still below the 200-day — mixed regime: the 1.3556 close sat 0.3 of a pip under the resolution trigger (10-day high, 1.3559); tomorrow's bar decides the side.",
        support="1.3500 (round number), with the 50% Fib (1.3439) beneath.",
        resistance="1.3559 (10-day high / resolution trigger), with the 23.6% Fib (1.3639) and the 9-month high (1.3817) above.",
        priceAction="No new entry: the regime stays mixed — a close above 1.3559 resolves bullish (opening the D10 breakout) and restores the long bias; losing 1.3500 pressures the 50% Fib (1.3439). The Aug 17 position stays managed (stop 1.3490 / target 1.3800).",
        recommendation="WAIT FOR ANOTHER TRIGGER",
        trigger="None — mixed regime 0.3 of a pip from resolution: a close above 1.3559 (10-day high) resolves bullish; losing 1.3500 hands back the downside pressure. The existing position keeps stop 1.3490 / target 1.3800.",
        stop="N/A (no new trade).",
        target="N/A (no new trade).",
        rr="N/A", rrValue=0,
        justification="CPI has passed and the event window is clear, but today's close kept the regime mixed — by 0.3 of a pip. Discipline demands the resolution close above 1.3559 (or a rejection below 1.3500) before any new entry; the Aug 17 position runs with its structural stop/target.",
    ))

A["EUR/JPY"] = dict(
    quote="184.62", bias="ALTA", biasType="bull",
    pt=dict(
        fundamental="O EUR/JPY opera em 184,62 no fechamento diário de 19/08/2026 (referência BCE), recuando -0,13% e devolvendo a SMA50 (184,73) por margem estreita — a sequência de rompimentos D10 pausou sob a máxima de 20 dias (186,99). O carry BCE (2,25%)-BoJ (1,0%) segue amplo e o alinhamento de alta acima da SMA200 (183,85) está intacto; mas a janela de intervenção (até ~03/09) mantém o piso 2,5σ20 (≈272 pips) contra um teto de máxima de 9 meses a ~310 pips — R/R ~1:1. Indicadores calculados da série diária BCE/Frankfurter (523 pregões, 01/08/2024 a 19/08/2026).",
        trend="Acima da SMA200 (183,85) e sob a SMA50 (184,73) por margem estreita — alinhamento de alta (SMA50 > SMA200); a pausa sob a máxima de 20 dias (186,99) mantém a estrutura, com a máxima de 9 meses (187,73) no topo.",
        support="183,85 (SMA200) / 183,46 (Fib 50%), com a Fib 61,8% (182,45) abaixo.",
        resistance="187,73 (máxima de 9 meses), com a máxima de 20 dias (186,99) e a SMA50 (184,73) no caminho.",
        priceAction="Sem entrada — o piso de intervenção (2,5σ20 ≈ 272 pips) contra o teto da máxima de 9 meses (187,73) segue degradando qualquer configuração a ~1:1. Aguardar a expiração da janela (~03/09) ou retração à zona 182,45-183,46 para comprimir o risco.",
        recommendation="AGUARDAR OUTRO GATILHO",
        trigger="Nenhum — piso de intervenção (≈272 pips) versus teto de 187,73 trava o R/R em ~1:1. Reavaliar após ~03/09 ou em retração à zona 182,45-183,46 (Fib 61,8% / 50%).",
        stop="N/A (sem operação).",
        target="N/A (sem operação).",
        rr="N/A", rrValue=0,
        justification="A pausa sob a SMA50 não altera a leitura: alinhamento de alta pleno, mas a regra de intervenção exige stop ≥ 2,5σ20 enquanto o alvo mais distante (187,73) paga ~1:1. Sem operação até a janela envelhecer ou o preço recuar para comprimir o risco.",
    ),
    en=dict(
        fundamental="EUR/JPY trades at 184.62 on the 19/08/2026 daily close (ECB reference), easing -0.13% and handing back the 50-day SMA (184.73) by a narrow margin — the D10 breakout sequence paused under the 20-day high (186.99). The ECB (2.25%)-BoJ (1.00%) carry remains wide and the bull alignment above the 200-day SMA (183.85) is intact; but the intervention window (until ~Sep 3) keeps the 2.5-sigma20 floor (~=272 pips) against a 9-month-high cap ~310 pips away — R/R ~1:1. Indicators computed from the ECB/Frankfurter daily series (523 sessions, 01/08/2024 to 19/08/2026).",
        trend="Above the 200-day SMA (183.85) and below the 50-day (184.73) by a narrow margin — bull alignment (SMA50 > SMA200); the pause under the 20-day high (186.99) keeps the structure, with the 9-month high (187.73) on top.",
        support="183.85 (200-day SMA) / 183.46 (50% Fib), with the 61.8% Fib (182.45) beneath.",
        resistance="187.73 (9-month high), with the 20-day high (186.99) and the 50-day SMA (184.73) in the path.",
        priceAction="No entry — the intervention floor (2.5-sigma20 ~= 272 pips) against the 9-month-high cap (187.73) still degrades any configuration to ~1:1. Wait for the window to expire (~Sep 3) or a pullback to the 182.45-183.46 zone to compress risk.",
        recommendation="WAIT FOR ANOTHER TRIGGER",
        trigger="None — intervention floor (~=272 pips) versus the 187.73 cap locks R/R at ~1:1. Reassess after ~Sep 3 or on a pullback to the 182.45-183.46 zone (61.8% / 50% Fibs).",
        stop="N/A (no trade).",
        target="N/A (no trade).",
        rr="N/A", rrValue=0,
        justification="The pause under the 50-day SMA changes nothing: full bull alignment, but the intervention rule demands a stop >= 2.5-sigma20 while the farthest target (187.73) pays ~1:1. No trade until the window ages out or price pulls back to compress risk.",
    ))

A["GBP/JPY"] = dict(
    quote="215.66", bias="ALTA", biasType="bull",
    pt=dict(
        fundamental="O GBP/JPY opera em 215,66 no fechamento diário de 19/08/2026 (referência BCE), recuando -0,16% e pausando sobre a SMA50 (215,54) — a posição do ticket de 14/08 (entrada 215,90, stop 213,90, alvo 219,00) segue aberta, levemente abaixo da entrada. O CPI do Reino Unido foi divulgado hoje e a janela de eventos está livre; mas o piso de intervenção 2,5σ20 (≈314 pips) segue ativo até ~03/09 e mantém qualquer nova entrada em R/R <1 — a máxima de 9 meses (219,14) está a apenas ~1,6%. Indicadores calculados da série diária BCE/Frankfurter (523 pregões, 01/08/2024 a 19/08/2026).",
        trend="Acima das SMA50 (215,54) e SMA200 (212,11) — alinhamento de alta; a pausa sobre a SMA50 mantém a estrutura, com a máxima de 20 dias (218,27) e a de 9 meses (219,14) acima.",
        support="215,24 (Fib 23,6%), com o redondo 213,00 e a Fib 38,2% (212,82) abaixo.",
        resistance="219,14 (máxima de 9 meses), com a máxima de 20 dias (218,27) no caminho.",
        priceAction="Sem nova entrada — o piso de intervenção (≈314 pips) versus o teto de 219,14 segue bloqueando adições; a posição do ticket de 14/08 segue gerenciada (stop 213,90 / alvo 219,00), com o alvo a ~1,6%.",
        recommendation="AGUARDAR OUTRO GATILHO",
        trigger="Nenhum — piso de intervenção ativo até ~03/09 degrada qualquer R/R novo. A posição existente segue com stop 213,90 / alvo 219,00; adição reavaliada após a janela.",
        stop="N/A (sem nova operação).",
        target="N/A (sem nova operação).",
        rr="N/A", rrValue=0,
        justification="A estrutura segue de alta e o CPI já passou, mas o piso de intervenção mantém qualquer adição abaixo de 1:2 — gerenciar o ticket existente rumo a 219,00 e reavaliar adições após ~03/09.",
    ),
    en=dict(
        fundamental="GBP/JPY trades at 215.66 on the 19/08/2026 daily close (ECB reference), easing -0.16% and pausing on the 50-day SMA (215.54) — the Aug 14 ticket's position (entry 215.90, stop 213.90, target 219.00) stays open, slightly below entry. UK CPI was released this morning and the event window is clear; but the 2.5-sigma20 intervention floor (~=314 pips) remains active until ~Sep 3 and keeps any new entry below R/R 1 — the 9-month high (219.14) is only ~1.6% away. Indicators computed from the ECB/Frankfurter daily series (523 sessions, 01/08/2024 to 19/08/2026).",
        trend="Above the 50-day (215.54) and 200-day (212.11) SMAs — bull alignment; the pause on the 50-day keeps the structure, with the 20-day high (218.27) and the 9-month high (219.14) above.",
        support="215.24 (23.6% Fib), with the 213.00 round number and the 38.2% Fib (212.82) beneath.",
        resistance="219.14 (9-month high), with the 20-day high (218.27) in the path.",
        priceAction="No new entry — the intervention floor (~=314 pips) versus the 219.14 cap still blocks adds; the Aug 14 ticket stays managed (stop 213.90 / target 219.00), with the target ~1.6% away.",
        recommendation="WAIT FOR ANOTHER TRIGGER",
        trigger="None — intervention floor active until ~Sep 3 degrades any new R/R. The existing position keeps stop 213.90 / target 219.00; adds reassessed after the window.",
        stop="N/A (no new trade).",
        target="N/A (no new trade).",
        rr="N/A", rrValue=0,
        justification="The structure stays bullish and CPI has passed, but the intervention floor keeps any add below 1:2 — manage the existing ticket toward 219.00 and reassess adds after ~Sep 3.",
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
            "EUR/USD": "-0.15%",
            "USD/JPY": "+0.30%",
            "AUD/USD": "-0.19%",
            "GBP/USD": "-0.25%",
            "EUR/JPY": "+0.15%",
            "GBP/JPY": "+0.05%"
        };'''
new_changes = '''        const dailyChanges = {
            "EUR/USD": "+0.25%",
            "USD/JPY": "-0.38%",
            "AUD/USD": "-0.50%",
            "GBP/USD": "+0.22%",
            "EUR/JPY": "-0.13%",
            "GBP/JPY": "-0.16%"
        };'''
idx = rep(idx, old_changes, new_changes, "ticker")
old_be = 'dataBasis: "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 522 daily sessions (01/08/2024–18/08/2026).",'
new_be = 'dataBasis: "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 523 daily sessions (01/08/2024–19/08/2026).",'
old_bp = 'dataBasis: "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, sigma20 e Donchian calculados · 522 pregões (01/08/2024 a 18/08/2026).",'
new_bp = 'dataBasis: "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, sigma20 e Donchian calculados · 523 pregões (01/08/2024 a 19/08/2026).",'
idx = rep(idx, old_be, new_be, "dataBasis EN")
idx = rep(idx, old_bp, new_bp, "dataBasis PT")

with open(IDX, "w", encoding="utf-8") as f:
    f.write(idx)
print("OK: index.html")

# ---------------- static pages ----------------
GAUGE = {"EUR/USD": 71, "USD/JPY": 62, "AUD/USD": 6, "GBP/USD": 95, "EUR/JPY": 20, "GBP/JPY": 11}
OLD_GAUGE = {"EUR/USD": 55, "USD/JPY": 7, "AUD/USD": 24, "GBP/USD": 44, "EUR/JPY": 27, "GBP/JPY": 20}

BLUF = {
 "USD/JPY": ('<span class="lang-en"><span class="bluf-action wait">WAIT</span> — breakout handed back; floor until ~03/09</span><span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — rompimento devolvido; piso até ~03/09</span>',
             '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — D10 breakout; 2.5σ20 floor blocks R/R</span><span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — rompimento D10; piso 2,5σ20 bloqueia o R/R</span>'),
 "AUD/USD": ('<span class="lang-en"><span class="bluf-action wait">WAIT</span> — pullback nearing the 0.6990-0.7065 zone</span><span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — retração aproximando da zona 0.6990-0.7065</span>',
             '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — 9-month high caps R/R; awaiting pullback zone</span><span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — máxima de 9 meses limita o R/R; aguardando zona de retração</span>'),
 "GBP/USD": ('<span class="lang-en"><span class="bluf-action wait">WAIT</span> — close 1.3556 just under the 1.3559 trigger; CPI passed</span><span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — fechamento 1.3556 sob o gatilho 1.3559; CPI passou</span>',
             '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — UK CPI (19/08) blocks entry; position from 1.3559 open</span><span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — CPI do RU (19/08) bloqueia entrada; posição de 1.3559 aberta</span>'),
 "GBP/JPY": ('<span class="lang-en"><span class="bluf-action wait">WAIT</span> — floor until ~03/09; position open from 215.9</span><span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — piso até ~03/09; posição aberta em 215.9</span>',
             '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — CPI (19/08) + floor block adds; position open from 215.9</span><span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — CPI (19/08) + piso bloqueiam adições; posição aberta em 215.9</span>'),
}

SVG = {
 "EUR/USD": [],
 "USD/JPY": [],
 "AUD/USD": [],
 "GBP/USD": [],
 "EUR/JPY": [("183.5", "183.5")],  # placeholder no-op; real swap below
 "GBP/JPY": [],
}
SVG["EUR/JPY"] = []  # 183.1 -> 183.5 handled inline below (single distinct old value)
PRICE = {"EUR/USD": ("1.1576", "1.1605"), "USD/JPY": ("159.7", "159.1"), "AUD/USD": ("0.7111", "0.7076"),
         "GBP/USD": ("1.3526", "1.3556"), "EUR/JPY": ("184.9", "184.6"), "GBP/JPY": ("216.0", "215.7")}

for pair, fname in PAGE.items():
    path = f"{DOCS}/{fname}"
    with open(path, encoding="utf-8") as f:
        h = f.read()
    od, nd = old_data[pair], A[pair]
    # 1) BLUF
    if pair in BLUF:
        new_bluf, old_bluf = BLUF[pair]
        h = rep(h, old_bluf, new_bluf, f"{fname} BLUF")
    # 2) fields
    for lang in ("pt", "en"):
        for fl in ["fundamental", "trend", "support", "resistance", "priceAction",
                   "recommendation", "trigger", "stop", "target", "justification"]:
            oldv, newv = od[lang][fl], nd[lang][fl]
            if oldv == newv:
                continue
            if fl in ("stop", "target") and od[lang]["stop"] == od[lang]["target"] and nd[lang]["stop"] == nd[lang]["target"]:
                continue  # handled jointly below
            h = rep(h, oldv, newv, f"{fname} {lang}.{fl}", 1)
        if od[lang]["stop"] == od[lang]["target"] and nd[lang]["stop"] == nd[lang]["target"] and od[lang]["stop"] != nd[lang]["stop"]:
            h = rep(h, od[lang]["stop"], nd[lang]["stop"], f"{fname} {lang} stop+target", 2)
    # 3) rr (all pairs unchanged N/A or 1:2.77 — no-op)
    # 4) quote strong
    h = rep(h, f'<strong>{od["quote"]}</strong>', f'<strong>{nd["quote"]}</strong>', f"{fname} quote strong")
    # 5) price markers
    po, pn = PRICE[pair]
    h = rep(h, f'Price {po}</text>', f'Price {pn}</text>', f"{fname} price mark")
    h = rep(h, f'Preço {po}</text>', f'Preço {pn}</text>', f"{fname} preco mark")
    # 6) gauge
    h = rep(h, f'left: {OLD_GAUGE[pair]}%', f'left: {GAUGE[pair]}%', f"{fname} gauge", 2)
    # 7) svg ticks
    for oldv, newv in SVG[pair]:
        h = rep(h, f'text-anchor="middle">{oldv}</text>', f'text-anchor="middle">{newv}</text>', f"{fname} svg {oldv}", 2)
    with open(path, "w", encoding="utf-8") as f:
        f.write(h)
    print(f"OK: {fname} ({pair})")

# pages' data-basis lines
for fname in PAGE.values():
    p = f"{DOCS}/{fname}"
    with open(p, encoding="utf-8") as f:
        h = f.read()
    oen = "ECB/Frankfurter reference rates · SMA50/200, sigma20 &amp; Donchian computed · 522 daily sessions (01/08/2024–18/08/2026)."
    nen = "ECB/Frankfurter reference rates · SMA50/200, sigma20 &amp; Donchian computed · 523 daily sessions (01/08/2024–19/08/2026)."
    opt = "taxas de referência BCE/Frankfurter · SMA50/200, sigma20 e Donchian calculados · 522 pregões (01/08/2024 a 18/08/2026)."
    npt = "taxas de referência BCE/Frankfurter · SMA50/200, sigma20 e Donchian calculados · 523 pregões (01/08/2024 a 19/08/2026)."
    h = rep(h, oen, nen, f"{fname} basis EN")
    h = rep(h, opt, npt, f"{fname} basis PT")
    with open(p, "w", encoding="utf-8") as f:
        f.write(h)
print("OK: 6 pages data-basis")

# eur-jpy svg tick: Fib 50% 183.1 -> 183.5 (2x)
p = f"{DOCS}/eur-jpy.html"
with open(p, encoding="utf-8") as f:
    h = f.read()
h = rep(h, 'text-anchor="middle">183.1</text>', 'text-anchor="middle">183.5</text>', "eur-jpy svg 183.1", 2)
with open(p, "w", encoding="utf-8") as f:
    f.write(h)
print("OK: eur-jpy svg tick")
print("\nDONE: run verify_all.py next.")
