#!/usr/bin/env python3
"""Daily regeneration for the 04/09/2026 edition — back on the ECB/Frankfurter basis
(the logged-in MT5 terminal — XP demo — offers no FX symbols; compute_indicators fell back).
Basis: ECB/Frankfurter reference rates, 535 sessions 01/08/2024-04/09/2026 (last close: 04/09/2026).
Verdicts: EUR/USD SELL pullback 1.1629-1.1657 (1:2.36, re-armed — Fib50 back to 1.1657),
USD/JPY WAIT (yen surge 03/09 broke the averages; 2.5-sigma intervention floor 217 pips blocks all geometry),
AUD/USD BUY pullback 0.7141-0.7162 post-breakout retest (1:2.27; 04/09 close broke the D10/D20 high),
GBP/USD BUY pullback 1.3438-1.3448 (1:2.18; SMA50 reclaimed SMA200),
EUR/JPY WAIT (2.5-sigma floor 228 pips), GBP/JPY WAIT (long ticket REVOKED — zone steamrolled by the yen surge).
Also fixes the doubled 'Data basis:' prefix introduced in the 02/09 edition.
Aborts on any structural mismatch."""
import re, json, sys
from datetime import datetime, timezone

DOCS = r"C:/Projetos/forex-report/docs"
TS_DATE = "04/09/2026"
now = datetime.now(timezone.utc)
TS = TS_DATE + " " + now.strftime("%H:%M") + " UTC"
OLD_TS = "02/09/2026 00:20 UTC"

BASIS_EN_AMP = "ECB/Frankfurter reference rates · SMA50/200, sigma20 &amp; Donchian computed · 535 daily sessions (01/08/2024–04/09/2026)."
BASIS_PT = "taxas de referência BCE/Frankfurter · SMA50/200, σ20 e Donchian calculados · 535 pregões (01/08/2024 a 04/09/2026)."

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
      "fundamental": "O EUR/USD fechou em 1,1622 na sessão de 04/09/2026 (taxa de referência BCE/Frankfurter; a base voltou ao BCE porque o terminal MT5 logado não oferta símbolos de FX), subindo +0,06% — o quarto fechamento seguido sob a SMA200 (1,1630), com a SMA50 (1,1505) também abaixo: regime de baixa intacto. A troca de base reprecifica os âncoras de volta: a Fib 50% da perna de 9 meses (1,1340-1,1974) retorna a 1,1657 (era 1,1698 na base MT5 que revogou o ticket de 01/09) — e a geometria de venda volta a pagar. Macro: NFP de agosto atropelou a expectativa (+162 mil contra +56 mil projetados; desemprego 4,1%, salários +0,3%), dólar firme com DXY ~99,5 e odds de alta do Fed em setembro ~60% (FOMC 15-16/09); o BCE (2,25%) reúne-se em 09-10/09. Indicadores (SMA 50/200, σ20, Donchian e Fibonacci) calculados da série diária BCE/Frankfurter (535 pregões, 01/08/2024 a 04/09/2026).",
      "trend": "Fechamento sob a SMA200 (1,1630) com a SMA50 (1,1505) também abaixo — alinhamento de baixa; o preço pressiona a SMA200 por baixo, com a Fib 50% (1,1657) formando a zona de venda junto dela e as máximas de 10/20 pregões (1,1669/1,1699) acima.",
      "support": "1.1578 (mínima de 10 pregões), com a mínima de 20 pregões (1,1534) e a confluência Fib 78,6% / redondo (1,1476-1,1500) abaixo.",
      "resistance": "1.1630 (SMA200) / 1.1657 (Fib 50%) — a zona de venda —, com as máximas de 10/20 pregões (1,1669/1,1699) acima.",
      "priceAction": "Setup de venda na retração: aguardar fechamento diário dentro da zona 1.1629-1.1657 (SMA200 / Fib 50%) seguido de fechamento de baixa abaixo do fechamento anterior e do midpoint (1,1643) — entrada de referência 1.1640, stop 1.1685 (acima da Fib 50% e da máxima de 10 pregões; 45 pips ≥ piso 1,5σ20 de 42 pips), alvo 1.1534 (mínima de 20 pregões), com 1.1476-1.1500 como extensão. A confluência Fib 61,8% / mínima D10 (1,1578-1,1582) é o degrau intermediário.",
      "recommendation": "VENDA (SHORT) NA RETRAÇÃO",
      "trigger": "Fechamento diário dentro da zona 1.1629-1.1657 (SMA200 / Fib 50%) seguido de fechamento abaixo do fechamento anterior e do midpoint 1.1643 — entrada de referência 1.1640. Válido até o fechamento de 08/09; dentro da janela de 24h do BCE (09-10/09) ou do CPI dos EUA, reavaliar após o evento.",
      "stop": "1.1685 (acima da Fib 50% 1.1657 e da máxima de 10 pregões 1.1669; 45 pips ≥ 1,5σ20 de 42 pips) · risco sugerido ≤ 1% por operação.",
      "target": "1.1534 (mínima de 20 pregões; extensão 1.1476-1.1500, Fib 78,6% / redondo).",
      "rr": "1:2.36", "rrValue": 59,
      "justification": "A regra manda operar a retração contra a zona, não perseguir o preço — e a troca de base devolveu a zona: com a Fib 50% de volta a 1,1657 (o terminal MT5 logado não tem FX, o relatório retorna ao BCE), o stop 1.1685 volta a ficar acima da âncora estrutural e a matemática paga 1:2.36 até a mínima de 20 pregões — exatamente a geometria que a reprecificação MT5 havia destruído. O regime de baixa segue (quatro fechamentos sob a SMA200) e o NFP forte (+162 mil) reforça o vento contrário ao euro rumo ao FOMC. Vender a zona, não o mercado."
    },
    "en": {
      "fundamental": "EUR/USD closed at 1.1622 in the 04/09/2026 session (ECB/Frankfurter reference rate; the basis returned to the ECB because the logged-in MT5 terminal offers no FX symbols), up +0.06% — the fourth consecutive close under the 200-day SMA (1.1630), with the 50-day (1.1505) also below: the bear regime stands. The basis switch re-prices the anchors back: the 50% Fib of the 9-month leg (1.1340-1.1974) returns to 1.1657 (it was 1.1698 on the MT5 basis that revoked the Sep 1 ticket) — and the short geometry pays again. Macro: August NFP steamrolled expectations (+162k vs +56k forecast; unemployment 4.1%, wages +0.3%), the dollar firm with DXY ~99.5 and September Fed hike odds ~60% (FOMC Sep 15-16); the ECB (2.25%) meets Sep 9-10. Indicators (SMA 50/200, sigma20, Donchian and Fibonacci) computed from the ECB/Frankfurter daily series (535 sessions, 01/08/2024 to 04/09/2026).",
      "trend": "Close under the 200-day SMA (1.1630) with the 50-day (1.1505) also below — bearish alignment; price presses the 200-day from beneath, with the 50% Fib (1.1657) forming the selling zone alongside it and the 10/20-day highs (1.1669/1.1699) above.",
      "support": "1.1578 (10-day low), with the 20-day low (1.1534) and the 78.6% Fib / round confluence (1.1476-1.1500) beneath.",
      "resistance": "1.1630 (200-day SMA) / 1.1657 (50% Fib) — the selling zone —, with the 10/20-day highs (1.1669/1.1699) above.",
      "priceAction": "Sell-the-pullback setup: wait for a daily close inside the 1.1629-1.1657 zone (200-day SMA / 50% Fib) followed by a lower close below the previous close and the midpoint (1.1643) — entry reference 1.1640, stop 1.1685 (above the 50% Fib and the 10-day high; 45 pips >= the 42-pip 1.5-sigma20 floor), target 1.1534 (20-day low), with 1.1476-1.1500 as extension. The 61.8% Fib / D10 low confluence (1.1578-1.1582) is the intermediate step.",
      "recommendation": "SELL (SHORT) ON PULLBACK",
      "trigger": "Daily close inside the 1.1629-1.1657 zone (200-day SMA / 50% Fib) followed by a close below the previous close and the 1.1643 midpoint — entry reference 1.1640. Valid through the 08/09 close; inside the ECB (Sep 9-10) or US CPI 24h windows, reassess after the event.",
      "stop": "1.1685 (above the 50% Fib 1.1657 and the 10-day high 1.1669; 45 pips >= the 42-pip 1.5-sigma20 floor) · suggested risk ≤ 1% per trade.",
      "target": "1.1534 (20-day low; extension 1.1476-1.1500, 78.6% Fib / round).",
      "rr": "1:2.36", "rrValue": 59,
      "justification": "The rule says trade the pullback into the zone, not chase price — and the basis switch gave the zone back: with the 50% Fib returned to 1.1657 (the logged-in MT5 terminal has no FX, the report reverts to the ECB), the 1.1685 stop sits above the structural anchor again and the math pays 1:2.36 to the 20-day low — exactly the geometry the MT5 re-pricing had destroyed. The bear regime holds (four closes under the 200-day SMA) and the strong NFP (+162k) reinforces the euro headwind into the FOMC. Sell the zone, not the market."
    }
  },
  "USD/JPY": {
    "quote": "156.25", "bias": "NEUTRO", "biasType": "neutral",
    "pt": {
      "fundamental": "O USD/JPY fechou em 156,25 na sessão de 04/09/2026 (taxa de referência BCE/Frankfurter; a base voltou ao BCE porque o terminal MT5 logado não oferta símbolos de FX), com leve alta de +0,15% — mera pausa depois do terremoto de 03/09: -2,25% num único dia (159,60 → 156,01), o pior tombo desde a intervenção de julho, movido por apostas de alta mais agressiva do BoJ (mercado precifica passos acima de 25 pb na reunião de 17-18/09) e retomada do talk de intervenção — o yen tocou 155,28 no intraday. O fechamento caiu sob a SMA200 (158,42) e sob a SMA50 (160,58): alinhamento MISTO (a SMA50 segue acima da SMA200) — padrão WAIT, e o piso de intervenção 2,5σ20 (σ20 = 87 pips → 217 pips) reprova qualquer geometria disponível. NFP forte (+162 mil) sustenta o dólar, mas o par agora é uma disputa entre Fed hawkish e BoJ hawkish. Indicadores calculados da série diária BCE/Frankfurter (535 pregões, 01/08/2024 a 04/09/2026).",
      "trend": "Fechamento sob a SMA200 (158,42) e sob a SMA50 (160,58), mas com a SMA50 ainda acima da SMA200 — alinhamento misto; a mínima de 10/20 pregões (156,01) é o piso imediato, com a Fib 61,8% (156,94) no caminho de recuperação e a máxima de 9 meses (163,91) distante.",
      "support": "156.01 (mínimas de 10/20 pregões), com a Fib 78,6% (155,04) e o redondo 155,00 abaixo.",
      "resistance": "158.27 (Fib 50%) / 158.42 (SMA200), com a SMA50 (160,58) e a máxima de 9 meses (163,91) acima.",
      "priceAction": "Sem entrada — dois bloqueios. Primeiro, o alinhamento misto exige um rompimento confirmado para resolver (fechamento sob 156,01 resolve para baixo; reconquista de 158,27-158,42 rearma o lado de alta). Segundo, o piso de intervenção: com σ20 = 87 pips, stop mínimo 2,5σ20 = 217 pips — uma venda em 156,00 exigiria alvo ~434 pips abaixo (151,66, sob a mínima de 9 meses 152,63) e uma compra não tem estrutura. Rearmar: compressão da σ20 ou formação de base acima das médias. BoJ 17-18/09 é o árbitro.",
      "recommendation": "AGUARDAR OUTRO GATILHO",
      "trigger": "Nenhum — piso de intervenção (2,5σ20 = 217 pips) reprova toda a geometria disponível e o alinhamento é misto. Assistir ao fechamento sob 156,01 (resolução de baixa) ou à reconquista de 158,27-158,42 (rearma de alta) — e à compressão da σ20.",
      "stop": "N/A (sem operação).",
      "target": "N/A (sem operação).",
      "rr": "N/A", "rrValue": 0,
      "justification": "O surto do yen não é um setup, é um evento: em 24 horas o par perdeu duas médias, a σ20 saltou para 87 pips e o piso de intervenção (217 pips) passou a valer mais do que qualquer âncora no gráfico — venda nenhuma paga 1:2 com alvo estrutural, e compra abaixo das médias é aposta. Regra é regra: depois de um gap estrutural, deixa-se a poeira baixar. O livro rearma quando a volatilidade comprimir ou o preço formar base."
    },
    "en": {
      "fundamental": "USD/JPY closed at 156.25 in the 04/09/2026 session (ECB/Frankfurter reference rate; the basis returned to the ECB because the logged-in MT5 terminal offers no FX symbols), a mild +0.15% — a mere pause after the Sep 3 earthquake: -2.25% in a single day (159.60 → 156.01), the worst tumble since the July intervention, driven by bets on a more aggressive BoJ (markets price steps above 25 bp at the Sep 17-18 meeting) and renewed intervention talk — the yen touched 155.28 intraday. The close fell under the 200-day SMA (158.42) and under the 50-day (160.58): MIXED alignment (the 50-day stays above the 200-day) — a WAIT pattern, and the 2.5-sigma20 intervention floor (sigma20 = 87 pips → 217 pips) rejects every available geometry. The strong NFP (+162k) supports the dollar, but the pair is now a tug-of-war between a hawkish Fed and a hawkish BoJ. Indicators computed from the ECB/Frankfurter daily series (535 sessions, 01/08/2024 to 04/09/2026).",
      "trend": "Close under the 200-day SMA (158.42) and under the 50-day (160.58), but with the 50-day still above the 200-day — mixed alignment; the 10/20-day low (156.01) is the immediate floor, with the 61.8% Fib (156.94) on the recovery path and the 9-month high (163.91) distant.",
      "support": "156.01 (10/20-day lows), with the 78.6% Fib (155.04) and the 155.00 round beneath.",
      "resistance": "158.27 (50% Fib) / 158.42 (200-day SMA), with the 50-day SMA (160.58) and the 9-month high (163.91) above.",
      "priceAction": "No entry — two blockers. First, the mixed alignment demands a confirmed breakout to resolve (a close under 156.01 resolves bearish; reclaiming 158.27-158.42 re-arms the bull side). Second, the intervention floor: with sigma20 = 87 pips, the minimum stop is 2.5-sigma20 = 217 pips — a short from 156.00 would need a target ~434 pips lower (151.66, under the 9-month low 152.63) and a long has no structure. Re-arm: sigma20 compression or a base forming above the averages. The BoJ Sep 17-18 is the arbiter.",
      "recommendation": "WAIT FOR ANOTHER TRIGGER",
      "trigger": "None — the intervention floor (2.5-sigma20 = 217 pips) rejects every available geometry and the alignment is mixed. Watch a close under 156.01 (bearish resolution) or the reclaim of 158.27-158.42 (bull re-arm) — and sigma20 compression.",
      "stop": "N/A (no trade).",
      "target": "N/A (no trade).",
      "rr": "N/A", "rrValue": 0,
      "justification": "The yen surge is not a setup, it is an event: in 24 hours the pair lost two averages, sigma20 jumped to 87 pips and the intervention floor (217 pips) outweighs any anchor on the chart — no short pays 1:2 with a structural target, and a long below the averages is a bet. A rule is a rule: after a structural gap, let the dust settle. The book re-arms when volatility compresses or price builds a base."
    }
  },
  "AUD/USD": {
    "quote": "0.7204", "bias": "ALTA", "biasType": "bull",
    "pt": {
      "fundamental": "O AUD/USD fechou em 0,7204 na sessão de 04/09/2026 (taxa de referência BCE/Frankfurter; a base voltou ao BCE porque o terminal MT5 logado não oferta símbolos de FX), subindo +0,14% e cravando o rompimento mecânico: o fechamento superou a máxima prévia de 10/20 pregões (0,7195) — a zona 0.7000-0.7020 aguardada desde 21/08 nunca foi tocada e o ticket antigo é substituído pelo reteste pós-rompimento. O alinhamento segue pleno de alta (SMA50 0,7036 > SMA200 0,6973). O NFP forte (+162 mil) deu suporte ao dólar, mas o AUD segurou o rompimento — o diferencial da RBA (4,35%, próxima reunião 29/09; bancos projetam 4,60% em novembro) segue atrás do par, com CPI australiano a 3,5% e WTI ~US$ 83. Indicadores calculados da série diária BCE/Frankfurter (535 pregões, 01/08/2024 a 04/09/2026).",
      "trend": "Acima das SMA50 (0,7036) e SMA200 (0,6973) — alinhamento de alta pleno; o fechamento de 04/09 rompeu as máximas de 10/20 pregões (0,7195), que caem à condição de suporte, com a máxima de 9 meses (0,7257) como teto estrutural.",
      "support": "0.7141 (mínima de 10 pregões), com a Fib 23,6% (0,7085) e a SMA50 (0,7036) abaixo.",
      "resistance": "0.7257 (máxima de 9 meses) — as máximas de 10/20 pregões (0,7195) caíram por fechamento.",
      "priceAction": "Setup de compra no reteste pós-rompimento: aguardar fechamento diário dentro da zona 0.7141-0.7162 (mínima D10 / redondo 0,7150) seguido de fechamento de alta acima do midpoint (0,7152) — entrada de referência 0.7155, stop 0.7110 (sob a base do rompimento; 45 pips ≥ piso 1,5σ20 de 40 pips), alvo 0.7257 (máxima de 9 meses). O nível rompido (0,7195-0,7204) vira suporte no caminho.",
      "recommendation": "COMPRA (LONG) NA RETRAÇÃO",
      "trigger": "Fechamento diário dentro da zona 0.7141-0.7162 (mínima D10 / redondo 0,7150) seguido de fechamento acima do fechamento anterior e do midpoint 0,7152 — entrada de referência 0.7155. Reavaliar se disparar dentro da janela de 24h de dados da China (CPI ~09/09).",
      "stop": "0.7110 (sob a mínima de 10 pregões 0.7141, base do rompimento; 45 pips ≥ 1,5σ20 de 40 pips) · risco sugerido ≤ 1% por operação.",
      "target": "0.7257 (máxima de 9 meses).",
      "rr": "1:2.27", "rrValue": 57,
      "justification": "O mercado escolheu o caminho do rompimento em vez da retração profunda — o livro acompanha: o rompimento de Donchian-10 é o gatilho validado do sistema (+0,123R/trade no backtest 2000-2026), mas perseguir o topo a 53 pips do teto de 9 meses pagaria menos de 1:1. A disciplina manda comprar o reteste da base (0.7141-0.7162) com stop sob ela: 45 pips de risco contra 102 até 0,7257 — 1:2.27 com o diferencial da RBA a favor. A vantagem segue sendo de quem espera."
    },
    "en": {
      "fundamental": "AUD/USD closed at 0.7204 in the 04/09/2026 session (ECB/Frankfurter reference rate; the basis returned to the ECB because the logged-in MT5 terminal offers no FX symbols), up +0.14% and printing the mechanical breakout: the close took out the prior 10/20-day high (0.7195) — the 0.7000-0.7020 zone awaited since Aug 21 was never touched and the old ticket is replaced by the post-breakout retest. The alignment stays fully bullish (50-day 0.7036 > 200-day 0.6973). The strong NFP (+162k) supported the dollar, but the AUD held the breakout — the RBA differential (4.35%, next meeting Sep 29; banks project 4.60% in November) stays behind the pair, with Australian CPI at 3.5% and WTI ~$83. Indicators computed from the ECB/Frankfurter daily series (535 sessions, 01/08/2024 to 04/09/2026).",
      "trend": "Above the 50-day (0.7036) and 200-day (0.6973) SMAs — full bull alignment; the Sep 4 close broke the 10/20-day highs (0.7195), which drop to support, with the 9-month high (0.7257) as the structural cap.",
      "support": "0.7141 (10-day low), with the 23.6% Fib (0.7085) and the 50-day SMA (0.7036) beneath.",
      "resistance": "0.7257 (9-month high) — the 10/20-day highs (0.7195) fell by close.",
      "priceAction": "Buy-the-post-breakout-retest setup: wait for a daily close inside the 0.7141-0.7162 zone (D10 low / 0.7150 round) followed by a higher close above the midpoint (0.7152) — entry reference 0.7155, stop 0.7110 (under the breakout base; 45 pips >= the 40-pip 1.5-sigma20 floor), target 0.7257 (9-month high). The broken level (0.7195-0.7204) turns into support on the way.",
      "recommendation": "BUY (LONG) ON PULLBACK",
      "trigger": "Daily close inside the 0.7141-0.7162 zone (D10 low / 0.7150 round) followed by a close above the previous close and the 0.7152 midpoint — entry reference 0.7155. Reassess if the trigger fires inside the China-data 24h window (CPI ~Sep 9).",
      "stop": "0.7110 (under the 10-day low 0.7141, the breakout base; 45 pips >= the 40-pip 1.5-sigma20 floor) · suggested risk ≤ 1% per trade.",
      "target": "0.7257 (9-month high).",
      "rr": "1:2.27", "rrValue": 57,
      "justification": "The market chose the breakout path over the deep pullback — the book follows: the Donchian-10 breakout is the system's validated trigger (+0.123R/trade in the 2000-2026 backtest), but chasing the top 53 pips under the 9-month ceiling would pay less than 1:1. Discipline says buy the retest of the base (0.7141-0.7162) with the stop under it: 45 pips of risk against 102 to 0.7257 — 1:2.27 with the RBA differential behind. The edge still belongs to whoever waits."
    }
  },
  "GBP/USD": {
    "quote": "1.3530", "bias": "ALTA", "biasType": "bull",
    "pt": {
      "fundamental": "O GBP/USD fechou em 1,3530 na sessão de 04/09/2026 (taxa de referência BCE/Frankfurter; a base voltou ao BCE porque o terminal MT5 logado não oferta símbolos de FX), subindo +0,24% e recuperando o redondo 1,3500 — e o alinhamento VIROU: a SMA50 (1,3448) recapturou a SMA200 (1,3438), devolvendo a leitura de alta plena (preço acima das duas médias). O fundamento: o mínimo de 10/20 pregões (1,3483, impresso em 02/09) segurou sobre a zona de confluência e o par reboteou mesmo com NFP forte (+162 mil) — o cable comprou o rumor da recuperação e não vendeu o dado. BoE a 3,75% (voto 6-3; reunião de 17/09), CPI do Reino Unido a 2,9%. Indicadores calculados da série diária BCE/Frankfurter (535 pregões, 01/08/2024 a 04/09/2026).",
      "trend": "Preço acima das SMA50 (1,3448) e SMA200 (1,3438) — cruzamento de alta fresco e raso —; a retração de 02/09 (1,3483) segurou acima da confluência, com a Fib 38,2% (1,3566) como resistência imediata e a máxima de 10 pregões (1,3634) acima.",
      "support": "1.3483 (mínimas de 10/20 pregões), com a confluência SMA50/SMA200 (1.3438-1.3448) e a Fib 61,8% (1.3411) abaixo.",
      "resistance": "1.3566 (Fib 38,2%), com a máxima de 10 pregões (1,3634) e a de 9 meses (1,3817) acima.",
      "priceAction": "Setup de compra na retração: aguardar fechamento diário dentro da confluência 1.3438-1.3448 (SMA200/SMA50) seguido de fechamento de alta acima do midpoint (1,3443) — entrada de referência 1.3445, stop 1.3390 (sob a Fib 61,8% 1.3411 e o redondo 1.3400; 55 pips ≥ piso 1,5σ20 de 52 pips), alvo 1.3565 (Fib 38,2%), com 1.3634 (máxima de 10 pregões) como extensão. A perda por fechamento da Fib 61,8% (1.3411) invalida o setup.",
      "recommendation": "COMPRA (LONG) NA RETRAÇÃO",
      "trigger": "Fechamento diário dentro da confluência 1.3438-1.3448 (SMA200/SMA50) seguido de fechamento acima do fechamento anterior e do midpoint 1.3443 — entrada de referência 1.3445. Reavaliar se disparar dentro da janela de 24h do CPI dos EUA; BoE 17/09 mais adiante.",
      "stop": "1.3390 (sob a Fib 61,8% 1.3411 e o redondo 1.3400; 55 pips ≥ 1,5σ20 de 52 pips) · risco sugerido ≤ 1% por operação.",
      "target": "1.3565 (Fib 38,2%; extensão 1.3634, máxima de 10 pregões).",
      "rr": "1:2.18", "rrValue": 55,
      "justification": "O cruzamento virou e a regra acompanha: SMA50 acima da SMA200 com preço acima das duas é alinhamento de alta — fresco e raso, o que pede entrada na retração, não perseguição. A confluência 1.3438-1.3448 é a âncora máxima da hierarquia (médias), o stop sob a Fib 61,8% cumpre o piso de volatilidade com folga e o alvo na Fib 38,2% paga 1:2.18 sem S/R intermediário no caminho. Quem comprou o mínimo de 02/09 tem a zona como recolocação; quem não comprou, agora tem o mapa."
    },
    "en": {
      "fundamental": "GBP/USD closed at 1.3530 in the 04/09/2026 session (ECB/Frankfurter reference rate; the basis returned to the ECB because the logged-in MT5 terminal offers no FX symbols), up +0.24% and reclaiming the 1.3500 round — and the alignment TURNED: the 50-day SMA (1.3448) reclaimed the 200-day (1.3438), restoring the full bullish read (price above both averages). The substance: the 10/20-day low (1.3483, printed Sep 2) held above the confluence zone and the pair rebounded even on a strong NFP (+162k) — cable bought the recovery story rather than selling the data. BoE at 3.75% (6-3 vote; meeting Sep 17), UK CPI at 2.9%. Indicators computed from the ECB/Frankfurter daily series (535 sessions, 01/08/2024 to 04/09/2026).",
      "trend": "Price above the 50-day (1.3448) and 200-day (1.3438) SMAs — a fresh, shallow bullish cross —; the Sep 2 pullback (1.3483) held above the confluence, with the 38.2% Fib (1.3566) as immediate resistance and the 10-day high (1.3634) above.",
      "support": "1.3483 (10/20-day lows), with the 50/200-day SMA confluence (1.3438-1.3448) and the 61.8% Fib (1.3411) beneath.",
      "resistance": "1.3566 (38.2% Fib), with the 10-day high (1.3634) and the 9-month high (1.3817) above.",
      "priceAction": "Buy-the-pullback setup: wait for a daily close inside the 1.3438-1.3448 confluence (200/50-day SMAs) followed by a higher close above the midpoint (1.3443) — entry reference 1.3445, stop 1.3390 (under the 61.8% Fib 1.3411 and the 1.3400 round; 55 pips >= the 52-pip 1.5-sigma20 floor), target 1.3565 (38.2% Fib), with 1.3634 (10-day high) as extension. A close below the 61.8% Fib (1.3411) invalidates the setup.",
      "recommendation": "BUY (LONG) ON PULLBACK",
      "trigger": "Daily close inside the 1.3438-1.3448 confluence (200/50-day SMAs) followed by a close above the previous close and the 1.3443 midpoint — entry reference 1.3445. Reassess if the trigger fires inside the US CPI 24h window; the BoE Sep 17 meeting is further out.",
      "stop": "1.3390 (under the 61.8% Fib 1.3411 and the 1.3400 round; 55 pips >= the 52-pip 1.5-sigma20 floor) · suggested risk ≤ 1% per trade.",
      "target": "1.3565 (38.2% Fib; extension 1.3634, the 10-day high).",
      "rr": "1:2.18", "rrValue": 55,
      "justification": "The cross turned and the rule follows: 50-day above the 200-day with price above both is bullish alignment — fresh and shallow, which demands buying the pullback, not chasing. The 1.3438-1.3448 confluence is the top of the anchor hierarchy (the averages), the stop under the 61.8% Fib clears the volatility floor with room, and the 38.2% Fib target pays 1:2.18 with no intermediate S/R in the path. Whoever bought the Sep 2 low has the zone as re-entry; whoever did not now has the map."
    }
  },
  "EUR/JPY": {
    "quote": "181.59", "bias": "NEUTRO", "biasType": "neutral",
    "pt": {
      "fundamental": "O EUR/JPY fechou em 181,59 na sessão de 04/09/2026 (taxa de referência BCE/Frankfurter; a base voltou ao BCE porque o terminal MT5 logado não oferta símbolos de FX), com saldo de +0,21% após o tombo de 03/09 (-2,15%, para 181,20) — o surto do yen derrubou o par das médias (SMA200 184,21 / SMA50 184,73) pela primeira vez no ano: alinhamento MISTO, padrão WAIT. O piso de intervenção volta a mandar: σ20 = 91 pips → 2,5σ20 = 228 pips; uma venda na zona 183.13-184.00 (Fib 61,8-50%) exigiria alvo 456 pips abaixo (179,44 — sob a mínima de 9 meses 180,28) e o rompimento para baixo de 181,20 não tem âncora que pague 1:2. O BCE reúne-se em 09-10/09 e o BoJ em 17-18/09 — dois bancos centrais hawkish puxando o par em direções opostas. Indicadores calculados da série diária BCE/Frankfurter (535 pregões, 01/08/2024 a 04/09/2026).",
      "trend": "Fechamento sob a SMA200 (184,21) e sob a SMA50 (184,73), mas com a SMA50 ainda acima da SMA200 — alinhamento misto; a mínima de 10/20 pregões (181,20) é o piso, com a Fib 61,8% (183,13) como primeira resistência e a máxima de 9 meses (187,73) acima.",
      "support": "181.20 (mínimas de 10/20 pregões), com a mínima de 9 meses (180,28) abaixo.",
      "resistance": "183.13 (Fib 61,8%) / 184.00 (Fib 50%), com a SMA200 (184,21), a SMA50 (184,73) e a máxima de 9 meses (187,73) acima.",
      "priceAction": "Sem entrada — o piso de intervenção (2,5σ20 = 228 pips) reprova toda a geometria: a venda na zona Fib 61,8-50% não encontra âncora a 456 pips e a compra não tem estrutura abaixo das médias. Rearmar: fechamento sob 181,20 resolve o mix para baixo (mas o piso segue vetando), reconquista de 184,00-184,21 rearma o lado de alta, ou compressão da σ20. BCE 09-10/09 e BoJ 17-18/09 arbitram.",
      "recommendation": "AGUARDAR OUTRO GATILHO",
      "trigger": "Nenhum — alinhamento misto e piso de intervenção (2,5σ20 = 228 pips) reprovam qualquer setup. Assistir à resolução: fechamento sob 181,20 (baixa) ou reconquista de 184,00-184,21 (alta).",
      "stop": "N/A (sem operação).",
      "target": "N/A (sem operação).",
      "rr": "N/A", "rrValue": 0,
      "justification": "O cross perdeu as duas médias num dia e a σ20 explodiu para 91 pips — o piso de intervenção (228 pips) agora vale mais que qualquer Fibonacci do pregão. Entre um BoJ que ameaça subir acima de 25 pb e um BCE hawkish na semana que vem, o par é campo minado institucional: sem geometria que pague 1:2 protegido, a posição é fora do mercado. O livro volta quando o preço resolver o mix — e a volatilidade deixar."
    },
    "en": {
      "fundamental": "EUR/JPY closed at 181.59 in the 04/09/2026 session (ECB/Frankfurter reference rate; the basis returned to the ECB because the logged-in MT5 terminal offers no FX symbols), up +0.21% after the Sep 3 tumble (-2.15%, to 181.20) — the yen surge knocked the pair off its averages (200-day 184.21 / 50-day 184.73) for the first time this year: MIXED alignment, a WAIT pattern. The intervention floor rules again: sigma20 = 91 pips → 2.5-sigma20 = 228 pips; a short from the 183.13-184.00 zone (61.8-50% Fib) would need a target 456 pips lower (179.44 — under the 9-month low 180.28) and a downside break of 181.20 has no anchor that pays 1:2. The ECB meets Sep 9-10 and the BoJ Sep 17-18 — two hawkish central banks pulling the pair in opposite directions. Indicators computed from the ECB/Frankfurter daily series (535 sessions, 01/08/2024 to 04/09/2026).",
      "trend": "Close under the 200-day SMA (184.21) and under the 50-day (184.73), but with the 50-day still above the 200-day — mixed alignment; the 10/20-day low (181.20) is the floor, with the 61.8% Fib (183.13) as first resistance and the 9-month high (187.73) above.",
      "support": "181.20 (10/20-day lows), with the 9-month low (180.28) beneath.",
      "resistance": "183.13 (61.8% Fib) / 184.00 (50% Fib), with the 200-day SMA (184.21), the 50-day (184.73) and the 9-month high (187.73) above.",
      "priceAction": "No entry — the intervention floor (2.5-sigma20 = 228 pips) rejects all geometry: the short from the 61.8-50% Fib zone finds no anchor 456 pips down and the long has no structure below the averages. Re-arm: a close under 181.20 resolves the mix bearish (the floor still vetoes), reclaiming 184.00-184.21 re-arms the bull side, or sigma20 compression. The ECB Sep 9-10 and BoJ Sep 17-18 arbitrate.",
      "recommendation": "WAIT FOR ANOTHER TRIGGER",
      "trigger": "None — mixed alignment and the intervention floor (2.5-sigma20 = 228 pips) reject any setup. Watch the resolution: a close under 181.20 (bearish) or the reclaim of 184.00-184.21 (bullish).",
      "stop": "N/A (no trade).",
      "target": "N/A (no trade).",
      "rr": "N/A", "rrValue": 0,
      "justification": "The cross lost both averages in a day and sigma20 exploded to 91 pips — the intervention floor (228 pips) now outweighs any session's Fibonacci. Between a BoJ threatening to hike above 25 bp and a hawkish ECB next week, the pair is an institutional minefield: with no geometry paying a protected 1:2, the position is out of the market. The book returns when price resolves the mix — and volatility allows."
    }
  },
  "GBP/JPY": {
    "quote": "211.41", "bias": "NEUTRO", "biasType": "neutral",
    "pt": {
      "fundamental": "O GBP/JPY fechou em 211,41 na sessão de 04/09/2026 (taxa de referência BCE/Frankfurter; a base voltou ao BCE porque o terminal MT5 logado não oferta símbolos de FX), rebatendo +0,40% depois do tombo de 03/09 (-2,29%, para 210,57) — o surto do yen atropelou a zona de compra 215.15-216.00 e o ticket de 02/09 foi REVOGADO sem disparo. O fechamento caiu sob a SMA200 (212,86) e sob a SMA50 (215,93): alinhamento MISTO, e o piso de intervenção sela o livro — σ20 = 121 pips → 2,5σ20 = 302 pips; nenhuma âncora no raio de 604 pips paga 1:2 em qualquer direção. BoE a 3,75% (17/09) e BoJ (17-18/09) na mesma semana. Indicadores calculados da série diária BCE/Frankfurter (535 pregões, 01/08/2024 a 04/09/2026).",
      "trend": "Fechamento sob a SMA200 (212,86) e sob a SMA50 (215,93), mas com a SMA50 ainda acima da SMA200 — alinhamento misto; a mínima de 10/20 pregões (210,57) é o piso, com a Fib 50% (212,26) e a SMA200 como primeiras resistências.",
      "support": "210.57 (mínimas de 10/20 pregões), com a Fib 78,6% (208,32) e a mínima de 9 meses (205,38) abaixo.",
      "resistance": "212.26 (Fib 50%) / 212.86 (SMA200), com a Fib 38,2% (213,89) e a SMA50 (215,93) acima.",
      "priceAction": "Sem entrada — o ticket de compra foi revogado (a zona 215.15-216.00 ficou 400 pips acima do preço) e o piso de intervenção (2,5σ20 = 302 pips) reprova qualquer geometria nova: venda a partir de 212.26-212.86 não encontra âncora a 604 pips, compra não tem estrutura. Rearmar: fechamento sob 210,57 resolve o mix para baixo (piso segue vetando), reconquista de 212.86-213.89 começa a consertar a estrutura, compressão da σ20 afrouxa o piso. BoE/BoJ em 17/09 arbitram.",
      "recommendation": "AGUARDAR OUTRO GATILHO",
      "trigger": "Nenhum — ticket revogado e piso de intervenção (2,5σ20 = 302 pips) bloqueiam o livro. Assistir ao fechamento sob 210,57 (resolução de baixa) ou à reconquista de 212.86-213.89 (reparo de estrutura).",
      "stop": "N/A (sem operação).",
      "target": "N/A (sem operação).",
      "rr": "N/A", "rrValue": 0,
      "justification": "Era um bom ticket — até o yen decidir mover 2,3% em um dia: a zona de compra foi atropelada sem disparo e o manda-livro manda revogar, não rezar para o preço voltar. Com σ20 a 121 pips, o piso de intervenção (302 pips) transforma qualquer desenho em loteria: sem âncora a 604 pips, não há 1:2 possível. Depois de um evento desses, a melhor posição é nenhuma — o livro rearma com estrutura, não com saudade."
    },
    "en": {
      "fundamental": "GBP/JPY closed at 211.41 in the 04/09/2026 session (ECB/Frankfurter reference rate; the basis returned to the ECB because the logged-in MT5 terminal offers no FX symbols), bouncing +0.40% after the Sep 3 tumble (-2.29%, to 210.57) — the yen surge steamrolled the 215.15-216.00 buying zone and the Sep 2 ticket was REVOKED without triggering. The close fell under the 200-day SMA (212.86) and under the 50-day (215.93): MIXED alignment, and the intervention floor seals the book — sigma20 = 121 pips → 2.5-sigma20 = 302 pips; no anchor within 604 pips pays 1:2 in either direction. BoE at 3.75% (Sep 17) and the BoJ (Sep 17-18) in the same week. Indicators computed from the ECB/Frankfurter daily series (535 sessions, 01/08/2024 to 04/09/2026).",
      "trend": "Close under the 200-day SMA (212.86) and under the 50-day (215.93), but with the 50-day still above the 200-day — mixed alignment; the 10/20-day low (210.57) is the floor, with the 50% Fib (212.26) and the 200-day SMA as first resistances.",
      "support": "210.57 (10/20-day lows), with the 78.6% Fib (208.32) and the 9-month low (205.38) beneath.",
      "resistance": "212.26 (50% Fib) / 212.86 (200-day SMA), with the 38.2% Fib (213.89) and the 50-day SMA (215.93) above.",
      "priceAction": "No entry — the long ticket was revoked (the 215.15-216.00 zone sits 400 pips above price) and the intervention floor (2.5-sigma20 = 302 pips) rejects any new geometry: a short from 212.26-212.86 finds no anchor 604 pips down, a long has no structure. Re-arm: a close under 210.57 resolves the mix bearish (the floor still vetoes), reclaiming 212.86-213.89 starts repairing the structure, sigma20 compression loosens the floor. The BoE/BoJ Sep 17 week arbitrates.",
      "recommendation": "WAIT FOR ANOTHER TRIGGER",
      "trigger": "None — ticket revoked and the intervention floor (2.5-sigma20 = 302 pips) block the book. Watch a close under 210.57 (bearish resolution) or the reclaim of 212.86-213.89 (structure repair).",
      "stop": "N/A (no trade).",
      "target": "N/A (no trade).",
      "rr": "N/A", "rrValue": 0,
      "justification": "It was a good ticket — until the yen decided to move 2.3% in a day: the buying zone was steamrolled without a trigger and the book says revoke, not pray for price to come back. With sigma20 at 121 pips, the intervention floor (302 pips) turns any blueprint into a lottery: with no anchor 604 pips away, no 1:2 exists. After an event like this, the best position is none — the book re-arms with structure, not with longing."
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
        # risk-suffix gate on directional stops
        assert d["pt"]["stop"].endswith("risco sugerido ≤ 1% por operação."), p
        assert d["en"]["stop"].endswith("suggested risk ≤ 1% per trade."), p
    else:
        assert d["pt"]["rrValue"] == 0 and d["en"]["rrValue"] == 0, p
# biasType gate vs computed alignment
ALIGN = {"EUR/USD": "bear", "USD/JPY": "neutral", "AUD/USD": "bull",
         "GBP/USD": "bull", "EUR/JPY": "neutral", "GBP/JPY": "neutral"}
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
# fix the doubled prefix inherited from the 02/09 edition + swap the basis
html = rep(html, 'dataBasis: "Data basis: Data basis: MetaTrader 5 D1 closes · SMA50/200, sigma20 & Donchian computed · 541 daily sessions (01/08/2024–01/09/2026).",',
                 'dataBasis: "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 535 daily sessions (01/08/2024–04/09/2026).",', "basis en")
html = rep(html, 'dataBasis: "Base de dados: Base de dados: fechamentos diários D1 do MetaTrader 5 · SMA50/200, σ20 e Donchian calculados · 541 pregões (01/08/2024 a 01/09/2026).",',
                 'dataBasis: "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, σ20 e Donchian calculados · 535 pregões (01/08/2024 a 04/09/2026).",', "basis pt")
html = rep(html, 'nextEvent: "US NFP — Friday, Sep 4"', 'nextEvent: "ECB Sep 9-10 · FOMC Sep 15-16"', "nextEvent en")
html = rep(html, 'nextEvent: "NFP dos EUA — sexta, 04/09"', 'nextEvent: "BCE 09-10/09 · FOMC 15-16/09"', "nextEvent pt")

html, n = re.subn(
    r"        const dailyChanges = \{.*?\n        \};",
    '''        const dailyChanges = {
            "EUR/USD": "+0.06%",
            "USD/JPY": "+0.15%",
            "AUD/USD": "+0.14%",
            "GBP/USD": "+0.24%",
            "EUR/JPY": "+0.21%",
            "GBP/JPY": "+0.40%"
        };''', html, count=1, flags=re.DOTALL)
if n != 1:
    print("FAIL: dailyChanges"); sys.exit(1)

html, n = re.subn(
    r"        const macroDrivers = \{.*?\n        \};",
    '''        const macroDrivers = {
            "EUR/USD": {
                en: ["NFP +162k, U. 4.1%", "Fed hike ~60%", "ECB Sep 9-10"],
                pt: ["NFP +162 mil, desemp. 4,1%", "Alta Fed ~60%", "BCE 09-10/09"]
            },
            "USD/JPY": {
                en: ["BoJ hike bets surge", "2.5-sigma floor 217p", "FOMC Sep 15-16"],
                pt: ["Apostas de alta no BoJ", "Piso 2,5-sigma 217p", "FOMC 15-16/09"]
            },
            "AUD/USD": {
                en: ["D10/20 breakout close", "RBA 4.35%", "Fed hike ~60%"],
                pt: ["Rompimento D10/D20", "RBA 4,35%", "Alta Fed ~60%"]
            },
            "GBP/USD": {
                en: ["Bull cross 50>200 SMA", "BoE 3.75% 6-3", "Fed hike ~60%"],
                pt: ["Cruzamento de alta 50>200", "BoE 3,75% 6-3", "Alta Fed ~60%"]
            },
            "EUR/JPY": {
                en: ["Yen surge Sep 3", "2.5-sigma floor 228p", "BoJ Sep 17-18"],
                pt: ["Surto do yen 03/09", "Piso 2,5-sigma 228p", "BoJ 17-18/09"]
            },
            "GBP/JPY": {
                en: ["Yen surge Sep 3", "2.5-sigma floor 302p", "BoE/BoJ Sep 17"],
                pt: ["Surto do yen 03/09", "Piso 2,5-sigma 302p", "BoE/BoJ 17/09"]
            }
        };''', html, count=1, flags=re.DOTALL)
if n != 1:
    print("FAIL: macroDrivers"); sys.exit(1)

open(P, "w", encoding="utf-8").write(html)
print(f"OK: index.html (forexData, 3 timestamps, basis fix, nextEvent, ticker, macroDrivers) — stamp {TS}")

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
    h = rep(h, '<span class="ts-date">02·09·26</span>', '<span class="ts-date">04·09·26</span>', f"{tag} ts-date")
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
    "_bluf_en": '<span class="lang-en"><span class="bluf-action sell">SELL</span> — basis back to ECB: Fib50 returns to 1.1657; short the 1.1629-1.1657 zone, target 1.1534 (1:2.36)</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action sell">VENDA</span> — base de volta ao BCE: Fib 50% retorna a 1,1657; vender a zona 1.1629-1.1657, alvo 1.1534 (1:2,36)</span>',
    "_tier_en": "Good", "_tier_pt": "Boa",
})
FD["USD/JPY"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — Sep 3 yen surge (-2.25%) broke both averages; the 217-pip intervention floor blocks all geometry</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — surto do yen de 03/09 (-2,25%) quebrou as duas médias; o piso de intervenção de 217 pips bloqueia tudo</span>',
    "_tier_en": "Moderate", "_tier_pt": "Moderada",
})
FD["AUD/USD"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action buy">BUY</span> — close broke the D10/D20 highs (0.7195); buy the retest 0.7141-0.7162, target 0.7257 (1:2.27)</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action buy">COMPRA</span> — fechamento rompeu as máximas D10/D20 (0,7195); comprar o reteste 0.7141-0.7162, alvo 0.7257 (1:2,27)</span>',
    "_tier_en": "High", "_tier_pt": "Alta",
})
FD["GBP/USD"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action buy">BUY</span> — bull cross: SMA50 reclaimed SMA200; buy the 1.3438-1.3448 confluence, target 1.3565 (1:2.18)</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action buy">COMPRA</span> — cruzamento de alta: SMA50 recapturou a SMA200; comprar a confluência 1.3438-1.3448, alvo 1.3565 (1:2,18)</span>',
    "_tier_en": "Good", "_tier_pt": "Boa",
})
FD["EUR/JPY"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — yen surge knocked the cross off its averages; the 228-pip intervention floor rejects all geometry</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — o surto do yen derrubou o cross das médias; o piso de intervenção de 228 pips rejeita qualquer geometria</span>',
    "_tier_en": "Moderate", "_tier_pt": "Moderada",
})
FD["GBP/JPY"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — ticket revoked: the yen surge steamrolled the 215.15-216.00 zone; 302-pip floor blocks the book</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — ticket revogado: o surto do yen atropelou a zona 215.15-216.00; piso de 302 pips bloqueia o livro</span>',
    "_tier_en": "Moderate", "_tier_pt": "Moderada",
})

CHIPS = {
    "EUR/USD": [('<span class="macro-chip lang-en">Fed Sep hike ~55%</span>', '<span class="macro-chip lang-en">Fed hike ~60%</span>', "1en"),
                ('<span class="macro-chip lang-pt" style="display:none;">Alta Fed set ~55%</span>', '<span class="macro-chip lang-pt" style="display:none;">Alta Fed ~60%</span>', "1pt")],
    "USD/JPY": [('<span class="macro-chip lang-en">¥160 MoF watch</span>', '<span class="macro-chip lang-en">¥ surge · BoJ 17-18</span>', "2en"),
                ('<span class="macro-chip lang-pt" style="display:none;">MoF vigia ¥160</span>', '<span class="macro-chip lang-pt" style="display:none;">Surto do yen · BoJ 17-18</span>', "2pt")],
    "AUD/USD": [('<span class="macro-chip lang-en">Fed hike ~55%</span>', '<span class="macro-chip lang-en">D10/D20 breakout</span>', "3en"),
                ('<span class="macro-chip lang-pt" style="display:none;">Alta Fed ~55%</span>', '<span class="macro-chip lang-pt" style="display:none;">Rompimento D10/D20</span>', "3pt")],
    "GBP/USD": [('<span class="macro-chip lang-en">Fed hike ~55%</span>', '<span class="macro-chip lang-en">Fed hike ~60%</span>', "4en"),
                ('<span class="macro-chip lang-pt" style="display:none;">Alta Fed ~55%</span>', '<span class="macro-chip lang-pt" style="display:none;">Alta Fed ~60%</span>', "4pt")],
    "EUR/JPY": [('<span class="macro-chip lang-en">¥160 MoF watch</span>', '<span class="macro-chip lang-en">¥ surge · BoJ 17-18</span>', "5en"),
                ('<span class="macro-chip lang-pt" style="display:none;">MoF vigia ¥160</span>', '<span class="macro-chip lang-pt" style="display:none;">Surto do yen · BoJ 17-18</span>', "5pt")],
    "GBP/JPY": [('<span class="macro-chip lang-en">¥160 MoF watch</span>', '<span class="macro-chip lang-en">¥ surge · BoJ 17-18</span>', "6en"),
                ('<span class="macro-chip lang-pt" style="display:none;">MoF vigia ¥160</span>', '<span class="macro-chip lang-pt" style="display:none;">Surto do yen · BoJ 17-18</span>', "6pt")],
}

# gauge percent computed from support/resistance leading numbers vs quote
GAUGE = {"EUR/USD": ("85", "1.1578", "1.1630"), "USD/JPY": ("11", "156.01", "158.27"),
         "AUD/USD": ("54", "0.7141", "0.7257"), "GBP/USD": ("57", "1.3483", "1.3566"),
         "EUR/JPY": ("20", "181.20", "183.13"), "GBP/JPY": ("50", "210.57", "212.26")}
TIER = {"EUR/USD": ("7/10", "", 7), "USD/JPY": ("0/10", "t-mod", 0),
        "AUD/USD": ("9/10", "t-high", 8), "GBP/USD": ("7/10", "", 7),
        "EUR/JPY": ("0/10", "t-mod", 0), "GBP/JPY": ("0/10", "t-mod", 0)}

def badge_for(action, en, pt):
    return (f'<span class="verdict-badge {action}">\n'
            f'                                    <span class="lang-en">{en}</span>\n'
            f'                                    <span class="lang-pt" style="display:none;">{pt}</span>\n'
            f'                                </span>')

# pages whose verdict class/labels change today: EUR/USD wait->sell, GBP/USD wait->buy, GBP/JPY buy->wait
BADGE = {
    "EUR/USD": (badge_for("sell", "SELL (SHORT) ON PULLBACK", "VENDA (SHORT) NA RETRAÇÃO"), [("wait", "sell")]),
    "GBP/USD": (badge_for("buy", "BUY (LONG) ON PULLBACK", "COMPRA (LONG) NA RETRAÇÃO"), [("wait", "buy")]),
    "GBP/JPY": (badge_for("wait", "WAIT FOR ANOTHER TRIGGER", "AGUARDAR OUTRO GATILHO"), [("buy", "wait")]),
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
led["meta"]["conventions"]["data"] = "ECB/Frankfurter daily reference rates (MetaTrader 5 D1 closes when the terminal offers FX symbols — it currently does not). All triggers and resolutions are CLOSE-based."
# GBP/JPY 02/09 long ticket -> revoked (moved to closed)
rev = [t for t in led["watching"] if t["pair"] == "GBP/JPY"][0]
rev["outcome"] = "revoked"
rev["exitDate"] = TS_DATE
rev["note"] = "revoked in the 04/09 edition: the 03/09 yen surge (BoJ hike bets + intervention talk) closed 210.57 straight through the 215.15-216.00 zone; on the ECB basis sigma20 = 121 pips puts the 2.5-sigma20 intervention floor at 302 pips — no structural geometry pays 1:2"
led["closed"].append(rev)
led["watching"] = [t for t in led["watching"] if t["pair"] != "GBP/JPY"]
# AUD/USD ticket replaced by the post-breakout retest (the 0.7000-0.7020 zone never traded)
for t in led["watching"]:
    if t["pair"] == "AUD/USD":
        t["reportDate"] = TS_DATE
        t["entry"] = 0.7155; t["stop"] = 0.7110; t["target"] = 0.7257; t["plannedR"] = 2.27
        t["triggerRule"] = "daily close inside 0.7141-0.7162 (10-day low + 0.7150 round) followed by a close above the previous close and the 0.7152 midpoint; skip if inside the China-data 24h window (CPI ~09/09)"
        t["note"] = "the 04/09 close (0.7204) broke the prior 10/20-day high 0.7195 — the stale 0.7000-0.7020 ticket is replaced by the post-breakout retest; stop 45 pips >= the 40-pip 1.5-sigma20 floor"
# new watching tickets: EUR/USD short + GBP/USD long
led["watching"].append({
    "pair": "EUR/USD", "reportDate": TS_DATE, "direction": "short", "setup": "pullback",
    "entry": 1.1640, "stop": 1.1685, "target": 1.1534, "plannedR": 2.36,
    "triggerRule": "daily close inside 1.1629-1.1657 (SMA200 + 50% Fib) followed by a close below the previous close and the 1.1643 midpoint; valid through the 08/09 close — inside the ECB (09-10/09) or US CPI 24h windows, reassess after the event",
    "note": "re-armed on the ECB/Frankfurter basis (Fib50 back to 1.1657; the logged-in MT5 terminal has no FX symbols); stop 1.1685 over the Fib50 and the 10-day high, 45 pips >= the 42-pip 1.5-sigma20 floor"
})
led["watching"].append({
    "pair": "GBP/USD", "reportDate": TS_DATE, "direction": "long", "setup": "pullback",
    "entry": 1.3445, "stop": 1.3390, "target": 1.3565, "plannedR": 2.18,
    "triggerRule": "daily close inside 1.3438-1.3448 (SMA200/SMA50 confluence) followed by a close above the previous close and the 1.3443 midpoint; skip if inside the US CPI 24h window",
    "note": "bull alignment restored (SMA50 1.3448 > SMA200 1.3438); stop 1.3390 under the 61.8% Fib 1.3411 and the 1.3400 round, 55 pips >= the 52-pip 1.5-sigma20 floor"
})
assert len([t for t in led["watching"] if t["pair"] == "EUR/USD"]) == 1
assert len([t for t in led["watching"] if t["pair"] == "AUD/USD"]) == 1
assert len([t for t in led["watching"] if t["pair"] == "GBP/USD"]) == 1
with open(LED, "w", encoding="utf-8") as f:
    json.dump(led, f, ensure_ascii=False, indent=2)
print("OK: track-record.json (GBP/JPY revoked; AUD/USD re-based; EUR/USD + GBP/USD appended)")
print(f"\nDONE {TS} — run verify_all.py next.")
