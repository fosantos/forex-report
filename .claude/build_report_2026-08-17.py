#!/usr/bin/env python3
"""17/08/2026 daily report build — FIRST report under the revised strategy rules
(SMA alignment bias, D10 close-breakout triggers, 1.5/2.5-sigma20 stop floors,
R/R >= 1:2 gate, risk suffix). Data basis: Frankfurter/ECB, 521 sessions
01/08/2024-17/08/2026 (compute_indicators.py run of 17/08/2026, last close 17/08).
Old field values are read from the live forexData block; every replacement is
count-asserted. Updates index.html (forexData, 3 timestamps, ticker, 2 dataBasis)
and the 6 static pages (fields + BLUF + SVG map + gauge + conviction + verdicts)."""
import json, re, sys

DOCS = r"C:/Projetos/forex-report/docs"
IDX = DOCS + "/index.html"
TS = "17/08/2026 21:10 UTC"
OLD_TS = "14/08/2026 20:19 UTC"

PAGE = {
    "EUR/USD": "eur-usd.html", "USD/JPY": "usd-jpy.html", "AUD/USD": "aud-usd.html",
    "GBP/USD": "gbp-usd.html", "EUR/JPY": "eur-jpy.html", "GBP/JPY": "gbp-jpy.html",
}

# ---------------- NEW ANALYSES (pt/en fields per pair) ----------------
A = {}
A["EUR/USD"] = dict(
    quote="1.1593", bias="BAIXA", biasType="bear",
    pt=dict(
        fundamental="O EUR/USD opera em 1,1593 no fechamento diário de 17/08/2026 (referência BCE, ~14:15 CET), avançando +0,22% e rompendo por fechamento a Fib 61,8% (1,1582) — o rally de correção agora pressiona diretamente a zona decisiva 1,1625-1,1657 (SMA200 / Fib 50%). O quadro macro segue o de 14/08: manutenção dividida do Fed em 9-3 a 3,50-3,75% (29/07), CPI de julho a +3,4% a.a. (divulgado 12/08, núcleo 2,5%) e DXY ~99,8 pressionam o dólar; o BCE a 2,25% limita o downside do euro. Mas os técnicos prevalecem: preço sob a SMA200 (1,1625) com SMA50 (1,1466) ainda abaixo dela — alinhamento de baixa — dentro do downtrend de 9 meses (1,1974 a 1,1340). Indicadores (SMA 50/200, σ20, Donchian e Fibonacci) calculados da série diária BCE/Frankfurter (521 pregões, 01/08/2024 a 17/08/2026).",
        trend="Abaixo da SMA200 (1,1625) e acima da SMA50 (1,1466), com SMA50 < SMA200 — alinhamento de baixa intacto; o rally de correção pressionou a Fib 61,8% (1,1582) e mira a confluência Fib 50% (1,1657) / SMA200 (1,1625).",
        support="1,1476 (Fib 78,6%), com a mínima de 9 meses em 1,1340 abaixo.",
        resistance="1,1657 (Fib 50%) em confluência com a SMA200 (1,1625) — a zona de venda; 1,1732 (Fib 38,2%) no topo.",
        priceAction="Uma rejeição na zona 1,1625-1,1657 — primeiro fechamento diário abaixo do fechamento anterior dentro da zona — retomaria a queda rumo a 1,1476-1,1450; fechamento diário acima de 1,1732 invalida o viés de baixa.",
        recommendation="VENDA (SHORT) NA RETRAÇÃO",
        trigger="Primeiro fechamento diário abaixo do fechamento anterior dentro da zona 1,1625-1,1657 (referência de entrada 1,1641, o meio da zona).",
        stop="1,1710 (Acima do número redondo 1,1700 e do piso de 1,5σ20 de 45 pips; invalida a SMA200) · risco sugerido ≤ 1% por operação.",
        target="1,1450 (Logo abaixo da Fib 78,6% em 1,1476).",
        rr="1:2.77", rrValue=69,
        justification="O alinhamento de baixa (SMA50 < SMA200 e preço sob a linha de 200 dias) prevalece sobre o macro de dólar pressionado, e o rally estaca exatamente na confluência Fib 50% / SMA200. Entrada vendida em 1,1641 com stop estrutural de 69 pips (≥ piso de 1,5σ20) e alvo a 191 pips entrega R/R de 1:2.77 rumo a 1,1450 — caminho limpo, sem S/R intermediária relevante.",
    ),
    en=dict(
        fundamental="EUR/USD trades at 1.1593 on the 17/08/2026 daily close (ECB reference, ~14:15 CET), up +0.22% and closing beyond the 61.8% Fib (1.1582) — the corrective rally now presses the decisive 1.1625-1.1657 zone (200-day SMA / 50% Fib). The macro backdrop carries over from Aug 14: the Fed's divided 9-3 hold at 3.50-3.75% (Jul 29), July CPI at +3.4% YoY (released Aug 12, core 2.5%) and DXY ~99.8 keep the dollar on the back foot; the ECB at 2.25% caps the euro's downside. But technicals prevail: price below the 200-day SMA (1.1625) with the 50-day (1.1466) still beneath it — bear alignment — inside the 9-month 1.1974 to 1.1340 downtrend. Indicators (SMA 50/200, sigma20, Donchian, Fibonacci) computed from the ECB/Frankfurter daily series (521 sessions, 01/08/2024 to 17/08/2026).",
        trend="Below the 200-day SMA (1.1625) and above the 50-day (1.1466), with SMA50 < SMA200 — bear alignment intact; the corrective rally has pressed the 61.8% Fib (1.1582) and targets the 50% Fib (1.1657) / 200-day SMA (1.1625) confluence.",
        support="1.1476 (78.6% Fib), with the 9-month low of 1.1340 beneath.",
        resistance="1.1657 (50% Fib) in confluence with the 200-day SMA (1.1625) — the selling zone; 1.1732 (38.2% Fib) on top.",
        priceAction="A rejection in the 1.1625-1.1657 zone — the first daily close below the previous close inside the zone — would resume the drop toward 1.1476-1.1450; a daily close above 1.1732 invalidates the bear bias.",
        recommendation="SELL (SHORT) ON PULLBACK",
        trigger="First daily close below the previous close inside the 1.1625-1.1657 zone (entry reference 1.1641, the zone midpoint).",
        stop="1.1710 (Above the 1.1700 round number and the 1.5-sigma20 floor of 45 pips; invalidates the 200-day SMA) · suggested risk ≤ 1% per trade.",
        target="1.1450 (Just below the 78.6% Fib at 1.1476).",
        rr="1:2.77", rrValue=69,
        justification="The bear alignment (SMA50 < SMA200, price under the 200-day line) outweighs the pressured-USD macro, and the rally stalls exactly at the 50% Fib / 200-day confluence. A short from 1.1641 with a 69-pip structural stop (>= the 1.5-sigma20 floor) and a 191-pip target delivers 1:2.77 R/R toward 1.1450 — a clean path with no relevant intermediate S/R.",
    ))

A["USD/JPY"] = dict(
    quote="159.23", bias="ALTA", biasType="bull",
    pt=dict(
        fundamental="O USD/JPY opera em 159,23 no fechamento diário de 17/08/2026 (referência BCE), subindo +0,14% enquanto o choque da intervenção conjunta EUA-Japão do início de agosto (estimada em ~US$ 75 bi) segue se desfazendo — o iene já devolveu cerca de metade dos ganhos e a janela de 30 dias de risco de intervenção permanece ativa. O BoJ manteve a taxa em 1,0% de forma hawkish em 31/07 (8-1, alta sinalizada para setembro) e o diferencial Fed (3,50-3,75%)-BoJ (1,0%) domina; a estrutura segue de alta com a SMA50 (161,14) acima da SMA200 (158,11) e o preço sobre esta última. Indicadores calculados da série diária BCE/Frankfurter (521 pregões, 01/08/2024 a 17/08/2026). O piso de stop de intervenção (2,5σ20 ≈ 267 pips) redefine o que é operável até a janela expirar.",
        trend="Acima da SMA200 (158,11) e abaixo da SMA50 (161,14) — alinhamento de alta (SMA50 > SMA200); o avanço de 152,63 a 163,91 segue restaurado, com a retração mirando a confluência Fib 50% (158,27) / SMA200 (158,11).",
        support="158,27 (Fib 50%) em confluência com a SMA200 (158,11); 156,94 (Fib 61,8%) abaixo.",
        resistance="159,60 (Fib 38,2%) na região atual, com a confluência SMA50 (161,14) / Fib 23,6% (161,25) acima; 163,91 (máxima de 9 meses) no topo.",
        priceAction="Sem gatilho acionável: com o piso de intervenção de 2,5σ20 (≈267 pips), qualquer stop estrutural a partir da zona 158,11-158,27 fica em ~300+ pips de risco e nenhum alvo atinge 1:2 — a SMA50 (161,14) entrega ~1:0,9 e a máxima de 163,91 ~1:1,8. Aguardar a janela de intervenção expirar (~03/09) ou retração mais profunda com σ20 comprimida.",
        recommendation="AGUARDAR OUTRO GATILHO",
        trigger="Nenhum gatilho operável — o piso de volatilidade de intervenção (2,5σ20 ≈ 267 pips) degrada todo R/R para abaixo de 1:2. Reavaliar quando a janela de 30 dias da intervenção expirar (~03/09), ou após retração à zona 158,11-158,27 com compressão da σ20.",
        stop="N/A (sem operação).",
        target="N/A (sem operação).",
        rr="N/A", rrValue=0,
        justification="O viés estrutural de alta está intacto (alinhamento SMA50 > SMA200, preço sobre os 200 dias), mas a regra de intervenção exige stop ≥ 2,5σ20 (≈267 pips) e o alvo mais distante disponível — a máxima de 163,91 — entrega apenas ~1:1,8. Técnicos e disciplina de risco vencem o carry: sem operação até a janela envelhecer.",
    ),
    en=dict(
        fundamental="USD/JPY trades at 159.23 on the 17/08/2026 daily close (ECB reference), up +0.14% as the early-August joint US-Japan intervention shock (estimated ~$75bn) keeps unwinding — the yen has given back about half of its gains and the 30-day intervention-risk window is still active. The BoJ held hawkishly at 1.00% on Jul 31 (8-1, a September hike signaled) and the Fed (3.50-3.75%)-BoJ (1.00%) differential dominates; structure stays bullish with the 50-day SMA (161.14) above the 200-day (158.11) and price on top of the latter. Indicators computed from the ECB/Frankfurter daily series (521 sessions, 01/08/2024 to 17/08/2026). The intervention stop floor (2.5-sigma20 ~= 267 pips) redefines what is tradeable until the window expires.",
        trend="Above the 200-day SMA (158.11) and below the 50-day (161.14) — bull alignment (SMA50 > SMA200); the 152.63 to 163.91 advance remains restored, with the pullback targeting the 50% Fib (158.27) / 200-day SMA (158.11) confluence.",
        support="158.27 (50% Fib) in confluence with the 200-day SMA (158.11); 156.94 (61.8% Fib) beneath.",
        resistance="159.60 (38.2% Fib) at the current region, with the 50-day SMA (161.14) / 23.6% Fib (161.25) confluence above; 163.91 (9-month high) on top.",
        priceAction="No actionable trigger: with the 2.5-sigma20 intervention floor (~=267 pips), any structural stop from the 158.11-158.27 zone sits ~300+ pips away and no target reaches 1:2 — the 50-day SMA (161.14) yields ~1:0.9 and the 163.91 high ~1:1.8. Wait for the intervention window to expire (~Sep 3) or a deeper pullback with compressed sigma20.",
        recommendation="WAIT FOR ANOTHER TRIGGER",
        trigger="No tradeable trigger — the intervention volatility floor (2.5-sigma20 ~= 267 pips) degrades every R/R below 1:2. Reassess when the 30-day intervention window expires (~Sep 3), or after a pullback to the 158.11-158.27 zone with sigma20 compression.",
        stop="N/A (no trade).",
        target="N/A (no trade).",
        rr="N/A", rrValue=0,
        justification="The structural bull bias is intact (SMA50 > SMA200, price above the 200-day), but the intervention rule demands a stop >= 2.5-sigma20 (~=267 pips) and the farthest available target — the 163.91 high — delivers only ~1:1.8. Technicals and risk discipline beat carry: no trade until the window ages out.",
    ))

A["AUD/USD"] = dict(
    quote="0.7125", bias="ALTA", biasType="bull",
    pt=dict(
        fundamental="O AUD/USD opera em 0,7125 no fechamento diário de 17/08/2026 (referência BCE), avançando +0,61% e fechando além da máxima de 10 pregões (0,7082) — rompimento Donchian-10 confirmado por fechamento, o maior fechamento em um mês, com a Fib 23,6% (0,7065) consolidada como suporte. O RBA manteve a taxa em 4,35% em 11/08 (padrão de espera), o petróleo firme (WTI ~US$ 82/bbl) sustenta o australiano e o CPI dos EUA a 3,4% com o Fed dividido mantém o dólar na defensiva. Alinhamento de alta: preço acima das SMA50 (0,6990) e SMA200 (0,6928) dentro do avanço de 0,6445 a 0,7257. Indicadores calculados da série diária BCE/Frankfurter (521 pregões, 01/08/2024 a 17/08/2026). O rompimento é direcionalmente válido — mas a máxima de 9 meses trava o risco-retorno.",
        trend="Acima das SMA50 (0,6990) e SMA200 (0,6928) — alinhamento de alta; o rompimento D10 de hoje (0,7125 > 0,7082) mira a máxima de 9 meses (0,7257), com a Fib 23,6% (0,7065) recém-rompida como primeiro suporte.",
        support="0,7065 (Fib 23,6% reconquistada), com a SMA50 (0,6990) abaixo.",
        resistance="0,7257 (máxima de 9 meses do avanço de 0,6445), com o número redondo 0,7200 no caminho.",
        priceAction="Sem entrada no rompimento de hoje: a máxima de 9 meses (0,7257) está a apenas ~130 pips — com stop estrutural abaixo de 0,7065 (~60-70 pips) o R/R máximo é ~1:1,8, e abaixo do redondo 0,7050 cai a ~1:1,4; o gate de 1:2 falha. Gatilhos futuros: retração à zona 0,6990-0,7065 (R/R ≥ 3 rumo a 0,7150) ou fechamento decisivo acima de 0,7257, abrindo ar limpo.",
        recommendation="AGUARDAR OUTRO GATILHO",
        trigger="Nenhum no rompimento de hoje — a máxima de 9 meses 0,7257 trava o R/R em ~1:1,8 com stop estrutural. Aguardar retração à zona 0,6990-0,7065 (SMA50 / Fib 23,6%) ou fechamento decisivo acima de 0,7257.",
        stop="N/A (sem operação).",
        target="N/A (sem operação).",
        rr="N/A", rrValue=0,
        justification="O rompimento Donchian-10 confirmado por fechamento valida a direção, mas a regra de R/R ≥ 1:2 com stop estrutural não fecha: nenhum alvo além de 0,7257 existe no horizonte de 9 meses e o nível está a ~1,8% — R/R máx ~1:1,8. Disciplina vence: aguardar retração à zona 0,6990-0,7065 ou novo ground.",
    ),
    en=dict(
        fundamental="AUD/USD trades at 0.7125 on the 17/08/2026 daily close (ECB reference), up +0.61% and closing beyond the 10-day high (0.7082) — a close-confirmed Donchian-10 breakout, the highest close in a month, with the 23.6% Fib (0.7065) consolidated as support. The RBA held at 4.35% on Aug 11 (waiting pattern), firm oil (WTI ~$82/bbl) underpins the aussie and US CPI at 3.4% with a divided Fed keeps the dollar defensive. Bull alignment: price above the 50-day (0.6990) and 200-day (0.6928) SMAs within the 0.6445 to 0.7257 advance. Indicators computed from the ECB/Frankfurter daily series (521 sessions, 01/08/2024 to 17/08/2026). The breakout is directionally valid — but the 9-month high caps the risk-reward.",
        trend="Above the 50-day (0.6990) and 200-day (0.6928) SMAs — bull alignment; today's D10 breakout (0.7125 > 0.7082) targets the 9-month high (0.7257), with the freshly-broken 23.6% Fib (0.7065) as first support.",
        support="0.7065 (reclaimed 23.6% Fib), with the 50-day SMA (0.6990) beneath.",
        resistance="0.7257 (9-month high of the 0.6445 advance), with the 0.7200 round number in the path.",
        priceAction="No entry on today's breakout: the 9-month high (0.7257) sits only ~130 pips away — with a structural stop below 0.7065 (~60-70 pips) the maximum R/R is ~1:1.8, and below the 0.7050 round it drops to ~1:1.4; the 1:2 gate fails. Future triggers: a pullback to the 0.6990-0.7065 zone (R/R >= 3 toward 0.7150) or a decisive close above 0.7257 opening clean air.",
        recommendation="WAIT FOR ANOTHER TRIGGER",
        trigger="None on today's breakout — the 9-month high at 0.7257 caps R/R at ~1:1.8 with a structural stop. Wait for a pullback to the 0.6990-0.7065 zone (50-day SMA / 23.6% Fib) or a decisive close above 0.7257.",
        stop="N/A (no trade).",
        target="N/A (no trade).",
        rr="N/A", rrValue=0,
        justification="The close-confirmed Donchian-10 breakout validates direction, but the R/R >= 1:2 rule with a structural stop doesn't close: no target beyond 0.7257 exists in the 9-month horizon and the level is only ~1.8% away — max R/R ~1:1.8. Discipline wins: wait for a pullback to 0.6990-0.7065 or fresh ground.",
    ))

A["GBP/USD"] = dict(
    quote="1.3559", bias="ALTA", biasType="bull",
    pt=dict(
        fundamental="O GBP/USD opera em 1,3559 no fechamento diário de 17/08/2026 (referência BCE), subindo +0,17% e fechando além da máxima de 10 pregões (1,3537) — rompimento Donchian-10 confirmado por fechamento, que resolve o estado misto do regime (preço acima das duas médias, mas com a SMA50 de 1,3373 ainda sob a SMA200 de 1,3406) na direção da alta. O BoE manteve a taxa em 3,75% em 30/07 (divisão 6-3, inflação a 2,6%) sustenta a libra, enquanto o CPI dos EUA a 3,4% e o Fed dividido (DXY ~99,8) pressionam o dólar. O par segue dentro do avanço de 1,3062 a 1,3817. Indicadores calculados da série diária BCE/Frankfurter (521 pregões, 01/08/2024 a 17/08/2026).",
        trend="Preço acima das SMA50 (1,3373) e SMA200 (1,3406) com SMA50 ainda abaixo da SMA200 — regime misto resolvido para a alta pelo rompimento D10 de hoje (1,3559 > 1,3537); o próximo obstáculo estrutural é a máxima de 9 meses (1,3817).",
        support="1,3537 (máxima de 10 dias rompida), com a Fib 38,2% (1,3528) e o número redondo 1,3500 abaixo.",
        resistance="1,3817 (máxima de 9 meses), com a zona 1,3600-1,3639 (número redondo / Fib 23,6%) no caminho.",
        priceAction="O rompimento confirmado por fechamento hoje (1,3559 > 1,3537) retoma o avanço rumo à máxima de 9 meses (1,3817); a perda de 1,3490 devolve o rompimento e invalida a entrada.",
        recommendation="COMPRA (LONG) NO ROMPIMENTO",
        trigger="Rompimento Donchian-10 confirmado no fechamento de hoje (1,3559 > máxima de 10 dias 1,3537) — entrada na região de 1,3559.",
        stop="1,3490 (Abaixo do número redondo 1,3500 e do piso de 1,5σ20 de 59 pips; devolve o rompimento) · risco sugerido ≤ 1% por operação.",
        target="1,3800 (No número redondo, logo abaixo da máxima de 9 meses em 1,3817).",
        rr="1:3.49", rrValue=87,
        justification="O fechamento além da máxima de 10 dias resolve o regime misto para a alta — a estrutura de rompimento se sobrepõe ao alinhamento incompleto das médias. Entrada em 1,3559 com stop estrutural de 69 pips (≥ piso de 1,5σ20 de 59) abaixo do redondo 1,3500 e alvo a 241 pips na máxima de 9 meses entrega R/R de 1:3.49; a zona 1,3600-1,3639 no caminho é confluência de continuação, não bloqueio estrutural.",
    ),
    en=dict(
        fundamental="GBP/USD trades at 1.3559 on the 17/08/2026 daily close (ECB reference), up +0.17% and closing beyond the 10-day high (1.3537) — a close-confirmed Donchian-10 breakout, which resolves the regime's mixed state (price above both SMAs but the 50-day at 1.3373 still below the 200-day at 1.3406) in the bullish direction. The BoE's hold at 3.75% on Jul 30 (6-3 split, inflation 2.6%) supports sterling, while US CPI at 3.4% and a divided Fed (DXY ~99.8) pressure the dollar. The pair remains inside the 1.3062 to 1.3817 advance. Indicators computed from the ECB/Frankfurter daily series (521 sessions, 01/08/2024 to 17/08/2026).",
        trend="Price above the 50-day (1.3373) and 200-day (1.3406) SMAs with the 50-day still below the 200-day — mixed regime resolved bullish by today's D10 breakout (1.3559 > 1.3537); the next structural obstacle is the 9-month high (1.3817).",
        support="1.3537 (broken 10-day high), with the 38.2% Fib (1.3528) and the 1.3500 round number beneath.",
        resistance="1.3817 (9-month high), with the 1.3600-1.3639 zone (round number / 23.6% Fib) en route.",
        priceAction="Today's close-confirmed breakout (1.3559 > 1.3537) resumes the advance toward the 9-month high (1.3817); losing 1.3490 hands back the breakout and invalidates the entry.",
        recommendation="BUY (LONG) ON BREAKOUT",
        trigger="Close-confirmed Donchian-10 breakout today (1.3559 > the 1.3537 10-day high) — entry in the 1.3559 area.",
        stop="1.3490 (Below the 1.3500 round number and the 1.5-sigma20 floor of 59 pips; hands back the breakout) · suggested risk ≤ 1% per trade.",
        target="1.3800 (On the round number, just below the 9-month high at 1.3817).",
        rr="1:3.49", rrValue=87,
        justification="The close beyond the 10-day high resolves the mixed regime bullish — breakout structure overrides the incomplete SMA alignment. An entry at 1.3559 with a 69-pip structural stop (>= the 59-pip 1.5-sigma20 floor) below the 1.3500 round and a 241-pip target at the 9-month high delivers 1:3.49 R/R; the 1.3600-1.3639 zone en route is continuation confluence, not a structural block.",
    ))

A["EUR/JPY"] = dict(
    quote="184.60", bias="ALTA", biasType="bull",
    pt=dict(
        fundamental="O EUR/JPY opera em 184,60 no fechamento diário de 17/08/2026 (referência BCE), subindo +0,36% com o choque de intervenção do início de agosto a desfazer-se e o carry BCE (2,25%)-BoJ (1,0%) retomando. O par fechou além da máxima de 10 pregões (183,93) — rompimento Donchian-10 — e reconquistou a SMA200 (183,78), mas segue sob a SMA50 (184,75). A janela de 30 dias de risco de intervenção segue ativa, mantendo o piso de stop em 2,5σ20 (≈272 pips). Indicadores calculados da série diária BCE/Frankfurter (521 pregões, 01/08/2024 a 17/08/2026). O rompimento é válido em direção — o risco-retorno não fecha.",
        trend="Acima da SMA200 (183,78) e sob a SMA50 (184,75) — alinhamento de alta (SMA50 > SMA200); o rompimento D10 de hoje (184,60 > 183,93) mira a máxima de 20 dias (186,99) e a de 9 meses (187,73).",
        support="183,78 (SMA200) / 183,02 (Fib 50%), com a Fib 61,8% (181,91) abaixo.",
        resistance="187,73 (máxima de 9 meses), com a máxima de 20 dias (186,99) e a SMA50 (184,75) no caminho.",
        priceAction="Sem entrada: com o piso de intervenção de 2,5σ20 (≈272 pips), o stop estrutural cai abaixo de 182,00 e o alvo mais distante (187,73) entrega apenas ~1:1 — o gate de 1:2 falha. Aguardar a janela expirar (~03/09) ou retração à zona 182,36-183,02 para comprimir o risco.",
        recommendation="AGUARDAR OUTRO GATILHO",
        trigger="Nenhum — o piso de intervenção (2,5σ20 ≈ 272 pips) versus o teto da máxima de 9 meses (187,73) degrada o R/R a ~1:1. Reavaliar após ~03/09 ou em retração à zona 182,36-183,02 (Fib 50% / 61,8%).",
        stop="N/A (sem operação).",
        target="N/A (sem operação).",
        rr="N/A", rrValue=0,
        justification="O rompimento D10 com reconquista da SMA200 valida a direção de alta, mas a regra de intervenção (stop ≥ 2,5σ20 ≈ 272 pips) empurra o stop para baixo de 182,00 enquanto a máxima de 9 meses (187,73) limita o ganho a ~310 pips — R/R ~1:1. Sem operação até a janela envelhecer ou o preço recuar para comprimir o risco.",
    ),
    en=dict(
        fundamental="EUR/JPY trades at 184.60 on the 17/08/2026 daily close (ECB reference), up +0.36% as the early-August intervention shock unwinds and the ECB (2.25%)-BoJ (1.00%) carry resumes. The pair closed beyond the 10-day high (183.93) — a Donchian-10 breakout — and reclaimed the 200-day SMA (183.78), but remains below the 50-day (184.75). The 30-day intervention-risk window is still active, keeping the stop floor at 2.5-sigma20 (~=272 pips). Indicators computed from the ECB/Frankfurter daily series (521 sessions, 01/08/2024 to 17/08/2026). The breakout is valid in direction — the risk-reward doesn't close.",
        trend="Above the 200-day SMA (183.78) and below the 50-day (184.75) — bull alignment (SMA50 > SMA200); today's D10 breakout (184.60 > 183.93) targets the 20-day high (186.99) and the 9-month high (187.73).",
        support="183.78 (200-day SMA) / 183.02 (50% Fib), with the 61.8% Fib (181.91) beneath.",
        resistance="187.73 (9-month high), with the 20-day high (186.99) and the 50-day SMA (184.75) in the path.",
        priceAction="No entry: with the 2.5-sigma20 intervention floor (~=272 pips), the structural stop drops below 182.00 and the farthest target (187.73) delivers only ~1:1 — the 1:2 gate fails. Wait for the window to expire (~Sep 3) or a pullback to the 182.36-183.02 zone to compress risk.",
        recommendation="WAIT FOR ANOTHER TRIGGER",
        trigger="None — the intervention floor (2.5-sigma20 ~= 272 pips) versus the 9-month high cap (187.73) degrades R/R to ~1:1. Reassess after ~Sep 3 or on a pullback to the 182.36-183.02 zone (50% / 61.8% Fibs).",
        stop="N/A (no trade).",
        target="N/A (no trade).",
        rr="N/A", rrValue=0,
        justification="The D10 breakout with the 200-day reclaim validates the bull direction, but the intervention rule (stop >= 2.5-sigma20 ~= 272 pips) pushes the stop below 182.00 while the 9-month high (187.73) caps the gain at ~310 pips — R/R ~1:1. No trade until the window ages out or price pulls back to compress risk.",
    ))

A["GBP/JPY"] = dict(
    quote="215.90", bias="ALTA", biasType="bull",
    pt=dict(
        fundamental="O GBP/JPY opera em 215,90 no fechamento diário de 17/08/2026 (referência BCE), subindo +0,31% — o rompimento antecipado pelo relatório de 14/08 foi acionado: fechamento diário acima da SMA50 (215,49) e da máxima de 10 pregões (215,24), o maior fechamento desde a máxima de 9 meses. O diferencial de carry BoE (3,75%)-BoJ (1,0%) segue amplo e o choque de intervenção se desfaz — mas a janela de 30 dias mantém o piso de stop em 2,5σ20 (≈315 pips), e a máxima de 9 meses (219,14) está a apenas ~1,5%. Indicadores calculados da série diária BCE/Frankfurter (521 pregões, 01/08/2024 a 17/08/2026).",
        trend="Acima das SMA50 (215,49) e SMA200 (211,96) — alinhamento de alta; o rompimento D10 de hoje (215,90 > 215,24) confirma o momentum, com a máxima de 20 dias (218,27) e a de 9 meses (219,14) acima.",
        support="215,24 (Fib 23,6%), com o número redondo 213,00 e a Fib 38,2% (212,82) abaixo.",
        resistance="219,14 (máxima de 9 meses), com a máxima de 20 dias (218,27) no caminho.",
        priceAction="Sem entrada nova: o rompimento de hoje esgota o ar até a máxima de 9 meses — com stop estrutural abaixo de 212,82 (Fib 38,2%) o R/R é ~1:0,9, e mesmo com stop de 1,5σ20 (213,90) cai a ~1:1,5; o piso de intervenção 2,5σ20 torna qualquer configuração pior. Gatilhos futuros: fechamento decisivo acima de 219,14 (ar limpo) ou retração à zona 213,00-214,00 com σ20 comprimida.",
        recommendation="AGUARDAR OUTRO GATILHO",
        trigger="Nenhum — o rompimento de hoje (215,90) já consumiu o alvo estrutural: a máxima de 9 meses (219,14) trava o R/R em ~0,9-1,5 com qualquer stop válido. Aguardar fechamento decisivo acima de 219,14 ou retração à zona 213,00-214,00.",
        stop="N/A (sem operação).",
        target="N/A (sem operação).",
        rr="N/A", rrValue=0,
        justification="O rompimento confirmado (215,90 > 215,50) valida o cenário de alta do relatório anterior — quem seguiu o ticket de 14/08 está posicionado — mas uma entrada nova não passa no gate: o teto de 219,14 e o piso de intervenção de 2,5σ20 (≈315 pips) degradam qualquer R/R a ~1:1. Sem nova operação até novo ground ou retração compressiva.",
    ),
    en=dict(
        fundamental="GBP/JPY trades at 215.90 on the 17/08/2026 daily close (ECB reference), up +0.31% — the breakout anticipated by the Aug 14 report fired: a daily close above the 50-day SMA (215.49) and the 10-day high (215.24), the highest close since the 9-month high. The BoE (3.75%)-BoJ (1.00%) carry gap remains wide and the intervention shock keeps unwinding — but the 30-day window holds the stop floor at 2.5-sigma20 (~=315 pips), and the 9-month high (219.14) is only ~1.5% away. Indicators computed from the ECB/Frankfurter daily series (521 sessions, 01/08/2024 to 17/08/2026).",
        trend="Above the 50-day (215.49) and 200-day (211.96) SMAs — bull alignment; today's D10 breakout (215.90 > 215.24) confirms momentum, with the 20-day high (218.27) and the 9-month high (219.14) above.",
        support="215.24 (23.6% Fib), with the 213.00 round number and the 38.2% Fib (212.82) beneath.",
        resistance="219.14 (9-month high), with the 20-day high (218.27) in the path.",
        priceAction="No new entry: today's breakout exhausts the air to the 9-month high — with a structural stop below 212.82 (38.2% Fib) R/R is ~1:0.9, and even a 1.5-sigma20 stop (213.90) drops it to ~1:1.5; the 2.5-sigma20 intervention floor makes any configuration worse. Future triggers: a decisive close above 219.14 (clean air) or a pullback to the 213.00-214.00 zone with compressed sigma20.",
        recommendation="WAIT FOR ANOTHER TRIGGER",
        trigger="None — today's breakout (215.90) already consumed the structural target: the 9-month high (219.14) caps R/R at ~0.9-1.5 with any valid stop. Wait for a decisive close above 219.14 or a pullback to the 213.00-214.00 zone.",
        stop="N/A (no trade).",
        target="N/A (no trade).",
        rr="N/A", rrValue=0,
        justification="The confirmed breakout (215.90 > 215.50) validates the prior report's bull case — anyone on the Aug 14 ticket is positioned — but a fresh entry fails the gate: the 219.14 cap and the 2.5-sigma20 intervention floor (~=315 pips) degrade every R/R to ~1:1. No new trade until fresh ground or a compressive pullback.",
    ))

# ---------------- helpers ----------------
def rep(text, old, new, where, n=1):
    c = text.count(old)
    if c != n:
        sys.exit(f"ERROR [{where}]: expected {n} occurrence(s), found {c}: {old[:80]}...")
    return text.replace(old, new)

def reps(h, old, new, where, n=1):
    """Idempotent rep: skip when the old text is already replaced by the new one."""
    if old not in h and new in h:
        print(f"  SKIP (already applied): {where}")
        return h
    return rep(h, old, new, where, n)

# ---------------- index.html ----------------
SNAP = r"C:/Projetos/forex-report/.claude/index_old_snapshot.html"
import os
with open(IDX, encoding="utf-8") as f:
    idx = f.read()

# parse current (old) forexData — prefer the pre-run snapshot when the live file was already updated
src = SNAP if os.path.exists(SNAP) else IDX
with open(src, encoding="utf-8") as f:
    src_html = f.read()
s = src_html.find("        const forexData = {")
if s == -1:
    sys.exit("ERROR: forexData block not found")
e = src_html.find("\n};", s) + len("\n};")
old_block = src_html[s:e]
old_data = json.loads(old_block[old_block.find("{"):-1].rstrip())

# build new block literal in the established format
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

# replace the block in the LIVE file (locate independently there)
s2 = idx.find("        const forexData = {")
if s2 == -1:
    sys.exit("ERROR: forexData block not found in live index.html")
e2 = idx.find("\n};", s2) + len("\n};")
for key in ["EUR/USD", "USD/JPY", "AUD/USD", "GBP/USD", "EUR/JPY", "GBP/JPY"]:
    if idx[s2:e2].count('"' + key + '"') != 1:
        sys.exit(f"ERROR: pair key {key} not found exactly once in live forexData block")
idx = idx[:s2] + new_block + idx[e2:]

# timestamps (idempotent: skip if already applied)
if OLD_TS in idx:
    m = re.search(r'(id="generationTime"[^>]*>Reports generated on: )[^<]*(</p>)', idx)
    if not m:
        sys.exit("ERROR: generationTime not found")
    idx = idx[:m.start()] + m.group(1) + TS + m.group(2) + idx[m.end():]
    if idx.count(OLD_TS) != 2:
        sys.exit(f"ERROR: expected 2 old timestamps, found {idx.count(OLD_TS)}")
    idx = idx.replace(OLD_TS, TS)

# ticker
old_changes = '''        const dailyChanges = {
            "EUR/USD": "+0.29%",
            "USD/JPY": "-0.20%",
            "AUD/USD": "+0.43%",
            "GBP/USD": "+0.33%",
            "EUR/JPY": "+0.08%",
            "GBP/JPY": "+0.13%"
        };'''
new_changes = '''        const dailyChanges = {
            "EUR/USD": "+0.22%",
            "USD/JPY": "+0.14%",
            "AUD/USD": "+0.61%",
            "GBP/USD": "+0.17%",
            "EUR/JPY": "+0.36%",
            "GBP/JPY": "+0.31%"
        };'''
# ticker + dataBasis (idempotent)
old_be = 'dataBasis: "Data basis: ECB/Frankfurter reference rates · SMA50/200 & Fibonacci computed · 520 daily sessions (01/08/2024–14/08/2026).",'
new_be = 'dataBasis: "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 521 daily sessions (01/08/2024–17/08/2026).",'
old_bp = 'dataBasis: "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200 e Fibonacci calculados · 520 pregões (01/08/2024 a 14/08/2026).",'
new_bp = 'dataBasis: "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, sigma20 e Donchian calculados · 521 pregões (01/08/2024 a 17/08/2026).",'
if old_changes in idx:
    idx = rep(idx, old_changes, new_changes, "ticker")
if old_be in idx:
    idx = rep(idx, old_be, new_be, "dataBasis EN")
if old_bp in idx:
    idx = rep(idx, old_bp, new_bp, "dataBasis PT")

with open(IDX, "w", encoding="utf-8") as f:
    f.write(idx)
print("OK: index.html (forexData + 3 timestamps + ticker + 2 dataBasis)")

# ---------------- static pages ----------------
GAUGE = {"EUR/USD": 65, "USD/JPY": 72, "AUD/USD": 31, "GBP/USD": 11, "EUR/JPY": 21, "GBP/JPY": 17}
OLD_GAUGE = {"EUR/USD": 86, "USD/JPY": 56, "AUD/USD": 44, "GBP/USD": 49, "EUR/JPY": 66, "GBP/JPY": 94}
NEW_SCORE = {"EUR/USD": "8/10", "USD/JPY": "0/10", "AUD/USD": "0/10", "GBP/USD": "10/10", "EUR/JPY": "0/10", "GBP/JPY": "0/10"}
OLD_SCORE = {"EUR/USD": "7/10", "USD/JPY": "7/10", "AUD/USD": "8/10", "GBP/USD": "8/10", "EUR/JPY": "0/10", "GBP/JPY": "7/10"}
NEW_VC = {"EUR/USD": "sell", "USD/JPY": "wait", "AUD/USD": "wait", "GBP/USD": "buy", "EUR/JPY": "wait", "GBP/JPY": "wait"}
OLD_VC = {"EUR/USD": "sell", "USD/JPY": "buy", "AUD/USD": "buy", "GBP/USD": "buy", "EUR/JPY": "wait", "GBP/JPY": "buy"}

BLUF = {
 "EUR/USD": ('<span class="lang-en"><span class="bluf-action sell">SHORT</span> on a pullback to <b>1.1641</b> &middot; stop <b>1.1710</b> &middot; target <b>1.1450</b> &middot; R/R <b>1:2.77</b></span><span class="lang-pt" style="display:none;"><span class="bluf-action sell">VENDA</span> na retração até <b>1.1641</b> &middot; stop <b>1.1710</b> &middot; alvo <b>1.1450</b> &middot; R/R <b>1:2.77</b></span>',
             '<span class="lang-en"><span class="bluf-action sell">SHORT</span> on a pullback to <b>1.1657</b> &middot; stop <b>1.1740</b> &middot; target <b>1.1450</b> &middot; R/R <b>1:2.49</b></span><span class="lang-pt" style="display:none;"><span class="bluf-action sell">VENDA</span> na retração até <b>1.1657</b> &middot; stop <b>1.1740</b> &middot; alvo <b>1.1450</b> &middot; R/R <b>1:2.49</b></span>'),
 "USD/JPY": ('<span class="lang-en"><span class="bluf-action wait">WAIT</span> — 2.5σ20 intervention floor blocks the R/R</span><span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — piso de intervenção 2,5σ20 bloqueia o R/R</span>',
             '<span class="lang-en"><span class="bluf-action buy">LONG</span> on a pullback to <b>158.1</b> &middot; stop <b>156.8</b> &middot; target <b>161.2</b> &middot; R/R <b>1:2.35</b></span><span class="lang-pt" style="display:none;"><span class="bluf-action buy">COMPRA</span> na retração até <b>158.1</b> &middot; stop <b>156.8</b> &middot; alvo <b>161.2</b> &middot; R/R <b>1:2.35</b></span>'),
 "AUD/USD": ('<span class="lang-en"><span class="bluf-action wait">WAIT</span> — D10 breakout priced in; 9-month high caps R/R</span><span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — rompimento D10 já precificado; máxima de 9 meses limita o R/R</span>',
             '<span class="lang-en"><span class="bluf-action buy">LONG</span> on a pullback to <b>0.6960</b> &middot; stop <b>0.6890</b> &middot; target <b>0.7150</b> &middot; R/R <b>1:2.71</b></span><span class="lang-pt" style="display:none;"><span class="bluf-action buy">COMPRA</span> na retração até <b>0.6960</b> &middot; stop <b>0.6890</b> &middot; alvo <b>0.7150</b> &middot; R/R <b>1:2.71</b></span>'),
 "GBP/USD": ('<span class="lang-en"><span class="bluf-action buy">LONG</span> on a breakout to <b>1.3559</b> &middot; stop <b>1.3490</b> &middot; target <b>1.3800</b> &middot; R/R <b>1:3.49</b></span><span class="lang-pt" style="display:none;"><span class="bluf-action buy">COMPRA</span> no rompimento de <b>1.3559</b> &middot; stop <b>1.3490</b> &middot; alvo <b>1.3800</b> &middot; R/R <b>1:3.49</b></span>',
             '<span class="lang-en"><span class="bluf-action buy">LONG</span> on a pullback to <b>1.3420</b> &middot; stop <b>1.3340</b> &middot; target <b>1.3625</b> &middot; R/R <b>1:2.56</b></span><span class="lang-pt" style="display:none;"><span class="bluf-action buy">COMPRA</span> na retração até <b>1.3420</b> &middot; stop <b>1.3340</b> &middot; alvo <b>1.3625</b> &middot; R/R <b>1:2.56</b></span>'),
 "GBP/JPY": ('<span class="lang-en"><span class="bluf-action wait">WAIT</span> — breakout fired at 215.9; 9-month high caps R/R</span><span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — rompimento acionado em 215.9; máxima de 9 meses limita o R/R</span>',
             '<span class="lang-en"><span class="bluf-action buy">LONG</span> on a breakout to <b>215.5</b> &middot; stop <b>213.9</b> &middot; target <b>219.0</b> &middot; R/R <b>1:2.19</b></span><span class="lang-pt" style="display:none;"><span class="bluf-action buy">COMPRA</span> no rompimento de <b>215.5</b> &middot; stop <b>213.9</b> &middot; alvo <b>219.0</b> &middot; R/R <b>1:2.19</b></span>'),
}

SVG = {  # pair -> ordered list of (old, new) tick values, each expected 2x
 "EUR/USD": [("1.1657", "1.1641"), ("1.1582", "1.1657"), ("1.1740", "1.1710")],
 "USD/JPY": [("156.8", "156.9"), ("161.2", "161.1")],
 "AUD/USD": [("0.6890", "0.7055"), ("0.6947", "0.6990"), ("0.6960", "0.7065"), ("0.7150", "0.7125")],
 "GBP/USD": [("1.3340", "1.3490"), ("1.3420", "1.3528"), ("1.3439", "1.3537"), ("1.3625", "1.3559"), ("1.3639", "1.3800")],
 "EUR/JPY": [("182.4", "183.0")],
 "GBP/JPY": [("212.2", "212.8"), ("213.9", "213.0"), ("215.4", "215.2"), ("215.5", "215.9"), ("219.0", "219.1")],
}
PRICE = {"EUR/USD": ("1.1567", "1.1593"), "USD/JPY": ("159.0", "159.2"), "AUD/USD": ("0.7082", "0.7125"),
         "GBP/USD": ("1.3537", "1.3559"), "EUR/JPY": ("183.9", "184.6"), "GBP/JPY": ("215.2", "215.9")}

for pair, fname in PAGE.items():
    path = f"{DOCS}/{fname}"
    with open(path, encoding="utf-8") as f:
        h = f.read()
    if f'<strong>{A[pair]["quote"]}</strong>' in h and f'Price {PRICE[pair][1]}</text>' in h:
        print(f"SKIP page (already converted): {fname}")
        continue
    od, nd = old_data[pair], A[pair]
    # 1) BLUF line (EUR/JPY's WAIT bluf is unchanged)
    if pair in BLUF:
        new_bluf, old_bluf = BLUF[pair]
        h = reps(h, old_bluf, new_bluf, f"{fname} BLUF")
    # 2) verdict classes
    if OLD_VC[pair] != NEW_VC[pair]:
        h = reps(h, f'trade-ticket verdict-{OLD_VC[pair]}', f'trade-ticket verdict-{NEW_VC[pair]}', f"{fname} ticket class")
        h = reps(h, f'verdict-badge {OLD_VC[pair]}', f'verdict-badge {NEW_VC[pair]}', f"{fname} badge class")
    # 3) field values (once per language per page)
    for lang in ("pt", "en"):
        for fl in ["fundamental", "trend", "support", "resistance", "priceAction",
                   "recommendation", "trigger", "stop", "target", "justification"]:
            oldv, newv = od[lang][fl], nd[lang][fl]
            if oldv == newv:
                continue
            h = reps(h, oldv, newv, f"{fname} {lang}.{fl}", 1)
    # 3b) rr string LAST (field texts above may contain it) — replace all remaining.
    # PT and EN rr strings are identical in this repo; single pass.
    oldrr, newrr = od["en"]["rr"], nd["en"]["rr"]
    if od["pt"]["rr"] != oldrr or nd["pt"]["rr"] != newrr:
        sys.exit(f"ERROR [{fname}]: PT/EN rr mismatch")
    if oldrr != newrr:
        if oldrr not in h and newrr in h:
            print(f"  SKIP (already applied): {fname} rr")
        else:
            remaining = h.count(oldrr)
            if not (1 <= remaining <= 4):
                sys.exit(f"ERROR [{fname}]: rr {oldrr} remaining count {remaining} unexpected")
            h = h.replace(oldrr, newrr)
            print(f"  {fname}: rr {oldrr} -> {newrr} ({remaining} occurrence(s))")
    # 4) quote <strong>
    h = reps(h, f'<strong>{od["quote"]}</strong>', f'<strong>{nd["quote"]}</strong>', f"{fname} quote strong")
    # 5) SVG price markers (Price/Preço)
    po, pn = PRICE[pair]
    h = reps(h, f'Price {po}</text>', f'Price {pn}</text>', f"{fname} price mark")
    h = reps(h, f'Preço {po}</text>', f'Preço {pn}</text>', f"{fname} preco mark")
    # 6) gauge
    h = reps(h, f'left: {OLD_GAUGE[pair]}%', f'left: {GAUGE[pair]}%', f"{fname} gauge", 2)
    # 7) conviction score
    if OLD_SCORE[pair] != NEW_SCORE[pair]:
        h = reps(h, OLD_SCORE[pair], NEW_SCORE[pair], f"{fname} conviction")
    # 8) SVG tick values
    for oldv, newv in SVG[pair]:
        h = reps(h, f'text-anchor="middle">{oldv}</text>', f'text-anchor="middle">{newv}</text>', f"{fname} svg {oldv}", 2)
    with open(path, "w", encoding="utf-8") as f:
        f.write(h)
    print(f"OK: {fname} ({pair})")

print("\nDONE: all files updated. Run verify_all.py next.")
