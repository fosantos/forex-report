#!/usr/bin/env python3
"""Daily regeneration for the 11/09/2026 edition — ECB/Frankfurter basis
(the logged-in MT5 terminal still returns no FX data — Python copy_rates_range and the
MCP bridge both fail with 'Terminal: Call failed'; compute_indicators fell back).
Basis: ECB/Frankfurter reference rates, 540 sessions 01/08/2024-11/09/2026 (last close: 11/09/2026).
Session: the events resolved — ECB HIKED +25 bp to 2.50% on 10/09 and the euro fell anyway
(sold-the-fact + Friday's hot US CPI: +0.4% m/m headline, 3.4% y/y, core 2.4% y/y cooling,
Fed hike odds ~60% into the 15-16/09 FOMC). EUR/USD -0.21% to 1.1592 — failed SMA200 reclaim
(one close over on 09/09, two back under) -> bear alignment restored -> SHORT PULLBACK ticket
re-armed at 1.1631-1.1657 (entry 1.1640, stop 1.1685, target SMA50 1.1527, 1:2.51), valid
through the 14/09 close (FOMC window caveat). USD/JPY 154.04: Thursday's bounce (+0.59%) died
on CPI; floor 2.5sigma20=235p vs 9-mo low 141p below -> WAIT (BoJ 17-18/09 ~80% priced +25bp).
AUD/USD 0.7173: two-day -0.72% pullback — the retest IS underway; ticket CARRIED unchanged
(buy 0.7141-0.7162, stop 0.7110, target 0.7257, 1:2.27), caveat swapped CPI->FOMC.
GBP/USD 1.3508: double rejection at 1.3565-1.3566; nearest target pays 1:1.47 -> WAIT for
FOMC/BoE. EUR/JPY 178.56: third 9-month low printed AFTER the ECB hike -> WAIT (floor 241p).
GBP/JPY 208.08: bounce capped under the re-priced 78.6% Fib (209.70) -> WAIT (floor 304p).
Verdicts: EUR/USD SELL pullback; AUD/USD BUY pullback; USD/JPY, GBP/USD, EUR/JPY, GBP/JPY WAIT.
Also prepends 3 wire items (ECB sell-the-fact / hot CPI / yen into the BoJ) to the news digest
+ news.html, trims the 3 past events off the week-ahead calendar strip, and patches
verify_all.py to the new stamp/ticker/stale dates. Aborts on any structural mismatch."""
import re, json, sys
from datetime import datetime, timezone

DOCS = r"C:/Projetos/forex-report/docs"
TS_DATE = "11/09/2026"
now = datetime.now(timezone.utc)
TS = TS_DATE + " " + now.strftime("%H:%M") + " UTC"
OLD_TS = "09/09/2026 20:54 UTC"

BASIS_EN_AMP = "ECB/Frankfurter reference rates · SMA50/200, sigma20 &amp; Donchian computed · 540 daily sessions (01/08/2024–11/09/2026)."
BASIS_PT = "taxas de referência BCE/Frankfurter · SMA50/200, σ20 e Donchian calculados · 540 pregões (01/08/2024 a 11/09/2026)."

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
    "quote": "1.1592", "bias": "BAIXA", "biasType": "bear",
    "pt": {
      "fundamental": "O EUR/USD fechou em 1,1592 na sessão de 11/09/2026 (taxa de referência BCE/Frankfurter; o terminal MT5 logado segue sem retornar dados de FX), caindo -0,21% — segundo fechamento de queda seguido após a recaptura falhada da SMA200: o BCE subiu 25 pb em 10/09 (depósito a 2,50%, o segundo alta desde o choque energético) e o euro caiu mesmo assim, vendido no fato contra um dólar turbinado pelo CPI de agosto (+0,4% m/m; 3,4% a/a; núcleo 2,4% a/a, esfriando) que manteve a alta do Fed em pauta (odds ~60%, FOMC 15-16/09). Com o fechamento de volta sob a SMA200 (1,1631) e a SMA50 (1,1527) ainda abaixo dela, o alinhamento volta a ser plenamente de baixa — e a zona de venda 1.1631-1.1657 (SMA200 + Fib 50%), desarmada na quarta pela recaptura, volta ao mapa. O fechamento parou a 14 pips da mínima de 10 pregões (1,1578), com a Fib 61,8% (1,1582) no caminho. Indicadores (SMA 50/200, σ20, Donchian e Fibonacci) calculados da série diária BCE/Frankfurter (540 pregões, 01/08/2024 a 11/09/2026).",
      "trend": "Fechamento sob a SMA200 (1,1631) com a SMA50 (1,1527) abaixo — alinhamento de baixa restaurado: a recaptura de 09/09 durou um pregão e o CPI dos EUA devolveu o regime; a mínima de 10 pregões (1,1578) e a Fib 61,8% (1,1582) são os pisos imediatos.",
      "support": "1.1578 (mínima de 10 pregões), com a Fib 61,8% (1.1582), a mínima de 20 pregões (1.1576), a SMA50 (1.1527) e o redondo 1.1500 abaixo.",
      "resistance": "1.1631 (SMA200), com a Fib 50% (1.1657) e a máxima de 20 pregões (1.1699) acima.",
      "priceAction": "Setup de venda no repique da zona 1.1631-1.1657 (SMA200 + Fib 50%): aguardar fechamento diário dentro da zona seguido de fechamento abaixo do fechamento anterior e do midpoint (1,1644) — entrada de referência 1.1640, stop 1.1685 (sobre a zona e a máxima de 09/09; 45 pips ≥ piso 1,5σ20 de ~45 pips), alvo 1.1527 (SMA50), cruzando o cluster 1.1576-1.1582. Fechamento sob 1.1578 sem o repique rearmaria o mapa uma casa abaixo.",
      "recommendation": "VENDA (SHORT) NA RETRAÇÃO",
      "trigger": "Fechamento diário dentro da zona 1.1631-1.1657 (SMA200 + Fib 50%) seguido de fechamento abaixo do fechamento anterior e do midpoint 1,1644 — entrada de referência 1.1640. Válido até o fechamento de 14/09; dentro da janela de 24h do FOMC (15-16/09), reavaliar após o evento.",
      "stop": "1.1685 (sobre a zona 1.1631-1.1657 e a máxima de 09/09; 45 pips ≥ piso 1,5σ20 de ~45 pips) · risco sugerido ≤ 1% por operação.",
      "target": "1.1527 (SMA50), com o cluster 1.1576-1.1582 no caminho.",
      "rr": "1:2.51", "rrValue": 63,
      "justification": "A recaptura durou um pregão: o BCE entregou o alta e o euro caiu — quando o preço ignora o fato hawkish, o fato relevante é o fluxo. A regra realinha o viés para baixa (fechamento sob a SMA200 com a SMA50 abaixo) e repõe o curto na mesma zona de sempre, agora com o CPI já passado: vender o repique de 1.1631-1.1657 com stop estrutural sobre a zona paga 1:2.51 (113 pips contra 45) até a SMA50. O FOMC de 15-16/09 é a única janela aberta — o ticket vale até o fechamento de 14/09."
    },
    "en": {
      "fundamental": "EUR/USD closed at 1.1592 in the 11/09/2026 session (ECB/Frankfurter reference rate; the logged-in MT5 terminal still returns no FX data), down -0.21% — a second straight down close after the failed SMA200 reclaim: the ECB hiked 25 bp on Sep 10 (deposit to 2.50%, the second hike since the energy shock) and the euro fell anyway, sold on the fact against a dollar turbocharged by August CPI (+0.4% m/m; 3.4% y/y; core 2.4% y/y, cooling) that kept the Fed hike in play (~60% odds, FOMC Sep 15-16). With the close back under the 200-day SMA (1.1631) and the 50-day (1.1527) still below it, the alignment turns fully bearish again — and the 1.1631-1.1657 selling zone (SMA200 + 50% Fib), disarmed on Wednesday by the reclaim, returns to the map. The close stopped 14 pips above the 10-day low (1.1578), with the 61.8% Fib (1.1582) in the way. Indicators (SMA 50/200, sigma20, Donchian and Fibonacci) computed from the ECB/Frankfurter daily series (540 sessions, 01/08/2024 to 11/09/2026).",
      "trend": "Close under the 200-day SMA (1.1631) with the 50-day (1.1527) below — bear alignment restored: the Sep 9 reclaim lasted one session and US CPI handed the regime back; the 10-day low (1.1578) and the 61.8% Fib (1.1582) are the immediate floors.",
      "support": "1.1578 (10-day low), with the 61.8% Fib (1.1582), the 20-day low (1.1576), the 50-day SMA (1.1527) and the 1.1500 round beneath.",
      "resistance": "1.1631 (SMA200), with the 50% Fib (1.1657) and the 20-day high (1.1699) above.",
      "priceAction": "Short-the-pullback setup into the 1.1631-1.1657 zone (SMA200 + 50% Fib): wait for a daily close inside the zone followed by a close below the previous close and the midpoint (1.1644) — entry reference 1.1640, stop 1.1685 (over the zone and the Sep 9 high; 45 pips >= the ~45-pip 1.5-sigma20 floor), target 1.1527 (50-day SMA), crossing the 1.1576-1.1582 cluster. A close under 1.1578 without the pullback would re-map the book one shelf lower.",
      "recommendation": "SELL (SHORT) ON PULLBACK",
      "trigger": "Daily close inside the 1.1631-1.1657 zone (SMA200 + 50% Fib) followed by a close below the previous close and the 1.1644 midpoint — entry reference 1.1640. Valid through the Sep 14 close; inside the FOMC (Sep 15-16) 24h window, reassess after the event.",
      "stop": "1.1685 (over the 1.1631-1.1657 zone and the Sep 9 high; 45 pips >= the ~45-pip 1.5-sigma20 floor) · suggested risk ≤ 1% per trade.",
      "target": "1.1527 (50-day SMA), with the 1.1576-1.1582 cluster on the way.",
      "rr": "1:2.51", "rrValue": 63,
      "justification": "The reclaim lasted one session: the ECB delivered the hike and the euro fell — when price ignores the hawkish fact, the fact that matters is the flow. The rule re-aligns the bias bearish (close under the SMA200 with the 50-day below) and puts the short back at the same old zone, now with CPI behind us: selling the 1.1631-1.1657 pullback with a structural stop over the zone pays 1:2.51 (113 pips against 45) down to the 50-day SMA. The Sep 15-16 FOMC is the only open window — the ticket runs through the Sep 14 close."
    }
  },
  "USD/JPY": {
    "quote": "154.04", "bias": "BAIXA", "biasType": "bear",
    "pt": {
      "fundamental": "O USD/JPY fechou em 154,04 na sessão de 11/09/2026 (taxa de referência BCE/Frankfurter; o terminal MT5 logado segue sem retornar dados de FX), caindo -0,09% — o repique de quinta (+0,59%, primeiro fechamento de alta em cinco pregões) não sobreviveu ao CPI quente dos EUA (+0,4% m/m; 3,4% a/a), que manteve a alta do Fed em pauta (odds ~60%, FOMC 15-16/09) contra um BoJ que o mercado já precifica ~80% para +25 pb (para 1,25%) em 17-18/09. A leitura segue BAIXA (rompimento confirmado desde a edição de 07/09; a mínima de 10/20 pregões segue em 153,27) e a geometria segue bloqueada: com σ20 a 94 pips, o piso de intervenção 2,5σ20 vale 235 pips — uma venda em 154,04 exigiria alvo a ~470 pips (149,34), sob a mínima de 9 meses (152,63), onde só resta o redondo 150,00. O MoF segue em alerta desde a intervenção de julho; a 141 pips da mínima de 9 meses, o risco de intervenção segue máximo. Indicadores calculados da série diária BCE/Frankfurter (540 pregões, 01/08/2024 a 11/09/2026).",
      "trend": "Fechamento sob a SMA200 (158,36) e sob a SMA50 (159,79), com a SMA50 ainda acima da SMA200 — o rompimento confirmado das mínimas de 10/20 pregões mantém a resolução para baixo: leitura de baixa com o repique travado sob 154,18, a 141 pips da mínima de 9 meses (152,63).",
      "support": "152.63 (mínima de 9 meses), com o redondo 152.50 abaixo — 153.27 (mínima de 10/20 pregões) é a primeira defesa.",
      "resistance": "154.75 (fechamento de segunda) / 154.18 (fechamento de quinta), com a Fib 78,6% / redondo (155.04-155.00) e a mínima quebrada de 03/09 (156.01) acima.",
      "priceAction": "Sem entrada — o CPI travou o repique e a perseguição continua reprovada: com σ20 = 94 pips, o piso de intervenção (2,5σ20 = 235 pips) exige alvo a ~149,35 e a única âncora no caminho é o redondo 150,00 (terceiro nível). Vender a 141 pips da mínima de 9 meses com o MoF em alerta é entregar o stop ao interveniente. Rearmar: compressão da σ20, base sobre 152.63/152.50 ou retração com estrutura até 155.04-156.01. FOMC 15-16/09 e BoJ 17-18/09 são os árbitros.",
      "recommendation": "AGUARDAR OUTRO GATILHO",
      "trigger": "Nenhum — o piso de intervenção (2,5σ20 = 235 pips) reprova a venda a 141 pips da mínima de 9 meses e a compra não tem estrutura sob as médias. Assistir à reação sobre 152.63 e à compressão da σ20; FOMC (15-16/09) e BoJ (17-18/09) decidem o próximo capítulo.",
      "stop": "N/A (sem operação).",
      "target": "N/A (sem operação).",
      "rr": "N/A", "rrValue": 0,
      "justification": "Dois hawkish e um repique morto: o CPI quente devolveu o vento americano, o BoJ a ~80% para +25 pb segura o iene, e o par fecha a semana comprimido entre a mínima de 9 meses e o repique travado. O piso de intervenção (235 pips) não negocia: mirar ~470 pips abaixo cai em território sem estrutura — só o redondo 150,00. Entre FOMC e BoJ na mesma semana, evento decide; o relatório não paga o prêmio de ficar na frente do MoF."
    },
    "en": {
      "fundamental": "USD/JPY closed at 154.04 in the 11/09/2026 session (ECB/Frankfurter reference rate; the logged-in MT5 terminal still returns no FX data), down -0.09% — Thursday's bounce (+0.59%, the first up close in five sessions) did not survive the hot US CPI (+0.4% m/m; 3.4% y/y), which kept the Fed hike in play (~60% odds, FOMC Sep 15-16) against a BoJ now ~80% priced for +25 bp (to 1.25%) on Sep 17-18. The read stays BEAR (confirmed breakdown since the Sep 7 edition; the 10/20-day low still sits at 153.27) and the geometry stays blocked: with sigma20 at 94 pips the 2.5-sigma20 intervention floor is worth 235 pips — a short from 154.04 would need a target ~470 pips lower (149.34), under the 9-month low (152.63), where only the 150.00 round remains. The MoF stays on alert since the July intervention; 141 pips above a 9-month low, intervention risk stays maximal. Indicators computed from the ECB/Frankfurter daily series (540 sessions, 01/08/2024 to 11/09/2026).",
      "trend": "Close under the 200-day SMA (158.36) and under the 50-day (159.79), with the 50-day still above the 200-day — the confirmed break of the 10/20-day lows keeps the resolution bearish: a bear read with the bounce capped under 154.18, 141 pips above the 9-month low (152.63).",
      "support": "152.63 (9-month low), with the 152.50 round beneath — 153.27 (the 10/20-day low) is the first defense.",
      "resistance": "154.75 (Monday's close) / 154.18 (Thursday's close), with the 78.6% Fib / round (155.04-155.00) and the broken Sep 3 low (156.01) above.",
      "priceAction": "No entry — CPI killed the bounce and the chase stays rejected: with sigma20 = 94 pips, the intervention floor (2.5-sigma20 = 235 pips) demands a target at ~149.35 and the only anchor on the way is the 150.00 round (tier three). Selling 141 pips above the 9-month low with the MoF on alert is handing the stop to the intervenor. Re-arm: sigma20 compression, a base over 152.63/152.50, or a structured pullback to 155.04-156.01. The FOMC Sep 15-16 and BoJ Sep 17-18 are the arbiters.",
      "recommendation": "WAIT FOR ANOTHER TRIGGER",
      "trigger": "None — the intervention floor (2.5-sigma20 = 235 pips) rejects a short 141 pips above the 9-month low and a long has no structure under the averages. Watch the reaction at 152.63 and sigma20 compression; the FOMC (Sep 15-16) and BoJ (Sep 17-18) decide the next chapter.",
      "stop": "N/A (no trade).",
      "target": "N/A (no trade).",
      "rr": "N/A", "rrValue": 0,
      "justification": "Two hawks and one dead bounce: the hot CPI handed the wind back to the dollar, the BoJ at ~80% for +25 bp holds the yen, and the pair closes the week compressed between the 9-month low and a capped bounce. The intervention floor (235 pips) does not negotiate: aiming ~470 pips lower lands in structureless territory — only the 150.00 round. With the FOMC and the BoJ in the same week, the event decides; the report does not pay the premium of standing in front of the MoF."
    }
  },
  "AUD/USD": {
    "quote": "0.7173", "bias": "ALTA", "biasType": "bull",
    "pt": {
      "fundamental": "O AUD/USD fechou em 0,7173 na sessão de 11/09/2026 (taxa de referência BCE/Frankfurter; o terminal MT5 logado segue sem retornar dados de FX), caindo -0,17% — segundo pregão de queda seguido (-0,72% desde o topo de 0,7225), com o CPI quente dos EUA (+0,4% m/m; 3,4% a/a) derrubando o bloco de commodities do topo de 20 pregões. O reteste que o ticket esperava está em curso: a retração já devolveu o nível rompido (0,7195-0,7204) e a zona de compra 0.7141-0.7162 fica 11-32 pips abaixo. O alinhamento segue pleno de alta (SMA50 0,7066 > SMA200 0,6991; preço acima das duas) e o motor é o mesmo: diferencial da RBA (4,35%, próxima reunião 29/09; bancos projetam 4,60% em novembro), CPI australiano a 3,5% e WTI ~US$ 83. O ticket segue no livro, com a ressalva do CPI trocada pela janela do FOMC (15-16/09). Indicadores calculados da série diária BCE/Frankfurter (540 pregões, 01/08/2024 a 11/09/2026).",
      "trend": "Acima das SMA50 (0,7066) e SMA200 (0,6991) — alinhamento de alta pleno; a retração de dois pregões devolveu o nível rompido (0,7195) e busca a zona de reteste 0.7141-0.7162, com a máxima de 9 meses (0,7257) como teto estrutural.",
      "support": "0.7141 (mínima de 10 pregões), com a Fib 23,6% (0.7102), a mínima de 20 pregões (0.7076) e a SMA50 (0.7066) abaixo.",
      "resistance": "0.7225 (máxima de 10/20 pregões), com o nível rompido (0.7195-0.7204) no meio do caminho e a máxima de 9 meses (0.7257) acima.",
      "priceAction": "Setup de compra no reteste pós-rompimento (carregado): aguardar fechamento diário dentro da zona 0.7141-0.7162 (mínima D10 / redondo 0,7150) seguido de fechamento de alta acima do midpoint (0,7152) — entrada de referência 0.7155, stop 0.7110 (sob a base do rompimento; 45 pips ≥ piso 1,5σ20 de ~42 pips), alvo 0.7257 (máxima de 9 meses). Fechamento sob 0.7141 cancela o setup; disparo dentro da janela de 24h do FOMC (15-16/09): reavaliar após o evento.",
      "recommendation": "COMPRA (LONG) NA RETRAÇÃO",
      "trigger": "Fechamento diário dentro da zona 0.7141-0.7162 (mínima D10 / redondo 0,7150) seguido de fechamento acima do fechamento anterior e do midpoint 0,7152 — entrada de referência 0.7155. Válido até o fechamento de 14/09; dentro da janela de 24h do FOMC (15-16/09), reavaliar após o evento.",
      "stop": "0.7110 (sob a mínima de 10 pregões 0.7141, base do rompimento; 45 pips ≥ 1,5σ20 de ~42 pips) · risco sugerido ≤ 1% por operação.",
      "target": "0.7257 (máxima de 9 meses), com o nível rompido (0.7195-0.7204) virando resistência no caminho.",
      "rr": "1:2.27", "rrValue": 57,
      "justification": "O reteste deixou de ser tese e virou preço: dois pregões de queda devolveram o nível rompido e apontam para a zona 0.7141-0.7162 — a entrada disciplinada que o livro espera desde 04/09. Comprar a zona com stop sob ela paga 1:2.27 (102 pips contra 45) com o diferencial da RBA a favor; perseguir a partir daqui continua pagando menos de 1:1. A ressalva migra do CPI para o FOMC (15-16/09): o ticket vale até o fechamento de 14/09. A vantagem segue com quem espera."
    },
    "en": {
      "fundamental": "AUD/USD closed at 0.7173 in the 11/09/2026 session (ECB/Frankfurter reference rate; the logged-in MT5 terminal still returns no FX data), down -0.17% — a second straight down session (-0.72% from the 0.7225 top), with the hot US CPI (+0.4% m/m; 3.4% y/y) knocking the commodity bloc off its 20-day high. The retest the ticket was waiting for is underway: the pullback has already handed back the broken level (0.7195-0.7204) and the buying zone 0.7141-0.7162 sits 11-32 pips below. The alignment stays fully bullish (50-day 0.7066 > 200-day 0.6991; price above both) and the engine is the same: the RBA differential (4.35%, next meeting Sep 29; banks project 4.60% by November), Australian CPI at 3.5% and WTI ~$83. The ticket stays on the book, with the CPI caveat swapped for the FOMC (Sep 15-16) window. Indicators computed from the ECB/Frankfurter daily series (540 sessions, 01/08/2024 to 11/09/2026).",
      "trend": "Above the 50-day (0.7066) and 200-day (0.6991) SMAs — full bull alignment; the two-session pullback handed back the broken level (0.7195) and seeks the 0.7141-0.7162 retest zone, with the 9-month high (0.7257) as the structural cap.",
      "support": "0.7141 (10-day low), with the 23.6% Fib (0.7102), the 20-day low (0.7076) and the 50-day SMA (0.7066) beneath.",
      "resistance": "0.7225 (10/20-day high), with the broken level (0.7195-0.7204) halfway and the 9-month high (0.7257) above.",
      "priceAction": "Post-breakout retest long setup (carried): wait for a daily close inside the 0.7141-0.7162 zone (D10 low / 0.7150 round) followed by a higher close above the midpoint (0.7152) — entry reference 0.7155, stop 0.7110 (under the breakout base; 45 pips >= the ~42-pip 1.5-sigma20 floor), target 0.7257 (9-month high). A close under 0.7141 cancels the setup; a trigger inside the FOMC (Sep 15-16) 24h window: reassess after the event.",
      "recommendation": "BUY (LONG) ON PULLBACK",
      "trigger": "Daily close inside the 0.7141-0.7162 zone (D10 low / 0.7150 round) followed by a close above the previous close and the 0.7152 midpoint — entry reference 0.7155. Valid through the Sep 14 close; inside the FOMC (Sep 15-16) 24h window, reassess after the event.",
      "stop": "0.7110 (under the 10-day low 0.7141, the breakout base; 45 pips >= the ~42-pip 1.5-sigma20 floor) · suggested risk ≤ 1% per trade.",
      "target": "0.7257 (9-month high), with the broken level (0.7195-0.7204) turning into resistance on the way.",
      "rr": "1:2.27", "rrValue": 57,
      "justification": "The retest stopped being a thesis and became price: two down sessions handed back the broken level and point to the 0.7141-0.7162 zone — the disciplined entry the book has awaited since Sep 4. Buying the zone with the stop under it pays 1:2.27 (102 pips against 45) with the RBA differential behind; chasing from here still pays under 1:1. The caveat migrates from CPI to the FOMC (Sep 15-16): the ticket runs through the Sep 14 close. The edge still belongs to whoever waits."
    }
  },
  "GBP/USD": {
    "quote": "1.3508", "bias": "ALTA", "biasType": "bull",
    "pt": {
      "fundamental": "O GBP/USD fechou em 1,3508 na sessão de 11/09/2026 (taxa de referência BCE/Frankfurter; o terminal MT5 logado segue sem retornar dados de FX), caindo -0,09% — segundo fechamento de queda seguido depois da dupla rejeição no cluster 1.3565-1.3566 (máxima de 10 pregões + Fib 38,2%) que a edição anterior flagrou como alvo virando obstáculo. O alinhamento de alta segue pleno (SMA50 1,3475 > SMA200 1,3447; preço acima das duas), mas a aritmética segue reprovada: da zona reprecificada (1.3447-1.3475, midpoint 1,3461) com stop estrutural em 1.3390 (71 pips ≥ piso 1,5σ20 de ~48 pips), o cluster 1.3565-1.3566 paga 1:1,47 — e o único alvo que paga mais de 1:2 (máxima de 20 pregões, 1.3656) fica além do duplo teto rejeitado duas vezes nesta semana. O CPI dos EUA (+0,4% m/m) segurou o dólar; o BoE (17/09, 3,75%, voto 6-3) reprecifica o mapa em três pregões. Indicadores calculados da série diária BCE/Frankfurter (540 pregões, 01/08/2024 a 11/09/2026).",
      "trend": "Preço acima das SMA50 (1,3475) e SMA200 (1,3447) — alinhamento de alta pleno; a dupla rejeição no cluster 1.3565-1.3566 devolveu o par à metade da faixa, com a zona de retração 1.3447-1.3475 de volta ao radar.",
      "support": "1.3483 (mínimas de 10/20 pregões), com a confluência SMA200/SMA50 (1.3447-1.3475) e a Fib 61,8% (1.3411) abaixo.",
      "resistance": "1.3565 (máxima de 10 pregões + Fib 38,2% 1.3566 — duplo teto da semana), com a máxima de 20 pregões (1.3656) acima.",
      "priceAction": "Sem entrada — o prêmio segue sob o portão: da zona reprecificada (midpoint 1,3461), stop 1.3390 contra o cluster 1.3565-1.3566 paga 1:1,47; esticar até a máxima de 20 pregões (1.3656) cruza o duplo teto rejeitado duas vezes — bloqueio intermediário de primeira ordem. Fechamento sob a Fib 61,8% (1.3411) invalida a estrutura de alta. Rearmar: recuo da zona até os redondos (1.3400-1.3447), compressão da σ20 ou quebra limpa de 1.3566 reprecificando os alvos. FOMC (15-16/09) e BoE (17/09) arbitram.",
      "recommendation": "AGUARDAR OUTRO GATILHO",
      "trigger": "Nenhum — o alvo estrutural mais próximo paga 1:1,47 e o único alvo acima de 1:2 (1.3656) fica além do duplo teto de 1.3565-1.3566; o BoE (17/09) reprecifica o mapa em três pregões. Reavaliar após o FOMC e o BoE.",
      "stop": "N/A (sem operação).",
      "target": "N/A (sem operação).",
      "rr": "N/A", "rrValue": 0,
      "justification": "A semana entregou o cenário que o portão de R/R teme: alinhamento de alta limpo com o alvo virando obstáculo. O cluster 1.3565-1.3566 rejeitou o preço duas vezes em três pregões — usá-lo como alvo paga 1:1,47; atravessá-lo em direção a 1.3656 é pagar pedágio duas vezes. O cable segue o par mais firme contra o dólar, e é justamente por isso que a disciplina manda esperar: o FOMC (15-16/09) testa o viés e o BoE (17/09) reprecifica zona, stop e alvo de uma vez."
    },
    "en": {
      "fundamental": "GBP/USD closed at 1.3508 in the 11/09/2026 session (ECB/Frankfurter reference rate; the logged-in MT5 terminal still returns no FX data), down -0.09% — a second straight down close after the double rejection at the 1.3565-1.3566 cluster (10-day high + 38.2% Fib) that the previous edition had flagged as the target turning into an obstacle. The bull alignment stands (50-day 1.3475 > 200-day 1.3447; price above both), but the arithmetic stays rejected: from the re-priced zone (1.3447-1.3475, midpoint 1.3461) with a structural stop at 1.3390 (71 pips >= the ~48-pip 1.5-sigma20 floor), the 1.3565-1.3566 cluster pays 1:1.47 — and the only target paying over 1:2 (the 20-day high, 1.3656) sits beyond the double top rejected twice this week. US CPI (+0.4% m/m) held the dollar up; the BoE (Sep 17, 3.75%, 6-3 vote) re-prices the map in three sessions. Indicators computed from the ECB/Frankfurter daily series (540 sessions, 01/08/2024 to 11/09/2026).",
      "trend": "Price above the 50-day (1.3475) and 200-day (1.3447) SMAs — full bull alignment; the double rejection at the 1.3565-1.3566 cluster returned the pair to mid-range, with the 1.3447-1.3475 pullback zone back on the radar.",
      "support": "1.3483 (10/20-day lows), with the 200/50-day SMA confluence (1.3447-1.3475) and the 61.8% Fib (1.3411) beneath.",
      "resistance": "1.3565 (10-day high + 38.2% Fib 1.3566 — the week's double top), with the 20-day high (1.3656) above.",
      "priceAction": "No entry — the premium stays under the gate: from the re-priced zone (midpoint 1.3461), stop 1.3390 against the 1.3565-1.3566 cluster pays 1:1.47; stretching to the 20-day high (1.3656) crosses the twice-rejected double top — a first-order intermediate block. A close below the 61.8% Fib (1.3411) invalidates the bull structure. Re-arm: the zone sliding back to the rounds (1.3400-1.3447), sigma20 compression, or a clean break of 1.3566 re-pricing the targets. The FOMC (Sep 15-16) and BoE (Sep 17) arbitrate.",
      "recommendation": "WAIT FOR ANOTHER TRIGGER",
      "trigger": "None — the nearest structural target pays 1:1.47 and the only 1:2+ target (1.3656) sits beyond the 1.3565-1.3566 double top; the BoE (Sep 17) re-prices the map in three sessions. Reassess after the FOMC and the BoE.",
      "stop": "N/A (no trade).",
      "target": "N/A (no trade).",
      "rr": "N/A", "rrValue": 0,
      "justification": "The week delivered the scenario the R/R gate dreads: a clean bull alignment with the target turning into an obstacle. The 1.3565-1.3566 cluster rejected price twice in three sessions — using it as a target pays 1:1.47; crossing it toward 1.3656 means paying the toll twice. Cable remains the firmest pair against the dollar, and that is precisely why discipline says wait: the FOMC (Sep 15-16) tests the bias and the BoE (Sep 17) re-prices zone, stop and target at once."
    }
  },
  "EUR/JPY": {
    "quote": "178.56", "bias": "BAIXA", "biasType": "bear",
    "pt": {
      "fundamental": "O EUR/JPY fechou em 178,56 na sessão de 11/09/2026 (taxa de referência BCE/Frankfurter; o terminal MT5 logado segue sem retornar dados de FX), caindo -0,30% e devolvendo por completo o repique de quinta (+0,28% para 179,10) — terceira mínima de 9 meses da sequência (178,59 → 178,56), cravada depois do alta do BCE (25 pb, depósito a 2,50%): quando o falcão europeu não segura o cruzamento, o motor é o iene — o mercado precifica ~80% de +25 pb do BoJ (para 1,25%) na reunião de 17-18/09, com o MoF em alerta desde a intervenção de julho. As médias empataram (SMA50 184,163 ≈ SMA200 184,162 — cruzamento de baixa se desenhando) e a geometria segue bloqueada: σ20 a 96 pips faz o piso de intervenção 2,5σ20 valer 241 pips — uma venda exigiria alvo a ~482 pips (173,74), território sem estrutura. Indicadores calculados da série diária BCE/Frankfurter (540 pregões, 01/08/2024 a 11/09/2026).",
      "trend": "Fechamento sob a SMA200 (184,16) e sob a SMA50 (184,16), com as médias empatadas no mesmo ponto — a sequência de rompimentos (181,20 → 180,28 → 179,20 → 178,59 → 178,56) mantém a resolução para baixo: leitura de baixa em mínimas de 9 meses sucessivas, com o repique de um pregão já devolvido.",
      "support": "178.56 é o próprio fechamento — mínima de 9 meses —; abaixo, apenas os redondos 178.00 / 177.50.",
      "resistance": "179.10 (fechamento de quinta) / redondo 179.50, com a mínima quebrada de 9 meses (180.28) e as mínimas de 03-04/09 (181.20-181.59) acima.",
      "priceAction": "Sem entrada — a direção segue resolvida para baixo, mas o piso de intervenção (2,5σ20 = 241 pips) reprova a perseguição em mínima de 9 meses sem âncoras à frente; compra sob duas médias é aposta contra o BoJ. Rearmar: compressão da σ20 ou reteste estruturado de 180.28-181.20. O BoJ 17-18/09 é o árbitro — com o BCE já entregue, o desempate é todo do iene.",
      "recommendation": "AGUARDAR OUTRO GATILHO",
      "trigger": "Nenhum — o piso de intervenção (2,5σ20 = 241 pips) e a ausência de âncoras sob a mínima de 9 meses reprovam qualquer setup. Assistir à reação nos redondos 178,00 / 177,50 e à compressão da σ20; BoJ 17-18/09 arbitra.",
      "stop": "N/A (sem operação).",
      "target": "N/A (sem operação).",
      "rr": "N/A", "rrValue": 0,
      "justification": "Terceira mínima de 9 meses e desta vez com o BCE já no preço: o alta de 25 pb não comprou nem um pregão de estrutura — o repique de quinta foi devolvido inteiro na sexta. O problema segue o mesmo: o piso de intervenção (241 pips) manda procurar âncora a ~482 pips abaixo e a janela de 9 meses acabou — só restam redondos, âncoras de terceiro nível. Com as médias empatadas e o BoJ a ~80% de alta, o desempate é evento, não preço. Fora do mercado."
    },
    "en": {
      "fundamental": "EUR/JPY closed at 178.56 in the 11/09/2026 session (ECB/Frankfurter reference rate; the logged-in MT5 terminal still returns no FX data), down -0.30% and giving back Thursday's bounce (+0.28% to 179.10) in full — the sequence's third 9-month low (178.59 → 178.56), printed after the ECB's hike (25 bp, deposit to 2.50%): when the European hawk cannot hold the cross, the engine is the yen — the market prices ~80% odds of a +25-bp BoJ step (to 1.25%) at the Sep 17-18 meeting, with the MoF on alert since the July intervention. The averages have met (50-day 184.163 ≈ 200-day 184.162 — a bearish cross drawing) and the geometry stays blocked: sigma20 at 96 pips puts the 2.5-sigma20 intervention floor at 241 pips — a short would need a target ~482 pips lower (173.74), territory with no structure. Indicators computed from the ECB/Frankfurter daily series (540 sessions, 01/08/2024 to 11/09/2026).",
      "trend": "Close under the 200-day SMA (184.16) and under the 50-day (184.16), the two averages meeting on the same point — the breakdown sequence (181.20 → 180.28 → 179.20 → 178.59 → 178.56) keeps the resolution bearish: a bear read on successive 9-month lows, with the one-session bounce already returned.",
      "support": "178.56 is the close itself — the 9-month low; beneath it, only the 178.00 / 177.50 rounds.",
      "resistance": "179.10 (Thursday's close) / 179.50 round, with the broken 9-month low (180.28) and the Sep 3-4 lows (181.20-181.59) above.",
      "priceAction": "No entry — the direction stays resolved bearish, but the intervention floor (2.5-sigma20 = 241 pips) rejects the chase at a 9-month low with no anchors ahead; a long under two averages is a bet against the BoJ. Re-arm: sigma20 compression or a structured retest of 180.28-181.20. The BoJ Sep 17-18 is the arbiter — with the ECB delivered, the tiebreak is all yen.",
      "recommendation": "WAIT FOR ANOTHER TRIGGER",
      "trigger": "None — the intervention floor (2.5-sigma20 = 241 pips) and the absence of anchors beneath the 9-month low reject any setup. Watch the reaction at the 178.00 / 177.50 rounds and sigma20 compression; the BoJ Sep 17-18 arbitrates.",
      "stop": "N/A (no trade).",
      "target": "N/A (no trade).",
      "rr": "N/A", "rrValue": 0,
      "justification": "A third 9-month low, this time with the ECB already in the price: the 25-bp hike did not buy a single session of structure — Thursday's bounce was returned in full on Friday. The problem is the same: the intervention floor (241 pips) demands an anchor ~482 pips below and the 9-month window has run out — only tier-three rounds remain. With the averages meeting and the BoJ ~80% priced to hike, the tiebreak is the event, not the price. Out of the market."
    }
  },
  "GBP/JPY": {
    "quote": "208.08", "bias": "BAIXA", "biasType": "bear",
    "pt": {
      "fundamental": "O GBP/JPY fechou em 208,08 na sessão de 11/09/2026 (taxa de referência BCE/Frankfurter; o terminal MT5 logado segue sem retornar dados de FX), caindo -0,18% — o repique de quinta (+0,26% para 208,46) parou sob a Fib 78,6% quebrada (reprecificada para 209,70 pela rotação da janela de 9 meses) e devolveu a maior parte na sexta. A mínima de 9 meses reprecificou para cima, 207,13 (a mínima de 206,47 saiu da janela) — 95 pips abaixo do fechamento. A leitura segue BAIXA e a geometria segue bloqueada: σ20 a 122 pips faz o piso de intervenção 2,5σ20 valer 304 pips — uma venda exigiria alvo a ~608 pips (202,00), sob a mínima de 9 meses. BoJ a ~80% para +25 pb (1,25%) e BoE a 3,75% decidem na mesma semana (17-18/09). Indicadores calculados da série diária BCE/Frankfurter (540 pregões, 01/08/2024 a 11/09/2026).",
      "trend": "Fechamento sob a SMA200 (212,93) e sob a SMA50 (215,30), com a SMA50 ainda acima da SMA200 — a sequência de rompimentos (210,57 → 209,39 → 207,91) mantém a resolução para baixo: leitura de baixa com o repique travado sob a Fib 78,6% quebrada (209,70).",
      "support": "207.13 (mínima de 9 meses, reprecificada), com o redondo 207.00 abaixo — 207.91 (mínima de 10/20 pregões) é a primeira defesa.",
      "resistance": "209.70 (Fib 78,6% reprecificada) / redondo 209.00, com a mínima quebrada de 03/09 (210.57) e a confluência Fib 50% / SMA200 (213.14-212.93) acima.",
      "priceAction": "Sem entrada — direção resolvida para baixo, geometria bloqueada: com σ20 = 122 pips, o piso de intervenção (2,5σ20 = 304 pips) manda procurar âncora a ~608 pips e ela está sob a mínima de 9 meses; compra não tem estrutura. Rearmar: compressão da σ20 ou reteste estruturado de 209.70-210.57. BoE/BoJ em 17-18/09 arbitram.",
      "recommendation": "AGUARDAR OUTRO GATILHO",
      "trigger": "Nenhum — o piso de intervenção (2,5σ20 = 304 pips) reprova qualquer geometria. Assistir à reação sobre a mínima de 9 meses (207.13) e à compressão da σ20.",
      "stop": "N/A (sem operação).",
      "target": "N/A (sem operação).",
      "rr": "N/A", "rrValue": 0,
      "justification": "O repique parou exatamente onde a regra manda respeitar: sob a Fib quebrada, agora reprecificada em 209,70 pela rotação da janela de 9 meses. Abaixo, a mínima também reprecificou para 207,13 — e mesmo com o alvo mais próximo, o piso de intervenção (304 pips) exige mirar ~202,00, onde não há nada além de redondos. Depois da intervenção de julho e do surto de 03/09, a lição não muda: não se paga caro para ficar na frente do MoF. Fora do mercado até a estrutura — ou o BoJ — entregarem algo."
    },
    "en": {
      "fundamental": "GBP/JPY closed at 208.08 in the 11/09/2026 session (ECB/Frankfurter reference rate; the logged-in MT5 terminal still returns no FX data), down -0.18% — Thursday's bounce (+0.26% to 208.46) stopped under the broken 78.6% Fib (re-priced to 209.70 by the 9-month window's rotation) and gave most of it back on Friday. The 9-month low re-priced higher to 207.13 (the old 206.47 left the window) — 95 pips below the close. The read stays BEAR and the geometry stays blocked: sigma20 at 122 pips puts the 2.5-sigma20 intervention floor at 304 pips — a short would need a target ~608 pips lower (202.00), under the 9-month low. The BoJ ~80% priced for +25 bp (1.25%) and the BoE at 3.75% decide in the same week (Sep 17-18). Indicators computed from the ECB/Frankfurter daily series (540 sessions, 01/08/2024 to 11/09/2026).",
      "trend": "Close under the 200-day SMA (212.93) and under the 50-day (215.30), with the 50-day still above the 200-day — the breakdown sequence (210.57 → 209.39 → 207.91) keeps the resolution bearish: a bear read with the bounce capped under the broken 78.6% Fib (209.70).",
      "support": "207.13 (9-month low, re-priced), with the 207.00 round beneath — 207.91 (the 10/20-day low) is the first defense.",
      "resistance": "209.70 (re-priced 78.6% Fib) / 209.00 round, with the broken Sep 3 low (210.57) and the 50% Fib / 200-day SMA confluence (213.14-212.93) above.",
      "priceAction": "No entry — direction resolved bearish, geometry blocked: with sigma20 = 122 pips, the intervention floor (2.5-sigma20 = 304 pips) demands an anchor ~608 pips away and it sits under the 9-month low; a long has no structure. Re-arm: sigma20 compression or a structured retest of 209.70-210.57. The BoE/BoJ Sep 17-18 week arbitrates.",
      "recommendation": "WAIT FOR ANOTHER TRIGGER",
      "trigger": "None — the intervention floor (2.5-sigma20 = 304 pips) rejects any geometry. Watch the reaction at the 9-month low (207.13) and sigma20 compression.",
      "stop": "N/A (no trade).",
      "target": "N/A (no trade).",
      "rr": "N/A", "rrValue": 0,
      "justification": "The bounce stopped exactly where the rule says to respect it: under the broken Fib, now re-priced to 209.70 by the 9-month window's rotation. Below, the low also re-priced to 207.13 — and even with the nearer target, the intervention floor (304 pips) demands aiming at ~202.00, where nothing but rounds exist. After the July intervention and the Sep 3 surge, the lesson holds: do not pay up to stand in front of the MoF. Out of the market until the structure — or the BoJ — delivers something."
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
html = rep(html, 'dataBasis: "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 538 daily sessions (01/08/2024–09/09/2026).",',
                 'dataBasis: "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 540 daily sessions (01/08/2024–11/09/2026).",', "basis en")
html = rep(html, 'dataBasis: "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, σ20 e Donchian calculados · 538 pregões (01/08/2024 a 09/09/2026).",',
                 'dataBasis: "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, σ20 e Donchian calculados · 540 pregões (01/08/2024 a 11/09/2026).",', "basis pt")
html = rep(html, 'nextEvent: "ECB Sep 10 · US CPI ~Sep 10",', 'nextEvent: "FOMC Sep 15-16 · BoE/BoJ Sep 17-18",', "nextEvent en")
html = rep(html, 'nextEvent: "BCE 10/09 · CPI EUA ~10/09",', 'nextEvent: "FOMC 15-16/09 · BoE/BoJ 17-18/09",', "nextEvent pt")

html, n = re.subn(
    r"        const dailyChanges = \{.*?\n        \};",
    '''        const dailyChanges = {
            "EUR/USD": "-0.21%",
            "USD/JPY": "-0.09%",
            "AUD/USD": "-0.17%",
            "GBP/USD": "-0.09%",
            "EUR/JPY": "-0.30%",
            "GBP/JPY": "-0.18%"
        };''', html, count=1, flags=re.DOTALL)
if n != 1:
    print("FAIL: dailyChanges"); sys.exit(1)

html, n = re.subn(
    r"        const macroDrivers = \{.*?\n        \};",
    '''        const macroDrivers = {
            "EUR/USD": {
                en: ["Bear regime back", "Short 1.1631-1.1657", "FOMC Sep 15-16"],
                pt: ["Regime de baixa de volta", "Curto 1.1631-1.1657", "FOMC 15-16/09"]
            },
            "USD/JPY": {
                en: ["Bounce died on CPI", "2.5σ floor 235p", "BoJ Sep 17-18"],
                pt: ["Repique morreu no CPI", "Piso 2,5σ 235p", "BoJ 17-18/09"]
            },
            "AUD/USD": {
                en: ["Retest underway", "Zone 0.7141-0.7162", "RBA Sep 29"],
                pt: ["Reteste em curso", "Zona 0.7141-0.7162", "RBA 29/09"]
            },
            "GBP/USD": {
                en: ["Double top 1.3565", "Premium < 1:2 gate", "BoE Sep 17"],
                pt: ["Topo duplo 1.3565", "Prêmio < 1:2", "BoE 17/09"]
            },
            "EUR/JPY": {
                en: ["3rd 9-month low", "2.5σ floor 241p", "BoJ Sep 17-18"],
                pt: ["3ª mín. de 9 meses", "Piso 2,5σ 241p", "BoJ 17-18/09"]
            },
            "GBP/JPY": {
                en: ["Fib re-priced 209.70", "2.5σ floor 304p", "BoE/BoJ Sep 17"],
                pt: ["Fib reprecificada 209,70", "Piso 2,5σ 304p", "BoE/BoJ 17/09"]
            }
        };''', html, count=1, flags=re.DOTALL)
if n != 1:
    print("FAIL: macroDrivers"); sys.exit(1)

# ---- news wire digest (newsData): update stamp + prepend the 11/09 items ----
html = rep(html, 'updated: "' + OLD_TS + '",', 'updated: "' + TS + '",', "newsData.updated")

NEWS_ITEMS = '''                {
                    date: "11/09/2026",
                    category: "cb",
                    impact: "high",
                    pairs: ["EUR/USD", "EUR/JPY"],
                    pt: {
                        headline: "BCE sobe 25 pb para 2,50% e o euro cai mesmo assim: recaptura falhada devolve o regime de baixa",
                        summary: "O BCE entregou o alta de 25 pb em 10/09 (depósito a 2,50%, o segundo desde o choque energético) — e o euro foi vendido no fato: o EUR/USD caiu -0,31% na quinta e -0,21% na sexta, fechando a 1,1592, de volta sob a SMA200 (1,1631) depois da recaptura de um pregão de 09/09. Com a SMA50 (1,1527) ainda abaixo, o alinhamento volta a ser plenamente de baixa e a zona de venda 1.1631-1.1657 (SMA200 + Fib 50%) retorna ao mapa — entrada 1.1640, stop 1.1685, alvo 1.1527 (1:2,51), válida até o fechamento de 14/09.",
                        take: "A regra realinha o viés sem hesitar: recaptura de SMA200 que dura um pregão é rejeição, e venda no fato hawkish é fluxo. O curto volta ao livro no repique — dentro da janela de 24h do FOMC (15-16/09), reavaliar após o evento. No EUR/JPY, o alta do BCE não segurou o cruzamento: terceira mínima de 9 meses (178,56) com o BoJ a ~80% de +25 pb."
                    },
                    en: {
                        headline: "ECB hikes 25 bp to 2.50% and the euro falls anyway: failed reclaim hands the bear regime back",
                        summary: "The ECB delivered the 25-bp hike on Sep 10 (deposit to 2.50%, the second since the energy shock) — and the euro was sold on the fact: EUR/USD fell -0.31% Thursday and -0.21% Friday, closing at 1.1592, back under the SMA200 (1.1631) after Wednesday's one-session reclaim. With the 50-day (1.1527) still below, the alignment turns fully bearish again and the 1.1631-1.1657 selling zone (SMA200 + 50% Fib) returns to the map — entry 1.1640, stop 1.1685, target 1.1527 (1:2.51), valid through the Sep 14 close.",
                        take: "The rule re-aligns the bias without hesitation: an SMA200 reclaim that lasts one session is a rejection, and selling a delivered hawkish fact is flow. The short goes back on the book at the pullback — inside the FOMC (Sep 15-16) 24h window, reassess after the event. In EUR/JPY, the ECB hike did not hold the cross: a third 9-month low (178.56) with the BoJ ~80% priced for +25 bp."
                    }
                },
                {
                    date: "11/09/2026",
                    category: "macro",
                    impact: "high",
                    pairs: ["EUR/USD", "USD/JPY", "AUD/USD", "GBP/USD"],
                    pt: {
                        headline: "CPI de agosto quente no headline (+0,4% m/m; 3,4% a/a) mantém a alta do Fed em pauta e sustenta o dólar",
                        summary: "O CPI dos EUA de agosto (11/09, 12:30 UTC) veio +0,4% m/m no headline (ante +0,1% em julho) e 3,4% a/a, com o núcleo esfriando para 2,4% a/a (+0,3% m/m) — headline quente o bastante para manter a alta do Fed em pauta (odds ~60%) no FOMC de 15-16/09. O dólar firme derrubou o AUD/USD do topo de 20 pregões (0,7173, reteste em curso rumo à zona 0.7141-0.7162) e devolveu o GBP/USD ao meio da faixa (1,3508) após a dupla rejeição em 1.3565-1.3566.",
                        take: "O filtro de eventos concentra tudo no FOMC: os dois tickets do livro (venda do EUR/USD no repique, compra do AUD/USD no reteste) valem até o fechamento de 14/09 — disparo dentro da janela de 24h manda reavaliar após o evento. Núcleo esfriando com headline quente é o cenário que mais divide o comitê."
                    },
                    en: {
                        headline: "Hot August headline CPI (+0.4% m/m; 3.4% y/y) keeps the Fed hike in play and underpins the dollar",
                        summary: "August US CPI (Sep 11, 12:30 UTC) printed +0.4% m/m on the headline (from +0.1% in July) and 3.4% y/y, with core cooling to 2.4% y/y (+0.3% m/m) — a headline hot enough to keep the Fed hike in play (~60% odds) at the Sep 15-16 FOMC. The firm dollar knocked AUD/USD off its 20-day high (0.7173, the retest underway toward the 0.7141-0.7162 zone) and pushed GBP/USD back to mid-range (1.3508) after the double rejection at 1.3565-1.3566.",
                        take: "The event filter concentrates everything on the FOMC: both live tickets (EUR/USD short on the pullback, AUD/USD long on the retest) are valid through the Sep 14 close — a trigger inside the 24h window mandates reassessing after the event. Cooling core with a hot headline is the scenario that splits the committee most."
                    }
                },
                {
                    date: "11/09/2026",
                    category: "cb",
                    impact: "high",
                    pairs: ["USD/JPY", "EUR/JPY", "GBP/JPY"],
                    pt: {
                        headline: "Iene segura a vantagem rumo ao BoJ: repique do USD/JPY morre no CPI e EUR/JPY crava terceira mínima de 9 meses",
                        summary: "A semana fecha com o iene no comando: o repique do USD/JPY (+0,59% na quinta, primeiro fechamento de alta em cinco pregões) morreu no CPI quente e o par fechou a 154,04 (-0,09%), a 141 pips da mínima de 9 meses (152,63); o EUR/JPY devolveu inteiro o repique de quinta e cravou a terceira mínima de 9 meses (178,56, -0,30%) — mesmo depois do alta do BCE; o GBP/JPY parou em 208,08 (-0,18%) sob a Fib 78,6% quebrada (reprecificada em 209,70). O mercado precifica ~80% de +25 pb do BoJ (para 1,25%) em 17-18/09, com o MoF em alerta desde a intervenção de julho.",
                        take: "Os pisos de intervenção (2,5σ20) seguem em 235-304 pips e nenhuma âncora estrutural paga 1:2 — os três pares com iene permanecem em AGUARDAR. FOMC (15-16/09) e BoJ (17-18/09) na mesma semana decidem o capítulo; não se corre na frente do MoF."
                    },
                    en: {
                        headline: "Yen holds the high ground into the BoJ: USD/JPY's bounce dies on CPI and EUR/JPY prints a third 9-month low",
                        summary: "The week closes with the yen in charge: USD/JPY's bounce (+0.59% Thursday, the first up close in five sessions) died on the hot CPI and the pair closed at 154.04 (-0.09%), 141 pips above the 9-month low (152.63); EUR/JPY gave back Thursday's bounce in full and printed a third 9-month low (178.56, -0.30%) — even after the ECB hike; GBP/JPY stopped at 208.08 (-0.18%) under the broken 78.6% Fib (re-priced to 209.70). The market prices ~80% odds of a +25-bp BoJ step (to 1.25%) on Sep 17-18, with the MoF on alert since the July intervention.",
                        take: "The intervention floors (2.5-sigma20) still run 235-304 pips and no structural anchor pays 1:2 — the three yen pairs stay on WAIT. The FOMC (Sep 15-16) and BoJ (Sep 17-18) in the same week decide the chapter; do not front-run the MoF."
                    }
                },
'''
html = rep(html, '            items: [\n                {\n                    date: "09/09/2026"',
            "            items: [\n" + NEWS_ITEMS + "                {\n                    date: \"09/09/2026\"", "newsData item prepend")

open(P, "w", encoding="utf-8").write(html)
print(f"OK: index.html (forexData, 3 timestamps, basis, nextEvent, ticker, macroDrivers, news digest) — stamp {TS}")

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
    h = rep(h, '<span class="ts-date">09·09·26</span>', '<span class="ts-date">11·09·26</span>', f"{tag} ts-date")
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
              '<div class="section-content lang-pt" style="display:none;">' + d["pt"]["fundamental"] + "</div>", f"{tag} fundamental pt")
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
    "_bluf_en": '<span class="lang-en"><span class="bluf-action sell">SELL</span> — failed reclaim: two closes back under the SMA200 despite the ECB&rsquo;s 25-bp hike; short the pullback into 1.1631-1.1657, target the 50-day SMA (1:2.51)</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action sell">VENDA</span> — recaptura falhada: dois fechamentos de volta sob a SMA200 mesmo com o alta de 25 pb do BCE; vender o repique em 1.1631-1.1657, alvo na SMA50 (1:2,51)</span>',
    "_tier_en": "High", "_tier_pt": "Alta",
})
FD["USD/JPY"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — the bounce died on CPI (154.04); the 235-pip intervention floor still blocks the book</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — o repique morreu no CPI (154,04); o piso de intervenção de 235 pips segue bloqueando o livro</span>',
    "_tier_en": "Moderate", "_tier_pt": "Moderada",
})
FD["AUD/USD"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action buy">BUY</span> — the retest is underway (0.7173, two down sessions); buy the zone 0.7141-0.7162, target 0.7257 (1:2.27)</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action buy">COMPRA</span> — o reteste está em curso (0,7173, dois pregões de queda); comprar a zona 0.7141-0.7162, alvo 0.7257 (1:2,27)</span>',
    "_tier_en": "High", "_tier_pt": "Alta",
})
FD["GBP/USD"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — double rejection at 1.3565-1.3566; the nearest target pays 1:1.47 and the BoE (17/09) re-prices the map</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — dupla rejeição em 1.3565-1.3566; o alvo mais próximo paga 1:1,47 e o BoE (17/09) reprecifica o mapa</span>',
    "_tier_en": "Moderate", "_tier_pt": "Moderada",
})
FD["EUR/JPY"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — third 9-month low (178.56) even after the ECB hike; the 241-pip intervention floor rejects all geometry</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — terceira mínima de 9 meses (178,56) mesmo após o alta do BCE; o piso de intervenção de 241 pips rejeita qualquer geometria</span>',
    "_tier_en": "Moderate", "_tier_pt": "Moderada",
})
FD["GBP/JPY"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — the bounce stalled under the re-priced 78.6% Fib (209.70); the 304-pip intervention floor rejects all geometry</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — o repique parou sob a Fib 78,6% reprecificada (209,70); o piso de intervenção de 304 pips rejeita qualquer geometria</span>',
    "_tier_en": "Moderate", "_tier_pt": "Moderada",
})

# bias flip today: neutral -> bear on EUR/USD (failed SMA200 reclaim; SMA50 below SMA200)
BIAS_SWAP = {
    "EUR/USD": ("neutral", "bear", "EUR/USD - NEUTRAL", "EUR/USD - BEARISH", "EUR/USD - NEUTRO", "EUR/USD - BAIXA"),
}

CHIPS = {
    "EUR/USD": [('<span class="macro-chip lang-en">ECB decision 10/09</span>', '<span class="macro-chip lang-en">ECB hiked to 2.50%</span>', "en"),
                ('<span class="macro-chip lang-pt" style="display:none;">Decisão do BCE 10/09</span>', '<span class="macro-chip lang-pt" style="display:none;">BCE subiu para 2,50%</span>', "pt")],
    "USD/JPY": [],
    "AUD/USD": [],
    "GBP/USD": [],
    "EUR/JPY": [],
    "GBP/JPY": [],
}

# gauge percent computed from support/resistance leading numbers vs quote
GAUGE = {"EUR/USD": ("26", "1.1578", "1.1631"), "USD/JPY": ("67", "152.63", "154.75"),
         "AUD/USD": ("38", "0.7141", "0.7225"), "GBP/USD": ("30", "1.3483", "1.3565"),
         "EUR/JPY": ("0", "178.56", "179.10"), "GBP/JPY": ("37", "207.13", "209.70")}
# conviction score = round(R*3) clamped to [3,10]; 0 for WAIT pairs
TIER = {"EUR/USD": ("8/10", "", 8), "USD/JPY": ("0/10", "t-mod", 0),
        "AUD/USD": ("7/10", "", 7), "GBP/USD": ("0/10", "t-mod", 0),
        "EUR/JPY": ("0/10", "t-mod", 0), "GBP/JPY": ("0/10", "t-mod", 0)}

# verdict flip today: EUR/USD wait -> sell (short pullback re-armed)
BADGE = {
    "EUR/USD": ('<span class="verdict-badge sell">\n                                    <span class="lang-en">SELL (SHORT) ON PULLBACK</span>\n                                    <span class="lang-pt" style="display:none;">VENDA (SHORT) NA RETRAÇÃO</span>\n                                </span>',
                [("wait", "sell")]),
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

# Resolve nothing: the only live ticket (AUD/USD long retest, 09/09) never fired —
# 10/09 closed 0.71849 and 11/09 0.71726, both above the 0.7141-0.7162 zone.
for t in led["watching"]:
    if t["pair"] == "AUD/USD":
        t["reportDate"] = TS_DATE
        t["triggerRule"] = "daily close inside 0.7141-0.7162 (10-day low + 0.7150 round) followed by a close above the previous close and the 0.7152 midpoint; valid through the 14/09 close — inside the FOMC (15-16/09) 24h window, reassess after the event"
        t["note"] = "retest underway: two down sessions (-0.72% from 0.7225) already handed back the broken 0.7195 level; ticket carried unchanged (stop 45 pips >= the 42-pip 1.5-sigma20 floor), the US-CPI clause swapped for the FOMC window; a close under 0.7141 kills the setup"
assert len([t for t in led["watching"] if t["pair"] == "AUD/USD"]) == 1

# Append: EUR/USD short pullback — failed SMA200 reclaim restores the bear alignment.
led["watching"].insert(0, {
    "pair": "EUR/USD",
    "reportDate": TS_DATE,
    "direction": "short",
    "setup": "pullback",
    "entry": 1.164,
    "stop": 1.1685,
    "target": 1.1527,
    "plannedR": 2.51,
    "triggerRule": "daily close inside 1.1631-1.1657 (SMA200 + 50% Fib) followed by a close below the previous close and the 1.1644 midpoint; valid through the 14/09 close — inside the FOMC (15-16/09) 24h window, reassess after the event",
    "note": "failed SMA200 reclaim: one close over (09/09, 1.1652) then two back under (10-11/09) despite the ECB hiking to 2.50% — bear alignment restored (close 1.1592 < SMA200 1.1631, SMA50 1.1527 below); stop 45 pips >= the 45-pip 1.5-sigma20 floor; target the 50-day SMA (1.1527)"
})
assert len(led["watching"]) == 2
assert len([t for t in led["watching"] if t["pair"] == "EUR/USD"]) == 1

with open(LED, "w", encoding="utf-8") as f:
    json.dump(led, f, ensure_ascii=False, indent=2)
print("OK: track-record.json (AUD/USD carried + FOMC clause, EUR/USD short appended)")

# =====================================================================
# 4. news.html — hero dateline + new wire cards + basis note + calendar trim
# =====================================================================
NP = DOCS + "/news.html"
nh = open(NP, encoding="utf-8").read()
nh = rep(nh, '<span class="lang-en">Wire updated: ' + OLD_TS + '</span>', '<span class="lang-en">Wire updated: ' + TS + '</span>', "news hero en")
nh = rep(nh, '<span class="lang-pt" style="display:none;">Telégrafo atualizado em: ' + OLD_TS + '</span>', '<span class="lang-pt" style="display:none;">Telégrafo atualizado em: ' + TS + '</span>', "news hero pt")
nh = rep(nh, "numbers and dates reflect the report's data basis of 09/09/2026", "numbers and dates reflect the report's data basis of 11/09/2026", "news note en")
nh = rep(nh, "refletem a base de dados do relatório de 09/09/2026", "refletem a base de dados do relatório de 11/09/2026", "news note pt")

# week-ahead calendar: drop the three cells already delivered (China CPI, ECB, US CPI)
for cell_label, cell_html in [
    ("cal China CPI", '''                <div class="cal-cell">
                    <span class="cal-date">&asymp;09/09</span>
                    <span class="cal-event"><span class="lang-en">China CPI</span><span class="lang-pt" style="display:none;">CPI da China</span></span>
                    <div class="cal-meta"><span class="cal-impact high" aria-hidden="true"></span><span class="cal-cur">CNY</span><span class="cal-cur">AUD</span></div>
                </div>
'''),
    ("cal ECB", '''                <div class="cal-cell">
                    <span class="cal-date">09-10/09</span>
                    <span class="cal-event"><span class="lang-en">ECB decision</span><span class="lang-pt" style="display:none;">Decisão do BCE</span></span>
                    <div class="cal-meta"><span class="cal-impact high" aria-hidden="true"></span><span class="cal-cur">EUR</span></div>
                </div>
'''),
    ("cal US CPI", '''                <div class="cal-cell">
                    <span class="cal-date">&asymp;10/09</span>
                    <span class="cal-event"><span class="lang-en">US CPI</span><span class="lang-pt" style="display:none;">CPI dos EUA</span></span>
                    <div class="cal-meta"><span class="cal-impact high" aria-hidden="true"></span><span class="cal-cur">USD</span></div>
                </div>
'''),
]:
    nh = rep(nh, cell_html, "", cell_label)

NEWS_CARDS = '''                <!-- News 0: ECB sell-the-fact — failed reclaim restores the bear regime -->
                <article class="news-card">
                    <div class="news-card-top">
                        <span class="news-cat"><span class="lang-en">Central Banks</span><span class="lang-pt" style="display:none;">Bancos Centrais</span></span>
                        <span class="impact-badge high"><span class="lang-en">High Impact</span><span class="lang-pt" style="display:none;">Impacto Alto</span></span>
                        <span class="news-date">11/09/2026</span>
                    </div>
                    <h2 class="news-title">
                        <span class="lang-en">ECB hikes 25 bp to 2.50% and the euro falls anyway: failed reclaim hands the bear regime back</span>
                        <span class="lang-pt" style="display:none;">BCE sobe 25 pb para 2,50% e o euro cai mesmo assim: recaptura falhada devolve o regime de baixa</span>
                    </h2>
                    <p class="news-summary">
                        <span class="lang-en">The ECB delivered the 25-bp hike on Sep 10 (deposit to 2.50%, the second since the energy shock) — and the euro was sold on the fact: EUR/USD fell -0.31% Thursday and -0.21% Friday, closing at 1.1592, back under the SMA200 (1.1631) after Wednesday's one-session reclaim. With the 50-day (1.1527) still below, the alignment turns fully bearish again and the 1.1631-1.1657 selling zone (SMA200 + 50% Fib) returns to the map — entry 1.1640, stop 1.1685, target 1.1527 (1:2.51), valid through the Sep 14 close.</span>
                        <span class="lang-pt" style="display:none;">O BCE entregou o alta de 25 pb em 10/09 (depósito a 2,50%, o segundo desde o choque energético) — e o euro foi vendido no fato: o EUR/USD caiu -0,31% na quinta e -0,21% na sexta, fechando a 1,1592, de volta sob a SMA200 (1,1631) depois da recaptura de um pregão de 09/09. Com a SMA50 (1,1527) ainda abaixo, o alinhamento volta a ser plenamente de baixa e a zona de venda 1.1631-1.1657 (SMA200 + Fib 50%) retorna ao mapa — entrada 1.1640, stop 1.1685, alvo 1.1527 (1:2,51), válida até o fechamento de 14/09.</span>
                    </p>
                    <div class="news-take">
                        <span class="take-tag"><span class="lang-en">Desk take</span><span class="lang-pt" style="display:none;">Leitura da mesa</span></span>
                        <span class="lang-en">The rule re-aligns the bias without hesitation: an SMA200 reclaim that lasts one session is a rejection, and selling a delivered hawkish fact is flow. The short goes back on the book at the pullback — inside the FOMC (Sep 15-16) 24h window, reassess after the event. In EUR/JPY, the ECB hike did not hold the cross: a third 9-month low (178.56) with the BoJ ~80% priced for +25 bp.</span>
                        <span class="lang-pt" style="display:none;">A regra realinha o viés sem hesitar: recaptura de SMA200 que dura um pregão é rejeição, e venda no fato hawkish é fluxo. O curto volta ao livro no repique — dentro da janela de 24h do FOMC (15-16/09), reavaliar após o evento. No EUR/JPY, o alta do BCE não segurou o cruzamento: terceira mínima de 9 meses (178,56) com o BoJ a ~80% de +25 pb.</span>
                    </div>
                    <div class="news-pairs">
                        <span class="np-label"><span class="lang-en">Watch</span><span class="lang-pt" style="display:none;">Acompanhar</span></span>
                        <a href="eur-usd.html" class="pair-link-chip">EUR/USD</a>
                        <a href="eur-jpy.html" class="pair-link-chip">EUR/JPY</a>
                    </div>
                </article>

                <!-- News 1: Hot headline CPI keeps the Fed hike in play -->
                <article class="news-card">
                    <div class="news-card-top">
                        <span class="news-cat"><span class="lang-en">Macro Data</span><span class="lang-pt" style="display:none;">Dados Macro</span></span>
                        <span class="impact-badge high"><span class="lang-en">High Impact</span><span class="lang-pt" style="display:none;">Impacto Alto</span></span>
                        <span class="news-date">11/09/2026</span>
                    </div>
                    <h2 class="news-title">
                        <span class="lang-en">Hot August headline CPI (+0.4% m/m; 3.4% y/y) keeps the Fed hike in play and underpins the dollar</span>
                        <span class="lang-pt" style="display:none;">CPI de agosto quente no headline (+0,4% m/m; 3,4% a/a) mantém a alta do Fed em pauta e sustenta o dólar</span>
                    </h2>
                    <p class="news-summary">
                        <span class="lang-en">August US CPI (Sep 11, 12:30 UTC) printed +0.4% m/m on the headline (from +0.1% in July) and 3.4% y/y, with core cooling to 2.4% y/y (+0.3% m/m) — a headline hot enough to keep the Fed hike in play (~60% odds) at the Sep 15-16 FOMC. The firm dollar knocked AUD/USD off its 20-day high (0.7173, the retest underway toward the 0.7141-0.7162 zone) and pushed GBP/USD back to mid-range (1.3508) after the double rejection at 1.3565-1.3566.</span>
                        <span class="lang-pt" style="display:none;">O CPI dos EUA de agosto (11/09, 12:30 UTC) veio +0,4% m/m no headline (ante +0,1% em julho) e 3,4% a/a, com o núcleo esfriando para 2,4% a/a (+0,3% m/m) — headline quente o bastante para manter a alta do Fed em pauta (odds ~60%) no FOMC de 15-16/09. O dólar firme derrubou o AUD/USD do topo de 20 pregões (0,7173, reteste em curso rumo à zona 0.7141-0.7162) e devolveu o GBP/USD ao meio da faixa (1,3508) após a dupla rejeição em 1.3565-1.3566.</span>
                    </p>
                    <div class="news-take">
                        <span class="take-tag"><span class="lang-en">Desk take</span><span class="lang-pt" style="display:none;">Leitura da mesa</span></span>
                        <span class="lang-en">The event filter concentrates everything on the FOMC: both live tickets (EUR/USD short on the pullback, AUD/USD long on the retest) are valid through the Sep 14 close — a trigger inside the 24h window mandates reassessing after the event. Cooling core with a hot headline is the scenario that splits the committee most.</span>
                        <span class="lang-pt" style="display:none;">O filtro de eventos concentra tudo no FOMC: os dois tickets do livro (venda do EUR/USD no repique, compra do AUD/USD no reteste) valem até o fechamento de 14/09 — disparo dentro da janela de 24h manda reavaliar após o evento. Núcleo esfriando com headline quente é o cenário que mais divide o comitê.</span>
                    </div>
                    <div class="news-pairs">
                        <span class="np-label"><span class="lang-en">Watch</span><span class="lang-pt" style="display:none;">Acompanhar</span></span>
                        <a href="eur-usd.html" class="pair-link-chip">EUR/USD</a>
                        <a href="usd-jpy.html" class="pair-link-chip">USD/JPY</a>
                        <a href="aud-usd.html" class="pair-link-chip">AUD/USD</a>
                        <a href="gbp-usd.html" class="pair-link-chip">GBP/USD</a>
                    </div>
                </article>

                <!-- News 2: Yen holds the high ground into the BoJ -->
                <article class="news-card">
                    <div class="news-card-top">
                        <span class="news-cat"><span class="lang-en">Central Banks</span><span class="lang-pt" style="display:none;">Bancos Centrais</span></span>
                        <span class="impact-badge high"><span class="lang-en">High Impact</span><span class="lang-pt" style="display:none;">Impacto Alto</span></span>
                        <span class="news-date">11/09/2026</span>
                    </div>
                    <h2 class="news-title">
                        <span class="lang-en">Yen holds the high ground into the BoJ: USD/JPY&rsquo;s bounce dies on CPI and EUR/JPY prints a third 9-month low</span>
                        <span class="lang-pt" style="display:none;">Iene segura a vantagem rumo ao BoJ: repique do USD/JPY morre no CPI e EUR/JPY crava terceira mínima de 9 meses</span>
                    </h2>
                    <p class="news-summary">
                        <span class="lang-en">The week closes with the yen in charge: USD/JPY&rsquo;s bounce (+0.59% Thursday, the first up close in five sessions) died on the hot CPI and the pair closed at 154.04 (-0.09%), 141 pips above the 9-month low (152.63); EUR/JPY gave back Thursday&rsquo;s bounce in full and printed a third 9-month low (178.56, -0.30%) — even after the ECB hike; GBP/JPY stopped at 208.08 (-0.18%) under the broken 78.6% Fib (re-priced to 209.70). The market prices ~80% odds of a +25-bp BoJ step (to 1.25%) on Sep 17-18, with the MoF on alert since the July intervention.</span>
                        <span class="lang-pt" style="display:none;">A semana fecha com o iene no comando: o repique do USD/JPY (+0,59% na quinta, primeiro fechamento de alta em cinco pregões) morreu no CPI quente e o par fechou a 154,04 (-0,09%), a 141 pips da mínima de 9 meses (152,63); o EUR/JPY devolveu inteiro o repique de quinta e cravou a terceira mínima de 9 meses (178,56, -0,30%) — mesmo depois do alta do BCE; o GBP/JPY parou em 208,08 (-0,18%) sob a Fib 78,6% quebrada (reprecificada em 209,70). O mercado precifica ~80% de +25 pb do BoJ (para 1,25%) em 17-18/09, com o MoF em alerta desde a intervenção de julho.</span>
                    </p>
                    <div class="news-take">
                        <span class="take-tag"><span class="lang-en">Desk take</span><span class="lang-pt" style="display:none;">Leitura da mesa</span></span>
                        <span class="lang-en">The intervention floors (2.5&sigma;20) still run 235-304 pips and no structural anchor pays 1:2 — the three yen pairs stay on WAIT. The FOMC (Sep 15-16) and BoJ (Sep 17-18) in the same week decide the chapter; do not front-run the MoF.</span>
                        <span class="lang-pt" style="display:none;">Os pisos de intervenção (2,5σ20) seguem em 235-304 pips e nenhuma âncora estrutural paga 1:2 — os três pares com iene permanecem em AGUARDAR. FOMC (15-16/09) e BoJ (17-18/09) na mesma semana decidem o capítulo; não se corre na frente do MoF.</span>
                    </div>
                    <div class="news-pairs">
                        <span class="np-label"><span class="lang-en">Watch</span><span class="lang-pt" style="display:none;">Acompanhar</span></span>
                        <a href="usd-jpy.html" class="pair-link-chip">USD/JPY</a>
                        <a href="eur-jpy.html" class="pair-link-chip">EUR/JPY</a>
                        <a href="gbp-jpy.html" class="pair-link-chip">GBP/JPY</a>
                    </div>
                </article>

'''
nh = rep(nh, "                <!-- News 0: ECB eve — euro reclaims the SMA200 -->", NEWS_CARDS + "                <!-- News 0: ECB eve — euro reclaims the SMA200 -->", "news card prepend")
open(NP, "w", encoding="utf-8").write(nh)
print("OK: news.html (dateline, 3 new cards, basis note, calendar trimmed to FOMC/BoE/BoJ/RBA)")

# =====================================================================
# 5. patch verify_all.py to the new edition
# =====================================================================
VP = r"C:/Projetos/forex-report/pipeline/verify_all.py"
v = open(VP, encoding="utf-8").read()
v = rep(v, 'TODAY_TS = "09/09/2026 20:54 UTC"', 'TODAY_TS = "' + TS + '"', "verify TODAY_TS")
v = rep(v, 'TODAY_DATE = "09/09/2026"  # basis session date (report edition: 09/09/2026)', 'TODAY_DATE = "11/09/2026"  # basis session date (report edition: 11/09/2026)', "verify TODAY_DATE")
v = rep(v, '''TICKER = [("EUR/USD","+0.33%"),("USD/JPY","-0.67%"),("AUD/USD","+0.14%"),
          ("GBP/USD","+0.14%"),("EUR/JPY","-0.34%"),("GBP/JPY","-0.53%")]''',
        '''TICKER = [("EUR/USD","-0.21%"),("USD/JPY","-0.09%"),("AUD/USD","-0.17%"),
          ("GBP/USD","-0.09%"),("EUR/JPY","-0.30%"),("GBP/JPY","-0.18%")]''', "verify TICKER")
v = rep(v, 'for stale in ["02/09/2026", "01/09/2026", "19/08/2026", "18/08/2026", "17/08/2026", "14/08/2026", "13/08/2026", "04/09/2026", "07/09/2026"]:',
        'for stale in ["02/09/2026", "01/09/2026", "19/08/2026", "18/08/2026", "17/08/2026", "14/08/2026", "13/08/2026", "04/09/2026", "07/09/2026", "09/09/2026"]:', "verify static stale")
open(VP, "w", encoding="utf-8").write(v)
print("OK: verify_all.py patched to the 11/09/2026 edition")

print(f"\nDONE {TS} — run verify_all.py next.")
