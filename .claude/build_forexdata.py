#!/usr/bin/env python3
"""Replace the forexData block + timestamps + ticker + macroDrivers + dataBasis strings
in docs/index.html with verified computed data (report compiled 14/08/2026 19:50 UTC, last ECB close 14/08/2026).
Data basis: Frankfurter/ECB daily series, 520 sessions 01/08/2024-14/08/2026; SMA50/200 and Fibonacci
computed from that series (see compute_indicators.py run of 14/08/2026).
Aborts on any structural mismatch. Validates forexData parses as JSON + key order + rrValue consistency."""
import re, json, sys

PATH = r"C:/Projetos/forex-report/docs/index.html"
TS = "14/08/2026 19:50 UTC"
OLD_TS = "14/08/2026 13:30 UTC"

with open(PATH, encoding="utf-8") as f:
    html = f.read()

# ---- New forexData block (literal string, matches existing indentation/style) ----
NEW_BLOCK = '''        const forexData = {
          "EUR/USD": {
                    "quote": "1.1567",
                    "bias": "BAIXA",
                    "biasType": "bear",
                    "pt": {
                              "fundamental": "O EUR/USD opera em 1,1567 no fechamento diário de 14/08/2026 (referência BCE, ~14:15 CET), avançando +0,29% e pressionando a Fib 61,8% (1,1582) por baixo — mas a estrutura técnica ainda prevalece sobre um cenário macro de dólar pressionado. A manutenção dividida do Fed em 9-3 a 3,50-3,75% em 29/07 e o CPI dos EUA de julho em +3,4% a.a. (divulgado em 12/08, abaixo dos 3,5% anteriores, núcleo 2,5%) — que reduziu as chances de alta em setembro, com o DXY recuando a ~99,8 — mantêm o dólar na defensiva, porém o par segue abaixo da SMA200 (1,1625) dentro do downtrend de 9 meses (1,1974 a 1,1340). O BCE a 2,25% (com aperto adicional para 2,50% precificado) limita o downside do euro. Os indicadores (SMA 50/200 e Fibonacci) são calculados a partir da série diária BCE/Frankfurter (520 pregões, 01/08/2024 a 14/08/2026). A recuperação estaca na confluência Fib 50% (1,1657) / SMA200 (1,1625) — zona de retomada de baixa.",
                              "trend": "Abaixo da SMA200 (1,1625) e acima da SMA50 (1,1465); o downtrend de médio prazo (1,1974 a 1,1340) segue intacto — o avanço atual é uma correção de baixa pressionando a Fib 61,8% (1,1582), rumo à confluência Fib 50% / SMA200.",
                              "support": "1,1476 (Fib 78,6%), com a mínima de 1,1340 abaixo.",
                              "resistance": "1,1582 (Fib 61,8%) na região atual; a confluência Fib 50% (1,1657) / SMA200 (1,1625) — a zona de venda — acima, e 1,1732 (Fib 38,2%) no topo.",
                              "priceAction": "Uma rejeição de baixa (pin bar / engolfo de baixa) na confluência 1,1625-1,1657 (SMA200 / Fib 50%), com fechamento diário retomando abaixo de 1,1582 (Fib 61,8%), retomaria a queda rumo a 1,1476-1,1450.",
                              "recommendation": "VENDA (SHORT) NA RETRAÇÃO",
                              "trigger": "Rejeição de baixa (pin bar / engolfo de baixa) em 1,1657 (confluência Fib 50% / SMA200), com fechamento diário sustentando abaixo de 1,1582.",
                              "stop": "1,1740 (Acima da Fib 38,2% em 1,1732).",
                              "target": "1,1450 (Logo abaixo da Fib 78,6% em 1,1476).",
                              "rr": "1:2.49",
                              "rrValue": 62,
                              "justification": "A estrutura técnica — abaixo da SMA200 e com a recuperação contida pela confluência Fib 50% / SMA200 — supera o macro de dólar pressionado, mantendo o viés de baixa ainda que o par tenha subido +0,29% hoje. Uma rejeição na confluência 1,1657/1,1625 oferece entrada vendida com stop protegido acima da Fib 38,2% e R/R de 1:2.49 rumo a 1,1450."
                    },
                    "en": {
                              "fundamental": "EUR/USD trades at 1.1567 on the 14/08/2026 daily close (ECB reference, ~14:15 CET), up +0.29% and pressing the 61.8% Fib (1.1582) from below — but the technical structure still overrides a pressured-dollar macro backdrop. The Fed's divided 9-3 hold at 3.50-3.75% on July 29 and July US CPI of +3.4% YoY (released Aug 12, down from 3.5%, core 2.5%) — which trimmed September hike odds, with DXY easing to ~99.8 — keep the dollar on the back foot, yet the pair remains below its 200-day SMA (1.1625) inside the 9-month 1.1974 to 1.1340 downtrend. The ECB at 2.25% (further tightening to 2.50% priced) caps the euro's downside. Indicators (SMA 50/200, Fibonacci) are computed from the ECB/Frankfurter daily series (520 sessions, 01/08/2024 to 14/08/2026). The bounce stalls at the 50% Fib (1.1657) / 200-day SMA (1.1625) confluence — the bear-resumption zone.",
                              "trend": "Below the 200-day SMA (1.1625) and above the 50-day SMA (1.1465); the medium-term downtrend (1.1974 to 1.1340) stays intact — the current push is a bear-market rally pressing the 61.8% Fib (1.1582), headed toward the 50% Fib / 200-day confluence.",
                              "support": "1.1476 (78.6% Fib), with the 1.1340 swing low beneath.",
                              "resistance": "1.1582 (61.8% Fib) at the current region; the 50% Fib (1.1657) / 200-day SMA (1.1625) confluence — the selling zone — above, and 1.1732 (38.2% Fib) on top.",
                              "priceAction": "A bearish rejection (pin bar / bearish engulfing) at the 1.1625-1.1657 confluence (200-day SMA / 50% Fib), with a daily close back below 1.1582 (61.8% Fib), would resume the drop toward 1.1476-1.1450.",
                              "recommendation": "SELL (SHORT) ON PULLBACK",
                              "trigger": "Bearish rejection (pin bar / bearish engulfing) at 1.1657 (50% Fib / 200-day SMA confluence), on a daily close holding below 1.1582.",
                              "stop": "1.1740 (Above the 38.2% Fib at 1.1732).",
                              "target": "1.1450 (Just below the 78.6% Fib at 1.1476).",
                              "rr": "1:2.49",
                              "rrValue": 62,
                              "justification": "The technical structure — below the 200-day SMA with the bounce capped by the 50% Fib / 200-day confluence — outweighs the pressured-USD macro, keeping the bias bearish even after today's +0.29% pop. A rejection at the 1.1657/1.1625 confluence offers a short with a structurally-protected stop above the 38.2% Fib and 1:2.49 R/R toward 1.1450."
                    }
          },
          "USD/JPY": {
                    "quote": "159.01",
                    "bias": "ALTA",
                    "biasType": "bull",
                    "pt": {
                              "fundamental": "O USD/JPY opera em 159,01 no fechamento diário de 14/08/2026 (referência BCE), recuando -0,20% enquanto o mercado digere a intervenção conjunta EUA-Japão de início de agosto (estimada em ~US$ 75 bi do lado japonês) — que levou o par da máxima de 163,91 (28/07) à região de 156,3-156,7 — e o iene já devolveu cerca de metade dos ganhos. Após a manutenção hawkish do BoJ a 1,0% em 31/07 (divisão 8-1, Takata a favor de 1,25%; alta em setembro sinalizada), o par reconquistou a SMA200 (158,09) e repousa sob a Fib 38,2% (159,60) do avanço de 152,63 a 163,91, com a SMA50 (161,16) acima. O CPI dos EUA em 3,4% (mais brando) pressiona o dólar, mas o amplo diferencial Fed (3,50-3,75%)-BoJ (1,0%) e a retomada do carry dominam; a estrutura segue de alta acima dos 200 dias. Indicadores calculados a partir da série diária BCE/Frankfurter (520 pregões, 01/08/2024 a 14/08/2026).",
                              "trend": "Acima da SMA200 (158,09) e abaixo da SMA50 (161,16) — o avanço de 152,63 a 163,91 foi restaurado após o mergulho de intervenção a ~156,3-156,7; a retração mira a confluência Fib 50% (158,27) / SMA200 (158,09).",
                              "support": "158,27 (Fib 50%) em confluência com a SMA200 de 158,09; 156,94 (Fib 61,8%) abaixo.",
                              "resistance": "159,60 (Fib 38,2%) na região atual, com a confluência SMA50 (161,16) / Fib 23,6% (161,25) acima; 163,91 (máxima) no topo.",
                              "priceAction": "Uma rejeição de alta (pin bar / engolfo bullish) na confluência 158,09-158,27 (SMA200 / Fib 50%), com fechamento diário sustentando acima de 159,00, retomaria a alta rumo a 161,16-162,50.",
                              "recommendation": "COMPRA (LONG) NA RETRAÇÃO",
                              "trigger": "Rejeição de alta (pin bar / engolfo bullish) em 158,10 (confluência Fib 50% / SMA200 reconquistada), com fechamento diário sustentando acima de 159,00.",
                              "stop": "156,80 (Abaixo da Fib 61,8% em 156,94).",
                              "target": "161,16 (Confluência SMA50 / Fib 23,6%).",
                              "rr": "1:2.35",
                              "rrValue": 59,
                              "justification": "A reconquista da SMA200, com o choque de intervenção a desfazer-se e o carry retomando, sustenta o viés de alta — os técnicos ganham do macro. Uma retração até a confluência Fib 50% / SMA200 reconquistada oferece entrada comprada com stop protegido abaixo da Fib 61,8% e R/R de 1:2.35 rumo à SMA50. Volatilidade residual de intervenção — dimensione adequadamente."
                    },
                    "en": {
                              "fundamental": "USD/JPY trades at 159.01 on the 14/08/2026 daily close (ECB reference), easing -0.20% as the market digests the early-August US-Japan joint intervention (estimated ~$75bn on the Japanese side) — which took the pair from the 163.91 high (Jul 28) to the 156.3-156.7 area — and the yen has already given back about half of its gains. After the BoJ's hawkish hold at 1.00% on July 31 (8-1 split, Takata seeking 1.25%; a September hike signaled), the pair has reclaimed its 200-day SMA (158.09) and sits below the 38.2% Fib (159.60) of the 152.63 to 163.91 advance, with the 50-day SMA (161.16) above. US CPI at 3.4% (softer) pressures the dollar, but the wide Fed (3.50-3.75%)-BoJ (1.00%) differential and the carry resumption dominate; structure stays bullish above the 200-day. Indicators computed from the ECB/Frankfurter daily series (520 sessions, 01/08/2024 to 14/08/2026).",
                              "trend": "Above the 200-day SMA (158.09) and below the 50-day SMA (161.16) — the 152.63 to 163.91 advance has been restored after the intervention dive to ~156.3-156.7; the pullback targets the 50% Fib (158.27) / 200-day SMA (158.09) confluence.",
                              "support": "158.27 (50% Fib) in confluence with the 158.09 200-day SMA; 156.94 (61.8% Fib) beneath.",
                              "resistance": "159.60 (38.2% Fib) at the current region, with the 50-day SMA (161.16) / 23.6% Fib (161.25) confluence above; 163.91 (swing high) on top.",
                              "priceAction": "A bullish rejection (pin bar / bullish engulfing) at the 158.09-158.27 confluence (200-day SMA / 50% Fib), with a daily close back above 159.00, would resume the up-move toward 161.16-162.50.",
                              "recommendation": "BUY (LONG) ON PULLBACK",
                              "trigger": "Bullish rejection (pin bar / bullish engulfing) at 158.10 (50% Fib / reclaimed 200-day SMA confluence), on a daily close back above 159.00.",
                              "stop": "156.80 (Below the 61.8% Fib at 156.94).",
                              "target": "161.16 (50-day SMA / 23.6% Fib confluence).",
                              "rr": "1:2.35",
                              "rrValue": 59,
                              "justification": "The reclaim of the 200-day SMA, with the intervention shock unwinding and carry resuming, sustains the bullish bias — technicals win over macro. A pullback to the 50% Fib / reclaimed 200-day SMA confluence offers a long with a protected stop below the 61.8% Fib and 1:2.35 R/R toward the 50-day SMA. Residual intervention volatility — size accordingly."
                    }
          },
          "AUD/USD": {
                    "quote": "0.7082",
                    "bias": "ALTA",
                    "biasType": "bull",
                    "pt": {
                              "fundamental": "O AUD/USD opera em 0,7082 no fechamento diário de 14/08/2026 (referência BCE), avançando +0,43%, rompendo a Fib 23,6% (0,7065) e marcando nova máxima de 30 dias — sustentando a tendência de alta acima da SMA200 (0,6925). O RBA manteve a taxa em 4,35% em 11/08 (padrão de espera, com cortes improváveis antes de 2027) e o petróleo firme (WTI ~US$ 82/bbl, +33% a/a) sustentam o australiano, enquanto o CPI dos EUA em 3,4% (mais brando), a manutenção dividida do Fed e o DXY ~99,8 limitam o dólar. O par opera acima das SMA50 (0,6990) e SMA200 (0,6925) dentro da tendência mais ampla de 0,6445 a 0,7257. Indicadores calculados a partir da série diária BCE/Frankfurter (520 pregões, 01/08/2024 a 14/08/2026). A estrutura segue de alta enquanto a SMA200 segurar.",
                              "trend": "Acima das SMA50 (0,6990) e SMA200 (0,6925) — rompeu a Fib 23,6% (0,7065) e mira a máxima de 0,7257 dentro da tendência ampla iniciada em 0,6445; retrações encontram a Fib 38,2% (0,6947).",
                              "support": "0,6947 (Fib 38,2%), com a Fib 23,6% (0,7065) recém-rompida atuando como suporte de curto prazo e a SMA200 (0,6925) abaixo.",
                              "resistance": "0,7257 (máxima de 9 meses do avanço de 0,6445), sem obstáculos fib intermediários acima da região atual.",
                              "priceAction": "Uma rejeição de alta (pin bar / engolfo bullish) na zona 0,6947-0,6960 (Fib 38,2%), com fechamento diário novamente acima de 0,7010, retomaria a alta rumo a 0,7150.",
                              "recommendation": "COMPRA (LONG) NA RETRAÇÃO",
                              "trigger": "Rejeição de alta (pin bar / engolfo bullish) em 0,6960 (zona Fib 38,2%), com fechamento diário sustentando acima de 0,7010.",
                              "stop": "0,6890 (Abaixo da SMA200 de 0,6925).",
                              "target": "0,7150 (Acima da Fib 23,6% em 0,7065).",
                              "rr": "1:2.71",
                              "rrValue": 68,
                              "justification": "A estrutura acima de ambas as SMAs com a Fib 23,6% recém-rompida, respaldada por um RBA a 4,35% em modo de espera e commodities firmes (WTI ~US$ 82) contra um Fed dividido e CPI brando, mantém o viés de alta. Uma retração até a Fib 38,2% oferece entrada comprada com stop protegido abaixo da SMA200 e R/R de 1:2.71 rumo a 0,7150."
                    },
                    "en": {
                              "fundamental": "AUD/USD trades at 0.7082 on the 14/08/2026 daily close (ECB reference), up +0.43%, breaking the 23.6% Fib (0.7065) and printing a fresh 30-day high — holding its uptrend above the 200-day SMA (0.6925). The RBA held at 4.35% on Aug 11 (holding pattern, cuts unlikely before 2027) and firm oil (WTI ~$82/bbl, +33% YoY) underpin the aussie, while US CPI at 3.4% (softer), the Fed's divided hold and DXY ~99.8 cap the dollar. The pair trades above the 50-day (0.6990) and 200-day (0.6925) SMAs within the broader 0.6445 to 0.7257 uptrend. Indicators computed from the ECB/Frankfurter daily series (520 sessions, 01/08/2024 to 14/08/2026). Structure stays bullish while the 200-day holds.",
                              "trend": "Above both the 50-day (0.6990) and 200-day (0.6925) SMAs — it has broken the 23.6% Fib (0.7065) and eyes the 0.7257 high within the broad uptrend from 0.6445; pullbacks meet the 38.2% Fib (0.6947).",
                              "support": "0.6947 (38.2% Fib), with the freshly-broken 23.6% Fib (0.7065) acting as near-term support and the 200-day SMA (0.6925) beneath.",
                              "resistance": "0.7257 (9-month high of the 0.6445 advance), with no intermediate Fib obstacles above the current region.",
                              "priceAction": "A bullish rejection (pin bar / bullish engulfing) at the 0.6947-0.6960 zone (38.2% Fib), with a daily close back above 0.7010, would resume the uptrend toward 0.7150.",
                              "recommendation": "BUY (LONG) ON PULLBACK",
                              "trigger": "Bullish rejection (pin bar / bullish engulfing) at 0.6960 (38.2% Fib zone), on a daily close back above 0.7010.",
                              "stop": "0.6890 (Below the 0.6925 200-day SMA).",
                              "target": "0.7150 (Above the 23.6% Fib at 0.7065).",
                              "rr": "1:2.71",
                              "rrValue": 68,
                              "justification": "The structure above both SMAs with the 23.6% Fib freshly broken, backed by an RBA on hold at 4.35% and firm commodities (WTI ~$82) against a divided Fed and soft CPI, keeps the bias bullish. A pullback to the 38.2% Fib offers a long with a protected stop below the 200-day SMA and 1:2.71 R/R toward 0.7150."
                    }
          },
          "GBP/USD": {
                    "quote": "1.3537",
                    "bias": "ALTA",
                    "biasType": "bull",
                    "pt": {
                              "fundamental": "O GBP/USD opera em 1,3537 no fechamento diário de 14/08/2026 (referência BCE), avançando +0,33% e rompendo por margem estreita a Fib 38,2% (1,3528), sustentando acima de ambas as SMAs. A manutenção do BoE a 3,75% em 30/07 (divisão 6-3, três dissidentes a favor de 4,00%; inflação a 2,6%) sustenta a libra, enquanto o CPI dos EUA em 3,4% (mais brando) e a manutenção dividida do Fed (DXY ~99,8) pressionam o dólar. Dentro do uptrend de 1,3062 a 1,3817, o próximo obstáculo é a Fib 23,6% (1,3639), acima das SMA50 (1,3369) e SMA200 (1,3404). Indicadores calculados a partir da série diária BCE/Frankfurter (520 pregões, 01/08/2024 a 14/08/2026). A estrutura segue de alta enquanto a SMA200 segurar.",
                              "trend": "Acima das SMA50 (1,3369) e SMA200 (1,3404); rompeu por margem estreita a Fib 38,2% (1,3528) dentro do uptrend de 1,3062 a 1,3817, próximo obstáculo a Fib 23,6% (1,3639).",
                              "support": "1,3439 (Fib 50%), com a Fib 38,2% (1,3528) recém-rompida atuando como suporte de curto prazo e a SMA200 (1,3404) abaixo.",
                              "resistance": "1,3639 (Fib 23,6%), com a máxima de 1,3817 acima.",
                              "priceAction": "Uma rejeição de alta (pin bar / engolfo bullish) na zona 1,3439-1,3404 (Fib 50% / SMA200), com fechamento diário novamente acima de 1,3470, retomaria a alta rumo a 1,3528-1,3625.",
                              "recommendation": "COMPRA (LONG) NA RETRAÇÃO",
                              "trigger": "Rejeição de alta (pin bar / engolfo bullish) em 1,3420 (confluência Fib 50% / SMA200), com fechamento diário sustentando acima de 1,3470.",
                              "stop": "1,3340 (Abaixo da Fib 61,8% em 1,3350).",
                              "target": "1,3625 (Logo abaixo da Fib 23,6% em 1,3639).",
                              "rr": "1:2.56",
                              "rrValue": 64,
                              "justification": "A estrutura acima de ambas as SMAs com a Fib 38,2% recém-rompida, reforçada por um BoE hawkish a 3,75% (divisão 6-3) contra um Fed dividido e CPI brando, mantém o viés de alta. Uma retração até a confluência Fib 50% / SMA200 oferece entrada comprada com stop protegido abaixo da Fib 61,8% e R/R de 1:2.56 rumo a 1,3625."
                    },
                    "en": {
                              "fundamental": "GBP/USD trades at 1.3537 on the 14/08/2026 daily close (ECB reference), up +0.33% and narrowly breaking the 38.2% Fib (1.3528), holding above both SMAs. The BoE's hold at 3.75% on July 30 (6-3 split, three dissents for 4.00%; inflation at 2.6%) supports sterling, while US CPI at 3.4% (softer) and the Fed's divided hold (DXY ~99.8) pressure the dollar. Within the 1.3062 to 1.3817 uptrend, the next hurdle is the 23.6% Fib (1.3639), above the 50-day (1.3369) and 200-day (1.3404) SMAs. Indicators computed from the ECB/Frankfurter daily series (520 sessions, 01/08/2024 to 14/08/2026). Structure stays bullish while the 200-day holds.",
                              "trend": "Above both the 50-day (1.3369) and 200-day (1.3404) SMAs; it has narrowly broken the 38.2% Fib (1.3528) within the 1.3062 to 1.3817 uptrend, next hurdle the 23.6% Fib (1.3639).",
                              "support": "1.3439 (50% Fib), with the freshly-broken 38.2% Fib (1.3528) acting as near-term support and the 200-day SMA (1.3404) beneath.",
                              "resistance": "1.3639 (23.6% Fib), with the 1.3817 swing high above.",
                              "priceAction": "A bullish rejection (pin bar / bullish engulfing) at the 1.3439-1.3404 zone (50% Fib / 200-day SMA), with a daily close back above 1.3470, would resume the uptrend toward 1.3528-1.3625.",
                              "recommendation": "BUY (LONG) ON PULLBACK",
                              "trigger": "Bullish rejection (pin bar / bullish engulfing) at 1.3420 (50% Fib / 200-day SMA confluence), on a daily close back above 1.3470.",
                              "stop": "1.3340 (Below the 61.8% Fib at 1.3350).",
                              "target": "1.3625 (Just below the 23.6% Fib at 1.3639).",
                              "rr": "1:2.56",
                              "rrValue": 64,
                              "justification": "The structure above both SMAs with the 38.2% Fib freshly broken, reinforced by a hawkish BoE at 3.75% (6-3 split) against a divided Fed and soft CPI, keeps the bias bullish. A pullback to the 50% Fib / 200-day SMA confluence offers a long with a protected stop below the 61.8% Fib and 1:2.56 R/R toward 1.3625."
                    }
          },
          "EUR/JPY": {
                    "quote": "183.93",
                    "bias": "ALTA",
                    "biasType": "bull",
                    "pt": {
                              "fundamental": "O EUR/JPY opera em 183,93 no fechamento diário de 14/08/2026 (referência BCE), subindo +0,08% enquanto o choque de intervenção no iene do início de agosto se desfaz e o carry trade retoma. Após o mergulho pós-intervenção até a região da Fib 61,8% (181,09), o par reconquistou a SMA200 (183,74) — agora por ~19 pips — e repousa entre a Fib 38,2% (183,62) e a SMA50 (184,75), dentro do avanço de 176,99 a 187,73. O diferencial de carry BCE (2,25%)-BoJ (1,0%) segue amplo, mas a reconquista estreita da SMA200 não oferece gatilho limpo. Indicadores calculados a partir da série diária BCE/Frankfurter (520 pregões, 01/08/2024 a 14/08/2026).",
                              "trend": "Acima da SMA200 (183,74) por margem estreita e abaixo da SMA50 (184,75) — o avanço de 176,99 a 187,73 foi restaurado em estrutura, mas o gatilho direcional não é limpo.",
                              "support": "182,36 (Fib 50%), com a SMA200 de 183,74 logo acima.",
                              "resistance": "184,75 (SMA50) em confluência com a Fib 23,6% (185,19); 187,73 (máxima) acima.",
                              "priceAction": "Sem gatilho de price-action acionável: a reconquista da SMA200 por margem estreita não oferece entrada de risco-retorno limpa. Aguardar fechamento diário decisivo acima de 185,19 (rompimento) ou rejeição em 182,36 (retração).",
                              "recommendation": "AGUARDAR OUTRO GATILHO",
                              "trigger": "Nenhum gatilho acionável — reconquista da SMA200 (183,74) por margem estreita. Aguardar rompimento decisivo de 185,19 (SMA50 / Fib 23,6%) com follow-through, ou retração até 182,36 (Fib 50%).",
                              "stop": "N/A (sem operação).",
                              "target": "N/A (sem operação).",
                              "rr": "N/A",
                              "rrValue": 0,
                              "justification": "A reconquista da SMA200 (183,74) por apenas ~19 pips após o choque de intervenção não oferece setup direcional limpo: um longo em retração até a Fib 50% (182,36) estaca em R/R ~1:1,6 rumo à SMA50, e um longo no rompimento de 185,19 estaca em R/R ~1:1,4 rumo à máxima de 187,73, com alvos estendidos bloqueados por essa mesma máxima. Técnicos ganham — aguardar rompimento decisivo ou retração mais profunda para destravar R/R ≥ 1:2."
                    },
                    "en": {
                              "fundamental": "EUR/JPY trades at 183.93 on the 14/08/2026 daily close (ECB reference), rising +0.08% as the early-August yen intervention shock unwinds and carry trade resumes. After the post-intervention dive to the 61.8% Fib region (181.09), the pair has reclaimed its 200-day SMA (183.74) — now by ~19 pips — and sits between the 38.2% Fib (183.62) and the 50-day SMA (184.75), within the 176.99 to 187.73 advance. The ECB (2.25%)-BoJ (1.00%) carry gap remains wide, but the narrow 200-day reclaim offers no clean trigger. Indicators computed from the ECB/Frankfurter daily series (520 sessions, 01/08/2024 to 14/08/2026).",
                              "trend": "Above the 200-day SMA (183.74) by a narrow margin and below the 50-day SMA (184.75) — the 176.99 to 187.73 advance has been restored in structure, but the directional trigger is not clean.",
                              "support": "182.36 (50% Fib), with the 183.74 200-day SMA just above.",
                              "resistance": "184.75 (50-day SMA) in confluence with the 23.6% Fib (185.19); 187.73 (swing high) above.",
                              "priceAction": "No actionable price-action trigger: the narrow 200-day reclaim offers no clean risk-reward entry. Wait for a decisive daily close above 185.19 (breakout) or a rejection at 182.36 (pullback).",
                              "recommendation": "WAIT FOR ANOTHER TRIGGER",
                              "trigger": "No actionable trigger — narrow reclaim of the 200-day SMA (183.74). Wait for a decisive breakout of 185.19 (50-day SMA / 23.6% Fib) with follow-through, or a pullback to 182.36 (50% Fib).",
                              "stop": "N/A (no trade).",
                              "target": "N/A (no trade).",
                              "rr": "N/A",
                              "rrValue": 0,
                              "justification": "The 200-day SMA (183.74) reclaim by only ~19 pips after the intervention shock offers no clean directional setup: a pullback long to the 50% Fib (182.36) caps at ~1:1.6 R/R to the 50-day SMA, and a breakout long above 185.19 caps at ~1:1.4 R/R to the 187.73 swing high, with extension targets blocked by that same high. Technicals win — wait for a decisive breakout or a deeper pullback to unlock R/R of at least 1:2."
                    }
          },
          "GBP/JPY": {
                    "quote": "215.24",
                    "bias": "ALTA",
                    "biasType": "bull",
                    "pt": {
                              "fundamental": "O GBP/JPY opera em 215,24 no fechamento diário de 14/08/2026 (referência BCE), subindo +0,13% com o choque de intervenção no iene a desfazer-se e o carry a retomar. O par reconquistou decisivamente a SMA200 (211,89) e repousa colado sob a SMA50 (215,45), sobre a Fib 23,6% (214,83) do avanço de 200,87 a 219,14. O amplo diferencial de carry BoE (3,75%)-BoJ (1,0%) e a retomada do carry dominam; a estrutura segue de alta acima dos 200 dias. Indicadores calculados a partir da série diária BCE/Frankfurter (520 pregões, 01/08/2024 a 14/08/2026).",
                              "trend": "Acima da SMA200 (211,89) e colado sob a SMA50 (215,45) — o avanço de 200,87 a 219,14 foi restaurado; rompimento da SMA50 miraria a máxima de 219,14.",
                              "support": "212,16 (Fib 38,2%), com a SMA200 de 211,89 abaixo.",
                              "resistance": "215,45 (SMA50) em confluência com a Fib 23,6% (214,83); 219,14 (máxima) acima.",
                              "priceAction": "Um fechamento diário decisivo acima de 215,50 (SMA50 / Fib 23,6%), com follow-through, retomaria a alta rumo à máxima de 219,14.",
                              "recommendation": "COMPRA (LONG) NO ROMPIMENTO",
                              "trigger": "Fechamento diário acima de 215,50 (acima da SMA50 em 215,45 e da Fib 23,6% em 214,83), com follow-through.",
                              "stop": "213,90 (Abaixo da Fib 23,6% em 214,83).",
                              "target": "219,00 (Logo abaixo da máxima de 219,14).",
                              "rr": "1:2.19",
                              "rrValue": 55,
                              "justification": "A reconquista decisiva da SMA200, com o choque de intervenção a desfazer-se e o carry retomando, inverte o viés para alta — os técnicos ganham do macro. Um rompimento da confluência SMA50 / Fib 23,6% oferece entrada comprada com stop protegido abaixo da Fib 23,6% e R/R de 1:2.19 rumo à máxima de 219,14 — caminho limpo, sem S/R intermediária bloqueando. Volatilidade residual de intervenção — dimensione adequadamente."
                    },
                    "en": {
                              "fundamental": "GBP/JPY trades at 215.24 on the 14/08/2026 daily close (ECB reference), up +0.13% with the yen intervention shock unwinding and carry resuming. The pair has decisively reclaimed its 200-day SMA (211.89) and sits glued just below the 50-day SMA (215.45), on the 23.6% Fib (214.83) of the 200.87 to 219.14 advance. The wide BoE (3.75%)-BoJ (1.00%) carry gap and the carry resumption dominate; structure stays bullish above the 200-day. Indicators computed from the ECB/Frankfurter daily series (520 sessions, 01/08/2024 to 14/08/2026).",
                              "trend": "Above the 200-day SMA (211.89) and glued just below the 50-day SMA (215.45) — the 200.87 to 219.14 advance has been restored; a 50-day SMA breakout would target the 219.14 swing high.",
                              "support": "212.16 (38.2% Fib), with the 211.89 200-day SMA beneath.",
                              "resistance": "215.45 (50-day SMA) in confluence with the 23.6% Fib (214.83); 219.14 (swing high) above.",
                              "priceAction": "A decisive daily close above 215.50 (50-day SMA / 23.6% Fib), with follow-through, would resume the up-move toward the 219.14 swing high.",
                              "recommendation": "BUY (LONG) ON BREAKOUT",
                              "trigger": "Daily close above 215.50 (above the 50-day SMA at 215.45 and the 23.6% Fib at 214.83), with follow-through.",
                              "stop": "213.90 (Below the 23.6% Fib at 214.83).",
                              "target": "219.00 (Just below the 219.14 swing high).",
                              "rr": "1:2.19",
                              "rrValue": 55,
                              "justification": "The decisive reclaim of the 200-day SMA, with the intervention shock unwinding and carry resuming, flips the bias to bullish — technicals win over macro. A breakout of the 50-day SMA / 23.6% Fib confluence offers a long with a protected stop below the 23.6% Fib and 1:2.19 R/R toward the 219.14 swing high — clean path with no intermediate S/R blocking. Residual intervention volatility — size accordingly."
                    }
          }
};'''

# ---- Replace forexData block ----
start = html.find("        const forexData = {")
if start == -1:
    sys.exit("ERROR: forexData start not found")
end_marker = "\n};"
end = html.find(end_marker, start)
if end == -1:
    sys.exit("ERROR: forexData end not found")
end += len(end_marker)

old_block = html[start:end]
for key in ["EUR/USD", "USD/JPY", "AUD/USD", "GBP/USD", "EUR/JPY", "GBP/JPY"]:
    if old_block.count('"' + key + '"') != 1:
        sys.exit(f"ERROR: pair key {key} not found exactly once in old forexData block")

html = html[:start] + NEW_BLOCK + html[end:]

# ---- Replace timestamps (3 spots) ----
# Spot 1: #generationTime badge
m = re.search(r'(id="generationTime"[^>]*>Reports generated on: )[^<]*(</p>)', html)
if not m:
    sys.exit("ERROR: #generationTime badge not found")
html = html[:m.start()] + m.group(1) + TS + m.group(2) + html[m.end():]

# Spots 2 & 3: the two generatedAt strings still holding OLD_TS
count = html.count(OLD_TS)
if count != 2:
    sys.exit(f"ERROR: expected 2 remaining old timestamp occurrences, found {count}")
html = html.replace(OLD_TS, TS)

# ---- Replace dailyChanges (ticker) block ----
old_changes = '''        const dailyChanges = {
            "EUR/USD": "-0.09%",
            "USD/JPY": "+0.15%",
            "AUD/USD": "-0.28%",
            "GBP/USD": "-0.25%",
            "EUR/JPY": "+0.06%",
            "GBP/JPY": "-0.10%"
        };'''
new_changes = '''        const dailyChanges = {
            "EUR/USD": "+0.29%",
            "USD/JPY": "-0.20%",
            "AUD/USD": "+0.43%",
            "GBP/USD": "+0.33%",
            "EUR/JPY": "+0.08%",
            "GBP/JPY": "+0.13%"
        };'''
if old_changes not in html:
    sys.exit("ERROR: dailyChanges block not found verbatim")
html = html.replace(old_changes, new_changes)

# ---- Replace macroDrivers block ----
old_drivers = '''        const macroDrivers = {
            "EUR/USD": {
                en: ["Fed hold 3.50-3.75%", "CPI 3.4%", "ECB 2.25%"],
                pt: ["Fed 3,50-3,75%", "CPI 3,4%", "BCE 2,25%"]
            },
            "USD/JPY": {
                en: ["BoJ 1.00% hawkish", "Carry resumed", "Fed–BoJ gap"],
                pt: ["BoJ 1,0% hawkish", "Carry retomado", "Diferencial Fed–BoJ"]
            },
            "AUD/USD": {
                en: ["RBA 4.35%", "Brent $87", "Fed dovish"],
                pt: ["RBA 4,35%", "Brent $87", "Fed dovish"]
            },
            "GBP/USD": {
                en: ["BoE 3.75% 6-3", "CPI 3.4%", "Fed dovish"],
                pt: ["BoE 3,75% 6-3", "CPI 3,4%", "Fed dovish"]
            },
            "EUR/JPY": {
                en: ["BoJ 1.00% hawkish", "Carry resumed", "ECB–BoJ gap"],
                pt: ["BoJ 1,0% hawkish", "Carry retomado", "Diferencial BCE–BoJ"]
            },
            "GBP/JPY": {
                en: ["BoJ 1.00% hawkish", "Carry resumed", "BoE–BoJ gap"],
                pt: ["BoJ 1,0% hawkish", "Carry retomado", "Diferencial BoE–BoJ"]
            }
        };'''
new_drivers = '''        const macroDrivers = {
            "EUR/USD": {
                en: ["Fed hold 3.50-3.75%", "CPI 3.4%", "ECB 2.25%"],
                pt: ["Fed 3,50-3,75%", "CPI 3,4%", "BCE 2,25%"]
            },
            "USD/JPY": {
                en: ["BoJ 1.00% hawkish", "Intervention fade", "Fed–BoJ gap"],
                pt: ["BoJ 1,0% hawkish", "Intervenção esvaindo", "Diferencial Fed–BoJ"]
            },
            "AUD/USD": {
                en: ["RBA 4.35%", "WTI $82", "Fed dovish"],
                pt: ["RBA 4,35%", "WTI $82", "Fed dovish"]
            },
            "GBP/USD": {
                en: ["BoE 3.75% 6-3", "CPI 2.6%", "Fed dovish"],
                pt: ["BoE 3,75% 6-3", "IPC 2,6%", "Fed dovish"]
            },
            "EUR/JPY": {
                en: ["BoJ 1.00% hawkish", "Intervention fade", "ECB–BoJ gap"],
                pt: ["BoJ 1,0% hawkish", "Intervenção esvaindo", "Diferencial BCE–BoJ"]
            },
            "GBP/JPY": {
                en: ["BoJ 1.00% hawkish", "Intervention fade", "BoE–BoJ gap"],
                pt: ["BoJ 1,0% hawkish", "Intervenção esvaindo", "Diferencial BoE–BoJ"]
            }
        };'''
if old_drivers not in html:
    sys.exit("ERROR: macroDrivers block not found verbatim")
html = html.replace(old_drivers, new_drivers)

# ---- Replace the two dataBasis i18n strings ----
old_basis_en = 'dataBasis: "Data basis: ECB/Frankfurter reference rates · SMA50/200 & Fibonacci computed · 519 daily sessions (01/08/2024–13/08/2026).",'
new_basis_en = 'dataBasis: "Data basis: ECB/Frankfurter reference rates · SMA50/200 & Fibonacci computed · 520 daily sessions (01/08/2024–14/08/2026).",'
if html.count(old_basis_en) != 1:
    sys.exit(f"ERROR: EN dataBasis not found exactly once ({html.count(old_basis_en)})")
html = html.replace(old_basis_en, new_basis_en)

old_basis_pt = 'dataBasis: "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200 e Fibonacci calculados · 519 pregões (01/08/2024 a 13/08/2026).",'
new_basis_pt = 'dataBasis: "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200 e Fibonacci calculados · 520 pregões (01/08/2024 a 14/08/2026).",'
if html.count(old_basis_pt) != 1:
    sys.exit(f"ERROR: PT dataBasis not found exactly once ({html.count(old_basis_pt)})")
html = html.replace(old_basis_pt, new_basis_pt)

with open(PATH, "w", encoding="utf-8") as f:
    f.write(html)

# ---- Validate: extract forexData and parse as JSON ----
s = html.find("const forexData = {")
s2 = html.find("{", s)
e = html.find("\n};", s) + len("\n};")
js_text = html[s2:e].rstrip()
json_text = js_text[:-1].rstrip()  # remove trailing ';' -> leaves '{ ... }'
try:
    data = json.loads(json_text)
except json.JSONDecodeError as ex:
    sys.exit(f"ERROR: forexData is not valid JSON: {ex}")

order = list(data.keys())
expected = ["EUR/USD", "USD/JPY", "AUD/USD", "GBP/USD", "EUR/JPY", "GBP/JPY"]
assert order == expected, f"Key order wrong: {order}"

# rrValue consistency check
for pair, d in data.items():
    rr = d["en"]["rr"]
    rv = d["en"]["rrValue"]
    if rr == "N/A":
        assert rv == 0, f"{pair}: N/A but rrValue={rv}"
        continue
    mobj = re.match(r"1:([0-9]+\.[0-9]+)", rr)
    assert mobj, f"{pair}: bad rr {rr}"
    R = float(mobj.group(1))
    assert rv == round(R*25), f"{pair}: rr {rr} -> round(R*25)={round(R*25)} != rrValue {rv}"

# Bias consistency: recommendation verdict keywords
for pair, d in data.items():
    rec = d["en"]["recommendation"]
    assert any(k in rec for k in ("WAIT", "SELL", "BUY")), f"{pair}: recommendation missing verdict keyword"
    recpt = d["pt"]["recommendation"]
    assert any(k in recpt for k in ("AGUARDAR", "VENDA", "COMPRA")), f"{pair}: PT recommendation missing verdict keyword"

print("OK: index.html updated and forexData validated.")
print("Pair order:", order)
for pair, d in data.items():
    print(f"  {pair}: quote={d['quote']} bias={d['bias']}({d['biasType']}) rec={d['en']['recommendation']} rr={d['en']['rr']} rrValue={d['en']['rrValue']}")
