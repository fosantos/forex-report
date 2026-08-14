#!/usr/bin/env python3
"""Replace the forexData block + timestamps + ticker + macroDrivers + dataBasis strings
in docs/index.html with verified computed data (report compiled 14/08/2026, last ECB close 13/08/2026).
Aborts on any structural mismatch. Validates forexData parses as JSON + key order + rrValue consistency."""
import re, json, sys

PATH = r"C:/Projetos/forex-report/docs/index.html"
TS = "14/08/2026 13:30 UTC"
OLD_TS = "11/08/2026 13:30 UTC"

with open(PATH, encoding="utf-8") as f:
    html = f.read()

# ---- New forexData block (literal string, matches existing indentation/style) ----
NEW_BLOCK = '''        const forexData = {
          "EUR/USD": {
                    "quote": "1.1534",
                    "bias": "BAIXA",
                    "biasType": "bear",
                    "pt": {
                              "fundamental": "O EUR/USD opera em 1,1534 no fechamento diário de 13/08/2026 (referência BCE, ~14:15 CET), com a estrutura técnica prevalecendo sobre um cenário macro de dólar pressionado. A manutenção dividida do Fed em 9-3 a 3,50-3,75% em 29/07 e o CPI dos EUA de julho em +3,4% a.a. (divulgado em 12/08, abaixo dos 3,5% anteriores, núcleo 2,5%) — que reduziu as chances de alta em setembro — mantêm o dólar na defensiva, mas o par segue abaixo da SMA200 (1,1625) dentro do downtrend de 9 meses (1,1974 a 1,1340). O BCE a 2,25% (com alta para 2,50% precificada em setembro) limita o downside do euro. Os indicadores (SMA 50/200 e Fibonacci) são calculados a partir da série diária BCE/Frankfurter (519 pregões, 01/08/2024 a 13/08/2026). A recuperação estaca na confluência Fib 50% (1,1657) / SMA200 (1,1625) — zona de retomada de baixa.",
                              "trend": "Abaixo da SMA200 (1,1625) e acima da SMA50 (1,1466); o downtrend de médio prazo (1,1974 a 1,1340) segue intacto, com o movimento atual sendo uma correção de baixa rumo à confluência Fib 50% / SMA200.",
                              "support": "1,1476 (Fib 78,6%), com a mínima de 1,1340 abaixo.",
                              "resistance": "1,1657 (Fib 50%) em confluência com a SMA200 de 1,1625; 1,1732 (Fib 38,2%) acima.",
                              "priceAction": "Uma rejeição de baixa (pin bar / engolfo de baixa) na confluência 1,1625-1,1657 (SMA200 / Fib 50%), com fechamento diário retomando abaixo de 1,1582 (Fib 61,8%), retomaria a queda rumo a 1,1476-1,1450.",
                              "recommendation": "VENDA (SHORT) NA RETRAÇÃO",
                              "trigger": "Rejeição de baixa (pin bar / engolfo de baixa) em 1,1657 (confluência Fib 50% / SMA200), com fechamento diário sustentando abaixo de 1,1582.",
                              "stop": "1,1740 (Acima da Fib 38,2% em 1,1732).",
                              "target": "1,1450 (Logo abaixo da Fib 78,6% em 1,1476).",
                              "rr": "1:2.49",
                              "rrValue": 62,
                              "justification": "A estrutura técnica — abaixo da SMA200 e falhando na Fib 50% — supera o macro de dólar pressionado, mantendo o viés de baixa. Uma rejeição na confluência 1,1657/1,1625 (Fib 50% / SMA200) oferece entrada vendida com stop protegido acima da Fib 38,2% e R/R de 1:2.49 rumo a 1,1450."
                    },
                    "en": {
                              "fundamental": "EUR/USD trades at 1.1534 on the 13/08/2026 daily close (ECB reference, ~14:15 CET), with the technical structure overriding a pressured-dollar macro backdrop. The Fed's divided 9-3 hold at 3.50-3.75% on July 29 and July US CPI of +3.4% YoY (released Aug 12, down from 3.5%, core 2.5%) — which trimmed September hike odds — keep the dollar on the back foot, but the pair remains below its 200-day SMA (1.1625) inside the 9-month 1.1974 to 1.1340 downtrend. The ECB at 2.25% (a September hike to 2.50% is priced) caps the euro's downside. Indicators (SMA 50/200, Fibonacci) are computed from the ECB/Frankfurter daily series (519 sessions, 01/08/2024 to 13/08/2026). The bounce stalls at the 50% Fib (1.1657) / 200-day SMA (1.1625) confluence — the bear-resumption zone.",
                              "trend": "Below the 200-day SMA (1.1625) and above the 50-day SMA (1.1466); the medium-term downtrend (1.1974 to 1.1340) stays intact, with the bounce a bear-market rally into the 50% Fib / 200-day confluence.",
                              "support": "1.1476 (78.6% Fib), with the 1.1340 swing low beneath.",
                              "resistance": "1.1657 (50% Fib) in confluence with the 1.1625 200-day SMA; 1.1732 (38.2% Fib) above.",
                              "priceAction": "A bearish rejection (pin bar / bearish engulfing) at the 1.1625-1.1657 confluence (200-day SMA / 50% Fib), with a daily close back below 1.1582 (61.8% Fib), would resume the drop toward 1.1476-1.1450.",
                              "recommendation": "SELL (SHORT) ON PULLBACK",
                              "trigger": "Bearish rejection (pin bar / bearish engulfing) at 1.1657 (50% Fib / 200-day SMA confluence), on a daily close holding below 1.1582.",
                              "stop": "1.1740 (Above the 38.2% Fib at 1.1732).",
                              "target": "1.1450 (Just below the 78.6% Fib at 1.1476).",
                              "rr": "1:2.49",
                              "rrValue": 62,
                              "justification": "The technical structure — below the 200-day SMA and failing at the 50% Fib — outweighs the pressured-USD macro, keeping the bias bearish. A rejection at the 1.1657/1.1625 confluence (50% Fib / 200-day SMA) offers a short with a structurally-protected stop above the 38.2% Fib and 1:2.49 R/R toward 1.1450."
                    }
          },
          "USD/JPY": {
                    "quote": "159.33",
                    "bias": "ALTA",
                    "biasType": "bull",
                    "pt": {
                              "fundamental": "O USD/JPY opera em 159,33 no fechamento diário de 13/08/2026 (referência BCE), recuperando +0,15% enquanto o choque de intervenção conjunta EUA-Japão do início de agosto se desfaz e o carry trade retoma. Após a manutenção hawkish do BoJ a 1,0% em 31/07 (divisão 8-1, Takata a favor de 1,25%; alta em setembro sinalizada) e a intervenção que levou o par até ~152,63, o USD/JPY reconquistou a SMA200 (158,06) e repousa sob a SMA50 (161,18), sobre a Fib 38,2% (159,60) do avanço de 152,63 a 163,91. O CPI dos EUA em 3,4% (mais brando) pressiona o dólar, mas o amplo diferencial Fed (3,50-3,75%)-BoJ (1,0%) e a retomada do carry dominam; a estrutura voltou a ser de alta acima dos 200 dias. Indicadores calculados a partir da série diária BCE/Frankfurter (519 pregões).",
                              "trend": "Acima da SMA200 (158,06) e abaixo da SMA50 (161,18) — o avanço de 152,63 a 163,91 foi restaurado após o mergulho de intervenção; a retração mira a confluência Fib 50% (158,27) / SMA200 (158,06).",
                              "support": "158,27 (Fib 50%) em confluência com a SMA200 de 158,06; 156,94 (Fib 61,8%) abaixo.",
                              "resistance": "161,25 (Fib 23,6%) em confluência com a SMA50 de 161,18; 163,91 (máxima) acima.",
                              "priceAction": "Uma rejeição de alta (pin bar / engolfo bullish) na confluência 158,06-158,27 (SMA200 / Fib 50%), com fechamento diário sustentando acima de 159,00, retomaria a alta rumo a 161,18-162,50.",
                              "recommendation": "COMPRA (LONG) NA RETRAÇÃO",
                              "trigger": "Rejeição de alta (pin bar / engolfo bullish) em 158,10 (confluência Fib 50% / SMA200 reconquistada), com fechamento diário sustentando acima de 159,00.",
                              "stop": "156,80 (Abaixo da Fib 61,8% em 156,94).",
                              "target": "161,18 (Confluência SMA50 / Fib 23,6%).",
                              "rr": "1:2.37",
                              "rrValue": 59,
                              "justification": "A reconquista da SMA200, com o choque de intervenção a desfazer-se e o carry retomando, inverte o viés para alta — os técnicos ganham do macro. Uma retração até a confluência Fib 50% / SMA200 reconquistada oferece entrada comprada com stop protegido abaixo da Fib 61,8% e R/R de 1:2.37 rumo à SMA50. Volatilidade residual de intervenção — dimensione adequadamente."
                    },
                    "en": {
                              "fundamental": "USD/JPY trades at 159.33 on the 13/08/2026 daily close (ECB reference), recovering +0.15% as the early-August US-Japan joint intervention shock unwinds and carry trade resumes. After the BoJ's hawkish hold at 1.00% on July 31 (8-1 split, Takata seeking 1.25%; a September hike signaled) and the intervention that drove the pair as low as ~152.63, USD/JPY has reclaimed its 200-day SMA (158.06) and sits below the 50-day SMA (161.18), on the 38.2% Fib (159.60) of the 152.63 to 163.91 advance. US CPI at 3.4% (softer) pressures the dollar, but the wide Fed (3.50-3.75%)-BoJ (1.00%) differential and the carry resumption dominate; structure is back to bullish above the 200-day. Indicators computed from the ECB/Frankfurter daily series (519 sessions).",
                              "trend": "Above the 200-day SMA (158.06) and below the 50-day SMA (161.18) — the 152.63 to 163.91 advance has been restored after the intervention dive; the pullback targets the 50% Fib (158.27) / 200-day SMA (158.06) confluence.",
                              "support": "158.27 (50% Fib) in confluence with the 158.06 200-day SMA; 156.94 (61.8% Fib) beneath.",
                              "resistance": "161.25 (23.6% Fib) in confluence with the 161.18 50-day SMA; 163.91 (swing high) above.",
                              "priceAction": "A bullish rejection (pin bar / bullish engulfing) at the 158.06-158.27 confluence (200-day SMA / 50% Fib), with a daily close back above 159.00, would resume the up-move toward 161.18-162.50.",
                              "recommendation": "BUY (LONG) ON PULLBACK",
                              "trigger": "Bullish rejection (pin bar / bullish engulfing) at 158.10 (50% Fib / reclaimed 200-day SMA confluence), on a daily close back above 159.00.",
                              "stop": "156.80 (Below the 61.8% Fib at 156.94).",
                              "target": "161.18 (50-day SMA / 23.6% Fib confluence).",
                              "rr": "1:2.37",
                              "rrValue": 59,
                              "justification": "The reclaim of the 200-day SMA, with the intervention shock unwinding and carry resuming, flips the bias to bullish — technicals win over macro. A pullback to the 50% Fib / reclaimed 200-day SMA confluence offers a long with a protected stop below the 61.8% Fib and 1:2.37 R/R toward the 50-day SMA. Residual intervention volatility — size accordingly."
                    }
          },
          "AUD/USD": {
                    "quote": "0.7052",
                    "bias": "ALTA",
                    "biasType": "bull",
                    "pt": {
                              "fundamental": "O AUD/USD opera em 0,7052 no fechamento diário de 13/08/2026 (referência BCE), sustentando a tendência de alta acima da SMA200 (0,6922). O RBA manteve a taxa em 4,35% em 11/08 (a presidente Bullock sinalizou novas altas possíveis, com inflação núcleo em 3,6%) e o Brent acima de US$ 87/bbl (+30% no ano, tensões Irã/Hormuz) sustentam o australiano, enquanto o CPI dos EUA em 3,4% (mais brando) e a manutenção dividida do Fed limitam o dólar. O par repousa sob a Fib 23,6% (0,7065) do avanço de 0,6445 a 0,7257, acima das SMA50 (0,6991) e SMA200 (0,6922). Indicadores calculados a partir da série diária BCE/Frankfurter (519 pregões). A estrutura segue de alta enquanto a SMA200 segurar.",
                              "trend": "Acima das SMA50 (0,6991) e SMA200 (0,6922) — sob a Fib 23,6% dentro da tendência mais ampla de 0,6445 a 0,7257; a retração mira a Fib 38,2% (0,6947).",
                              "support": "0,6947 (Fib 38,2%), com a SMA200 de 0,6922 abaixo.",
                              "resistance": "0,7065 (Fib 23,6%) na região atual, com a máxima de 0,7257 acima.",
                              "priceAction": "Uma rejeição de alta (pin bar / engolfo bullish) na zona 0,6947-0,6960 (Fib 38,2%), com fechamento diário novamente acima de 0,7010, retomaria a alta rumo a 0,7150.",
                              "recommendation": "COMPRA (LONG) NA RETRAÇÃO",
                              "trigger": "Rejeição de alta (pin bar / engolfo bullish) em 0,6960 (zona Fib 38,2%), com fechamento diário sustentando acima de 0,7010.",
                              "stop": "0,6890 (Abaixo da SMA200 de 0,6922).",
                              "target": "0,7150 (Acima da Fib 23,6% em 0,7065).",
                              "rr": "1:2.71",
                              "rrValue": 68,
                              "justification": "A estrutura acima de ambas as SMAs, respaldada por um RBA a 4,35% com viés hawkish e commodities firmes (Brent ~US$ 87) contra um Fed dividido e CPI brando, mantém o viés de alta. Uma retração até a Fib 38,2% oferece entrada comprada com stop protegido abaixo da SMA200 e R/R de 1:2.71 rumo a 0,7150."
                    },
                    "en": {
                              "fundamental": "AUD/USD trades at 0.7052 on the 13/08/2026 daily close (ECB reference), holding its uptrend above the 200-day SMA (0.6922). The RBA held at 4.35% on Aug 11 (Governor Bullock flagged more hikes possible, trimmed-mean inflation at 3.6%) and Brent above $87/bbl (+30% YTD, Iran/Hormuz tensions) underpin the aussie, while US CPI at 3.4% (softer) and the Fed's divided hold cap the dollar. The pair sits just below the 23.6% Fib (0.7065) of the 0.6445 to 0.7257 advance, above the 50-day (0.6991) and 200-day (0.6922) SMAs. Indicators computed from the ECB/Frankfurter daily series (519 sessions). Structure stays bullish while the 200-day holds.",
                              "trend": "Above both the 50-day (0.6991) and 200-day (0.6922) SMAs — just below the 23.6% Fib within the broader 0.6445 to 0.7257 uptrend; pullback target is the 38.2% Fib (0.6947).",
                              "support": "0.6947 (38.2% Fib), with the 0.6922 200-day SMA beneath.",
                              "resistance": "0.7065 (23.6% Fib) at the current region, with the 0.7257 swing high above.",
                              "priceAction": "A bullish rejection (pin bar / bullish engulfing) at the 0.6947-0.6960 zone (38.2% Fib), with a daily close back above 0.7010, would resume the uptrend toward 0.7150.",
                              "recommendation": "BUY (LONG) ON PULLBACK",
                              "trigger": "Bullish rejection (pin bar / bullish engulfing) at 0.6960 (38.2% Fib zone), on a daily close back above 0.7010.",
                              "stop": "0.6890 (Below the 0.6922 200-day SMA).",
                              "target": "0.7150 (Above the 23.6% Fib at 0.7065).",
                              "rr": "1:2.71",
                              "rrValue": 68,
                              "justification": "The structure above both SMAs, backed by a hawkish-tilt RBA at 4.35% and firm commodities (Brent ~$87) against a divided Fed and soft CPI, keeps the bias bullish. A pullback to the 38.2% Fib offers a long with a protected stop below the 200-day SMA and 1:2.71 R/R toward 0.7150."
                    }
          },
          "GBP/USD": {
                    "quote": "1.3492",
                    "bias": "ALTA",
                    "biasType": "bull",
                    "pt": {
                              "fundamental": "O GBP/USD opera em 1,3492 no fechamento diário de 13/08/2026 (referência BCE), sustentando acima de ambas as SMAs. A manutenção do BoE a 3,75% em 30/07 (divisão 6-3, três dissidentes a favor de 4,00%) sustenta a libra, enquanto o CPI dos EUA em 3,4% (mais brando) e a manutenção dividida do Fed pressionam o dólar. O par reconquistou a Fib 50% (1,3439) do avanço de 1,3062 a 1,3817 e mira a Fib 38,2% (1,3528), acima das SMA50 (1,3368) e SMA200 (1,3402). Indicadores calculados a partir da série diária BCE/Frankfurter (519 pregões). A estrutura segue de alta enquanto a SMA200 segurar.",
                              "trend": "Acima das SMA50 (1,3368) e SMA200 (1,3402); reconquistando a Fib 50% (1,3439) dentro do uptrend de 1,3062 a 1,3817, próximo obstáculo a Fib 38,2% (1,3528).",
                              "support": "1,3439 (Fib 50%), com a SMA200 de 1,3402 abaixo.",
                              "resistance": "1,3528 (Fib 38,2%), com a máxima de 1,3817 acima.",
                              "priceAction": "Uma rejeição de alta (pin bar / engolfo bullish) na zona 1,3439-1,3402 (Fib 50% / SMA200), com fechamento diário novamente acima de 1,3470, retomaria a alta rumo a 1,3528-1,3625.",
                              "recommendation": "COMPRA (LONG) NA RETRAÇÃO",
                              "trigger": "Rejeição de alta (pin bar / engolfo bullish) em 1,3420 (confluência Fib 50% / SMA200), com fechamento diário sustentando acima de 1,3470.",
                              "stop": "1,3340 (Abaixo da Fib 61,8% em 1,3350).",
                              "target": "1,3625 (Acima da Fib 38,2% em 1,3528).",
                              "rr": "1:2.56",
                              "rrValue": 64,
                              "justification": "A estrutura acima de ambas as SMAs, reforçada por um BoE hawkish a 3,75% (divisão 6-3) contra um Fed dividido e CPI brando, mantém o viés de alta. Uma retração até a confluência Fib 50% / SMA200 oferece entrada comprada com stop protegido abaixo da Fib 61,8% e R/R de 1:2.56 rumo a 1,3625."
                    },
                    "en": {
                              "fundamental": "GBP/USD trades at 1.3492 on the 13/08/2026 daily close (ECB reference), holding above both SMAs. The BoE's hold at 3.75% on July 30 (6-3 split, three dissents for 4.00%) supports sterling, while US CPI at 3.4% (softer) and the Fed's divided hold pressure the dollar. The pair has reclaimed the 50% Fib (1.3439) of the 1.3062 to 1.3817 advance and eyes the 38.2% Fib (1.3528), above the 50-day (1.3368) and 200-day (1.3402) SMAs. Indicators computed from the ECB/Frankfurter daily series (519 sessions). Structure stays bullish while the 200-day holds.",
                              "trend": "Above both the 50-day (1.3368) and 200-day (1.3402) SMAs; reclaiming the 50% Fib (1.3439) within the 1.3062 to 1.3817 uptrend, next hurdle the 38.2% Fib (1.3528).",
                              "support": "1.3439 (50% Fib), with the 1.3402 200-day SMA beneath.",
                              "resistance": "1.3528 (38.2% Fib), with the 1.3817 swing high above.",
                              "priceAction": "A bullish rejection (pin bar / bullish engulfing) at the 1.3439-1.3402 zone (50% Fib / 200-day SMA), with a daily close back above 1.3470, would resume the uptrend toward 1.3528-1.3625.",
                              "recommendation": "BUY (LONG) ON PULLBACK",
                              "trigger": "Bullish rejection (pin bar / bullish engulfing) at 1.3420 (50% Fib / 200-day SMA confluence), on a daily close back above 1.3470.",
                              "stop": "1.3340 (Below the 61.8% Fib at 1.3350).",
                              "target": "1.3625 (Above the 38.2% Fib at 1.3528).",
                              "rr": "1:2.56",
                              "rrValue": 64,
                              "justification": "The structure above both SMAs, reinforced by a hawkish BoE at 3.75% (6-3 split) against a divided Fed and soft CPI, keeps the bias bullish. A pullback to the 50% Fib / 200-day SMA confluence offers a long with a protected stop below the 61.8% Fib and 1:2.56 R/R toward 1.3625."
                    }
          },
          "EUR/JPY": {
                    "quote": "183.77",
                    "bias": "ALTA",
                    "biasType": "bull",
                    "pt": {
                              "fundamental": "O EUR/JPY opera em 183,77 no fechamento diário de 13/08/2026 (referência BCE), subindo +0,06% enquanto o choque de intervenção no iene do início de agosto se desfaz e o carry trade retoma. Após o mergulho até a Fib 61,8% (181,09), o par reconquistou por margem estreita a SMA200 (183,72) e repousa entre a Fib 38,2% (183,62) e a SMA50 (184,80), dentro do avanço de 176,99 a 187,73. O diferencial de carry BCE (2,25%)-BoJ (1,0%) segue amplo, mas a reconquista da SMA200 por apenas ~5 pips não oferece gatilho limpo. Indicadores calculados a partir da série diária BCE/Frankfurter (519 pregões).",
                              "trend": "Acima da SMA200 (183,72) por margem estreita e abaixo da SMA50 (184,80) — o avanço de 176,99 a 187,73 foi restaurado em estrutura, mas o gatilho direcional não é limpo.",
                              "support": "182,36 (Fib 50%), com a SMA200 de 183,72 logo acima.",
                              "resistance": "184,80 (SMA50) em confluência com a Fib 23,6% (185,19); 187,73 (máxima) acima.",
                              "priceAction": "Sem gatilho de price-action acionável: a reconquista da SMA200 por margem estreita não oferece entrada de risco-retorno limpa. Aguardar fechamento diário decisivo acima de 185,19 (rompimento) ou rejeição em 182,36 (retração).",
                              "recommendation": "AGUARDAR OUTRO GATILHO",
                              "trigger": "Nenhum gatilho acionável — reconquista da SMA200 (183,72) por margem estreita. Aguardar rompimento decisivo de 185,19 (SMA50 / Fib 23,6%) com follow-through, ou retração até 182,36 (Fib 50%).",
                              "stop": "N/A (sem operação).",
                              "target": "N/A (sem operação).",
                              "rr": "N/A",
                              "rrValue": 0,
                              "justification": "A reconquista da SMA200 (183,72) por apenas ~5 pips após o choque de intervenção não oferece setup direcional limpo: um longo em retração até a Fib 50% (182,36) estaca em R/R ~1:1,8 rumo à SMA50, e um longo no rompimento de 185,19 estaca em R/R ~1:1,9 rumo à máxima de 187,73, com alvos estendidos bloqueados por essa mesma máxima. Técnicos ganham — aguardar rompimento decisivo ou retração mais profunda para destravar R/R ≥ 1:2."
                    },
                    "en": {
                              "fundamental": "EUR/JPY trades at 183.77 on the 13/08/2026 daily close (ECB reference), rising +0.06% as the early-August yen intervention shock unwinds and carry trade resumes. After the dive to the 61.8% Fib (181.09), the pair has narrowly reclaimed its 200-day SMA (183.72) and sits between the 38.2% Fib (183.62) and the 50-day SMA (184.80), within the 176.99 to 187.73 advance. The ECB (2.25%)-BoJ (1.00%) carry gap remains wide, but the 200-day reclaim by only ~5 pips offers no clean trigger. Indicators computed from the ECB/Frankfurter daily series (519 sessions).",
                              "trend": "Above the 200-day SMA (183.72) by a narrow margin and below the 50-day SMA (184.80) — the 176.99 to 187.73 advance has been restored in structure, but the directional trigger is not clean.",
                              "support": "182.36 (50% Fib), with the 183.72 200-day SMA just above.",
                              "resistance": "184.80 (50-day SMA) in confluence with the 23.6% Fib (185.19); 187.73 (swing high) above.",
                              "priceAction": "No actionable price-action trigger: the narrow 200-day reclaim offers no clean risk-reward entry. Wait for a decisive daily close above 185.19 (breakout) or a rejection at 182.36 (pullback).",
                              "recommendation": "WAIT FOR ANOTHER TRIGGER",
                              "trigger": "No actionable trigger — narrow reclaim of the 200-day SMA (183.72). Wait for a decisive breakout of 185.19 (50-day SMA / 23.6% Fib) with follow-through, or a pullback to 182.36 (50% Fib).",
                              "stop": "N/A (no trade).",
                              "target": "N/A (no trade).",
                              "rr": "N/A",
                              "rrValue": 0,
                              "justification": "The 200-day SMA (183.72) reclaim by only ~5 pips after the intervention shock offers no clean directional setup: a pullback long to the 50% Fib (182.36) caps at ~1:1.8 R/R to the 50-day SMA, and a breakout long above 185.19 caps at ~1:1.9 R/R to the 187.73 swing high, with extension targets blocked by that same high. Technicals win — wait for a decisive breakout or a deeper pullback to unlock R/R of at least 1:2."
                    }
          },
          "GBP/JPY": {
                    "quote": "214.96",
                    "bias": "ALTA",
                    "biasType": "bull",
                    "pt": {
                              "fundamental": "O GBP/JPY opera em 214,96 no fechamento diário de 13/08/2026 (referência BCE), com o choque de intervenção no iene a desfazer-se e o carry a retomar. O par reconquistou a SMA200 (211,83) decisivamente e repousa sob a SMA50 (215,45), sobre a Fib 23,6% (214,83) do avanço de 200,87 a 219,14. O amplo diferencial de carry BoE (3,75%)-BoJ (1,0%) e a retomada do carry dominam; a estrutura voltou a ser de alta acima dos 200 dias. Indicadores calculados a partir da série diária BCE/Frankfurter (519 pregões).",
                              "trend": "Acima da SMA200 (211,83) e abaixo da SMA50 (215,45) — o avanço de 200,87 a 219,14 foi restaurado; rompimento da SMA50 miraria a máxima de 219,14.",
                              "support": "212,16 (Fib 38,2%), com a SMA200 de 211,83 abaixo.",
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
                              "fundamental": "GBP/JPY trades at 214.96 on the 13/08/2026 daily close (ECB reference), with the yen intervention shock unwinding and carry resuming. The pair has decisively reclaimed its 200-day SMA (211.83) and sits below the 50-day SMA (215.45), on the 23.6% Fib (214.83) of the 200.87 to 219.14 advance. The wide BoE (3.75%)-BoJ (1.00%) carry gap and the carry resumption dominate; structure is back to bullish above the 200-day. Indicators computed from the ECB/Frankfurter daily series (519 sessions).",
                              "trend": "Above the 200-day SMA (211.83) and below the 50-day SMA (215.45) — the 200.87 to 219.14 advance has been restored; a 50-day SMA breakout would target the 219.14 swing high.",
                              "support": "212.16 (38.2% Fib), with the 211.83 200-day SMA beneath.",
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
            "EUR/USD": "-0.13%",
            "USD/JPY": "+0.35%",
            "AUD/USD": "+0.01%",
            "GBP/USD": "-0.03%",
            "EUR/JPY": "+0.22%",
            "GBP/JPY": "+0.32%"
        };'''
new_changes = '''        const dailyChanges = {
            "EUR/USD": "-0.09%",
            "USD/JPY": "+0.15%",
            "AUD/USD": "-0.28%",
            "GBP/USD": "-0.25%",
            "EUR/JPY": "+0.06%",
            "GBP/JPY": "-0.10%"
        };'''
if old_changes not in html:
    sys.exit("ERROR: dailyChanges block not found verbatim")
html = html.replace(old_changes, new_changes)

# ---- Replace macroDrivers block ----
old_drivers = '''        const macroDrivers = {
            "EUR/USD": {
                en: ["Fed hold 3.50-3.75%", "USD soft", "ECB 2.25%"],
                pt: ["Fed 3,50-3,75%", "USD macio", "BCE 2,25%"]
            },
            "USD/JPY": {
                en: ["BoJ hold 1.00%", "Carry resumed", "Fed–BoJ gap"],
                pt: ["BoJ 1,0%", "Carry retomado", "Diferencial Fed–BoJ"]
            },
            "AUD/USD": {
                en: ["RBA 4.35%", "Brent $83", "Fed dovish"],
                pt: ["RBA 4,35%", "Brent $83", "Fed dovish"]
            },
            "GBP/USD": {
                en: ["BoE 3.75% 6-3", "CPI 2.6%", "Fed dovish"],
                pt: ["BoE 3,75% 6-3", "IPC 2,6%", "Fed dovish"]
            },
            "EUR/JPY": {
                en: ["BoJ hold 1.00%", "Carry resumed", "ECB–BoJ gap"],
                pt: ["BoJ 1,0%", "Carry retomado", "Diferencial BCE–BoJ"]
            },
            "GBP/JPY": {
                en: ["BoJ hold 1.00%", "Carry resumed", "BoE–BoJ gap"],
                pt: ["BoJ 1,0%", "Carry retomado", "Diferencial BoE–BoJ"]
            }
        };'''
new_drivers = '''        const macroDrivers = {
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
if old_drivers not in html:
    sys.exit("ERROR: macroDrivers block not found verbatim")
html = html.replace(old_drivers, new_drivers)

# ---- Replace the two dataBasis i18n strings ----
old_basis_en = 'dataBasis: "Data basis: ECB/Frankfurter reference rates · SMA50/200 & Fibonacci computed · 517 daily sessions (01/08/2024–11/08/2026).",'
new_basis_en = 'dataBasis: "Data basis: ECB/Frankfurter reference rates · SMA50/200 & Fibonacci computed · 519 daily sessions (01/08/2024–13/08/2026).",'
if html.count(old_basis_en) != 1:
    sys.exit(f"ERROR: EN dataBasis not found exactly once ({html.count(old_basis_en)})")
html = html.replace(old_basis_en, new_basis_en)

old_basis_pt = 'dataBasis: "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200 e Fibonacci calculados · 517 pregões (01/08/2024 a 11/08/2026).",'
new_basis_pt = 'dataBasis: "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200 e Fibonacci calculados · 519 pregões (01/08/2024 a 13/08/2026).",'
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
