#!/usr/bin/env python3
"""18/08/2026 daily report build. Data basis: Frankfurter/ECB, 522 sessions
01/08/2024-18/08/2026 (compute_indicators.py run of 18/08/2026).
Key calls: EUR/USD short-pullback zone unchanged (2-day rejection under it);
USD/JPY D10 breakout but 2.5-sigma20 intervention floor caps R/R; GBP/USD gave
the breakout back (close 1.3526 < 1.3559 -> MIXED -> NEUTRO) and UK CPI 19/08
(event filter) blocks new GBP entries; EUR/JPY, GBP/JPY still intervention-capped.
Old field values are read from the live (17/08) forexData; count-asserted."""
import json, re, sys, os

DOCS = r"C:/Projetos/forex-report/docs"
IDX = DOCS + "/index.html"
TS = "18/08/2026 20:45 UTC"
OLD_TS = "17/08/2026 21:10 UTC"
PAGE = {
    "EUR/USD": "eur-usd.html", "USD/JPY": "usd-jpy.html", "AUD/USD": "aud-usd.html",
    "GBP/USD": "gbp-usd.html", "EUR/JPY": "eur-jpy.html", "GBP/JPY": "gbp-jpy.html",
}

A = {}
A["EUR/USD"] = dict(
    quote="1.1576", bias="BAIXA", biasType="bear",
    pt=dict(
        fundamental="O EUR/USD opera em 1,1576 no fechamento diário de 18/08/2026 (referência BCE, ~14:15 CET), recuando -0,15% e fechando de volta abaixo da Fib 61,8% (1,1582) — a recuperação de dois dias estacou antes da zona decisiva 1,1625-1,1657 (SMA200 / Fib 50%), sem sequer tocá-la por fechamento. O quadro macro segue o de 17/08: manutenção dividida do Fed em 9-3 a 3,50-3,75% (29/07), CPI dos EUA de julho a +3,4% a.a. (12/08, núcleo 2,5%) e DXY ~99,8 pressionam o dólar; o BCE a 2,25% limita o downside do euro. Alinhamento de baixa intacto (SMA50 1,1466 < SMA200 1,1625; preço sob a linha de 200 dias) dentro do downtrend de 9 meses (1,1974 a 1,1340). Indicadores (SMA 50/200, σ20, Donchian e Fibonacci) calculados da série diária BCE/Frankfurter (522 pregões, 01/08/2024 a 18/08/2026).",
        trend="Abaixo da SMA200 (1,1625) e acima da SMA50 (1,1466), com SMA50 < SMA200 — alinhamento de baixa; o rally parou sob a zona 1,1625-1,1657 e o fechamento de hoje devolveu o par abaixo da Fib 61,8% (1,1582).",
        support="1,1476 (Fib 78,6%), com a mínima de 9 meses em 1,1340 abaixo.",
        resistance="1,1657 (Fib 50%) em confluência com a SMA200 (1,1625) — a zona de venda; 1,1732 (Fib 38,2%) no topo.",
        priceAction="A rejeição de dois dias sob a zona 1,1625-1,1657 — sem fechamento dentro dela — reforça a oferta acima: o gatilho segue o primeiro fechamento diário abaixo do anterior dentro da zona, retomando a queda rumo a 1,1476-1,1450; fechamento acima de 1,1732 invalida o viés de baixa.",
        recommendation="VENDA (SHORT) NA RETRAÇÃO",
        trigger="Primeiro fechamento diário abaixo do fechamento anterior dentro da zona 1,1625-1,1657 (referência de entrada 1,1641, o meio da zona).",
        stop="1,1710 (Acima do número redondo 1,1700 e do piso de 1,5σ20 de 45 pips; invalida a SMA200) · risco sugerido ≤ 1% por operação.",
        target="1,1450 (Logo abaixo da Fib 78,6% em 1,1476).",
        rr="1:2.77", rrValue=69,
        justification="O alinhamento de baixa (SMA50 < SMA200 e preço sob a linha de 200 dias) prevalece sobre o macro de dólar pressionado, e o rally estaca exatamente na confluência Fib 50% / SMA200. Entrada vendida em 1,1641 com stop estrutural de 69 pips (≥ piso de 1,5σ20) e alvo a 191 pips entrega R/R de 1:2.77 rumo a 1,1450 — caminho limpo, sem S/R intermediária relevante.",
    ),
    en=dict(
        fundamental="EUR/USD trades at 1.1576 on the 18/08/2026 daily close (ECB reference, ~14:15 CET), easing -0.15% and closing back below the 61.8% Fib (1.1582) — the two-day recovery stalled before the decisive 1.1625-1.1657 zone (200-day SMA / 50% Fib) without even touching it on a close. The macro backdrop carries over: the Fed's divided 9-3 hold at 3.50-3.75% (Jul 29), July US CPI at +3.4% YoY (Aug 12, core 2.5%) and DXY ~99.8 pressure the dollar; the ECB at 2.25% caps the euro's downside. Bear alignment intact (SMA50 1.1466 < SMA200 1.1625; price below the 200-day line) inside the 9-month 1.1974 to 1.1340 downtrend. Indicators (SMA 50/200, sigma20, Donchian, Fibonacci) computed from the ECB/Frankfurter daily series (522 sessions, 01/08/2024 to 18/08/2026).",
        trend="Below the 200-day SMA (1.1625) and above the 50-day (1.1466), with SMA50 < SMA200 — bear alignment; the rally stalled under the 1.1625-1.1657 zone and today's close handed the pair back below the 61.8% Fib (1.1582).",
        support="1.1476 (78.6% Fib), with the 9-month low of 1.1340 beneath.",
        resistance="1.1657 (50% Fib) in confluence with the 200-day SMA (1.1625) — the selling zone; 1.1732 (38.2% Fib) on top.",
        priceAction="The two-day rejection under the 1.1625-1.1657 zone — with no close inside it — reinforces the supply above: the trigger remains the first daily close below the previous close inside the zone, resuming the drop toward 1.1476-1.1450; a daily close above 1.1732 invalidates the bear bias.",
        recommendation="SELL (SHORT) ON PULLBACK",
        trigger="First daily close below the previous close inside the 1.1625-1.1657 zone (entry reference 1.1641, the zone midpoint).",
        stop="1.1710 (Above the 1.1700 round number and the 1.5-sigma20 floor of 45 pips; invalidates the 200-day SMA) · suggested risk ≤ 1% per trade.",
        target="1.1450 (Just below the 78.6% Fib at 1.1476).",
        rr="1:2.77", rrValue=69,
        justification="The bear alignment (SMA50 < SMA200, price under the 200-day line) outweighs the pressured-USD macro, and the rally stalls exactly at the 50% Fib / 200-day confluence. A short from 1.1641 with a 69-pip structural stop (>= the 1.5-sigma20 floor) and a 191-pip target delivers 1:2.77 R/R toward 1.1450 — a clean path with no relevant intermediate S/R.",
    ))

A["USD/JPY"] = dict(
    quote="159.70", bias="ALTA", biasType="bull",
    pt=dict(
        fundamental="O USD/JPY opera em 159,70 no fechamento diário de 18/08/2026 (referência BCE), avançando +0,30% e fechando além da máxima de 10 pregões (159,33) — rompimento Donchian-10 confirmado por fechamento, com a Fib 38,2% (159,60) recém-recuperada. O BoJ segue hawkish a 1,0% (31/07, 8-1, alta sinalizada) e o diferencial Fed (3,50-3,75%)-BoJ domina; a estrutura é de alta acima da SMA200 (158,14). Mas a janela de 30 dias da intervenção conjunta de início de agosto segue ativa até ~03/09 — mantendo o piso de stop em 2,5σ20 (≈269 pips), que degrada o R/R do rompimento a ~1:1,6 mesmo com alvo na máxima de 163,91. Indicadores calculados da série diária BCE/Frankfurter (522 pregões, 01/08/2024 a 18/08/2026).",
        trend="Acima da SMA200 (158,14) e abaixo da SMA50 (161,13) — alinhamento de alta; rompimento D10 hoje (159,70 > 159,33) acima da Fib 38,2% (159,60), mirando a confluência SMA50 / Fib 23,6% (161,13-161,25).",
        support="159,60 (Fib 38,2% recém-recuperada), com a confluência Fib 50% (158,27) / SMA200 (158,14) abaixo.",
        resistance="161,10 (confluência SMA50 161,13 / Fib 23,6% 161,25), com a máxima de 9 meses (163,91) no topo.",
        priceAction="Rompimento D10 confirmado, porém sem entrada: o piso de intervenção 2,5σ20 (≈269 pips) exige stop ≤ 157,00 e o melhor alvo disponível (máxima de 163,91) entrega ~1:1,6 — o gate de 1:2 falha. Reavaliar após ~03/09 ou em retração à zona 158,14-158,27.",
        recommendation="AGUARDAR OUTRO GATILHO",
        trigger="Nenhum — rompimento D10 válido (159,70 > 159,33), mas o piso de intervenção (2,5σ20 ≈ 269 pips) degrada o R/R a ~1:1,6. Reavaliar quando a janela dos 30 dias expirar (~03/09) ou após retração à zona 158,14-158,27.",
        stop="N/A (sem operação).",
        target="N/A (sem operação).",
        rr="N/A", rrValue=0,
        justification="O alinhamento de alta e o rompimento D10 são direcionalmente válidos, mas a regra de intervenção exige stop ≥ 2,5σ20 (≈269 pips): o alvo mais distante (máxima de 9 meses, 163,91) paga apenas ~1:1,6. Técnicos e disciplina de risco vencem o carry: aguardar a janela envelhecer.",
    ),
    en=dict(
        fundamental="USD/JPY trades at 159.70 on the 18/08/2026 daily close (ECB reference), up +0.30% and closing beyond the 10-day high (159.33) — a close-confirmed Donchian-10 breakout, with the 38.2% Fib (159.60) freshly reclaimed. The BoJ remains hawkish at 1.00% (Jul 31, 8-1, a hike signaled) and the Fed (3.50-3.75%)-BoJ differential dominates; structure is bullish above the 200-day SMA (158.14). But the 30-day window from the early-August joint intervention stays active until ~Sep 3 — holding the stop floor at 2.5-sigma20 (~=269 pips), which degrades the breakout's R/R to ~1:1.6 even targeting the 163.91 high. Indicators computed from the ECB/Frankfurter daily series (522 sessions, 01/08/2024 to 18/08/2026).",
        trend="Above the 200-day SMA (158.14) and below the 50-day (161.13) — bull alignment; D10 breakout today (159.70 > 159.33) above the 38.2% Fib (159.60), targeting the 50-day SMA / 23.6% Fib confluence (161.13-161.25).",
        support="159.60 (freshly-reclaimed 38.2% Fib), with the 50% Fib (158.27) / 200-day SMA (158.14) confluence beneath.",
        resistance="161.10 (50-day SMA 161.13 / 23.6% Fib 161.25 confluence), with the 9-month high (163.91) on top.",
        priceAction="D10 breakout confirmed, yet no entry: the 2.5-sigma20 intervention floor (~=269 pips) demands a stop <= 157.00 and the best available target (the 163.91 high) yields ~1:1.6 — the 1:2 gate fails. Reassess after ~Sep 3 or on a pullback to the 158.14-158.27 zone.",
        recommendation="WAIT FOR ANOTHER TRIGGER",
        trigger="None — valid D10 breakout (159.70 > 159.33), but the intervention floor (2.5-sigma20 ~= 269 pips) degrades R/R to ~1:1.6. Reassess when the 30-day window expires (~Sep 3) or after a pullback to 158.14-158.27.",
        stop="N/A (no trade).",
        target="N/A (no trade).",
        rr="N/A", rrValue=0,
        justification="The bull alignment and the D10 breakout are directionally valid, but the intervention rule demands a stop >= 2.5-sigma20 (~=269 pips): the farthest target (the 163.91 high) pays only ~1:1.6. Technicals and risk discipline beat carry: wait for the window to age out.",
    ))

A["AUD/USD"] = dict(
    quote="0.7111", bias="ALTA", biasType="bull",
    pt=dict(
        fundamental="O AUD/USD opera em 0,7111 no fechamento diário de 18/08/2026 (referência BCE), recuando -0,19% e consolidando acima da Fib 23,6% (0,7065) no dia seguinte ao rompimento D10. O RBA mantém a taxa em 4,35% (11/08, padrão de espera), o petróleo firme (WTI ~US$ 82/bbl) sustenta o australiano e o quadro de dólar pressionado segue; alinhamento de alta acima das SMA50 (0,6992) e SMA200 (0,6930) dentro do avanço de 0,6445 a 0,7257. A máxima de 9 meses (0,7257) segue a apenas ~2% — travando o R/R de qualquer perseguição. Indicadores calculados da série diária BCE/Frankfurter (522 pregões, 01/08/2024 a 18/08/2026).",
        trend="Acima das SMA50 (0,6992) e SMA200 (0,6930) — alinhamento de alta; consolidação entre a Fib 23,6% (0,7065) e a máxima de 10 dias (0,7125), com a máxima de 9 meses (0,7257) acima.",
        support="0,7065 (Fib 23,6% reconquistada), com a SMA50 (0,6992) abaixo.",
        resistance="0,7257 (máxima de 9 meses do avanço de 0,6445), com o número redondo 0,7200 no caminho.",
        priceAction="Sem gatilho: o rompimento de ontem esgota o ar até 0,7257 e a retração ainda não alcançou a zona de compra. Gatilhos: retração à zona 0,6990-0,7065 (SMA50 / Fib 23,6%, R/R ≥ 3 rumo a 0,7150) ou fechamento decisivo acima de 0,7257, abrindo ar limpo.",
        recommendation="AGUARDAR OUTRO GATILHO",
        trigger="Nenhum — aguardar retração à zona 0,6990-0,7065 (SMA50 / Fib 23,6%) ou fechamento decisivo acima de 0,7257.",
        stop="N/A (sem operação).",
        target="N/A (sem operação).",
        rr="N/A", rrValue=0,
        justification="Estrutura de alta intacta, mas os dois caminhos seguem bloqueados: a perseguição do rompimento trava na máxima de 9 meses (R/R máx ~1:1,8 com stop estrutural) e a retração não chegou à zona de compra. Sem operação — aguardar a zona ou novo ground.",
    ),
    en=dict(
        fundamental="AUD/USD trades at 0.7111 on the 18/08/2026 daily close (ECB reference), easing -0.19% and consolidating above the 23.6% Fib (0.7065) the day after the D10 breakout. The RBA holds at 4.35% (Aug 11, waiting pattern), firm oil (WTI ~$82/bbl) underpins the aussie and the pressured-dollar backdrop persists; bull alignment above the 50-day (0.6992) and 200-day (0.6930) SMAs within the 0.6445 to 0.7257 advance. The 9-month high (0.7257) sits only ~2% away — capping the R/R of any chase. Indicators computed from the ECB/Frankfurter daily series (522 sessions, 01/08/2024 to 18/08/2026).",
        trend="Above the 50-day (0.6992) and 200-day (0.6930) SMAs — bull alignment; consolidation between the 23.6% Fib (0.7065) and the 10-day high (0.7125), with the 9-month high (0.7257) above.",
        support="0.7065 (reclaimed 23.6% Fib), with the 50-day SMA (0.6992) beneath.",
        resistance="0.7257 (9-month high of the 0.6445 advance), with the 0.7200 round number in the path.",
        priceAction="No trigger: yesterday's breakout exhausts the air to 0.7257 and the pullback has not reached the buying zone. Triggers: a pullback to the 0.6990-0.7065 zone (50-day SMA / 23.6% Fib, R/R >= 3 toward 0.7150) or a decisive close above 0.7257 opening clean air.",
        recommendation="WAIT FOR ANOTHER TRIGGER",
        trigger="None — wait for a pullback to the 0.6990-0.7065 zone (50-day SMA / 23.6% Fib) or a decisive close above 0.7257.",
        stop="N/A (no trade).",
        target="N/A (no trade).",
        rr="N/A", rrValue=0,
        justification="Bull structure intact, but both paths remain blocked: chasing the breakout caps at the 9-month high (max R/R ~1:1.8 with a structural stop) and the pullback has not reached the buying zone. No trade — wait for the zone or fresh ground.",
    ))

A["GBP/USD"] = dict(
    quote="1.3526", bias="NEUTRO", biasType="neutral",
    pt=dict(
        fundamental="O GBP/USD opera em 1,3526 no fechamento diário de 18/08/2026 (referência BCE), recuando -0,25% e devolvendo o rompimento — o fechamento voltou abaixo da máxima de 10 dias (1,3559) e o regime regressou ao estado misto (preço acima das duas médias, mas SMA50 1,3376 ainda sob a SMA200 1,3408). O ticket de 17/08 segue posicionado e gerenciado (entrada de referência 1,3559, stop 1,3490, alvo 1,3800). O CPI do Reino Unido amanhã (19/08, 07:00 London) está dentro da janela de 24h do filtro de eventos: nenhuma nova entrada em pares de libra. BoE a 3,75% (6-3, 30/07) e dólar pressionado seguem como pano de fundo. Indicadores calculados da série diária BCE/Frankfurter (522 pregões, 01/08/2024 a 18/08/2026).",
        trend="Preço acima das SMA50 (1,3376) e SMA200 (1,3408), com SMA50 ainda abaixo da SMA200 — regime misto: o rompimento de 17/08 foi devolvido (fechamento 1,3526 < 1,3559) e o viés volta a AGUARDAR resolução.",
        support="1,3500 (número redondo), com a Fib 50% (1,3439) abaixo.",
        resistance="1,3559 (máxima de 10 dias / gatilho devolvido), com a Fib 23,6% (1,3639) e a máxima de 9 meses (1,3817) acima.",
        priceAction="Sem nova entrada: regime misto somado ao CPI do RU (19/08, 07:00) bloqueiam pelo filtro de eventos. A posição do ticket de 17/08 segue aberta com stop 1,3490 / alvo 1,3800; reavaliar após o evento.",
        recommendation="AGUARDAR OUTRO GATILHO",
        trigger="Nenhum — regime misto (SMA50 < SMA200) e CPI do RU amanhã (19/08, 07:00 London) dentro da janela de 24h. A posição existente segue gerenciada (stop 1,3490 / alvo 1,3800); reavaliar após o evento.",
        stop="N/A (sem nova operação).",
        target="N/A (sem nova operação).",
        rr="N/A", rrValue=0,
        justification="O fechamento de volta sob 1,3559 devolve o regime misto e o CPI do RU bloqueia novas entradas pelas próximas 24h. A posição do ticket de 17/08 permanece com stop estrutural 1,3490 e alvo 1,3800 — sem adição e sem nova entrada até o evento passar.",
    ),
    en=dict(
        fundamental="GBP/USD trades at 1.3526 on the 18/08/2026 daily close (ECB reference), easing -0.25% and handing back the breakout — the close fell back below the 10-day high (1.3559) and the regime returned to mixed (price above both SMAs but the 50-day 1.3376 still below the 200-day 1.3408). The Aug 17 ticket remains positioned and managed (entry reference 1.3559, stop 1.3490, target 1.3800). UK CPI tomorrow (Aug 19, 07:00 London) sits inside the event filter's 24h window: no new entries on sterling pairs. The BoE at 3.75% (6-3, Jul 30) and the pressured dollar remain the backdrop. Indicators computed from the ECB/Frankfurter daily series (522 sessions, 01/08/2024 to 18/08/2026).",
        trend="Price above the 50-day (1.3376) and 200-day (1.3408) SMAs, with the 50-day still below the 200-day — mixed regime: Aug 17's breakout was handed back (close 1.3526 < 1.3559) and the bias returns to WAIT for resolution.",
        support="1.3500 (round number), with the 50% Fib (1.3439) beneath.",
        resistance="1.3559 (10-day high / handed-back trigger), with the 23.6% Fib (1.3639) and the 9-month high (1.3817) above.",
        priceAction="No new entry: the mixed regime plus UK CPI (Aug 19, 07:00) block via the event filter. The Aug 17 ticket stays open with stop 1.3490 / target 1.3800; reassess after the event.",
        recommendation="WAIT FOR ANOTHER TRIGGER",
        trigger="None — mixed regime (SMA50 < SMA200) and UK CPI tomorrow (Aug 19, 07:00 London) inside the 24h window. The existing position stays managed (stop 1.3490 / target 1.3800); reassess after the event.",
        stop="N/A (no new trade).",
        target="N/A (no new trade).",
        rr="N/A", rrValue=0,
        justification="The close back below 1.3559 returns the regime to mixed and UK CPI blocks new entries for the next 24h. The Aug 17 position remains on with its structural stop 1.3490 and target 1.3800 — no adds and no new entry until the event passes.",
    ))

A["EUR/JPY"] = dict(
    quote="184.87", bias="ALTA", biasType="bull",
    pt=dict(
        fundamental="O EUR/JPY opera em 184,87 no fechamento diário de 18/08/2026 (referência BCE), subindo +0,15% — segundo fechamento além da máxima de 10 pregões, agora também acima da SMA50 (184,74): rompimento D10 confirmado em sequência, com o carry BCE (2,25%)-BoJ (1,0%) retomando. Mas a janela de 30 dias da intervenção de início de agosto segue ativa (até ~03/09), mantendo o piso de stop em 2,5σ20 (≈272 pips): um stop ≤ 181,90 contra o alvo mais distante (máxima de 9 meses, 187,73, ~310 pips) entrega ~1:1 — o gate de 1:2 falha. Indicadores calculados da série diária BCE/Frankfurter (522 pregões, 01/08/2024 a 18/08/2026).",
        trend="Acima das SMA200 (183,81) e SMA50 (184,74) — alinhamento de alta pleno; sequência de fechamentos D10 (184,87 > 184,60) mira a máxima de 20 dias (186,99) e a de 9 meses (187,73).",
        support="183,81 (SMA200) / 183,09 (Fib 50%), com a Fib 61,8% (182,00) abaixo.",
        resistance="187,73 (máxima de 9 meses), com a máxima de 20 dias (186,99) e a SMA50 (184,74) no caminho.",
        priceAction="Sem entrada — o piso de intervenção (2,5σ20 ≈ 272 pips) contra o teto da máxima de 9 meses (187,73) degrada qualquer configuração a ~1:1. Aguardar a expiração da janela (~03/09) ou retração à zona 182,00-183,09 para comprimir o risco.",
        recommendation="AGUARDAR OUTRO GATILHO",
        trigger="Nenhum — rompimento D10 em sequência, mas o piso de intervenção (≈272 pips) versus o teto de 187,73 trava o R/R em ~1:1. Reavaliar após ~03/09 ou em retração à zona 182,00-183,09 (Fib 61,8% / 50%).",
        stop="N/A (sem operação).",
        target="N/A (sem operação).",
        rr="N/A", rrValue=0,
        justification="Alinhamento de alta pleno e rompimento confirmado — mas a regra de intervenção exige stop ≥ 2,5σ20 (≈272 pips) enquanto o alvo mais distante (187,73) paga ~1:1. Sem operação até a janela envelhecer ou o preço recuar para comprimir o risco.",
    ),
    en=dict(
        fundamental="EUR/JPY trades at 184.87 on the 18/08/2026 daily close (ECB reference), up +0.15% — a second close beyond the 10-day high, now also above the 50-day SMA (184.74): a sequenced D10 breakout confirmation, with the ECB (2.25%)-BoJ (1.00%) carry resuming. But the 30-day intervention window remains active (until ~Sep 3), holding the stop floor at 2.5-sigma20 (~=272 pips): a stop <= 181.90 against the farthest target (the 9-month high, 187.73, ~310 pips) yields ~1:1 — the 1:2 gate fails. Indicators computed from the ECB/Frankfurter daily series (522 sessions, 01/08/2024 to 18/08/2026).",
        trend="Above the 200-day SMA (183.81) and the 50-day (184.74) — full bull alignment; the sequenced D10 closes (184.87 > 184.60) target the 20-day high (186.99) and the 9-month high (187.73).",
        support="183.81 (200-day SMA) / 183.09 (50% Fib), with the 61.8% Fib (182.00) beneath.",
        resistance="187.73 (9-month high), with the 20-day high (186.99) and the 50-day SMA (184.74) in the path.",
        priceAction="No entry — the intervention floor (2.5-sigma20 ~= 272 pips) against the 9-month-high cap (187.73) degrades any configuration to ~1:1. Wait for the window to expire (~Sep 3) or a pullback to the 182.00-183.09 zone to compress risk.",
        recommendation="WAIT FOR ANOTHER TRIGGER",
        trigger="None — sequenced D10 breakout, but the intervention floor (~=272 pips) versus the 187.73 cap locks R/R at ~1:1. Reassess after ~Sep 3 or on a pullback to the 182.00-183.09 zone (61.8% / 50% Fibs).",
        stop="N/A (no trade).",
        target="N/A (no trade).",
        rr="N/A", rrValue=0,
        justification="Full bull alignment and a confirmed breakout — but the intervention rule demands a stop >= 2.5-sigma20 (~=272 pips) while the farthest target (187.73) pays ~1:1. No trade until the window ages out or price pulls back to compress risk.",
    ))

A["GBP/JPY"] = dict(
    quote="216.01", bias="ALTA", biasType="bull",
    pt=dict(
        fundamental="O GBP/JPY opera em 216,01 no fechamento diário de 18/08/2026 (referência BCE), subindo +0,05% — novo fechamento além da máxima de 10 pregões (215,90), e a posição do ticket de 14/08 (entrada 215,90, stop 213,90, alvo 219,00) segue aberta e no azul. O CPI do Reino Unido amanhã (19/08, 07:00 London) bloqueia novas entradas em pares de libra pela janela de 24h, e o piso de intervenção 2,5σ20 (≈314 pips) manteria qualquer configuração nova em R/R <1 de qualquer forma. Indicadores calculados da série diária BCE/Frankfurter (522 pregões, 01/08/2024 a 18/08/2026).",
        trend="Acima das SMA50 (215,52) e SMA200 (212,03) — alinhamento de alta; fechamentos sucessivos além do D10 miram a máxima de 20 dias (218,27) e a de 9 meses (219,14).",
        support="215,24 (Fib 23,6%), com o redondo 213,00 e a Fib 38,2% (212,82) abaixo.",
        resistance="219,14 (máxima de 9 meses), com a máxima de 20 dias (218,27) no caminho.",
        priceAction="Sem nova entrada — CPI do RU (19/08, 07:00) e o piso de intervenção (≈314 pips) bloqueiam adições; a posição do ticket de 14/08 segue gerenciada (stop 213,90 / alvo 219,00).",
        recommendation="AGUARDAR OUTRO GATILHO",
        trigger="Nenhum — CPI do RU em 19/08 (07:00 London) bloqueia novas entradas em libra e o piso 2,5σ20 degrada qualquer R/R. A posição existente segue com stop 213,90 / alvo 219,00.",
        stop="N/A (sem nova operação).",
        target="N/A (sem nova operação).",
        rr="N/A", rrValue=0,
        justification="A estrutura segue de alta e a posição aberta acompanha o movimento, mas o filtro de eventos (CPI do RU dentro de 24h) e o piso de intervenção bloqueiam qualquer adição. Sem nova operação — gerenciar o ticket existente até o alvo de 219,00.",
    ),
    en=dict(
        fundamental="GBP/JPY trades at 216.01 on the 18/08/2026 daily close (ECB reference), up +0.05% — another close beyond the 10-day high (215.90), and the Aug 14 ticket's position (entry 215.90, stop 213.90, target 219.00) remains open and in the green. UK CPI tomorrow (Aug 19, 07:00 London) blocks new sterling entries through the 24h window, and the 2.5-sigma20 intervention floor (~=314 pips) would keep any new configuration below R/R 1 regardless. Indicators computed from the ECB/Frankfurter daily series (522 sessions, 01/08/2024 to 18/08/2026).",
        trend="Above the 50-day (215.52) and 200-day (212.03) SMAs — bull alignment; successive D10 closes target the 20-day high (218.27) and the 9-month high (219.14).",
        support="215.24 (23.6% Fib), with the 213.00 round number and the 38.2% Fib (212.82) beneath.",
        resistance="219.14 (9-month high), with the 20-day high (218.27) in the path.",
        priceAction="No new entry — UK CPI (Aug 19, 07:00) and the intervention floor (~=314 pips) block adds; the Aug 14 ticket stays managed (stop 213.90 / target 219.00).",
        recommendation="WAIT FOR ANOTHER TRIGGER",
        trigger="None — UK CPI on Aug 19 (07:00 London) blocks new sterling entries and the 2.5-sigma20 floor degrades any R/R. The existing position keeps stop 213.90 / target 219.00.",
        stop="N/A (no new trade).",
        target="N/A (no new trade).",
        rr="N/A", rrValue=0,
        justification="The structure stays bullish and the open position follows through, but the event filter (UK CPI inside 24h) and the intervention floor block any add. No new trade — manage the existing ticket toward the 219.00 target.",
    ))

# ---------------- helpers ----------------
def rep(text, old, new, where, n=1):
    c = text.count(old)
    if c != n:
        sys.exit(f"ERROR [{where}]: expected {n} occurrence(s), found {c}: {old[:80]}...")
    return text.replace(old, new)

# ---------------- index.html ----------------
SNAP = r"C:/Projetos/forex-report/.claude/index_old_snapshot.html"
with open(IDX, encoding="utf-8") as f:
    idx = f.read()
src = SNAP if os.path.exists(SNAP) else IDX
with open(src, encoding="utf-8") as f:
    src_html = f.read()
s = src_html.find("        const forexData = {")
if s == -1:
    sys.exit("ERROR: forexData block not found in source")
e = src_html.find("\n};", s) + len("\n};")
old_block = src_html[s:e]
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
if s2 == -1:
    sys.exit("ERROR: forexData block not found in live index.html")
e2 = idx.find("\n};", s2) + len("\n};")
idx = idx[:s2] + new_block + idx[e2:]

if OLD_TS in idx:
    m = re.search(r'(id="generationTime"[^>]*>Reports generated on: )[^<]*(</p>)', idx)
    if not m:
        sys.exit("ERROR: generationTime not found")
    idx = idx[:m.start()] + m.group(1) + TS + m.group(2) + idx[m.end():]
    if idx.count(OLD_TS) != 2:
        sys.exit(f"ERROR: expected 2 old timestamps, found {idx.count(OLD_TS)}")
    idx = idx.replace(OLD_TS, TS)

old_changes = '''        const dailyChanges = {
            "EUR/USD": "+0.22%",
            "USD/JPY": "+0.14%",
            "AUD/USD": "+0.61%",
            "GBP/USD": "+0.17%",
            "EUR/JPY": "+0.36%",
            "GBP/JPY": "+0.31%"
        };'''
new_changes = '''        const dailyChanges = {
            "EUR/USD": "-0.15%",
            "USD/JPY": "+0.30%",
            "AUD/USD": "-0.19%",
            "GBP/USD": "-0.25%",
            "EUR/JPY": "+0.15%",
            "GBP/JPY": "+0.05%"
        };'''
old_be = 'dataBasis: "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 521 daily sessions (01/08/2024–17/08/2026).",'
new_be = 'dataBasis: "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 522 daily sessions (01/08/2024–18/08/2026).",'
old_bp = 'dataBasis: "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, sigma20 e Donchian calculados · 521 pregões (01/08/2024 a 17/08/2026).",'
new_bp = 'dataBasis: "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, sigma20 e Donchian calculados · 522 pregões (01/08/2024 a 18/08/2026).",'
if old_changes in idx:
    idx = rep(idx, old_changes, new_changes, "ticker")
if old_be in idx:
    idx = rep(idx, old_be, new_be, "dataBasis EN")
if old_bp in idx:
    idx = rep(idx, old_bp, new_bp, "dataBasis PT")

with open(IDX, "w", encoding="utf-8") as f:
    f.write(idx)
print("OK: index.html")

# static pages' own data-basis line
for fname in PAGE.values():
    p = f"{DOCS}/{fname}"
    with open(p, encoding="utf-8") as f:
        h = f.read()
    oen = "ECB/Frankfurter reference rates · SMA50/200, sigma20 &amp; Donchian computed · 521 daily sessions (01/08/2024–17/08/2026)."
    nen = "ECB/Frankfurter reference rates · SMA50/200, sigma20 &amp; Donchian computed · 522 daily sessions (01/08/2024–18/08/2026)."
    opt = "taxas de referência BCE/Frankfurter · SMA50/200, sigma20 e Donchian calculados · 521 pregões (01/08/2024 a 17/08/2026)."
    npt = "taxas de referência BCE/Frankfurter · SMA50/200, sigma20 e Donchian calculados · 522 pregões (01/08/2024 a 18/08/2026)."
    if oen in h:
        h = rep(h, oen, nen, f"{fname} basis EN")
        h = rep(h, opt, npt, f"{fname} basis PT")
    with open(p, "w", encoding="utf-8") as f:
        f.write(h)
print("OK: 6 pages data-basis")

# ---------------- static pages ----------------
GAUGE = {"EUR/USD": 55, "USD/JPY": 7, "AUD/USD": 24, "GBP/USD": 44, "EUR/JPY": 27, "GBP/JPY": 20}
OLD_GAUGE = {"EUR/USD": 65, "USD/JPY": 72, "AUD/USD": 31, "GBP/USD": 8, "EUR/JPY": 21, "GBP/JPY": 17}
NEW_SCORE = {"EUR/USD": "8/10", "USD/JPY": "0/10", "AUD/USD": "0/10", "GBP/USD": "0/10", "EUR/JPY": "0/10", "GBP/JPY": "0/10"}
OLD_SCORE = {"EUR/USD": "8/10", "USD/JPY": "0/10", "AUD/USD": "0/10", "GBP/USD": "10/10", "EUR/JPY": "0/10", "GBP/JPY": "0/10"}
NEW_VC = {"EUR/USD": "sell", "USD/JPY": "wait", "AUD/USD": "wait", "GBP/USD": "wait", "EUR/JPY": "wait", "GBP/JPY": "wait"}
OLD_VC = {"EUR/USD": "sell", "USD/JPY": "wait", "AUD/USD": "wait", "GBP/USD": "buy", "EUR/JPY": "wait", "GBP/JPY": "wait"}

BLUF = {
 "USD/JPY": ('<span class="lang-en"><span class="bluf-action wait">WAIT</span> — D10 breakout; 2.5σ20 floor blocks R/R</span><span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — rompimento D10; piso 2,5σ20 bloqueia o R/R</span>',
             '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — 2.5σ20 intervention floor blocks the R/R</span><span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — piso de intervenção 2,5σ20 bloqueia o R/R</span>'),
 "AUD/USD": ('<span class="lang-en"><span class="bluf-action wait">WAIT</span> — 9-month high caps R/R; awaiting pullback zone</span><span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — máxima de 9 meses limita o R/R; aguardando zona de retração</span>',
             '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — D10 breakout priced in; 9-month high caps R/R</span><span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — rompimento D10 já precificado; máxima de 9 meses limita o R/R</span>'),
 "GBP/USD": ('<span class="lang-en"><span class="bluf-action wait">WAIT</span> — UK CPI (19/08) blocks entry; position from 1.3559 open</span><span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — CPI do RU (19/08) bloqueia entrada; posição de 1.3559 aberta</span>',
             '<span class="lang-en"><span class="bluf-action buy">LONG</span> on a breakout to <b>1.3559</b> &middot; stop <b>1.3490</b> &middot; target <b>1.3800</b> &middot; R/R <b>1:3.49</b></span><span class="lang-pt" style="display:none;"><span class="bluf-action buy">COMPRA</span> no rompimento de <b>1.3559</b> &middot; stop <b>1.3490</b> &middot; alvo <b>1.3800</b> &middot; R/R <b>1:3.49</b></span>'),
 "GBP/JPY": ('<span class="lang-en"><span class="bluf-action wait">WAIT</span> — CPI (19/08) + floor block adds; position open from 215.9</span><span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — CPI (19/08) + piso bloqueiam adições; posição aberta em 215.9</span>',
             '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — breakout fired at 215.9; 9-month high caps R/R</span><span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — rompimento acionado em 215.9; máxima de 9 meses limita o R/R</span>'),
}

SVG = {  # (old, new) tick values, each 2x — empty where unchanged
 "EUR/USD": [],
 "USD/JPY": [],
 "AUD/USD": [],
 "GBP/USD": [("1.3490", "1.3500")],
 "EUR/JPY": [("183.0", "183.1"), ("184.8", "184.7")],
 "GBP/JPY": [("215.9", "216.0")],
}
PRICE = {"EUR/USD": ("1.1593", "1.1576"), "USD/JPY": ("159.2", "159.7"), "AUD/USD": ("0.7125", "0.7111"),
         "GBP/USD": ("1.3559", "1.3526"), "EUR/JPY": ("184.6", "184.9"), "GBP/JPY": ("215.9", "216.0")}
# GBP/USD: bias class swaps (bull -> neutral)
BIAS_SWAPS = {
 "GBP/USD": [
   ('report-container bias-bull', 'report-container bias-neutral'),
   ('GBP/USD - BULLISH', 'GBP/USD - NEUTRAL'),
   ('GBP/USD - ALTA', 'GBP/USD - NEUTRO'),
 ],
}

for pair, fname in PAGE.items():
    path = f"{DOCS}/{fname}"
    with open(path, encoding="utf-8") as f:
        h = f.read()
    if f'Price {PRICE[pair][1]}</text>' in h and f'<strong>{A[pair]["quote"]}</strong>' in h and OLD_TS.replace("/", "/") not in h:
        # already converted heuristic: new quote present
        pass
    od, nd = old_data[pair], A[pair]
    # 1) BLUF
    if pair in BLUF:
        new_bluf, old_bluf = BLUF[pair]
        if old_bluf in h:
            h = rep(h, old_bluf, new_bluf, f"{fname} BLUF")
    # 2) verdict classes
    if OLD_VC[pair] != NEW_VC[pair]:
        h = rep(h, f'trade-ticket verdict-{OLD_VC[pair]}', f'trade-ticket verdict-{NEW_VC[pair]}', f"{fname} ticket class")
        h = rep(h, f'verdict-badge {OLD_VC[pair]}', f'verdict-badge {NEW_VC[pair]}', f"{fname} badge class")
    # 2b) bias class swaps
    for old, new in BIAS_SWAPS.get(pair, []):
        h = rep(h, old, new, f"{fname} bias swap")
    # 3) fields
    for lang in ("pt", "en"):
        for fl in ["fundamental", "trend", "support", "resistance", "priceAction",
                   "recommendation", "trigger", "stop", "target", "justification"]:
            oldv, newv = od[lang][fl], nd[lang][fl]
            if oldv == newv:
                continue
            h = rep(h, oldv, newv, f"{fname} {lang}.{fl}", 1)
    # 3b) rr strings
    oldrr, newrr = od["en"]["rr"], nd["en"]["rr"]
    if od["pt"]["rr"] != oldrr or nd["pt"]["rr"] != newrr:
        sys.exit(f"ERROR [{fname}]: PT/EN rr mismatch")
    if oldrr != newrr:
        remaining = h.count(oldrr)
        if not (1 <= remaining <= 4):
            sys.exit(f"ERROR [{fname}]: rr {oldrr} remaining count {remaining}")
        h = h.replace(oldrr, newrr)
        print(f"  {fname}: rr {oldrr} -> {newrr} ({remaining})")
    # 4) quote strong
    h = rep(h, f'<strong>{od["quote"]}</strong>', f'<strong>{nd["quote"]}</strong>', f"{fname} quote strong")
    # 5) price markers (BEFORE svg ticks to avoid prefix collisions)
    po, pn = PRICE[pair]
    h = rep(h, f'Price {po}</text>', f'Price {pn}</text>', f"{fname} price mark")
    h = rep(h, f'Preço {po}</text>', f'Preço {pn}</text>', f"{fname} preco mark")
    # 6) gauge
    h = rep(h, f'left: {OLD_GAUGE[pair]}%', f'left: {GAUGE[pair]}%', f"{fname} gauge", 2)
    # 7) conviction
    if OLD_SCORE[pair] != NEW_SCORE[pair]:
        h = rep(h, OLD_SCORE[pair], NEW_SCORE[pair], f"{fname} conviction")
    # 8) svg ticks
    for oldv, newv in SVG[pair]:
        h = rep(h, f'text-anchor="middle">{oldv}</text>', f'text-anchor="middle">{newv}</text>', f"{fname} svg {oldv}", 2)
    with open(path, "w", encoding="utf-8") as f:
        f.write(h)
    print(f"OK: {fname} ({pair})")

print("\nDONE: run verify_all.py next.")
