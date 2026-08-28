#!/usr/bin/env python3
"""28/08/2026 daily report build. Data basis: Frankfurter/ECB, 530 sessions
01/08/2024-28/08/2026 (compute_indicators.py run of 28/08/2026).
Jackson Hole week — Warsh's keynote (28/08, 10:00 ET) landed hawkish (hike
bets up, yields up, DXY ~99.2) but AFTER the ~13:15 UTC ECB snapshot, so the
reaction prices in from Monday 31/08. All verdicts WAIT, all biases ALTA:
- EUR/USD: week-long drift to 1.1643; the last two closes slipped under the
  50% Fib (1.1657) — pullback pressing the SMA200 (1.1629) / 1.1625 floor;
  1.1700-1.1732 cap intact; event window today (no new USD entries).
- USD/JPY: ground up to 159.68, reclaiming the 38.2% Fib, 2 pips under the
  10-day high; zone 158.25-158.27 untouched; intervention floor (~224 pips)
  until ~03/09 still fails the gate (best R/R ~1:1.9).
- AUD/USD: D10 continuation extended on 26/08 (0.7185 > 0.7168); Friday 5
  pips under 0.7200, ~62 pips under the 9-mo high; chase ~1:1.4. WAIT.
- GBP/USD: pullback deepened 27/08 (-0.35%); closes under the 23.6% Fib,
  56 pips above the 1.3538/1.3500 zone; position +24 pips; both open
  tickets hit the 10-session expiry check on Monday's run.
- EUR/JPY: fresh 10-day high close 185.91 glued to the 23.6% Fib; floor
  2.5-sigma20 (~217 pips) vs the 187.73 cap (~182) ~1:0.8. WAIT.
- GBP/JPY: week's high 217.07 (25/08) then a shallow dip; position +99
  pips, target 219.00 ~0.97% away; floor until ~03/09. WAIT.
Ledger: no resolutions (both open tickets annotated at 9/10 sessions);
watching stays empty."""
import json, re, sys

DOCS = r"C:/Projetos/forex-report/docs"
IDX = DOCS + "/index.html"
TS = "28/08/2026 22:05 UTC"
OLD_TS = "24/08/2026 18:35 UTC"
PAGE = {
    "EUR/USD": "eur-usd.html", "USD/JPY": "usd-jpy.html", "AUD/USD": "aud-usd.html",
    "GBP/USD": "gbp-usd.html", "EUR/JPY": "eur-jpy.html", "GBP/JPY": "gbp-jpy.html",
}

A = {}
A["EUR/USD"] = dict(
    quote="1.1643", bias="ALTA", biasType="bull",
    pt=dict(
        fundamental="O EUR/USD opera em 1,1643 no fechamento diário de 28/08/2026 (referência BCE), estável (-0,02%) e encerrando a semana em deriva lenta (1,1664 → 1,1643): os dois últimos fechamentos escorregaram sob a Fib 50% (1.1657) pela primeira vez desde o rompimento — a retração agora pressiona a SMA200 (1.1629) e o piso 1.1625, que delimitam a validade do rompimento de 20/08. A σ20 comprimiu a 28 pips, a menor da fase. Jackson Hole: o keynote de Warsh (28/08, 10h ET) soou hawkish — apostas em ALTA de juros subiram, yields subiram, DXY ~99,2 — mas o discurso saiu DEPOIS do snapshot do BCE (~13:15 UTC): a reação começa a ser preciosada na segunda (31/08). Janela de eventos hoje: sem novas entradas; reavaliar após o evento. Perder 1.1625 devolve a zona à disputa. Indicadores (SMA 50/200, σ20, Donchian e Fibonacci) calculados da série diária BCE/Frankfurter (530 pregões, 01/08/2024 a 28/08/2026).",
        trend="Preço acima da SMA200 (1.1629) com SMA50 (1.1484) ainda abaixo — regime misto resolvido para a alta pelo rompimento D10 de 20/08; a retração devolveu a Fib 50% (1.1657) à condição de resistência imediata, com a confluência 1.1700-1.1732 (redondo / Fib 38,2%) acima.",
        support="1.1629 (SMA200) / 1.1625 (piso da zona do rompimento), com a mínima de 10 pregões (1.1576) abaixo.",
        resistance="1.1657 (Fib 50%) devolvida a resistência imediata, com a confluência 1.1700-1.1732 (redondo / Fib 38,2%) e a máxima de 9 meses (1.1974) acima.",
        priceAction="Sem entrada — janela de eventos (keynote de hoje) e retração sem fechamento de tendência: o gatilho segue sendo fechamento acima de 1.1732 (abre 1.1824-1.1974); do lado da perda, fechamento sob 1.1625 invalida a resolução de alta e devolve o regime ao misto. Na segunda, reavaliar com a reação a Jackson Hole preciada.",
        recommendation="AGUARDAR OUTRO GATILHO",
        trigger="Nenhum — janela de eventos (Jackson Hole hoje) e retração sem fechamento de tendência. Aguardar fechamento acima de 1.1732 para mirar 1.1824-1.1974; fechamento sob 1.1625 devolve a zona à disputa.",
        stop="N/A (sem operação).",
        target="N/A (sem operação).",
        rr="N/A", rrValue=0,
        justification="A retração fez o que retrações fazem — devolveu a Fib 50% e está testando a retenção da SMA200 — mas sem fechamento de tendência fora da zona não há gatilho mecânico, e o keynote hawkish de Warsh só entra no preço na segunda. Disciplina: esperar a segunda com os níveis 1.1625 e 1.1732 marcando o campo.",
    ),
    en=dict(
        fundamental="EUR/USD trades at 1.1643 on the 28/08/2026 daily close (ECB reference), flat (-0.02%) and ending the week in a slow drift (1.1664 → 1.1643): the last two closes slipped under the 50% Fib (1.1657) for the first time since the breakout — the pullback now presses the 200-day SMA (1.1629) and the 1.1625 floor that delimit the Aug 20 breakout's validity. Sigma20 compressed to 28 pips, the tightest of the phase. Jackson Hole: Warsh's keynote (Aug 28, 10am ET) landed hawkish — rate-hike bets rose, yields rose, DXY ~99.2 — but the speech came AFTER the ECB snapshot (~13:15 UTC): the reaction starts pricing on Monday (Aug 31). Event window today: no new entries; reassess after the event. Losing 1.1625 returns the zone to dispute. Indicators (SMA 50/200, sigma20, Donchian, Fibonacci) computed from the ECB/Frankfurter daily series (530 sessions, 01/08/2024 to 28/08/2026).",
        trend="Price above the 200-day SMA (1.1629) with the 50-day (1.1484) still below — mixed regime resolved bullish by the Aug 20 D10 breakout; the pullback returns the 50% Fib (1.1657) to immediate resistance, with the 1.1700-1.1732 confluence (round / 38.2% Fib) above.",
        support="1.1629 (200-day SMA) / 1.1625 (breakout zone floor), with the 10-day low (1.1576) beneath.",
        resistance="1.1657 (50% Fib) back as immediate resistance, with the 1.1700-1.1732 confluence (round / 38.2% Fib) and the 9-month high (1.1974) above.",
        priceAction="No entry — event window (today's keynote) and a pullback with no trend-direction close: the trigger remains a close above 1.1732 (opens 1.1824-1.1974); on the loss side, a close under 1.1625 invalidates the bullish resolution and returns the regime to mixed. On Monday, reassess with the Jackson Hole reaction priced.",
        recommendation="WAIT FOR ANOTHER TRIGGER",
        trigger="None — event window (Jackson Hole today) and a pullback with no trend-direction close. Wait for a close above 1.1732 to target 1.1824-1.1974; a close under 1.1625 returns the zone to dispute.",
        stop="N/A (no trade).",
        target="N/A (no trade).",
        rr="N/A", rrValue=0,
        justification="The pullback did what pullbacks do — handed back the 50% Fib and is testing the 200-day's retention — but with no trend-direction close away from the zone there is no mechanical trigger, and Warsh's hawkish keynote only enters the price on Monday. Discipline: wait for Monday with the 1.1625 and 1.1732 levels marking the field.",
    ))

A["USD/JPY"] = dict(
    quote="159.68", bias="ALTA", biasType="bull",
    pt=dict(
        fundamental="O USD/JPY opera em 159,68 no fechamento diário de 28/08/2026 (referência BCE), subindo +0,18% e encerrando a semana em cinco alta-dias em seis: o par reconquistou a Fib 38,2% (159,60) e parou a 2 pips da máxima de 10 pregões (159,70). A zona de compra 158,25-158,27 (SMA200 / Fib 50%) segue intocada por fechamento — a retração parou em 158,70. O keynote hawkish de Warsh reabre o diferencial Fed-BoJ (suporte ao par), mas a janela de intervenção (até ~03/09) mantém o piso 2,5σ20 (≈224 pips): até um rompimento D10 acima de 159,70 entrega só ~1:1,9 rumo à máxima de 9 meses (163,91) — o gate falha. Indicadores calculados da série diária BCE/Frankfurter (530 pregões, 01/08/2024 a 28/08/2026).",
        trend="Acima da SMA200 (158,35) e abaixo da SMA50 (160,91) — alinhamento de alta; a pressão de compra recuperou a Fib 38,2% (159,60) e cola o par na máxima de 10 pregões (159,70), com a confluência SMA50 / Fib 23,6% (160,91-161,25) acima.",
        support="158,27 (Fib 50%) / 158,25 (SMA200), com a Fib 38,2% (159,60) recuperada como primeiro degrau.",
        resistance="161,02 (SMA50) / 161,25 (Fib 23,6%), com a máxima de 10 pregões (159,70) no caminho.",
        priceAction="Sem gatilho: nem a retração (zona intocada) nem o rompimento passam no gate enquanto o piso de intervenção (2,5σ20 ≈ 224 pips) estiver ativo — do fecho atual, mesmo mirando a máxima de 9 meses (163,91) o R/R não chega a 1:2. Reavaliar após ~03/09 (expiração da janela) ou em fechamento dentro da zona com σ20 comprimida.",
        recommendation="AGUARDAR OUTRO GATILHO",
        trigger="Nenhum — piso de intervenção ativo até ~03/09. Reavaliar quando a janela expirar ou após fechamento dentro da zona 158,25-158,27 com compressão de σ20.",
        stop="N/A (sem operação).",
        target="N/A (sem operação).",
        rr="N/A", rrValue=0,
        justification="O desenho de alta segue — compressão de σ20 (106 → 90 pips), reconquista da Fib 38,2% e cola na máxima de 10 dias — mas a aritmética da intervenção ainda bloqueia qualquer entrada. O keynote hawkish ajuda o par e ajuda o risco de jawboning; a janela envelhece em ~03/09.",
    ),
    en=dict(
        fundamental="USD/JPY trades at 159.68 on the 28/08/2026 daily close (ECB reference), up +0.18% and closing the week with five up-days in six: the pair reclaimed the 38.2% Fib (159.60) and stopped 2 pips under the 10-day high (159.70). The 158.25-158.27 buying zone (200-day SMA / 50% Fib) remains untouched by a close — the pullback bottomed at 158.70. Warsh's hawkish keynote reopens the Fed-BoJ differential (pair-supportive), but the intervention window (until ~Sep 3) holds the 2.5-sigma20 floor (~=224 pips): even a D10 breakout above 159.70 yields only ~1:1.9 toward the 9-month high (163.91) — the gate fails. Indicators computed from the ECB/Frankfurter daily series (530 sessions, 01/08/2024 to 28/08/2026).",
        trend="Above the 200-day SMA (158.35) and below the 50-day (160.91) — bull alignment; the bid reclaimed the 38.2% Fib (159.60) and glues the pair to the 10-day high (159.70), with the 50-day SMA / 23.6% Fib confluence (160.91-161.25) above.",
        support="158.27 (50% Fib) / 158.25 (200-day SMA), with the reclaimed 38.2% Fib (159.60) as the first step.",
        resistance="161.02 (50-day SMA) / 161.25 (23.6% Fib), with the 10-day high (159.70) in the path.",
        priceAction="No trigger: neither the pullback (zone untouched) nor the breakout passes the gate while the intervention floor (2.5-sigma20 ~= 224 pips) is active — from the current close, even targeting the 9-month high (163.91) the R/R stays under 1:2. Reassess after ~Sep 3 (window expiry) or on a close inside the zone with compressed sigma20.",
        recommendation="WAIT FOR ANOTHER TRIGGER",
        trigger="None — intervention floor active until ~Sep 3. Reassess when the window expires or after a close inside the 158.25-158.27 zone with sigma20 compression.",
        stop="N/A (no trade).",
        target="N/A (no trade).",
        rr="N/A", rrValue=0,
        justification="The bull blueprint holds — sigma20 compression (106 → 90 pips), the 38.2% Fib reclaimed and the pair glued to the 10-day high — but the intervention arithmetic still blocks any entry. The hawkish keynote helps the pair and helps the jawboning risk; the window ages out ~Sep 3.",
    ))

A["AUD/USD"] = dict(
    quote="0.7195", bias="ALTA", biasType="bull",
    pt=dict(
        fundamental="O AUD/USD opera em 0,7195 no fechamento diário de 28/08/2026 (referência BCE), subindo +0,07% e completando três fechamentos consecutivos em expansão do rompimento: 26/08 (0,7185) superou a antiga máxima de 10 pregões (0,7168) — continuação D10 confirmada dentro do alinhamento de alta (SMA50 0,7011 > SMA200 0,6956). O fechamento parou a 5 pips do redondo 0,7200 e a ~62 pips da máxima de 9 meses (0,7257); a zona de compra 0,7000-0,7065 (SMA50 / Fib 23,6%) segue intocada. RBA a 4,35%; WTI recuou ~4-5% na semana (~US$ 83) e o dólar reagiu hawkish a Jackson Hole — ventos mistos no curto prazo. Indicadores calculados da série diária BCE/Frankfurter (530 pregões, 01/08/2024 a 28/08/2026).",
        trend="Acima das SMA50 (0,7011) e SMA200 (0,6956) — alinhamento de alta; continuação D10 (0,7185 > 0,7168) com o redondo 0,7200 e a máxima de 9 meses (0,7257) como tetos imediatos.",
        support="0.7168 (base do rompimento de 21/08), com a SMA50 (0.7011) e a Fib 23,6% (0.7065) abaixo.",
        resistance="0.7257 (máxima de 9 meses do avanço de 0,6445), com o redondo 0,7200 no caminho.",
        priceAction="Sem gatilho: a perseguição segue travada — de 0,7195 com stop estrutural sob a base do rompimento (0,7152, ~43 pips ≥ piso de 36) o teto 0,7257 entrega ~1:1,4. Gatilhos: fechamento dentro da zona 0,7000-0,7065 (R/R ≥ 3) ou fechamento decisivo acima de 0,7257.",
        recommendation="AGUARDAR OUTRO GATILHO",
        trigger="Nenhum — aguardar fechamento dentro da zona 0,7000-0,7065 (SMA50 / Fib 23,6%) ou fechamento decisivo acima de 0,7257.",
        stop="N/A (sem operação).",
        target="N/A (sem operação).",
        rr="N/A", rrValue=0,
        justification="A continuação imprimiu e respeitou os tetos — o mercado está a 5 pips do redondo 0,7200 sem força para atravessá-lo na semana. Com teto duplo (0,7200/0,7257) a ~62 pips e o piso de stop em 36, a matemática não fecha 1:2; a zona intocada segue sendo o único gatilho de qualidade.",
    ),
    en=dict(
        fundamental="AUD/USD trades at 0.7195 on the 28/08/2026 daily close (ECB reference), up +0.07% and completing a third consecutive higher close expanding the breakout: Aug 26 (0.7185) took out the former 10-day high (0.7168) — D10 continuation confirmed within the bull alignment (50-day 0.7011 > 200-day 0.6956). The close stopped 5 pips under the 0.7200 round and ~62 pips under the 9-month high (0.7257); the 0.7000-0.7065 buying zone (50-day SMA / 23.6% Fib) remains untouched. RBA at 4.35%; WTI fell ~4-5% on the week (~$83) and the dollar turned hawkish on Jackson Hole — mixed short-term headwinds. Indicators computed from the ECB/Frankfurter daily series (530 sessions, 01/08/2024 to 28/08/2026).",
        trend="Above the 50-day (0.7011) and 200-day (0.6956) SMAs — bull alignment; D10 continuation (0.7185 > 0.7168) with the 0.7200 round and the 9-month high (0.7257) as the immediate caps.",
        support="0.7168 (Aug 21 breakout base), with the 50-day SMA (0.7011) and the 23.6% Fib (0.7065) beneath.",
        resistance="0.7257 (9-month high of the 0.6445 advance), with the 0.7200 round number in the path.",
        priceAction="No trigger: the chase stays capped — from 0.7195 with a structural stop under the breakout base (0.7152, ~43 pips >= the 36-pip floor) the 0.7257 cap yields ~1:1.4. Triggers: a close inside the 0.7000-0.7065 zone (R/R >= 3) or a decisive close above 0.7257.",
        recommendation="WAIT FOR ANOTHER TRIGGER",
        trigger="None — wait for a close inside the 0.7000-0.7065 zone (50-day SMA / 23.6% Fib) or a decisive close above 0.7257.",
        stop="N/A (no trade).",
        target="N/A (no trade).",
        rr="N/A", rrValue=0,
        justification="The continuation printed and respected the caps — the market sits 5 pips under the 0.7200 round without the strength to cross it this week. With a double cap (0.7200/0.7257) ~62 pips away and a 36-pip stop floor, the math doesn't close 1:2; the untouched zone remains the only quality trigger.",
    ))

A["GBP/USD"] = dict(
    quote="1.3583", bias="ALTA", biasType="bull",
    pt=dict(
        fundamental="O GBP/USD opera em 1,3583 no fechamento diário de 28/08/2026 (referência BCE), flat (+0,01%) após a retração ter se aprofundado em 27/08 (-0,35%): os fechamentos devolveram a Fib 23,6% (1.3644) e o par assenta 56 pips acima da zona 1.3500-1.3538 (redondo / Fib 38,2%), ainda com a SMA200 (1.3428) intacta abaixo. A posição do ticket de 17/08 segue aberta com +24 pips (stop 1,3490 / alvo 1,3800) — e completa a 10ª sessão na segunda (31/08): sem cruzamento de alvo ou stop até lá, o ticket expira por tempo. Warsh soou hawkish em Jackson Hole (vento contrário ao GBP via dólar); BoE 3,75% (6-3, próxima reunião 17/09). Janela de eventos hoje: sem novas entradas. Indicadores calculados da série diária BCE/Frankfurter (530 pregões, 01/08/2024 a 28/08/2026).",
        trend="Preço acima das SMA50 (1.3417) e SMA200 (1.3428), com SMA50 ainda sob a SMA200 — regime misto resolvido para a alta pelo rompimento D10 de 20/08; a retração devolveu a Fib 23,6% (1.3644) a resistência, com a máxima de 9 meses (1.3817) acima.",
        support="1.3538 (Fib 38,2%), com o redondo 1.3500 abaixo.",
        resistance="1.3817 (máxima de 9 meses), com a Fib 23,6% (1.3644) devolvida a resistência.",
        priceAction="Sem nova entrada — janela de eventos (Jackson Hole hoje) e retração ainda sem toque na zona: gatilhos pós-evento são (a) toque na zona 1.3500-1.3538 seguido de fechamento de tendência acima do midpoint, ou (b) fechamento de reconquista acima de 1.3644. A posição existente segue (stop 1.3490 / alvo 1.3800), com checagem de expiração na segunda.",
        recommendation="AGUARDAR OUTRO GATILHO",
        trigger="Nenhum — janela de eventos e retração sem toque na zona 1.3500-1.3538. Pós-evento: toque na zona + fechamento de tendência, ou reconquista acima de 1.3644. Posição existente segue (stop 1.3490 / alvo 1.3800); expiração checada na segunda (31/08).",
        stop="N/A (sem nova operação).",
        target="N/A (sem nova operação).",
        rr="N/A", rrValue=0,
        justification="A retração se aprofundou e agora testa se a zona de 1,35 resiste — o campo fica entre o redondo 1.3500 e a reconquista de 1.3644, com Warsh hawkish pesando contra via dólar. Sem gatilho mecânico hoje; a posição de 17/08 segue gerenciada e a segunda decide a expiração.",
    ),
    en=dict(
        fundamental="GBP/USD trades at 1.3583 on the 28/08/2026 daily close (ECB reference), flat (+0.01%) after the pullback deepened on Aug 27 (-0.35%): closes handed back the 23.6% Fib (1.3644) and the pair settles 56 pips above the 1.3500-1.3538 zone (round / 38.2% Fib), with the 200-day SMA (1.3428) still intact beneath. The Aug 17 ticket stays open with +24 pips (stop 1.3490 / target 1.3800) — and it completes its 10th session on Monday (Aug 31): with no target or stop close-crossed by then, the ticket expires on time. Warsh sounded hawkish at Jackson Hole (a GBP headwind via the dollar); BoE 3.75% (6-3, next meeting Sep 17). Event window today: no new entries. Indicators computed from the ECB/Frankfurter daily series (530 sessions, 01/08/2024 to 28/08/2026).",
        trend="Price above the 50-day (1.3417) and 200-day (1.3428) SMAs, with the 50-day still below the 200-day — mixed regime resolved bullish by the Aug 20 D10 breakout; the pullback returns the 23.6% Fib (1.3644) to resistance, with the 9-month high (1.3817) above.",
        support="1.3538 (38.2% Fib), with the 1.3500 round beneath.",
        resistance="1.3817 (9-month high), with the 23.6% Fib (1.3644) back as resistance.",
        priceAction="No new entry — event window (Jackson Hole today) and a pullback not yet touching the zone: post-event triggers are (a) a touch of the 1.3500-1.3538 zone followed by a trend-direction close above its midpoint, or (b) a reclaim close above 1.3644. The existing position stays (stop 1.3490 / target 1.3800), with the expiry check on Monday.",
        recommendation="WAIT FOR ANOTHER TRIGGER",
        trigger="None — event window and a pullback with no touch of the 1.3500-1.3538 zone. Post-event: a zone touch + trend-direction close, or a reclaim above 1.3644. Existing position stays (stop 1.3490 / target 1.3800); expiry checked Monday (Aug 31).",
        stop="N/A (no new trade).",
        target="N/A (no new trade).",
        rr="N/A", rrValue=0,
        justification="The pullback deepened and now tests whether the 1.35 area holds — the field sits between the 1.3500 round and the 1.3644 reclaim, with hawkish Warsh weighing via the dollar. No mechanical trigger today; the Aug 17 position stays managed and Monday decides the expiry.",
    ))

A["EUR/JPY"] = dict(
    quote="185.91", bias="ALTA", biasType="bull",
    pt=dict(
        fundamental="O EUR/JPY opera em 185,91 no fechamento diário de 28/08/2026 (referência BCE), avançando +0,16% e imprimindo nova máxima de fechamento de 10 pregões (185,91 > 185,66), colado à Fib 23,6% (185,97) — o alinhamento de alta segue pleno (SMA50 184,77 > SMA200 184,12) e a σ20 comprimiu a 87 pips. Mas a janela de intervenção (até ~03/09) mantém o piso 2,5σ20 (≈217 pips): stop ≤ 183,74 contra o teto da máxima de 9 meses (187,73, a ~182 pips) entrega ~1:0,8 — o gate falha, mesmo com a compressão de volatilidade. O keynote hawkish de Warsh reabre o diferencial BCE-BoJ, mas também sustenta o risco de jawboning do MoF. Indicadores calculados da série diária BCE/Frankfurter (530 pregões, 01/08/2024 a 28/08/2026).",
        trend="Acima das SMA50 (184,77) e SMA200 (184,12) — alinhamento de alta pleno; máxima D10 (185,91) colada à Fib 23,6% (185,97), com a máxima de 20 dias (185,91) equalizada e a de 9 meses (187,73) acima.",
        support="184.77 (SMA50) / 184.88 (Fib 38,2%), com a Fib 50% (184.00) abaixo.",
        resistance="187.73 (máxima de 9 meses), com a Fib 23,6% (185.97) colada ao fechamento.",
        priceAction="Sem entrada — o piso de intervenção (≈217 pips) contra o teto de 187,73 trava qualquer configuração (~1:0,8). Aguardar a expiração da janela (~03/09) ou retração à zona 183,13-184,00 (Fib 61,8-50%) para comprimir o risco.",
        recommendation="AGUARDAR OUTRO GATILHO",
        trigger="Nenhum — piso de intervenção ativo até ~03/09 versus teto de 187,73 trava o R/R em ~1:0,8. Reavaliar após a janela ou em retração à zona 183,13-184,00.",
        stop="N/A (sem operação).",
        target="N/A (sem operação).",
        rr="N/A", rrValue=0,
        justification="A compressão de volatilidade (111 → 87 pips) aproxima a aritmética do gate, mas ainda não a vira: stop de ~217 pips contra teto de ~182. Sem operação até ~03/09; a estrutura segue de alta e o preço testa a confluência da Fib 23,6%.",
    ),
    en=dict(
        fundamental="EUR/JPY trades at 185.91 on the 28/08/2026 daily close (ECB reference), up +0.16% and printing a fresh 10-day closing high (185.91 > 185.66), glued to the 23.6% Fib (185.97) — the bull alignment stays full (50-day 184.77 > 200-day 184.12) and sigma20 compressed to 87 pips. But the intervention window (until ~Sep 3) holds the 2.5-sigma20 floor (~=217 pips): a stop <= 183.74 against the 9-month-high cap (187.73, ~182 pips away) yields ~1:0.8 — the gate fails, even with the volatility compression. Warsh's hawkish keynote reopens the ECB-BoJ differential, but it also sustains the MoF's jawboning risk. Indicators computed from the ECB/Frankfurter daily series (530 sessions, 01/08/2024 to 28/08/2026).",
        trend="Above the 50-day (184.77) and 200-day (184.12) SMAs — full bull alignment; the D10 high (185.91) glued to the 23.6% Fib (185.97), with the 20-day high (185.91) equalized and the 9-month high (187.73) above.",
        support="184.77 (50-day SMA) / 184.88 (38.2% Fib), with the 50% Fib (184.00) beneath.",
        resistance="187.73 (9-month high), with the 23.6% Fib (185.97) glued to the close.",
        priceAction="No entry — the intervention floor (~=217 pips) against the 187.73 cap blocks any configuration (~1:0.8). Wait for the window to expire (~Sep 3) or a pullback to the 183.13-184.00 zone (61.8-50% Fib) to compress risk.",
        recommendation="WAIT FOR ANOTHER TRIGGER",
        trigger="None — intervention floor active until ~Sep 3 versus the 187.73 cap locks R/R at ~1:0.8. Reassess after the window or on a pullback to 183.13-184.00.",
        stop="N/A (no trade).",
        target="N/A (no trade).",
        rr="N/A", rrValue=0,
        justification="The volatility compression (111 → 87 pips) brings the arithmetic closer to the gate, but doesn't flip it yet: a ~217-pip stop against a ~182-pip cap. No trade until ~Sep 3; the structure stays bullish and the price tests the 23.6% Fib confluence.",
    ))

A["GBP/JPY"] = dict(
    quote="216.89", bias="ALTA", biasType="bull",
    pt=dict(
        fundamental="O GBP/JPY opera em 216,89 no fechamento diário de 28/08/2026 (referência BCE), subindo +0,19% e recuperando metade da micro-correção da semana: 25/08 imprimiu a máxima de fechamento de 10 pregões (217,07 > 216,72), seguida de dois recuos (216,81/216,48) e do retorno de sexta. A posição do ticket de 14/08 (entrada 215,90, stop 213,90, alvo 219,00) segue aberta com +99 pips — e completa a 10ª sessão na segunda (31/08): sem cruzamento de alvo ou stop até lá, o ticket expira por tempo. O piso de intervenção 2,5σ20 (≈265 pips, com σ20 comprimida a 106 pips) segue ativo até ~03/09 e trava adições em R/R <1 contra o teto de 219,14. Indicadores calculados da série diária BCE/Frankfurter (530 pregões, 01/08/2024 a 28/08/2026).",
        trend="Acima das SMA50 (215,87) e SMA200 (212,62) — alinhamento de alta; máxima D10 em 217,07 (25/08) com a máxima de 20 dias (217,07) equalizada e a de 9 meses (219,14) acima — o alvo do ticket quase colado à máxima.",
        support="215.87 (SMA50) / 215.83 (Fib 23,6%), com a Fib 38,2% (213.79) abaixo.",
        resistance="219.14 (máxima de 9 meses), com a máxima de 20 dias (217.07) no caminho.",
        priceAction="Sem nova entrada — o alvo do ticket (219,00) está a ~0,97% e colado à máxima de 9 meses; gerenciar a posição existente (stop 213,90 / alvo 219,00) e reavaliar adições apenas após fechamento acima de 219,14 (~03/09 ou novo ground). A segunda (31/08) decide expiração se nenhum nível for cruzado.",
        recommendation="AGUARDAR OUTRO GATILHO",
        trigger="Nenhum — piso de intervenção ativo até ~03/09 e teto de 219,14 colado ao alvo do ticket. Posição existente segue (stop 213,90 / alvo 219,00); adição apenas acima de 219,14; expiração checada na segunda (31/08).",
        stop="N/A (sem nova operação).",
        target="N/A (sem nova operação).",
        rr="N/A", rrValue=0,
        justification="A posição legada oscila a ~1% do alvo com a estrutura de alta inteira a favor — mas adições seguem bloqueadas pelo piso de intervenção e pelo teto de 219,14 colado ao alvo. A segunda decide entre colheita por alvo e expiração por tempo.",
    ),
    en=dict(
        fundamental="GBP/JPY trades at 216.89 on the 28/08/2026 daily close (ECB reference), up +0.19% and recovering half the week's micro-correction: Aug 25 printed the 10-day closing high (217.07 > 216.72), followed by two lower days (216.81/216.48) and Friday's rebound. The Aug 14 ticket's position (entry 215.90, stop 213.90, target 219.00) stays open with +99 pips — and it completes its 10th session on Monday (Aug 31): with no target or stop close-crossed by then, the ticket expires on time. The 2.5-sigma20 intervention floor (~=265 pips, with sigma20 compressed to 106) remains active until ~Sep 3 and locks adds below R/R 1 against the 219.14 cap. Indicators computed from the ECB/Frankfurter daily series (530 sessions, 01/08/2024 to 28/08/2026).",
        trend="Above the 50-day (215.87) and 200-day (212.62) SMAs — bull alignment; the D10 high at 217.07 (Aug 25) with the 20-day high (217.07) equalized and the 9-month high (219.14) above — the ticket's target almost glued to the high.",
        support="215.87 (50-day SMA) / 215.83 (23.6% Fib), with the 38.2% Fib (213.79) beneath.",
        resistance="219.14 (9-month high), with the 20-day high (217.07) in the path.",
        priceAction="No new entry — the ticket's target (219.00) is ~0.97% away and glued to the 9-month high; manage the existing position (stop 213.90 / target 219.00) and reassess adds only after a close above 219.14 (~Sep 3 or fresh ground). Monday (Aug 31) decides expiry if no level is crossed.",
        recommendation="WAIT FOR ANOTHER TRIGGER",
        trigger="None — intervention floor active until ~Sep 3 and the 219.14 cap glued to the ticket's target. Existing position stays (stop 213.90 / target 219.00); adds only above 219.14; expiry checked Monday (Aug 31).",
        stop="N/A (no new trade).",
        target="N/A (no new trade).",
        rr="N/A", rrValue=0,
        justification="The legacy position oscillates ~1% from its target with the entire bull structure behind it — but adds stay blocked by the intervention floor and the 219.14 cap glued to the target. Monday decides between a target harvest and a time expiry.",
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
            "EUR/USD": "-0.30%",
            "USD/JPY": "+0.27%",
            "AUD/USD": "-0.09%",
            "GBP/USD": "-0.16%",
            "EUR/JPY": "-0.04%",
            "GBP/JPY": "+0.11%"
        };'''
new_changes = '''        const dailyChanges = {
            "EUR/USD": "-0.02%",
            "USD/JPY": "+0.18%",
            "AUD/USD": "+0.07%",
            "GBP/USD": "+0.01%",
            "EUR/JPY": "+0.16%",
            "GBP/JPY": "+0.19%"
        };'''
idx = rep(idx, old_changes, new_changes, "ticker")
old_be = 'dataBasis: "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 526 daily sessions (01/08/2024–24/08/2026).",'
new_be = 'dataBasis: "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 530 daily sessions (01/08/2024–28/08/2026).",'
old_bp = 'dataBasis: "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, sigma20 e Donchian calculados · 526 pregões (01/08/2024 a 24/08/2026).",'
new_bp = 'dataBasis: "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, sigma20 e Donchian calculados · 530 pregões (01/08/2024 a 28/08/2026).",'
idx = rep(idx, old_be, new_be, "dataBasis EN")
idx = rep(idx, old_bp, new_bp, "dataBasis PT")

with open(IDX, "w", encoding="utf-8") as f:
    f.write(idx)
print("OK: index.html")

# ---------------- static pages ----------------
GAUGE = {"EUR/USD": 50, "USD/JPY": 51, "AUD/USD": 30, "GBP/USD": 16, "EUR/JPY": 39, "GBP/JPY": 31}
OLD_GAUGE = {"EUR/USD": 9, "USD/JPY": 64, "AUD/USD": 51, "GBP/USD": 37, "EUR/JPY": 29, "GBP/JPY": 39}
# conviction stays 0/10 everywhere (all WAIT); verdicts/biases unchanged (all wait/bull)

BLUF = {  # (old_inner, new_inner) swaps on the BLUF line
 "EUR/USD": [('<span class="bluf-action wait">WAIT</span> — breakout pullback holds above 1.1657; 1.1732 clearance still needed</span>',
              '<span class="bluf-action wait">WAIT</span> — pullback under the 1.1657 Fib toward the 200-day; Jackson Hole reaction due Monday</span>'),
             ('<span class="bluf-action wait">AGUARDAR</span> — retração preserva o rompimento acima de 1.1657; falta fechar acima de 1.1732</span>',
              '<span class="bluf-action wait">AGUARDAR</span> — retração sob a Fib 1.1657 rumo à SMA200; reação de Jackson Hole sai segunda</span>')],
 "USD/JPY": [('<span class="bluf-action wait">WAIT</span> — pullback rejected above the zone; floor until ~03/09</span>',
              '<span class="bluf-action wait">WAIT</span> — pressing the 10-day high (159.70); intervention floor until ~03/09</span>'),
             ('<span class="bluf-action wait">AGUARDAR</span> — retração rejeitada acima da zona; piso até ~03/09</span>',
              '<span class="bluf-action wait">AGUARDAR</span> — pressionando a máxima de 10 dias (159,70); piso de intervenção até ~03/09</span>')],
 "AUD/USD": [('<span class="bluf-action wait">WAIT</span> — D10 continuation Friday; 9-month high caps; zone 0.7000-0.7065 still valid</span>',
              '<span class="bluf-action wait">WAIT</span> — breakout extended; 0.7200/0.7257 caps; zone pullback still the trigger</span>'),
             ('<span class="bluf-action wait">AGUARDAR</span> — rompimento D10 na sexta; máxima de 9 meses trava; zona 0.7000-0.7065 segue válida</span>',
              '<span class="bluf-action wait">AGUARDAR</span> — rompimento estendido; tetos 0.7200/0.7257; retração à zona segue sendo o gatilho</span>')],
 "GBP/USD": [('<span class="bluf-action wait">WAIT</span> — position +75 pips toward 1.3800; adds only above 1.3817</span>',
              '<span class="bluf-action wait">WAIT</span> — deep pullback toward 1.3538; position +24 pips; expiry check Monday</span>'),
             ('<span class="bluf-action wait">AGUARDAR</span> — posição +75 pips rumo a 1.3800; adição só acima de 1.3817</span>',
              '<span class="bluf-action wait">AGUARDAR</span> — retração profunda rumo a 1.3538; posição +24 pips; checagem de expiração segunda</span>')],
 "EUR/JPY": [('<span class="bluf-action wait">WAIT</span> — intervention floor vs 187.73 cap (~1:0.8); window to ~03/09</span>',
              '<span class="bluf-action wait">WAIT</span> — fresh 10-day highs against the intervention wall (~1:0.8)</span>'),
             ('<span class="bluf-action wait">AGUARDAR</span> — piso de intervenção vs teto 187,73 (~1:0,8); janela até ~03/09</span>',
              '<span class="bluf-action wait">AGUARDAR</span> — novas máximas de 10 dias contra o muro de intervenção (~1:0,8)</span>')],
 "GBP/JPY": [('<span class="bluf-action wait">WAIT</span> — new D10 close; position +105 pips, target ~0.95% away</span>',
              '<span class="bluf-action wait">WAIT</span> — position +99 pips; expiry check Monday; floor until ~03/09</span>'),
             ('<span class="bluf-action wait">AGUARDAR</span> — novo rompimento D10; posição +105 pips, alvo a ~0,95%</span>',
              '<span class="bluf-action wait">AGUARDAR</span> — posição +99 pips; checagem de expiração segunda; piso até ~03/09</span>')],
}

NEXT_EVENT = {  # (old EN, new EN, old PT, new PT)
 "EUR/USD": ("Jackson Hole Aug 27-29", "Jackson Hole reaction",
             "Jackson Hole 27-29/08", "Reação de Jackson Hole"),
 "USD/JPY": ("Jackson Hole &amp; BoJ speakers", "BoJ Sep meeting &amp; MoF",
             "Jackson Hole e discursos do BoJ", "BoJ em setembro e MoF"),
 "AUD/USD": ("Jackson Hole &amp; RBA speakers", "China data &amp; JH reaction",
             "Jackson Hole e RBA", "Dados da China e reação do JH"),
 "GBP/USD": ("Jackson Hole Aug 27-29", "Jackson Hole reaction",
             "Jackson Hole 27-29/08", "Reação de Jackson Hole"),
 "EUR/JPY": ("Jackson Hole &amp; BoJ speakers", "BoJ September meeting",
             "Jackson Hole e discursos do BoJ", "Reunião do BoJ em setembro"),
 "GBP/JPY": ("Jackson Hole &amp; BoJ speakers", "BoJ September meeting",
             "Jackson Hole e discursos do BoJ", "Reunião de setembro do BoJ"),
}

GAUGE_LABELS = {  # (old now-label, new now-label, [(side, old, new), ...]) — omit unchanged sides
 "EUR/USD": ("1.1664", "1.1643", [("l", "1.1657", "1.1629"), ("r", "1.1732", "1.1657")]),
 "USD/JPY": ("159.12", "159.68", [("r", "159.60", "161.02")]),  # rgv-l 158.27 unchanged
 "AUD/USD": ("0.7162", "0.7195", [("l", "0.7065", "0.7168")]),  # rgv-r 0.7257 unchanged
 "GBP/USD": ("1.3634", "1.3583", [("l", "1.3528", "1.3538")]),  # rgv-r 1.3817 unchanged
 "EUR/JPY": ("185.60", "185.91", [("l", "184.74", "184.77")]),  # rgv-r 187.73 unchanged
 "GBP/JPY": ("216.95", "216.89", [("l", "215.57", "215.87")]),  # rgv-r 219.14 unchanged
}

for pair, fname in PAGE.items():
    path = f"{DOCS}/{fname}"
    with open(path, encoding="utf-8") as f:
        h = f.read()
    od, nd = old_data[pair], A[pair]
    # 1) BLUF inner text
    for old, new in BLUF[pair]:
        h = rep(h, old, new, f"{fname} BLUF")
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
    # 3) rr — unchanged (N/A) everywhere
    # 4) quote strong
    h = rep(h, f'<strong>{od["quote"]}</strong>', f'<strong>{nd["quote"]}</strong>', f"{fname} quote strong")
    # 5) gauge position (now + marker)
    h = rep(h, f'left: {OLD_GAUGE[pair]}%', f'left: {GAUGE[pair]}%', f"{fname} gauge", 2)
    # 5b) gauge text labels
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

# pages' data-basis lines + chip refreshes
for fname in PAGE.values():
    p = f"{DOCS}/{fname}"
    with open(p, encoding="utf-8") as f:
        h = f.read()
    oen = "ECB/Frankfurter reference rates · SMA50/200, sigma20 &amp; Donchian computed · 526 daily sessions (01/08/2024–24/08/2026)."
    nen = "ECB/Frankfurter reference rates · SMA50/200, sigma20 &amp; Donchian computed · 530 daily sessions (01/08/2024–28/08/2026)."
    opt = "taxas de referência BCE/Frankfurter · SMA50/200, sigma20 e Donchian calculados · 526 pregões (01/08/2024 a 24/08/2026)."
    npt = "taxas de referência BCE/Frankfurter · SMA50/200, sigma20 e Donchian calculados · 530 pregões (01/08/2024 a 28/08/2026)."
    h = rep(h, oen, nen, f"{fname} basis EN")
    h = rep(h, opt, npt, f"{fname} basis PT")
    if fname == "eur-usd.html":
        h = rep(h, '<span class="macro-chip lang-en">Fed hold 3.50-3.75%</span>', '<span class="macro-chip lang-en">Warsh hawkish JH</span>', f"{fname} chip EN 1")
        h = rep(h, '<span class="macro-chip lang-pt" style="display:none;">Fed 3,50-3,75%</span>', '<span class="macro-chip lang-pt" style="display:none;">Warsh hawkish (JH)</span>', f"{fname} chip PT 1")
    if fname == "aud-usd.html":
        h = rep(h, 'WTI $85', 'WTI $83', f"{fname} WTI chips", 2)
    with open(p, "w", encoding="utf-8") as f:
        f.write(h)
print("OK: 6 pages data-basis + chips")

# ---------------- track-record ledger ----------------
LED = DOCS + "/track-record.json"
with open(LED, encoding="utf-8") as f:
    led = f.read()
led = rep(led, '"lastUpdated": "24/08/2026"', '"lastUpdated": "28/08/2026"', "ledger lastUpdated")
led = rep(led, '"note": "legacy 14/08 ticket: 24/08 close 216.95 (+105 pips), fresh D10 close; target 219.00 ~0.95% away"',
          '"note": "legacy 14/08 ticket: 28/08 close 216.89 (+99 pips); 9/10 sessions elapsed — expiry check on 31/08 unless a level close-crosses"',
          "ledger GBP/JPY note")
led = rep(led, '"note": "24/08 close 1.3634 (+75 pips); consolidating on the 23.6% Fib; target 1.3800 ~1.2% away"',
          '"note": "28/08 close 1.3583 (+24 pips); pullback deepened under the 23.6% Fib; 9/10 sessions — expiry check on 31/08"',
          "ledger GBP/USD note")
json.loads(led)  # validate
with open(LED, "w", encoding="utf-8") as f:
    f.write(led)
print("OK: track-record.json (no resolutions; both open tickets annotated at 9/10 sessions; watching stays empty)")

print("\nDONE: run verify_all.py next.")
