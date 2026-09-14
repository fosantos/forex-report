#!/usr/bin/env python3
"""Daily regeneration for the 14/09/2026 edition — ECB/Frankfurter basis
(the logged-in MT5 terminal still returns no FX data; compute_indicators fell back).
Basis: ECB/Frankfurter reference rates, 541 sessions 01/08/2024-14/09/2026 (last close: 14/09/2026).
Session: FOMC-week Monday. EUR/USD -0.35% to 1.1551 — third straight down close sweeping the
10-day low (1.1578), the 20-day low (1.1576) and the 61.8% Fib (1.1582) in one go: confirmed
10-day breakdown. The 1.1631-1.1657 pullback short expired unfired (validity ended at the 14/09
close, zone never printed) and the book re-maps one shelf lower, as the 11/09 edition promised:
SHORT BREAKOUT — trigger a daily close < 1.1551, entry 1.1550, stop 1.1600 (50p >= 46p floor),
target 1.1440 (110p, under the 78.6% Fib 1.1476 / 1.1450 round), 1:2.20, valid through the
15/09 close (FOMC 15-16/09 caveat). AUD/USD -0.60% to 0.7130: third down session broke the
0.7141 floor and killed the retest ticket by its own condition; the re-priced shelf
(0.7076-0.7102) pays ~1:1.5 with the broken zone overhead -> WAIT (cable's Sep 9 verdict).
USD/JPY 154.55 (+0.33%): bounce stretches, floor 2.5sigma20=238p still blocks -> WAIT.
GBP/USD 1.3495: fourth down close, double top caps the premium -> WAIT for FOMC/BoE.
EUR/JPY 178.52: fourth 9-month low + 50/200-day death cross printed -> WAIT (floor 235p).
GBP/JPY 208.56: second bounce close under the re-priced 78.6% Fib (209.82) -> WAIT (floor 303p).
Verdicts: EUR/USD SELL breakout; USD/JPY, AUD/USD, GBP/USD, EUR/JPY, GBP/JPY WAIT.
Also prepends 2 wire items (dollar front foot / FOMC week) to the news digest + news.html
and patches verify_all.py to the new stamp/ticker/stale dates. Aborts on any structural mismatch."""
import re, json, sys
from datetime import datetime, timezone

DOCS = r"C:/Projetos/forex-report/docs"
TS_DATE = "14/09/2026"
now = datetime.now(timezone.utc)
TS = TS_DATE + " " + now.strftime("%H:%M") + " UTC"
OLD_TS = "11/09/2026 17:15 UTC"

BASIS_EN_AMP = "ECB/Frankfurter reference rates · SMA50/200, sigma20 &amp; Donchian computed · 541 daily sessions (01/08/2024–14/09/2026)."
BASIS_PT = "taxas de referência BCE/Frankfurter · SMA50/200, σ20 e Donchian calculados · 541 pregões (01/08/2024 a 14/09/2026)."

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
    "quote": "1.1551", "bias": "BAIXA", "biasType": "bear",
    "pt": {
      "fundamental": "O EUR/USD fechou em 1,1551 na sessão de 14/09/2026 (taxa de referência BCE/Frankfurter; o terminal MT5 logado segue sem retornar dados de FX), caindo -0,35% — terceiro fechamento de queda seguido e o mapa rearmado uma casa abaixo, como a edição anterior prometeu: o fechamento varreu de uma vez a mínima de 10 pregões (1,1578), a de 20 (1,1576) e a Fib 61,8% (1,1582). O repique de venda 1.1631-1.1657 (SMA200 + Fib 50%) expirou sem disparar — o mercado foi para o outro lado — e o dólar abre a semana do FOMC na frente: com o Fed a 3,50-3,75% e o CPI quente de agosto (+0,4% m/m) na mesa, a alta segue em pauta (odds ~60%, decisão em 16/09; casas de previsão chegam a ~85%). O alinhamento segue plenamente de baixa (fechamento sob a SMA200 1,1631, SMA50 1,1529 abaixo dela) com o preço 22 pips sobre a SMA50 — o piso imediato. Indicadores (SMA 50/200, σ20, Donchian e Fibonacci) calculados da série diária BCE/Frankfurter (541 pregões, 01/08/2024 a 14/09/2026).",
      "trend": "Fechamento sob a SMA200 (1,1631) com a SMA50 (1,1529) abaixo — alinhamento de baixa pleno e agora com rompimento confirmado: o fechamento de segunda cravou nova mínima de 10/20 pregões (1,1551) sob a Fib 61,8% (1,1582), com a SMA50 (1,1529) como primeira defesa 22 pips abaixo.",
      "support": "1.1551 é o próprio fechamento — mínima de 10/20 pregões —, com a Fib 78,6% (1.1476) e os redondos 1.1450/1.1400 abaixo; a mínima de 9 meses (1.1340) é o andar de baixo.",
      "resistance": "1.1582 (Fib 61,8% + mínimas quebradas de 10/20 pregões, 1.1578/1.1576), com o redondo 1.1600 e a SMA200 (1.1631) acima.",
      "priceAction": "Setup de venda no rompimento (mapa rearmado uma casa abaixo): o rompimento de 10 pregões está confirmado pelo fechamento de 1,1551 — o gatilho do livro é o próximo fechamento diário sob 1.1551 (entrada de referência 1.1550), stop 1.1600 (sobre o cluster rompido 1.1578-1.1582 e o redondo; 50 pips ≥ piso 1,5σ20 de ~46 pips), alvo 1.1440 (sob a confluência Fib 78,6% 1.1476 + redondo 1.1450), cruzando o redondo 1.1500. Repique que feche de volta sobre 1.1600 cancela o mapa.",
      "recommendation": "VENDA (SHORT) NO ROMPIMENTO",
      "trigger": "Fechamento diário abaixo da mínima de 10 pregões 1.1551 — entrada de referência 1.1550. Válido até o fechamento de 15/09; dentro da janela de 24h do FOMC (15-16/09), reavaliar após o evento.",
      "stop": "1.1600 (sobre o cluster rompido 1.1578-1.1582 e o redondo 1.1600; 50 pips ≥ piso 1,5σ20 de ~46 pips) · risco sugerido ≤ 1% por operação.",
      "target": "1.1440 (sob a confluência Fib 78,6% (1.1476) + redondo 1.1450), com o redondo 1.1500 no caminho e a mínima de 9 meses (1.1340) no andar de baixo.",
      "rr": "1:2.20", "rrValue": 55,
      "justification": "O repique nunca veio e a regra não persegue: o ticket de 1.1631-1.1657 expirou sem disparar e o próprio fechamento entregou o gatilho da casa seguinte — mínima de 10 pregões varrida por fechamento, o padrão validado pelo backtest. Vender o rompimento com stop estrutural sobre o cluster entregue paga 1:2.20 (110 pips contra 50) até sob a confluência 1.1476/1.1450. A janela do FOMC (15-16/09) limita o ticket ao fechamento de terça: dentro das 24h do evento, reavaliar."
    },
    "en": {
      "fundamental": "EUR/USD closed at 1.1551 in the 14/09/2026 session (ECB/Frankfurter reference rate; the logged-in MT5 terminal still returns no FX data), down -0.35% — a third straight down close and the book re-mapped one shelf lower, as the previous edition promised: the close swept the 10-day low (1.1578), the 20-day (1.1576) and the 61.8% Fib (1.1582) in one go. The 1.1631-1.1657 pullback short (SMA200 + 50% Fib) expired unfired — the market went the other way — and the dollar opens the FOMC week on the front foot: with the Fed at 3.50-3.75% and August's hot CPI (+0.4% m/m) on the table, the hike stays in play (~60% odds, decision on Sep 16; prediction venues run as high as ~85%). The alignment stays fully bearish (close under the SMA200 1.1631, 50-day 1.1529 below it) with price 22 pips above the 50-day — the immediate floor. Indicators (SMA 50/200, sigma20, Donchian and Fibonacci) computed from the ECB/Frankfurter daily series (541 sessions, 01/08/2024 to 14/09/2026).",
      "trend": "Close under the 200-day SMA (1.1631) with the 50-day (1.1529) below — full bear alignment now with a confirmed breakdown: Monday's close printed a fresh 10/20-day low (1.1551) under the 61.8% Fib (1.1582), with the 50-day SMA (1.1529) the first defense 22 pips below.",
      "support": "1.1551 is the close itself — the 10/20-day low —, with the 78.6% Fib (1.1476) and the 1.1450/1.1400 rounds beneath; the 9-month low (1.1340) is the lower floor.",
      "resistance": "1.1582 (61.8% Fib + the broken 10/20-day lows, 1.1578/1.1576), with the 1.1600 round and the SMA200 (1.1631) above.",
      "priceAction": "Short-the-breakout setup (the book re-mapped one shelf lower): the 10-day breakdown is confirmed by Monday's 1.1551 close — the ticket's trigger is the next daily close under 1.1551 (entry reference 1.1550), stop 1.1600 (over the broken 1.1578-1.1582 cluster and the round; 50 pips >= the ~46-pip 1.5-sigma20 floor), target 1.1440 (under the 78.6% Fib 1.1476 + 1.1450 round confluence), crossing the 1.1500 round. A pullback closing back over 1.1600 cancels the map.",
      "recommendation": "SELL (SHORT) ON BREAKOUT",
      "trigger": "Daily close under the 10-day low 1.1551 — entry reference 1.1550. Valid through the Sep 15 close; inside the FOMC (Sep 15-16) 24h window, reassess after the event.",
      "stop": "1.1600 (over the broken 1.1578-1.1582 cluster and the 1.1600 round; 50 pips >= the ~46-pip 1.5-sigma20 floor) · suggested risk ≤ 1% per trade.",
      "target": "1.1440 (under the 78.6% Fib (1.1476) + 1.1450 round confluence), with the 1.1500 round on the way and the 9-month low (1.1340) as the lower floor.",
      "rr": "1:2.20", "rrValue": 55,
      "justification": "The pullback never came and the rule does not chase: the 1.1631-1.1657 ticket expired unfired and the close itself delivered the next-shelf trigger — a 10-day low swept by close, the pattern the backtest validated. Selling the breakout with a structural stop over the surrendered cluster pays 1:2.20 (110 pips against 50) down to under the 1.1476/1.1450 confluence. The FOMC (Sep 15-16) window caps the ticket at Tuesday's close: inside the event's 24h, reassess."
    }
  },
  "USD/JPY": {
    "quote": "154.55", "bias": "BAIXA", "biasType": "bear",
    "pt": {
      "fundamental": "O USD/JPY fechou em 154,55 na sessão de 14/09/2026 (taxa de referência BCE/Frankfurter; o terminal MT5 logado segue sem retornar dados de FX), subindo +0,33% — segundo fechamento de alta em três pregões, recuperando o fechamento de quinta (154,18) e mirando o de segunda passada (154,75) e a Fib 78,6%/redondo (155,04-155,00). O repique não muda o mapa: a leitura segue BAIXA (rompimento confirmado desde a edição de 07/09; a mínima de 10/20 pregões segue em 153,27) e a geometria segue bloqueada — com σ20 a 95 pips, o piso de intervenção 2,5σ20 vale 238 pips e uma venda em 154,55 exigiria alvo a ~476 pips (149,79), sob a mínima de 9 meses (152,63), onde só resta o redondo 150,00. A 192 pips da mínima de 9 meses, com o MoF em alerta desde a intervenção conjunta de julho, o risco segue máximo — e a semana entrega os dois árbitros de uma vez: FOMC 15-16/09 (Fed a 3,50-3,75%, alta ~60% em pauta) e BoJ 17-18/09 (~80% para +25 pb, a 1,25%). Indicadores calculados da série diária BCE/Frankfurter (541 pregões, 01/08/2024 a 14/09/2026).",
      "trend": "Fechamento sob a SMA200 (158,35) e sob a SMA50 (159,64), com a SMA50 ainda acima da SMA200 — o rompimento confirmado das mínimas de 10/20 pregões mantém a resolução para baixa: leitura de baixa com o repique esticado a 154,55, 192 pips acima da mínima de 9 meses (152,63) e sob a barreira 154,75/155,04.",
      "support": "152.63 (mínima de 9 meses), com o redondo 152.50 abaixo — 153.27 (mínima de 10/20 pregões) é a primeira defesa.",
      "resistance": "154.75 (fechamento de 07/09) / 155.04 (Fib 78,6% + redondo), com a mínima quebrada de 03/09 (156.01) acima.",
      "priceAction": "Sem entrada — o repique estica e a perseguição continua reprovada: com σ20 = 95 pips, o piso de intervenção (2,5σ20 = 238 pips) exige alvo a ~149,80 e a única âncora no caminho é o redondo 150,00 (terceiro nível). Vender a 192 pips da mínima de 9 meses com o MoF em alerta é entregar o stop ao interveniente. Rearmar: compressão da σ20, base sobre 152.63/152.50 ou retração com estrutura até 155.04-156.01. FOMC (15-16/09) e BoJ (17-18/09) decidem o capítulo.",
      "recommendation": "AGUARDAR OUTRO GATILHO",
      "trigger": "Nenhum — o piso de intervenção (2,5σ20 = 238 pips) reprova a venda a 192 pips da mínima de 9 meses e a compra não tem estrutura sob as médias. Assistir à reação sobre 152.63 e à compressão da σ20; FOMC (15-16/09) e BoJ (17-18/09) decidem o próximo capítulo.",
      "stop": "N/A (sem operação).",
      "target": "N/A (sem operação).",
      "rr": "N/A", "rrValue": 0,
      "justification": "O repique ganhou um segundo pregão, mas a aritmética não mudou: o piso de intervenção (238 pips) não negocia e mirar ~476 pips abaixo cai em território sem estrutura — só o redondo 150,00. Com FOMC e BoJ na mesma semana, o evento decide; o relatório não paga o prêmio de ficar na frente do MoF — nem do comitê."
    },
    "en": {
      "fundamental": "USD/JPY closed at 154.55 in the 14/09/2026 session (ECB/Frankfurter reference rate; the logged-in MT5 terminal still returns no FX data), up +0.33% — a second up close in three sessions, reclaiming Thursday's close (154.18) and aiming at last Monday's (154.75) and the 78.6% Fib / round (155.04-155.00). The bounce does not change the map: the read stays BEAR (confirmed breakdown since the Sep 7 edition; the 10/20-day low still sits at 153.27) and the geometry stays blocked — with sigma20 at 95 pips the 2.5-sigma20 intervention floor is worth 238 pips and a short from 154.55 would need a target ~476 pips lower (149.79), under the 9-month low (152.63), where only the 150.00 round remains. 192 pips above a 9-month low, with the MoF on alert since the July joint intervention, the risk stays maximal — and the week delivers both arbiters at once: FOMC Sep 15-16 (Fed at 3.50-3.75%, hike ~60% in play) and BoJ Sep 17-18 (~80% for +25 bp, to 1.25%). Indicators computed from the ECB/Frankfurter daily series (541 sessions, 01/08/2024 to 14/09/2026).",
      "trend": "Close under the 200-day SMA (158.35) and under the 50-day (159.64), with the 50-day still above the 200-day — the confirmed break of the 10/20-day lows keeps the resolution bearish: a bear read with the bounce stretched to 154.55, 192 pips above the 9-month low (152.63) and under the 154.75/155.04 barrier.",
      "support": "152.63 (9-month low), with the 152.50 round beneath — 153.27 (the 10/20-day low) is the first defense.",
      "resistance": "154.75 (the 07/09 close) / 155.04 (78.6% Fib + round), with the broken Sep 3 low (156.01) above.",
      "priceAction": "No entry — the bounce stretches and the chase stays rejected: with sigma20 = 95 pips, the intervention floor (2.5-sigma20 = 238 pips) demands a target at ~149.80 and the only anchor on the way is the 150.00 round (tier three). Selling 192 pips above the 9-month low with the MoF on alert is handing the stop to the intervenor. Re-arm: sigma20 compression, a base over 152.63/152.50, or a structured pullback to 155.04-156.01. The FOMC (Sep 15-16) and BoJ (Sep 17-18) decide the chapter.",
      "recommendation": "WAIT FOR ANOTHER TRIGGER",
      "trigger": "None — the intervention floor (2.5-sigma20 = 238 pips) rejects a short 192 pips above the 9-month low and a long has no structure under the averages. Watch the reaction at 152.63 and sigma20 compression; the FOMC (Sep 15-16) and BoJ (Sep 17-18) decide the next chapter.",
      "stop": "N/A (no trade).",
      "target": "N/A (no trade).",
      "rr": "N/A", "rrValue": 0,
      "justification": "The bounce won a second session, but the arithmetic did not change: the intervention floor (238 pips) does not negotiate and aiming ~476 pips lower lands in structureless territory — only the 150.00 round. With the FOMC and the BoJ in the same week, the event decides; the report does not pay the premium of standing in front of the MoF — or the committee."
    }
  },
  "AUD/USD": {
    "quote": "0.7130", "bias": "ALTA", "biasType": "bull",
    "pt": {
      "fundamental": "O AUD/USD fechou em 0,7130 na sessão de 14/09/2026 (taxa de referência BCE/Frankfurter; o terminal MT5 logado segue sem retornar dados de FX), caindo -0,60% — terceiro pregão de queda seguido (-1,31% desde o topo de 0,7225), o pior dia da sequência: o fechamento varreu o piso da zona de compra (0.7141) e matou o ticket pela própria condição de cancelamento. O reteste virou quebra local e o alinhamento de alta, embora intacto (SMA50 0,7070 > SMA200 0,6994; preço acima das duas, 60 pips sobre a SMA50), não paga entrada: da próxima prateleira (0.7076-0.7102, mínima de 20 pregões + Fib 23,6%) com stop estrutural em 0.7040 (49 pips ≥ piso 1,5σ20 de ~42 pips), o alvo estrutural mais próximo — a própria zona quebrada 0.7141-0.7162 — paga ~1:1,5 e o próximo (0.7195-0.7204) fica além dela: portão de 1:2 reprovado, o mesmo veredito do cable em 09/09. O motor segue: diferencial da RBA (4,35%, reunião de 29/09; bancos projetam 4,60% em novembro), CPI australiano a 3,5% e WTI ~US$ 83 — mas o FOMC (15-16/09) reprecifica tudo antes. Indicadores calculados da série diária BCE/Frankfurter (541 pregões, 01/08/2024 a 14/09/2026).",
      "trend": "Acima das SMA50 (0,7070) e SMA200 (0,6994) — alinhamento de alta pleno; a retração de três pregões (-1,31%) varreu o piso da zona 0.7141-0.7162 e cravou nova mínima de 10 pregões (0,7130), com a prateleira seguinte em 0.7076-0.7102 (mínima de 20 pregões + Fib 23,6%).",
      "support": "0.7102 (Fib 23,6%), com a mínima de 20 pregões (0.7076) e a SMA50 (0.7070) abaixo — 0.7130 (fechamento) é a nova mínima de 10 pregões.",
      "resistance": "0.7141 (piso quebrado da zona 0.7141-0.7162), com o nível entregue (0.7195-0.7204) e a máxima de 10/20 pregões (0.7225) acima.",
      "priceAction": "Sem entrada — o reteste virou quebra local e o prêmio caiu sob o portão: da prateleira 0.7076-0.7102 (midpoint 0,7089) com stop 0.7040 (49 pips ≥ piso de ~42 pips), a zona quebrada 0.7141-0.7162 paga ~1:1,5 e o nível 0.7195-0.7204 — o único que paga 1:2+ — fica além dela: obstáculo intermediário de primeira ordem. Rearmar: base sobre 0.7076-0.7102 com fechamento de volta sobre 0.7141, ou o FOMC (15-16/09) reprecificando os alvos; RBA em 29/09.",
      "recommendation": "AGUARDAR OUTRO GATILHO",
      "trigger": "Nenhum — o alvo estrutural mais próximo paga ~1:1,5 e o único acima de 1:2 (0.7195-0.7204) fica além da zona quebrada 0.7141-0.7162; o FOMC (15-16/09) reprecifica o mapa em dois pregões. Reavaliar após o evento.",
      "stop": "N/A (sem operação).",
      "target": "N/A (sem operação).",
      "rr": "N/A", "rrValue": 0,
      "justification": "O ticket morreu pela própria cláusula — fechamento sob 0,7141 — e a regra não insiste: a mesma aritmética que tirou o cable do livro em 09/09 tira o AUD agora, com o agravante de três pregões verdes para o dólar na semana do FOMC. O alinhamento de alta segue de pé e a prateleira 0.7076-0.7102 é o lugar do longo — mas só depois que o evento passar e o preço provar a base. A vantagem segue com quem espera."
    },
    "en": {
      "fundamental": "AUD/USD closed at 0.7130 in the 14/09/2026 session (ECB/Frankfurter reference rate; the logged-in MT5 terminal still returns no FX data), down -0.60% — a third straight down session (-1.31% from the 0.7225 top) and the worst day of the sequence: the close swept the buying zone's floor (0.7141) and killed the ticket by its own cancellation condition. The retest became a local breakdown, and the bull alignment — though intact (50-day 0.7070 > 200-day 0.6994; price above both, 60 pips over the 50-day) — pays no entry: from the next shelf (0.7076-0.7102, 20-day low + 23.6% Fib) with a structural stop at 0.7040 (49 pips >= the ~42-pip 1.5-sigma20 floor), the nearest structural target — the broken 0.7141-0.7162 zone itself — pays ~1:1.5 and the next (0.7195-0.7204) sits beyond it: the 1:2 gate rejected, the same verdict cable got on Sep 9. The engine is unchanged: the RBA differential (4.35%, meeting on Sep 29; banks project 4.60% by November), Australian CPI at 3.5% and WTI ~$83 — but the FOMC (Sep 15-16) re-prices everything first. Indicators computed from the ECB/Frankfurter daily series (541 sessions, 01/08/2024 to 14/09/2026).",
      "trend": "Above the 50-day (0.7070) and 200-day (0.6994) SMAs — full bull alignment; the three-session pullback (-1.31%) swept the 0.7141-0.7162 zone's floor and printed a fresh 10-day low (0.7130), with the next shelf at 0.7076-0.7102 (20-day low + 23.6% Fib).",
      "support": "0.7102 (23.6% Fib), with the 20-day low (0.7076) and the 50-day SMA (0.7070) beneath — 0.7130 (the close) is the fresh 10-day low.",
      "resistance": "0.7141 (the broken floor of the 0.7141-0.7162 zone), with the handed-back level (0.7195-0.7204) and the 10/20-day high (0.7225) above.",
      "priceAction": "No entry — the retest became a local breakdown and the premium fell under the gate: from the 0.7076-0.7102 shelf (midpoint 0.7089) with a stop at 0.7040 (49 pips >= the ~42-pip floor), the broken 0.7141-0.7162 zone pays ~1:1.5 and the 0.7195-0.7204 level — the only one paying 1:2+ — sits beyond it: a first-order intermediate block. Re-arm: a base over 0.7076-0.7102 with a close back over 0.7141, or the FOMC (Sep 15-16) re-pricing the targets; RBA on Sep 29.",
      "recommendation": "WAIT FOR ANOTHER TRIGGER",
      "trigger": "None — the nearest structural target pays ~1:1.5 and the only 1:2+ target (0.7195-0.7204) sits beyond the broken 0.7141-0.7162 zone; the FOMC (Sep 15-16) re-prices the map in two sessions. Reassess after the event.",
      "stop": "N/A (no trade).",
      "target": "N/A (no trade).",
      "rr": "N/A", "rrValue": 0,
      "justification": "The ticket died by its own clause — a close under 0.7141 — and the rule does not insist: the same arithmetic that took cable off the book on Sep 9 now takes the AUD, with the aggravation of three straight dollar-green sessions into the FOMC week. The bull alignment stands and the 0.7076-0.7102 shelf is the long's place — but only after the event passes and price proves the base. The edge still belongs to whoever waits."
    }
  },
  "GBP/USD": {
    "quote": "1.3495", "bias": "ALTA", "biasType": "bull",
    "pt": {
      "fundamental": "O GBP/USD fechou em 1,3495 na sessão de 14/09/2026 (taxa de referência BCE/Frankfurter; o terminal MT5 logado segue sem retornar dados de FX), caindo -0,10% — quarto fechamento de queda seguido desde a dupla rejeição no cluster 1.3565-1.3566, agora a 12 pips das mínimas de 10/20 pregões (1.3483). O alinhamento de alta segue pleno (SMA50 1,3478 > SMA200 1,3448; preço acima das duas) e a aritmética segue reprovada: da zona 1.3448-1.3478 (confluência das médias, midpoint 1,3463) com stop estrutural em 1.3390 (73 pips ≥ piso 1,5σ20 de ~47 pips), o cluster paga ~1:1,4 — e o único alvo que paga 1:2+ (máxima de 20 pregões, 1.3656) fica além do topo duplo rejeitado duas vezes. A semana reprecifica tudo: FOMC 15-16/09 (Fed a 3,50-3,75%, alta ~60% em pauta) e BoE 17/09 (3,75%, último voto 6-3). Indicadores calculados da série diária BCE/Frankfurter (541 pregões, 01/08/2024 a 14/09/2026).",
      "trend": "Preço acima das SMA50 (1,3478) e SMA200 (1,3448) — alinhamento de alta pleno; o quarto fechamento de queda seguido pressiona a prateleira 1.3483 (mínimas de 10/20 pregões), com a zona de retração 1.3448-1.3478 logo abaixo.",
      "support": "1.3483 (mínimas de 10/20 pregões), com a confluência SMA200/SMA50 (1.3448-1.3478) e a Fib 61,8% (1.3411) abaixo.",
      "resistance": "1.3565 (máxima de 10 pregões + Fib 38,2% 1.3566 — topo duplo), com a máxima de 20 pregões (1.3656) acima.",
      "priceAction": "Sem entrada — o prêmio segue sob o portão: da zona 1.3448-1.3478 (midpoint 1,3461), stop 1.3390 contra o cluster 1.3565-1.3566 paga ~1:1,4; esticar até a máxima de 20 pregões (1.3656) cruza o topo duplo rejeitado duas vezes — bloqueio intermediário de primeira ordem. Fechamento sob a Fib 61,8% (1.3411) invalida a estrutura de alta. Rearmar: recuo da zona até os redondos (1.3400-1.3448), compressão da σ20 ou quebra limpa de 1.3566 reprecificando os alvos. FOMC (15-16/09) e BoE (17/09) arbitram.",
      "recommendation": "AGUARDAR OUTRO GATILHO",
      "trigger": "Nenhum — o alvo estrutural mais próximo paga ~1:1,4 e o único alvo acima de 1:2 (1.3656) fica além do topo duplo 1.3565-1.3566; o BoE (17/09) reprecifica o mapa em três pregões. Reavaliar após o FOMC e o BoE.",
      "stop": "N/A (sem operação).",
      "target": "N/A (sem operação).",
      "rr": "N/A", "rrValue": 0,
      "justification": "Quarto fechamento de queda e o cable segue o par mais firme contra o dólar — justamente por isso a disciplina manda esperar: o cluster 1.3565-1.3566 segue rejeitando alvos, o FOMC (15-16/09) testa o viés antes e o BoE (17/09) reprecifica zona, stop e alvo de uma vez. Se a prateleira 1.3483 entregar, a zona das médias devolve o mapa — depois dos eventos."
    },
    "en": {
      "fundamental": "GBP/USD closed at 1.3495 in the 14/09/2026 session (ECB/Frankfurter reference rate; the logged-in MT5 terminal still returns no FX data), down -0.10% — a fourth straight down close since the double rejection at the 1.3565-1.3566 cluster, now 12 pips above the 10/20-day lows (1.3483). The bull alignment stands (50-day 1.3478 > 200-day 1.3448; price above both) and the arithmetic stays rejected: from the 1.3448-1.3478 zone (the averages' confluence, midpoint 1.3463) with a structural stop at 1.3390 (73 pips >= the ~47-pip 1.5-sigma20 floor), the cluster pays ~1:1.4 — and the only target paying 1:2+ (the 20-day high, 1.3656) sits beyond the twice-rejected double top. The week re-prices everything: FOMC Sep 15-16 (Fed at 3.50-3.75%, hike ~60% in play) and BoE Sep 17 (3.75%, last vote 6-3). Indicators computed from the ECB/Frankfurter daily series (541 sessions, 01/08/2024 to 14/09/2026).",
      "trend": "Price above the 50-day (1.3478) and 200-day (1.3448) SMAs — full bull alignment; the fourth straight down close presses the 1.3483 shelf (10/20-day lows), with the 1.3448-1.3478 pullback zone just below.",
      "support": "1.3483 (10/20-day lows), with the 200/50-day SMA confluence (1.3448-1.3478) and the 61.8% Fib (1.3411) beneath.",
      "resistance": "1.3565 (10-day high + 38.2% Fib 1.3566 — the double top), with the 20-day high (1.3656) above.",
      "priceAction": "No entry — the premium stays under the gate: from the 1.3448-1.3478 zone (midpoint 1.3461), stop 1.3390 against the 1.3565-1.3566 cluster pays ~1:1.4; stretching to the 20-day high (1.3656) crosses the twice-rejected double top — a first-order intermediate block. A close below the 61.8% Fib (1.3411) invalidates the bull structure. Re-arm: the zone sliding back to the rounds (1.3400-1.3448), sigma20 compression, or a clean break of 1.3566 re-pricing the targets. The FOMC (Sep 15-16) and BoE (Sep 17) arbitrate.",
      "recommendation": "WAIT FOR ANOTHER TRIGGER",
      "trigger": "None — the nearest structural target pays ~1:1.4 and the only 1:2+ target (1.3656) sits beyond the 1.3565-1.3566 double top; the BoE (Sep 17) re-prices the map in three sessions. Reassess after the FOMC and the BoE.",
      "stop": "N/A (no trade).",
      "target": "N/A (no trade).",
      "rr": "N/A", "rrValue": 0,
      "justification": "A fourth down close and cable remains the firmest pair against the dollar — precisely why discipline says wait: the 1.3565-1.3566 cluster keeps rejecting targets, the FOMC (Sep 15-16) tests the bias before the BoE (Sep 17) re-prices zone, stop and target at once. If the 1.3483 shelf gives way, the averages' zone hands the map back — after the events."
    }
  },
  "EUR/JPY": {
    "quote": "178.52", "bias": "BAIXA", "biasType": "bear",
    "pt": {
      "fundamental": "O EUR/JPY fechou em 178,52 na sessão de 14/09/2026 (taxa de referência BCE/Frankfurter; o terminal MT5 logado segue sem retornar dados de FX), caindo -0,02% — quarta mínima de 9 meses da sequência (178,59 → 178,56 → 178,52), agora com o cruzamento de baixa confirmado: a SMA50 (184,03) cruzou para baixo da SMA200 (184,15) depois do empate da sexta. Com o BCE (2,50%) já entregue e o mercado precificando ~80% de +25 pb do BoJ (para 1,25%) em 17-18/09, o motor segue sendo o iene — e o MoF segue em alerta desde a intervenção conjunta de julho. A geometria segue bloqueada: σ20 a 94 pips faz o piso de intervenção 2,5σ20 valer 235 pips — uma venda exigiria alvo a ~470 pips (173,82), território sem estrutura além dos redondos 178,00/177,50. Indicadores calculados da série diária BCE/Frankfurter (541 pregões, 01/08/2024 a 14/09/2026).",
      "trend": "Fechamento sob a SMA200 (184,15) e sob a SMA50 (184,03), agora com a SMA50 cruzando para baixo — a sequência de rompimentos (181,20 → 180,28 → 179,20 → 178,59 → 178,56 → 178,52) mantém a resolução para baixa: leitura de baixa em mínimas de 9 meses sucessivas.",
      "support": "178.52 é o próprio fechamento — quarta mínima de 9 meses —; abaixo, apenas os redondos 178.00/177.50.",
      "resistance": "179.10 (fechamento de quinta) / redondo 179.50, com a mínima quebrada (180.28) e as mínimas de 03-04/09 (181.20-181.59) acima.",
      "priceAction": "Sem entrada — a direção segue resolvida para baixa, mas o piso de intervenção (2,5σ20 = 235 pips) reprova a perseguição em mínima de 9 meses sem âncoras à frente; compra sob duas médias em cruzamento de baixa é aposta contra o BoJ. Rearmar: compressão da σ20 ou reteste estruturado de 180.28-181.20. O BoJ 17-18/09 é o árbitro.",
      "recommendation": "AGUARDAR OUTRO GATILHO",
      "trigger": "Nenhum — o piso de intervenção (2,5σ20 = 235 pips) e a ausência de âncoras sob a mínima de 9 meses reprovam qualquer setup. Assistir à reação nos redondos 178,00/177,50 e à compressão da σ20; BoJ 17-18/09 arbitra.",
      "stop": "N/A (sem operação).",
      "target": "N/A (sem operação).",
      "rr": "N/A", "rrValue": 0,
      "justification": "Quarta mínima de 9 meses e desta vez com o cruzamento de baixa no painel: o empate das médias virou SMA50 sob a SMA200. O problema segue o mesmo: o piso de intervenção (235 pips) manda procurar âncora a ~470 pips abaixo e a janela de 9 meses acabou — só restam redondos, âncoras de terceiro nível. Com o BoJ a ~80% de alta, o desempate é evento, não preço. Fora do mercado."
    },
    "en": {
      "fundamental": "EUR/JPY closed at 178.52 in the 14/09/2026 session (ECB/Frankfurter reference rate; the logged-in MT5 terminal still returns no FX data), down -0.02% — the sequence's fourth 9-month low (178.59 → 178.56 → 178.52), this time with the bearish cross confirmed: the 50-day SMA (184.03) slipped under the 200-day (184.15) after Friday's tie. With the ECB (2.50%) already delivered and the market pricing ~80% odds of a +25-bp BoJ step (to 1.25%) on Sep 17-18, the engine remains the yen — and the MoF stays on alert since the July joint intervention. The geometry stays blocked: sigma20 at 94 pips puts the 2.5-sigma20 intervention floor at 235 pips — a short would need a target ~470 pips lower (173.82), territory with no structure beyond the 178.00/177.50 rounds. Indicators computed from the ECB/Frankfurter daily series (541 sessions, 01/08/2024 to 14/09/2026).",
      "trend": "Close under the 200-day SMA (184.15) and under the 50-day (184.03), now with the 50-day crossing below — the breakdown sequence (181.20 → 180.28 → 179.20 → 178.59 → 178.56 → 178.52) keeps the resolution bearish: a bear read on successive 9-month lows.",
      "support": "178.52 is the close itself — a fourth 9-month low; beneath it, only the 178.00/177.50 rounds.",
      "resistance": "179.10 (Thursday's close) / 179.50 round, with the broken 9-month low (180.28) and the Sep 3-4 lows (181.20-181.59) above.",
      "priceAction": "No entry — the direction stays resolved bearish, but the intervention floor (2.5-sigma20 = 235 pips) rejects the chase at a 9-month low with no anchors ahead; a long under two averages in a fresh bearish cross is a bet against the BoJ. Re-arm: sigma20 compression or a structured retest of 180.28-181.20. The BoJ Sep 17-18 is the arbiter.",
      "recommendation": "WAIT FOR ANOTHER TRIGGER",
      "trigger": "None — the intervention floor (2.5-sigma20 = 235 pips) and the absence of anchors beneath the 9-month low reject any setup. Watch the reaction at the 178.00/177.50 rounds and sigma20 compression; the BoJ Sep 17-18 arbitrates.",
      "stop": "N/A (no trade).",
      "target": "N/A (no trade).",
      "rr": "N/A", "rrValue": 0,
      "justification": "A fourth 9-month low, this time with the bearish cross on the board: Friday's tie of the averages became a 50-day under the 200-day. The problem is the same: the intervention floor (235 pips) demands an anchor ~470 pips below and the 9-month window has run out — only tier-three rounds remain. With the BoJ ~80% priced to hike, the tiebreak is the event, not the price. Out of the market."
    }
  },
  "GBP/JPY": {
    "quote": "208.56", "bias": "BAIXA", "biasType": "bear",
    "pt": {
      "fundamental": "O GBP/JPY fechou em 208,56 na sessão de 14/09/2026 (taxa de referência BCE/Frankfurter; o terminal MT5 logado segue sem retornar dados de FX), subindo +0,23% — segundo fechamento de alta seguido desde a mínima de 10/20 pregões (207,91), ainda sob a Fib 78,6% quebrada, reprecificada mais uma vez pela rotação da janela de 9 meses (209,70 → 209,82; a mínima de 9 meses subiu para 207,29 com a saída do 207,13). A leitura segue BAIXA (rompimento confirmado desde a edição de 07/09) e a geometria segue bloqueada: σ20 a 121 pips faz o piso de intervenção 2,5σ20 valer 303 pips — uma venda exigiria alvo a ~606 pips (202,50), sob a mínima de 9 meses. BoJ a ~80% para +25 pb (1,25%) e BoE a 3,75% decidem na mesma semana (17-18/09), com o FOMC (15-16/09) abrindo a sequência. Indicadores calculados da série diária BCE/Frankfurter (541 pregões, 01/08/2024 a 14/09/2026).",
      "trend": "Fechamento sob a SMA200 (212,94) e sob a SMA50 (215,13), com a SMA50 ainda acima da SMA200 — a sequência de rompimentos (210,57 → 209,39 → 207,91) mantém a resolução para baixa: leitura de baixa com o repique de dois pregões travado sob a Fib 78,6% reprecificada (209,82).",
      "support": "207.29 (mínima de 9 meses, reprecificada), com o redondo 207.00 abaixo — 207.91 (mínima de 10/20 pregões) é a primeira defesa.",
      "resistance": "209.82 (Fib 78,6% reprecificada) / redondo 209.00, com a mínima quebrada de 03/09 (210.57) acima.",
      "priceAction": "Sem entrada — direção resolvida para baixo, geometria bloqueada: com σ20 = 121 pips, o piso de intervenção (2,5σ20 = 303 pips) manda procurar âncora a ~606 pips e ela está sob a mínima de 9 meses; compra não tem estrutura. Rearmar: compressão da σ20 ou reteste estruturado de 209.82-210.57. BoE/BoJ em 17-18/09 arbitram.",
      "recommendation": "AGUARDAR OUTRO GATILHO",
      "trigger": "Nenhum — o piso de intervenção (2,5σ20 = 303 pips) reprova qualquer geometria. Assistir à reação sobre a mínima de 9 meses (207.29) e à compressão da σ20.",
      "stop": "N/A (sem operação).",
      "target": "N/A (sem operação).",
      "rr": "N/A", "rrValue": 0,
      "justification": "O repique ganhou um segundo pregão e parou no mesmo lugar: sob a Fib quebrada, agora reprecificada em 209,82 pela rotação da janela. Abaixo, a mínima também subiu para 207,29 — e mesmo com o alvo mais próximo, o piso de intervenção (303 pips) exige mirar ~202,50, onde não há nada além de redondos. Depois da intervenção conjunta de julho e do surto de 03/09, a lição não muda: não se paga caro para ficar na frente do MoF. Fora do mercado até a estrutura — ou o BoJ — entregarem algo."
    },
    "en": {
      "fundamental": "GBP/JPY closed at 208.56 in the 14/09/2026 session (ECB/Frankfurter reference rate; the logged-in MT5 terminal still returns no FX data), up +0.23% — a second straight up close off the 10/20-day low (207.91), still under the broken 78.6% Fib, re-priced once more by the 9-month window's rotation (209.70 → 209.82; the 9-month low rose to 207.29 as the 207.13 left the window). The read stays BEAR (confirmed breakdown since the Sep 7 edition) and the geometry stays blocked: sigma20 at 121 pips puts the 2.5-sigma20 intervention floor at 303 pips — a short would need a target ~606 pips lower (202.50), under the 9-month low. The BoJ ~80% priced for +25 bp (1.25%) and the BoE at 3.75% decide in the same week (Sep 17-18), with the FOMC (Sep 15-16) opening the sequence. Indicators computed from the ECB/Frankfurter daily series (541 sessions, 01/08/2024 to 14/09/2026).",
      "trend": "Close under the 200-day SMA (212.94) and under the 50-day (215.13), with the 50-day still above the 200-day — the breakdown sequence (210.57 → 209.39 → 207.91) keeps the resolution bearish: a bear read with the two-session bounce capped under the re-priced 78.6% Fib (209.82).",
      "support": "207.29 (9-month low, re-priced), with the 207.00 round beneath — 207.91 (the 10/20-day low) is the first defense.",
      "resistance": "209.82 (re-priced 78.6% Fib) / 209.00 round, with the broken Sep 3 low (210.57) above.",
      "priceAction": "No entry — direction resolved bearish, geometry blocked: with sigma20 = 121 pips, the intervention floor (2.5-sigma20 = 303 pips) demands an anchor ~606 pips away and it sits under the 9-month low; a long has no structure. Re-arm: sigma20 compression or a structured retest of 209.82-210.57. The BoE/BoJ Sep 17-18 week arbitrates.",
      "recommendation": "WAIT FOR ANOTHER TRIGGER",
      "trigger": "None — the intervention floor (2.5-sigma20 = 303 pips) rejects any geometry. Watch the reaction at the 9-month low (207.29) and sigma20 compression.",
      "stop": "N/A (no trade).",
      "target": "N/A (no trade).",
      "rr": "N/A", "rrValue": 0,
      "justification": "The bounce won a second session and stopped in the same place: under the broken Fib, now re-priced to 209.82 by the window's rotation. Below, the low also rose to 207.29 — and even with the nearer target, the intervention floor (303 pips) demands aiming at ~202.50, where nothing but rounds exist. After the July joint intervention and the Sep 3 surge, the lesson holds: do not pay up to stand in front of the MoF. Out of the market until the structure — or the BoJ — delivers something."
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
html = rep(html, 'dataBasis: "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 540 daily sessions (01/08/2024–11/09/2026).",',
                 'dataBasis: "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 541 daily sessions (01/08/2024–14/09/2026).",', "basis en")
html = rep(html, 'dataBasis: "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, σ20 e Donchian calculados · 540 pregões (01/08/2024 a 11/09/2026).",',
                 'dataBasis: "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, σ20 e Donchian calculados · 541 pregões (01/08/2024 a 14/09/2026).",', "basis pt")

html, n = re.subn(
    r"        const dailyChanges = \{.*?\n        \};",
    '''        const dailyChanges = {
            "EUR/USD": "-0.35%",
            "USD/JPY": "+0.33%",
            "AUD/USD": "-0.60%",
            "GBP/USD": "-0.10%",
            "EUR/JPY": "-0.02%",
            "GBP/JPY": "+0.23%"
        };''', html, count=1, flags=re.DOTALL)
if n != 1:
    print("FAIL: dailyChanges"); sys.exit(1)

html, n = re.subn(
    r"        const macroDrivers = \{.*?\n        \};",
    '''        const macroDrivers = {
            "EUR/USD": {
                en: ["10-day low broken", "Short < 1.1551", "FOMC Sep 15-16"],
                pt: ["Mín. 10 preg. rompida", "Venda < 1,1551", "FOMC 15-16/09"]
            },
            "USD/JPY": {
                en: ["Bounce to 154.55", "2.5σ floor 238p", "FOMC/BoJ this week"],
                pt: ["Repique a 154,55", "Piso 2,5σ 238p", "FOMC/BoJ na semana"]
            },
            "AUD/USD": {
                en: ["Retest killed <0.7141", "Shelf 0.7076-0.7102", "RBA Sep 29"],
                pt: ["Reteste morto <0,7141", "Prateleira 0,7076-0,7102", "RBA 29/09"]
            },
            "GBP/USD": {
                en: ["4th down close", "Premium < 1:2 gate", "BoE Sep 17"],
                pt: ["4ª queda seguida", "Prêmio < 1:2", "BoE 17/09"]
            },
            "EUR/JPY": {
                en: ["Death cross printed", "2.5σ floor 235p", "BoJ Sep 17-18"],
                pt: ["Cruzamento de baixa", "Piso 2,5σ 235p", "BoJ 17-18/09"]
            },
            "GBP/JPY": {
                en: ["Fib re-priced 209.82", "2.5σ floor 303p", "BoE/BoJ Sep 17"],
                pt: ["Fib reprecificada 209,82", "Piso 2,5σ 303p", "BoE/BoJ 17/09"]
            }
        };''', html, count=1, flags=re.DOTALL)
if n != 1:
    print("FAIL: macroDrivers"); sys.exit(1)

# ---- news wire digest (newsData): update stamp + prepend the 14/09 items ----
html = rep(html, 'updated: "' + OLD_TS + '",', 'updated: "' + TS + '",', "newsData.updated")

NEWS_ITEMS = '''                {
                    date: "14/09/2026",
                    category: "flow",
                    impact: "high",
                    pairs: ["EUR/USD", "AUD/USD"],
                    pt: {
                        headline: "Dólar abre a semana do FOMC na frente: EUR/USD rompe a mínima de 10 pregões e os dois tickets de sexta saem do livro",
                        summary: "A segunda-feira varreu os dois tickets vivos numa sessão só. O EUR/USD caiu -0,35% para 1,1551 — terceiro fechamento de queda seguido, varrendo as mínimas de 10/20 pregões (1.1578/1.1576) e a Fib 61,8% (1.1582): o rompimento confirmado expirou sem disparar o curto do repique 1.1631-1.1657 e rearmou o mapa uma casa abaixo — venda em fechamento sob 1.1551, stop 1.1600, alvo 1.1440 (1:2,20), válida até o fechamento de 15/09. O AUD/USD foi pior: -0,60% para 0,7130, terceiro pregão de queda (-1,31% desde o topo de 0,7225), quebrou o piso 0,7141 e matou o ticket do reteste pela própria condição — a prateleira seguinte (0.7076-0.7102, mínima de 20 pregões + Fib 23,6%) paga menos de 1:2 com a zona quebrada no caminho, e o par migra para AGUARDAR.",
                        take: "O livro registra sem drama: um ticket expirou sem disparar — o repique nunca veio — e outro morreu pela própria condição de fechamento. O que resta direcional é o próprio rompimento, e só até a janela de 24h do FOMC fechá-lo: o curto exige seu fechamento confirmatório sob 1,1551 e nada é perseguido a duas sessões do comitê."
                    },
                    en: {
                        headline: "Dollar opens FOMC week on the front foot: EUR/USD breaks the 10-day low and both Friday tickets come off the book",
                        summary: "Monday swept the desk's two live tickets in one session. EUR/USD fell -0.35% to 1.1551 — a third straight down close straight through the 10/20-day lows (1.1578/1.1576) and the 61.8% Fib (1.1582): the confirmed breakdown expired the 1.1631-1.1657 pullback short unfired and re-mapped the book one shelf lower — short a daily close under 1.1551, stop 1.1600, target 1.1440 (1:2.20), valid through the Sep 15 close. AUD/USD fared worse: -0.60% to 0.7130, a third down session (-1.31% from the 0.7225 top) that broke the 0.7141 floor and killed the retest ticket by its own condition — the next shelf (0.7076-0.7102, 20-day low + 23.6% Fib) pays under 1:2 with the broken zone overhead, so the pair moves to WAIT.",
                        take: "The ledger records it plainly: one ticket expired unfired — the pullback never came — and one was killed by its own close-condition. What remains directional is the breakdown itself, and only until the FOMC 24h window shuts it: the short needs its own confirming close under 1.1551, and nothing is chased two sessions before the committee."
                    }
                },
                {
                    date: "14/09/2026",
                    category: "cb",
                    impact: "high",
                    pairs: ["EUR/USD", "USD/JPY", "GBP/USD"],
                    pt: {
                        headline: "Semana do FOMC abre com o mercado dividido: ~60% de alta em pauta para quarta, BoE e BoJ nas 48h seguintes",
                        summary: "O FOMC de 15-16/09 lidera o filtro de eventos da semana: com o Fed a 3,50-3,75% e o CPI quente de agosto (+0,4% m/m; 3,4% a/a, núcleo esfriando a 2,4% a/a) mantendo a alta em pauta (~60% precificados, com casas de previsão divididas entre 46% e 85%), nenhuma entrada direcional nova dentro da janela de 24h — o curto de rompimento do EUR/USD vale só até o fechamento de 15/09. O BoE (17/09, 3,75%, último voto 6-3) reprecifica o mapa travado do cable; o BoJ (17-18/09, ~80% para +25 pb, a 1,25%) decide os cruzamentos com iene com o MoF em alerta desde a intervenção conjunta de julho — os pisos de 2,5σ20 (235-303 pips) mantêm os três pares em AGUARDAR.",
                        take: "Três decisões em 72 horas reprecificam todos os mapas do livro: o curto do EUR/USD passa o bastão ao FOMC, o cable espera o BoE e os pares com iene esperam o BoJ — o relatório não fica na frente do comitê e muito menos do MoF."
                    },
                    en: {
                        headline: "FOMC week opens with a split market: ~60% hike odds into Wednesday's decision, BoE and BoJ follow within 48 hours",
                        summary: "The Sep 15-16 FOMC tops the event filter this week: with the Fed at 3.50-3.75% and August's hot headline CPI (+0.4% m/m; 3.4% y/y, core cooling to 2.4% y/y) keeping the hike in play (~60% priced, with prediction venues split as wide as 46-85%), no new directional entry inside the 24h window — the EUR/USD breakout short runs only through the Sep 15 close. The BoE (Sep 17, 3.75%, last vote 6-3) re-prices cable's capped map; the BoJ (Sep 17-18, ~80% priced for +25 bp to 1.25%) decides the yen crosses with the MoF on alert since the July joint intervention — the 2.5-sigma20 floors (235-303 pips) keep all three yen pairs on WAIT.",
                        take: "Three decisions in 72 hours re-price every map on the book: the EUR/USD short hands the baton to the FOMC, cable waits for the BoE, and the yen pairs wait for the BoJ — the report does not stand in front of the committee, and even less in front of the MoF."
                    }
                },
'''
html = rep(html, '            items: [\n                {\n                    date: "11/09/2026"',
            "            items: [\n" + NEWS_ITEMS + "                {\n                    date: \"11/09/2026\"", "newsData item prepend")

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
    # data basis + next event + chips + ts-date + rr-seal
    h = resub(h, r"<div class=\"data-basis\">.*?</div>",
              '<div class="data-basis"><span class="db-tag"><span class="lang-en">Basis</span><span class="lang-pt" style="display:none;">Base</span>:</span> <span class="lang-en">' + BASIS_EN_AMP + '</span><span class="lang-pt" style="display:none;">' + BASIS_PT + "</span></div>",
              f"{tag} basis")
    h = resub(h, r"<div class=\"next-event\">.*?</div>", next_ev, f"{tag} next-event")
    for old, new, lab in chips:
        h = rep(h, old, new, f"{tag} chip {lab}")
    h = rep(h, '<span class="ts-date">11·09·26</span>', '<span class="ts-date">14·09·26</span>', f"{tag} ts-date")
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
    "EUR/USD": '<div class="next-event"><span class="ne-tag"><span class="lang-en">Next focus</span><span class="lang-pt" style="display:none;">Próximo foco</span></span> <span class="lang-en">FOMC 15-16/09</span><span class="lang-pt" style="display:none;">FOMC 15-16/09</span></div>',
    "USD/JPY": '<div class="next-event"><span class="ne-tag"><span class="lang-en">Next focus</span><span class="lang-pt" style="display:none;">Próximo foco</span></span> <span class="lang-en">FOMC 15-16/09 · BoJ 17-18/09</span><span class="lang-pt" style="display:none;">FOMC 15-16/09 · BoJ 17-18/09</span></div>',
    "AUD/USD": '<div class="next-event"><span class="ne-tag"><span class="lang-en">Next focus</span><span class="lang-pt" style="display:none;">Próximo foco</span></span> <span class="lang-en">FOMC 15-16/09 · RBA 29/09</span><span class="lang-pt" style="display:none;">FOMC 15-16/09 · RBA 29/09</span></div>',
    "GBP/USD": '<div class="next-event"><span class="ne-tag"><span class="lang-en">Next focus</span><span class="lang-pt" style="display:none;">Próximo foco</span></span> <span class="lang-en">FOMC 15-16/09 · BoE 17/09</span><span class="lang-pt" style="display:none;">FOMC 15-16/09 · BoE 17/09</span></div>',
    "EUR/JPY": '<div class="next-event"><span class="ne-tag"><span class="lang-en">Next focus</span><span class="lang-pt" style="display:none;">Próximo foco</span></span> <span class="lang-en">BoJ 17-18/09</span><span class="lang-pt" style="display:none;">BoJ 17-18/09</span></div>',
    "GBP/JPY": '<div class="next-event"><span class="ne-tag"><span class="lang-en">Next focus</span><span class="lang-pt" style="display:none;">Próximo foco</span></span> <span class="lang-en">BoE 17/09 · BoJ 17-18/09</span><span class="lang-pt" style="display:none;">BoE 17/09 · BoJ 17-18/09</span></div>',
}

FD["EUR/USD"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action sell">SELL</span> — confirmed breakdown: the 1.1551 close took out the 10/20-day lows and the 61.8% Fib; short a close under 1.1551, stop 1.1600, target 1.1440 (1:2.20)</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action sell">VENDA</span> — rompimento confirmado: o fechamento 1,1551 varreu as mínimas de 10/20 pregões e a Fib 61,8%; vender um fechamento sob 1,1551, stop 1,1600, alvo 1,1440 (1:2,20)</span>',
    "_tier_en": "High", "_tier_pt": "Alta",
})
FD["USD/JPY"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — the bounce stretches to 154.55 into the FOMC/BoJ week; the 238-pip intervention floor still rejects every geometry</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — o repique estica para 154,55 na semana do FOMC/BoJ; o piso de intervenção de 238 pips segue rejeitando qualquer geometria</span>',
    "_tier_en": "Moderate", "_tier_pt": "Moderada",
})
FD["AUD/USD"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — three down sessions (-1.31%) broke the 0.7141 floor and killed the ticket; the 0.7076-0.7102 shelf pays under 1:2 with the broken zone overhead</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — três pregões de queda (-1,31%) quebraram o piso 0,7141 e mataram o ticket; a prateleira 0,7076-0,7102 paga menos de 1:2 com a zona quebrada no caminho</span>',
    "_tier_en": "Moderate", "_tier_pt": "Moderada",
})
FD["GBP/USD"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — a fourth down close presses the 1.3483 shelf; the 1.3565-1.3566 double top still caps the premium ahead of the FOMC/BoE</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — quarto fechamento de queda pressiona a prateleira 1,3483; o topo duplo 1.3565-1.3566 segue capando o prêmio antes de FOMC/BoE</span>',
    "_tier_en": "Moderate", "_tier_pt": "Moderada",
})
FD["EUR/JPY"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — a fourth 9-month low (178.52) with the 50/200-day bearish cross printed; the 235-pip intervention floor rejects all geometry into the BoJ</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — quarta mínima de 9 meses (178,52) com o cruzamento de baixa das médias; o piso de intervenção de 235 pips rejeita qualquer geometria rumo ao BoJ</span>',
    "_tier_en": "Moderate", "_tier_pt": "Moderada",
})
FD["GBP/JPY"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — a second bounce close (208.56) stays under the re-priced 78.6% Fib (209.82); the 303-pip intervention floor rejects all geometry</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — segundo fechamento de repique (208,56) sob a Fib 78,6% reprecificada (209,82); o piso de intervenção de 303 pips rejeita qualquer geometria</span>',
    "_tier_en": "Moderate", "_tier_pt": "Moderada",
})

# no bias flips today: EUR/USD bear, USD/JPY bear, AUD/USD bull, GBP/USD bull, EUR/JPY bear, GBP/JPY bear
BIAS_SWAP = {}

# chips stay as-is (all still accurate); no swaps this edition
CHIPS = {"EUR/USD": [], "USD/JPY": [], "AUD/USD": [], "GBP/USD": [], "EUR/JPY": [], "GBP/JPY": []}

# gauge percent computed from support/resistance leading numbers vs quote
GAUGE = {"EUR/USD": ("0", "1.1551", "1.1582"), "USD/JPY": ("91", "152.63", "154.75"),
         "AUD/USD": ("72", "0.7102", "0.7141"), "GBP/USD": ("15", "1.3483", "1.3565"),
         "EUR/JPY": ("0", "178.52", "179.10"), "GBP/JPY": ("50", "207.29", "209.82")}
# conviction score = round(R*3) clamped to [3,10]; 0 for WAIT pairs
TIER = {"EUR/USD": ("7/10", "", 7), "USD/JPY": ("0/10", "t-mod", 0),
        "AUD/USD": ("0/10", "t-mod", 0), "GBP/USD": ("0/10", "t-mod", 0),
        "EUR/JPY": ("0/10", "t-mod", 0), "GBP/JPY": ("0/10", "t-mod", 0)}

# verdict flips today: EUR/USD sell-pullback -> sell-breakout (text only); AUD/USD buy -> wait
BADGE = {
    "EUR/USD": ('<span class="verdict-badge sell">\n                                    <span class="lang-en">SELL (SHORT) ON BREAKOUT</span>\n                                    <span class="lang-pt" style="display:none;">VENDA (SHORT) NO ROMPIMENTO</span>\n                                </span>',
                []),
    "AUD/USD": ('<span class="verdict-badge wait">\n                                    <span class="lang-en">WAIT FOR ANOTHER TRIGGER</span>\n                                    <span class="lang-pt" style="display:none;">AGUARDAR OUTRO GATILHO</span>\n                                </span>',
                [("buy", "wait")]),
}

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

# Resolve the two live tickets against the 14/09 close:
# EUR/USD short pullback (11/09): validity ended at the 14/09 close with the zone never
# printing — the close (1.1551) went straight through the 1.1578 shelf -> revoked, re-mapped.
# AUD/USD long retest (11/09): the kill condition printed — the 14/09 close (0.7130) broke
# the 0.7141 zone floor -> revoked.
resolved = []
for t in led["watching"]:
    if t["pair"] == "EUR/USD":
        t["note"] = "revoked in the 14/09 edition: validity expired at the 14/09 close with the zone never printing — the close (1.1551, -0.35%) broke straight through the 10-day low (1.1578) instead; re-mapped one shelf lower as a breakout short (<1.1551)"
        t.update({"outcome": "revoked", "exitDate": "14/09/2026", "entryDate": None, "realizedR": None})
        resolved.append(t)
    elif t["pair"] == "AUD/USD":
        t["note"] = "revoked in the 14/09 edition: the kill condition printed — the 14/09 close (0.7130, -0.60%) broke the 0.7141 zone floor; three down sessions (-1.31% from 0.7225) turned the retest into a local breakdown and the re-priced shelf (0.7076-0.7102) pays under 1:2 with the broken zone overhead — reassess after the FOMC (15-16/09)"
        t.update({"outcome": "revoked", "exitDate": "14/09/2026", "entryDate": None, "realizedR": None})
        resolved.append(t)
    else:
        print("FAIL: unexpected watching ticket for", t["pair"]); sys.exit(1)
assert len(resolved) == 2
led["watching"] = []
led["closed"].extend(resolved)

# Append: EUR/USD short breakout — confirmed 10-day Donchian breakdown, one shelf lower.
led["watching"].append({
    "pair": "EUR/USD",
    "reportDate": TS_DATE,
    "direction": "short",
    "setup": "breakout",
    "entry": 1.155,
    "stop": 1.16,
    "target": 1.144,
    "plannedR": 2.2,
    "triggerRule": "daily close under the 10-day Donchian low 1.1551 (entry reference 1.1550); valid through the 15/09 close — inside the FOMC (15-16/09) 24h window, reassess after the event",
    "note": "confirmed 10-day breakdown: the 14/09 close (1.1551, -0.35%) took out the 10/20-day lows (1.1578/1.1576) and the 61.8% Fib (1.1582) in one go; stop 50 pips over the broken cluster + the 1.1600 round (>= the 46-pip 1.5-sigma20 floor); target 1.1440 under the 78.6% Fib (1.1476) / 1.1450 round, above the 9-month low (1.1340)"
})
assert len(led["watching"]) == 1
assert len([t for t in led["watching"] if t["pair"] == "EUR/USD"]) == 1

with open(LED, "w", encoding="utf-8") as f:
    json.dump(led, f, ensure_ascii=False, indent=2)
print("OK: track-record.json (EUR/USD + AUD/USD revoked, EUR/USD breakout short appended)")

# =====================================================================
# 4. news.html — hero dateline + new wire cards + basis note
# =====================================================================
NP = DOCS + "/news.html"
nh = open(NP, encoding="utf-8").read()
nh = rep(nh, '<span class="lang-en">Wire updated: ' + OLD_TS + '</span>', '<span class="lang-en">Wire updated: ' + TS + '</span>', "news hero en")
nh = rep(nh, '<span class="lang-pt" style="display:none;">Telégrafo atualizado em: ' + OLD_TS + '</span>', '<span class="lang-pt" style="display:none;">Telégrafo atualizado em: ' + TS + '</span>', "news hero pt")
nh = rep(nh, "numbers and dates reflect the report's data basis of 11/09/2026", "numbers and dates reflect the report's data basis of 14/09/2026", "news note en")
nh = rep(nh, "refletem a base de dados do relatório de 11/09/2026", "refletem a base de dados do relatório de 14/09/2026", "news note pt")

NEWS_CARDS = '''                <!-- News 0: Dollar opens FOMC week on the front foot — both tickets off the book -->
                <article class="news-card">
                    <div class="news-card-top">
                        <span class="news-cat"><span class="lang-en">Market Flow</span><span class="lang-pt" style="display:none;">Fluxo de Mercado</span></span>
                        <span class="impact-badge high"><span class="lang-en">High Impact</span><span class="lang-pt" style="display:none;">Impacto Alto</span></span>
                        <span class="news-date">14/09/2026</span>
                    </div>
                    <h2 class="news-title">
                        <span class="lang-en">Dollar opens FOMC week on the front foot: EUR/USD breaks the 10-day low and both Friday tickets come off the book</span>
                        <span class="lang-pt" style="display:none;">Dólar abre a semana do FOMC na frente: EUR/USD rompe a mínima de 10 pregões e os dois tickets de sexta saem do livro</span>
                    </h2>
                    <p class="news-summary">
                        <span class="lang-en">Monday swept the desk's two live tickets in one session. EUR/USD fell -0.35% to 1.1551 — a third straight down close straight through the 10/20-day lows (1.1578/1.1576) and the 61.8% Fib (1.1582): the confirmed breakdown expired the 1.1631-1.1657 pullback short unfired and re-mapped the book one shelf lower — short a daily close under 1.1551, stop 1.1600, target 1.1440 (1:2.20), valid through the Sep 15 close. AUD/USD fared worse: -0.60% to 0.7130, a third down session (-1.31% from the 0.7225 top) that broke the 0.7141 floor and killed the retest ticket by its own condition — the next shelf (0.7076-0.7102, 20-day low + 23.6% Fib) pays under 1:2 with the broken zone overhead, so the pair moves to WAIT.</span>
                        <span class="lang-pt" style="display:none;">A segunda-feira varreu os dois tickets vivos numa sessão só. O EUR/USD caiu -0,35% para 1,1551 — terceiro fechamento de queda seguido, varrendo as mínimas de 10/20 pregões (1.1578/1.1576) e a Fib 61,8% (1.1582): o rompimento confirmado expirou sem disparar o curto do repique 1.1631-1.1657 e rearmou o mapa uma casa abaixo — venda em fechamento sob 1.1551, stop 1.1600, alvo 1.1440 (1:2,20), válida até o fechamento de 15/09. O AUD/USD foi pior: -0,60% para 0,7130, terceiro pregão de queda (-1,31% desde o topo de 0,7225), quebrou o piso 0,7141 e matou o ticket do reteste pela própria condição — a prateleira seguinte (0.7076-0.7102, mínima de 20 pregões + Fib 23,6%) paga menos de 1:2 com a zona quebrada no caminho, e o par migra para AGUARDAR.</span>
                    </p>
                    <div class="news-take">
                        <span class="take-tag"><span class="lang-en">Desk take</span><span class="lang-pt" style="display:none;">Leitura da mesa</span></span>
                        <span class="lang-en">The ledger records it plainly: one ticket expired unfired — the pullback never came — and one was killed by its own close-condition. What remains directional is the breakdown itself, and only until the FOMC 24h window shuts it: the short needs its own confirming close under 1.1551, and nothing is chased two sessions before the committee.</span>
                        <span class="lang-pt" style="display:none;">O livro registra sem drama: um ticket expirou sem disparar — o repique nunca veio — e outro morreu pela própria condição de fechamento. O que resta direcional é o próprio rompimento, e só até a janela de 24h do FOMC fechá-lo: o curto exige seu fechamento confirmatório sob 1,1551 e nada é perseguido a duas sessões do comitê.</span>
                    </div>
                    <div class="news-pairs">
                        <span class="np-label"><span class="lang-en">Watch</span><span class="lang-pt" style="display:none;">Acompanhar</span></span>
                        <a href="eur-usd.html" class="pair-link-chip">EUR/USD</a>
                        <a href="aud-usd.html" class="pair-link-chip">AUD/USD</a>
                    </div>
                </article>

                <!-- News 1: FOMC week opens — three decisions in 72 hours -->
                <article class="news-card">
                    <div class="news-card-top">
                        <span class="news-cat"><span class="lang-en">Central Banks</span><span class="lang-pt" style="display:none;">Bancos Centrais</span></span>
                        <span class="impact-badge high"><span class="lang-en">High Impact</span><span class="lang-pt" style="display:none;">Impacto Alto</span></span>
                        <span class="news-date">14/09/2026</span>
                    </div>
                    <h2 class="news-title">
                        <span class="lang-en">FOMC week opens with a split market: ~60% hike odds into Wednesday's decision, BoE and BoJ follow within 48 hours</span>
                        <span class="lang-pt" style="display:none;">Semana do FOMC abre com o mercado dividido: ~60% de alta em pauta para quarta, BoE e BoJ nas 48h seguintes</span>
                    </h2>
                    <p class="news-summary">
                        <span class="lang-en">The Sep 15-16 FOMC tops the event filter this week: with the Fed at 3.50-3.75% and August's hot headline CPI (+0.4% m/m; 3.4% y/y, core cooling to 2.4% y/y) keeping the hike in play (~60% priced, with prediction venues split as wide as 46-85%), no new directional entry inside the 24h window — the EUR/USD breakout short runs only through the Sep 15 close. The BoE (Sep 17, 3.75%, last vote 6-3) re-prices cable's capped map; the BoJ (Sep 17-18, ~80% priced for +25 bp to 1.25%) decides the yen crosses with the MoF on alert since the July joint intervention — the 2.5-sigma20 floors (235-303 pips) keep all three yen pairs on WAIT.</span>
                        <span class="lang-pt" style="display:none;">O FOMC de 15-16/09 lidera o filtro de eventos da semana: com o Fed a 3,50-3,75% e o CPI quente de agosto (+0,4% m/m; 3,4% a/a, núcleo esfriando a 2,4% a/a) mantendo a alta em pauta (~60% precificados, com casas de previsão divididas entre 46% e 85%), nenhuma entrada direcional nova dentro da janela de 24h — o curto de rompimento do EUR/USD vale só até o fechamento de 15/09. O BoE (17/09, 3,75%, último voto 6-3) reprecifica o mapa travado do cable; o BoJ (17-18/09, ~80% para +25 pb, a 1,25%) decide os cruzamentos com iene com o MoF em alerta desde a intervenção conjunta de julho — os pisos de 2,5σ20 (235-303 pips) mantêm os três pares em AGUARDAR.</span>
                    </p>
                    <div class="news-take">
                        <span class="take-tag"><span class="lang-en">Desk take</span><span class="lang-pt" style="display:none;">Leitura da mesa</span></span>
                        <span class="lang-en">Three decisions in 72 hours re-price every map on the book: the EUR/USD short hands the baton to the FOMC, cable waits for the BoE, and the yen pairs wait for the BoJ — the report does not stand in front of the committee, and even less in front of the MoF.</span>
                        <span class="lang-pt" style="display:none;">Três decisões em 72 horas reprecificam todos os mapas do livro: o curto do EUR/USD passa o bastão ao FOMC, o cable espera o BoE e os pares com iene esperam o BoJ — o relatório não fica na frente do comitê e muito menos do MoF.</span>
                    </div>
                    <div class="news-pairs">
                        <span class="np-label"><span class="lang-en">Watch</span><span class="lang-pt" style="display:none;">Acompanhar</span></span>
                        <a href="eur-usd.html" class="pair-link-chip">EUR/USD</a>
                        <a href="usd-jpy.html" class="pair-link-chip">USD/JPY</a>
                        <a href="gbp-usd.html" class="pair-link-chip">GBP/USD</a>
                    </div>
                </article>

'''
nh = rep(nh, "                <!-- News 0: ECB sell-the-fact — failed reclaim restores the bear regime -->", NEWS_CARDS + "                <!-- News 0: ECB sell-the-fact — failed reclaim restores the bear regime -->", "news card prepend")
open(NP, "w", encoding="utf-8").write(nh)
print("OK: news.html (dateline, 2 new cards, basis note)")

# =====================================================================
# 5. patch verify_all.py to the new edition
# =====================================================================
VP = r"C:/Projetos/forex-report/pipeline/verify_all.py"
v = open(VP, encoding="utf-8").read()
v = rep(v, 'TODAY_TS = "11/09/2026 17:15 UTC"', 'TODAY_TS = "' + TS + '"', "verify TODAY_TS")
v = rep(v, 'TODAY_DATE = "11/09/2026"  # basis session date (report edition: 11/09/2026)', 'TODAY_DATE = "14/09/2026"  # basis session date (report edition: 14/09/2026)', "verify TODAY_DATE")
v = rep(v, '''TICKER = [("EUR/USD","-0.21%"),("USD/JPY","-0.09%"),("AUD/USD","-0.17%"),
          ("GBP/USD","-0.09%"),("EUR/JPY","-0.30%"),("GBP/JPY","-0.18%")]''',
        '''TICKER = [("EUR/USD","-0.35%"),("USD/JPY","+0.33%"),("AUD/USD","-0.60%"),
          ("GBP/USD","-0.10%"),("EUR/JPY","-0.02%"),("GBP/JPY","+0.23%")]''', "verify TICKER")
v = rep(v, 'for stale in ["02/09/2026", "01/09/2026", "19/08/2026", "18/08/2026", "17/08/2026", "14/08/2026", "13/08/2026", "04/09/2026", "07/09/2026", "09/09/2026"]:',
        'for stale in ["02/09/2026", "01/09/2026", "19/08/2026", "18/08/2026", "17/08/2026", "14/08/2026", "13/08/2026", "04/09/2026", "07/09/2026", "09/09/2026", "11/09/2026"]:', "verify static stale")
open(VP, "w", encoding="utf-8").write(v)
print("OK: verify_all.py patched to the 14/09/2026 edition")

print(f"\nDONE {TS} — run verify_all.py next.")
