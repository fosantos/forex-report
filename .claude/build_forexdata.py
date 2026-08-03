#!/usr/bin/env python3
"""Replace the forexData block + timestamps + ticker in docs/index.html with verified computed data.
Aborts on any structural mismatch. Validates forexData parses as JS-object-equivalent JSON."""
import re, json, sys

PATH = r"C:/Projetos/forex-report/docs/index.html"
TS = "03/08/2026 13:30 UTC"

with open(PATH, encoding="utf-8") as f:
    html = f.read()

# ---- New forexData block (literal string, matches existing indentation/style) ----
NEW_BLOCK = '''        const forexData = {
          "EUR/USD": {
                    "quote": "1.1535",
                    "bias": "BAIXA",
                    "biasType": "bear",
                    "pt": {
                              "fundamental": "O EUR/USD opera em 1,1535 no fechamento diário de 03/08/2026 (referência BCE, ~14:15 CET), com a estrutura técnica prevalecendo sobre um cenário macro de dólar mais fraco. A manutenção dividida do Fed em 9-3 a 3,50-3,75% em 29/07 (chairman Warsh) e a fraqueza do dólar por contágio do iene alimentaram uma correção de +1,5% desde a mínima de 1,1340, mas o par segue abaixo da SMA200 (1,1628) dentro do downtrend de 9 meses (1,1974 a 1,1340). Os indicadores (SMA 50/200 e Fibonacci) são calculados a partir da série diária BCE/Frankfurter (511 pregões, 01/08/2024 a 03/08/2026). A recuperação estaca na confluência Fib 50% (1,1657) / SMA200 (1,1628) — zona de retomada de baixa.",
                              "trend": "Abaixo da SMA200 (1,1628) e acima da SMA50 (1,1481); o downtrend de médio prazo (1,1974 a 1,1340) segue intacto, com o movimento atual sendo uma correção de baixa rumo à confluência Fib 50% / SMA200.",
                              "support": "1,1476 (Fib 78,6%), com a mínima de 1,1340 abaixo.",
                              "resistance": "1,1657 (Fib 50%) em confluência com a SMA200 de 1,1628; 1,1732 (Fib 38,2%) acima.",
                              "priceAction": "Uma rejeição de baixa (pin bar / engolfo de baixa) na confluência 1,1628-1,1657 (SMA200 / Fib 50%), com fechamento diário retomando abaixo de 1,1582 (Fib 61,8%), retomaria a queda rumo a 1,1476-1,1450.",
                              "recommendation": "VENDA (SHORT) NA RETRAÇÃO",
                              "trigger": "Rejeição de baixa (pin bar / engolfo de baixa) em 1,1657 (confluência Fib 50% / SMA200), com fechamento diário sustentando abaixo de 1,1582.",
                              "stop": "1,1740 (Acima da Fib 38,2% em 1,1732).",
                              "target": "1,1450 (Logo abaixo da Fib 78,6% em 1,1476).",
                              "rr": "1:2.49",
                              "rrValue": 62,
                              "justification": "A estrutura técnica — abaixo da SMA200 e falhando na Fib 50% — supera o macro de dólar mais fraco, mantendo o viés de baixa. Uma rejeição na confluência 1,1657/1,1628 (Fib 50% / SMA200) oferece entrada vendida com stop protegido acima da Fib 38,2% e R/R de 1:2.49 rumo a 1,1450."
                    },
                    "en": {
                              "fundamental": "EUR/USD trades at 1.1535 on the 03/08/2026 daily close (ECB reference, ~14:15 CET), with the technical structure overriding a softer-USD macro backdrop. The Fed's divided 9-3 hold at 3.50-3.75% on July 29 (Chair Warsh) and yen-spillover dollar weakness have fueled a +1.5% bounce off the 1.1340 low, but the pair remains below its 200-day SMA (1.1628) inside the 9-month 1.1974 to 1.1340 downtrend. Indicators (SMA 50/200, Fibonacci) are computed from the ECB/Frankfurter daily series (511 sessions, 01/08/2024 to 03/08/2026). The recovery stalls at the 50% Fib (1.1657) / 200-day SMA (1.1628) confluence — the bear-resumption zone.",
                              "trend": "Below the 200-day SMA (1.1628) and above the 50-day SMA (1.1481); the medium-term downtrend (1.1974 to 1.1340) stays intact, with the bounce a bear-market rally into the 50% Fib / 200-day confluence.",
                              "support": "1.1476 (78.6% Fib), with the 1.1340 swing low beneath.",
                              "resistance": "1.1657 (50% Fib) in confluence with the 1.1628 200-day SMA; 1.1732 (38.2% Fib) above.",
                              "priceAction": "A bearish rejection (pin bar / bearish engulfing) at the 1.1628-1.1657 confluence (200-day SMA / 50% Fib), with a daily close back below 1.1582 (61.8% Fib), would resume the drop toward 1.1476-1.1450.",
                              "recommendation": "SELL (SHORT) ON PULLBACK",
                              "trigger": "Bearish rejection (pin bar / bearish engulfing) at 1.1657 (50% Fib / 200-day SMA confluence), on a daily close holding below 1.1582.",
                              "stop": "1.1740 (Above the 38.2% Fib at 1.1732).",
                              "target": "1.1450 (Just below the 78.6% Fib at 1.1476).",
                              "rr": "1:2.49",
                              "rrValue": 62,
                              "justification": "The technical structure — below the 200-day SMA and failing at the 50% Fib — outweighs the softer-USD macro, keeping the bias bearish. A rejection at the 1.1657/1.1628 confluence (50% Fib / 200-day SMA) offers a short with a structurally-protected stop above the 38.2% Fib and 1:2.49 R/R toward 1.1450."
                    }
          },
          "USD/JPY": {
                    "quote": "156.68",
                    "bias": "BAIXA",
                    "biasType": "bear",
                    "pt": {
                              "fundamental": "O USD/JPY opera em 156,68 no fechamento diário de 03/08/2026 (referência BCE), desabando -2,22% após a manutenção hawkish do BoJ a 1,0% (8-1 em 31/07) e a suspeita de intervenção do MoF no iene durante a noite. O par rompeu a SMA200 (157,81) e a SMA50 (161,35), caindo sobre a Fib 61,8% (156,66) do avanço de 152,17 a 163,91. O choque de intervenção supera o diferencial ainda amplo Fed-BoJ; a estrutura agora é de baixa abaixo dos 200 dias. Indicadores calculados a partir da série diária BCE/Frankfurter (511 pregões).",
                              "trend": "Abaixo das SMA50 (161,35) e SMA200 (157,81) — o avanço de 152,17 a 163,91 foi rompido; a primeira perna de reversão de baixa mira a zona Fib 61,8%/78,6% (156,66/154,68).",
                              "support": "154,68 (Fib 78,6%), com a mínima de 152,17 abaixo.",
                              "resistance": "158,04 (Fib 50%) em confluência com a rompida SMA200 de 157,81; 159,43 (Fib 38,2%) acima.",
                              "priceAction": "Uma rejeição de máxima descendente (engolfo de baixa) na zona 158,04-157,81 (Fib 50% / SMA200 rompida), com fechamento diário novamente abaixo de 156,66, miraria 154,68.",
                              "recommendation": "VENDA (SHORT) NA RETRAÇÃO",
                              "trigger": "Rejeição de máxima descendente (engolfo de baixa) em 158,00 (Fib 50% / SMA200 rompida), com fechamento diário novamente abaixo de 156,66.",
                              "stop": "159,50 (Acima da Fib 38,2% em 159,43).",
                              "target": "154,50 (Logo abaixo da Fib 78,6% em 154,68).",
                              "rr": "1:2.33",
                              "rrValue": 58,
                              "justification": "O rompimento abaixo da SMA200, impulsionado pela manutenção hawkish do BoJ e pela suspeita de intervenção, supera o amplo diferencial Fed-BoJ; a estrutura é de baixa. Uma retração até a Fib 50% / SMA200 rompida oferece entrada vendida com stop protegido acima da Fib 38,2% e R/R de 1:2.33 rumo a 154,50. Volatilidade de choque de intervenção — dimensione adequadamente."
                    },
                    "en": {
                              "fundamental": "USD/JPY trades at 156.68 on the 03/08/2026 daily close (ECB reference), collapsing -2.22% after the BoJ's hawkish hold at 1.00% (8-1 on July 31) and suspected MoF yen intervention overnight. The pair has sliced through its 200-day SMA (157.81) and 50-day SMA (161.35), landing on the 61.8% Fib (156.66) of the 152.17 to 163.91 uptrend. The intervention shock overrides the still-wide Fed-BoJ differential; structure is now bearish below the 200-day. Indicators computed from the ECB/Frankfurter daily series (511 sessions).",
                              "trend": "Below both the 50-day (161.35) and 200-day (157.81) SMAs — the 152.17 to 163.91 uptrend has broken; the first leg of a bear reversal targets the 61.8%/78.6% Fib zone (156.66/154.68).",
                              "support": "154.68 (78.6% Fib), with the 152.17 swing low beneath.",
                              "resistance": "158.04 (50% Fib) in confluence with the broken 157.81 200-day SMA; 159.43 (38.2% Fib) above.",
                              "priceAction": "A lower-high rejection (bearish engulfing) at the 158.04-157.81 zone (50% Fib / broken 200-day SMA), with a daily close back below 156.66, would target 154.68.",
                              "recommendation": "SELL (SHORT) ON PULLBACK",
                              "trigger": "Lower-high rejection (bearish engulfing) at 158.00 (50% Fib / broken 200-day SMA), on a daily close back below 156.66.",
                              "stop": "159.50 (Above the 38.2% Fib at 159.43).",
                              "target": "154.50 (Just below the 78.6% Fib at 154.68).",
                              "rr": "1:2.33",
                              "rrValue": 58,
                              "justification": "The breakdown below the 200-day SMA, driven by the BoJ's hawkish hold and suspected intervention, overrides the wide Fed-BoJ rate gap; structure is bearish. A bounce to the 50% Fib / broken 200-day offers a short with a protected stop above the 38.2% Fib and 1:2.33 R/R toward 154.50. Intervention-shock volatility — size accordingly."
                    }
          },
          "AUD/USD": {
                    "quote": "0.7007",
                    "bias": "ALTA",
                    "biasType": "bull",
                    "pt": {
                              "fundamental": "O AUD/USD opera em 0,7007 no fechamento diário de 03/08/2026 (referência BCE), sustentando a tendência de alta acima da SMA200 (0,6901). Um RBA hawkish a 4,35% (manutenção por unanimidade após o ciclo de altas de 2026 reverter os cortes do ano anterior) e a alta de +16% no Brent no mês sustentam o australiano, enquanto a manutenção dividida e dovish do Fed limita o dólar. O par repousa sobre uma SMA50 lateral (0,7007), abaixo da Fib 23,6% (0,7065) do avanço de 0,6445 a 0,7257. Indicadores calculados a partir da série diária BCE/Frankfurter (511 pregões). A estrutura segue de alta enquanto a SMA200 segurar.",
                              "trend": "Acima das SMA50 (0,7007) e SMA200 (0,6901) — repousando sobre uma SMA50 lateral dentro da tendência mais ampla de 0,6445 a 0,7257; a retração mira a Fib 38,2% (0,6947).",
                              "support": "0,6947 (Fib 38,2%), com a SMA200 de 0,6901 abaixo.",
                              "resistance": "0,7065 (Fib 23,6%), com a máxima de 0,7257 acima.",
                              "priceAction": "Uma rejeição de alta (pin bar / engolfo bullish) na zona 0,6947-0,6960 (Fib 38,2%), com fechamento diário novamente acima de 0,7010, retomaria a alta rumo a 0,7150.",
                              "recommendation": "COMPRA (LONG) NA RETRAÇÃO",
                              "trigger": "Rejeição de alta (pin bar / engolfo bullish) em 0,6960 (zona Fib 38,2%), com fechamento diário sustentando acima de 0,7010.",
                              "stop": "0,6890 (Abaixo da SMA200 de 0,6901).",
                              "target": "0,7150 (Acima da Fib 23,6% em 0,7065).",
                              "rr": "1:2.71",
                              "rrValue": 68,
                              "justification": "A estrutura acima de ambas as SMAs, respaldada por um RBA a 4,35% e commodities firmes contra um Fed dividido, mantém o viés de alta. Uma retração até a Fib 38,2% oferece entrada comprada com stop protegido abaixo da SMA200 e R/R de 1:2.71 rumo a 0,7150."
                    },
                    "en": {
                              "fundamental": "AUD/USD trades at 0.7007 on the 03/08/2026 daily close (ECB reference), holding its uptrend above the 200-day SMA (0.6901). A hawkish RBA at 4.35% (held unanimously after its 2026 hiking cycle reversed the prior year's cuts) and Brent's +16% monthly surge underpin the aussie, while the Fed's divided dovish hold caps the dollar. The pair rests on a flat 50-day SMA (0.7007), below the 23.6% Fib (0.7065) of the 0.6445 to 0.7257 advance. Indicators computed from the ECB/Frankfurter daily series (511 sessions). Structure stays bullish while the 200-day holds.",
                              "trend": "Above both the 50-day (0.7007) and 200-day (0.6901) SMAs — resting on a flat 50-day within the broader 0.6445 to 0.7257 uptrend; pullback target is the 38.2% Fib (0.6947).",
                              "support": "0.6947 (38.2% Fib), with the 0.6901 200-day SMA beneath.",
                              "resistance": "0.7065 (23.6% Fib), with the 0.7257 swing high above.",
                              "priceAction": "A bullish rejection (pin bar / bullish engulfing) at the 0.6947-0.6960 zone (38.2% Fib), with a daily close back above 0.7010, would resume the uptrend toward 0.7150.",
                              "recommendation": "BUY (LONG) ON PULLBACK",
                              "trigger": "Bullish rejection (pin bar / bullish engulfing) at 0.6960 (38.2% Fib zone), on a daily close back above 0.7010.",
                              "stop": "0.6890 (Below the 0.6901 200-day SMA).",
                              "target": "0.7150 (Above the 23.6% Fib at 0.7065).",
                              "rr": "1:2.71",
                              "rrValue": 68,
                              "justification": "The structure above both SMAs, backed by a 4.35% RBA and firm commodities against a divided Fed, keeps the bias bullish. A pullback to the 38.2% Fib offers a long with a protected stop below the 200-day SMA and 1:2.71 R/R toward 0.7150."
                    }
          },
          "GBP/USD": {
                    "quote": "1.3470",
                    "bias": "ALTA",
                    "biasType": "bull",
                    "pt": {
                              "fundamental": "O GBP/USD opera em 1,3470 no fechamento diário de 03/08/2026 (referência BCE), sustentando acima de ambas as SMAs. A manutenção hawkish do BoE a 3,75% (7-2 em 30/07, com Pill e Greene votando por alta) e a inflação a 2,6% sustentam a libra, enquanto a manutenção dividida e dovish do Fed pressiona o dólar. O par reconquistou a Fib 50% (1,3430) do avanço de 1,3044 a 1,3817 e mira a Fib 38,2% (1,3522), acima das SMA50 (1,3362) e SMA200 (1,3396). Indicadores calculados a partir da série diária BCE/Frankfurter (511 pregões). A estrutura segue de alta enquanto a SMA200 segurar.",
                              "trend": "Acima das SMA50 (1,3362) e SMA200 (1,3396); reconquistando a Fib 50% (1,3430) dentro do uptrend de 1,3044 a 1,3817, próximo obstáculo a Fib 38,2% (1,3522).",
                              "support": "1,3430 (Fib 50%), com a SMA200 de 1,3396 abaixo.",
                              "resistance": "1,3522 (Fib 38,2%), com a máxima de 1,3817 acima.",
                              "priceAction": "Uma rejeição de alta (pin bar / engolfo bullish) na zona 1,3430-1,3396 (Fib 50% / SMA200), com fechamento diário novamente acima de 1,3470, retomaria a alta rumo a 1,3522-1,3620.",
                              "recommendation": "COMPRA (LONG) NA RETRAÇÃO",
                              "trigger": "Rejeição de alta (pin bar / engolfo bullish) em 1,3410 (confluência Fib 50% / SMA200), com fechamento diário sustentando acima de 1,3470.",
                              "stop": "1,3330 (Abaixo da Fib 61,8% em 1,3339).",
                              "target": "1,3620 (Acima da Fib 38,2% em 1,3522).",
                              "rr": "1:2.63",
                              "rrValue": 66,
                              "justification": "A estrutura acima de ambas as SMAs, reforçada por um BoE hawkish contra um Fed dividido, mantém o viés de alta. Uma retração até a confluência Fib 50% / SMA200 oferece entrada comprada com stop protegido abaixo da Fib 61,8% e R/R de 1:2.63 rumo a 1,3620."
                    },
                    "en": {
                              "fundamental": "GBP/USD trades at 1.3470 on the 03/08/2026 daily close (ECB reference), holding above both SMAs. The BoE's hawkish hold at 3.75% (7-2 on July 30, with Pill and Greene seeking a hike) and inflation at 2.6% support sterling, while the Fed's divided dovish hold pressures the dollar. The pair has reclaimed the 50% Fib (1.3430) of the 1.3044 to 1.3817 advance and eyes the 38.2% Fib (1.3522), above the 50-day (1.3362) and 200-day (1.3396) SMAs. Indicators computed from the ECB/Frankfurter daily series (511 sessions). Structure stays bullish while the 200-day holds.",
                              "trend": "Above both the 50-day (1.3362) and 200-day (1.3396) SMAs; reclaiming the 50% Fib (1.3430) within the 1.3044 to 1.3817 uptrend, next hurdle the 38.2% Fib (1.3522).",
                              "support": "1.3430 (50% Fib), with the 1.3396 200-day SMA beneath.",
                              "resistance": "1.3522 (38.2% Fib), with the 1.3817 swing high above.",
                              "priceAction": "A bullish rejection (pin bar / bullish engulfing) at the 1.3430-1.3396 zone (50% Fib / 200-day SMA), with a daily close back above 1.3470, would resume the uptrend toward 1.3522-1.3620.",
                              "recommendation": "BUY (LONG) ON PULLBACK",
                              "trigger": "Bullish rejection (pin bar / bullish engulfing) at 1.3410 (50% Fib / 200-day SMA confluence), on a daily close back above 1.3470.",
                              "stop": "1.3330 (Below the 61.8% Fib at 1.3339).",
                              "target": "1.3620 (Above the 38.2% Fib at 1.3522).",
                              "rr": "1:2.63",
                              "rrValue": 66,
                              "justification": "The structure above both SMAs, reinforced by a hawkish BoE against a divided Fed, keeps the bias bullish. A pullback to the 50% Fib / 200-day SMA confluence offers a long with a protected stop below the 61.8% Fib and 1:2.63 R/R toward 1.3620."
                    }
          },
          "EUR/JPY": {
                    "quote": "180.73",
                    "bias": "BAIXA",
                    "biasType": "bear",
                    "pt": {
                              "fundamental": "O EUR/JPY opera em 180,73 no fechamento diário de 03/08/2026 (referência BCE), desabando -1,80% enquanto a manutenção hawkish do BoJ a 1,0% e a suspeita de intervenção no iene dispararam um desenrolar agressivo de posições em cruzes. O par rompeu a SMA200 (183,48) e a SMA50 (185,24), caindo sobre a Fib 61,8% (180,72) do avanço de 176,39 a 187,73. Apesar do diferencial de carry ainda amplo entre BCE (2,25%) e BoJ (1,0%), o choque de intervenção domina; a estrutura agora é de baixa abaixo dos 200 dias. Indicadores calculados a partir da série diária BCE/Frankfurter (511 pregões).",
                              "trend": "Abaixo das SMA50 (185,24) e SMA200 (183,48) — o avanço de 176,39 a 187,73 foi rompido; a perna de baixa repousa sobre a Fib 61,8% (180,72).",
                              "support": "178,81 (Fib 78,6%), com a mínima de 176,39 abaixo.",
                              "resistance": "183,48 (SMA200) em confluência com a Fib 38,2% (183,39); 185,24 (SMA50) acima.",
                              "priceAction": "Uma rejeição de máxima descendente (engolfo de baixa) na zona 183,39-183,48 (Fib 38,2% / SMA200 rompida), com fechamento diário novamente abaixo de 182,06 (Fib 50%), miraria 180,72-178,81.",
                              "recommendation": "VENDA (SHORT) NA RETRAÇÃO",
                              "trigger": "Rejeição de máxima descendente (engolfo de baixa) em 183,40 (confluência Fib 38,2% / SMA200 rompida), com fechamento diário novamente abaixo de 182,06.",
                              "stop": "184,60 (Acima da zona de rejeição, abaixo da SMA50 em 185,24).",
                              "target": "180,70 (Fib 61,8%), estendido a 178,81 (Fib 78,6%).",
                              "rr": "1:2.25",
                              "rrValue": 56,
                              "justification": "O rompimento abaixo da SMA200, impulsionado pela manutenção hawkish do BoJ e pela suspeita de intervenção, supera o amplo diferencial de carry BCE-BoJ; a estrutura é de baixa. Uma retração até a Fib 38,2% / SMA200 rompida oferece entrada vendida com stop protegido e R/R de 1:2.25 rumo à Fib 61,8% (180,70). Volatilidade de choque de intervenção — dimensione adequadamente."
                    },
                    "en": {
                              "fundamental": "EUR/JPY trades at 180.73 on the 03/08/2026 daily close (ECB reference), crashing -1.80% as the BoJ's hawkish hold at 1.00% and suspected yen intervention triggered aggressive cross-unwinding. The pair has sliced through its 200-day SMA (183.48) and 50-day SMA (185.24), landing on the 61.8% Fib (180.72) of the 176.39 to 187.73 uptrend. Despite the still-wide ECB (2.25%)-BoJ (1.00%) carry gap, the intervention shock dominates; structure is now bearish below the 200-day. Indicators computed from the ECB/Frankfurter daily series (511 sessions).",
                              "trend": "Below both the 50-day (185.24) and 200-day (183.48) SMAs — the 176.39 to 187.73 uptrend has broken; the bear leg sits on the 61.8% Fib (180.72).",
                              "support": "178.81 (78.6% Fib), with the 176.39 swing low beneath.",
                              "resistance": "183.48 (200-day SMA) in confluence with the 38.2% Fib (183.39); 185.24 (50-day SMA) above.",
                              "priceAction": "A lower-high rejection (bearish engulfing) at the 183.39-183.48 zone (38.2% Fib / broken 200-day SMA), with a daily close back below 182.06 (50% Fib), would target 180.72-178.81.",
                              "recommendation": "SELL (SHORT) ON PULLBACK",
                              "trigger": "Lower-high rejection (bearish engulfing) at 183.40 (38.2% Fib / broken 200-day SMA confluence), on a daily close back below 182.06.",
                              "stop": "184.60 (Above the rejection zone, below the 50-day SMA at 185.24).",
                              "target": "180.70 (61.8% Fib), extended to 178.81 (78.6% Fib).",
                              "rr": "1:2.25",
                              "rrValue": 56,
                              "justification": "The breakdown below the 200-day SMA, driven by the BoJ's hawkish hold and suspected intervention, overrides the wide ECB-BoJ carry gap; structure is bearish. A bounce to the 38.2% Fib / broken 200-day offers a short with a protected stop and 1:2.25 R/R toward the 61.8% Fib (180.70). Intervention-shock volatility — size accordingly."
                    }
          },
          "GBP/JPY": {
                    "quote": "211.05",
                    "bias": "BAIXA",
                    "biasType": "bear",
                    "pt": {
                              "fundamental": "O GBP/JPY opera em 211,05 no fechamento diário de 03/08/2026 (referência BCE), despencando -1,87% enquanto a manutenção hawkish do BoJ a 1,0% e a suspeita de intervenção no iene atingiram as cruzes com mais força. O par rompeu a SMA200 (211,40) e a SMA50 (215,60), agora entre a Fib 38,2% (212,03) e a Fib 50% (209,84) do avanço de 200,53 a 219,14. Apesar do amplo diferencial de carry BoE (3,75%)-BoJ (1,0%), o choque de intervenção domina; a estrutura agora é de baixa abaixo dos 200 dias. Indicadores calculados a partir da série diária BCE/Frankfurter (511 pregões).",
                              "trend": "Abaixo das SMA50 (215,60) e SMA200 (211,40) — o avanço de 200,53 a 219,14 foi rompido; a perna de baixa mira a Fib 50% (209,84).",
                              "support": "209,84 (Fib 50%), com a 207,64 (Fib 61,8%) abaixo.",
                              "resistance": "212,03 (Fib 38,2%) logo acima da rompida SMA200 de 211,40; 215,60 (SMA50) acima.",
                              "priceAction": "Uma rejeição de máxima descendente (engolfo de baixa) na zona 211,40-212,03 (SMA200 rompida / Fib 38,2%), com fechamento diário novamente abaixo de 210,50, miraria 209,84.",
                              "recommendation": "VENDA (SHORT) NA RETRAÇÃO",
                              "trigger": "Rejeição de máxima descendente (engolfo de baixa) em 211,50 (zona SMA200 rompida / Fib 38,2%), com fechamento diário novamente abaixo de 210,50.",
                              "stop": "212,30 (Acima da Fib 38,2% em 212,03).",
                              "target": "209,80 (Fib 50%).",
                              "rr": "1:2.12",
                              "rrValue": 53,
                              "justification": "O rompimento abaixo da SMA200, impulsionado pela manutenção hawkish do BoJ e pela suspeita de intervenção, supera o amplo diferencial de carry BoE-BoJ; a estrutura é de baixa. Uma retração até a SMA200 rompida / Fib 38,2% oferece entrada vendida com stop protegido acima da Fib 38,2% e R/R de 1:2.12 rumo à Fib 50% (209,80) — o caminho mais limpo, sem S/R intermediária bloqueando. Volatilidade de choque de intervenção — dimensione adequadamente."
                    },
                    "en": {
                              "fundamental": "GBP/JPY trades at 211.05 on the 03/08/2026 daily close (ECB reference), plunging -1.87% as the BoJ's hawkish hold at 1.00% and suspected yen intervention hit the crosses hardest. The pair has broken its 200-day SMA (211.40) and 50-day SMA (215.60), now sitting between the 38.2% Fib (212.03) and 50% Fib (209.84) of the 200.53 to 219.14 uptrend. Despite the wide BoE (3.75%)-BoJ (1.00%) carry gap, the intervention shock dominates; structure is now bearish below the 200-day. Indicators computed from the ECB/Frankfurter daily series (511 sessions).",
                              "trend": "Below both the 50-day (215.60) and 200-day (211.40) SMAs — the 200.53 to 219.14 uptrend has broken; the bear leg eyes the 50% Fib (209.84).",
                              "support": "209.84 (50% Fib), with the 207.64 (61.8% Fib) beneath.",
                              "resistance": "212.03 (38.2% Fib) just above the broken 211.40 200-day SMA; 215.60 (50-day SMA) above.",
                              "priceAction": "A lower-high rejection (bearish engulfing) at the 211.40-212.03 zone (broken 200-day SMA / 38.2% Fib), with a daily close back below 210.50, would target 209.84.",
                              "recommendation": "SELL (SHORT) ON PULLBACK",
                              "trigger": "Lower-high rejection (bearish engulfing) at 211.50 (broken 200-day SMA / 38.2% Fib zone), on a daily close back below 210.50.",
                              "stop": "212.30 (Above the 38.2% Fib at 212.03).",
                              "target": "209.80 (50% Fib).",
                              "rr": "1:2.12",
                              "rrValue": 53,
                              "justification": "The breakdown below the 200-day SMA, driven by the BoJ's hawkish hold and suspected intervention, overrides the wide BoE-BoJ carry gap; structure is bearish. A bounce to the broken 200-day / 38.2% Fib offers a short with a protected stop above the 38.2% Fib and 1:2.12 R/R toward the 50% Fib (209.80) — the cleanest path with no intermediate S/R blocking. Intervention-shock volatility — size accordingly."
                    }
          }
};'''

# ---- Replace forexData block ----
# Match from 'const forexData = {' to the matching '};' that closes it.
start = html.find("        const forexData = {")
if start == -1:
    sys.exit("ERROR: forexData start not found")
# find the closing '};' — search for '\n};' after start
end_marker = "\n};"
end = html.find(end_marker, start)
if end == -1:
    sys.exit("ERROR: forexData end not found")
end += len(end_marker)

old_block = html[start:end]
# sanity: ensure old block contains all six pair keys in order
for key in ["EUR/USD", "USD/JPY", "AUD/USD", "GBP/USD", "EUR/JPY", "GBP/JPY"]:
    if old_block.count('"' + key + '"') != 1:
        sys.exit(f"ERROR: pair key {key} not found exactly once in old forexData block")

html = html[:start] + NEW_BLOCK + html[end:]

# ---- Replace timestamps (3 spots) ----
# #generationTime badge
m = re.search(r'(id="generationTime"[^>]*>Reports generated on: )[^<]*(</p>)', html)
if not m:
    sys.exit("ERROR: #generationTime badge not found")
html = html[:m.start()] + m.group(1) + TS + m.group(2) + html[m.end():]

# EN generatedAt
en_re = re.compile(r'(en:\s*\{[^}]*?generatedAt:\s*")([^"]*)(")')
# This is fragile because of nested braces; do targeted literal replacements instead.
old_ts = "02/08/2026 15:00 UTC"
count = html.count(old_ts)
if count != 2:
    sys.exit(f"ERROR: expected 2 remaining old timestamp occurrences, found {count}")
html = html.replace(old_ts, TS)

# ---- Replace ticker changes block ----
old_changes = '''            const changes = {
                "EUR/USD": "+0.08%",
                "USD/JPY": "-1.66%",
                "AUD/USD": "+0.53%",
                "GBP/USD": "+0.25%",
                "EUR/JPY": "-1.58%",
                "GBP/JPY": "-1.42%"
            };'''
new_changes = '''            const changes = {
                "EUR/USD": "+0.44%",
                "USD/JPY": "-2.22%",
                "AUD/USD": "-0.16%",
                "GBP/USD": "+0.36%",
                "EUR/JPY": "-1.80%",
                "GBP/JPY": "-1.87%"
            };'''
if old_changes not in html:
    sys.exit("ERROR: ticker changes block not found verbatim")
html = html.replace(old_changes, new_changes)

with open(PATH, "w", encoding="utf-8") as f:
    f.write(html)

# ---- Validate: extract forexData and parse as JSON ----
s = html.find("const forexData = {")
s2 = html.find("{", s)
# find matching close
e = html.find("\n};", s) + len("\n};")
js_text = html[s2:e].rstrip()              # from '{' to '};'
# strip trailing '};' -> '}'  and convert to JSON by stripping nothing (keys already quoted)
json_text = js_text[:-2].rstrip()          # remove '};' -> ends with '}'
# It's already valid JSON syntax (double-quoted keys/strings). Validate:
try:
    data = json.loads(json_text)
except json.JSONDecodeError as ex:
    sys.exit(f"ERROR: forexData is not valid JSON: {ex}")

# Key order check
order = list(data.keys())
expected = ["EUR/USD", "USD/JPY", "AUD/USD", "GBP/USD", "EUR/JPY", "GBP/JPY"]
assert order == expected, f"Key order wrong: {order}"

# rrValue consistency check
import re as _re
for pair, d in data.items():
    rr = d["en"]["rr"]
    rv = d["en"]["rrValue"]
    if rr == "N/A":
        assert rv == 0, f"{pair}: N/A but rrValue={rv}"
        continue
    mobj = _re.match(r"1:([0-9]+\.[0-9]+)", rr)
    assert mobj, f"{pair}: bad rr {rr}"
    R = float(mobj.group(1))
    assert abs(round(R*25) - rv) <= 1, f"{pair}: rr {rr} -> round(R*25)={round(R*25)} != rrValue {rv}"
    assert rv == round(R*25) or abs(rv - round(R*25)) <= 0, f"{pair}: rrValue mismatch"

print("OK: index.html updated and forexData validated.")
print("Pair order:", order)
for pair, d in data.items():
    print(f"  {pair}: quote={d['quote']} bias={d['bias']}({d['biasType']}) rec={d['en']['recommendation']} rr={d['en']['rr']} rrValue={d['en']['rrValue']}")
