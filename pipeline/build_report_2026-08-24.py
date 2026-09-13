#!/usr/bin/env python3
"""24/08/2026 daily report build. Data basis: Frankfurter/ECB, 526 sessions
01/08/2024-24/08/2026 (compute_indicators.py run of 24/08/2026).
Consolidation day after the 20-21/08 breakout wave — no verdict changes:
- EUR/USD: first pullback close (-0.30% to 1.1664) holds above the reclaimed
  50% Fib (1.1657) / SMA200 (1.1628); Fri's 1.1699 stopped ~1 pip under the
  1.1700 round — the 1.1700-1.1732 confluence still caps (~1:1). WAIT.
- USD/JPY: pullback died ABOVE the 158.25-158.27 zone (lowest close 158.70),
  bounce +0.27% back under the 38.2% Fib (159.60); zone untouched, floor
  2.5-sigma20 (~266 pips) until ~03/09. WAIT.
- AUD/USD: Fri 0.7168 printed the D10 continuation breakout; round 0.7200 +
  9-mo high 0.7257 cap the chase; 0.7000-0.7065 zone still untouched. WAIT.
- GBP/USD: settling on the 23.6% Fib (1.3639); Aug-17 position +75 pips
  toward 1.3800; adds only above the 9-mo high 1.3817. WAIT.
- EUR/JPY: flat under Fri's D10 close; intervention floor (~278 pips) vs the
  187.73 cap ~1:0.8; window to ~03/09. WAIT.
- GBP/JPY: fresh D10 close 216.95 (> 216.72); position +105 pips, target
  219.00 ~0.95% away glued to the 9-mo high 219.14. WAIT.
Also fixes two pre-existing defects: eur-jpy.html's empty BLUF text and
eur-usd.html's bias-badge left on bias-bear after the 20/08 bull flip; the
static range-gauge text labels (now-value + bounds) are refreshed to match
the current S/R after drifting stale since 14/08."""
import json, re, sys

DOCS = r"C:/Projetos/forex-report/docs"
IDX = DOCS + "/index.html"
TS = "24/08/2026 18:35 UTC"
OLD_TS = "20/08/2026 20:55 UTC"
PAGE = {
    "EUR/USD": "eur-usd.html", "USD/JPY": "usd-jpy.html", "AUD/USD": "aud-usd.html",
    "GBP/USD": "gbp-usd.html", "EUR/JPY": "eur-jpy.html", "GBP/JPY": "gbp-jpy.html",
}

A = {}
A["EUR/USD"] = dict(
    quote="1.1664", bias="ALTA", biasType="bull",
    pt=dict(
        fundamental="O EUR/USD opera em 1,1664 no fechamento diário de 24/08/2026 (referência BCE), cedendo -0,30% na primeira pausa após o rompimento: a sequência 20-21/08 (1,1681/1,1699) parou a ~1 pip do redondo 1,1700 e a confluência 1,1700-1,1732 (redondo / Fib 38,2%) rejeitou o avanço — retração que ainda preserva a Fib 50% reconquistada (1,1657) e a SMA200 (1,1628). O regime misto segue resolvido para a ALTA pelo rompimento D10; perder 1,1625 devolve a zona à disputa. Macro: Fed dividido (9-3, 3,50-3,75%) com Jackson Hole em 27-29/08 (primeiro discurso de Warsh como chair, sexta), DXY ~98,9 fraco, CPI dos EUA 3,4%, BCE 2,25%. Indicadores (SMA 50/200, σ20, Donchian e Fibonacci) calculados da série diária BCE/Frankfurter (526 pregões, 01/08/2024 a 24/08/2026).",
        trend="Preço acima da SMA200 (1,1628) com SMA50 (1,1474) ainda abaixo — regime misto resolvido para a alta pelo rompimento D10 (1,1681 > 1,1605, confirmado em 1,1699); o primeiro teste da confluência 1,1700-1,1732 foi rejeitado por ~1 pip (1,1699), com 1,1824 (Fib 23,6%) e a máxima de 9 meses (1,1974) acima.",
        support="1,1657 (Fib 50% reconquistada) / 1,1628 (SMA200), com a mínima de 10 pregões (1,1534) abaixo.",
        resistance="1,1732 (Fib 38,2%), com o redondo 1,1700 no caminho e 1,1824 (Fib 23,6%) / 1,1974 (máxima de 9 meses) acima.",
        priceAction="Sem entrada: a retração preserva o rompimento, mas a confluência 1,1700-1,1732 está a 68 pips e bloqueia o caminho para qualquer alvo ≥1:2 — o stop estrutural (~54 pips, sob 1,1610) mal alcança o piso de 1,5σ20 (52 pips) e a perseguição sem fechamento acima dela não passa no gate. Gatilho: fechamento acima de 1,1732 abrindo 1,1824-1,1974.",
        recommendation="AGUARDAR OUTRO GATILHO",
        trigger="Nenhum — o teste da confluência 1,1700-1,1732 foi rejeitado (1,1699) e o R/R segue ~1:1. Aguardar fechamento acima de 1,1732 para mirar 1,1824-1,1974 com stop sob a SMA200; perda de 1,1625 devolve a zona à disputa.",
        stop="N/A (sem operação).",
        target="N/A (sem operação).",
        rr="N/A", rrValue=0,
        justification="Disciplina: o viés de alta do rompimento segue intacto (fechamentos acima da SMA200), mas o primeiro obstáculo real a 68 pips continua travando qualquer configuração em ~1:1. A retração é saudável; esperar a limpeza de 1,1732 — de preferência fora da janela de Jackson Hole (27-29/08).",
    ),
    en=dict(
        fundamental="EUR/USD trades at 1.1664 on the 24/08/2026 daily close (ECB reference), giving back -0.30% in the first pause after the breakout: the Aug 20-21 sequence (1.1681/1.1699) stopped ~1 pip under the 1.1700 round and the 1.1700-1.1732 confluence (round / 38.2% Fib) rejected the advance — a pullback that still holds the reclaimed 50% Fib (1.1657) and the 200-day SMA (1.1628). The mixed regime stays resolved BULLISH by the D10 breakout; losing 1.1625 returns the zone to dispute. Macro: divided Fed (9-3, 3.50-3.75%) with Jackson Hole on Aug 27-29 (Warsh's first speech as chair, Friday), weak DXY ~98.9, US CPI 3.4%, ECB 2.25%. Indicators (SMA 50/200, sigma20, Donchian, Fibonacci) computed from the ECB/Frankfurter daily series (526 sessions, 01/08/2024 to 24/08/2026).",
        trend="Price above the 200-day SMA (1.1628) with the 50-day (1.1474) still below — mixed regime resolved bullish by the D10 breakout (1.1681 > 1.1605, confirmed at 1.1699); the first test of the 1.1700-1.1732 confluence was rejected by ~1 pip (1.1699), with 1.1824 (23.6% Fib) and the 9-month high (1.1974) above.",
        support="1.1657 (reclaimed 50% Fib) / 1.1628 (200-day SMA), with the 10-day low (1.1534) beneath.",
        resistance="1.1732 (38.2% Fib), with the 1.1700 round in the path and 1.1824 (23.6% Fib) / 1.1974 (9-month high) above.",
        priceAction="No entry: the pullback preserves the breakout, but the 1.1700-1.1732 confluence sits 68 pips away and blocks the path to any >=1:2 target — the structural stop (~54 pips, under 1.1610) barely reaches the 1.5-sigma20 floor (52 pips) and chasing without a close above it fails the gate. Trigger: a close above 1.1732 opening 1.1824-1.1974.",
        recommendation="WAIT FOR ANOTHER TRIGGER",
        trigger="None — the first test of the 1.1700-1.1732 confluence was rejected (1.1699) and R/R stays ~1:1. Wait for a close above 1.1732 to target 1.1824-1.1974 with a stop under the 200-day SMA; losing 1.1625 returns the zone to dispute.",
        stop="N/A (no trade).",
        target="N/A (no trade).",
        rr="N/A", rrValue=0,
        justification="Discipline: the breakout's bull bias stays intact (closes above the 200-day SMA), but the first real obstacle 68 pips away keeps capping any configuration at ~1:1. The pullback is healthy; wait for 1.1732 to clear — preferably outside the Jackson Hole window (Aug 27-29).",
    ))

A["USD/JPY"] = dict(
    quote="159.12", bias="ALTA", biasType="bull",
    pt=dict(
        fundamental="O USD/JPY opera em 159,12 no fechamento diário de 24/08/2026 (referência BCE), recuperando +0,27% após a retração morrer acima da zona: a mínima de fechamento (158,70-158,76 em 20-21/08) nunca tocou a zona de compra 158,25-158,27 (SMA200 / Fib 50%), e o rebote devolveu o par à faixa 158,7-159,7. O BoJ segue hawkish a 1,0% (Himino fala em 27/08, reunião de setembro à vista) e o diferencial Fed-BoJ é amplo, com o alinhamento de alta intacto acima da SMA200; mas a janela de intervenção (até ~03/09) mantém o piso 2,5σ20 (≈266 pips), que degrada qualquer entrada a R/R <1:2. Indicadores calculados da série diária BCE/Frankfurter (526 pregões, 01/08/2024 a 24/08/2026).",
        trend="Acima da SMA200 (158,25) e abaixo da SMA50 (161,02) — alinhamento de alta; retração rejeitada acima da zona com o par de volta sob a Fib 38,2% (159,60), dentro do canal de 10 pregões (158,70-159,70).",
        support="158,27 (Fib 50%) / 158,25 (SMA200), com a mínima de 10 pregões (158,70) já recuperada e a Fib 61,8% (156,94) abaixo.",
        resistance="159,60 (Fib 38,2%), com a máxima de 10 pregões (159,70), a confluência SMA50 / Fib 23,6% (161,02-161,25) e a máxima de 9 meses (163,91) acima.",
        priceAction="Sem gatilho: a zona 158,25-158,27 segue intocada por fechamento (mínima 158,70) e o piso de intervenção (2,5σ20 ≈ 266 pips) degrada tanto a entrada em retração quanto qualquer perseguição a R/R <1:2. Reavaliar após ~03/09 ou em fechamento dentro da zona com σ20 comprimida.",
        recommendation="AGUARDAR OUTRO GATILHO",
        trigger="Nenhum — piso de intervenção ativo até ~03/09 e zona 158,25-158,27 intocada. Reavaliar quando a janela expirar ou após fechamento dentro da zona com compressão de σ20.",
        stop="N/A (sem operação).",
        target="N/A (sem operação).",
        rr="N/A", rrValue=0,
        justification="O desenho segue: alinhamento de alta, retração que morreu acima da zona e rebote — mas sem toque na zona não há gatilho de retração, e com o piso de intervenção a perseguição não passa no gate. A janela envelhece em ~03/09.",
    ),
    en=dict(
        fundamental="USD/JPY trades at 159.12 on the 24/08/2026 daily close (ECB reference), bouncing +0.27% after the pullback died above the zone: the lowest close (158.70-158.76 on Aug 20-21) never touched the 158.25-158.27 buying zone (200-day SMA / 50% Fib), and the rebound put the pair back inside the 158.7-159.7 band. The BoJ remains hawkish at 1.00% (Himino speaks Aug 27, September meeting in sight) and the Fed-BoJ differential is wide, with the bull alignment intact above the 200-day; but the intervention window (until ~Sep 3) holds the 2.5-sigma20 floor (~=266 pips), degrading any entry below 1:2 R/R. Indicators computed from the ECB/Frankfurter daily series (526 sessions, 01/08/2024 to 24/08/2026).",
        trend="Above the 200-day SMA (158.25) and below the 50-day (161.02) — bull alignment; pullback rejected above the zone with the pair back under the 38.2% Fib (159.60), inside the 10-day channel (158.70-159.70).",
        support="158.27 (50% Fib) / 158.25 (200-day SMA), with the 10-day low (158.70) already reclaimed and the 61.8% Fib (156.94) beneath.",
        resistance="159.60 (38.2% Fib), with the 10-day high (159.70), the 50-day SMA / 23.6% Fib confluence (161.02-161.25) and the 9-month high (163.91) above.",
        priceAction="No trigger: the 158.25-158.27 zone remains untouched by a close (lowest 158.70) and the intervention floor (2.5-sigma20 ~= 266 pips) degrades both the pullback entry and any chase below 1:2 R/R. Reassess after ~Sep 3 or on a close inside the zone with compressed sigma20.",
        recommendation="WAIT FOR ANOTHER TRIGGER",
        trigger="None — intervention floor active until ~Sep 3 and the 158.25-158.27 zone untouched. Reassess when the window expires or after a close inside the zone with sigma20 compression.",
        stop="N/A (no trade).",
        target="N/A (no trade).",
        rr="N/A", rrValue=0,
        justification="The blueprint holds: bull alignment, a pullback that died above the zone and a rebound — but without a touch of the zone there is no pullback trigger, and with the intervention floor the chase fails the gate. The window ages out ~Sep 3.",
    ))

A["AUD/USD"] = dict(
    quote="0.7162", bias="ALTA", biasType="bull",
    pt=dict(
        fundamental="O AUD/USD opera em 0,7162 no fechamento diário de 24/08/2026 (referência BCE), praticamente estável (-0,09%) sob a nova máxima de 10 pregões: sexta (21/08) imprimiu o rompimento D10 de continuação (0,7168 > 0,7125) dentro do alinhamento de alta (SMA50 0,7000 > SMA200 0,6943). O redondo 0,7200 e a máxima de 9 meses (0,7257) seguem de teto; a zona de compra 0,7000-0,7065 (SMA50 / Fib 23,6%) segue intocada por fechamento. RBA a 4,35% (atas de 20/08), WTI ~US$ 85 e dólar pressionado (DXY ~98,9). Indicadores calculados da série diária BCE/Frankfurter (526 pregões, 01/08/2024 a 24/08/2026).",
        trend="Acima das SMA50 (0,7000) e SMA200 (0,6943) — alinhamento de alta; rompimento D10 de continuação (0,7168 > 0,7125) segurado sob a máxima, com o redondo 0,7200 e a máxima de 9 meses (0,7257) acima.",
        support="0,7065 (Fib 23,6%), com a SMA50 (0,7000) abaixo.",
        resistance="0,7257 (máxima de 9 meses do avanço de 0,6445), com o redondo 0,7200 no caminho.",
        priceAction="Sem gatilho: a perseguição ao rompimento trava no teto — de 0,7168 com stop ≥42 pips (piso 1,5σ20) o alvo 0,7257 entrega ~1:2 no limite, com o redondo 0,7200 bloqueando o caminho. Gatilhos: fechamento dentro da zona 0,7000-0,7065 (R/R ≥ 3 rumo a 0,7168) ou fechamento decisivo acima de 0,7257.",
        recommendation="AGUARDAR OUTRO GATILHO",
        trigger="Nenhum — aguardar fechamento dentro da zona 0,7000-0,7065 (SMA50 / Fib 23,6%) ou fechamento decisivo acima de 0,7257.",
        stop="N/A (sem operação).",
        target="N/A (sem operação).",
        rr="N/A", rrValue=0,
        justification="O rompimento de sexta valida a tendência, mas não oferece entrada: teto a ~90 pips contra piso de stop de 42 e o redondo 0,7200 no meio do caminho. A zona intocada segue sendo o gatilho de qualidade (R/R ≥ 3); sem operação.",
    ),
    en=dict(
        fundamental="AUD/USD trades at 0.7162 on the 24/08/2026 daily close (ECB reference), essentially flat (-0.09%) under the new 10-day high: Friday (Aug 21) printed the D10 continuation breakout (0.7168 > 0.7125) within the bull alignment (50-day 0.7000 > 200-day 0.6943). The 0.7200 round and the 9-month high (0.7257) remain the cap; the 0.7000-0.7065 buying zone (50-day SMA / 23.6% Fib) remains untouched by a close. RBA at 4.35% (Aug 20 minutes), WTI ~$85 and the pressured dollar (DXY ~98.9). Indicators computed from the ECB/Frankfurter daily series (526 sessions, 01/08/2024 to 24/08/2026).",
        trend="Above the 50-day (0.7000) and 200-day (0.6943) SMAs — bull alignment; D10 continuation breakout (0.7168 > 0.7125) held under the high, with the 0.7200 round and the 9-month high (0.7257) above.",
        support="0.7065 (23.6% Fib), with the 50-day SMA (0.7000) beneath.",
        resistance="0.7257 (9-month high of the 0.6445 advance), with the 0.7200 round number in the path.",
        priceAction="No trigger: chasing the breakout runs into the cap — from 0.7168 with a stop >=42 pips (1.5-sigma20 floor) the 0.7257 target yields ~1:2 at best, with the 0.7200 round blocking the path. Triggers: a close inside the 0.7000-0.7065 zone (R/R >= 3 toward 0.7168) or a decisive close above 0.7257.",
        recommendation="WAIT FOR ANOTHER TRIGGER",
        trigger="None — wait for a close inside the 0.7000-0.7065 zone (50-day SMA / 23.6% Fib) or a decisive close above 0.7257.",
        stop="N/A (no trade).",
        target="N/A (no trade).",
        rr="N/A", rrValue=0,
        justification="Friday's breakout validates the trend but offers no entry: a cap ~90 pips away against a 42-pip stop floor and the 0.7200 round in between. The untouched zone remains the quality trigger (R/R >= 3); no trade.",
    ))

A["GBP/USD"] = dict(
    quote="1.3634", bias="ALTA", biasType="bull",
    pt=dict(
        fundamental="O GBP/USD opera em 1,3634 no fechamento diário de 24/08/2026 (referência BCE), cedendo -0,16% e assentando sobre a Fib 23,6% (1,3639) — consolidação saudável do rompimento D10 de 20/08 (1,3626 > 1,3559, estendido a 1,3656 em 21/08). A posição do ticket de 17/08 segue aberta com +75 pips (stop 1,3490 / alvo 1,3800, a ~1,2%). BoE 3,75% (6-3, próxima reunião 17/09), CPI do RU 2,6% e dólar pressionado; Jackson Hole 27-29/08 é o foco da semana para o USD. Indicadores calculados da série diária BCE/Frankfurter (526 pregões, 01/08/2024 a 24/08/2026).",
        trend="Preço acima das SMA50 (1,3394) e SMA200 (1,3419), com SMA50 ainda sob a SMA200 — regime misto resolvido para a alta pelo rompimento D10; o fechamento assenta na Fib 23,6% (1,3639), com a máxima de 9 meses (1,3817) acima.",
        support="1,3528 (Fib 38,2% reconquistada), com o redondo 1,3500 abaixo.",
        resistance="1,3817 (máxima de 9 meses), com a Fib 23,6% (1,3639) logo acima.",
        priceAction="Sem nova entrada: a máxima de 9 meses (1,3817) segue de teto — com stop estrutural sob a Fib 38,2% (1,3520, ~114 pips) o melhor alvo entrega ~1:1,6. A posição existente corre rumo ao alvo 1,3800; adição reavaliada em fechamento acima de 1,3817 (ar limpo).",
        recommendation="AGUARDAR OUTRO GATILHO",
        trigger="Nenhum — consolidação válida sobre a Fib 23,6%, mas a máxima de 9 meses trava R/R em ~1:1,6 com stop estrutural. Posição existente segue (stop 1,3490 / alvo 1,3800); adição apenas acima de 1,3817.",
        stop="N/A (sem nova operação).",
        target="N/A (sem nova operação).",
        rr="N/A", rrValue=0,
        justification="O rompimento segue intacto e a posição de 17/08 caminha para o alvo com a retração assentando no primeiro suporte. Entrada nova não passa no gate (teto a ~1,4% contra stop ~114 pips → ~1:1,6). Sem adição até novo ground.",
    ),
    en=dict(
        fundamental="GBP/USD trades at 1.3634 on the 24/08/2026 daily close (ECB reference), easing -0.16% and settling on the 23.6% Fib (1.3639) — a healthy consolidation of the Aug 20 D10 breakout (1.3626 > 1.3559, extended to 1.3656 on Aug 21). The Aug 17 ticket stays open with +75 pips (stop 1.3490 / target 1.3800, ~1.2% away). BoE 3.75% (6-3, next meeting Sep 17), UK CPI 2.6% and the pressured dollar; Jackson Hole Aug 27-29 is the week's focus for USD. Indicators computed from the ECB/Frankfurter daily series (526 sessions, 01/08/2024 to 24/08/2026).",
        trend="Price above the 50-day (1.3394) and 200-day (1.3419) SMAs, with the 50-day still below the 200-day — mixed regime resolved bullish by the D10 breakout; the close settles on the 23.6% Fib (1.3639), with the 9-month high (1.3817) above.",
        support="1.3528 (reclaimed 38.2% Fib), with the 1.3500 round beneath.",
        resistance="1.3817 (9-month high), with the 23.6% Fib (1.3639) just above.",
        priceAction="No new entry: the 9-month high (1.3817) remains the cap — with a structural stop under the 38.2% Fib (1.3520, ~114 pips) the best target yields ~1:1.6. The existing position keeps running toward 1.3800; adds reassessed on a close above 1.3817 (clean air).",
        recommendation="WAIT FOR ANOTHER TRIGGER",
        trigger="None — valid consolidation on the 23.6% Fib, but the 9-month high caps R/R at ~1:1.6 with a structural stop. Existing position stays (stop 1.3490 / target 1.3800); adds only above 1.3817.",
        stop="N/A (no new trade).",
        target="N/A (no new trade).",
        rr="N/A", rrValue=0,
        justification="The breakout stays intact and the Aug 17 position walks toward its target with the pullback settling on the first support. A fresh entry fails the gate (cap ~1.4% away against a ~114-pip stop → ~1:1.6). No adds until fresh ground.",
    ))

A["EUR/JPY"] = dict(
    quote="185.60", bias="ALTA", biasType="bull",
    pt=dict(
        fundamental="O EUR/JPY opera em 185,60 no fechamento diário de 24/08/2026 (referência BCE), estável (-0,04%) sob a máxima de 10 pregões: sexta (21/08) imprimiu novo rompimento D10 (185,66 > 185,45) com o par acima de ambas as médias (SMA50 184,74 > SMA200 183,98) — alinhamento de alta pleno, agora colado na Fib 23,6% (185,80). Mas a janela de intervenção (até ~03/09; Himino fala em 27/08, reunião do BoJ em setembro) mantém o piso 2,5σ20 (≈278 pips): stop ≤ 182,82 contra o teto da máxima de 9 meses (187,73, a ~213 pips) entrega ~1:0,8 — o gate falha. Indicadores calculados da série diária BCE/Frankfurter (526 pregões, 01/08/2024 a 24/08/2026).",
        trend="Acima das SMA50 (184,74) e SMA200 (183,98) — alinhamento de alta pleno; rompimento D10 (185,66) colado à Fib 23,6% (185,80), com a máxima de 20 dias (186,99) e a de 9 meses (187,73) acima.",
        support="184,74 (SMA50) / 183,98 (SMA200), com a Fib 50% (183,65) abaixo.",
        resistance="187,73 (máxima de 9 meses), com a Fib 23,6% (185,80) e a máxima de 20 dias (186,99) no caminho.",
        priceAction="Sem entrada — o piso de intervenção (≈278 pips) contra o teto de 187,73 trava qualquer configuração (~1:0,8). Aguardar a expiração da janela (~03/09) ou retração à zona 182,69-183,65 (Fib 61,8-50%) para comprimir o risco.",
        recommendation="AGUARDAR OUTRO GATILHO",
        trigger="Nenhum — piso de intervenção ativo até ~03/09 versus teto de 187,73 trava o R/R em ~1:0,8. Reavaliar após a janela ou em retração à zona 182,69-183,65.",
        stop="N/A (sem operação).",
        target="N/A (sem operação).",
        rr="N/A", rrValue=0,
        justification="Alinhamento de alta pleno e rompimento confirmado — mas a aritmética da intervenção não perdoa: stop de ~278 pips contra teto de ~213. Sem operação até ~03/09; a estrutura segue de alta.",
    ),
    en=dict(
        fundamental="EUR/JPY trades at 185.60 on the 24/08/2026 daily close (ECB reference), flat (-0.04%) under the 10-day high: Friday (Aug 21) printed another D10 breakout (185.66 > 185.45) with the pair above both SMAs (50-day 184.74 > 200-day 183.98) — full bull alignment, now glued to the 23.6% Fib (185.80). But the intervention window (until ~Sep 3; Himino speaks Aug 27, BoJ meeting in September) holds the 2.5-sigma20 floor (~=278 pips): a stop <= 182.82 against the 9-month-high cap (187.73, ~213 pips away) yields ~1:0.8 — the gate fails. Indicators computed from the ECB/Frankfurter daily series (526 sessions, 01/08/2024 to 24/08/2026).",
        trend="Above the 50-day (184.74) and 200-day (183.98) SMAs — full bull alignment; D10 breakout (185.66) glued to the 23.6% Fib (185.80), with the 20-day high (186.99) and the 9-month high (187.73) above.",
        support="184.74 (50-day SMA) / 183.98 (200-day SMA), with the 50% Fib (183.65) beneath.",
        resistance="187.73 (9-month high), with the 23.6% Fib (185.80) and the 20-day high (186.99) in the path.",
        priceAction="No entry — the intervention floor (~=278 pips) against the 187.73 cap blocks any configuration (~1:0.8). Wait for the window to expire (~Sep 3) or a pullback to the 182.69-183.65 zone (61.8-50% Fib) to compress risk.",
        recommendation="WAIT FOR ANOTHER TRIGGER",
        trigger="None — intervention floor active until ~Sep 3 versus the 187.73 cap locks R/R at ~1:0.8. Reassess after the window or on a pullback to 182.69-183.65.",
        stop="N/A (no trade).",
        target="N/A (no trade).",
        rr="N/A", rrValue=0,
        justification="Full bull alignment and a confirmed breakout — but the intervention arithmetic is unforgiving: a ~278-pip stop against a ~213-pip cap. No trade until ~Sep 3; the structure stays bullish.",
    ))

A["GBP/JPY"] = dict(
    quote="216.95", bias="ALTA", biasType="bull",
    pt=dict(
        fundamental="O GBP/JPY opera em 216,95 no fechamento diário de 24/08/2026 (referência BCE), avançando +0,11% e fechando além da máxima de 10 pregões (216,72) — novo rompimento D10 com a posição do ticket de 14/08 (entrada 215,90, stop 213,90, alvo 219,00) aberta com +105 pips e o alvo a ~0,95%, colado à máxima de 9 meses (219,14). O piso de intervenção 2,5σ20 (≈320 pips) segue ativo até ~03/09 (Himino em 27/08) e mantém adições em R/R <1 — a máxima de 9 meses trava qualquer configuração nova. Indicadores calculados da série diária BCE/Frankfurter (526 pregões, 01/08/2024 a 24/08/2026).",
        trend="Acima das SMA50 (215,65) e SMA200 (212,34) — alinhamento de alta; rompimento D10 (216,95 > 216,72) com a máxima de 20 dias (218,15) e a de 9 meses (219,14) acima — o alvo do ticket quase colado à máxima.",
        support="215,57 (Fib 23,6%), com a Fib 38,2% (213,35) e o redondo 213,00 abaixo.",
        resistance="219,14 (máxima de 9 meses), com a máxima de 20 dias (218,15) no caminho.",
        priceAction="Sem nova entrada — o alvo do ticket (219,00) está a ~0,95% e colado à máxima de 9 meses; gerenciar a posição existente (stop 213,90 / alvo 219,00) e reavaliar adições apenas após fechamento acima de 219,14 (~03/09 ou novo ground).",
        recommendation="AGUARDAR OUTRO GATILHO",
        trigger="Nenhum — piso de intervenção ativo até ~03/09 e teto de 219,14 colado ao alvo do ticket. Posição existente segue (stop 213,90 / alvo 219,00); adição apenas acima de 219,14.",
        stop="N/A (sem nova operação).",
        target="N/A (sem nova operação).",
        rr="N/A", rrValue=0,
        justification="A posição legada entra na reta final com a estrutura de alta inteira a favor — mas adições seguem bloqueadas pelo piso de intervenção e pelo teto de 219,14 colado ao alvo. Gerenciar e colher.",
    ),
    en=dict(
        fundamental="GBP/JPY trades at 216.95 on the 24/08/2026 daily close (ECB reference), up +0.11% and closing beyond the 10-day high (216.72) — a fresh D10 breakout with the Aug 14 ticket's position (entry 215.90, stop 213.90, target 219.00) open with +105 pips and the target ~0.95% away, glued to the 9-month high (219.14). The 2.5-sigma20 intervention floor (~=320 pips) remains active until ~Sep 3 (Himino Aug 27) and keeps adds below R/R 1 — the 9-month high caps any new configuration. Indicators computed from the ECB/Frankfurter daily series (526 sessions, 01/08/2024 to 24/08/2026).",
        trend="Above the 50-day (215.65) and 200-day (212.34) SMAs — bull alignment; D10 breakout (216.95 > 216.72) with the 20-day high (218.15) and the 9-month high (219.14) above — the ticket's target almost glued to the high.",
        support="215.57 (23.6% Fib), with the 38.2% Fib (213.35) and the 213.00 round beneath.",
        resistance="219.14 (9-month high), with the 20-day high (218.15) in the path.",
        priceAction="No new entry — the ticket's target (219.00) is ~0.95% away and glued to the 9-month high; manage the existing position (stop 213.90 / target 219.00) and reassess adds only after a close above 219.14 (~Sep 3 or fresh ground).",
        recommendation="WAIT FOR ANOTHER TRIGGER",
        trigger="None — intervention floor active until ~Sep 3 and the 219.14 cap glued to the ticket's target. Existing position stays (stop 213.90 / target 219.00); adds only above 219.14.",
        stop="N/A (no new trade).",
        target="N/A (no new trade).",
        rr="N/A", rrValue=0,
        justification="The legacy position enters the home stretch with the entire bull structure behind it — but adds stay blocked by the intervention floor and the 219.14 cap glued to the target. Manage and harvest.",
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

# dashboard default badge already WAIT — no verdict swap needed
m = re.search(r'(id="generationTime"[^>]*>Reports generated on: )[^<]*(</p>)', idx)
if not m:
    sys.exit("ERROR: generationTime not found")
idx = idx[:m.start()] + m.group(1) + TS + m.group(2) + idx[m.end():]
if idx.count(OLD_TS) != 2:
    sys.exit(f"ERROR: expected 2 old timestamps, found {idx.count(OLD_TS)}")
idx = idx.replace(OLD_TS, TS)

old_changes = '''        const dailyChanges = {
            "EUR/USD": "+0.66%",
            "USD/JPY": "-0.21%",
            "AUD/USD": "+0.43%",
            "GBP/USD": "+0.52%",
            "EUR/JPY": "+0.45%",
            "GBP/JPY": "+0.31%"
        };'''
new_changes = '''        const dailyChanges = {
            "EUR/USD": "-0.30%",
            "USD/JPY": "+0.27%",
            "AUD/USD": "-0.09%",
            "GBP/USD": "-0.16%",
            "EUR/JPY": "-0.04%",
            "GBP/JPY": "+0.11%"
        };'''
idx = rep(idx, old_changes, new_changes, "ticker")
old_be = 'dataBasis: "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 524 daily sessions (01/08/2024–20/08/2026).",'
new_be = 'dataBasis: "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 526 daily sessions (01/08/2024–24/08/2026).",'
old_bp = 'dataBasis: "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, sigma20 e Donchian calculados · 524 pregões (01/08/2024 a 20/08/2026).",'
new_bp = 'dataBasis: "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, sigma20 e Donchian calculados · 526 pregões (01/08/2024 a 24/08/2026).",'
idx = rep(idx, old_be, new_be, "dataBasis EN")
idx = rep(idx, old_bp, new_bp, "dataBasis PT")

with open(IDX, "w", encoding="utf-8") as f:
    f.write(idx)
print("OK: index.html")

# ---------------- static pages ----------------
GAUGE = {"EUR/USD": 9, "USD/JPY": 64, "AUD/USD": 51, "GBP/USD": 37, "EUR/JPY": 29, "GBP/JPY": 39}
OLD_GAUGE = {"EUR/USD": 32, "USD/JPY": 37, "AUD/USD": 21, "GBP/USD": 34, "EUR/JPY": 24, "GBP/JPY": 28}
# conviction stays 0/10 everywhere (all WAIT); verdicts/biases unchanged (all wait/bull)

BLUF = {  # (old_inner, new_inner) swaps on the BLUF line
 "EUR/USD": [('<span class="bluf-action wait">WAIT</span> — zone broken to the upside; 1.1732 clearance needed</span>',
              '<span class="bluf-action wait">WAIT</span> — breakout pullback holds above 1.1657; 1.1732 clearance still needed</span>'),
             ('<span class="bluf-action wait">AGUARDAR</span> — zona rompida para cima; falta fechar acima de 1.1732</span>',
              '<span class="bluf-action wait">AGUARDAR</span> — retração preserva o rompimento acima de 1.1657; falta fechar acima de 1.1732</span>')],
 "USD/JPY": [('<span class="bluf-action wait">WAIT</span> — pullback nearing the 158.19-158.27 zone; floor until ~03/09</span>',
              '<span class="bluf-action wait">WAIT</span> — pullback rejected above the zone; floor until ~03/09</span>'),
             ('<span class="bluf-action wait">AGUARDAR</span> — retração aproximando da zona 158.19-158.27; piso até ~03/09</span>',
              '<span class="bluf-action wait">AGUARDAR</span> — retração rejeitada acima da zona; piso até ~03/09</span>')],
 "AUD/USD": [('<span class="bluf-action wait">WAIT</span> — zone 0.6990-0.7065 still untouched by close</span>',
              '<span class="bluf-action wait">WAIT</span> — D10 continuation Friday; 9-month high caps; zone 0.7000-0.7065 still valid</span>'),
             ('<span class="bluf-action wait">AGUARDAR</span> — zona 0.6990-0.7065 segue intocada por fechamento</span>',
              '<span class="bluf-action wait">AGUARDAR</span> — rompimento D10 na sexta; máxima de 9 meses trava; zona 0.7000-0.7065 segue válida</span>')],
 "GBP/USD": [('<span class="bluf-action wait">WAIT</span> — breakout resolved bullish; 9-month high caps R/R; position open</span>',
              '<span class="bluf-action wait">WAIT</span> — position +75 pips toward 1.3800; adds only above 1.3817</span>'),
             ('<span class="bluf-action wait">AGUARDAR</span> — rompimento resolveu para alta; máxima de 9 meses trava R/R; posição aberta</span>',
              '<span class="bluf-action wait">AGUARDAR</span> — posição +75 pips rumo a 1.3800; adição só acima de 1.3817</span>')],
 "EUR/JPY": [('<span class="bluf-action wait">WAIT</span> </span>',
              '<span class="bluf-action wait">WAIT</span> — intervention floor vs 187.73 cap (~1:0.8); window to ~03/09</span>'),
             ('<span class="bluf-action wait">AGUARDAR</span> </span>',
              '<span class="bluf-action wait">AGUARDAR</span> — piso de intervenção vs teto 187,73 (~1:0,8); janela até ~03/09</span>')],
 "GBP/JPY": [('<span class="bluf-action wait">WAIT</span> — position nearing the 219.00 target; floor until ~03/09</span>',
              '<span class="bluf-action wait">WAIT</span> — new D10 close; position +105 pips, target ~0.95% away</span>'),
             ('<span class="bluf-action wait">AGUARDAR</span> — posição aproximando do alvo 219.00; piso até ~03/09</span>',
              '<span class="bluf-action wait">AGUARDAR</span> — novo rompimento D10; posição +105 pips, alvo a ~0,95%</span>')],
}

NEXT_EVENT = {  # (old EN, new EN, old PT, new PT)
 "EUR/USD": ("US CPI &amp; Fed speakers", "Jackson Hole Aug 27-29",
             "CPI dos EUA &amp; discursos do Fed", "Jackson Hole 27-29/08"),
 "USD/JPY": ("US CPI &amp; Fed speakers", "Jackson Hole &amp; BoJ speakers",
             "CPI dos EUA &amp; discursos do Fed", "Jackson Hole e discursos do BoJ"),
 "AUD/USD": ("US CPI &amp; Fed speakers", "Jackson Hole &amp; RBA speakers",
             "CPI dos EUA &amp; discursos do Fed", "Jackson Hole e RBA"),
 "GBP/USD": ("US CPI &amp; Fed speakers", "Jackson Hole Aug 27-29",
             "CPI dos EUA &amp; discursos do Fed", "Jackson Hole 27-29/08"),
 "EUR/JPY": ("US CPI &amp; Fed speakers", "Jackson Hole &amp; BoJ speakers",
             "CPI dos EUA &amp; discursos do Fed", "Jackson Hole e discursos do BoJ"),
 "GBP/JPY": ("US CPI &amp; Fed speakers", "Jackson Hole &amp; BoJ speakers",
             "CPI dos EUA &amp; discursos do Fed", "Jackson Hole e discursos do BoJ"),
}

GAUGE_LABELS = {  # (old now-label, new now-label, [(side, old, new), ...])
 "EUR/USD": ("1.1567", "1.1664", [("l", "1.1476", "1.1657"), ("r", "1.1582", "1.1732")]),
 "USD/JPY": ("159.01", "159.12", [("l", "158.3", "158.27"), ("r", "159.6", "159.60")]),
 "AUD/USD": ("0.7082", "0.7162", [("l", "0.6947", "0.7065")]),  # rgv-r 0.7257 unchanged
 "GBP/USD": ("1.3537", "1.3634", [("l", "1.3439", "1.3528"), ("r", "1.3639", "1.3817")]),
 "EUR/JPY": ("183.93", "185.60", [("l", "182.4", "184.74"), ("r", "184.8", "187.73")]),
 "GBP/JPY": ("215.24", "216.95", [("l", "212.2", "215.57"), ("r", "215.4", "219.14")]),
}

for pair, fname in PAGE.items():
    path = f"{DOCS}/{fname}"
    with open(path, encoding="utf-8") as f:
        h = f.read()
    od, nd = old_data[pair], A[pair]
    # 1) BLUF inner text
    for old, new in BLUF[pair]:
        h = rep(h, old, new, f"{fname} BLUF")
    # 2) fix stale bias-badge class on eur-usd (left bear after the 20/08 flip)
    if pair == "EUR/USD":
        h = rep(h, '<div class="bias-badge bias-bear">', '<div class="bias-badge bias-bull">', f"{fname} badge fix")
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
    # 3b) rr — unchanged (N/A) everywhere
    # 4) quote strong
    h = rep(h, f'<strong>{od["quote"]}</strong>', f'<strong>{nd["quote"]}</strong>', f"{fname} quote strong")
    # 5) gauge position (now + marker)
    h = rep(h, f'left: {OLD_GAUGE[pair]}%', f'left: {GAUGE[pair]}%', f"{fname} gauge", 2)
    # 5b) gauge text labels (stale since 14/08)
    old_now, new_now, rgv_swaps = GAUGE_LABELS[pair]
    h = rep(h, f'>{old_now}</div>', f'>{new_now}</div>', f"{fname} gauge now-label")
    for side, old_rgv, new_rgv in rgv_swaps:
        h = rep(h, f'<span class="rgv-{side}">{old_rgv}</span>', f'<span class="rgv-{side}">{new_rgv}</span>', f"{fname} rgv-{side}")
    # 6) next-event line
    oen, nen, opt_, npt = NEXT_EVENT[pair]
    h = rep(h, f'<span class="lang-en">{oen}</span>', f'<span class="lang-en">{nen}</span>', f"{fname} next-event EN")
    h = rep(h, f'<span class="lang-pt" style="display:none;">{opt_}</span>', f'<span class="lang-pt" style="display:none;">{npt}</span>', f"{fname} next-event PT")
    with open(path, "w", encoding="utf-8") as f:
        f.write(h)
    print(f"OK: {fname} ({pair})")

# pages' data-basis lines + AUD WTI chip refresh
for fname in PAGE.values():
    p = f"{DOCS}/{fname}"
    with open(p, encoding="utf-8") as f:
        h = f.read()
    oen = "ECB/Frankfurter reference rates · SMA50/200, sigma20 &amp; Donchian computed · 524 daily sessions (01/08/2024–20/08/2026)."
    nen = "ECB/Frankfurter reference rates · SMA50/200, sigma20 &amp; Donchian computed · 526 daily sessions (01/08/2024–24/08/2026)."
    opt = "taxas de referência BCE/Frankfurter · SMA50/200, sigma20 e Donchian calculados · 524 pregões (01/08/2024 a 20/08/2026)."
    npt = "taxas de referência BCE/Frankfurter · SMA50/200, sigma20 e Donchian calculados · 526 pregões (01/08/2024 a 24/08/2026)."
    h = rep(h, oen, nen, f"{fname} basis EN")
    h = rep(h, opt, npt, f"{fname} basis PT")
    if fname == "aud-usd.html":
        h = rep(h, 'WTI $82', 'WTI $85', f"{fname} WTI chips", 2)
    with open(p, "w", encoding="utf-8") as f:
        f.write(h)
print("OK: 6 pages data-basis")

# ---------------- track-record ledger ----------------
LED = DOCS + "/track-record.json"
with open(LED, encoding="utf-8") as f:
    led = f.read()
led = rep(led, '"lastUpdated": "20/08/2026"', '"lastUpdated": "24/08/2026"', "ledger lastUpdated")
led = rep(led, '"note": "legacy 14/08 ticket: 20/08 close 216.33 (+43 pips), target 219.00 ~1.2% away"',
          '"note": "legacy 14/08 ticket: 24/08 close 216.95 (+105 pips), fresh D10 close; target 219.00 ~0.95% away"',
          "ledger GBP/JPY note")
led = rep(led, '"note": "20/08 close 1.3626 (+67 pips); D10 breakout resolved the regime bullish; target 1.3800 ~1.4% away"',
          '"note": "24/08 close 1.3634 (+75 pips); consolidating on the 23.6% Fib; target 1.3800 ~1.2% away"',
          "ledger GBP/USD note")
json.loads(led)  # validate
with open(LED, "w", encoding="utf-8") as f:
    f.write(led)
print("OK: track-record.json (no resolutions; both open tickets annotated; watching stays empty)")

print("\nDONE: run verify_all.py next.")
