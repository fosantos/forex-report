#!/usr/bin/env python3
"""Daily regeneration for the 02/09/2026 edition — first report on the MetaTrader 5 basis.
Basis: MT5 D1 closes, 541 sessions 01/08/2024-01/09/2026 (last completed close: 01/09/2026).
Verdicts: EUR/USD WAIT (short ticket REVOKED — Fib50 re-priced 1.1657->1.1698, R/R ~1:1.4),
USD/JPY WAIT (D10 breakout held; arms post-NFP), AUD/USD BUY pullback 0.7000-0.7020 (1:3.08),
GBP/USD WAIT (neutral; new D10 low on the 50% Fib), EUR/JPY WAIT (2.5-sigma20 floor 111 pips),
GBP/JPY BUY pullback 215.15-216.00, stop 213.75, target 219.50 (1:2.11, re-priced).
Aborts on any structural mismatch."""
import re, json, sys
from datetime import datetime

DOCS = r"C:/Projetos/forex-report/docs"
TS_DATE = "02/09/2026"
TS = TS_DATE + " " + datetime.now().strftime("%H:%M") + " UTC"
OLD_TS_EN = "Reports generated on: 01/09/2026 18:04 UTC"
OLD_TS_PT = "Relatórios gerados em: 01/09/2026 18:04 UTC"

BASIS_EN_AMP = "MetaTrader 5 D1 closes · SMA50/200, sigma20 &amp; Donchian computed · 541 daily sessions (01/08/2024–01/09/2026)."
BASIS_EN = BASIS_EN_AMP.replace("&amp;", "&")
BASIS_PT = "fechamentos diários D1 do MetaTrader 5 · SMA50/200, σ20 e Donchian calculados · 541 pregões (01/08/2024 a 01/09/2026)."
OLD_BASIS_EN = "ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 511 daily sessions (01/09/2024–01/09/2026)."
OLD_BASIS_PT = "taxas de referência BCE/Frankfurter · SMA50/200, sigma20 e Donchian calculados · 511 pregões (01/09/2024 a 01/09/2026)."

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
    "quote": "1.1593", "bias": "BAIXA", "biasType": "bear",
    "pt": {
      "fundamental": "O EUR/USD fechou em 1,1593 na sessão de 01/09/2026 (fechamento D1 do MetaTrader 5; mid ao vivo 1,1593), caindo -0,21% e cravando o segundo fechamento sob a SMA200 (1,1631) — o regime de baixa segue (SMA50 1,1494 < SMA200), mas com a migração da base de dados para o terminal MT5 os âncoras foram reprecificados: a Fib 50% da perna de 9 meses (1,1358-1,2038) subiu para 1,1698 (era 1,1657 na série BCE) e a Fib 61,8% para 1,1618. Consequência disciplinada: o ticket de venda do relatório anterior (entrada 1,1620, stop 1,1665, alvo 1,1515) foi REVOGADO — o stop deixou de ficar acima da Fib 50% e o R/R com proteção estrutural cai para ~1:1,4. Macro: ~55% de probabilidade de alta do Fed em setembro, DXY ~99,5; NFP sexta (04/09) arbitra; o BCE reúne-se em 09-10/09. Indicadores (SMA 50/200, σ20, Donchian e Fibonacci) calculados da série D1 do MetaTrader 5 (541 pregões, 01/08/2024 a 01/09/2026).",
      "trend": "Fechamento sob a SMA200 (1,1631) com a SMA50 (1,1494) também abaixo — alinhamento de baixa; a Fib 61,8% (1,1618) e a SMA200 formam a zona de resistência imediata, com a Fib 50% (1,1698) acima e a mínima de 20 pregões (1,1524) abaixo.",
      "support": "1.1583 (mínima de 10 pregões devolvida), com a mínima de 20 pregões (1,1524) e a confluência Fib 78,6% / redondo (1,1504-1,1500) abaixo.",
      "resistance": "1.1618 (Fib 61,8%) / 1.1631 (SMA200), com a Fib 50% (1,1698) e a de 38,2% (1,1779) acima.",
      "priceAction": "Sem entrada — o gate reprova a venda na retração: da zona 1,1618-1,1631, um stop acima da Fib 50% (1,1705+) paga só ~1:1,4 rumo a 1,1524, e um stop de 51 pips (piso 1,5σ20, σ20 = 34 pips) assentaria sob a máxima de 20 pregões (1,1678) sem proteção estrutural. Rearmar: (a) retração estendida à Fib 50% 1,1690-1,1700 com fechamento de rejeição devolvendo 1,1618 — a geometria volta a pagar ≥1:2; (b) fechamento sob 1,1583 abrindo 1,1524/1,1504. NFP sexta (04/09) arbitra o diferencial.",
      "recommendation": "AGUARDAR OUTRO GATILHO",
      "trigger": "Nenhum — R/R reprovado na reprecificação MT5 (Fib 50% a 1,1698). Rearmar em rejeição na Fib 50% (1,1690-1,1700) com fechamento sob 1,1618, ou em fechamento sob a mínima de 10 pregões (1,1583).",
      "stop": "N/A (sem operação).",
      "target": "N/A (sem operação).",
      "rr": "N/A", "rrValue": 0,
      "justification": "Trocar a série de referência não é detalhe: a Fib 50% migrando de 1,1657 para 1,1698 destruiu a proteção do stop do ticket de 01/09 — e o manda-livro diz revogar, não relaxar o gate. O regime de baixa segue de pé (dois fechamentos sob a SMA200, SMA50 sob a SMA200), mas entre a zona 1,1618-1,1631 e o alvo 1,1524 a matemática agora paga ~1:1,4 com stop estrutural. Disciplina: sem 1:2 protegido, sem operação — e o NFP de sexta ainda pode redefinir o campo."
    },
    "en": {
      "fundamental": "EUR/USD closed at 1.1593 in the 01/09/2026 session (MetaTrader 5 D1 close; live mid 1.1593), down -0.21% and printing a second close under the 200-day SMA (1.1631) — the bear regime holds (50-day 1.1494 < 200-day) — but with the data basis migrated to the MT5 terminal the anchors were repriced: the 50% Fib of the 9-month leg (1.1358-1.2038) moved up to 1.1698 (from 1.1657 on the ECB series) and the 61.8% Fib to 1.1618. Disciplined consequence: the previous report's short ticket (entry 1.1620, stop 1.1665, target 1.1515) was REVOKED — the stop no longer sits above the 50% Fib and the structurally-protected R/R drops to ~1:1.4. Macro: ~55% odds of a Fed September hike, DXY ~99.5; Friday's NFP (Sep 4) arbitrates; the ECB Governing Council meets Sep 9-10. Indicators (SMA 50/200, sigma20, Donchian, Fibonacci) computed from the MetaTrader 5 D1 series (541 sessions, 01/08/2024 to 01/09/2026).",
      "trend": "Close under the 200-day SMA (1.1631) with the 50-day (1.1494) also below — bearish alignment; the 61.8% Fib (1.1618) and the 200-day SMA form the immediate resistance zone, with the 50% Fib (1.1698) above and the 20-day low (1.1524) beneath.",
      "support": "1.1583 (10-day low handed back), with the 20-day low (1.1524) and the 78.6% Fib / round confluence (1.1504-1.1500) beneath.",
      "resistance": "1.1618 (61.8% Fib) / 1.1631 (200-day SMA), with the 50% Fib (1.1698) and the 38.2% (1.1779) above.",
      "priceAction": "No entry — the gate rejects the short-on-pullback: from the 1.1618-1.1631 zone, a stop above the 50% Fib (1.1705+) pays only ~1:1.4 toward 1.1524, and a 51-pip stop (the 1.5-sigma20 floor; sigma20 = 34 pips) would sit under the 20-day high (1.1678) without structural protection. Re-arm: (a) an extended pullback to the 50% Fib 1.1690-1.1700 with a rejection close handing back 1.1618 — geometry pays >=1:2 again; (b) a close under 1.1583 opening 1.1524/1.1504. Friday's NFP (Sep 4) arbitrates the differential.",
      "recommendation": "WAIT FOR ANOTHER TRIGGER",
      "trigger": "None — R/R rejected on the MT5 re-pricing (50% Fib at 1.1698). Re-arm on a rejection at the 50% Fib (1.1690-1.1700) with a close under 1.1618, or on a close under the 10-day low (1.1583).",
      "stop": "N/A (no trade).",
      "target": "N/A (no trade).",
      "rr": "N/A", "rrValue": 0,
      "justification": "Switching the reference series is not a detail: the 50% Fib migrating from 1.1657 to 1.1698 destroyed the Sep 1 ticket's stop protection — and the book says revoke, not relax the gate. The bear regime still stands (two closes under the 200-day SMA, 50-day under the 200-day), but between the 1.1618-1.1631 zone and the 1.1524 target the math now pays ~1:1.4 with a structural stop. Discipline: no protected 1:2, no trade — and Friday's NFP can still redefine the field."
    }
  },
  "USD/JPY": {
    "quote": "160.18", "bias": "ALTA", "biasType": "bull",
    "pt": {
      "fundamental": "O USD/JPY fechou em 160,18 na sessão de 01/09/2026 (fechamento D1 do MetaTrader 5; mid ao vivo 160,22), subindo +0,28% e confirmando o rompimento Donchian-10: o fechamento superou a máxima anterior de 10 pregões (160,06) — segunda sessão de força, com os yields dos JGBs de 30 anos em máximas e o dólar firme (~55% de chance de alta do Fed em setembro, DXY ~99,5). O alinhamento segue de alta (SMA50 160,79 > SMA200 158,44) e a Fib 38,2% (159,39) segue reconquistada. A aritmética melhorou na base MT5: uma retração à zona 159,39-159,73 (Fib 38,2% / máxima D10 devolvida) com stop sob a Fib 50%/SMA200 (157,90; 170 pips ≥ piso de intervenção 2,5σ20 = 150 pips) pagaria ~1:2,5 rumo à máxima de 9 meses (163,85) — mas o cluster SMA50/Fib 23,6% (160,79-161,09) paira sobre o preço e o NFP de sexta (04/09) fecha a janela de entrada. Com o yen de volta acima de 160, o MoF reassume o jawboning — o piso de 2,5σ20 segue ativo. Indicadores calculados da série D1 do MetaTrader 5 (541 pregões, 01/08/2024 a 01/09/2026).",
      "trend": "Acima da SMA200 (158,44) e sob a SMA50 (160,79) — alinhamento de alta; rompimento D10 confirmado (160,18 > 160,06), com a confluência SMA50 / Fib 23,6% (160,79-161,09) como teto imediato e a máxima de 9 meses (163,85) acima.",
      "support": "159.39 (Fib 38,2%), com a SMA200 (158,44) e a Fib 50% (158,01) abaixo.",
      "resistance": "160.79 (SMA50) / 161.09 (Fib 23,6%), com o redondo 162,00 e a máxima de 9 meses (163,85) acima.",
      "priceAction": "Sem entrada — o rompimento D10 está impresso e a retração à zona 159,39-159,73 pagaria ~1:2,5 com stop aprovado (157,90), mas o disparo só vale após o NFP de sexta (04/09): fechamentos de quinta (03/09) caem dentro da janela de 24h do evento. Até lá, deixar o rompimento correr sem nós.",
      "recommendation": "AGUARDAR OUTRO GATILHO",
      "trigger": "Nenhum — a zona de retração 159,39-159,73 (Fib 38,2% / D10 devolvida) com stop 157,90 paga ~1:2,5 rumo a 163,85, mas arma somente para fechamentos após o NFP (04/09).",
      "stop": "N/A (sem operação).",
      "target": "N/A (sem operação).",
      "rr": "N/A", "rrValue": 0,
      "justification": "O desenho de alta avançou (rompimento D10, Fib 38,2% reconquistada) e a base MT5 pela primeira vez fecha a aritmética do lado de quem espera a retração — mas dois filtros mandam aguardar: o cluster 160,79-161,09 diretamente acima e o NFP em 48h. Com o yen acima de 160 e o MoF de prontidão, o piso de 2,5σ20 (150 pips) segue ativo. Disciplina: o setup arma depois do evento."
    },
    "en": {
      "fundamental": "USD/JPY closed at 160.18 in the 01/09/2026 session (MetaTrader 5 D1 close; live mid 160.22), up +0.28% and confirming the Donchian-10 breakout: the close took out the prior 10-day high (160.06) — a second session of strength, with 30-year JGB yields at highs and the dollar firm (~55% odds of a Fed September hike, DXY ~99.5). The alignment stays bullish (50-day 160.79 > 200-day 158.44) and the 38.2% Fib (159.39) stays reclaimed. The arithmetic improved on the MT5 basis: a pullback to the 159.39-159.73 zone (38.2% Fib / handed-back D10 high) with a stop under the 50% Fib/SMA200 (157.90; 170 pips >= the 2.5-sigma20 intervention floor = 150 pips) would pay ~1:2.5 toward the 9-month high (163.85) — but the 50-day/23.6% Fib cluster (160.79-161.09) hangs over price and Friday's NFP (Sep 4) closes the entry window. With the yen back above 160, the MoF resumes jawboning — the 2.5-sigma20 floor stays active. Indicators computed from the MetaTrader 5 D1 series (541 sessions, 01/08/2024 to 01/09/2026).",
      "trend": "Above the 200-day SMA (158.44) and under the 50-day (160.79) — bull alignment; D10 breakout confirmed (160.18 > 160.06), with the 50-day / 23.6% Fib confluence (160.79-161.09) as the immediate cap and the 9-month high (163.85) above.",
      "support": "159.39 (38.2% Fib), with the 200-day SMA (158.44) and the 50% Fib (158.01) beneath.",
      "resistance": "160.79 (50-day SMA) / 161.09 (23.6% Fib), with the 162.00 round and the 9-month high (163.85) above.",
      "priceAction": "No entry — the D10 breakout is printed and a pullback to the 159.39-159.73 zone would pay ~1:2.5 with an approved stop (157.90), but the trigger is only valid after Friday's NFP (Sep 4): Thursday (Sep 3) closes fall inside the event's 24h window. Until then, let the breakout run without us.",
      "recommendation": "WAIT FOR ANOTHER TRIGGER",
      "trigger": "None — the pullback zone 159.39-159.73 (38.2% Fib / handed-back D10) with a 157.90 stop pays ~1:2.5 toward 163.85, but arms only for closes after the NFP (Sep 4).",
      "stop": "N/A (no trade).",
      "target": "N/A (no trade).",
      "rr": "N/A", "rrValue": 0,
      "justification": "The bull blueprint advanced (D10 breakout, 38.2% Fib reclaimed) and the MT5 basis closes the arithmetic for the patient for the first time — but two filters say wait: the 160.79-161.09 cluster directly overhead and the NFP inside 48h. With the yen above 160 and the MoF on alert, the 2.5-sigma20 floor (150 pips) stays active. Discipline: the setup arms after the event."
    }
  },
  "AUD/USD": {
    "quote": "0.7145", "bias": "ALTA", "biasType": "bull",
    "pt": {
      "fundamental": "O AUD/USD fechou em 0,7145 na sessão de 01/09/2026 (fechamento D1 do MetaTrader 5; mid ao vivo 0,7147), caindo -0,30% — terceiro dia da retração do topo 0,7194 (máxima de 10/20 pregões), devolvendo o redondo 0,7200 e mirando a zona de compra 0.7000-0.7020 (redondo / SMA50 0,7020), ainda intocada. O alinhamento segue de alta (SMA50 0,7020 > SMA200 0,6973) e o par assenta 125 pips acima da zona. RBA a 4,35% (próxima reunião 29/09; ANZ/CBA veem alta para 4,60% em novembro), CPI australiano a 3,5%; WTI ~US$ 83 e o dólar firme (~55% de chance de alta do Fed) pesam no curto prazo — a retração é o preço de entrada, não a invalidação. NFP sexta (04/09): disparo dentro da janela de 24h, reavaliar após o evento. Indicadores calculados da série D1 do MetaTrader 5 (541 pregões, 01/08/2024 a 01/09/2026).",
      "trend": "Acima das SMA50 (0,7020) e SMA200 (0,6973) — alinhamento de alta; a retração devolveu o redondo 0,7200 e a máxima de 10/20 pregões (0,7194) à condição de resistência, com a máxima de 9 meses (0,7257) acima.",
      "support": "0.7113 (mínima de 10 pregões), com a Fib 23,6% (0,7089) e a zona de compra 0.7000-0.7020 (redondo / SMA50) abaixo.",
      "resistance": "0.7194 (máximas de 10/20 pregões), com o redondo 0,7200 no caminho e a máxima de 9 meses (0,7257) acima.",
      "priceAction": "Setup de compra na retração: aguardar fechamento diário dentro da zona 0.7000-0.7020 (redondo / SMA50) seguido de fechamento de alta acima do midpoint (0,7010) — entrada de referência 0.7010, stop sob a SMA200/redondo (0.6950), alvo 0.7195 (máxima de 20 pregões), com 0.7257 como extensão. A mínima de 10 dias (0,7113) e a Fib 23,6% (0,7089) são os degraus intermediários.",
      "recommendation": "COMPRA (LONG) NA RETRAÇÃO",
      "trigger": "Fechamento diário dentro da zona 0.7000-0.7020 (redondo / SMA50) seguido de fechamento acima do fechamento anterior e do midpoint 0.7010 — entrada de referência 0.7010. Dentro da janela de 24h do NFP (quinta), reavaliar após o evento.",
      "stop": "0.6950 (sob a SMA200 0.6973 e o redondo 0.6950; 60 pips ≥ 1,5σ20 de 35 pips) · risco sugerido ≤ 1% por operação.",
      "target": "0.7195 (máxima de 20 pregões; extensão 0.7257, máxima de 9 meses).",
      "rr": "1:3.08", "rrValue": 77,
      "justification": "A zona intocada segue sendo o gatilho que este relatório espera desde 21/08 — três dias de retração encaminham o preço para ela com o alinhamento de alta intacto e o diferencial da RBA (4,35% e subindo nas projeções dos bancos) atrás do AUD. Comprar o redondo/SMA50 paga 1:3.08 até a máxima de 20 pregões com stop estrutural sob a SMA200; perseguir o topo pagaria ~1:1,4. A vantagem é de quem espera."
    },
    "en": {
      "fundamental": "AUD/USD closed at 0.7145 in the 01/09/2026 session (MetaTrader 5 D1 close; live mid 0.7147), down -0.30% — the third day of the pullback from the 0.7194 top (10/20-day high), handing back the 0.7200 round and aiming at the 0.7000-0.7020 buying zone (round / 50-day SMA at 0.7020), still untouched. The alignment stays bullish (50-day 0.7020 > 200-day 0.6973) and the pair sits 125 pips above the zone. RBA at 4.35% (next meeting Sep 29; ANZ/CBA see a hike to 4.60% in November), Australian CPI at 3.5%; WTI ~$83 and the firm dollar (~55% Fed hike odds) weigh short-term — the pullback is the entry price, not the invalidation. NFP Friday (Sep 4): a trigger inside the 24h window gets reassessed after the event. Indicators computed from the MetaTrader 5 D1 series (541 sessions, 01/08/2024 to 01/09/2026).",
      "trend": "Above the 50-day (0.7020) and 200-day (0.6973) SMAs — bull alignment; the pullback returned the 0.7200 round and the 10/20-day high (0.7194) to resistance, with the 9-month high (0.7257) above.",
      "support": "0.7113 (10-day low), with the 23.6% Fib (0.7089) and the 0.7000-0.7020 buying zone (round / 50-day SMA) beneath.",
      "resistance": "0.7194 (10/20-day highs), with the 0.7200 round in the path and the 9-month high (0.7257) above.",
      "priceAction": "Buy-the-pullback setup: wait for a daily close inside the 0.7000-0.7020 zone (round / 50-day SMA) followed by a higher close above the midpoint (0.7010) — entry reference 0.7010, stop under the SMA200/round (0.6950), target 0.7195 (20-day high), with 0.7257 as extension. The 10-day low (0.7113) and the 23.6% Fib (0.7089) are the intermediate steps.",
      "recommendation": "BUY (LONG) ON PULLBACK",
      "trigger": "Daily close inside the 0.7000-0.7020 zone (round / 50-day SMA) followed by a close above the previous close and the 0.7010 midpoint — entry reference 0.7010. Inside the NFP 24h window (Thursday), reassess after the event.",
      "stop": "0.6950 (under the 200-day SMA 0.6973 and the 0.6950 round; 60 pips >= the 35-pip 1.5-sigma20 floor) · suggested risk ≤ 1% per trade.",
      "target": "0.7195 (20-day high; extension 0.7257, the 9-month high).",
      "rr": "1:3.08", "rrValue": 77,
      "justification": "The untouched zone remains the trigger this report has awaited since Aug 21 — three pullback days steer price toward it with the bull alignment intact and the RBA differential (4.35% and rising in bank projections) behind the AUD. Buying the round/50-day pays 1:3.08 to the 20-day high with a structural stop under the 200-day SMA; chasing the top would pay ~1:1.4. The edge sits with whoever waits."
    }
  },
  "GBP/USD": {
    "quote": "1.3515", "bias": "NEUTRO", "biasType": "neutral",
    "pt": {
      "fundamental": "O GBP/USD fechou em 1,3515 na sessão de 01/09/2026 (fechamento D1 do MetaTrader 5; mid ao vivo 1,3515), caindo -0,25% e imprimindo nova mínima de 10 pregões (1,3515 < 1,3534), colado sobre a Fib 50% (1,3507) da perna de 9 meses. O alinhamento segue NEUTRO: preço acima das duas médias, mas com a SMA50 (1,3435) escorregada sob a SMA200 (1,3438) — o rompimento D10 para baixo não resolve o mix (a leitura de baixa exige fechamento sob a SMA200). BoE a 3,75% (6-3; próxima reunião 17/09), CPI do Reino Unido a 2,9%; o dólar firme (~55% de chance de alta do Fed) pressiona; NFP sexta (04/09). Indicadores calculados da série D1 do MetaTrader 5 (541 pregões, 01/08/2024 a 01/09/2026).",
      "trend": "Preço acima das SMA50 (1,3435) e SMA200 (1,3438), mas com SMA50 sob a SMA200 — alinhamento neutro; mínima de 10 pregões impressa sobre a Fib 50% (1,3507), com a Fib 38,2% (1,3587) acima e a mínima de 20 pregões (1,3454) abaixo.",
      "support": "1.3454 (mínima de 20 pregões), com a confluência SMA50/SMA200 (1,3435-1,3438) e a Fib 61,8% (1,3426) abaixo.",
      "resistance": "1.3587 (Fib 38,2%), com a máxima de 20 pregões (1,3647), a Fib 23,6% (1,3686) e a de 9 meses (1,3846) acima.",
      "priceAction": "Sem gatilho — o mix exige critério de rompimento: (a) fechamento sob a confluência 1,3435-1,3438 / Fib 61,8% (1,3426) abre as extensões 1,3346-1,3260 e reorienta o viés para baixa; (b) reconquista por fechamento acima de 1,3587/1,3647 devolve a leitura de alta. A perda da Fib 50% (1,3507) por fechamento antecipa o caminho (a). Até lá, sem entrada.",
      "recommendation": "AGUARDAR OUTRO GATILHO",
      "trigger": "Nenhum — alinhamento neutro. Assistir à perda da confluência 1,3435-1,3438 (ou da Fib 50% 1,3507, como antecipação) ou à reconquista de 1,3587/1,3647 para definir o próximo setup.",
      "stop": "N/A (sem operação).",
      "target": "N/A (sem operação).",
      "rr": "N/A", "rrValue": 0,
      "justification": "O cruzamento de médias segue invertido (SMA50 sob a SMA200) e a mínima de 10 pregões sobre a Fib 50% é um aviso — mas regra é regra: sem fechamento sob a SMA200 não há leitura de baixa, e sem alinhamento qualquer entrada é aposta, não setup. O campo decide entre a confluência 1,3435-1,3438 e a reconquista de 1,3587; NFP sexta (04/09) e BoE 17/09 são os árbitros macro."
    },
    "en": {
      "fundamental": "GBP/USD closed at 1.3515 in the 01/09/2026 session (MetaTrader 5 D1 close; live mid 1.3515), down -0.25% and printing a new 10-day low (1.3515 < 1.3534), glued onto the 50% Fib (1.3507) of the 9-month leg. The alignment stays NEUTRAL: price above both averages but with the 50-day (1.3435) slipped under the 200-day (1.3438) — the downside D10 print doesn't resolve the mix (a bearish read requires a close under the 200-day SMA). BoE at 3.75% (6-3; next meeting Sep 17), UK CPI at 2.9%; the firm dollar (~55% Fed hike odds) presses; NFP Friday (Sep 4). Indicators computed from the MetaTrader 5 D1 series (541 sessions, 01/08/2024 to 01/09/2026).",
      "trend": "Price above the 50-day (1.3435) and 200-day (1.3438) SMAs, but with the 50-day under the 200-day — neutral alignment; a 10-day low printed on the 50% Fib (1.3507), with the 38.2% Fib (1.3587) above and the 20-day low (1.3454) beneath.",
      "support": "1.3454 (20-day low), with the 50/200-day SMA confluence (1.3435-1.3438) and the 61.8% Fib (1.3426) beneath.",
      "resistance": "1.3587 (38.2% Fib), with the 20-day high (1.3647), the 23.6% Fib (1.3686) and the 9-month high (1.3846) above.",
      "priceAction": "No trigger — the mix demands a breakout criterion: (a) a close under the 1.3435-1.3438 confluence / 61.8% Fib (1.3426) opens the 1.3346-1.3260 extensions and reorients the bias bearish; (b) a reclaim close above 1.3587/1.3647 restores the bullish read. Losing the 50% Fib (1.3507) by close would pre-empt path (a). Until then, no entry.",
      "recommendation": "WAIT FOR ANOTHER TRIGGER",
      "trigger": "None — neutral alignment. Watch the loss of the 1.3435-1.3438 confluence (or of the 50% Fib 1.3507, as an early tell) or the reclaim of 1.3587/1.3647 to define the next setup.",
      "stop": "N/A (no trade).",
      "target": "N/A (no trade).",
      "rr": "N/A", "rrValue": 0,
      "justification": "The moving-average cross stays inverted (50-day under the 200-day) and the 10-day low onto the 50% Fib is a warning — but a rule is a rule: without a close under the 200-day SMA there is no bearish read, and without alignment any entry is a bet, not a setup. The field is decided between the 1.3435-1.3438 confluence and the 1.3587 reclaim; Friday's NFP and the Sep 17 BoE are the macro arbiters."
    }
  },
  "EUR/JPY": {
    "quote": "185.67", "bias": "ALTA", "biasType": "bull",
    "pt": {
      "fundamental": "O EUR/JPY fechou em 185,67 na sessão de 01/09/2026 (fechamento D1 do MetaTrader 5; mid ao vivo 185,74), estável (+0,06%) e colado sob a máxima de 10/20 pregões (185,84). O alinhamento segue pleno de alta (SMA50 184,81 > SMA200 184,26), mas o piso de intervenção voltou a pesar na base MT5: com σ20 a 45 pips, o piso 2,5σ20 é ≈111 pips (o yen de volta acima de 160 mantém o MoF de prontidão) — uma retração à zona 184,67-184,81 (mínima D10 / SMA50) exige stop sob a SMA200/Fib 50% (183,90-184,01, ~75-85 pips) e falha o piso; e o rompimento acima de 185,84 contra o teto de 9 meses (187,54) entrega ~1:1,4 com stop aprovado. O keynote hawkish de Warsh sustenta o diferencial BCE-BoJ (BCE em 09-10/09; BoJ em 17-18/09). Indicadores calculados da série D1 do MetaTrader 5 (541 pregões, 01/08/2024 a 01/09/2026).",
      "trend": "Acima das SMA50 (184,81) e SMA200 (184,26) — alinhamento de alta pleno; fechamento sob a máxima de 10/20 pregões (185,84), com a Fib 23,6% (185,87) e a máxima de 9 meses (187,54) acima.",
      "support": "184.81 (SMA50) / 184.67 (mínima de 10 pregões), com a SMA200 (184,26) e a Fib 50% (184,01) abaixo.",
      "resistance": "185.84 (máximas de 10/20 pregões) / 185.87 (Fib 23,6%), com a máxima de 9 meses (187,54) acima.",
      "priceAction": "Sem entrada — o piso de intervenção (2,5σ20 ≈ 111 pips) reprova o stop estrutural da retração (~75-85 pips) e o rompimento entrega ~1:1,4. Rearmar: retração profunda à zona 183,18-184,01 (Fib 61,8-50%) reprecifica o stop, ou compressão da σ20 que afrouxe o piso. NFP sexta (04/09) e BoJ 17-18/09 no radar.",
      "recommendation": "AGUARDAR OUTRO GATILHO",
      "trigger": "Nenhum — o piso de intervenção reprova o setup de retração e o rompimento entrega ~1:1,4. Reavaliar em retração à zona 183,18-184,01 (Fib 61,8-50%) ou com σ20 comprimida.",
      "stop": "N/A (sem operação).",
      "target": "N/A (sem operação).",
      "rr": "N/A", "rrValue": 0,
      "justification": "A estrutura de alta segue inteira e o preço dança sob o gatilho — mas o gate é o gate: com o yen acima de 160 e o MoF de prontidão, o piso de 2,5σ20 (111 pips) reprova qualquer stop estrutural disponível na zona de retração, e o teto de 187,54 não paga o rompimento. Sem 1:2 protegido, sem operação."
    },
    "en": {
      "fundamental": "EUR/JPY closed at 185.67 in the 01/09/2026 session (MetaTrader 5 D1 close; live mid 185.74), flat (+0.06%) and glued under the 10/20-day high (185.84). The alignment stays fully bullish (50-day 184.81 > 200-day 184.26), but the intervention floor weighs again on the MT5 basis: with sigma20 at 45 pips the 2.5-sigma20 floor is ~=111 pips (the yen back above 160 keeps the MoF on alert) — a pullback to the 184.67-184.81 zone (D10 low / 50-day SMA) requires a stop under the 200-day/50% Fib (183.90-184.01, ~75-85 pips) and fails the floor; and the breakout above 185.84 against the 9-month cap (187.54) yields ~1:1.4 with an approved stop. Warsh's hawkish keynote sustains the ECB-BoJ differential (ECB Sep 9-10; BoJ Sep 17-18). Indicators computed from the MetaTrader 5 D1 series (541 sessions, 01/08/2024 to 01/09/2026).",
      "trend": "Above the 50-day (184.81) and 200-day (184.26) SMAs — full bull alignment; close under the 10/20-day high (185.84), with the 23.6% Fib (185.87) and the 9-month high (187.54) above.",
      "support": "184.81 (50-day SMA) / 184.67 (10-day low), with the 200-day SMA (184.26) and the 50% Fib (184.01) beneath.",
      "resistance": "185.84 (10/20-day highs) / 185.87 (23.6% Fib), with the 9-month high (187.54) above.",
      "priceAction": "No entry — the intervention floor (2.5-sigma20 ~= 111 pips) rejects the pullback's structural stop (~75-85 pips) and the breakout yields ~1:1.4. Re-arm: a deep pullback to the 183.18-184.01 zone (61.8-50% Fib) re-prices the stop, or a sigma20 compression loosens the floor. NFP Friday (Sep 4) and the BoJ Sep 17-18 on the radar.",
      "recommendation": "WAIT FOR ANOTHER TRIGGER",
      "trigger": "None — the intervention floor rejects the pullback setup and the breakout yields ~1:1.4. Reassess on a pullback to the 183.18-184.01 zone (61.8-50% Fib) or with compressed sigma20.",
      "stop": "N/A (no trade).",
      "target": "N/A (no trade).",
      "rr": "N/A", "rrValue": 0,
      "justification": "The bull structure stands whole and price dances under the trigger — but the gate is the gate: with the yen above 160 and the MoF on alert, the 2.5-sigma20 floor (111 pips) rejects every structural stop available in the pullback zone, and the 187.54 cap doesn't pay for the breakout. No protected 1:2, no trade."
    }
  },
  "GBP/JPY": {
    "quote": "216.47", "bias": "ALTA", "biasType": "bull",
    "pt": {
      "fundamental": "O GBP/JPY fechou em 216,47 na sessão de 01/09/2026 (fechamento D1 do MetaTrader 5; mid ao vivo 216,54), estável (+0,03%) e segurando a Fib 23,6% (216,21). O alinhamento segue pleno de alta (SMA50 216,00 > SMA200 212,89). Reprecificação na base MT5: a σ20 lê 70 pips e o piso de intervenção 2,5σ20 sobe para ≈175 pips (yen acima de 160, MoF de prontidão) — o ticket de compra foi reajustado: entrada 215,60, stop 213,75 (sob a Fib 38,2% 214,15; 185 pips ≥ piso), alvo 219,50 (região da máxima de 9 meses 219,56), R/R 1:2.11. BoE 17/09 e BoJ 17-18/09 são os próximos focos institucionais; NFP sexta (04/09) — disparo dentro da janela de 24h, reavaliar após o evento. Indicadores calculados da série D1 do MetaTrader 5 (541 pregões, 01/08/2024 a 01/09/2026).",
      "trend": "Acima das SMA50 (216,00) e SMA200 (212,89) — alinhamento de alta pleno; fechamento acima da Fib 23,6% (216,21) e sob a máxima de 10/20 pregões (217,26), com a máxima de 9 meses (219,56) acima.",
      "support": "216.00 (SMA50), com a mínima de 10 pregões (215,15) e a Fib 38,2% (214,15) abaixo.",
      "resistance": "217.26 (máximas de 10/20 pregões), com o redondo 218,00 e a máxima de 9 meses (219,56) acima.",
      "priceAction": "Setup de compra na retração: aguardar fechamento diário dentro da zona 215.15-216.00 (mínima D10 / SMA50) seguido de fechamento de alta — entrada de referência 215,60, stop 213,75 (sob a Fib 38,2%), alvo 219,50 (região da máxima de 9 meses). A perda por fechamento da Fib 38,2% (214,15) invalida o setup.",
      "recommendation": "COMPRA (LONG) NA RETRAÇÃO",
      "trigger": "Fechamento diário dentro da zona 215.15-216.00 (mínima D10 / SMA50) seguido de fechamento acima do fechamento anterior — entrada de referência 215,60. Dentro da janela de 24h do NFP (quinta), reavaliar após o evento.",
      "stop": "213.75 (sob a Fib 38,2% 214.15 e acima do redondo 213.50; 185 pips ≥ 2,5σ20 de 175 pips) · risco sugerido ≤ 1% por operação.",
      "target": "219.50 (região da máxima de 9 meses 219.56).",
      "rr": "1:2.11", "rrValue": 53,
      "justification": "A estrutura não mudou — o que mudou é a régua: na base MT5 a σ20 lê 70 pips e o piso de intervenção sobe para ~175 pips, empurrando o stop para 213,75 (sob a Fib 38,2%) e a entrada para 215,60; mesmo assim a zona D10/SMA50 comporta o setup com R/R de 1:2.11 rumo ao topo de 9 meses. Comprar a retração à zona, não o topo de 217."
    },
    "en": {
      "fundamental": "GBP/JPY closed at 216.47 in the 01/09/2026 session (MetaTrader 5 D1 close; live mid 216.54), flat (+0.03%) and holding the 23.6% Fib (216.21). The alignment stays fully bullish (50-day 216.00 > 200-day 212.89). Re-priced on the MT5 basis: sigma20 reads 70 pips and the 2.5-sigma20 intervention floor rises to ~=175 pips (yen above 160, MoF on alert) — the buy ticket was adjusted: entry 215.60, stop 213.75 (under the 38.2% Fib 214.15; 185 pips >= floor), target 219.50 (9-month-high region 219.56), R/R 1:2.11. BoE Sep 17 and BoJ Sep 17-18 are the next institutional focuses; NFP Friday (Sep 4) — a trigger inside the 24h window gets reassessed after the event. Indicators computed from the MetaTrader 5 D1 series (541 sessions, 01/08/2024 to 01/09/2026).",
      "trend": "Above the 50-day (216.00) and 200-day (212.89) SMAs — full bull alignment; close above the 23.6% Fib (216.21) and under the 10/20-day high (217.26), with the 9-month high (219.56) above.",
      "support": "216.00 (50-day SMA), with the 10-day low (215.15) and the 38.2% Fib (214.15) beneath.",
      "resistance": "217.26 (10/20-day highs), with the 218.00 round and the 9-month high (219.56) above.",
      "priceAction": "Buy-the-pullback setup: wait for a daily close inside the 215.15-216.00 zone (D10 low / 50-day SMA) followed by a higher close — entry reference 215.60, stop 213.75 (under the 38.2% Fib), target 219.50 (9-month-high region). A close below the 38.2% Fib (214.15) invalidates the setup.",
      "recommendation": "BUY (LONG) ON PULLBACK",
      "trigger": "Daily close inside the 215.15-216.00 zone (D10 low / 50-day SMA) followed by a close above the previous close — entry reference 215.60. Inside the NFP 24h window (Thursday), reassess after the event.",
      "stop": "213.75 (under the 38.2% Fib 214.15 and above the 213.50 round; 185 pips >= the 175-pip 2.5-sigma20 floor) · suggested risk ≤ 1% per trade.",
      "target": "219.50 (9-month-high region, 219.56).",
      "rr": "1:2.11", "rrValue": 53,
      "justification": "The structure didn't change — what changed is the yardstick: on the MT5 basis sigma20 reads 70 pips and the intervention floor rises to ~175 pips, pushing the stop to 213.75 (under the 38.2% Fib) and the entry to 215.60; even so, the D10/50-day zone fits the setup at 1:2.11 R/R toward the 9-month top. Buy the pullback into the zone, not the 217 top."
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

P = DOCS + "/index.html"
html = open(P, encoding="utf-8").read()

html, n = re.subn(r"        const forexData = \{.*?\n\};",
                  "        const forexData = " + fd_json + ";", html, count=1, flags=re.DOTALL)
if n != 1:
    print("FAIL: forexData block"); sys.exit(1)

html = rep(html, OLD_TS_EN, "Reports generated on: " + TS, "ts en badge+i18n", count=2)
html = rep(html, 'generatedAt: "Relatórios gerados em: 01/09/2026 18:04 UTC"', 'generatedAt: "Relatórios gerados em: ' + TS + '"', "ts pt i18n")
html = rep(html, OLD_BASIS_EN, "Data basis: " + BASIS_EN, "basis en")
html = rep(html, OLD_BASIS_PT, "Base de dados: " + BASIS_PT, "basis pt")
html = rep(html, 'nextEvent: "US CPI & Fed speakers"', 'nextEvent: "US NFP — Friday, Sep 4"', "nextEvent en")
html = rep(html, 'nextEvent: "CPI dos EUA & discursos do Fed"', 'nextEvent: "NFP dos EUA — sexta, 04/09"', "nextEvent pt")

html, n = re.subn(
    r"        const dailyChanges = \{.*?\n        \};",
    '''        const dailyChanges = {
            "EUR/USD": "-0.21%",
            "USD/JPY": "+0.28%",
            "AUD/USD": "-0.30%",
            "GBP/USD": "-0.25%",
            "EUR/JPY": "+0.06%",
            "GBP/JPY": "+0.03%"
        };''', html, count=1, flags=re.DOTALL)
if n != 1:
    print("FAIL: dailyChanges"); sys.exit(1)

html, n = re.subn(
    r"        const macroDrivers = \{.*?\n        \};",
    '''        const macroDrivers = {
            "EUR/USD": {
                en: ["Fed hike odds ~55%", "DXY ~99.5", "ECB Sep 9-10"],
                pt: ["Alta Fed ~55%", "DXY ~99,5", "BCE 09-10/09"]
            },
            "USD/JPY": {
                en: ["BoJ 1.00% hawkish", "¥160 MoF watch", "NFP Sep 4"],
                pt: ["BoJ 1,0% hawkish", "MoF vigia ¥160", "NFP 04/09"]
            },
            "AUD/USD": {
                en: ["RBA 4.35%", "WTI $83", "Fed hike ~55%"],
                pt: ["RBA 4,35%", "WTI $83", "Alta Fed ~55%"]
            },
            "GBP/USD": {
                en: ["BoE 3.75% 6-3", "CPI 2.9%", "Fed hike ~55%"],
                pt: ["BoE 3,75% 6-3", "IPC 2,9%", "Alta Fed ~55%"]
            },
            "EUR/JPY": {
                en: ["BoJ 1.00% hawkish", "¥160 MoF watch", "ECB Sep 9-10"],
                pt: ["BoJ 1,0% hawkish", "MoF vigia ¥160", "BCE 09-10/09"]
            },
            "GBP/JPY": {
                en: ["BoJ 1.00% hawkish", "¥160 MoF watch", "BoE Sep 17"],
                pt: ["BoJ 1,0% hawkish", "MoF vigia ¥160", "BoE 17/09"]
            }
        };''', html, count=1, flags=re.DOTALL)
if n != 1:
    print("FAIL: macroDrivers"); sys.exit(1)

open(P, "w", encoding="utf-8").write(html)
print(f"OK: index.html (forexData, 3 timestamps, basis, nextEvent, ticker, macroDrivers) — stamp {TS}")

# =====================================================================
# 2. Static pages
# =====================================================================
PAGE = {"EUR/USD": "eur-usd.html", "USD/JPY": "usd-jpy.html", "AUD/USD": "aud-usd.html",
        "GBP/USD": "gbp-usd.html", "EUR/JPY": "eur-jpy.html", "GBP/JPY": "gbp-jpy.html"}

def update_page(pair, fname, d, gauge_pct, sup_txt, res_txt, chips, next_ev, tier, tier_cls, bar_on, badge):
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
    h = rep(h, '<span class="ts-date">01·09·26</span>', '<span class="ts-date">02·09·26</span>', f"{tag} ts-date")
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
    # verdict badge (class + labels) — only when changing
    if badge:
        h = resub(h, r"<span class=\"verdict-badge \w+\">\s*<span class=\"lang-en\">[^<]*</span>\s*<span class=\"lang-pt\" style=\"display:none;\">[^<]*</span>\s*</span>",
                  badge, f"{tag} verdict badge")
    # ticket class change (eur-usd: sell -> wait)
    h = h.replace('class="trade-ticket verdict-sell"', 'class="trade-ticket verdict-wait"')
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
    "EUR/USD": '<div class="next-event"><span class="ne-tag"><span class="lang-en">Next focus</span><span class="lang-pt" style="display:none;">Próximo foco</span></span> <span class="lang-en">NFP Friday 04/09 · ECB 09-10/09</span><span class="lang-pt" style="display:none;">NFP sexta 04/09 · BCE 09-10/09</span></div>',
    "USD/JPY": '<div class="next-event"><span class="ne-tag"><span class="lang-en">Next focus</span><span class="lang-pt" style="display:none;">Próximo foco</span></span> <span class="lang-en">NFP 04/09 · BoJ 17-18/09</span><span class="lang-pt" style="display:none;">NFP 04/09 · BoJ 17-18/09</span></div>',
    "AUD/USD": '<div class="next-event"><span class="ne-tag"><span class="lang-en">Next focus</span><span class="lang-pt" style="display:none;">Próximo foco</span></span> <span class="lang-en">NFP Friday 04/09</span><span class="lang-pt" style="display:none;">NFP sexta 04/09</span></div>',
    "GBP/USD": '<div class="next-event"><span class="ne-tag"><span class="lang-en">Next focus</span><span class="lang-pt" style="display:none;">Próximo foco</span></span> <span class="lang-en">NFP 04/09 · BoE 17/09</span><span class="lang-pt" style="display:none;">NFP 04/09 · BoE 17/09</span></div>',
    "EUR/JPY": '<div class="next-event"><span class="ne-tag"><span class="lang-en">Next focus</span><span class="lang-pt" style="display:none;">Próximo foco</span></span> <span class="lang-en">NFP 04/09 · BoJ 17-18/09</span><span class="lang-pt" style="display:none;">NFP 04/09 · BoJ 17-18/09</span></div>',
    "GBP/JPY": '<div class="next-event"><span class="ne-tag"><span class="lang-en">Next focus</span><span class="lang-pt" style="display:none;">Próximo foco</span></span> <span class="lang-en">NFP 04/09 · BoJ 17-18/09</span><span class="lang-pt" style="display:none;">NFP 04/09 · BoJ 17-18/09</span></div>',
}

FD["EUR/USD"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — bear regime holds, but the MT5 re-pricing (Fib50 → 1.1698) revoked the short: R/R ~1:1.4</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — regime de baixa segue, mas a reprecificação MT5 (Fib 50% → 1,1698) revogou a venda: R/R ~1:1,4</span>',
    "_tier_en": "Moderate", "_tier_pt": "Moderada",
})
FD["USD/JPY"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — D10 breakout held under the 160.79-161.09 cap; pullback 159.39-159.73 arms only post-NFP</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — rompimento D10 preso sob o teto 160,79-161,09; retração 159,39-159,73 arma só pós-NFP</span>',
    "_tier_en": "Moderate", "_tier_pt": "Moderada",
})
FD["AUD/USD"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action buy">BUY</span> — third pullback day; buy the 0.7000-0.7020 zone, target 0.7195 (R/R 1:3.08)</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action buy">COMPRA</span> — terceiro dia de retração; comprar a zona 0.7000-0.7020, alvo 0.7195 (R/R 1:3,08)</span>',
    "_tier_en": "High", "_tier_pt": "Alta",
})
FD["GBP/USD"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — new 10-day low on the 50% Fib (1.3507); 1.3435-1.3438 vs 1.3587 decides</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — nova mínima de 10 pregões sobre a Fib 50% (1,3507); 1.3435-1.3438 vs 1.3587 decide</span>',
    "_tier_en": "Moderate", "_tier_pt": "Moderada",
})
FD["EUR/JPY"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action wait">WAIT</span> — glued under 185.84; the intervention floor (111 pips) still rejects the stop</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action wait">AGUARDAR</span> — colado sob 185,84; o piso de intervenção (111 pips) segue rejeitando o stop</span>',
    "_tier_en": "Moderate", "_tier_pt": "Moderada",
})
FD["GBP/JPY"].update({
    "_bluf_en": '<span class="lang-en"><span class="bluf-action buy">BUY</span> — re-priced on MT5: buy the 215.15-216.00 zone, stop 213.75, target 219.50 (1:2.11)</span>',
    "_bluf_pt": '<span class="lang-pt" style="display:none;"><span class="bluf-action buy">COMPRA</span> — reprecificado no MT5: comprar a zona 215.15-216.00, stop 213,75, alvo 219,50 (1:2,11)</span>',
    "_tier_en": "Good", "_tier_pt": "Boa",
})

CHIPS = {
    "EUR/USD": [('<span class="macro-chip lang-en">Fed Sep hike ~57%</span>', '<span class="macro-chip lang-en">Fed Sep hike ~55%</span>', "1en"),
                ('<span class="macro-chip lang-pt" style="display:none;">Alta Fed set ~57%</span>', '<span class="macro-chip lang-pt" style="display:none;">Alta Fed set ~55%</span>', "1pt")],
    "USD/JPY": [('<span class="macro-chip lang-en">Intervention fade</span>', '<span class="macro-chip lang-en">¥160 MoF watch</span>', "2en"),
                ('<span class="macro-chip lang-pt" style="display:none;">Intervenção esvaindo</span>', '<span class="macro-chip lang-pt" style="display:none;">MoF vigia ¥160</span>', "2pt")],
    "AUD/USD": [('<span class="macro-chip lang-en">Fed dovish</span>', '<span class="macro-chip lang-en">Fed hike ~55%</span>', "3en"),
                ('<span class="macro-chip lang-pt" style="display:none;">Fed dovish</span>', '<span class="macro-chip lang-pt" style="display:none;">Alta Fed ~55%</span>', "3pt")],
    "GBP/USD": [('<span class="macro-chip lang-en">CPI 2.6%</span>', '<span class="macro-chip lang-en">CPI 2.9%</span>', "4en"),
                ('<span class="macro-chip lang-pt" style="display:none;">IPC 2,6%</span>', '<span class="macro-chip lang-pt" style="display:none;">IPC 2,9%</span>', "4pt"),
                ('<span class="macro-chip lang-en">Fed dovish</span>', '<span class="macro-chip lang-en">Fed hike ~55%</span>', "4en2"),
                ('<span class="macro-chip lang-pt" style="display:none;">Fed dovish</span>', '<span class="macro-chip lang-pt" style="display:none;">Alta Fed ~55%</span>', "4pt2")],
    "EUR/JPY": [('<span class="macro-chip lang-en">Intervention fade</span>', '<span class="macro-chip lang-en">¥160 MoF watch</span>', "5en"),
                ('<span class="macro-chip lang-pt" style="display:none;">Intervenção esvaindo</span>', '<span class="macro-chip lang-pt" style="display:none;">MoF vigia ¥160</span>', "5pt")],
    "GBP/JPY": [('<span class="macro-chip lang-en">Intervention fade</span>', '<span class="macro-chip lang-en">¥160 MoF watch</span>', "6en"),
                ('<span class="macro-chip lang-pt" style="display:none;">Intervenção esvaindo</span>', '<span class="macro-chip lang-pt" style="display:none;">MoF vigia ¥160</span>', "6pt")],
}

# gauge percent computed from support/resistance leading numbers vs quote
GAUGE = {"EUR/USD": ("29", "1.1583", "1.1618"), "USD/JPY": ("56", "159.39", "160.79"),
         "AUD/USD": ("40", "0.7113", "0.7194"), "GBP/USD": ("46", "1.3454", "1.3587"),
         "EUR/JPY": ("83", "184.81", "185.84"), "GBP/JPY": ("37", "216.00", "217.26")}
TIER = {"EUR/USD": ("0/10", "t-mod", 0), "USD/JPY": ("0/10", "t-mod", 0),
        "AUD/USD": ("9/10", "t-high", 8), "GBP/USD": ("0/10", "t-mod", 0),
        "EUR/JPY": ("0/10", "t-mod", 0), "GBP/JPY": ("6/10", "", 6)}
BADGE = {"EUR/USD": '<span class="verdict-badge wait">\n                                    <span class="lang-en">WAIT FOR ANOTHER TRIGGER</span>\n                                    <span class="lang-pt" style="display:none;">AGUARDAR OUTRO GATILHO</span>\n                                </span>'}

for pair, fname in PAGE.items():
    g = GAUGE[pair]; t = TIER[pair]
    update_page(pair, fname, FD[pair], g[0], g[1], g[2], CHIPS[pair], NEXT_EV[pair],
                t[0], t[1], t[2], BADGE.get(pair))

# =====================================================================
# 3. track-record ledger
# =====================================================================
LED = DOCS + "/track-record.json"
led = json.load(open(LED, encoding="utf-8"))
led["meta"]["lastUpdated"] = TS_DATE
led["meta"]["conventions"]["data"] = "MetaTrader 5 D1 closes (fallback: ECB/Frankfurter daily reference rates). All triggers and resolutions are CLOSE-based."
led["meta"]["conventions"]["revoked"] = "A watching ticket withdrawn by a later report before its trigger fired (e.g. levels re-priced on the current data basis); realized R is null."
# EUR/USD 01/09 short ticket -> revoked (moved to closed)
rev = [t for t in led["watching"] if t["pair"] == "EUR/USD"][0]
rev["outcome"] = "revoked"
rev["exitDate"] = TS_DATE
rev["note"] = "revoked in the 02/09 MT5-basis edition: the 50% Fib re-priced 1.1657 -> 1.1698, so stop 1.1665 lost its structural cover; protected R/R ~1:1.4 fails the 1:2 gate"
led["closed"].append(rev)
led["watching"] = [t for t in led["watching"] if t["pair"] != "EUR/USD"]
# AUD/USD ticket refreshed (same levels, SMA50 now 0.7020 on MT5)
for t in led["watching"]:
    if t["pair"] == "AUD/USD":
        t["reportDate"] = TS_DATE
        t["triggerRule"] = "daily close inside 0.7000-0.7020 (round + 50-day SMA) followed by a close above the previous close and the 0.7010 midpoint; skip if inside the NFP 24h window (reassess after 04/09)"
        t["note"] = "zone awaited since 21/08; third pullback day from the 0.7194 top engages it"
    if t["pair"] == "GBP/JPY":
        t["reportDate"] = TS_DATE
        t["entry"] = 215.60; t["stop"] = 213.75; t["target"] = 219.50; t["plannedR"] = 2.11
        t["triggerRule"] = "daily close inside 215.15-216.00 (D10 low + 50-day SMA) followed by a close above the previous close; skip if inside the NFP 24h window"
        t["note"] = "re-priced on the MT5 basis (sigma20 70): stop 213.75 under the 38.2% Fib 214.15; 185 pips >= the 175-pip 2.5-sigma20 intervention floor"
with open(LED, "w", encoding="utf-8") as f:
    json.dump(led, f, ensure_ascii=False, indent=2)
print("OK: track-record.json (EUR/USD revoked; AUD/USD + GBP/JPY re-dated/re-priced)")
print(f"\nDONE {TS} — run verify_all.py next.")
