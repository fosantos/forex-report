#!/usr/bin/env python3
"""20/08/2026 daily report build. Data basis: Frankfurter/ECB, 524 sessions
01/08/2024-20/08/2026 (compute_indicators.py run of 20/08/2026).
Regime day: EUR/USD (+0.66%) and GBP/USD both closed D10 breakouts that resolve
their MIXED regimes BULLISH -> both biases flip to ALTA; the EUR/USD short
watching ticket is superseded (zone exceeded). No tradeable R/R anywhere:
EUR/USD capped by the 1.1700-1.1732 confluence (66 pips above), GBP/USD by the
9-month high, JPY pairs by intervention floors (~03/09), USD/JPY nearing its
pullback zone, AUD zone untouched by close. Verdicts: 6x WAIT."""
import json, re, sys

DOCS = r"C:/Projetos/forex-report/docs"
IDX = DOCS + "/index.html"
TS = "20/08/2026 20:55 UTC"
OLD_TS = "19/08/2026 20:50 UTC"
PAGE = {
    "EUR/USD": "eur-usd.html", "USD/JPY": "usd-jpy.html", "AUD/USD": "aud-usd.html",
    "GBP/USD": "gbp-usd.html", "EUR/JPY": "eur-jpy.html", "GBP/JPY": "gbp-jpy.html",
}

A = {}
A["EUR/USD"] = dict(
    quote="1.1681", bias="ALTA", biasType="bull",
    pt=dict(
        fundamental="O EUR/USD opera em 1,1681 no fechamento diário de 20/08/2026 (referência BCE, ~14:15 CET), saltando +0,66% — o maior fechamento em quase 3 meses — e atravessando a zona 1,1625-1,1657 (SMA200 / Fib 50%): fechamento além da máxima de 10 pregões (1,1605) que resolve o regime misto para a ALTA, devolvendo o par sobre a SMA200 (1,1627) pela primeira vez desde junho. O viés de baixa de 9 meses foi rechaçado sem o fechamento de rejeição na zona — o setup vendido foi superado. Macro: Fed dividido (9-3, 3,50-3,75%), CPI dos EUA 3,4%, DXY ~99,8 fraco, BCE 2,25%. Indicadores (SMA 50/200, σ20, Donchian e Fibonacci) calculados da série diária BCE/Frankfurter (524 pregões, 01/08/2024 a 20/08/2026). Falta a liberação do ar para operar.",
        trend="Preço acima da SMA200 (1,1627) mas com SMA50 (1,1470) ainda abaixo — regime misto resolvido para a alta pelo rompimento D10 (1,1681 > 1,1605); o próximo obstáculo estrutural é a confluência 1,1700-1,1732 (redondo / Fib 38,2%) e, acima, 1,1824 (Fib 23,6%) e a máxima de 9 meses (1,1974).",
        support="1,1657 (Fib 50% reconquistada) / 1,1627 (SMA200), com a mínima de 10 pregões (1,1534) abaixo.",
        resistance="1,1732 (Fib 38,2%), com 1,1824 (Fib 23,6%) e a máxima de 9 meses (1,1974) acima.",
        priceAction="Sem entrada: o rompimento é válido e resolve o misto para a alta, mas a confluência 1,1700-1,1732 está a apenas 66 pips — R/R ~1:1 rumo a ela; mirando 1,1974 com stop estrutural sob a SMA200 (1,1620, ~61 pips) o gate pede caminho limpo que ainda não existe. Gatilho: fechamento acima de 1,1732 abrindo 1,1824-1,1974.",
        recommendation="AGUARDAR OUTRO GATILHO",
        trigger="Nenhum — rompimento D10 válido (1,1681 > 1,1605) resolve o misto para a alta, mas a confluência 1,1700-1,1732 trava o R/R (~1:1). Aguardar fechamento acima de 1,1732 para mirar 1,1824-1,1974 com stop sob a SMA200; perda de 1,1625 devolve a zona à disputa.",
        stop="N/A (sem operação).",
        target="N/A (sem operação).",
        rr="N/A", rrValue=0,
        justification="A travessia da zona por fechamento é um evento de regime: o viés vira ALTA e o antigo gatilho vendido foi superado. Mas disciplina é disciplina — com o primeiro obstáculo real a 66 pips e o stop estrutural (sob a SMA200 reconquistada) a ~61 pips, nenhum alvo fecha 1:2. Aguardar a limpeza de 1,1732.",
    ),
    en=dict(
        fundamental="EUR/USD trades at 1.1681 on the 20/08/2026 daily close (ECB reference, ~14:15 CET), jumping +0.66% — the highest close in almost three months — and blowing through the 1.1625-1.1657 zone (200-day SMA / 50% Fib): a close beyond the 10-day high (1.1605) that resolves the mixed regime BULLISH, putting the pair back above the 200-day SMA (1.1627) for the first time since June. The 9-month bear bias was rejected without the zone rejection close — the short setup was overrun. Macro: divided Fed (9-3, 3.50-3.75%), US CPI 3.4%, weak DXY ~99.8, ECB 2.25%. Indicators (SMA 50/200, sigma20, Donchian, Fibonacci) computed from the ECB/Frankfurter daily series (524 sessions, 01/08/2024 to 20/08/2026). What's missing is clean air to trade.",
        trend="Price above the 200-day SMA (1.1627) but with the 50-day (1.1470) still below — mixed regime resolved bullish by the D10 breakout (1.1681 > 1.1605); the next structural obstacle is the 1.1700-1.1732 confluence (round / 38.2% Fib) and, above, 1.1824 (23.6% Fib) and the 9-month high (1.1974).",
        support="1.1657 (reclaimed 50% Fib) / 1.1627 (200-day SMA), with the 10-day low (1.1534) beneath.",
        resistance="1.1732 (38.2% Fib), with 1.1824 (23.6% Fib) and the 9-month high (1.1974) above.",
        priceAction="No entry: the breakout is valid and resolves the mix bullish, but the 1.1700-1.1732 confluence sits only 66 pips away — R/R ~1:1 toward it; targeting 1.1974 with a structural stop under the 200-day SMA (1.1620, ~61 pips) demands a clean path that doesn't exist yet. Trigger: a close above 1.1732 opening 1.1824-1.1974.",
        recommendation="WAIT FOR ANOTHER TRIGGER",
        trigger="None — valid D10 breakout (1.1681 > 1.1605) resolves the mix bullish, but the 1.1700-1.1732 confluence caps R/R (~1:1). Wait for a close above 1.1732 to target 1.1824-1.1974 with a stop under the 200-day SMA; losing 1.1625 returns the zone to dispute.",
        stop="N/A (no trade).",
        target="N/A (no trade).",
        rr="N/A", rrValue=0,
        justification="The zone crossing on a close is a regime event: the bias turns BULLISH and the former short trigger was overrun. But discipline is discipline — with the first real obstacle 66 pips away and the structural stop (under the reclaimed 200-day) ~61 pips away, no target closes 1:2. Wait for 1.1732 to clear.",
    ))

A["USD/JPY"] = dict(
    quote="158.76", bias="ALTA", biasType="bull",
    pt=dict(
        fundamental="O USD/JPY opera em 158,76 no fechamento diário de 20/08/2026 (referência BCE), recuando -0,21% e aproximando a retração da zona de compra 158,19-158,27 (SMA200 / Fib 50%) — agora a ~60 pips. O BoJ segue hawkish a 1,0% e o diferencial Fed-BoJ é amplo, com o alinhamento de alta intacto acima da SMA200; mas a janela de intervenção (até ~03/09) mantém o piso 2,5σ20 (≈265 pips), que degrada qualquer entrada a R/R <1:2. Indicadores calculados da série diária BCE/Frankfurter (524 pregões, 01/08/2024 a 20/08/2026).",
        trend="Acima da SMA200 (158,19) e abaixo da SMA50 (161,07) — alinhamento de alta; a retração desde a máxima de 10 pregões (159,70) mira a confluência Fib 50% (158,27) / SMA200 (158,19), a ~60 pips do fechamento.",
        support="158,27 (Fib 50%) / 158,19 (SMA200), com a Fib 61,8% (156,94) abaixo.",
        resistance="159,60 (Fib 38,2%), com a confluência SMA50 / Fib 23,6% (161,07-161,25) e a máxima de 9 meses (163,91) acima.",
        priceAction="Sem gatilho: a zona se aproxima, mas o piso de intervenção (2,5σ20 ≈ 265 pips) degrada tanto a entrada em retração quanto qualquer perseguição a R/R <1:2. Reavaliar após ~03/09 ou em fechamento dentro da zona com σ20 comprimida.",
        recommendation="AGUARDAR OUTRO GATILHO",
        trigger="Nenhum — piso de intervenção ativo até ~03/09. Reavaliar quando a janela expirar ou após fechamento dentro da zona 158,19-158,27 com compressão de σ20.",
        stop="N/A (sem operação).",
        target="N/A (sem operação).",
        rr="N/A", rrValue=0,
        justification="A retração caminha para a zona como o desenho pede — mas com o piso de intervenção ativo, a entrada permanece bloqueada. O alinhamento de alta segue; a janela envelhece em ~03/09.",
    ),
    en=dict(
        fundamental="USD/JPY trades at 158.76 on the 20/08/2026 daily close (ECB reference), easing -0.21% and bringing the pullback within ~60 pips of the 158.19-158.27 buying zone (200-day SMA / 50% Fib). The BoJ remains hawkish at 1.00% and the Fed-BoJ differential is wide, with the bull alignment intact above the 200-day; but the intervention window (until ~Sep 3) holds the 2.5-sigma20 floor (~=265 pips), degrading any entry below 1:2 R/R. Indicators computed from the ECB/Frankfurter daily series (524 sessions, 01/08/2024 to 20/08/2026).",
        trend="Above the 200-day SMA (158.19) and below the 50-day (161.07) — bull alignment; the pullback from the 10-day high (159.70) targets the 50% Fib (158.27) / 200-day SMA (158.19) confluence, ~60 pips from the close.",
        support="158.27 (50% Fib) / 158.19 (200-day SMA), with the 61.8% Fib (156.94) beneath.",
        resistance="159.60 (38.2% Fib), with the 50-day SMA / 23.6% Fib confluence (161.07-161.25) and the 9-month high (163.91) above.",
        priceAction="No trigger: the zone approaches, but the intervention floor (2.5-sigma20 ~= 265 pips) degrades both the pullback entry and any chase below 1:2 R/R. Reassess after ~Sep 3 or on a close inside the zone with compressed sigma20.",
        recommendation="WAIT FOR ANOTHER TRIGGER",
        trigger="None — intervention floor active until ~Sep 3. Reassess when the window expires or after a close inside the 158.19-158.27 zone with sigma20 compression.",
        stop="N/A (no trade).",
        target="N/A (no trade).",
        rr="N/A", rrValue=0,
        justification="The pullback walks into the zone just as the blueprint asks — but with the intervention floor active, the entry stays blocked. The bull alignment holds; the window ages out ~Sep 3.",
    ))

A["AUD/USD"] = dict(
    quote="0.7106", bias="ALTA", biasType="bull",
    pt=dict(
        fundamental="O AUD/USD opera em 0,7106 no fechamento diário de 20/08/2026 (referência BCE), saltando +0,43% de volta da Fib 23,6% (0,7065) — a retração beirou a zona de compra 0,6990-0,7065 sem fechamento dentro dela, e o rebote manteve o par acima do nível. RBA a 4,35% (11/08), WTI ~US$ 82 e dólar pressionado seguem; alinhamento de alta acima das SMA50 (0,6995) e SMA200 (0,6936) dentro do avanço de 0,6445 a 0,7257. Indicadores calculados da série diária BCE/Frankfurter (524 pregões, 01/08/2024 a 20/08/2026).",
        trend="Acima das SMA50 (0,6995) e SMA200 (0,6936) — alinhamento de alta; rebote sobre a Fib 23,6% (0,7065) sem toque por fechamento na zona 0,6990-0,7065, com a máxima de 9 meses (0,7257) acima.",
        support="0,7065 (Fib 23,6%), com a SMA50 (0,6995) abaixo.",
        resistance="0,7257 (máxima de 9 meses do avanço de 0,6445), com o número redondo 0,7200 no caminho.",
        priceAction="Sem gatilho: a zona 0,6990-0,7065 segue intocada por fechamento e a máxima de 9 meses trava a perseguição. Gatilhos: fechamento dentro da zona (R/R ≥ 3 rumo a 0,7150) ou fechamento decisivo acima de 0,7257.",
        recommendation="AGUARDAR OUTRO GATILHO",
        trigger="Nenhum — aguardar fechamento dentro da zona 0,6990-0,7065 (SMA50 / Fib 23,6%) ou fechamento decisivo acima de 0,7257.",
        stop="N/A (sem operação).",
        target="N/A (sem operação).",
        rr="N/A", rrValue=0,
        justification="A zona foi checada e rejeitada por baixo — o pullback perdeu o primeiro contato; nova aproximação continua válida (R/R ≥ 3 na zona), e a perseguição segue travada pela máxima de 9 meses. Sem operação.",
    ),
    en=dict(
        fundamental="AUD/USD trades at 0.7106 on the 20/08/2026 daily close (ECB reference), bouncing +0.43% back off the 23.6% Fib (0.7065) — the pullback grazed the 0.6990-0.7065 buying zone without a close inside it, and the rebound kept the pair above the level. RBA at 4.35% (Aug 11), WTI ~$82 and the pressured dollar persist; bull alignment above the 50-day (0.6995) and 200-day (0.6936) SMAs within the 0.6445 to 0.7257 advance. Indicators computed from the ECB/Frankfurter daily series (524 sessions, 01/08/2024 to 20/08/2026).",
        trend="Above the 50-day (0.6995) and 200-day (0.6936) SMAs — bull alignment; rebound off the 23.6% Fib (0.7065) without a close touching the 0.6990-0.7065 zone, with the 9-month high (0.7257) above.",
        support="0.7065 (23.6% Fib), with the 50-day SMA (0.6995) beneath.",
        resistance="0.7257 (9-month high of the 0.6445 advance), with the 0.7200 round number in the path.",
        priceAction="No trigger: the 0.6990-0.7065 zone remains untouched by a close and the 9-month high caps the chase. Triggers: a close inside the zone (R/R >= 3 toward 0.7150) or a decisive close above 0.7257.",
        recommendation="WAIT FOR ANOTHER TRIGGER",
        trigger="None — wait for a close inside the 0.6990-0.7065 zone (50-day SMA / 23.6% Fib) or a decisive close above 0.7257.",
        stop="N/A (no trade).",
        target="N/A (no trade).",
        rr="N/A", rrValue=0,
        justification="The zone was probed and rejected from above — the pullback missed its first contact; a new approach remains valid (R/R >= 3 in the zone), and the chase stays capped by the 9-month high. No trade.",
    ))

A["GBP/USD"] = dict(
    quote="1.3626", bias="ALTA", biasType="bull",
    pt=dict(
        fundamental="O GBP/USD opera em 1,3626 no fechamento diário de 20/08/2026 (referência BCE), avançando +0,52% e fechando além da máxima de 10 pregões (1,3559) — o rompimento D10 finalmente imprimiu e resolveu o regime misto para a ALTA (o fechamento parou 1,3 pip sob a Fib 23,6% de 1,3639). O CPI do RU passou sem trauma e a janela de eventos segue livre; BoE 3,75% (6-3) e dólar pressionado sustentam. A posição do ticket de 17/08 segue aberta com +67 pips (stop 1,3490 / alvo 1,3800). Indicadores calculados da série diária BCE/Frankfurter (524 pregões, 01/08/2024 a 20/08/2026).",
        trend="Preço acima das SMA50 (1,3384) e SMA200 (1,3414), com SMA50 ainda sob a SMA200 — regime misto resolvido para a alta pelo rompimento D10 (1,3626 > 1,3559); o fechamento parou sob a Fib 23,6% (1,3639), com a máxima de 9 meses (1,3817) acima.",
        support="1,3528 (Fib 38,2% reconquistada), com o redondo 1,3500 abaixo.",
        resistance="1,3817 (máxima de 9 meses), com a Fib 23,6% (1,3639) logo acima.",
        priceAction="Sem nova entrada: o rompimento é válido, mas a máxima de 9 meses (1,3817) está a ~1,4% e trava o R/R — com stop estrutural sob a Fib 38,2% (1,3520, ~106 pips) o melhor alvo entrega ~1:1,8. A posição existente segue rumo ao alvo 1,3800; adição reavaliada em fechamento acima de 1,3817 (ar limpo).",
        recommendation="AGUARDAR OUTRO GATILHO",
        trigger="Nenhum — rompimento D10 válido (1,3626 > 1,3559) resolve o misto para a alta, mas a máxima de 9 meses trava R/R em ~1:1,8 com stop estrutural. Posição existente segue (stop 1,3490 / alvo 1,3800); adição apenas acima de 1,3817.",
        stop="N/A (sem nova operação).",
        target="N/A (sem nova operação).",
        rr="N/A", rrValue=0,
        justification="O rompimento que faltava imprimiu — o viés vira ALTA e a posição de 17/08 acompanha rumo a 1,3800. Mas entrada nova não passa no gate: o teto de 1,3817 a ~1,4% contra stop estrutural de ~106 pips entrega ~1:1,8. Sem adição até novo ground.",
    ),
    en=dict(
        fundamental="GBP/USD trades at 1.3626 on the 20/08/2026 daily close (ECB reference), up +0.52% and closing beyond the 10-day high (1.3559) — the D10 breakout finally printed and resolves the mixed regime BULLISH (the close stopped 1.3 pips under the 23.6% Fib at 1.3639). UK CPI passed without trauma and the event window stays clear; BoE 3.75% (6-3) and the pressured dollar underpin. The Aug 17 ticket stays open with +67 pips (stop 1.3490 / target 1.3800). Indicators computed from the ECB/Frankfurter daily series (524 sessions, 01/08/2024 to 20/08/2026).",
        trend="Price above the 50-day (1.3384) and 200-day (1.3414) SMAs, with the 50-day still below the 200-day — mixed regime resolved bullish by the D10 breakout (1.3626 > 1.3559); the close stopped under the 23.6% Fib (1.3639), with the 9-month high (1.3817) above.",
        support="1.3528 (reclaimed 38.2% Fib), with the 1.3500 round beneath.",
        resistance="1.3817 (9-month high), with the 23.6% Fib (1.3639) just above.",
        priceAction="No new entry: the breakout is valid, but the 9-month high (1.3817) sits ~1.4% away and caps R/R — with a structural stop under the 38.2% Fib (1.3520, ~106 pips) the best target yields ~1:1.8. The existing position keeps running toward 1.3800; adds reassessed on a close above 1.3817 (clean air).",
        recommendation="WAIT FOR ANOTHER TRIGGER",
        trigger="None — valid D10 breakout (1.3626 > 1.3559) resolves the mix bullish, but the 9-month high caps R/R at ~1:1.8 with a structural stop. Existing position stays (stop 1.3490 / target 1.3800); adds only above 1.3817.",
        stop="N/A (no new trade).",
        target="N/A (no new trade).",
        rr="N/A", rrValue=0,
        justification="The missing breakout printed — the bias turns BULLISH and the Aug 17 position rides toward 1.3800. But a fresh entry fails the gate: the 1.3817 cap ~1.4% away against a ~106-pip structural stop yields ~1:1.8. No adds until fresh ground.",
    ))

A["EUR/JPY"] = dict(
    quote="185.45", bias="ALTA", biasType="bull",
    pt=dict(
        fundamental="O EUR/JPY opera em 185,45 no fechamento diário de 20/08/2026 (referência BCE), avançando +0,45% e fechando além da máxima de 10 pregões (184,87) — novo rompimento D10 com o par acima de ambas as médias (SMA50 184,74 > SMA200 183,90): alinhamento de alta pleno. Mas a janela de intervenção (até ~03/09) mantém o piso 2,5σ20 (≈277 pips): stop ≤ 182,68 contra o teto da máxima de 9 meses (187,73, a ~230 pips) entrega ~1:0,8 — o gate falha. Indicadores calculados da série diária BCE/Frankfurter (524 pregões, 01/08/2024 a 20/08/2026).",
        trend="Acima das SMA50 (184,74) e SMA200 (183,90) — alinhamento de alta pleno; rompimento D10 (185,45 > 184,87) mira a máxima de 20 dias (186,99) e a de 9 meses (187,73).",
        support="184,74 (SMA50) / 183,90 (SMA200), com a Fib 50% (183,46) abaixo.",
        resistance="187,73 (máxima de 9 meses), com a máxima de 20 dias (186,99) no caminho.",
        priceAction="Sem entrada — o piso de intervenção (≈277 pips) contra o teto de 187,73 segue travando qualquer configuração (~1:0,8). Aguardar a expiração da janela (~03/09) ou retração à zona 182,45-183,46 para comprimir o risco.",
        recommendation="AGUARDAR OUTRO GATILHO",
        trigger="Nenhum — piso de intervenção ativo até ~03/09 versus teto de 187,73 trava o R/R em ~1:0,8. Reavaliar após a janela ou em retração à zona 182,45-183,46.",
        stop="N/A (sem operação).",
        target="N/A (sem operação).",
        rr="N/A", rrValue=0,
        justification="Alinhamento de alta pleno e rompimento confirmado — mas a aritmética da intervenção não perdoa: stop de ~277 pips contra teto de ~230. Sem operação até ~03/09; a estrutura segue de alta.",
    ),
    en=dict(
        fundamental="EUR/JPY trades at 185.45 on the 20/08/2026 daily close (ECB reference), up +0.45% and closing beyond the 10-day high (184.87) — another D10 breakout with the pair above both SMAs (50-day 184.74 > 200-day 183.90): full bull alignment. But the intervention window (until ~Sep 3) holds the 2.5-sigma20 floor (~=277 pips): a stop <= 182.68 against the 9-month-high cap (187.73, ~230 pips away) yields ~1:0.8 — the gate fails. Indicators computed from the ECB/Frankfurter daily series (524 sessions, 01/08/2024 to 20/08/2026).",
        trend="Above the 50-day (184.74) and 200-day (183.90) SMAs — full bull alignment; D10 breakout (185.45 > 184.87) targets the 20-day high (186.99) and the 9-month high (187.73).",
        support="184.74 (50-day SMA) / 183.90 (200-day SMA), with the 50% Fib (183.46) beneath.",
        resistance="187.73 (9-month high), with the 20-day high (186.99) in the path.",
        priceAction="No entry — the intervention floor (~=277 pips) against the 187.73 cap still blocks any configuration (~1:0.8). Wait for the window to expire (~Sep 3) or a pullback to the 182.45-183.46 zone to compress risk.",
        recommendation="WAIT FOR ANOTHER TRIGGER",
        trigger="None — intervention floor active until ~Sep 3 versus the 187.73 cap locks R/R at ~1:0.8. Reassess after the window or on a pullback to 182.45-183.46.",
        stop="N/A (no trade).",
        target="N/A (no trade).",
        rr="N/A", rrValue=0,
        justification="Full bull alignment and a confirmed breakout — but the intervention arithmetic is unforgiving: a ~277-pip stop against a ~230-pip cap. No trade until ~Sep 3; the structure stays bullish.",
    ))

A["GBP/JPY"] = dict(
    quote="216.33", bias="ALTA", biasType="bull",
    pt=dict(
        fundamental="O GBP/JPY opera em 216,33 no fechamento diário de 20/08/2026 (referência BCE), avançando +0,31% e fechando além da máxima de 10 pregões (216,01) — a posição do ticket de 14/08 (entrada 215,90, stop 213,90, alvo 219,00) segue aberta com +43 pips e o alvo a apenas ~1,2%. O piso de intervenção 2,5σ20 (≈318 pips) segue ativo até ~03/09 e mantém adições em R/R <1 — a máxima de 9 meses (219,14) colada no alvo trava qualquer configuração nova. Indicadores calculados da série diária BCE/Frankfurter (524 pregões, 01/08/2024 a 20/08/2026).",
        trend="Acima das SMA50 (215,57) e SMA200 (212,19) — alinhamento de alta; rompimento D10 (216,33 > 216,01) com a máxima de 20 dias (218,27) e a de 9 meses (219,14) acima — o alvo do ticket quase colado à máxima.",
        support="215,24 (Fib 23,6%), com o redondo 213,00 e a Fib 38,2% (212,82) abaixo.",
        resistance="219,14 (máxima de 9 meses), com a máxima de 20 dias (218,27) no caminho.",
        priceAction="Sem nova entrada — o alvo do ticket (219,00) está a ~1,2% e colado à máxima de 9 meses; gerenciar a posição existente (stop 213,90 / alvo 219,00) e reavaliar adições apenas após fechamento acima de 219,14 (~03/09 ou novo ground).",
        recommendation="AGUARDAR OUTRO GATILHO",
        trigger="Nenhum — piso de intervenção ativo até ~03/09 e teto de 219,14 colado ao alvo do ticket. Posição existente segue (stop 213,90 / alvo 219,00); adição apenas acima de 219,14.",
        stop="N/A (sem nova operação).",
        target="N/A (sem nova operação).",
        rr="N/A", rrValue=0,
        justification="A posição legada caminha para o alvo com a estrutura de alta inteira a favor — mas adições seguem bloqueadas pelo piso de intervenção e pelo teto de 219,14 colado ao alvo. Gerenciar e colher.",
    ),
    en=dict(
        fundamental="GBP/JPY trades at 216.33 on the 20/08/2026 daily close (ECB reference), up +0.31% and closing beyond the 10-day high (216.01) — the Aug 14 ticket's position (entry 215.90, stop 213.90, target 219.00) stays open with +43 pips and the target only ~1.2% away. The 2.5-sigma20 intervention floor (~=318 pips) remains active until ~Sep 3 and keeps adds below R/R 1 — the 9-month high (219.14) glued to the target caps any new configuration. Indicators computed from the ECB/Frankfurter daily series (524 sessions, 01/08/2024 to 20/08/2026).",
        trend="Above the 50-day (215.57) and 200-day (212.19) SMAs — bull alignment; D10 breakout (216.33 > 216.01) with the 20-day high (218.27) and the 9-month high (219.14) above — the ticket's target almost glued to the high.",
        support="215.24 (23.6% Fib), with the 213.00 round number and the 38.2% Fib (212.82) beneath.",
        resistance="219.14 (9-month high), with the 20-day high (218.27) in the path.",
        priceAction="No new entry — the ticket's target (219.00) is ~1.2% away and glued to the 9-month high; manage the existing position (stop 213.90 / target 219.00) and reassess adds only after a close above 219.14 (~Sep 3 or fresh ground).",
        recommendation="WAIT FOR ANOTHER TRIGGER",
        trigger="None — intervention floor active until ~Sep 3 and the 219.14 cap glued to the ticket's target. Existing position stays (stop 213.90 / target 219.00); adds only above 219.14.",
        stop="N/A (no new trade).",
        target="N/A (no new trade).",
        rr="N/A", rrValue=0,
        justification="The legacy position walks toward its target with the entire bull structure behind it — but adds stay blocked by the intervention floor and the 219.14 cap glued to the target. Manage and harvest.",
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

# dashboard default badge reflects EUR/USD (now WAIT)
idx = rep(idx, 'verdict-badge sell" id="reportVerdictBadge">SELL (SHORT) ON PULLBACK',
          'verdict-badge wait" id="reportVerdictBadge">WAIT FOR ANOTHER TRIGGER', "index default badge")

m = re.search(r'(id="generationTime"[^>]*>Reports generated on: )[^<]*(</p>)', idx)
if not m:
    sys.exit("ERROR: generationTime not found")
idx = idx[:m.start()] + m.group(1) + TS + m.group(2) + idx[m.end():]
if idx.count(OLD_TS) != 2:
    sys.exit(f"ERROR: expected 2 old timestamps, found {idx.count(OLD_TS)}")
idx = idx.replace(OLD_TS, TS)

old_changes = '''        const dailyChanges = {
            "EUR/USD": "+0.25%",
            "USD/JPY": "-0.38%",
            "AUD/USD": "-0.50%",
            "GBP/USD": "+0.22%",
            "EUR/JPY": "-0.13%",
            "GBP/JPY": "-0.16%"
        };'''
new_changes = '''        const dailyChanges = {
            "EUR/USD": "+0.66%",
            "USD/JPY": "-0.21%",
            "AUD/USD": "+0.43%",
            "GBP/USD": "+0.52%",
            "EUR/JPY": "+0.45%",
            "GBP/JPY": "+0.31%"
        };'''
idx = rep(idx, old_changes, new_changes, "ticker")
old_be = 'dataBasis: "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 523 daily sessions (01/08/2024–19/08/2026).",'
new_be = 'dataBasis: "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 524 daily sessions (01/08/2024–20/08/2026).",'
old_bp = 'dataBasis: "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, sigma20 e Donchian calculados · 523 pregões (01/08/2024 a 19/08/2026).",'
new_bp = 'dataBasis: "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, sigma20 e Donchian calculados · 524 pregões (01/08/2024 a 20/08/2026).",'
idx = rep(idx, old_be, new_be, "dataBasis EN")
idx = rep(idx, old_bp, new_bp, "dataBasis PT")

with open(IDX, "w", encoding="utf-8") as f:
    f.write(idx)
print("OK: index.html")

# ---------------- static pages ----------------
GAUGE = {"EUR/USD": 32, "USD/JPY": 37, "AUD/USD": 21, "GBP/USD": 34, "EUR/JPY": 24, "GBP/JPY": 28}
OLD_GAUGE = {"EUR/USD": 71, "USD/JPY": 62, "AUD/USD": 6, "GBP/USD": 95, "EUR/JPY": 20, "GBP/JPY": 11}
NEW_SCORE = {"EUR/USD": "0/10", "USD/JPY": "0/10", "AUD/USD": "0/10", "GBP/USD": "0/10", "EUR/JPY": "0/10", "GBP/JPY": "0/10"}
OLD_SCORE = {"EUR/USD": "8/10", "USD/JPY": "0/10", "AUD/USD": "0/10", "GBP/USD": "0/10", "EUR/JPY": "0/10", "GBP/JPY": "0/10"}
NEW_VC = {"EUR/USD": "wait", "USD/JPY": "wait", "AUD/USD": "wait", "GBP/USD": "wait", "EUR/JPY": "wait", "GBP/JPY": "wait"}
OLD_VC = {"EUR/USD": "sell", "USD/JPY": "wait", "AUD/USD": "wait", "GBP/USD": "wait", "EUR/JPY": "wait", "GBP/JPY": "wait"}

BLUF = {
 "EUR/USD": ('<span class="lang-en"><span class="bluf-action wait">WAIT</span> — zone broken to the upside; 1.1732 clearance needed</span><span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — zona rompida para cima; falta fechar acima de 1.1732</span>',
             '<span class="lang-en"><span class="bluf-action sell">SHORT</span> on a pullback to <b>1.1641</b> &middot; stop <b>1.1710</b> &middot; target <b>1.1450</b> &middot; R/R <b>1:2.77</b></span><span class="lang-pt" style="display:none;"><span class="bluf-action sell">VENDA</span> na retração até <b>1.1641</b> &middot; stop <b>1.1710</b> &middot; alvo <b>1.1450</b> &middot; R/R <b>1:2.77</b></span>'),
 "USD/JPY": ('<span class="lang-en"><span class="bluf-action wait">WAIT</span> — pullback nearing the 158.19-158.27 zone; floor until ~03/09</span><span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — retração aproximando da zona 158.19-158.27; piso até ~03/09</span>',
             '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — breakout handed back; floor until ~03/09</span><span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — rompimento devolvido; piso até ~03/09</span>'),
 "AUD/USD": ('<span class="lang-en"><span class="bluf-action wait">WAIT</span> — zone 0.6990-0.7065 still untouched by close</span><span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — zona 0.6990-0.7065 segue intocada por fechamento</span>',
             '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — pullback nearing the 0.6990-0.7065 zone</span><span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — retração aproximando da zona 0.6990-0.7065</span>'),
 "GBP/USD": ('<span class="lang-en"><span class="bluf-action wait">WAIT</span> — breakout resolved bullish; 9-month high caps R/R; position open</span><span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — rompimento resolveu para alta; máxima de 9 meses trava R/R; posição aberta</span>',
             '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — close 1.3556 just under the 1.3559 trigger; CPI passed</span><span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — fechamento 1.3556 sob o gatilho 1.3559; CPI passou</span>'),
 "GBP/JPY": ('<span class="lang-en"><span class="bluf-action wait">WAIT</span> — position nearing the 219.00 target; floor until ~03/09</span><span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — posição aproximando do alvo 219.00; piso até ~03/09</span>',
             '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — floor until ~03/09; position open from 215.9</span><span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — piso até ~03/09; posição aberta em 215.9</span>'),
}

SVG = {  # ordered (old, new) swaps, collision-safe
 "EUR/USD": [("1.1657", "1.1732"), ("1.1476", "1.1657"), ("1.1450", "1.1620"), ("1.1641", "1.1681")],
 "USD/JPY": [],
 "AUD/USD": [],
 "GBP/USD": [("1.3537", "1.3639"), ("1.3559", "1.3626"), ("1.3800", "1.3817")],
 "EUR/JPY": [],
 "GBP/JPY": [],
}
PRICE = {"EUR/USD": ("1.1605", "1.1681"), "USD/JPY": ("159.1", "158.8"), "AUD/USD": ("0.7076", "0.7106"),
         "GBP/USD": ("1.3556", "1.3626"), "EUR/JPY": ("184.6", "185.4"), "GBP/JPY": ("215.7", "216.3")}

VERDICT_SWAPS = {
 "EUR/USD": [('trade-ticket verdict-sell', 'trade-ticket verdict-wait'),
             ('verdict-badge sell', 'verdict-badge wait')],
}
BIAS_SWAPS = {
 "EUR/USD": [('report-container bias-bear', 'report-container bias-bull'),
             ('EUR/USD - BEARISH', 'EUR/USD - BULLISH'),
             ('EUR/USD - BAIXA', 'EUR/USD - ALTA')],
 "GBP/USD": [('report-container bias-neutral', 'report-container bias-bull'),
             ('GBP/USD - NEUTRAL', 'GBP/USD - BULLISH'),
             ('GBP/USD - NEUTRO', 'GBP/USD - ALTA')],
}

for pair, fname in PAGE.items():
    path = f"{DOCS}/{fname}"
    with open(path, encoding="utf-8") as f:
        h = f.read()
    od, nd = old_data[pair], A[pair]
    # 1) BLUF
    if pair in BLUF:
        new_bluf, old_bluf = BLUF[pair]
        h = rep(h, old_bluf, new_bluf, f"{fname} BLUF")
    # 2) verdict classes
    for old, new in VERDICT_SWAPS.get(pair, []):
        h = rep(h, old, new, f"{fname} verdict swap")
    # 2b) bias classes
    for old, new in BIAS_SWAPS.get(pair, []):
        h = rep(h, old, new, f"{fname} bias swap")
    # 3) fields
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
    # 3b) rr
    oldrr, newrr = od["en"]["rr"], nd["en"]["rr"]
    if oldrr != newrr:
        remaining = h.count(oldrr)
        if not (1 <= remaining <= 4):
            sys.exit(f"ERROR [{fname}]: rr {oldrr} remaining count {remaining}")
        h = h.replace(oldrr, newrr)
        print(f"  {fname}: rr {oldrr} -> {newrr} ({remaining})")
    # 4) quote strong
    h = rep(h, f'<strong>{od["quote"]}</strong>', f'<strong>{nd["quote"]}</strong>', f"{fname} quote strong")
    # 5) price markers
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

# pages' data-basis lines
for fname in PAGE.values():
    p = f"{DOCS}/{fname}"
    with open(p, encoding="utf-8") as f:
        h = f.read()
    oen = "ECB/Frankfurter reference rates · SMA50/200, sigma20 &amp; Donchian computed · 523 daily sessions (01/08/2024–19/08/2026)."
    nen = "ECB/Frankfurter reference rates · SMA50/200, sigma20 &amp; Donchian computed · 524 daily sessions (01/08/2024–20/08/2026)."
    opt = "taxas de referência BCE/Frankfurter · SMA50/200, sigma20 e Donchian calculados · 523 pregões (01/08/2024 a 19/08/2026)."
    npt = "taxas de referência BCE/Frankfurter · SMA50/200, sigma20 e Donchian calculados · 524 pregões (01/08/2024 a 20/08/2026)."
    h = rep(h, oen, nen, f"{fname} basis EN")
    h = rep(h, opt, npt, f"{fname} basis PT")
    with open(p, "w", encoding="utf-8") as f:
        f.write(h)
print("OK: 6 pages data-basis")
print("\nDONE: run verify_all.py next.")
