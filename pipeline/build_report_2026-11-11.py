#!/usr/bin/env python3
"""11/11/2026 edition. Wednesday ECB fixing extends the post-CPI dollar bid.
EUR/USD and AUD/USD print marginal new 9-month lows (first close, not the
confirmation). USD/JPY closes back above the SMA200 but stays mixed.
No ticket clears the gate. Static pages are regenerated separately."""
import json

INDEX = r"C:/Projetos/forex-report/docs/index.html"
LEDGER = r"C:/Projetos/forex-report/docs/track-record.json"
NEWS = r"C:/Projetos/forex-report/docs/news.html"
SITEMAP = r"C:/Projetos/forex-report/docs/sitemap.xml"
VERIFY = r"C:/Projetos/forex-report/pipeline/verify_all.py"
TS = "11/11/2026 20:25 UTC"
OLD_TS = "10/11/2026 23:10 UTC"
BASIS = "583 sessions, 01/08/2024 to 11/11/2026"
BASIS_PT = "583 pregões, 01/08/2024 a 11/11/2026"

def pair(quote, bias, bias_type, pt, en):
    return {"quote": quote, "bias": bias, "biasType": bias_type, "pt": pt, "en": en}

EUR = pair("1.1127", "BAIXA", "bear",
    pt={
        "fundamental": "O EUR/USD fechou em 1,1127 na sessão de quarta 11/11/2026 (taxa de referência BCE/Frankfurter), caindo -0,78% (-87 pips) a partir de 1,1214. O fechamento é uma nova mínima de 9 meses e de 10/20 pregões, 3 pips sob a mínima anterior (1,1130, 29/10). É o primeiro print do extremo, não o segundo fechamento de confirmação. O movimento prolonga o dólar do CPI de terça (+0,4% no mês, núcleo +0,3%). Quarta é feriado de Veterans Day nos EUA (mercado de títulos recomendado fechado; sem dado do BLS). O Fed segue em 3,75-4,00% e o mercado passou a discutir uma alta de 50 pontos-base em dezembro. Alinhamento de baixa pleno (fechamento sob a SMA200 1,1536, SMA50 1,1323 abaixo dela). Um short sob 1,1127 com stop sobre 1.1267 (~140 pips, piso de 62) joga o 1:2 em 1.0847, através de 1.1100, 1.1050, 1.1000 e 1.0950. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (1,1536) com a SMA50 (1,1323) abaixo dela — alinhamento de baixa pleno. O próprio fechamento é a mínima de 10/20 pregões e de 9 meses.",
        "support": "1.1127 (mínima de 9 meses e de 10/20 pregões, 11/11), com o redondo 1.1100 logo abaixo.",
        "resistance": "1.1267 (máxima de 10/20 pregões, 04/11), com a Fib 78,6% em 1,1292 e a SMA50 (1,1323) acima.",
        "priceAction": "Primeiro fechamento sob 1.1130, por 3 pips. Sem o segundo print e com o 1:2 atravessando quatro redondos. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "1,1127 é o extremo novo. A regra pede um segundo fechamento sob ele, e mesmo assim o stop que cobre 1.1267 atravessa 1.1100, 1.1050, 1.1000 e 1.0950.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "A baixa alinhou e o euro fez a mínima de 9 meses, mas 3 pips não são a confirmação e o alvo estrutural cai na escada de redondos. A mesa não vende o primeiro print."
    },
    en={
        "fundamental": "EUR/USD closed at 1.1127 in the Wednesday 11/11/2026 session (ECB/Frankfurter reference rate), down -0.78% (-87 pips) from 1.1214. The close is a new 9-month and 10/20-day low, 3 pips under the prior low (1.1130, Oct 29). It is the first print of the extreme, not the second confirming close. The move extends Tuesday's post-CPI dollar (headline +0.4% m/m, core +0.3%). Wednesday is the US Veterans Day holiday (dollar bond market recommended shut; no BLS release). The Fed is still at 3.75-4.00% and the market is now debating a 50-basis-point hike in December. Full bear alignment (close under the SMA200 1.1536, SMA50 1.1323 below it). A short under 1.1127 with a stop over 1.1267 (~140 pips, 62-pip floor) puts the 1:2 at 1.0847, through 1.1100, 1.1050, 1.1000 and 1.0950. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (1.1536) with the 50-day (1.1323) below it — full bear alignment. Today's close is the 10/20-day and 9-month low.",
        "support": "1.1127 (the 9-month and 10/20-day low, Nov 11), with the 1.1100 round just below.",
        "resistance": "1.1267 (the 10/20-day high, Nov 4), with the 78.6% Fib at 1.1292 and the SMA50 (1.1323) above.",
        "priceAction": "First close under 1.1130, by 3 pips. No second print, and the 1:2 crosses four rounds. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "1.1127 is the new extreme. The rule asks for a second close under it, and even then the stop that covers 1.1267 crosses 1.1100, 1.1050, 1.1000 and 1.0950.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The bear stack is aligned and the euro made the 9-month low, but 3 pips are not the confirmation and the structural target falls on the round-number ladder. The desk does not sell the first print."
    })

USDJPY = pair("159.23", "NEUTRO", "neutral",
    pt={
        "fundamental": "O USD/JPY fechou em 159,23 na sessão de quarta 11/11/2026 (taxa de referência BCE/Frankfurter), subindo +0,66% (+105 pips). O fechamento voltou para cima da SMA200 (158,65), por 58 pips, e é a nova máxima de 10 e de 20 pregões. A SMA50 (157,24) continua sob a SMA200 — alinhamento misto, não alta. O piso de 1,5σ20 é de 72 pips, então um stop sob a SMA200 não cabe. Um stop sob a SMA50 (~199 pips) joga o 1:2 perto de 163,21, através de 160,00, 161,00 e 162,00, encostando na máxima de 9 meses (163,91). O CPI de terça já ficou para trás. O BoJ segue em 1,25%. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento acima da SMA200 (158,65), mas a SMA50 (157,24) ainda está abaixo dela — alinhamento misto. A máxima de 9 meses segue 163,91.",
        "support": "158.65 (a SMA200, devolvida hoje) e 158.46 (máxima antiga de 10 pregões), com a SMA50 em 157,24 e a mínima de 20 pregões em 156,80.",
        "resistance": "159.23 (máxima de 10/20 pregões, o próprio fechamento) e o redondo 160,00, com a máxima de 9 meses em 163,91.",
        "priceAction": "Rompimento de 10/20 pregões num mapa misto. O stop que respeita o piso de 72 pips empurra o alvo para a escada de redondos. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "Um segundo fechamento acima de 159,23 confirmaria o extremo de 20 pregões, mas o stop sob a SMA50 não entrega 1:2 antes de 160,00, 161,00 e 162,00. Vender contra o fechamento de hoje não tem alinhamento.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O iene cedeu a máxima de 20 pregões, mas a SMA50 não cruzou a SMA200. 58 pips até a média longa cabem no piso de 72, e o alvo longo atravessa três redondos."
    },
    en={
        "fundamental": "USD/JPY closed at 159.23 in the Wednesday 11/11/2026 session (ECB/Frankfurter reference rate), up +0.66% (+105 pips). The close moved back above the SMA200 (158.65), by 58 pips, and is the new 10-day and 20-day high. The SMA50 (157.24) is still under the SMA200 — mixed alignment, not a bull stack. The 1.5-sigma20 floor is 72 pips, so a stop under the SMA200 does not fit. A stop under the SMA50 (~199 pips) puts the 1:2 near 163.21, through 160.00, 161.00 and 162.00, into the 9-month high (163.91). Tuesday's CPI is behind us. The BoJ is still at 1.25%. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close above the SMA200 (158.65), but the SMA50 (157.24) is still below it — mixed alignment. The 9-month high remains 163.91.",
        "support": "158.65 (the SMA200, handed back today) and 158.46 (the old 10-day high), with the SMA50 at 157.24 and the 20-day low at 156.80.",
        "resistance": "159.23 (the 10/20-day high, today's close) and the 160.00 round, with the 9-month high at 163.91.",
        "priceAction": "A 10/20-day break on a mixed map. The stop that respects the 72-pip floor pushes the target onto the round ladder. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "A second close above 159.23 would confirm the 20-day extreme, but the stop under the SMA50 does not deliver a 1:2 before 160.00, 161.00 and 162.00. A short against today's close has no alignment.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The yen gave up the 20-day high, but the SMA50 has not crossed the SMA200. 58 pips down to the long average fit inside the 72-pip floor, and the long target crosses three rounds."
    })

AUD = pair("0.6859", "BAIXA", "bear",
    pt={
        "fundamental": "O AUD/USD fechou em 0,6859 na sessão de quarta 11/11/2026 (taxa de referência BCE/Frankfurter), caindo -0,65% (-45 pips). O fechamento é uma nova mínima de 9 meses e de 10/20 pregões, 1 pip sob a mínima anterior (0,6860). É o primeiro print do extremo. A SMA50 (0,7033) está sob a SMA200 (0,7055) e o preço está sob as duas — alinhamento de baixa. O piso de 1,5σ20 é de 64 pips. Um short sob 0,6859 com stop sobre 0,7025 (~166 pips) joga o 1:2 através de 0,6800, 0,6700 e 0,6600. O RBA está em 4,85%. O dólar pós-CPI fez o trabalho; a regra do extremo maior ainda pede o segundo fechamento. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (0,7055) com a SMA50 (0,7033) abaixo dela — alinhamento de baixa. O próprio fechamento é a mínima de 10/20 pregões e de 9 meses.",
        "support": "0.6859 (mínima de 9 meses e de 10/20 pregões, 11/11), com o redondo 0.6800 abaixo.",
        "resistance": "0.7025 (máxima de 10 pregões) e 0.7034 (máxima de 20 pregões), com a SMA50 (0,7033) e a SMA200 (0,7055) no teto.",
        "priceAction": "Primeiro fechamento sob 0,6860, por 1 pip. Sem o segundo print e com o stop estrutural atravessando três redondos. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "0,6859 é o extremo novo. A regra pede um segundo fechamento sob ele. O stop que cobre 0,7025 não entrega 1:2 antes de 0,6800, 0,6700 e 0,6600.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O Aussie cravou a mínima de 9 meses por 1 pip. Isso arma o extremo, não a venda. O caminho de um 1:2 estrutural está bloqueado."
    },
    en={
        "fundamental": "AUD/USD closed at 0.6859 in the Wednesday 11/11/2026 session (ECB/Frankfurter reference rate), down -0.65% (-45 pips). The close is a new 9-month and 10/20-day low, 1 pip under the prior low (0.6860). It is the first print of the extreme. The SMA50 (0.7033) sits under the SMA200 (0.7055) and price is under both — bear alignment. The 1.5-sigma20 floor is 64 pips. A short under 0.6859 with a stop over 0.7025 (~166 pips) puts the 1:2 through 0.6800, 0.6700 and 0.6600. The RBA cash rate is 4.85%. The post-CPI dollar did the work; the major-extreme rule still asks for the second close. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (0.7055) with the SMA50 (0.7033) below it — bear alignment. Today's close is the 10/20-day and 9-month low.",
        "support": "0.6859 (the 9-month and 10/20-day low, Nov 11), with the 0.6800 round below.",
        "resistance": "0.7025 (the 10-day high) and 0.7034 (the 20-day high), with the SMA50 (0.7033) and the SMA200 (0.7055) as the ceiling.",
        "priceAction": "First close under 0.6860, by 1 pip. No second print, and the structural stop crosses three rounds. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "0.6859 is the new extreme. The rule asks for a second close under it. The stop that covers 0.7025 does not deliver a 1:2 before 0.6800, 0.6700 and 0.6600.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The Aussie pinned the 9-month low by 1 pip. That arms the extreme, not the short. The path of a structural 1:2 is blocked."
    })

GBP = pair("1.3307", "BAIXA", "bear",
    pt={
        "fundamental": "O GBP/USD fechou em 1,3307 na sessão de quarta 11/11/2026 (taxa de referência BCE/Frankfurter), caindo -0,86% (-116 pips) a partir de 1,3423. Voltou para baixo das duas médias: SMA50 1,3358 e SMA200 1,3422. Alinhamento de baixa (a SMA50 também está sob a SMA200). Não é rompimento de 10 pregões — a mínima de 20 pregões segue 1.3247, 60 pips abaixo, dentro do piso de 78. O PIB do Reino Unido (1ª estimativa do 3º trimestre) sai quinta 12/11 às 07:00 UTC. O short de 22/10 já fechou no stop em 04/11. A Bank Rate está em 4,00%. Um stop sobre 1.3500 a partir de 1,3307 (~193 pips) joga o 1:2 através de 1.3247 e da mínima de 9 meses (1,3160). Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (1,3422) e sob a SMA50 (1,3358), com a SMA50 abaixo da SMA200 — alinhamento de baixa. A máxima de 10/20 pregões segue 1.3500.",
        "support": "1.3247 (mínima de 20 pregões), com a mínima de 9 meses em 1.3160 e o redondo 1.3200 no meio.",
        "resistance": "1.3358 (a SMA50) e 1.3422 (a SMA200), com a máxima de 10/20 pregões em 1.3500.",
        "priceAction": "Queda de 116 pips, de volta sob as duas médias, sem renovar 1.3247. 60 pips de ar cabem no piso. Sem ticket antes do PIB britânico.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "1.3247 é o piso de 20 pregões. O preço está 60 pips acima dele, dentro do piso de 78, e um stop sobre 1.3500 atravessa 1.3160 no alvo. Reavaliar após o PIB do Reino Unido (12/11, 07:00 UTC).",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O cabo devolveu a SMA200, mas não fez o extremo de 20 pregões. O ar até 1.3247 é menor que o piso, e o alvo estrutural cai na mínima de 9 meses."
    },
    en={
        "fundamental": "GBP/USD closed at 1.3307 in the Wednesday 11/11/2026 session (ECB/Frankfurter reference rate), down -0.86% (-116 pips) from 1.3423. It moved back under both averages: SMA50 1.3358 and SMA200 1.3422. Bear alignment (the SMA50 is also under the SMA200). It is not a 10-day break — the 20-day low is still 1.3247, 60 pips below, inside the 78-pip floor. UK GDP (Q3 first estimate) is due Thursday Nov 12 at 07:00 UTC. The Oct 22 short already stopped out on Nov 4. Bank Rate is 4.00%. A stop over 1.3500 from 1.3307 (~193 pips) puts the 1:2 through 1.3247 and the 9-month low (1.3160). Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (1.3422) and under the SMA50 (1.3358), with the SMA50 below the SMA200 — bear alignment. The 10/20-day high is still 1.3500.",
        "support": "1.3247 (the 20-day low), with the 9-month low at 1.3160 and the 1.3200 round in between.",
        "resistance": "1.3358 (the SMA50) and 1.3422 (the SMA200), with the 10/20-day high at 1.3500.",
        "priceAction": "A 116-pip drop, back under both averages, without renewing 1.3247. 60 pips of air fit inside the floor. No ticket ahead of UK GDP.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "1.3247 is the 20-day floor. Price is 60 pips above it, inside the 78-pip floor, and a stop over 1.3500 crosses 1.3160 on the target. Reassess after UK GDP (Nov 12, 07:00 UTC).",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "Cable handed back the SMA200, but it did not make the 20-day extreme. The air down to 1.3247 is smaller than the floor, and the structural target lands on the 9-month low."
    })

EURJPY = pair("177.18", "BAIXA", "bear",
    pt={
        "fundamental": "O EUR/JPY fechou em 177,18 na sessão de quarta 11/11/2026 (taxa de referência BCE/Frankfurter), caindo -0,12% (-21 pips). A mínima de 10 pregões segue 175,68 e a de 9 meses / 20 pregões 175,51. O fechamento ficou 150 pips acima de 175,68, além do piso de 104. Uma venda sob 175,68 com stop sobre 178,30 (~262 pips) joga o 1:2 dentro do cluster de set-out/2025. Alinhamento de baixa (fechamento sob a SMA200 183,00 e a SMA50 178,02). O euro fez mínima de 9 meses contra o dólar; contra o iene, não. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (183,00) com a SMA50 (178,02) abaixo dela — alinhamento de baixa pleno. A máxima de 10/20 pregões está em 178,30 (04/11).",
        "support": "175.68 (mínima de 10 pregões, 30/10) e 175.51 (mínima de 9 meses e de 20 pregões, 23/10), com o redondo 175,00 abaixo.",
        "resistance": "178.30 (máxima de 10/20 pregões, 04/11) e a SMA50 (178,02), com a Fib 78,6% em 178,12.",
        "priceAction": "Queda de 21 pips, ainda longe de 175,68. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "O fechamento sob 175,68 continua sendo a regra do extremo, mas o stop sobre 178,30 coloca o alvo no cluster de 2025. O preço de hoje está 150 pips acima desse piso.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O cruzado não acompanhou a mínima do euro. 150 pips separam o preço do gatilho, e o stop estrutural empurra o alvo para 2025."
    },
    en={
        "fundamental": "EUR/JPY closed at 177.18 in the Wednesday 11/11/2026 session (ECB/Frankfurter reference rate), down -0.12% (-21 pips). The 10-day low is still 175.68 and the 9-month / 20-day low is 175.51. The close finished 150 pips above 175.68, beyond the 104-pip floor. A short under 175.68 with a stop over 178.30 (~262 pips) puts the 1:2 inside the Sep-Oct 2025 cluster. Bear alignment (close under the SMA200 183.00 and the SMA50 178.02). The euro made a 9-month low against the dollar; against the yen, it did not. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (183.00) with the SMA50 (178.02) below it — full bear alignment. The 10/20-day high is 178.30 (Nov 4).",
        "support": "175.68 (the 10-day low, Oct 30) and 175.51 (the 9-month and 20-day low, Oct 23), with the 175.00 round below.",
        "resistance": "178.30 (the 10/20-day high, Nov 4) and the SMA50 (178.02), with the 78.6% Fib at 178.12.",
        "priceAction": "A 21-pip dip, still far from 175.68. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The close under 175.68 is still the extreme's rule, but the stop over 178.30 puts the target in the 2025 cluster. Today's price is 150 pips above that floor.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The cross did not follow the euro's low. 150 pips separate price from the trigger, and the structural stop pushes the target into 2025."
    })

GBPJPY = pair("211.89", "BAIXA", "bear",
    pt={
        "fundamental": "O GBP/JPY fechou em 211,89 na sessão de quarta 11/11/2026 (taxa de referência BCE/Frankfurter), caindo -0,20% (-43 pips). Ficou 104 pips sob a SMA200 (212,93) — dentro do piso de 121 pips — e acima da SMA50 (210,02). Alinhamento de baixa. A mínima de 10 pregões está em 210,49 e a de 20 pregões em 209,27. Um stop sobre a SMA200 a partir de 210,49 joga o 1:2 para baixo da mínima de 9 meses (207,32). O PIB britânico sai quinta 12/11 às 07:00 UTC. BoE em 4,00%, BoJ em 1,25%. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (212,93) com a SMA50 (210,02) abaixo dela — alinhamento de baixa. A máxima de 10/20 pregões está em 213,63 (04/11).",
        "support": "210.49 (mínima de 10 pregões), com 209,27 (mínima de 20 pregões) e a mínima de 9 meses em 207,32.",
        "resistance": "212.93 (a SMA200), com a Fib 50% em 213,23 e a máxima de 10/20 pregões em 213,63.",
        "priceAction": "Queda de 43 pips e ainda dentro do piso da SMA200. Sem ticket antes do PIB britânico.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "210,49 é o piso de 10 pregões. Vender aqui, a 104 pips da SMA200, não paga o piso de 121. O stop estrutural sobre a média joga o alvo para baixo de 207,32. Reavaliar após o PIB (12/11, 07:00 UTC).",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "Cento e quatro pips sob a SMA200 cabem no piso de 121. O cabo fraco não abriu geometria no cruzado. A mesa espera o PIB."
    },
    en={
        "fundamental": "GBP/JPY closed at 211.89 in the Wednesday 11/11/2026 session (ECB/Frankfurter reference rate), down -0.20% (-43 pips). It finished 104 pips under the SMA200 (212.93) — inside the 121-pip floor — and above the SMA50 (210.02). Bear alignment. The 10-day low is 210.49 and the 20-day low is 209.27. A stop over the SMA200 from 210.49 throws the 1:2 under the 9-month low (207.32). UK GDP is due Thursday Nov 12 at 07:00 UTC. BoE at 4.00%, BoJ at 1.25%. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (212.93) with the SMA50 (210.02) below it — bear alignment. The 10/20-day high is 213.63 (Nov 4).",
        "support": "210.49 (the 10-day low), with 209.27 (the 20-day low) and the 9-month low at 207.32.",
        "resistance": "212.93 (the SMA200), with the 50% Fib at 213.23 and the 10/20-day high at 213.63.",
        "priceAction": "A 43-pip dip and still inside the SMA200's floor. No ticket ahead of UK GDP.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "210.49 is the 10-day floor. Selling here, 104 pips under the SMA200, does not pay the 121-pip floor. The structural stop over the average throws the target under 207.32. Reassess after GDP (Nov 12, 07:00 UTC).",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "One hundred four pips under the SMA200 fit inside the 121-pip floor. Weak cable did not open geometry on the cross. The desk waits for GDP."
    })

DATA = {
    "EUR/USD": EUR, "USD/JPY": USDJPY, "AUD/USD": AUD,
    "GBP/USD": GBP, "EUR/JPY": EURJPY, "GBP/JPY": GBPJPY,
}
DRIVERS = {
    "EUR/USD": {
        "en": ["New 9-month low by 3 pips", "First print, not the confirmation", "Structural target crosses four rounds"],
        "pt": ["Nova mín. de 9m por 3 pips", "Primeiro print, não a confirmação", "Alvo estrutural cruza quatro redondos"],
    },
    "USD/JPY": {
        "en": ["Back above the SMA200 by 58 pips", "SMA50 still underneath, mixed map", "160.00 still blocks a long"],
        "pt": ["De volta acima da SMA200 por 58 pips", "SMA50 ainda abaixo, mapa misto", "160.00 ainda bloqueia a compra"],
    },
    "AUD/USD": {
        "en": ["New 9-month low by 1 pip", "First print, not the confirmation", "Stop over 0.7025 has no clean path"],
        "pt": ["Nova mín. de 9m por 1 pip", "Primeiro print, não a confirmação", "Stop sobre 0.7025 sem caminho limpo"],
    },
    "GBP/USD": {
        "en": ["Back under both averages", "60 pips of air inside a 78-pip floor", "UK GDP Thursday at 0700 UTC"],
        "pt": ["De volta sob as duas médias", "60 pips de ar num piso de 78", "PIB do Reino Unido quinta às 0700 UTC"],
    },
    "EUR/JPY": {
        "en": ["150 pips above 175.68", "Euro's low did not travel here", "2025 cluster still blocks"],
        "pt": ["150 pips acima de 175,68", "A mínima do euro não chegou aqui", "Cluster de 2025 ainda bloqueia"],
    },
    "GBP/JPY": {
        "en": ["104 pips under the SMA200", "Inside the 121-pip floor", "UK GDP Thursday at 0700 UTC"],
        "pt": ["104 pips sob a SMA200", "Dentro do piso de 121", "PIB do Reino Unido quinta às 0700 UTC"],
    },
}

NEWS_ITEM_JS = r'''                {
                    date: "11/11/2026",
                    category: "flow",
                    impact: "high",
                    pairs: ["EUR/USD", "USD/JPY", "AUD/USD", "GBP/USD", "EUR/JPY", "GBP/JPY"],
                    pt: {
                        headline: "O dólar do CPI chega na quarta — euro e Aussie fazem mínima de 9 meses, e nenhum ticket arma",
                        summary: "A taxa BCE/Frankfurter de 11/11 prolonga o dólar do CPI de terça (+0,4% no mês, núcleo +0,3%). Quarta é Veterans Day nos EUA, sem dado novo do BLS. No livro: EUR/USD 1,1127 (−0,78%), nova mínima de 9 meses por 3 pips sob 1,1130 — primeiro print. AUD/USD 0,6859 (−0,65%), nova mínima de 9 meses por 1 pip sob 0,6860 — primeiro print. USD/JPY 159,23 (+0,66%) voltou para cima da SMA200, mas a SMA50 continua abaixo — mapa misto, e 160,00 bloqueia a compra. GBP/USD 1,3307 (−0,86%) devolveu as duas médias sem renovar 1.3247; o PIB britânico sai quinta às 07:00 UTC. EUR/JPY 177,18 e GBP/JPY 211,89 não abriram geometria. Os seis ficam em AGUARDAR.",
                        take: "O extremo apareceu no euro e no Aussie por um punhado de pips. A regra pede o segundo fechamento, e o 1:2 estrutural não tem caminho. O livro segue vazio."
                    },
                    en: {
                        headline: "The post-CPI dollar lands on Wednesday — euro and Aussie make 9-month lows, and no ticket arms",
                        summary: "The 11/11 ECB/Frankfurter fixing extends Tuesday's post-CPI dollar (headline +0.4% m/m, core +0.3%). Wednesday is US Veterans Day, with no new BLS release. In the book: EUR/USD 1.1127 (−0.78%), a new 9-month low by 3 pips under 1.1130 — first print. AUD/USD 0.6859 (−0.65%), a new 9-month low by 1 pip under 0.6860 — first print. USD/JPY 159.23 (+0.66%) closed back above the SMA200, but the SMA50 is still below — a mixed map, and 160.00 blocks the long. GBP/USD 1.3307 (−0.86%) handed back both averages without renewing 1.3247; UK GDP is due Thursday at 07:00 UTC. EUR/JPY 177.18 and GBP/JPY 211.89 did not open geometry. All six stay on WAIT.",
                        take: "The extreme showed up on the euro and the Aussie by a handful of pips. The rule asks for the second close, and the structural 1:2 has no path. The book stays empty."
                    }
                },
'''

NEWS_CARD = r'''                <!-- News 11/11/2026: post-CPI dollar; EUR and AUD marginal 9-month lows; all six WAIT -->
                <article class="news-card">
                    <div class="news-card-top">
                        <span class="news-cat"><span class="lang-en">Market Flow</span><span class="lang-pt" style="display:none;">Fluxo de Mercado</span></span>
                        <span class="impact-badge high"><span class="lang-en">High Impact</span><span class="lang-pt" style="display:none;">Impacto Alto</span></span>
                        <span class="news-date">11/11/2026</span>
                    </div>
                    <h2 class="news-title">
                        <span class="lang-en">The post-CPI dollar lands on Wednesday — euro and Aussie make 9-month lows, and no ticket arms</span>
                        <span class="lang-pt" style="display:none;">O dólar do CPI chega na quarta — euro e Aussie fazem mínima de 9 meses, e nenhum ticket arma</span>
                    </h2>
                    <p class="news-summary">
                        <span class="lang-en">The 11/11 ECB/Frankfurter fixing extends Tuesday's post-CPI dollar (headline +0.4% m/m, core +0.3%). Wednesday is US Veterans Day, with no new BLS release. In the book: EUR/USD 1.1127 (−0.78%), a new 9-month low by 3 pips under 1.1130 — first print. AUD/USD 0.6859 (−0.65%), a new 9-month low by 1 pip under 0.6860 — first print. USD/JPY 159.23 (+0.66%) closed back above the SMA200, but the SMA50 is still below — a mixed map, and 160.00 blocks the long. GBP/USD 1.3307 (−0.86%) handed back both averages without renewing 1.3247; UK GDP is due Thursday at 07:00 UTC. EUR/JPY 177.18 and GBP/JPY 211.89 did not open geometry. All six stay on WAIT.</span>
                        <span class="lang-pt" style="display:none;">A taxa BCE/Frankfurter de 11/11 prolonga o dólar do CPI de terça (+0,4% no mês, núcleo +0,3%). Quarta é Veterans Day nos EUA, sem dado novo do BLS. No livro: EUR/USD 1,1127 (−0,78%), nova mínima de 9 meses por 3 pips sob 1,1130 — primeiro print. AUD/USD 0,6859 (−0,65%), nova mínima de 9 meses por 1 pip sob 0,6860 — primeiro print. USD/JPY 159,23 (+0,66%) voltou para cima da SMA200, mas a SMA50 continua abaixo — mapa misto, e 160,00 bloqueia a compra. GBP/USD 1,3307 (−0,86%) devolveu as duas médias sem renovar 1.3247; o PIB britânico sai quinta às 07:00 UTC. EUR/JPY 177,18 e GBP/JPY 211,89 não abriram geometria. Os seis ficam em AGUARDAR.</span>
                    </p>
                    <div class="news-take">
                        <span class="take-tag"><span class="lang-en">Desk take</span><span class="lang-pt" style="display:none;">Leitura da mesa</span></span>
                        <span class="lang-en">The extreme showed up on the euro and the Aussie by a handful of pips. The rule asks for the second close, and the structural 1:2 has no path. The book stays empty.</span>
                        <span class="lang-pt" style="display:none;">O extremo apareceu no euro e no Aussie por um punhado de pips. A regra pede o segundo fechamento, e o 1:2 estrutural não tem caminho. O livro segue vazio.</span>
                    </div>
                    <div class="news-pairs">
                        <span class="np-label"><span class="lang-en">Watch</span><span class="lang-pt" style="display:none;">Acompanhar</span></span>
                        <a href="eur-usd.html" class="pair-link-chip">EUR/USD</a><a href="usd-jpy.html" class="pair-link-chip">USD/JPY</a><a href="aud-usd.html" class="pair-link-chip">AUD/USD</a><a href="gbp-usd.html" class="pair-link-chip">GBP/USD</a><a href="eur-jpy.html" class="pair-link-chip">EUR/JPY</a><a href="gbp-jpy.html" class="pair-link-chip">GBP/JPY</a>
                    </div>
                </article>

'''

NEW_CAL = '''                <div class="cal-cell">
                    <span class="cal-date">10/11</span>
                    <span class="cal-event"><span class="lang-en">US CPI +0.4% m/m, core +0.3%</span><span class="lang-pt" style="display:none;">CPI dos EUA +0,4% m/m, núcleo +0,3%</span></span>
                    <div class="cal-meta"><span class="cal-impact high" aria-hidden="true"></span><span class="cal-cur">USD</span></div>
                </div>
                <div class="cal-cell">
                    <span class="cal-date">11/11</span>
                    <span class="cal-event"><span class="lang-en">US Veterans Day — no BLS release</span><span class="lang-pt" style="display:none;">Veterans Day nos EUA — sem dado do BLS</span></span>
                    <div class="cal-meta"><span class="cal-impact low" aria-hidden="true"></span><span class="cal-cur">USD</span></div>
                </div>
                <div class="cal-cell">
                    <span class="cal-date">12/11</span>
                    <span class="cal-event"><span class="lang-en">UK GDP, Q3 first estimate, 07:00 UTC</span><span class="lang-pt" style="display:none;">PIB do Reino Unido, 1ª estimativa do 3º tri, 07:00 UTC</span></span>
                    <div class="cal-meta"><span class="cal-impact high" aria-hidden="true"></span><span class="cal-cur">GBP</span></div>
                </div>
                <div class="cal-cell">
                    <span class="cal-date">13/11</span>
                    <span class="cal-event"><span class="lang-en">US PPI, October, 13:30 UTC</span><span class="lang-pt" style="display:none;">PPI dos EUA, outubro, 13:30 UTC</span></span>
                    <div class="cal-meta"><span class="cal-impact med" aria-hidden="true"></span><span class="cal-cur">USD</span></div>
                </div>'''

def main():
    with open(INDEX, encoding="utf-8") as f:
        idx = f.read()
    if idx.count(OLD_TS) != 4:
        raise SystemExit("expected 4 old timestamps, found %d" % idx.count(OLD_TS))
    idx = idx.replace(OLD_TS, TS)

    start = idx.find("        const forexData = {")
    end = idx.find("        /* ==========================================\n           B. Market metadata")
    if start < 0 or end < 0:
        raise SystemExit("forexData markers missing")
    idx = idx[:start] + "        const forexData = " + json.dumps(DATA, ensure_ascii=False, indent=4) + ";\n\n" + idx[end:]

    d0 = idx.find("        const dailyChanges = {")
    d1 = idx.find("        const macroDrivers = {")
    changes = {
        "EUR/USD": "-0.78%", "USD/JPY": "+0.66%", "AUD/USD": "-0.65%",
        "GBP/USD": "-0.86%", "EUR/JPY": "-0.12%", "GBP/JPY": "-0.20%",
    }
    idx = idx[:d0] + "        const dailyChanges = " + json.dumps(changes, ensure_ascii=False, indent=4) + ";\n\n" + idx[d1:]

    m0 = idx.find("        const macroDrivers = {")
    m1 = idx.find("        /* ==========================================\n           B2. News")
    if m0 < 0 or m1 < 0:
        raise SystemExit("macroDrivers markers missing")
    idx = idx[:m0] + "        const macroDrivers = " + json.dumps(DRIVERS, ensure_ascii=False, indent=4) + ";\n\n\n" + idx[m1:]

    needle = "            items: [\n"
    at = idx.find(needle)
    if at < 0:
        raise SystemExit("news items missing")
    idx = idx[:at + len(needle)] + NEWS_ITEM_JS + idx[at + len(needle):]
    if idx.count(TS) != 4:
        raise SystemExit("timestamp count %d" % idx.count(TS))
    s = idx.find("const forexData = {"); s2 = idx.find("{", s)
    e = idx.find("\n};", s) + len("\n};")
    parsed = json.loads(idx[s2:e][:-1].rstrip())
    assert list(parsed) == list(DATA)
    with open(INDEX, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(idx)
    print("index.html patched")

    with open(LEDGER, encoding="utf-8") as f:
        ledger = json.load(f)
    assert ledger["watching"] == [] and ledger["open"] == []
    ledger["meta"]["lastUpdated"] = "11/11/2026"
    with open(LEDGER, "w", encoding="utf-8", newline="\n") as f:
        json.dump(ledger, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("ledger lastUpdated only")

    with open(NEWS, encoding="utf-8") as f:
        news = f.read()
    news = news.replace(
        "Market Wire · CPI 0.4%, Dollar Does Not Break",
        "Market Wire · Post-CPI Dollar, Two New 9-Month Lows")
    news = news.replace(
        "Telégrafo da Mesa · CPI 0,4%, Dólar Não Rompe",
        "Telégrafo da Mesa · Dólar Pós-CPI, Duas Mínimas de 9 Meses")
    news = news.replace(OLD_TS, TS)
    start = news.find('                <div class="cal-cell">')
    end = news.find("            </div>\n        </section>", start)
    if start < 0 or end < 0:
        raise SystemExit("calendar block missing")
    news = news[:start] + NEW_CAL + "\n" + news[end:]
    marker = "                <!-- News 10/11/2026 evening:"
    if marker not in news:
        raise SystemExit("news marker missing")
    news = news.replace(marker, NEWS_CARD + marker, 1)
    with open(NEWS, "w", encoding="utf-8", newline="\n") as f:
        f.write(news)
    print("news.html patched")

    with open(SITEMAP, encoding="utf-8") as f:
        sm = f.read()
    n = sm.count("2026-11-10")
    if n != 9:
        raise SystemExit("expected 9 sitemap dates, found %d" % n)
    sm = sm.replace("2026-11-10", "2026-11-11")
    with open(SITEMAP, "w", encoding="utf-8", newline="\n") as f:
        f.write(sm)
    print("sitemap patched")

    with open(VERIFY, encoding="utf-8") as f:
        v = f.read()
    v = v.replace('TODAY_TS = "10/11/2026 23:10 UTC"', 'TODAY_TS = "%s"' % TS)
    v = v.replace(
        'TODAY_DATE = "10/11/2026"  # basis session date (report edition: 10/11/2026 evening)',
        'TODAY_DATE = "11/11/2026"  # basis session date (report edition: 11/11/2026)')
    old_ticker = '''TICKER = [("EUR/USD","+0.19%"),("USD/JPY","+0.15%"),("AUD/USD","+0.14%"),
          ("GBP/USD","+0.05%"),("EUR/JPY","+0.33%"),("GBP/JPY","+0.20%")]'''
    new_ticker = '''TICKER = [("EUR/USD","-0.78%"),("USD/JPY","+0.66%"),("AUD/USD","-0.65%"),
          ("GBP/USD","-0.86%"),("EUR/JPY","-0.12%"),("GBP/JPY","-0.20%")]'''
    if old_ticker not in v:
        raise SystemExit("ticker block missing")
    v = v.replace(old_ticker, new_ticker)
    with open(VERIFY, "w", encoding="utf-8", newline="\n") as f:
        f.write(v)
    print("verify constants patched")

if __name__ == "__main__":
    main()
