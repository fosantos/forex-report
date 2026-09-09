#!/usr/bin/env python3
"""Daily regeneration for the 09/09/2026 edition — ECB/Frankfurter basis
(the logged-in MT5 terminal still returns no FX data — Python copy_rates_range and the
MCP bridge both fail with 'Terminal: Call failed'; compute_indicators fell back).
Basis: ECB/Frankfurter reference rates, 538 sessions 01/08/2024-09/09/2026 (last close: 09/09/2026).
Session: ECB-eve squeeze — EUR/USD +0.33% to 1.1652, first close back over the SMA200 (1.1631)
after six below -> mixed alignment -> NEUTRAL / WAIT (major-level reclaim needs a confirming
close AND the ECB 10/09 + US CPI ~10/09 24h windows are open; the 07/09 short expired unfired
at the 08/09 close). Yen third wave — USD/JPY -0.67% to 153.27 (64 pips over the 9-month low
152.63), EUR/JPY -0.34% to a second straight 9-month low (178.59), GBP/JPY -0.53% through the
78.6% Fib (209.18); floors 225/238/302 pips -> the three JPY pairs stay on WAIT.
AUD/USD +0.14% to 0.7225: third confirming close over the breakout, fresh 20-day high, 32 pips
under the 9-month high -> BUY pullback retest carried (1:2.27), caveat swapped China->US CPI.
GBP/USD +0.14% to 1.3565 (at the 38.2% Fib): averages drifted (zone 1.3444-1.3467, midpoint
1.3455) and the nearest targets pay 1:1.71 / 1:1.97 — under the 1:2 gate -> ticket REVOKED, WAIT.
Verdicts: AUD/USD BUY pullback; EUR/USD, USD/JPY, GBP/USD, EUR/JPY, GBP/JPY WAIT.
Also prepends 3 wire items (ECB eve / yen third wave / cable ticket off) to news digest + news.html,
and patches verify_all.py to the new stamp/ticker/stale dates.
Aborts on any structural mismatch."""
import re, json, sys
from datetime import datetime, timezone

DOCS = r"C:/Projetos/forex-report/docs"
TS_DATE = "09/09/2026"
now = datetime.now(timezone.utc)
TS = TS_DATE + " " + now.strftime("%H:%M") + " UTC"
OLD_TS = "07/09/2026 20:42 UTC"

BASIS_EN_AMP = "ECB/Frankfurter reference rates · SMA50/200, sigma20 &amp; Donchian computed · 538 daily sessions (01/08/2024–09/09/2026)."
BASIS_PT = "taxas de referência BCE/Frankfurter · SMA50/200, σ20 e Donchian calculados · 538 pregões (01/08/2024 a 09/09/2026)."

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
    "quote": "1.1652", "bias": "NEUTRO", "biasType": "neutral",
    "pt": {
      "fundamental": "O EUR/USD fechou em 1,1652 na sessão de 09/09/2026 (taxa de referência BCE/Frankfurter; o terminal MT5 logado segue sem retornar dados de FX), subindo +0,33% — o primeiro fechamento sobre a SMA200 (1,1631) após seis pregões seguidos abaixo, quebrando a sequência na véspera da decisão: o regime de baixa terminou não numa quebra, mas numa recaptura. Com a SMA50 (1,1519) ainda abaixo da SMA200, o alinhamento volta a ser MISTO — leitura NEUTRA — e o fechamento também superou por pouco a máxima prévia de 10 pregões (1,1645), parando a 5 pips da Fib 50% (1,1657). O gatilho de venda da edição anterior expirou no fechamento de 08/09 sem disparar — a zona 1.1629-1.1657 nunca foi alcançada dentro da validade. Macro: o BCE (2,25%) entrega a decisão em 10/09 e o CPI dos EUA (~10/09) chega junto — as duas janelas de 24h já estão abertas; o NFP forte (+162 mil) segue com DXY ~99,5 e odds de alta do Fed ~60% (FOMC 15-16/09). Indicadores (SMA 50/200, σ20, Donchian e Fibonacci) calculados da série diária BCE/Frankfurter (538 pregões, 01/08/2024 a 09/09/2026).",
      "trend": "Fechamento de volta sobre a SMA200 (1,1631) com a SMA50 (1,1519) ainda abaixo — alinhamento misto: leitura NEUTRA após seis fechamentos de baixa; a Fib 50% (1,1657) e a máxima de 20 pregões (1,1699) são os tetos imediatos.",
      "support": "1.1614 (fechamento de terça), com o redondo 1.1600 e a mínima de 10 pregões (1.1578) abaixo.",
      "resistance": "1.1657 (Fib 50%), com a máxima prévia de 10 pregões (1.1645, superada por 7 pips) e a máxima de 20 pregões (1.1699) acima.",
      "priceAction": "Sem entrada — razão dupla: a recaptura da SMA200 é nível maior e exige segundo fechamento confirmatório para validar qualquer rompimento de alta, e as janelas de 24h do BCE (decisão em 10/09) e do CPI dos EUA (~10/09) bloqueiam novas entradas direcionais pela regra de eventos. Rearmar após os eventos: (a) fechamento confirmatório sobre 1,1657-1,1699 com a SMA50 perseguindo a SMA200 — gatilho de compra; (b) rejeição e fechamento de volta sob 1,1631 — o regime de baixa retorna com a zona 1.1629-1.1657 de volta ao mapa.",
      "recommendation": "AGUARDAR OUTRO GATILHO",
      "trigger": "Nenhum — recaptura de SMA200 é nível maior (exige segundo fechamento confirmatório) e as janelas de 24h do BCE (10/09) e do CPI dos EUA (~10/09) bloqueiam entrada: reavaliar após os eventos.",
      "stop": "N/A (sem operação).",
      "target": "N/A (sem operação).",
      "rr": "N/A", "rrValue": 0,
      "justification": "Seis fechamentos de baixa terminaram do jeito menos esperado — não com uma quebra, mas com o euro fechando de volta sobre a SMA200 na véspera do BCE. A regra, porém, não deixa ambiguidade: SMA50 ainda 112 pips abaixo da SMA200 é alinhamento misto, recaptura de média de 200 pregões é nível maior que pede confirmação, e duas janelas de evento de primeiro nível estão abertas ao mesmo tempo. O curto expirou sem disparar e nada o substitui hoje — o evento decide a direção; o preço, apenas o nível. Fora do mercado até o BCE e o CPI passarem."
    },
    "en": {
      "fundamental": "EUR/USD closed at 1.1652 in the 09/09/2026 session (ECB/Frankfurter reference rate; the logged-in MT5 terminal still returns no FX data), up +0.33% — the first close over the 200-day SMA (1.1631) after six sessions below, breaking the streak on decision eve: the bear regime ended not with a breakdown but with a reclaim. With the 50-day (1.1519) still under the 200-day, the alignment turns back MIXED — a NEUTRAL read — and the close also edged past the prior 10-day high (1.1645), stopping 5 pips under the 50% Fib (1.1657). The previous edition's short trigger expired at the 08/09 close without firing — the 1.1629-1.1657 zone was never reached inside its validity. Macro: the ECB (2.25%) delivers its decision on 10/09 and US CPI (~10/09) lands alongside — both 24h windows are already open; the strong NFP (+162k) still has DXY ~99.5 and September Fed hike odds ~60% (FOMC Sep 15-16). Indicators (SMA 50/200, sigma20, Donchian and Fibonacci) computed from the ECB/Frankfurter daily series (538 sessions, 01/08/2024 to 09/09/2026).",
      "trend": "Close back over the 200-day SMA (1.1631) with the 50-day (1.1519) still below — a mixed alignment: a NEUTRAL read after six bearish closes; the 50% Fib (1.1657) and the 20-day high (1.1699) are the immediate ceilings.",
      "support": "1.1614 (Tuesday's close), with the 1.1600 round and the 10-day low (1.1578) beneath.",
      "resistance": "1.1657 (50% Fib), with the prior 10-day high (1.1645, cleared by 7 pips) and the 20-day high (1.1699) above.",
      "priceAction": "No entry — a double reason: reclaiming the 200-day SMA is a major level and needs a second confirming close to validate any bullish breakout, and the ECB (decision 10/09) and US CPI (~10/09) 24h windows block new directional entries under the event rule. Re-arm after the events: (a) a confirming close over 1.1657-1.1699 with the 50-day chasing the 200-day — a buy trigger; (b) rejection and a close back under 1.1631 — the bear regime returns with the 1.1629-1.1657 zone back on the map.",
      "recommendation": "WAIT FOR ANOTHER TRIGGER",
      "trigger": "None — an SMA200 reclaim is a major level (it demands a second confirming close) and the ECB (10/09) and US CPI (~10/09) 24h windows block entry: reassess after the events.",
      "stop": "N/A (no trade).",
      "target": "N/A (no trade).",
      "rr": "N/A", "rrValue": 0,
      "justification": "Six bearish closes ended the least expected way — not with a breakdown but with the euro closing back over the 200-day SMA on ECB eve. The rule leaves no ambiguity, though: a 50-day still 112 pips under the 200-day is a mixed alignment, a 200-session average reclaimed is a major level asking for confirmation, and two top-tier event windows are open at once. The short expired unfired and nothing replaces it today — the event decides the direction; price, only the level. Out of the market until the ECB and the CPI are behind us."
    }
  },
  "USD/JPY": {
    "quote": "153.27", "bias": "BAIXA", "biasType": "bear",
    "pt": {
      "fundamental": "O USD/JPY fechou em 153,27 na sessão de 09/09/2026 (taxa de referência BCE/Frankfurter; o terminal MT5 logado segue sem retornar dados de FX), caindo -0,67% — quarto pregão de queda seguido e nova mínima de 10/20 pregões, agora a apenas 64 pips da mínima de 9 meses (152,63). A leitura segue BAIXA (rompimento confirmado desde a edição de segunda), mas a geometria segue bloqueada: com σ20 a 90 pips, o piso de intervenção 2,5σ20 vale 225 pips — uma venda em 153,27 exigiria alvo a ~450 pips (148,77), sob a mínima de 9 meses, onde só resta o redondo 150,00. O motor não muda desde 03/09: apostas de alta do BoJ acima de 25 pb na reunião de 17-18/09 e o MoF em alerta desde a intervenção de julho — a 64 pips da mínima de 9 meses, o risco de intervenção é máximo. Indicadores calculados da série diária BCE/Frankfurter (538 pregões, 01/08/2024 a 09/09/2026).",
      "trend": "Fechamento sob a SMA200 (158,38) e sob a SMA50 (160,08), com a SMA50 ainda acima da SMA200 — o rompimento confirmado das mínimas de 10/20 pregões mantém a resolução para baixo: leitura de baixa em queda estendida, a 64 pips da mínima de 9 meses (152,63).",
      "support": "152.63 (mínima de 9 meses), com o redondo 152.50 abaixo — 153.27 é o próprio fechamento, mínima de 10/20 pregões.",
      "resistance": "154.30 (fechamento de terça) / 154.75 (fechamento de segunda), com a Fib 78,6% / redondo (155.04-155.00) e a mínima quebrada de 03/09 (156.01) acima.",
      "priceAction": "Sem entrada — a perseguição continua reprovada: com σ20 = 90 pips, o piso de intervenção (2,5σ20 = 225 pips) exige alvo a ~148,80 e a única âncora no caminho é o redondo 150,00 (terceiro nível). Vender a 64 pips da mínima de 9 meses com o MoF em alerta é entregar o stop ao interveniente. Rearmar: compressão da σ20, base sobre 152,63/152,50 ou retração com estrutura até 155.04-156.01. BoJ 17-18/09 é o árbitro.",
      "recommendation": "AGUARDAR OUTRO GATILHO",
      "trigger": "Nenhum — o piso de intervenção (2,5σ20 = 225 pips) reprova a venda a 64 pips da mínima de 9 meses e a compra não tem estrutura sob as médias. Assistir à reação sobre 152.63 e à compressão da σ20; BoJ 17-18/09 decide o próximo capítulo.",
      "stop": "N/A (sem operação).",
      "target": "N/A (sem operação).",
      "rr": "N/A", "rrValue": 0,
      "justification": "O padrão se repete e a resposta também: quanto mais o iene cai, mais alto sobe o piso de intervenção — σ20 a 90 pips faz o 2,5σ20 valer 225 pips quando a âncora mais próxima abaixo é a própria mínima de 9 meses. A 64 pips de 152,63, cada pip de perseguição é um pip mais perto do MoF — e o relatório não paga esse prêmio. O BoJ em 17-18/09 pode entregar direção; até lá, a estrutura espera."
    },
    "en": {
      "fundamental": "USD/JPY closed at 153.27 in the 09/09/2026 session (ECB/Frankfurter reference rate; the logged-in MT5 terminal still returns no FX data), down -0.67% — a fourth consecutive down session and a fresh 10/20-day low, now just 64 pips above the 9-month low (152.63). The read stays BEAR (confirmed breakdown since Monday's edition), but the geometry stays blocked: with sigma20 at 90 pips the 2.5-sigma20 intervention floor is worth 225 pips — a short from 153.27 would need a target ~450 pips lower (148.77), under the 9-month low, where only the 150.00 round remains. The engine is unchanged since Sep 3: bets on BoJ steps above 25 bp at the Sep 17-18 meeting and a MoF on alert since the July intervention — 64 pips above a 9-month low, intervention risk is maximal. Indicators computed from the ECB/Frankfurter daily series (538 sessions, 01/08/2024 to 09/09/2026).",
      "trend": "Close under the 200-day SMA (158.38) and under the 50-day (160.08), with the 50-day still above the 200-day — the confirmed break of the 10/20-day lows keeps the resolution bearish: a bear read on an extended slide, 64 pips above the 9-month low (152.63).",
      "support": "152.63 (9-month low), with the 152.50 round beneath — 153.27 is the close itself, the 10/20-day low.",
      "resistance": "154.30 (Tuesday's close) / 154.75 (Monday's close), with the 78.6% Fib / round (155.04-155.00) and the broken Sep 3 low (156.01) above.",
      "priceAction": "No entry — the chase stays rejected: with sigma20 = 90 pips, the intervention floor (2.5-sigma20 = 225 pips) demands a target at ~148.80 and the only anchor on the way is the 150.00 round (tier three). Selling 64 pips above the 9-month low with the MoF on alert is handing the stop to the intervenor. Re-arm: sigma20 compression, a base over 152.63/152.50, or a structured pullback to 155.04-156.01. The BoJ Sep 17-18 is the arbiter.",
      "recommendation": "WAIT FOR ANOTHER TRIGGER",
      "trigger": "None — the intervention floor (2.5-sigma20 = 225 pips) rejects a short 64 pips above the 9-month low and a long has no structure under the averages. Watch the reaction at 152.63 and sigma20 compression; the BoJ Sep 17-18 decides the next chapter.",
      "stop": "N/A (no trade).",
      "target": "N/A (no trade).",
      "rr": "N/A", "rrValue": 0,
      "justification": "The pattern repeats and so does the answer: the further the yen falls, the higher the intervention floor rises — sigma20 at 90 pips puts 2.5-sigma20 at 225 pips when the nearest anchor below is the 9-month low itself. At 64 pips above 152.63, every pip of chase is a pip closer to the MoF — and the report does not pay that premium. The BoJ on Sep 17-18 can deliver direction; until then, the structure waits."
    }
  },
  "AUD/USD": {
    "quote": "0.7225", "bias": "ALTA", "biasType": "bull",
    "pt": {
      "fundamental": "O AUD/USD fechou em 0,7225 na sessão de 09/09/2026 (taxa de referência BCE/Frankfurter; o terminal MT5 logado segue sem retornar dados de FX), subindo +0,14% — o terceiro fechamento seguido sobre as máximas rompidas de 10/20 pregões (0,7195) e nova máxima de 20 pregões, a 32 pips do teto de 9 meses (0,7257). O alinhamento segue pleno de alta (SMA50 0,7055 > SMA200 0,6984). O motor é o mesmo: diferencial da RBA (4,35%, próxima reunião 29/09; bancos projetam 4,60% em novembro), CPI australiano a 3,5% e WTI ~US$ 83 — quarto pregão seguido ignorando o dólar forte do NFP (+162 mil). O ticket de reteste segue no livro, agora com a ressalva do CPI dos EUA (~10/09) no lugar da janela da China. Indicadores calculados da série diária BCE/Frankfurter (538 pregões, 01/08/2024 a 09/09/2026).",
      "trend": "Acima das SMA50 (0,7055) e SMA200 (0,6984) — alinhamento de alta pleno; terceiro fechamento sobre as máximas rompidas de 10/20 pregões (0,7195) e nova máxima de 20 pregões (0,7225), com a máxima de 9 meses (0,7257) como teto estrutural imediato.",
      "support": "0.7141 (mínima de 10 pregões), com a Fib 23,6% (0,7100) e a SMA50 (0,7055) abaixo.",
      "resistance": "0.7257 (máxima de 9 meses) — as máximas de 10/20 pregões agora são o próprio preço.",
      "priceAction": "Setup de compra no reteste pós-rompimento: aguardar fechamento diário dentro da zona 0.7141-0.7162 (mínima D10 / redondo 0,7150) seguido de fechamento de alta acima do midpoint (0,7152) — entrada de referência 0.7155, stop 0.7110 (sob a base do rompimento; 45 pips ≥ piso 1,5σ20 de 40 pips), alvo 0.7257 (máxima de 9 meses). O nível rompido (0,7195-0,7204) vira suporte no caminho.",
      "recommendation": "COMPRA (LONG) NA RETRAÇÃO",
      "trigger": "Fechamento diário dentro da zona 0.7141-0.7162 (mínima D10 / redondo 0,7150) seguido de fechamento acima do fechamento anterior e do midpoint 0,7152 — entrada de referência 0.7155. Reavaliar se disparar dentro da janela de 24h do CPI dos EUA (~10/09).",
      "stop": "0.7110 (sob a mínima de 10 pregões 0.7141, base do rompimento; 45 pips ≥ 1,5σ20 de 40 pips) · risco sugerido ≤ 1% por operação.",
      "target": "0.7257 (máxima de 9 meses).",
      "rr": "1:2.27", "rrValue": 57,
      "justification": "Terceiro fechamento confirmatório e o livro não muda uma vírgula: perseguir o topo a 32 pips do teto de 9 meses paga menos de 1:1; comprar o reteste da base (0.7141-0.7162) com stop sob ela paga 1:2.27 (45 pips contra 102) com o diferencial da RBA a favor. O Donchian-10 segue o gatilho validado do sistema (+0,123R/trade no backtest 2000-2026) — a entrada disciplinada é o reteste, não a perseguição. A ressalva migra da China para o CPI dos EUA (~10/09): dentro da janela, reavaliar após o evento. A vantagem continua com quem espera."
    },
    "en": {
      "fundamental": "AUD/USD closed at 0.7225 in the 09/09/2026 session (ECB/Frankfurter reference rate; the logged-in MT5 terminal still returns no FX data), up +0.14% — a third consecutive close over the broken 10/20-day highs (0.7195) and a fresh 20-day high, 32 pips under the 9-month ceiling (0.7257). The alignment stays fully bullish (50-day 0.7055 > 200-day 0.6984). The engine is the same: the RBA differential (4.35%, next meeting Sep 29; banks project 4.60% by November), Australian CPI at 3.5% and WTI ~$83 — a fourth session in a row ignoring the strong-NFP dollar (+162k). The retest ticket stays on the book, with the US CPI (~10/09) caveat replacing the China window. Indicators computed from the ECB/Frankfurter daily series (538 sessions, 01/08/2024 to 09/09/2026).",
      "trend": "Above the 50-day (0.7055) and 200-day (0.6984) SMAs — full bull alignment; third close over the broken 10/20-day highs (0.7195) and a fresh 20-day high (0.7225), with the 9-month high (0.7257) as the immediate structural cap.",
      "support": "0.7141 (10-day low), with the 23.6% Fib (0.7100) and the 50-day SMA (0.7055) beneath.",
      "resistance": "0.7257 (9-month high) — the 10/20-day highs are now the price itself.",
      "priceAction": "Buy-the-post-breakout-retest setup: wait for a daily close inside the 0.7141-0.7162 zone (D10 low / 0.7150 round) followed by a higher close above the midpoint (0.7152) — entry reference 0.7155, stop 0.7110 (under the breakout base; 45 pips >= the 40-pip 1.5-sigma20 floor), target 0.7257 (9-month high). The broken level (0.7195-0.7204) turns into support on the way.",
      "recommendation": "BUY (LONG) ON PULLBACK",
      "trigger": "Daily close inside the 0.7141-0.7162 zone (D10 low / 0.7150 round) followed by a close above the previous close and the 0.7152 midpoint — entry reference 0.7155. Reassess if the trigger fires inside the US CPI (~10/09) 24h window.",
      "stop": "0.7110 (under the 10-day low 0.7141, the breakout base; 45 pips >= the 40-pip 1.5-sigma20 floor) · suggested risk ≤ 1% per trade.",
      "target": "0.7257 (9-month high).",
      "rr": "1:2.27", "rrValue": 57,
      "justification": "A third confirming close and the book does not change a comma: chasing the top 32 pips under the 9-month ceiling pays less than 1:1; buying the retest of the base (0.7141-0.7162) with the stop under it pays 1:2.27 (45 pips against 102) with the RBA differential behind. The Donchian-10 remains the system's validated trigger (+0.123R/trade in the 2000-2026 backtest) — the disciplined entry is the retest, not the chase. The caveat migrates from China to US CPI (~10/09): inside the window, reassess after the event. The edge still belongs to whoever waits."
    }
  },
  "GBP/USD": {
    "quote": "1.3565", "bias": "ALTA", "biasType": "bull",
    "pt": {
      "fundamental": "O GBP/USD fechou em 1,3565 na sessão de 09/09/2026 (taxa de referência BCE/Frankfurter; o terminal MT5 logado segue sem retornar dados de FX), subindo +0,14% e encostando na Fib 38,2% (1,3566) — o alvo do ticket de compra virou o próprio preço. O alinhamento de alta segue pleno (SMA50 1,3467 > SMA200 1,3444; preço acima das duas), mas as médias continuaram deslizando para cima e a zona de compra reprecificada (1.3444-1.3467) comprime o prêmio: do midpoint 1,3455 com stop estrutural em 1.3390 (65 pips ≥ piso 1,5σ20 de 49 pips), os alvos mais próximos pagam 1:1,71 (Fib 38,2%) e 1:1,97 (máxima de 10 pregões 1,3583) — sob o portão de 1:2. O ticket sai do livro até o CPI dos EUA (~10/09) e o BoE (17/09, 3,75%, voto 6-3) reprecificarem o mapa. Indicadores calculados da série diária BCE/Frankfurter (538 pregões, 01/08/2024 a 09/09/2026).",
      "trend": "Preço acima das SMA50 (1,3467) e SMA200 (1,3444) — alinhamento de alta pleno; o fechamento encostou na Fib 38,2% (1,3566), com a máxima de 10 pregões (1,3583) e a de 20 pregões (1,3656) como tetos seguintes.",
      "support": "1.3483 (mínimas de 10/20 pregões), com a confluência SMA200/SMA50 (1.3444-1.3467) e a Fib 61,8% (1.3411) abaixo.",
      "resistance": "1.3566 (Fib 38,2% — no próprio preço), com a máxima de 10 pregões (1.3583) e a de 20 pregões (1.3656) acima.",
      "priceAction": "Sem entrada — o prêmio da retração caiu abaixo do portão: da zona reprecificada (midpoint 1,3455), stop 1.3390 (sob a Fib 61,8% e o redondo) contra alvo na Fib 38,2% (1.3566) paga 1:1,71; esticar até a máxima de 10 pregões (1.3583) paga 1:1,97 — nenhum passa de 1:2. A perda por fechamento da Fib 61,8% (1.3411) invalida a estrutura de alta. Rearmar: compressão da σ20, recuo da zona até os redondos (1.3400-1.3444) ou âncora nova acima de 1.3656. CPI dos EUA (~10/09) e BoE (17/09) arbitram.",
      "recommendation": "AGUARDAR OUTRO GATILHO",
      "trigger": "Nenhum — a zona reprecificada (1.3444-1.3467) deixa os alvos estruturais mais próximos em 1:1,71 / 1:1,97, sob o portão de 1:2; e a janela de 24h do CPI dos EUA (~10/09) estaria aberta de qualquer forma. Reavaliar após o CPI e o BoE (17/09).",
      "stop": "N/A (sem operação).",
      "target": "N/A (sem operação).",
      "rr": "N/A", "rrValue": 0,
      "justification": "O portão de R/R existe exatamente para isto: o alinhamento é de alta, a estrutura é limpa — mas as médias deslizaram para cima, o midpoint subiu para 1,3455 e o alvo da Fib 38,2% agora paga 1:1,71. Forçar a entrada seria trocar a regra pela vontade. O ticket sai do livro sem drama: com o CPI amanhã (~10/09) e o BoE em 17/09, os eventos podem reprecificar zona, stop e alvo de uma vez — ou entregar um recuo até a confluência original. O cable continua o par mais firme contra o dólar; a disciplina é que mudou, não o viés."
    },
    "en": {
      "fundamental": "GBP/USD closed at 1.3565 in the 09/09/2026 session (ECB/Frankfurter reference rate; the logged-in MT5 terminal still returns no FX data), up +0.14% and pressing on the 38.2% Fib (1.3566) — the long ticket's target has become the price itself. The bull alignment stands (50-day 1.3467 > 200-day 1.3444; price above both), but the averages kept drifting up and the re-priced buying zone (1.3444-1.3467) squeezes the premium: from the 1.3455 midpoint with a structural stop at 1.3390 (65 pips >= the 49-pip 1.5-sigma20 floor), the nearest targets pay 1:1.71 (38.2% Fib) and 1:1.97 (10-day high 1.3583) — under the 1:2 gate. The ticket comes off the book until US CPI (~10/09) and the BoE (17/09, 3.75%, 6-3 vote) re-price the map. Indicators computed from the ECB/Frankfurter daily series (538 sessions, 01/08/2024 to 09/09/2026).",
      "trend": "Price above the 50-day (1.3467) and 200-day (1.3444) SMAs — full bull alignment; the close pressed on the 38.2% Fib (1.3566), with the 10-day high (1.3583) and the 20-day high (1.3656) as the next ceilings.",
      "support": "1.3483 (10/20-day lows), with the 200/50-day SMA confluence (1.3444-1.3467) and the 61.8% Fib (1.3411) beneath.",
      "resistance": "1.3566 (38.2% Fib — at the price itself), with the 10-day high (1.3583) and the 20-day high (1.3656) above.",
      "priceAction": "No entry — the pullback premium fell under the gate: from the re-priced zone (midpoint 1.3455), stop 1.3390 (under the 61.8% Fib and the round) against the 38.2% Fib target (1.3566) pays 1:1.71; stretching to the 10-day high (1.3583) pays 1:1.97 — neither clears 1:2. A close below the 61.8% Fib (1.3411) invalidates the bull structure. Re-arm: sigma20 compression, the zone sliding back to the rounds (1.3400-1.3444), or a new anchor above 1.3656. US CPI (~10/09) and the BoE (17/09) arbitrate.",
      "recommendation": "WAIT FOR ANOTHER TRIGGER",
      "trigger": "None — the re-priced zone (1.3444-1.3467) leaves the nearest structural targets at 1:1.71 / 1:1.97, under the 1:2 gate; and the US CPI (~10/09) 24h window would be open regardless. Reassess after the CPI and the BoE (17/09).",
      "stop": "N/A (no trade).",
      "target": "N/A (no trade).",
      "rr": "N/A", "rrValue": 0,
      "justification": "The R/R gate exists for exactly this: the alignment is bullish, the structure is clean — but the averages drifted up, the midpoint rose to 1.3455 and the 38.2% Fib target now pays 1:1.71. Forcing the entry would be trading the will instead of the rule. The ticket comes off without drama: with CPI tomorrow (~10/09) and the BoE on 17/09, the events can re-price zone, stop and target at once — or hand back a pullback to the original confluence. Cable remains the firmest pair against the dollar; what changed is the discipline, not the bias."
    }
  },
  "EUR/JPY": {
    "quote": "178.59", "bias": "BAIXA", "biasType": "bear",
    "pt": {
      "fundamental": "O EUR/JPY fechou em 178,59 na sessão de 09/09/2026 (taxa de referência BCE/Frankfurter; o terminal MT5 logado segue sem retornar dados de FX), caindo -0,34% e cravando a segunda mínima de 9 meses consecutiva (178,59) — o fechamento rompeu o de terça (179,20) e não resta nenhuma âncora da janela de 9 meses abaixo do preço: só os redondos 178,00 / 177,50. A leitura segue BAIXA e a geometria segue bloqueada: σ20 a 95 pips faz o piso de intervenção 2,5σ20 valer 238 pips — uma venda exigiria alvo a ~476 pips (173,83), território sem estrutura. O BCE decide em 10/09 e o BoJ em 17-18/09 — dois hawkish puxando em direções opostas, com o yen levando todas desde 03/09. Indicadores calculados da série diária BCE/Frankfurter (538 pregões, 01/08/2024 a 09/09/2026).",
      "trend": "Fechamento sob a SMA200 (184,18) e sob a SMA50 (184,38), com a SMA50 ainda acima da SMA200 — a sequência de rompimentos (181,20 → 180,28 → 179,20 → 178,59) mantém a resolução para baixo: leitura de baixa em mínimas de 9 meses sucessivas.",
      "support": "178.59 é o próprio fechamento — mínima de 9 meses —; abaixo, apenas os redondos 178.00 / 177.50.",
      "resistance": "179.20 (fechamento de terça) / 179.50 (redondo), com a mínima quebrada de 9 meses (180.28) e as mínimas de 03-04/09 (181.20-181.59) acima.",
      "priceAction": "Sem entrada — a direção segue resolvida para baixo, mas o piso de intervenção (2,5σ20 = 238 pips) reprova a perseguição em mínima de 9 meses sem âncoras à frente; compra sob duas médias é aposta contra o BoJ. Rearmar: compressão da σ20 ou reteste estruturado de 180.28-181.20. BCE 10/09 e BoJ 17-18/09 arbitram.",
      "recommendation": "AGUARDAR OUTRO GATILHO",
      "trigger": "Nenhum — o piso de intervenção (2,5σ20 = 238 pips) e a ausência de âncoras sob a mínima de 9 meses reprovam qualquer setup. Assistir à reação nos redondos 178,00 / 177,50 e à compressão da σ20; BCE (10/09) e BoJ (17-18/09) arbitram.",
      "stop": "N/A (sem operação).",
      "target": "N/A (sem operação).",
      "rr": "N/A", "rrValue": 0,
      "justification": "Segunda mínima de 9 meses em dois dias e o problema continua o mesmo: não há para onde mirar. O piso de intervenção (238 pips) manda procurar âncora a ~476 pips abaixo e a janela de 9 meses acabou — só restam redondos, âncoras de terceiro nível. Entre o BCE de amanhã e o BoJ da semana que vem, o desempate é evento, não preço. Fora do mercado."
    },
    "en": {
      "fundamental": "EUR/JPY closed at 178.59 in the 09/09/2026 session (ECB/Frankfurter reference rate; the logged-in MT5 terminal still returns no FX data), down -0.34% and printing a second consecutive 9-month low (178.59) — the close broke Tuesday's (179.20) and no anchor from the 9-month window remains below price: only the 178.00 / 177.50 rounds. The read stays BEAR and the geometry stays blocked: sigma20 at 95 pips puts the 2.5-sigma20 intervention floor at 238 pips — a short would need a target ~476 pips lower (173.83), territory with no structure. The ECB decides on 10/09 and the BoJ on Sep 17-18 — two hawkish central banks pulling in opposite directions, with the yen winning every session since Sep 3. Indicators computed from the ECB/Frankfurter daily series (538 sessions, 01/08/2024 to 09/09/2026).",
      "trend": "Close under the 200-day SMA (184.18) and under the 50-day (184.38), with the 50-day still above the 200-day — the breakdown sequence (181.20 → 180.28 → 179.20 → 178.59) keeps the resolution bearish: a bear read on successive 9-month lows.",
      "support": "178.59 is the close itself — the 9-month low; beneath it, only the 178.00 / 177.50 rounds.",
      "resistance": "179.20 (Tuesday's close) / 179.50 (round), with the broken 9-month low (180.28) and the Sep 3-4 lows (181.20-181.59) above.",
      "priceAction": "No entry — the direction stays resolved bearish, but the intervention floor (2.5-sigma20 = 238 pips) rejects the chase at a 9-month low with no anchors ahead; a long under two averages is a bet against the BoJ. Re-arm: sigma20 compression or a structured retest of 180.28-181.20. The ECB 10/09 and BoJ Sep 17-18 arbitrate.",
      "recommendation": "WAIT FOR ANOTHER TRIGGER",
      "trigger": "None — the intervention floor (2.5-sigma20 = 238 pips) and the absence of anchors beneath the 9-month low reject any setup. Watch the reaction at the 178.00 / 177.50 rounds and sigma20 compression; the ECB (10/09) and BoJ (17-18/09) arbitrate.",
      "stop": "N/A (no trade).",
      "target": "N/A (no trade).",
      "rr": "N/A", "rrValue": 0,
      "justification": "A second 9-month low in two days and the problem is the same: there is nothing left to aim at. The intervention floor (238 pips) demands an anchor ~476 pips below and the 9-month window has run out — only rounds remain, tier-three anchors. Between tomorrow's ECB and next week's BoJ, the tiebreak is the event, not the price. Out of the market."
    }
  },
  "GBP/JPY": {
    "quote": "207.91", "bias": "BAIXA", "biasType": "bear",
    "pt": {
      "fundamental": "O GBP/JPY fechou em 207,91 na sessão de 09/09/2026 (taxa de referência BCE/Frankfurter; o terminal MT5 logado segue sem retornar dados de FX), caindo -0,53% — o fechamento rompeu por fechamento a Fib 78,6% (209,18) e cravou nova mínima de 10/20 pregões; a mínima de 9 meses reprecificou para 206,47 (a mínima de 205,38 saiu da janela de 9 meses). A leitura segue BAIXA e a geometria segue bloqueada: σ20 a 121 pips faz o piso de intervenção 2,5σ20 valer 302 pips — uma venda exigiria alvo a ~604 pips (201,87), sob a mínima de 9 meses. BoE a 3,75% e BoJ decidem na mesma semana (17-18/09). Indicadores calculados da série diária BCE/Frankfurter (538 pregões, 01/08/2024 a 09/09/2026).",
      "trend": "Fechamento sob a SMA200 (212,91) e sob a SMA50 (215,57), com a SMA50 ainda acima da SMA200 — a sequência de rompimentos (210,57 → 209,39 → 207,91) mantém a resolução para baixo: leitura de baixa com a Fib 78,6% (209,18) recém-rompida virando resistência.",
      "support": "206.47 (mínima de 9 meses, reprecificada), com o redondo 206.00 abaixo.",
      "resistance": "209.18 (Fib 78,6% quebrada) / redondo 209.00, com a mínima quebrada de 03/09 (210.57) e a confluência Fib 50% / SMA200 (212.81-212.91) acima.",
      "priceAction": "Sem entrada — direção resolvida para baixo, geometria bloqueada: com σ20 = 121 pips, o piso de intervenção (2,5σ20 = 302 pips) manda procurar âncora a ~604 pips e ela está sob a mínima de 9 meses; compra não tem estrutura. Rearmar: compressão da σ20 ou reteste estruturado de 209.18-210.57. BoE/BoJ em 17-18/09 arbitram.",
      "recommendation": "AGUARDAR OUTRO GATILHO",
      "trigger": "Nenhum — o piso de intervenção (2,5σ20 = 302 pips) reprova qualquer geometria. Assistir à reação sobre a mínima de 9 meses (206.47) e à compressão da σ20.",
      "stop": "N/A (sem operação).",
      "target": "N/A (sem operação).",
      "rr": "N/A", "rrValue": 0,
      "justification": "A Fib 78,6% cedeu por fechamento e o vazio abaixo só aumentou: com a mínima de 9 meses reprecificada em 206,47, o piso de intervenção (302 pips) exige alvo a ~201,90 — 450 pips além da mínima, onde não há nada além de redondos. Depois da intervenção de julho e do surto de 03/09, a lição não muda: não se paga caro para ficar na frente do MoF. Fora do mercado até a estrutura ou o BoJ entregarem algo."
    },
    "en": {
      "fundamental": "GBP/JPY closed at 207.91 in the 09/09/2026 session (ECB/Frankfurter reference rate; the logged-in MT5 terminal still returns no FX data), down -0.53% — the close broke the 78.6% Fib (209.18) by close and printed a fresh 10/20-day low; the 9-month low re-priced to 206.47 (the old 205.38 low left the window). The read stays BEAR and the geometry stays blocked: sigma20 at 121 pips puts the 2.5-sigma20 intervention floor at 302 pips — a short would need a target ~604 pips lower (201.87), under the 9-month low. The BoE at 3.75% and the BoJ decide in the same week (Sep 17-18). Indicators computed from the ECB/Frankfurter daily series (538 sessions, 01/08/2024 to 09/09/2026).",
      "trend": "Close under the 200-day SMA (212.91) and under the 50-day (215.57), with the 50-day still above the 200-day — the breakdown sequence (210.57 → 209.39 → 207.91) keeps the resolution bearish: a bear read with the freshly broken 78.6% Fib (209.18) turning into resistance.",
      "support": "206.47 (9-month low, re-priced), with the 206.00 round beneath.",
      "resistance": "209.18 (broken 78.6% Fib) / 209.00 round, with the broken Sep 3 low (210.57) and the 50% Fib / 200-day SMA confluence (212.81-212.91) above.",
      "priceAction": "No entry — direction resolved bearish, geometry blocked: with sigma20 = 121 pips, the intervention floor (2.5-sigma20 = 302 pips) demands an anchor ~604 pips away and it sits under the 9-month low; a long has no structure. Re-arm: sigma20 compression or a structured retest of 209.18-210.57. The BoE/BoJ Sep 17-18 week arbitrates.",
      "recommendation": "WAIT FOR ANOTHER TRIGGER",
      "trigger": "None — the intervention floor (2.5-sigma20 = 302 pips) rejects any geometry. Watch the reaction at the 9-month low (206.47) and sigma20 compression.",
      "stop": "N/A (no trade).",
      "target": "N/A (no trade).",
      "rr": "N/A", "rrValue": 0,
      "justification": "The 78.6% Fib gave way by close and the void below only grew: with the 9-month low re-priced at 206.47, the intervention floor (302 pips) demands a target at ~201.90 — 450 pips past the low, where nothing but rounds exist. After the July intervention and the Sep 3 surge, the lesson holds: do not pay up to stand in front of the MoF. Out of the market until the structure — or the BoJ — delivers something."
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
html = rep(html, 'dataBasis: "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 536 daily sessions (01/08/2024–07/09/2026).",',
                 'dataBasis: "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 538 daily sessions (01/08/2024–09/09/2026).",', "basis en")
html = rep(html, 'dataBasis: "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, σ20 e Donchian calculados · 536 pregões (01/08/2024 a 07/09/2026).",',
                 'dataBasis: "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, σ20 e Donchian calculados · 538 pregões (01/08/2024 a 09/09/2026).",', "basis pt")
html = rep(html, 'nextEvent: "ECB Sep 9-10 · FOMC Sep 15-16",', 'nextEvent: "ECB Sep 10 · US CPI ~Sep 10",', "nextEvent en")
html = rep(html, 'nextEvent: "BCE 09-10/09 · FOMC 15-16/09",', 'nextEvent: "BCE 10/09 · CPI EUA ~10/09",', "nextEvent pt")

html, n = re.subn(
    r"        const dailyChanges = \{.*?\n        \};",
    '''        const dailyChanges = {
            "EUR/USD": "+0.33%",
            "USD/JPY": "-0.67%",
            "AUD/USD": "+0.14%",
            "GBP/USD": "+0.14%",
            "EUR/JPY": "-0.34%",
            "GBP/JPY": "-0.53%"
        };''', html, count=1, flags=re.DOTALL)
if n != 1:
    print("FAIL: dailyChanges"); sys.exit(1)

html, n = re.subn(
    r"        const macroDrivers = \{.*?\n        \};",
    '''        const macroDrivers = {
            "EUR/USD": {
                en: ["SMA200 reclaimed", "Mixed alignment", "ECB Sep 10 · US CPI"],
                pt: ["SMA200 recapturada", "Alinhamento misto", "BCE 10/09 · CPI EUA"]
            },
            "USD/JPY": {
                en: ["4th down close", "9-mo low 64p below", "BoJ Sep 17-18"],
                pt: ["4º fech. de queda", "Mín. 9m a 64 pips", "BoJ 17-18/09"]
            },
            "AUD/USD": {
                en: ["3rd close over breakout", "RBA 4.35%", "9-mo high 32p away"],
                pt: ["3º fech. sobre rompimento", "RBA 4,35%", "Máx. 9m a 32 pips"]
            },
            "GBP/USD": {
                en: ["Bull alignment holds", "Premium < 1:2 gate", "US CPI ~Sep 10"],
                pt: ["Alinhamento alta segue", "Prêmio < 1:2", "CPI EUA ~10/09"]
            },
            "EUR/JPY": {
                en: ["2nd 9-month low", "2.5-sigma floor 238p", "ECB/BoJ Sep 10-18"],
                pt: ["2ª mín. de 9 meses", "Piso 2,5σ 238p", "BCE/BoJ 10-18/09"]
            },
            "GBP/JPY": {
                en: ["78.6% Fib broke", "2.5-sigma floor 302p", "BoE/BoJ Sep 17"],
                pt: ["Fib 78,6% rompeu", "Piso 2,5σ 302p", "BoE/BoJ 17/09"]
            }
        };''', html, count=1, flags=re.DOTALL)
if n != 1:
    print("FAIL: macroDrivers"); sys.exit(1)

# ---- news wire digest (newsData): update stamp + prepend the 09/09 items ----
html = rep(html, 'updated: "' + OLD_TS + '",', 'updated: "' + TS + '",', "newsData.updated")

NEWS_ITEMS = '''                {
                    date: "09/09/2026",
                    category: "cb",
                    impact: "high",
                    pairs: ["EUR/USD", "EUR/JPY"],
                    pt: {
                        headline: "Euro recaptura a SMA200 na véspera do BCE: EUR/USD fecha a 1,1652 e o curto sai do livro",
                        summary: "O EUR/USD subiu +0,33% para 1,1652 — o primeiro fechamento sobre a SMA200 (1,1631) após seis pregões seguidos abaixo —, parando a 5 pips da Fib 50% (1,1657) e superando por pouco a máxima prévia de 10 pregões (1,1645). O gatilho de venda da edição anterior (zona 1.1629-1.1657) expirou no fechamento de 08/09 sem disparar; com a SMA50 (1,1519) ainda sob a SMA200, o alinhamento volta a ser misto e a leitura vira NEUTRA na véspera da decisão do BCE (10/09) e do CPI dos EUA (~10/09).",
                        take: "A regra é clara: recaptura de SMA200 é nível maior — exige segundo fechamento confirmatório — e as janelas de 24h do BCE e do CPI bloqueiam novas entradas. EUR/USD em AGUARDAR; o evento decide a direção. No EUR/JPY, o BCE hawkish de amanhã contra o BoJ hawkish da semana que vem."
                    },
                    en: {
                        headline: "Euro reclaims the SMA200 on ECB eve: EUR/USD closes at 1.1652 and the short comes off the book",
                        summary: "EUR/USD rose +0.33% to 1.1652 — the first close over the SMA200 (1.1631) after six sessions below —, stopping 5 pips under the 50% Fib (1.1657) and narrowly clearing the prior 10-day high (1.1645). The previous edition's short trigger (1.1629-1.1657 zone) expired at the 08/09 close unfired; with the 50-day SMA (1.1519) still under the 200-day, the alignment turns back mixed and the read flips NEUTRAL on the eve of the ECB decision (10/09) and US CPI (~10/09).",
                        take: "The rule is clear: an SMA200 reclaim is a major level — it demands a second confirming close — and the ECB and CPI 24h windows block new entries. EUR/USD on WAIT; the event decides the direction. In EUR/JPY, tomorrow's hawkish ECB against next week's hawkish BoJ."
                    }
                },
                {
                    date: "09/09/2026",
                    category: "cb",
                    impact: "high",
                    pairs: ["USD/JPY", "EUR/JPY", "GBP/JPY"],
                    pt: {
                        headline: "Terceira onda do iene: USD/JPY vai a 153,27 e flerta com a mínima de 9 meses (152,63)",
                        summary: "O surto do iene segue sem poupar ninguém: USD/JPY caiu -0,67% para 153,27 — quarto pregão de queda seguido, a 64 pips da mínima de 9 meses (152,63) —, EUR/JPY cravou a segunda mínima de 9 meses consecutiva (178,59, -0,34%) e GBP/JPY rompeu por fechamento a Fib 78,6% (209,18), fechando a 207,91 (-0,53%). O motor não muda desde 03/09: apostas de alta do BoJ acima de 25 pb na reunião de 17-18/09 e o MoF em alerta desde a intervenção de julho; as σ20 seguem a 90-121 pips.",
                        take: "Os pisos de intervenção (2,5σ20) seguem em 225-302 pips e nenhuma âncora estrutural paga 1:2 — os três pares com iene permanecem em AGUARDAR, com o BoJ de 17-18/09 como árbitro. Perseguir a queda a 64 pips da mínima de 9 meses é entregar o stop ao MoF."
                    },
                    en: {
                        headline: "Yen third wave: USD/JPY hits 153.27 and flirts with the 9-month low (152.63)",
                        summary: "The yen surge still spares no one: USD/JPY fell -0.67% to 153.27 — a fourth straight down session, 64 pips above the 9-month low (152.63) —, EUR/JPY printed a second consecutive 9-month low (178.59, -0.34%) and GBP/JPY broke the 78.6% Fib (209.18) by close, ending at 207.91 (-0.53%). The engine is unchanged since Sep 3: bets on BoJ steps above 25 bp at the Sep 17-18 meeting and a MoF on alert since the July intervention; the sigma20s remain at 90-121 pips.",
                        take: "The intervention floors (2.5-sigma20) still run 225-302 pips and no structural anchor pays 1:2 — the three yen pairs stay on WAIT, with the Sep 17-18 BoJ as the arbiter. Chasing the drop 64 pips above the 9-month low is handing the stop to the MoF."
                    }
                },
                {
                    date: "09/09/2026",
                    category: "flow",
                    impact: "med",
                    pairs: ["GBP/USD", "AUD/USD"],
                    pt: {
                        headline: "Cable encosta na Fib 38,2% e o ticket sai do livro: prêmio da retração cai abaixo de 1:2",
                        summary: "O GBP/USD subiu +0,14% para 1,3565 — praticamente sobre a Fib 38,2% (1,3566). Com as médias deslizando para cima (SMA200 1,3444 / SMA50 1,3467), a zona de compra reprecificada (midpoint 1,3455) deixa os alvos estruturais mais próximos pagando 1:1,71 e 1:1,97 — sob o portão de 1:2 da metodologia. O AUD/USD, ao contrário, cravou o terceiro fechamento sobre o rompimento (0,7225, nova máxima de 20 pregões) e o ticket de reteste (0.7141-0.7162, alvo 0.7257) segue no livro, com a ressalva do CPI dos EUA (~10/09) no lugar da janela da China.",
                        take: "O portão de R/R existe para isso: ninguém força entrada — o ticket do cable é retirado até o CPI dos EUA (~10/09) e o BoE (17/09) reprecificarem o mapa. O AUD segue o único setup direcional do dia; se o reteste disparar dentro da janela do CPI, reavaliar após o evento."
                    },
                    en: {
                        headline: "Cable presses on the 38.2% Fib and the ticket comes off: pullback premium falls under 1:2",
                        summary: "GBP/USD rose +0.14% to 1.3565 — practically on the 38.2% Fib (1.3566). With the averages drifting up (SMA200 1.3444 / SMA50 1.3467), the re-priced buying zone (midpoint 1.3455) leaves the nearest structural targets paying 1:1.71 and 1:1.97 — under the methodology's 1:2 gate. AUD/USD, by contrast, printed a third close over the breakout (0.7225, a fresh 20-day high) and the retest ticket (0.7141-0.7162, target 0.7257) stays on the book, with the US CPI (~10/09) caveat replacing the China window.",
                        take: "That is what the R/R gate is for: nobody forces an entry — the cable ticket is withdrawn until US CPI (~10/09) and the BoE (17/09) re-price the map. The AUD remains the day's only directional setup; if the retest fires inside the CPI window, reassess after the event."
                    }
                },
'''
html = rep(html, '            items: [\n                {\n                    date: "07/09/2026"',
            "            items: [\n" + NEWS_ITEMS + "                {\n                    date: \"07/09/2026\"", "newsData item prepend")

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
    h = rep(h, '<span class="ts-date">07·09·26</span>', '<span class="ts-date">09·09·26</span>', f"{tag} ts-date")
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
    "EUR/USD": '<div class="next-event"><span class="ne-tag"><span class="lang-en">Next focus</span><span class="lang-pt" style="display:none;">Próximo foco</span></span> <span class="lang-en">ECB 10/09 · US CPI ~10/09</span><span class="lang-pt" style="display:none;">BCE 10/09 · CPI EUA ~10/09</span></div>',
    "USD/JPY": '<div class="next-event"><span class="ne-tag"><span class="lang-en">Next focus</span><span class="lang-pt" style="display:none;">Próximo foco</span></span> <span class="lang-en">BoJ 17-18/09 · FOMC 15-16/09</span><span class="lang-pt" style="display:none;">BoJ 17-18/09 · FOMC 15-16/09</span></div>',
    "AUD/USD": '<div class="next-event"><span class="ne-tag"><span class="lang-en">Next focus</span><span class="lang-pt" style="display:none;">Próximo foco</span></span> <span class="lang-en">US CPI ~10/09 · RBA 29/09</span><span class="lang-pt" style="display:none;">CPI EUA ~10/09 · RBA 29/09</span></div>',
    "GBP/USD": '<div class="next-event"><span class="ne-tag"><span class="lang-en">Next focus</span><span class="lang-pt" style="display:none;">Próximo foco</span></span> <span class="lang-en">US CPI ~10/09 · BoE 17/09</span><span class="lang-pt" style="display:none;">CPI EUA ~10/09 · BoE 17/09</span></div>',
    "EUR/JPY": '<div class="next-event"><span class="ne-tag"><span class="lang-en">Next focus</span><span class="lang-pt" style="display:none;">Próximo foco</span></span> <span class="lang-en">ECB 10/09 · BoJ 17-18/09</span><span class="lang-pt" style="display:none;">BCE 10/09 · BoJ 17-18/09</span></div>',
    "GBP/JPY": '<div class="next-event"><span class="ne-tag"><span class="lang-en">Next focus</span><span class="lang-pt" style="display:none;">Próximo foco</span></span> <span class="lang-en">BoE 17/09 · BoJ 17-18/09</span><span class="lang-pt" style="display:none;">BoE 17/09 · BoJ 17-18/09</span></div>',
}

FD["EUR/USD"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — close back over the 200-day (1.1631) ends the bear run, but the 50-day still below = mixed alignment; the ECB (10/09) and US CPI (~10/09) decide</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — fechamento de volta sobre a SMA200 (1,1631) encerra a sequência de baixa, mas a SMA50 abaixo deixa o mix; BCE (10/09) e CPI dos EUA (~10/09) decidem</span>',
    "_tier_en": "Moderate", "_tier_pt": "Moderada",
})
FD["USD/JPY"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — fourth down close 153.27, 64 pips over the 9-month low (152.63); the 225-pip intervention floor still blocks the book</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — quarto fechamento de queda em 153,27, a 64 pips da mínima de 9 meses (152,63); o piso de intervenção de 225 pips segue bloqueando o livro</span>',
    "_tier_en": "Moderate", "_tier_pt": "Moderada",
})
FD["AUD/USD"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action buy">BUY</span> — third confirming close over the D10/D20 highs (0.7195), fresh 20-day high; buy the retest 0.7141-0.7162, target 0.7257 (1:2.27)</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action buy">COMPRA</span> — terceiro fechamento confirmatório sobre as máximas D10/D20 (0,7195), nova máxima de 20 pregões; comprar o reteste 0.7141-0.7162, alvo 0.7257 (1:2,27)</span>',
    "_tier_en": "High", "_tier_pt": "Alta",
})
FD["GBP/USD"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — cable presses the 38.2% Fib (1.3566); the re-priced zone pays under 1:2 and the ticket is withdrawn until US CPI (~10/09) and the BoE (17/09)</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — o cable encosta na Fib 38,2% (1,3566); a zona reprecificada paga menos de 1:2 e o ticket sai do livro até o CPI dos EUA (~10/09) e o BoE (17/09)</span>',
    "_tier_en": "Moderate", "_tier_pt": "Moderada",
})
FD["EUR/JPY"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — second straight 9-month low (178.59); the 238-pip intervention floor rejects all geometry</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — segunda mínima de 9 meses seguida (178,59); o piso de intervenção de 238 pips rejeita qualquer geometria</span>',
    "_tier_en": "Moderate", "_tier_pt": "Moderada",
})
FD["GBP/JPY"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — the 78.6% Fib (209.18) broke by close; the 302-pip intervention floor rejects all geometry</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — a Fib 78,6% (209,18) cedeu por fechamento; o piso de intervenção de 302 pips rejeita qualquer geometria</span>',
    "_tier_en": "Moderate", "_tier_pt": "Moderada",
})

# bias flip today: bear -> neutral on EUR/USD (SMA200 reclaimed, SMA50 still below)
BIAS_SWAP = {
    "EUR/USD": ("bear", "neutral", "EUR/USD - BEARISH", "EUR/USD - NEUTRAL", "EUR/USD - BAIXA", "EUR/USD - NEUTRO"),
}

CHIPS = {
    "EUR/USD": [('<span class="macro-chip lang-en">ECB 2.25%</span>', '<span class="macro-chip lang-en">ECB decision 10/09</span>', "en"),
                ('<span class="macro-chip lang-pt" style="display:none;">BCE 2,25%</span>', '<span class="macro-chip lang-pt" style="display:none;">Decisão do BCE 10/09</span>', "pt")],
    "USD/JPY": [],
    "AUD/USD": [],
    "GBP/USD": [],
    "EUR/JPY": [],
    "GBP/JPY": [],
}

# gauge percent computed from support/resistance leading numbers vs quote
GAUGE = {"EUR/USD": ("88", "1.1614", "1.1657"), "USD/JPY": ("38", "152.63", "154.30"),
         "AUD/USD": ("72", "0.7141", "0.7257"), "GBP/USD": ("99", "1.3483", "1.3566"),
         "EUR/JPY": ("0", "178.59", "179.20"), "GBP/JPY": ("53", "206.47", "209.18")}
# conviction score = round(R*3) clamped to [3,10]; 0 for WAIT pairs
TIER = {"EUR/USD": ("0/10", "t-mod", 0), "USD/JPY": ("0/10", "t-mod", 0),
        "AUD/USD": ("7/10", "", 7), "GBP/USD": ("0/10", "t-mod", 0),
        "EUR/JPY": ("0/10", "t-mod", 0), "GBP/JPY": ("0/10", "t-mod", 0)}

# verdict flips today: EUR/USD sell -> wait, GBP/USD buy -> wait
BADGE = {
    "EUR/USD": ('<span class="verdict-badge wait">\n                                    <span class="lang-en">WAIT FOR ANOTHER TRIGGER</span>\n                                    <span class="lang-pt" style="display:none;">AGUARDAR OUTRO GATILHO</span>\n                                </span>',
                [("sell", "wait")]),
    "GBP/USD": ('<span class="verdict-badge wait">\n                                    <span class="lang-en">WAIT FOR ANOTHER TRIGGER</span>\n                                    <span class="lang-pt" style="display:none;">AGUARDAR OUTRO GATILHO</span>\n                                </span>',
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

# Resolve: EUR/USD short (validity expired at the 08/09 close unfired) and
# GBP/USD long (re-priced zone pays under the 1:2 gate) -> both revoked.
resolved = []
for t in led["watching"]:
    if t["pair"] == "EUR/USD":
        t["note"] = "revoked in the 09/09 edition: validity expired at the 08/09 close with the zone never printing (08/09 close 1.1614); the 09/09 close (1.1652, +0.33%) then reclaimed the SMA200 — the six-session bear regime ended and the read flips neutral inside the ECB (10/09) / US CPI (~10/09) windows"
        t["outcome"] = "revoked"; t["exitDate"] = "09/09/2026"; t["entryDate"] = None; t["realizedR"] = None
        resolved.append(t)
    if t["pair"] == "GBP/USD":
        t["note"] = "revoked in the 09/09 edition: with the averages drifted up (SMA200 1.3444 / SMA50 1.3467), the re-priced zone's midpoint (1.3455) leaves the nearest structural targets at 1:1.71 (Fib 38.2% 1.3566) and 1:1.97 (10-day high 1.3583) — under the 1:2 gate; reassess after US CPI (~10/09) and BoE (17/09)"
        t["outcome"] = "revoked"; t["exitDate"] = "09/09/2026"; t["entryDate"] = None; t["realizedR"] = None
        resolved.append(t)
led["watching"] = [t for t in led["watching"] if t["pair"] not in ("EUR/USD", "GBP/USD")]
led["closed"].extend(resolved)
assert len(resolved) == 2, "expected 2 resolutions"

# Carry: AUD/USD long retest — third confirming close, caveat swapped to the US-CPI window.
for t in led["watching"]:
    if t["pair"] == "AUD/USD":
        t["reportDate"] = TS_DATE
        t["triggerRule"] = "daily close inside 0.7141-0.7162 (10-day low + 0.7150 round) followed by a close above the previous close and the 0.7152 midpoint; skip if inside the US CPI (~10/09) 24h window"
        t["note"] = "third confirming close (0.7225 — also a fresh 20-day high) over the broken 0.7195 D10/D20 highs; ticket carried, the China-CPI clause swapped for the US-CPI window; stop 45 pips >= the 40-pip 1.5-sigma20 floor"
assert len([t for t in led["watching"] if t["pair"] == "AUD/USD"]) == 1
assert len(led["watching"]) == 1

with open(LED, "w", encoding="utf-8") as f:
    json.dump(led, f, ensure_ascii=False, indent=2)
print("OK: track-record.json (EUR/USD + GBP/USD revoked, AUD/USD carried)")

# =====================================================================
# 4. news.html — hero dateline + new wire cards + basis note
# =====================================================================
NP = DOCS + "/news.html"
nh = open(NP, encoding="utf-8").read()
nh = rep(nh, '<span class="lang-en">Wire updated: ' + OLD_TS + '</span>', '<span class="lang-en">Wire updated: ' + TS + '</span>', "news hero en")
nh = rep(nh, '<span class="lang-pt" style="display:none;">Telégrafo atualizado em: ' + OLD_TS + '</span>', '<span class="lang-pt" style="display:none;">Telégrafo atualizado em: ' + TS + '</span>', "news hero pt")
nh = rep(nh, "numbers and dates reflect the report's data basis of 07/09/2026", "numbers and dates reflect the report's data basis of 09/09/2026", "news note en")
nh = rep(nh, "refletem a base de dados do relatório de 07/09/2026", "refletem a base de dados do relatório de 09/09/2026", "news note pt")

NEWS_CARDS = '''                <!-- News 0: ECB eve — euro reclaims the SMA200 -->
                <article class="news-card">
                    <div class="news-card-top">
                        <span class="news-cat"><span class="lang-en">Central Banks</span><span class="lang-pt" style="display:none;">Bancos Centrais</span></span>
                        <span class="impact-badge high"><span class="lang-en">High Impact</span><span class="lang-pt" style="display:none;">Impacto Alto</span></span>
                        <span class="news-date">09/09/2026</span>
                    </div>
                    <h2 class="news-title">
                        <span class="lang-en">Euro reclaims the SMA200 on ECB eve: EUR/USD closes at 1.1652 and the short comes off the book</span>
                        <span class="lang-pt" style="display:none;">Euro recaptura a SMA200 na véspera do BCE: EUR/USD fecha a 1,1652 e o curto sai do livro</span>
                    </h2>
                    <p class="news-summary">
                        <span class="lang-en">EUR/USD rose +0.33% to 1.1652 — the first close over the SMA200 (1.1631) after six sessions below —, stopping 5 pips under the 50% Fib (1.1657) and narrowly clearing the prior 10-day high (1.1645). The previous edition's short trigger (1.1629-1.1657 zone) expired at the 08/09 close unfired; with the 50-day SMA (1.1519) still under the 200-day, the alignment turns back mixed and the read flips NEUTRAL on the eve of the ECB decision (10/09) and US CPI (~10/09).</span>
                        <span class="lang-pt" style="display:none;">O EUR/USD subiu +0,33% para 1,1652 — o primeiro fechamento sobre a SMA200 (1,1631) após seis pregões seguidos abaixo —, parando a 5 pips da Fib 50% (1,1657) e superando por pouco a máxima prévia de 10 pregões (1,1645). O gatilho de venda da edição anterior (zona 1.1629-1.1657) expirou no fechamento de 08/09 sem disparar; com a SMA50 (1,1519) ainda sob a SMA200, o alinhamento volta a ser misto e a leitura vira NEUTRA na véspera da decisão do BCE (10/09) e do CPI dos EUA (~10/09).</span>
                    </p>
                    <div class="news-take">
                        <span class="take-tag"><span class="lang-en">Desk take</span><span class="lang-pt" style="display:none;">Leitura da mesa</span></span>
                        <span class="lang-en">The rule is clear: an SMA200 reclaim is a major level — it demands a second confirming close — and the ECB and CPI 24h windows block new entries. EUR/USD on WAIT; the event decides the direction. In EUR/JPY, tomorrow's hawkish ECB against next week's hawkish BoJ.</span>
                        <span class="lang-pt" style="display:none;">A regra é clara: recaptura de SMA200 é nível maior — exige segundo fechamento confirmatório — e as janelas de 24h do BCE e do CPI bloqueiam novas entradas. EUR/USD em AGUARDAR; o evento decide a direção. No EUR/JPY, o BCE hawkish de amanhã contra o BoJ hawkish da semana que vem.</span>
                    </div>
                    <div class="news-pairs">
                        <span class="np-label"><span class="lang-en">Watch</span><span class="lang-pt" style="display:none;">Acompanhar</span></span>
                        <a href="eur-usd.html" class="pair-link-chip">EUR/USD</a>
                        <a href="eur-jpy.html" class="pair-link-chip">EUR/JPY</a>
                    </div>
                </article>

                <!-- News 1: Yen third wave -->
                <article class="news-card">
                    <div class="news-card-top">
                        <span class="news-cat"><span class="lang-en">Central Banks</span><span class="lang-pt" style="display:none;">Bancos Centrais</span></span>
                        <span class="impact-badge high"><span class="lang-en">High Impact</span><span class="lang-pt" style="display:none;">Impacto Alto</span></span>
                        <span class="news-date">09/09/2026</span>
                    </div>
                    <h2 class="news-title">
                        <span class="lang-en">Yen third wave: USD/JPY hits 153.27 and flirts with the 9-month low (152.63)</span>
                        <span class="lang-pt" style="display:none;">Terceira onda do iene: USD/JPY vai a 153,27 e flerta com a mínima de 9 meses (152,63)</span>
                    </h2>
                    <p class="news-summary">
                        <span class="lang-en">The yen surge still spares no one: USD/JPY fell -0.67% to 153.27 — a fourth straight down session, 64 pips above the 9-month low (152.63) —, EUR/JPY printed a second consecutive 9-month low (178.59, -0.34%) and GBP/JPY broke the 78.6% Fib (209.18) by close, ending at 207.91 (-0.53%). The engine is unchanged since Sep 3: bets on BoJ steps above 25 bp at the Sep 17-18 meeting and a MoF on alert since the July intervention; the sigma20s remain at 90-121 pips.</span>
                        <span class="lang-pt" style="display:none;">O surto do iene segue sem poupar ninguém: USD/JPY caiu -0,67% para 153,27 — quarto pregão de queda seguido, a 64 pips da mínima de 9 meses (152,63) —, EUR/JPY cravou a segunda mínima de 9 meses consecutiva (178,59, -0,34%) e GBP/JPY rompeu por fechamento a Fib 78,6% (209,18), fechando a 207,91 (-0,53%). O motor não muda desde 03/09: apostas de alta do BoJ acima de 25 pb na reunião de 17-18/09 e o MoF em alerta desde a intervenção de julho; as σ20 seguem a 90-121 pips.</span>
                    </p>
                    <div class="news-take">
                        <span class="take-tag"><span class="lang-en">Desk take</span><span class="lang-pt" style="display:none;">Leitura da mesa</span></span>
                        <span class="lang-en">The intervention floors (2.5&sigma;20) still run 225-302 pips and no structural anchor pays 1:2 — the three yen pairs stay on WAIT, with the Sep 17-18 BoJ as the arbiter. Chasing the drop 64 pips above the 9-month low is handing the stop to the MoF.</span>
                        <span class="lang-pt" style="display:none;">Os pisos de intervenção (2,5σ20) seguem em 225-302 pips e nenhuma âncora estrutural paga 1:2 — os três pares com iene permanecem em AGUARDAR, com o BoJ de 17-18/09 como árbitro. Perseguir a queda a 64 pips da mínima de 9 meses é entregar o stop ao MoF.</span>
                    </div>
                    <div class="news-pairs">
                        <span class="np-label"><span class="lang-en">Watch</span><span class="lang-pt" style="display:none;">Acompanhar</span></span>
                        <a href="usd-jpy.html" class="pair-link-chip">USD/JPY</a>
                        <a href="eur-jpy.html" class="pair-link-chip">EUR/JPY</a>
                        <a href="gbp-jpy.html" class="pair-link-chip">GBP/JPY</a>
                    </div>
                </article>

                <!-- News 2: Cable ticket off / AUD carried -->
                <article class="news-card">
                    <div class="news-card-top">
                        <span class="news-cat"><span class="lang-en">Market Flow</span><span class="lang-pt" style="display:none;">Fluxo &amp; Mercado</span></span>
                        <span class="impact-badge med"><span class="lang-en">Medium Impact</span><span class="lang-pt" style="display:none;">Impacto Médio</span></span>
                        <span class="news-date">09/09/2026</span>
                    </div>
                    <h2 class="news-title">
                        <span class="lang-en">Cable presses on the 38.2% Fib and the ticket comes off: pullback premium falls under 1:2</span>
                        <span class="lang-pt" style="display:none;">Cable encosta na Fib 38,2% e o ticket sai do livro: prêmio da retração cai abaixo de 1:2</span>
                    </h2>
                    <p class="news-summary">
                        <span class="lang-en">GBP/USD rose +0.14% to 1.3565 — practically on the 38.2% Fib (1.3566). With the averages drifting up (SMA200 1.3444 / SMA50 1.3467), the re-priced buying zone (midpoint 1.3455) leaves the nearest structural targets paying 1:1.71 and 1:1.97 — under the methodology's 1:2 gate. AUD/USD, by contrast, printed a third close over the breakout (0.7225, a fresh 20-day high) and the retest ticket (0.7141-0.7162, target 0.7257) stays on the book, with the US CPI (~10/09) caveat replacing the China window.</span>
                        <span class="lang-pt" style="display:none;">O GBP/USD subiu +0,14% para 1,3565 — praticamente sobre a Fib 38,2% (1,3566). Com as médias deslizando para cima (SMA200 1,3444 / SMA50 1,3467), a zona de compra reprecificada (midpoint 1,3455) deixa os alvos estruturais mais próximos pagando 1:1,71 e 1:1,97 — sob o portão de 1:2 da metodologia. O AUD/USD, ao contrário, cravou o terceiro fechamento sobre o rompimento (0,7225, nova máxima de 20 pregões) e o ticket de reteste (0.7141-0.7162, alvo 0.7257) segue no livro, com a ressalva do CPI dos EUA (~10/09) no lugar da janela da China.</span>
                    </p>
                    <div class="news-take">
                        <span class="take-tag"><span class="lang-en">Desk take</span><span class="lang-pt" style="display:none;">Leitura da mesa</span></span>
                        <span class="lang-en">That is what the R/R gate is for: nobody forces an entry — the cable ticket is withdrawn until US CPI (~10/09) and the BoE (17/09) re-price the map. The AUD remains the day's only directional setup; if the retest fires inside the CPI window, reassess after the event.</span>
                        <span class="lang-pt" style="display:none;">O portão de R/R existe para isso: ninguém força entrada — o ticket do cable é retirado até o CPI dos EUA (~10/09) e o BoE (17/09) reprecificarem o mapa. O AUD segue o único setup direcional do dia; se o reteste disparar dentro da janela do CPI, reavaliar após o evento.</span>
                    </div>
                    <div class="news-pairs">
                        <span class="np-label"><span class="lang-en">Watch</span><span class="lang-pt" style="display:none;">Acompanhar</span></span>
                        <a href="gbp-usd.html" class="pair-link-chip">GBP/USD</a>
                        <a href="aud-usd.html" class="pair-link-chip">AUD/USD</a>
                    </div>
                </article>

'''
nh = rep(nh, "                <!-- News 0: Yen second wave / breakdown resolves the yen biases -->", NEWS_CARDS + "                <!-- News 0: Yen second wave / breakdown resolves the yen biases -->", "news card prepend")
open(NP, "w", encoding="utf-8").write(nh)
print("OK: news.html (dateline, 3 new cards, basis note)")

# =====================================================================
# 5. patch verify_all.py to the new edition
# =====================================================================
VP = r"C:/Projetos/forex-report/.claude/verify_all.py"
v = open(VP, encoding="utf-8").read()
v = rep(v, 'TODAY_TS = "07/09/2026 20:42 UTC"', 'TODAY_TS = "' + TS + '"', "verify TODAY_TS")
v = rep(v, 'TODAY_DATE = "07/09/2026"  # basis session date (report edition: 07/09/2026)', 'TODAY_DATE = "09/09/2026"  # basis session date (report edition: 09/09/2026)', "verify TODAY_DATE")
v = rep(v, '''TICKER = [("EUR/USD","+0.00%"),("USD/JPY","-0.96%"),("AUD/USD","+0.15%"),
          ("GBP/USD","+0.01%"),("EUR/JPY","-0.96%"),("GBP/JPY","-0.95%")]''',
        '''TICKER = [("EUR/USD","+0.33%"),("USD/JPY","-0.67%"),("AUD/USD","+0.14%"),
          ("GBP/USD","+0.14%"),("EUR/JPY","-0.34%"),("GBP/JPY","-0.53%")]''', "verify TICKER")
v = rep(v, 'for stale in ["02/09/2026", "01/09/2026", "19/08/2026", "18/08/2026", "17/08/2026", "14/08/2026", "13/08/2026", "04/09/2026"]:',
        'for stale in ["02/09/2026", "01/09/2026", "19/08/2026", "18/08/2026", "17/08/2026", "14/08/2026", "13/08/2026", "04/09/2026", "07/09/2026"]:', "verify static stale")
open(VP, "w", encoding="utf-8").write(v)
print("OK: verify_all.py patched to the 09/09/2026 edition")

print(f"\nDONE {TS} — run verify_all.py next.")
