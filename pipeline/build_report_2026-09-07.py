#!/usr/bin/env python3
"""Daily regeneration for the 07/09/2026 edition — ECB/Frankfurter basis
(the logged-in MT5 terminal still offers no FX symbols; compute_indicators fell back).
Basis: ECB/Frankfurter reference rates, 536 sessions 01/08/2024-07/09/2026 (last close: 07/09/2026).
Session: yen second wave — USD/JPY -0.96% to 154.75 (breaks the 10/20-day low 156.01, Fib78.6 155.04
and the 155 round; Friday's resolution condition met -> bias flips BEAR), EUR/JPY -0.96% to 179.85
(fresh 9-month low, breaks 180.28 -> BEAR), GBP/JPY -0.95% to 209.39 (breaks 210.57 -> BEAR).
Intervention floors rise with sigma20 (227/240/307 pips) -> the three JPY pairs stay on WAIT.
Verdicts: EUR/USD SELL pullback 1.1629-1.1657 carried (1:2.36), AUD/USD BUY pullback 0.7141-0.7162
carried — breakout confirmed by a second close (1:2.27), GBP/USD BUY pullback re-priced to the
drifted averages 1.3440-1.3454 (1:2.09), USD/JPY / EUR/JPY / GBP/JPY WAIT.
Also prepends the yen-second-wave item to the news wire (index digest + news.html).
Aborts on any structural mismatch."""
import re, json, sys
from datetime import datetime, timezone

DOCS = r"C:/Projetos/forex-report/docs"
TS_DATE = "07/09/2026"
now = datetime.now(timezone.utc)
TS = TS_DATE + " " + now.strftime("%H:%M") + " UTC"
OLD_TS = "04/09/2026 19:03 UTC"

BASIS_EN_AMP = "ECB/Frankfurter reference rates · SMA50/200, sigma20 &amp; Donchian computed · 536 daily sessions (01/08/2024–07/09/2026)."
BASIS_PT = "taxas de referência BCE/Frankfurter · SMA50/200, σ20 e Donchian calculados · 536 pregões (01/08/2024 a 07/09/2026)."

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
    "quote": "1.1622", "bias": "BAIXA", "biasType": "bear",
    "pt": {
      "fundamental": "O EUR/USD fechou em 1,1622 na sessão de 07/09/2026 (taxa de referência BCE/Frankfurter; o terminal MT5 logado segue sem ofertar símbolos de FX), estável (0,00% na precisão da taxa de referência) — o quinto fechamento seguido sob a SMA200 (1,1630), com a SMA50 (1,1510) também abaixo: o regime de baixa atravessa a semana decisiva intacto. A zona de venda segue no lugar — SMA200 (1,1630) + Fib 50% (1,1657), com as máximas de 10/20 pregões (1,1669/1,1699) acima — e o gatilho expira no fechamento de 08/09, na véspera do BCE. Macro: o NFP forte (+162 mil; desemprego 4,1%) segue puxando o dólar com DXY ~99,5 e odds de alta do Fed ~60% (FOMC 15-16/09); o BCE (2,25%) decide em 09-10/09 e o CPI dos EUA (~10/09) fecha a sequência. Indicadores (SMA 50/200, σ20, Donchian e Fibonacci) calculados da série diária BCE/Frankfurter (536 pregões, 01/08/2024 a 07/09/2026).",
      "trend": "Fechamento sob a SMA200 (1,1630) com a SMA50 (1,1510) também abaixo — alinhamento de baixa no quinto pregão seguido; a zona de venda SMA200 / Fib 50% (1.1630-1.1657) espera logo acima do preço, com as máximas de 10/20 pregões (1.1669/1.1699) como teto seguinte.",
      "support": "1.1578 (mínima de 10 pregões), com a mínima de 20 pregões (1.1534) e a confluência Fib 78,6% / redondo (1.1476-1.1500) abaixo.",
      "resistance": "1.1630 (SMA200) / 1.1657 (Fib 50%) — a zona de venda —, com as máximas de 10/20 pregões (1.1669/1.1699) acima.",
      "priceAction": "Setup de venda na retração: aguardar fechamento diário dentro da zona 1.1629-1.1657 (SMA200 / Fib 50%) seguido de fechamento de baixa abaixo do fechamento anterior e do midpoint (1,1643) — entrada de referência 1.1640, stop 1.1685 (acima da Fib 50% e da máxima de 10 pregões; 45 pips ≥ piso 1,5σ20 de 42 pips), alvo 1.1534 (mínima de 20 pregões), com 1.1476-1.1500 como extensão. A confluência Fib 61,8% / mínima D10 (1.1578-1.1582) é o degrau intermediário.",
      "recommendation": "VENDA (SHORT) NA RETRAÇÃO",
      "trigger": "Fechamento diário dentro da zona 1.1629-1.1657 (SMA200 / Fib 50%) seguido de fechamento abaixo do fechamento anterior e do midpoint 1.1643 — entrada de referência 1.1640. Válido até o fechamento de 08/09; dentro da janela de 24h do BCE (09-10/09) ou do CPI dos EUA (~10/09), reavaliar após o evento.",
      "stop": "1.1685 (acima da Fib 50% 1.1657 e da máxima de 10 pregões 1.1669; 45 pips ≥ 1,5σ20 de 42 pips) · risco sugerido ≤ 1% por operação.",
      "target": "1.1534 (mínima de 20 pregões; extensão 1.1476-1.1500, Fib 78,6% / redondo).",
      "rr": "1:2.36", "rrValue": 59,
      "justification": "A zona é a mesma de sexta — e continuar válida é o ponto: cinco fechamentos sob a SMA200 com a SMA50 abaixo mantêm o regime de baixa, e o dólar chega à semana do BCE com o NFP (+162 mil) nas costas. A regra manda vender a retração contra SMA200 + Fib 50% (1.1629-1.1657), não o mercado parado em 1,1622: 45 pips de stop acima das âncoras estruturais contra 106 até a mínima de 20 pregões — 1:2.36 com folga sobre o piso de 42 pips. O gatilho expira no fechamento de 08/09; depois disso, o evento manda."
    },
    "en": {
      "fundamental": "EUR/USD closed at 1.1622 in the 07/09/2026 session (ECB/Frankfurter reference rate; the logged-in MT5 terminal still offers no FX symbols), flat (0.00% at reference-rate precision) — the fifth consecutive close under the 200-day SMA (1.1630), with the 50-day (1.1510) also below: the bear regime crosses into decision week intact. The selling zone stands where it was — 200-day SMA (1.1630) + 50% Fib (1.1657), with the 10/20-day highs (1.1669/1.1699) above — and the trigger expires at the 08/09 close, on the eve of the ECB. Macro: the strong NFP (+162k; unemployment 4.1%) keeps pulling the dollar with DXY ~99.5 and September Fed hike odds ~60% (FOMC Sep 15-16); the ECB (2.25%) decides Sep 9-10 and US CPI (~Sep 10) closes the sequence. Indicators (SMA 50/200, sigma20, Donchian and Fibonacci) computed from the ECB/Frankfurter daily series (536 sessions, 01/08/2024 to 07/09/2026).",
      "trend": "Close under the 200-day SMA (1.1630) with the 50-day (1.1510) also below — bearish alignment for the fifth session running; the 200-day SMA / 50% Fib selling zone (1.1630-1.1657) sits right above price, with the 10/20-day highs (1.1669/1.1699) as the next ceiling.",
      "support": "1.1578 (10-day low), with the 20-day low (1.1534) and the 78.6% Fib / round confluence (1.1476-1.1500) beneath.",
      "resistance": "1.1630 (200-day SMA) / 1.1657 (50% Fib) — the selling zone —, with the 10/20-day highs (1.1669/1.1699) above.",
      "priceAction": "Sell-the-pullback setup: wait for a daily close inside the 1.1629-1.1657 zone (200-day SMA / 50% Fib) followed by a lower close below the previous close and the midpoint (1.1643) — entry reference 1.1640, stop 1.1685 (above the 50% Fib and the 10-day high; 45 pips >= the 42-pip 1.5-sigma20 floor), target 1.1534 (20-day low), with 1.1476-1.1500 as extension. The 61.8% Fib / D10 low confluence (1.1578-1.1582) is the intermediate step.",
      "recommendation": "SELL (SHORT) ON PULLBACK",
      "trigger": "Daily close inside the 1.1629-1.1657 zone (200-day SMA / 50% Fib) followed by a close below the previous close and the 1.1643 midpoint — entry reference 1.1640. Valid through the 08/09 close; inside the ECB (Sep 9-10) or US CPI (~Sep 10) 24h windows, reassess after the event.",
      "stop": "1.1685 (above the 50% Fib 1.1657 and the 10-day high 1.1669; 45 pips >= the 42-pip 1.5-sigma20 floor) · suggested risk ≤ 1% per trade.",
      "target": "1.1534 (20-day low; extension 1.1476-1.1500, 78.6% Fib / round).",
      "rr": "1:2.36", "rrValue": 59,
      "justification": "The zone is the same as Friday's — and still being valid is the point: five closes under the 200-day SMA with the 50-day below keep the bear regime on, and the dollar arrives at ECB week with the NFP (+162k) at its back. The rule says sell the pullback into the 200-day SMA + 50% Fib (1.1629-1.1657), not a market parked at 1.1622: 45 pips of stop above the structural anchors against 106 to the 20-day low — 1:2.36 with room over the 42-pip floor. The trigger expires at the 08/09 close; after that, the event is in charge."
    }
  },
  "USD/JPY": {
    "quote": "154.75", "bias": "BAIXA", "biasType": "bear",
    "pt": {
      "fundamental": "O USD/JPY fechou em 154,75 na sessão de 07/09/2026 (taxa de referência BCE/Frankfurter; o terminal MT5 logado segue sem ofertar símbolos de FX), caindo -0,96% — o fechamento rompeu as mínimas de 10/20 pregões (156,01), a Fib 78,6% (155,04) e o redondo 155,00: a condição de resolução definida na sexta (fechamento sob 156,01) foi cumprida e o alinhamento misto RESOLVEU para baixo — a leitura vira BAIXA. Resolução, porém, não é entrada: com o surto ainda quente, a σ20 subiu a 91 pips e o piso de intervenção 2,5σ20 vai a 227 pips — uma venda em 154,75 exigiria alvo a ~454 pips (150,21), sob a mínima de 9 meses (152,63), onde só resta o redondo 150,00: sem âncora estrutural que pague 1:2. O motor segue o mesmo desde 03/09: apostas de alta do BoJ acima de 25 pb na reunião de 17-18/09 e o MoF em alerta desde a intervenção de julho; o NFP forte (+162 mil) segue sustentando o dólar no outro lado do cabo de guerra. Indicadores calculados da série diária BCE/Frankfurter (536 pregões, 01/08/2024 a 07/09/2026).",
      "trend": "Fechamento sob a SMA200 (158,41) e sob a SMA50 (160,43), com a SMA50 ainda acima da SMA200 — mas o rompimento confirmado das mínimas de 10/20 pregões (156,01 → 154,75) resolve o mix para baixo: leitura de baixa; a Fib 78,6% (155,04) e o redondo 155,00 caíram por fechamento e viram resistências.",
      "support": "152.63 (mínima de 9 meses), com o redondo 152.50 abaixo — 154.75 é o próprio fechamento, mínima de 10/20 pregões.",
      "resistance": "155.04 (Fib 78,6% / redondo 155,00), com a mínima quebrada de 03/09 (156.01), a Fib 61,8% (156.94) e a Fib 50% (158.27) acima.",
      "priceAction": "Sem entrada — a direção resolveu, a geometria não: com σ20 = 91 pips, o piso de intervenção (2,5σ20 = 227 pips) exige stop acima de ~157,00 e alvo a ~150,20 — sob a mínima de 9 meses (152,63), onde só resta o redondo 150,00 (âncora de 3º nível, insuficiente sozinha). Perseguir a queda a pouco mais de 200 pips da mínima de 9 meses é entregar o stop ao MoF. Rearmar: compressão da σ20, base sobre o redondo 155,00 ou retração com estrutura até 156.01-156.94. BoJ 17-18/09 é o árbitro.",
      "recommendation": "AGUARDAR OUTRO GATILHO",
      "trigger": "Nenhum — o piso de intervenção (2,5σ20 = 227 pips) reprova a venda e a compra não tem estrutura sob as médias. Assistir à reação sobre a mínima de 9 meses (152.63) e à compressão da σ20; BoJ 17-18/09 decide o próximo capítulo.",
      "stop": "N/A (sem operação).",
      "target": "N/A (sem operação).",
      "rr": "N/A", "rrValue": 0,
      "justification": "O mix resolveu — o fechamento sob 156,01 cumpriu a condição que o relatório de sexta estabeleceu e o neutro virou baixa — mas resolver não é operar: com σ20 a 91 pips, o piso de intervenção sobe a 227 pips e a única âncora a ~454 pips abaixo é o redondo 150,00, âncora de terceiro nível. A regra existe para isso: depois de o MoF entrar no preço em julho e o BoJ ameaçar subir acima de 25 pb, o risco de gap supera qualquer Fibonacci. Fora do mercado até a volatilidade entregar uma geometria — ou o BoJ entregar uma direção."
    },
    "en": {
      "fundamental": "USD/JPY closed at 154.75 in the 07/09/2026 session (ECB/Frankfurter reference rate; the logged-in MT5 terminal still offers no FX symbols), down -0.96% — the close broke the 10/20-day lows (156.01), the 78.6% Fib (155.04) and the 155.00 round: Friday's resolution condition (a close under 156.01) was met and the mixed alignment RESOLVED bearish — the read turns BEAR. Resolution, though, is not entry: with the surge still hot, sigma20 climbed to 91 pips and the 2.5-sigma20 intervention floor rises to 227 pips — a short from 154.75 would need a target ~454 pips lower (150.21), under the 9-month low (152.63), where only the 150.00 round remains: no structural anchor pays 1:2. The engine is unchanged since Sep 3: bets on BoJ steps above 25 bp at the Sep 17-18 meeting and a MoF on alert since the July intervention; the strong NFP (+162k) keeps supporting the dollar on the other side of the tug-of-war. Indicators computed from the ECB/Frankfurter daily series (536 sessions, 01/08/2024 to 07/09/2026).",
      "trend": "Close under the 200-day SMA (158.41) and under the 50-day (160.43), with the 50-day still above the 200-day — but the confirmed break of the 10/20-day lows (156.01 → 154.75) resolves the mix bearish: a bear read; the 78.6% Fib (155.04) and the 155.00 round fell by close and turn into resistances.",
      "support": "152.63 (9-month low), with the 152.50 round beneath — 154.75 is the close itself, the 10/20-day low.",
      "resistance": "155.04 (78.6% Fib / 155.00 round), with the broken Sep 3 low (156.01), the 61.8% Fib (156.94) and the 50% Fib (158.27) above.",
      "priceAction": "No entry — the direction resolved, the geometry did not: with sigma20 = 91 pips, the intervention floor (2.5-sigma20 = 227 pips) demands a stop above ~157.00 and a target at ~150.20 — under the 9-month low (152.63), where only the 150.00 round remains (a tier-3 anchor, insufficient on its own). Chasing the drop a little over 200 pips above the 9-month low is handing the stop to the MoF. Re-arm: sigma20 compression, a base over the 155.00 round, or a structured pullback to 156.01-156.94. The BoJ Sep 17-18 is the arbiter.",
      "recommendation": "WAIT FOR ANOTHER TRIGGER",
      "trigger": "None — the intervention floor (2.5-sigma20 = 227 pips) rejects the short and a long has no structure under the averages. Watch the reaction at the 9-month low (152.63) and sigma20 compression; the BoJ Sep 17-18 decides the next chapter.",
      "stop": "N/A (no trade).",
      "target": "N/A (no trade).",
      "rr": "N/A", "rrValue": 0,
      "justification": "The mix resolved — the close under 156.01 met the condition Friday's report had set and neutral turned bear — but resolving is not trading: with sigma20 at 91 pips, the intervention floor rises to 227 pips and the only anchor ~454 pips down is the 150.00 round, a tier-three anchor. The rule exists for this: after the MoF stepped into the price in July and the BoJ threatens to hike above 25 bp, gap risk outweighs any Fibonacci. Out of the market until volatility delivers a geometry — or the BoJ delivers a direction."
    }
  },
  "AUD/USD": {
    "quote": "0.7214", "bias": "ALTA", "biasType": "bull",
    "pt": {
      "fundamental": "O AUD/USD fechou em 0,7214 na sessão de 07/09/2026 (taxa de referência BCE/Frankfurter; o terminal MT5 logado segue sem ofertar símbolos de FX), subindo +0,15% e cravando o segundo fechamento confirmatório sobre as máximas rompidas de 10/20 pregões (0,7195) — o rompimento mecânico está confirmado e o teto estrutural agora é a máxima de 9 meses (0,7257), a 42 pips. O alinhamento segue pleno de alta (SMA50 0,7042 > SMA200 0,6976). O motor é o mesmo: diferencial da RBA (4,35%, próxima reunião 29/09; bancos projetam 4,60% em novembro), CPI australiano a 3,5% e WTI ~US$ 83 — o AUD ignorou o dólar forte do NFP (+162 mil) pela terceira sessão seguida. Indicadores calculados da série diária BCE/Frankfurter (536 pregões, 01/08/2024 a 07/09/2026).",
      "trend": "Acima das SMA50 (0,7042) e SMA200 (0,6976) — alinhamento de alta pleno; segundo fechamento sobre as máximas rompidas de 10/20 pregões (0,7195), com a máxima de 9 meses (0,7257) como teto estrutural imediato.",
      "support": "0.7141 (mínima de 10 pregões), com a Fib 23,6% (0,7091) e a SMA50 (0,7042) abaixo.",
      "resistance": "0.7257 (máxima de 9 meses) — as máximas de 10/20 pregões agora são o próprio preço.",
      "priceAction": "Setup de compra no reteste pós-rompimento: aguardar fechamento diário dentro da zona 0.7141-0.7162 (mínima D10 / redondo 0,7150) seguido de fechamento de alta acima do midpoint (0,7152) — entrada de referência 0.7155, stop 0.7110 (sob a base do rompimento; 45 pips ≥ piso 1,5σ20 de 40 pips), alvo 0.7257 (máxima de 9 meses). O nível rompido (0,7195-0,7204) vira suporte no caminho.",
      "recommendation": "COMPRA (LONG) NA RETRAÇÃO",
      "trigger": "Fechamento diário dentro da zona 0.7141-0.7162 (mínima D10 / redondo 0,7150) seguido de fechamento acima do fechamento anterior e do midpoint 0,7152 — entrada de referência 0.7155. Reavaliar se disparar dentro da janela de 24h de dados da China (CPI ~09/09).",
      "stop": "0.7110 (sob a mínima de 10 pregões 0.7141, base do rompimento; 45 pips ≥ 1,5σ20 de 40 pips) · risco sugerido ≤ 1% por operação.",
      "target": "0.7257 (máxima de 9 meses).",
      "rr": "1:2.27", "rrValue": 57,
      "justification": "A confirmação veio — segundo fechamento sobre 0,7195 — e o livro não muda uma vírgula: perseguir o topo a 42 pips do teto de 9 meses paga menos de 1:1; comprar o reteste da base (0.7141-0.7162) com stop sob ela paga 1:2.27 (45 pips contra 102) com o diferencial da RBA a favor. O rompimento de Donchian-10 é o gatilho validado do sistema (+0,123R/trade no backtest 2000-2026) — a entrada disciplinada é o reteste, não a perseguição. A vantagem segue sendo de quem espera."
    },
    "en": {
      "fundamental": "AUD/USD closed at 0.7214 in the 07/09/2026 session (ECB/Frankfurter reference rate; the logged-in MT5 terminal still offers no FX symbols), up +0.15% and printing the second confirming close over the broken 10/20-day highs (0.7195) — the mechanical breakout is confirmed and the structural cap is now the 9-month high (0.7257), 42 pips away. The alignment stays fully bullish (50-day 0.7042 > 200-day 0.6976). The engine is the same: the RBA differential (4.35%, next meeting Sep 29; banks project 4.60% by November), Australian CPI at 3.5% and WTI ~$83 — the AUD has now ignored the strong-NFP dollar (+162k) for three sessions in a row. Indicators computed from the ECB/Frankfurter daily series (536 sessions, 01/08/2024 to 07/09/2026).",
      "trend": "Above the 50-day (0.7042) and 200-day (0.6976) SMAs — full bull alignment; second close over the broken 10/20-day highs (0.7195), with the 9-month high (0.7257) as the immediate structural cap.",
      "support": "0.7141 (10-day low), with the 23.6% Fib (0.7091) and the 50-day SMA (0.7042) beneath.",
      "resistance": "0.7257 (9-month high) — the 10/20-day highs are now the price itself.",
      "priceAction": "Buy-the-post-breakout-retest setup: wait for a daily close inside the 0.7141-0.7162 zone (D10 low / 0.7150 round) followed by a higher close above the midpoint (0.7152) — entry reference 0.7155, stop 0.7110 (under the breakout base; 45 pips >= the 40-pip 1.5-sigma20 floor), target 0.7257 (9-month high). The broken level (0.7195-0.7204) turns into support on the way.",
      "recommendation": "BUY (LONG) ON PULLBACK",
      "trigger": "Daily close inside the 0.7141-0.7162 zone (D10 low / 0.7150 round) followed by a close above the previous close and the 0.7152 midpoint — entry reference 0.7155. Reassess if the trigger fires inside the China-data 24h window (CPI ~Sep 9).",
      "stop": "0.7110 (under the 10-day low 0.7141, the breakout base; 45 pips >= the 40-pip 1.5-sigma20 floor) · suggested risk ≤ 1% per trade.",
      "target": "0.7257 (9-month high).",
      "rr": "1:2.27", "rrValue": 57,
      "justification": "The confirmation came — a second close over 0.7195 — and the book does not change a comma: chasing the top 42 pips under the 9-month ceiling pays less than 1:1; buying the retest of the base (0.7141-0.7162) with the stop under it pays 1:2.27 (45 pips against 102) with the RBA differential behind. The Donchian-10 breakout is the system's validated trigger (+0.123R/trade in the 2000-2026 backtest) — the disciplined entry is the retest, not the chase. The edge still belongs to whoever waits."
    }
  },
  "GBP/USD": {
    "quote": "1.3531", "bias": "ALTA", "biasType": "bull",
    "pt": {
      "fundamental": "O GBP/USD fechou em 1,3531 na sessão de 07/09/2026 (taxa de referência BCE/Frankfurter; o terminal MT5 logado segue sem ofertar símbolos de FX), estável (+0,01%) acima do redondo 1,3500 — a calmaria antes da semana decisiva. O alinhamento de alta segue pleno (SMA50 1,3454 > SMA200 1,3440; preço acima das duas) e a confluência das médias deslizou para 1.3440-1.3454: a zona de compra foi reprecificada. O NFP forte (+162 mil) não derrubou o cable na sexta e nada o testou hoje; BoE a 3,75% (voto 6-3) decide em 17/09, CPI do Reino Unido a 2,9%, e o CPI dos EUA (~10/09) é o teste de meio de semana. Indicadores calculados da série diária BCE/Frankfurter (536 pregões, 01/08/2024 a 07/09/2026).",
      "trend": "Preço acima das SMA50 (1,3454) e SMA200 (1,3440) — alinhamento de alta pleno com o cruzamento engordando; a retração de 02/09 (1,3483) segue como piso intermediário, com a Fib 38,2% (1,3566) como resistência imediata e a máxima de 10 pregões (1,3632) acima.",
      "support": "1.3483 (mínimas de 10/20 pregões), com a confluência SMA50/SMA200 (1.3440-1.3454) e a Fib 61,8% (1.3411) abaixo.",
      "resistance": "1.3566 (Fib 38,2%), com a máxima de 10 pregões (1,3632) e a de 9 meses (1,3817) acima.",
      "priceAction": "Setup de compra na retração: aguardar fechamento diário dentro da confluência 1.3440-1.3454 (SMA200/SMA50) seguido de fechamento de alta acima do midpoint (1,3447) — entrada de referência 1.3447, stop 1.3390 (sob a Fib 61,8% 1.3411 e o redondo 1.3400; 57 pips ≥ piso 1,5σ20 de 49 pips), alvo 1.3566 (Fib 38,2%), com 1.3632 (máxima de 10 pregões) como extensão. A perda por fechamento da Fib 61,8% (1.3411) invalida o setup.",
      "recommendation": "COMPRA (LONG) NA RETRAÇÃO",
      "trigger": "Fechamento diário dentro da confluência 1.3440-1.3454 (SMA200/SMA50) seguido de fechamento acima do fechamento anterior e do midpoint 1.3447 — entrada de referência 1.3447. Reavaliar se disparar dentro da janela de 24h do CPI dos EUA (~10/09); BoE 17/09 mais adiante.",
      "stop": "1.3390 (sob a Fib 61,8% 1.3411 e o redondo 1.3400; 57 pips ≥ 1,5σ20 de 49 pips) · risco sugerido ≤ 1% por operação.",
      "target": "1.3566 (Fib 38,2%; extensão 1.3632, máxima de 10 pregões).",
      "rr": "1:2.09", "rrValue": 52,
      "justification": "Mesmo mapa, zona reprecificada: as médias deslizaram e a confluência agora é 1.3440-1.3454 — a entrada sobe junto (1.3447) e o alvo na Fib 38,2% (1.3566) comprime o prêmio para 1:2.09, ainda acima do portão, com o stop de 57 pips cumprindo o piso de 49 com folga. A hierarquia manda ancorar na confluência das médias (topo da lista) e o cable segue o par mais firme contra o dólar depois do NFP. Compra-se a retração de ~85 pips, não o mercado a 35 pips da Fib 38,2%."
    },
    "en": {
      "fundamental": "GBP/USD closed at 1.3531 in the 07/09/2026 session (ECB/Frankfurter reference rate; the logged-in MT5 terminal still offers no FX symbols), flat (+0.01%) above the 1.3500 round — the calm before decision week. The bull alignment stands (50-day 1.3454 > 200-day 1.3440; price above both) and the averages' confluence has drifted up to 1.3440-1.3454: the buying zone was re-priced. The strong NFP (+162k) failed to knock cable down on Friday and nothing tested it today; the BoE at 3.75% (6-3 vote) decides Sep 17, UK CPI at 2.9%, and US CPI (~Sep 10) is the mid-week test. Indicators computed from the ECB/Frankfurter daily series (536 sessions, 01/08/2024 to 07/09/2026).",
      "trend": "Price above the 50-day (1.3454) and 200-day (1.3440) SMAs — full bull alignment with the cross thickening; the Sep 2 pullback (1.3483) remains the intermediate floor, with the 38.2% Fib (1.3566) as immediate resistance and the 10-day high (1.3632) above.",
      "support": "1.3483 (10/20-day lows), with the 50/200-day SMA confluence (1.3440-1.3454) and the 61.8% Fib (1.3411) beneath.",
      "resistance": "1.3566 (38.2% Fib), with the 10-day high (1.3632) and the 9-month high (1.3817) above.",
      "priceAction": "Buy-the-pullback setup: wait for a daily close inside the 1.3440-1.3454 confluence (200/50-day SMAs) followed by a higher close above the midpoint (1.3447) — entry reference 1.3447, stop 1.3390 (under the 61.8% Fib 1.3411 and the 1.3400 round; 57 pips >= the 49-pip 1.5-sigma20 floor), target 1.3566 (38.2% Fib), with 1.3632 (10-day high) as extension. A close below the 61.8% Fib (1.3411) invalidates the setup.",
      "recommendation": "BUY (LONG) ON PULLBACK",
      "trigger": "Daily close inside the 1.3440-1.3454 confluence (200/50-day SMAs) followed by a close above the previous close and the 1.3447 midpoint — entry reference 1.3447. Reassess if the trigger fires inside the US CPI (~Sep 10) 24h window; the BoE Sep 17 meeting is further out.",
      "stop": "1.3390 (under the 61.8% Fib 1.3411 and the 1.3400 round; 57 pips >= the 49-pip 1.5-sigma20 floor) · suggested risk ≤ 1% per trade.",
      "target": "1.3566 (38.2% Fib; extension 1.3632, the 10-day high).",
      "rr": "1:2.09", "rrValue": 52,
      "justification": "Same map, re-priced zone: the averages drifted and the confluence is now 1.3440-1.3454 — the entry rises with them (1.3447) and the 38.2% Fib target (1.3566) squeezes the premium to 1:2.09, still through the gate, with the 57-pip stop clearing the 49-pip floor with room. The anchor hierarchy says tie the stop to the averages' confluence (top of the list), and cable remains the firmest pair against the dollar post-NFP. Buy the ~85-pip pullback, not a market 35 pips under the 38.2% Fib."
    }
  },
  "EUR/JPY": {
    "quote": "179.85", "bias": "BAIXA", "biasType": "bear",
    "pt": {
      "fundamental": "O EUR/JPY fechou em 179,85 na sessão de 07/09/2026 (taxa de referência BCE/Frankfurter; o terminal MT5 logado segue sem ofertar símbolos de FX), caindo -0,96% e cravando mínima de 9 meses: o fechamento rompeu a mínima de 10/20 pregões (181,20) e a mínima de 9 meses anterior (180,28) — a condição de resolução definida na sexta (fechamento sob 181,20) foi cumprida com folga e a leitura vira BAIXA (a quebra da mínima de 9 meses, nível maior, ainda aguarda fechamento confirmatório — que de qualquer forma não mudaria o veredito). A geometria segue bloqueada: σ20 subiu a 96 pips e o piso de intervenção 2,5σ20 vai a 240 pips — uma venda em 179,85 exigiria alvo a ~480 pips (175,05), território sem nenhuma âncora da janela de 9 meses. O BCE decide em 09-10/09 e o BoJ em 17-18/09 — dois hawkish puxando em direções opostas, com o yen levando a melhor desde 03/09. Indicadores calculados da série diária BCE/Frankfurter (536 pregões, 01/08/2024 a 07/09/2026).",
      "trend": "Fechamento sob a SMA200 (184,20) e sob a SMA50 (184,63), com a SMA50 ainda acima da SMA200 — mas o rompimento confirmado das mínimas de 10/20 pregões e de 9 meses (181,20 → 179,85) resolve o mix para baixo: leitura de baixa em mínima de 9 meses.",
      "support": "179.85 é o próprio fechamento — mínima de 9 meses —; abaixo, apenas os redondos 179,50 / 178,00.",
      "resistance": "180.28 (mínima de 9 meses quebrada) / 181.20-181.59 (as mínimas quebradas de 03-04/09), com a Fib 78,6% (181,54) no meio caminho e a Fib 61,8% (182,86) acima.",
      "priceAction": "Sem entrada — a direção resolveu para baixo, mas o piso de intervenção (2,5σ20 = 240 pips) reprova a perseguição: venda em 179,85 exigiria alvo a 175,05, sem âncora à frente; compra em mínima de 9 meses sob duas médias é aposta contra o BoJ. Rearmar: compressão da σ20 ou reteste estruturado de 181.20-181.59. BCE 09-10/09 e BoJ 17-18/09 arbitram.",
      "recommendation": "AGUARDAR OUTRO GATILHO",
      "trigger": "Nenhum — alinhamento resolvido para baixo, mas o piso de intervenção (2,5σ20 = 240 pips) e a ausência de âncoras abaixo da mínima de 9 meses reprovam qualquer setup. Assistir à reação nos redondos 179,50 / 178,00 e à compressão da σ20.",
      "stop": "N/A (sem operação).",
      "target": "N/A (sem operação).",
      "rr": "N/A", "rrValue": 0,
      "justification": "O cross cravou o que o relatório de sexta apontou: fechamento sob 181,20 resolve o mix — e veio com folga, rompendo também a mínima de 9 meses (180,28). Mas mínima de 9 meses com σ20 a 96 pips é o pior cenário para entrar: o piso de intervenção (240 pips) manda procurar âncora a ~480 pips abaixo e não há nenhuma na janela — só redondos. Entre um BCE hawkish e um BoJ hawkish, o desempate é o evento, não o preço. Fora do mercado."
    },
    "en": {
      "fundamental": "EUR/JPY closed at 179.85 in the 07/09/2026 session (ECB/Frankfurter reference rate; the logged-in MT5 terminal still offers no FX symbols), down -0.96% and printing a 9-month low: the close broke the 10/20-day low (181.20) and the prior 9-month low (180.28) — Friday's resolution condition (a close under 181.20) was met with room to spare and the read turns BEAR (the 9-month-low break, a major level, still awaits a confirming close — which would not change the verdict anyway). The geometry stays blocked: sigma20 climbed to 96 pips and the 2.5-sigma20 intervention floor rises to 240 pips — a short from 179.85 would need a target ~480 pips lower (175.05), territory with no anchor from the 9-month window. The ECB decides Sep 9-10 and the BoJ Sep 17-18 — two hawkish central banks pulling in opposite directions, with the yen winning since Sep 3. Indicators computed from the ECB/Frankfurter daily series (536 sessions, 01/08/2024 to 07/09/2026).",
      "trend": "Close under the 200-day SMA (184.20) and under the 50-day (184.63), with the 50-day still above the 200-day — but the confirmed break of the 10/20-day and 9-month lows (181.20 → 179.85) resolves the mix bearish: a bear read at a 9-month low.",
      "support": "179.85 is the close itself — the 9-month low; beneath it, only the 179.50 / 178.00 rounds.",
      "resistance": "180.28 (broken 9-month low) / 181.20-181.59 (the broken Sep 3-4 lows), with the 78.6% Fib (181.54) halfway and the 61.8% Fib (182.86) above.",
      "priceAction": "No entry — the direction resolved bearish, but the intervention floor (2.5-sigma20 = 240 pips) rejects the chase: a short from 179.85 would need a target at 175.05, with no anchor ahead; a long at a 9-month low under two averages is a bet against the BoJ. Re-arm: sigma20 compression or a structured retest of 181.20-181.59. The ECB Sep 9-10 and BoJ Sep 17-18 arbitrate.",
      "recommendation": "WAIT FOR ANOTHER TRIGGER",
      "trigger": "None — the alignment resolved bearish, but the intervention floor (2.5-sigma20 = 240 pips) and the absence of anchors beneath the 9-month low reject any setup. Watch the reaction at the 179.50 / 178.00 rounds and sigma20 compression.",
      "stop": "N/A (no trade).",
      "target": "N/A (no trade).",
      "rr": "N/A", "rrValue": 0,
      "justification": "The cross printed what Friday's report pointed to: a close under 181.20 resolves the mix — and it came with room, breaking the 9-month low (180.28) too. But a 9-month low with sigma20 at 96 pips is the worst entry scenario: the intervention floor (240 pips) demands an anchor ~480 pips below and none exists in the window — only rounds. Between a hawkish ECB and a hawkish BoJ, the tiebreak is the event, not the price. Out of the market."
    }
  },
  "GBP/JPY": {
    "quote": "209.39", "bias": "BAIXA", "biasType": "bear",
    "pt": {
      "fundamental": "O GBP/JPY fechou em 209,39 na sessão de 07/09/2026 (taxa de referência BCE/Frankfurter; o terminal MT5 logado segue sem ofertar símbolos de FX), caindo -0,95% — o fechamento rompeu a mínima de 10/20 pregões (210,57) e aniquilou o rebote de sexta: a condição de resolução definida na sexta (fechamento sob 210,57) foi cumprida, o mix RESOLVEU para baixo e a leitura vira BAIXA. O piso de intervenção sobe junto com a turbulência: σ20 = 123 pips → 2,5σ20 = 307 pips; uma venda exigiria alvo a ~614 pips (203,25), sob a mínima de 9 meses (205,38). BoE a 3,75% e BoJ decidem na mesma semana (17-18/09). Indicadores calculados da série diária BCE/Frankfurter (536 pregões, 01/08/2024 a 07/09/2026).",
      "trend": "Fechamento sob a SMA200 (212,88) e sob a SMA50 (215,84), com a SMA50 ainda acima da SMA200 — mas o rompimento confirmado da mínima de 10/20 pregões (210,57 → 209,39) resolve o mix para baixo: leitura de baixa; a Fib 78,6% (208,32) é o próximo degrau.",
      "support": "208.32 (Fib 78,6%), com a mínima de 9 meses (205.38) abaixo.",
      "resistance": "210.57-211.41 (as mínimas quebradas de 03-04/09), com a Fib 50% (212,26) e a SMA200 (212,88) acima.",
      "priceAction": "Sem entrada — direção resolvida para baixo, geometria bloqueada: com σ20 = 123 pips, o piso de intervenção (2,5σ20 = 307 pips) manda procurar âncora a ~614 pips e ela está sob a mínima de 9 meses (205,38); compra não tem estrutura. Rearmar: compressão da σ20 ou reteste estruturado de 210.57-211.41. BoE/BoJ em 17-18/09 arbitram.",
      "recommendation": "AGUARDAR OUTRO GATILHO",
      "trigger": "Nenhum — o piso de intervenção (2,5σ20 = 307 pips) reprova qualquer geometria. Assistir à reação sobre a Fib 78,6% (208,32) e à compressão da σ20.",
      "stop": "N/A (sem operação).",
      "target": "N/A (sem operação).",
      "rr": "N/A", "rrValue": 0,
      "justification": "Sexta foi rebote, segunda foi resolução: 209,39 fecha o debate do alinhamento — é baixa. Mas o cross segue volátil demais para o livro: σ20 a 123 pips faz o piso de intervenção subir a 307 pips, e a única coisa a ~614 pips abaixo é o vazio sob a mínima de 9 meses. Depois da intervenção de julho e do surto de 03/09, a lição é a mesma: não se paga caro para ficar na frente do MoF. A posição segue fora; a estrutura, esperando."
    },
    "en": {
      "fundamental": "GBP/JPY closed at 209.39 in the 07/09/2026 session (ECB/Frankfurter reference rate; the logged-in MT5 terminal still offers no FX symbols), down -0.95% — the close broke the 10/20-day low (210.57) and wiped out Friday's bounce: Friday's resolution condition (a close under 210.57) was met, the mix RESOLVED bearish and the read turns BEAR. The intervention floor rises with the turbulence: sigma20 = 123 pips → 2.5-sigma20 = 307 pips; a short would need a target ~614 pips lower (203.25), under the 9-month low (205.38). The BoE at 3.75% and the BoJ decide in the same week (Sep 17-18). Indicators computed from the ECB/Frankfurter daily series (536 sessions, 01/08/2024 to 07/09/2026).",
      "trend": "Close under the 200-day SMA (212.88) and under the 50-day (215.84), with the 50-day still above the 200-day — but the confirmed break of the 10/20-day low (210.57 → 209.39) resolves the mix bearish: a bear read; the 78.6% Fib (208.32) is the next step down.",
      "support": "208.32 (78.6% Fib), with the 9-month low (205.38) beneath.",
      "resistance": "210.57-211.41 (the broken Sep 3-4 lows), with the 50% Fib (212.26) and the 200-day SMA (212.88) above.",
      "priceAction": "No entry — direction resolved bearish, geometry blocked: with sigma20 = 123 pips, the intervention floor (2.5-sigma20 = 307 pips) demands an anchor ~614 pips away and it sits under the 9-month low (205.38); a long has no structure. Re-arm: sigma20 compression or a structured retest of 210.57-211.41. The BoE/BoJ Sep 17-18 week arbitrates.",
      "recommendation": "WAIT FOR ANOTHER TRIGGER",
      "trigger": "None — the intervention floor (2.5-sigma20 = 307 pips) rejects any geometry. Watch the reaction at the 78.6% Fib (208.32) and sigma20 compression.",
      "stop": "N/A (no trade).",
      "target": "N/A (no trade).",
      "rr": "N/A", "rrValue": 0,
      "justification": "Friday was a bounce, Monday was the resolution: 209.39 closes the alignment debate — it is bear. But the cross is still too violent for the book: sigma20 at 123 pips pushes the intervention floor to 307 pips, and the only thing ~614 pips below is the void under the 9-month low. After the July intervention and the Sep 3 surge, the lesson is the same: do not pay up to stand in front of the MoF. The position stays out; the structure waits."
    }
  }
}

fd_json = json.dumps(FD, ensure_ascii=False, indent=8)
json.loads(fd_json)  # sanity: must be valid JSON (hence valid JS)
assert list(json.loads(fd_json).keys()) == ["EUR/USD", "USD/JPY", "AUD/USD", "GBP/USD", "EUR/JPY", "GBP/JPY"]
# rrValue consistency gate
for p, d in FD.items():
    if d["pt"]["rr"] != "N/A":
        R = float(d["pt"]["rr"].split(":")[1])
        assert d["pt"]["rr"] == d["en"]["rr"] and d["pt"]["rrValue"] == d["en"]["rrValue"], p
        assert d["pt"]["rrValue"] == int(R * 25 + 0.5), p
        assert d["pt"]["stop"].endswith("risco sugerido ≤ 1% por operação."), p
        assert d["en"]["stop"].endswith("suggested risk ≤ 1% per trade."), p
    else:
        assert d["pt"]["rrValue"] == 0 and d["en"]["rrValue"] == 0, p
# biasType gate vs today's computed alignment (JPY pairs resolved bear by the confirmed breakdowns)
ALIGN = {"EUR/USD": "bear", "USD/JPY": "bear", "AUD/USD": "bull",
         "GBP/USD": "bull", "EUR/JPY": "bear", "GBP/JPY": "bear"}
for p, d in FD.items():
    assert d["biasType"] == ALIGN[p], p

P = DOCS + "/index.html"
html = open(P, encoding="utf-8").read()

html, n = re.subn(r"        const forexData = \{.*?\n\};",
                  "        const forexData = " + fd_json + ";", html, count=1, flags=re.DOTALL)
if n != 1:
    print("FAIL: forexData block"); sys.exit(1)

html = rep(html, "Reports generated on: " + OLD_TS, "Reports generated on: " + TS, "ts en badge+i18n", count=2)
html = rep(html, 'generatedAt: "Relatórios gerados em: ' + OLD_TS + '"', 'generatedAt: "Relatórios gerados em: ' + TS + '"', "ts pt i18n")
html = rep(html, 'dataBasis: "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 535 daily sessions (01/08/2024–04/09/2026).",',
                 'dataBasis: "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 536 daily sessions (01/08/2024–07/09/2026).",', "basis en")
html = rep(html, 'dataBasis: "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, σ20 e Donchian calculados · 535 pregões (01/08/2024 a 04/09/2026).",',
                 'dataBasis: "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, σ20 e Donchian calculados · 536 pregões (01/08/2024 a 07/09/2026).",', "basis pt")

html, n = re.subn(
    r"        const dailyChanges = \{.*?\n        \};",
    '''        const dailyChanges = {
            "EUR/USD": "+0.00%",
            "USD/JPY": "-0.96%",
            "AUD/USD": "+0.15%",
            "GBP/USD": "+0.01%",
            "EUR/JPY": "-0.96%",
            "GBP/JPY": "-0.95%"
        };''', html, count=1, flags=re.DOTALL)
if n != 1:
    print("FAIL: dailyChanges"); sys.exit(1)

html, n = re.subn(
    r"        const macroDrivers = \{.*?\n        \};",
    '''        const macroDrivers = {
            "EUR/USD": {
                en: ["5th close < SMA200", "Fed hike ~60%", "ECB Sep 9-10"],
                pt: ["5º fech. sob SMA200", "Alta Fed ~60%", "BCE 09-10/09"]
            },
            "USD/JPY": {
                en: ["Bearish resolution", "2.5-sigma floor 227p", "BoJ Sep 17-18"],
                pt: ["Resolução de baixa", "Piso 2,5-sigma 227p", "BoJ 17-18/09"]
            },
            "AUD/USD": {
                en: ["D10/20 breakout confirmed", "RBA 4.35%", "Fed hike ~60%"],
                pt: ["Rompimento D10/D20 confirmado", "RBA 4,35%", "Alta Fed ~60%"]
            },
            "GBP/USD": {
                en: ["Bull alignment holds", "BoE 3.75% 6-3", "Fed hike ~60%"],
                pt: ["Alinhamento de alta segue", "BoE 3,75% 6-3", "Alta Fed ~60%"]
            },
            "EUR/JPY": {
                en: ["9-month low close", "2.5-sigma floor 240p", "ECB/BoJ Sep 9-18"],
                pt: ["Fech. em mínima de 9 meses", "Piso 2,5-sigma 240p", "BCE/BoJ 09-18/09"]
            },
            "GBP/JPY": {
                en: ["Bearish resolution", "2.5-sigma floor 307p", "BoE/BoJ Sep 17"],
                pt: ["Resolução de baixa", "Piso 2,5-sigma 307p", "BoE/BoJ 17/09"]
            }
        };''', html, count=1, flags=re.DOTALL)
if n != 1:
    print("FAIL: macroDrivers"); sys.exit(1)

# ---- news wire digest (newsData): update stamp + prepend the yen-second-wave item ----
html = rep(html, 'updated: "06/09/2026 14:00 UTC",', 'updated: "' + TS + '",', "newsData.updated")

NEWS_ITEM = '''                {
                    date: "07/09/2026",
                    category: "cb",
                    impact: "high",
                    pairs: ["USD/JPY", "EUR/JPY", "GBP/JPY"],
                    pt: {
                        headline: "Iene estende o surto: USD/JPY perde 155 e EUR/JPY crava mínima de 9 meses",
                        summary: "A segunda onda do surto do iene varreu os cruzamentos na abertura da semana: USD/JPY caiu -0,96% para 154,75 — terceiro pregão de queda e primeiro fechamento sob o redondo 155,00 —, EUR/JPY caiu -0,96% para 179,85 (mínima de 9 meses, rompendo 180,28) e GBP/JPY recuou -0,95% para 209,39. O motor segue o mesmo desde 03/09: apostas de alta do BoJ acima de 25 pb na reunião de 17-18/09 e o MoF em alerta desde a intervenção de julho; a σ20 dos pares com iene subiu para 91-123 pips.",
                        take: "O rompimento confirmado cumpre a condição de resolução que o relatório de sexta estabeleceu: os três pares com iene viram BAIXA na edição de hoje — mas a σ20 mais alta endurece o piso de intervenção (2,5σ20) para 227-307 pips e nenhuma âncora estrutural paga 1:2. Seguem em AGUARDAR até a volatilidade comprimir; não se corre na frente do BoJ/MoF."
                    },
                    en: {
                        headline: "Yen extends the surge: USD/JPY loses 155 and EUR/JPY prints a 9-month low",
                        summary: "The yen surge's second wave swept the crosses at the open of the week: USD/JPY fell -0.96% to 154.75 — a third down session and the first close under the 155.00 round —, EUR/JPY dropped -0.96% to 179.85 (a 9-month low, breaking 180.28) and GBP/JPY slid -0.95% to 209.39. The engine is the same since Sep 3: bets on BoJ steps above 25 bp at the Sep 17-18 meeting and a MoF on alert since the July intervention; the yen pairs' sigma20 climbed to 91-123 pips.",
                        take: "The confirmed breakdown meets the resolution condition Friday's report had set: all three yen pairs turn BEARISH in today's edition — but the higher sigma20 hardens the intervention floor (2.5-sigma20) to 227-307 pips and no structural anchor pays 1:2. They stay on WAIT until volatility compresses; do not front-run the BoJ/MoF."
                    }
                },
'''
html = rep(html, "            items: [\n                {\n                    date: \"04/09/2026 12:30 UTC\"",
            "            items: [\n" + NEWS_ITEM + "                {\n                    date: \"04/09/2026 12:30 UTC\"", "newsData item prepend")

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
    h = rep(h, '<span class="ts-date">04·09·26</span>', '<span class="ts-date">07·09·26</span>', f"{tag} ts-date")
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
    "EUR/USD": '<div class="next-event"><span class="ne-tag"><span class="lang-en">Next focus</span><span class="lang-pt" style="display:none;">Próximo foco</span></span> <span class="lang-en">ECB 09-10/09 · FOMC 15-16/09</span><span class="lang-pt" style="display:none;">BCE 09-10/09 · FOMC 15-16/09</span></div>',
    "USD/JPY": '<div class="next-event"><span class="ne-tag"><span class="lang-en">Next focus</span><span class="lang-pt" style="display:none;">Próximo foco</span></span> <span class="lang-en">BoJ 17-18/09 · FOMC 15-16/09</span><span class="lang-pt" style="display:none;">BoJ 17-18/09 · FOMC 15-16/09</span></div>',
    "AUD/USD": '<div class="next-event"><span class="ne-tag"><span class="lang-en">Next focus</span><span class="lang-pt" style="display:none;">Próximo foco</span></span> <span class="lang-en">China CPI ~09/09 · RBA 29/09</span><span class="lang-pt" style="display:none;">CPI da China ~09/09 · RBA 29/09</span></div>',
    "GBP/USD": '<div class="next-event"><span class="ne-tag"><span class="lang-en">Next focus</span><span class="lang-pt" style="display:none;">Próximo foco</span></span> <span class="lang-en">BoE 17/09 · FOMC 15-16/09</span><span class="lang-pt" style="display:none;">BoE 17/09 · FOMC 15-16/09</span></div>',
    "EUR/JPY": '<div class="next-event"><span class="ne-tag"><span class="lang-en">Next focus</span><span class="lang-pt" style="display:none;">Próximo foco</span></span> <span class="lang-en">ECB 09-10/09 · BoJ 17-18/09</span><span class="lang-pt" style="display:none;">BCE 09-10/09 · BoJ 17-18/09</span></div>',
    "GBP/JPY": '<div class="next-event"><span class="ne-tag"><span class="lang-en">Next focus</span><span class="lang-pt" style="display:none;">Próximo foco</span></span> <span class="lang-en">BoE 17/09 · BoJ 17-18/09</span><span class="lang-pt" style="display:none;">BoE 17/09 · BoJ 17-18/09</span></div>',
}

FD["EUR/USD"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action sell">SELL</span> — fifth close under the 200-day; short the 1.1629-1.1657 zone, target 1.1534 (1:2.36)</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action sell">VENDA</span> — quinto fechamento sob a SMA200; vender a zona 1.1629-1.1657, alvo 1.1534 (1:2,36)</span>',
    "_tier_en": "Good", "_tier_pt": "Boa",
})
FD["USD/JPY"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — breakdown close 154.75 (under the 155 round) resolves the mix bearish; the 227-pip intervention floor still blocks the book</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — fechamento de rompimento em 154,75 (sob o redondo 155) resolve o mix para baixo; o piso de intervenção de 227 pips segue bloqueando o livro</span>',
    "_tier_en": "Moderate", "_tier_pt": "Moderada",
})
FD["AUD/USD"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action buy">BUY</span> — second confirming close over the D10/D20 highs (0.7195); buy the retest 0.7141-0.7162, target 0.7257 (1:2.27)</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action buy">COMPRA</span> — segundo fechamento confirmatório sobre as máximas D10/D20 (0,7195); comprar o reteste 0.7141-0.7162, alvo 0.7257 (1:2,27)</span>',
    "_tier_en": "High", "_tier_pt": "Alta",
})
FD["GBP/USD"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action buy">BUY</span> — bull alignment holds; buy the 1.3440-1.3454 confluence, target 1.3566 (1:2.09)</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action buy">COMPRA</span> — alinhamento de alta segue; comprar a confluência 1.3440-1.3454, alvo 1.3566 (1:2,09)</span>',
    "_tier_en": "Good", "_tier_pt": "Boa",
})
FD["EUR/JPY"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — fresh 9-month low (179.85) resolves the mix bearish; the 240-pip intervention floor rejects all geometry</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — mínima de 9 meses (179,85) resolve o mix para baixo; o piso de intervenção de 240 pips rejeita qualquer geometria</span>',
    "_tier_en": "Moderate", "_tier_pt": "Moderada",
})
FD["GBP/JPY"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — breakdown close 209.39 resolves the mix bearish; the 307-pip intervention floor rejects all geometry</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — fechamento de rompimento 209,39 resolve o mix para baixo; o piso de intervenção de 307 pips rejeita qualquer geometria</span>',
    "_tier_en": "Moderate", "_tier_pt": "Moderada",
})

# bias flips today: neutral -> bear on the three yen pairs (confirmed breakdowns)
BIAS_SWAP = {
    "USD/JPY": ("neutral", "bear", "USD/JPY - NEUTRAL", "USD/JPY - BEARISH", "USD/JPY - NEUTRO", "USD/JPY - BAIXA"),
    "EUR/JPY": ("neutral", "bear", "EUR/JPY - NEUTRAL", "EUR/JPY - BEARISH", "EUR/JPY - NEUTRO", "EUR/JPY - BAIXA"),
    "GBP/JPY": ("neutral", "bear", "GBP/JPY - NEUTRAL", "GBP/JPY - BEARISH", "GBP/JPY - NEUTRO", "GBP/JPY - BAIXA"),
}

CHIPS = {
    "EUR/USD": [],
    "USD/JPY": [('<span class="macro-chip lang-en">¥ surge · BoJ 17-18</span>', '<span class="macro-chip lang-en">¥ new lows · BoJ 17-18</span>', "en"),
                ('<span class="macro-chip lang-pt" style="display:none;">Surto do yen · BoJ 17-18</span>', '<span class="macro-chip lang-pt" style="display:none;">Novas mínimas do yen · BoJ 17-18</span>', "pt")],
    "AUD/USD": [],
    "GBP/USD": [],
    "EUR/JPY": [('<span class="macro-chip lang-en">¥ surge · BoJ 17-18</span>', '<span class="macro-chip lang-en">¥ 9-mo low · BoJ 17-18</span>', "en"),
                ('<span class="macro-chip lang-pt" style="display:none;">Surto do yen · BoJ 17-18</span>', '<span class="macro-chip lang-pt" style="display:none;">Yen em mínima de 9 meses</span>', "pt")],
    "GBP/JPY": [('<span class="macro-chip lang-en">¥ surge · BoJ 17-18</span>', '<span class="macro-chip lang-en">¥ new lows · BoJ 17-18</span>', "en"),
                ('<span class="macro-chip lang-pt" style="display:none;">Surto do yen · BoJ 17-18</span>', '<span class="macro-chip lang-pt" style="display:none;">Novas mínimas do yen · BoJ 17-18</span>', "pt")],
}

# gauge percent computed from support/resistance leading numbers vs quote
GAUGE = {"EUR/USD": ("85", "1.1578", "1.1630"), "USD/JPY": ("88", "152.63", "155.04"),
         "AUD/USD": ("63", "0.7141", "0.7257"), "GBP/USD": ("58", "1.3483", "1.3566"),
         "EUR/JPY": ("0", "179.85", "180.28"), "GBP/JPY": ("48", "208.32", "210.57")}
# conviction score = round(R*3) clamped to [3,10]; 0 for WAIT pairs
TIER = {"EUR/USD": ("7/10", "", 7), "USD/JPY": ("0/10", "t-mod", 0),
        "AUD/USD": ("7/10", "", 7), "GBP/USD": ("6/10", "", 6),
        "EUR/JPY": ("0/10", "t-mod", 0), "GBP/JPY": ("0/10", "t-mod", 0)}

# verdict classes/labels are unchanged today on all six pages (sell/wait/buy/wait/wait/wait)
BADGE = {}

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
# No watching ticket fired since 04/09 (no closes inside the trigger zones) and none
# resolves today; the three live tickets are carried into the 07/09 basis, with
# GBP/USD re-priced to the drifted averages.
for t in led["watching"]:
    if t["pair"] == "EUR/USD":
        t["reportDate"] = TS_DATE
        t["triggerRule"] = "daily close inside 1.1629-1.1657 (SMA200 + 50% Fib) followed by a close below the previous close and the 1.1643 midpoint; valid through the 08/09 close — inside the ECB (09-10/09) or US CPI (~10/09) 24h windows, reassess after the event"
        t["note"] = "carried into ECB week unchanged: the 07/09 close (1.1622, fifth under the SMA200) never reached the zone; stop 1.1685 over the Fib50 and the 10-day high, 45 pips >= the 42-pip 1.5-sigma20 floor"
    if t["pair"] == "AUD/USD":
        t["reportDate"] = TS_DATE
        t["note"] = "second confirming close (0.7214) over the broken 0.7195 D10/D20 highs — breakout confirmed, ticket carried; stop 45 pips >= the 40-pip 1.5-sigma20 floor"
    if t["pair"] == "GBP/USD":
        t["reportDate"] = TS_DATE
        t["entry"] = 1.3447; t["stop"] = 1.3390; t["target"] = 1.3566; t["plannedR"] = 2.09
        t["triggerRule"] = "daily close inside 1.3440-1.3454 (SMA200/SMA50 confluence) followed by a close above the previous close and the 1.3447 midpoint; skip if inside the US CPI (~10/09) 24h window"
        t["note"] = "zone re-priced with the drifted averages (SMA200 1.3440 / SMA50 1.3454); stop 1.3390 under the 61.8% Fib 1.3411 and the 1.3400 round, 57 pips >= the 49-pip 1.5-sigma20 floor"
assert len([t for t in led["watching"] if t["pair"] == "EUR/USD"]) == 1
assert len([t for t in led["watching"] if t["pair"] == "AUD/USD"]) == 1
assert len([t for t in led["watching"] if t["pair"] == "GBP/USD"]) == 1
with open(LED, "w", encoding="utf-8") as f:
    json.dump(led, f, ensure_ascii=False, indent=2)
print("OK: track-record.json (3 tickets carried, GBP/USD re-priced, no resolutions)")

# =====================================================================
# 4. news.html — hero dateline + kicker + new wire card + basis note
# =====================================================================
NP = DOCS + "/news.html"
nh = open(NP, encoding="utf-8").read()
nh = rep(nh, '<span class="lang-en">Wire updated: 06/09/2026 14:00 UTC</span>', '<span class="lang-en">Wire updated: ' + TS + '</span>', "news hero en")
nh = rep(nh, '<span class="lang-pt" style="display:none;">Telégrafo atualizado em: 06/09/2026 14:00 UTC</span>', '<span class="lang-pt" style="display:none;">Telégrafo atualizado em: ' + TS + '</span>', "news hero pt")
nh = rep(nh, '<span class="lang-en">Market Wire · Weekend Edition</span><span class="lang-pt" style="display:none;">Telégrafo da Mesa · Edição de Fim de Semana</span>',
             '<span class="lang-en">Market Wire · Central Bank Week</span><span class="lang-pt" style="display:none;">Telégrafo da Mesa · Semana de Bancos Centrais</span>', "news kicker")
nh = rep(nh, "numbers and dates reflect the report's data basis of 04/09/2026", "numbers and dates reflect the report's data basis of 07/09/2026", "news note en")
nh = rep(nh, "refletem a base de dados do relatório de 04/09/2026", "refletem a base de dados do relatório de 07/09/2026", "news note pt")

NEWS_CARD = '''                <!-- News 0: Yen second wave / breakdown resolves the yen biases -->
                <article class="news-card">
                    <div class="news-card-top">
                        <span class="news-cat"><span class="lang-en">Central Banks</span><span class="lang-pt" style="display:none;">Bancos Centrais</span></span>
                        <span class="impact-badge high"><span class="lang-en">High Impact</span><span class="lang-pt" style="display:none;">Impacto Alto</span></span>
                        <span class="news-date">07/09/2026</span>
                    </div>
                    <h2 class="news-title">
                        <span class="lang-en">Yen extends the surge: USD/JPY loses 155 and EUR/JPY prints a 9-month low</span>
                        <span class="lang-pt" style="display:none;">Iene estende o surto: USD/JPY perde 155 e EUR/JPY crava mínima de 9 meses</span>
                    </h2>
                    <p class="news-summary">
                        <span class="lang-en">The yen surge's second wave swept the crosses at the open of the week: USD/JPY fell -0.96% to 154.75 — a third down session and the first close under the 155.00 round —, EUR/JPY dropped -0.96% to 179.85 (a 9-month low, breaking 180.28) and GBP/JPY slid -0.95% to 209.39. The engine is the same since Sep 3: bets on BoJ steps above 25 bp at the Sep 17-18 meeting and a MoF on alert since the July intervention; the yen pairs' sigma20 climbed to 91-123 pips.</span>
                        <span class="lang-pt" style="display:none;">A segunda onda do surto do iene varreu os cruzamentos na abertura da semana: USD/JPY caiu -0,96% para 154,75 — terceiro pregão de queda e primeiro fechamento sob o redondo 155,00 —, EUR/JPY caiu -0,96% para 179,85 (mínima de 9 meses, rompendo 180,28) e GBP/JPY recuou -0,95% para 209,39. O motor segue o mesmo desde 03/09: apostas de alta do BoJ acima de 25 pb na reunião de 17-18/09 e o MoF em alerta desde a intervenção de julho; a σ20 dos pares com iene subiu para 91-123 pips.</span>
                    </p>
                    <div class="news-take">
                        <span class="take-tag"><span class="lang-en">Desk take</span><span class="lang-pt" style="display:none;">Leitura da mesa</span></span>
                        <span class="lang-en">The confirmed breakdown meets the resolution condition Friday's report had set: all three yen pairs turn BEARISH in today's edition — but the higher sigma20 hardens the intervention floor (2.5&sigma;20) to 227-307 pips and no structural anchor pays 1:2. They stay on WAIT until volatility compresses; do not front-run the BoJ/MoF.</span>
                        <span class="lang-pt" style="display:none;">O rompimento confirmado cumpre a condição de resolução que o relatório de sexta estabeleceu: os três pares com iene viram BAIXA na edição de hoje — mas a σ20 mais alta endurece o piso de intervenção (2,5σ20) para 227-307 pips e nenhuma âncora estrutural paga 1:2. Seguem em AGUARDAR até a volatilidade comprimir; não se corre na frente do BoJ/MoF.</span>
                    </div>
                    <div class="news-pairs">
                        <span class="np-label"><span class="lang-en">Watch</span><span class="lang-pt" style="display:none;">Acompanhar</span></span>
                        <a href="usd-jpy.html" class="pair-link-chip">USD/JPY</a>
                        <a href="eur-jpy.html" class="pair-link-chip">EUR/JPY</a>
                        <a href="gbp-jpy.html" class="pair-link-chip">GBP/JPY</a>
                    </div>
                </article>

'''
nh = rep(nh, "                <!-- News 1: US NFP / Fed repricing -->", NEWS_CARD + "                <!-- News 1: US NFP / Fed repricing -->", "news card prepend")
open(NP, "w", encoding="utf-8").write(nh)
print("OK: news.html (dateline, kicker, new card, basis note)")

print(f"\nDONE {TS} — run verify_all.py next.")
