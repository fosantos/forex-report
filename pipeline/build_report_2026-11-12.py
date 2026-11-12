#!/usr/bin/env python3
"""12/11/2026 edition. Thursday ECB fixing extends the dollar bid.
EUR/USD and AUD/USD print the second close through the old 9-month lows.
The 1:2 path is still blocked. No new tickets."""
import json

INDEX = r"C:/Projetos/forex-report/docs/index.html"
LEDGER = r"C:/Projetos/forex-report/docs/track-record.json"
NEWS = r"C:/Projetos/forex-report/docs/news.html"
SITEMAP = r"C:/Projetos/forex-report/docs/sitemap.xml"
VERIFY = r"C:/Projetos/forex-report/pipeline/verify_all.py"
TS = "12/11/2026 23:20 UTC"
OLD_TS = "11/11/2026 20:25 UTC"
BASIS = "584 sessions, 01/08/2024 to 12/11/2026"
BASIS_PT = "584 pregões, 01/08/2024 a 12/11/2026"

def pair(quote, bias, bias_type, pt, en):
    return {"quote": quote, "bias": bias, "biasType": bias_type, "pt": pt, "en": en}

EUR = pair("1.1081", "BAIXA", "bear",
    pt={
        "fundamental": "O EUR/USD fechou em 1,1081 na sessão de quinta 12/11/2026 (taxa de referência BCE/Frankfurter), caindo -0,41% (-46 pips) a partir de 1,1127. É o segundo fechamento sob a antiga mínima de 9 meses (1,1130) e o próprio fechamento é a nova mínima de 9 meses e de 10/20 pregões. O extremo maior ficou confirmado. O piso de 1,5σ20 é de 63 pips. Um stop sobre 1.1130 fica a 49 pips e não paga o piso. Um stop sobre a máxima de 10/20 pregões (1.1267, ~186 pips) joga o 1:2 em 1.0709, através de 1.1000, 1.0950 e 1.0900. O stop no piso, em 1.1144, joga o 1:2 em 1.0955, e 1.1000 fica no caminho. O Fed segue em 3,75-4,00%. O PPI americano sai sexta 13/11 às 13:30 UTC. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (1,1532) com a SMA50 (1,1312) abaixo dela — alinhamento de baixa pleno. O próprio fechamento é a mínima de 10/20 pregões e de 9 meses.",
        "support": "1.1081 (mínima de 9 meses e de 10/20 pregões, 12/11), com o redondo 1.1000 abaixo.",
        "resistance": "1.1130 (a mínima antiga, agora devolvida) e 1.1267 (máxima de 10/20 pregões, 04/11). A Fib 78,6% está em 1,1256. A SMA50 está em 1,1312.",
        "priceAction": "Segundo fechamento sob 1.1130, mais 46 pips. A confirmação chegou e o 1:2 continua sem caminho limpo. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "O segundo fechamento sob 1,1130 já saiu. O stop que respeita o piso de 63 pips coloca 1.1000 no meio do caminho até o 1:2. Sem gatilho novo.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "A regra do extremo maior foi cumprida. O livro mesmo assim não paga: o stop curto não cobre o piso e o stop que cobre o piso esbarra em 1.1000."
    },
    en={
        "fundamental": "EUR/USD closed at 1.1081 in the Thursday 12/11/2026 session (ECB/Frankfurter reference rate), down -0.41% (-46 pips) from 1.1127. It is the second close under the old 9-month low (1.1130) and today's close is the new 9-month and 10/20-day low. The major extreme is confirmed. The 1.5-sigma20 floor is 63 pips. A stop over 1.1130 is 49 pips and misses the floor. A stop over the 10/20-day high (1.1267, ~186 pips) puts the 1:2 at 1.0709, through 1.1000, 1.0950 and 1.0900. The floor stop, at 1.1144, puts the 1:2 at 1.0955, and 1.1000 sits in the path. The Fed is still at 3.75-4.00%. US PPI is due Friday Nov 13 at 13:30 UTC. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (1.1532) with the 50-day (1.1312) below it — full bear alignment. Today's close is the 10/20-day and 9-month low.",
        "support": "1.1081 (the 9-month and 10/20-day low, Nov 12), with the 1.1000 round below.",
        "resistance": "1.1130 (the old low, now handed back) and 1.1267 (the 10/20-day high, Nov 4). The 78.6% Fib is at 1.1256. The SMA50 is at 1.1312.",
        "priceAction": "Second close under 1.1130, another 46 pips. The confirmation arrived and the 1:2 still has no clean path. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The second close under 1.1130 has printed. The stop that respects the 63-pip floor puts 1.1000 in the middle of the path to the 1:2. No new trigger.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The major-extreme rule is met. The book still does not pay: the short stop misses the floor and the stop that clears the floor runs into 1.1000."
    })

USDJPY = pair("159.70", "NEUTRO", "neutral",
    pt={
        "fundamental": "O USD/JPY fechou em 159,70 na sessão de quinta 12/11/2026 (taxa de referência BCE/Frankfurter), subindo +0,30% (+47 pips). É o segundo fechamento acima de 159,23 e a nova máxima de 10/20 pregões. O preço está 103 pips acima da SMA200 (158,67). A SMA50 (157,31) continua sob a SMA200 — alinhamento misto. O piso de 1,5σ20 é de 71 pips, então um stop sob a SMA200 cabe. O 1:2 desse stop cai perto de 161,76, e o redondo 160,00 está a 30 pips. O BoJ segue em 1,25%. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento acima da SMA200 (158,67), com a SMA50 (157,31) ainda abaixo — alinhamento misto. A máxima de 9 meses segue 163,91.",
        "support": "158.67 (a SMA200) e 159.23 (a máxima de ontem), com a SMA50 em 157,31.",
        "resistance": "159.70 (máxima de 10/20 pregões, o próprio fechamento) e o redondo 160,00, com a máxima de 9 meses em 163,91.",
        "priceAction": "Segundo fechamento na máxima de 20 pregões, mapa ainda misto. 160,00 bloqueia o 1:2. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "O segundo fechamento acima de 159,23 saiu. Comprar com stop sob a SMA200 esbarra em 160,00 antes do 1:2. Vender contra a máxima não tem alinhamento.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O iene cedeu de novo, e a SMA50 ainda não cruzou. O stop estrutural cabe no piso, mas 30 pips de ar até 160,00 não são um caminho de 1:2."
    },
    en={
        "fundamental": "USD/JPY closed at 159.70 in the Thursday 12/11/2026 session (ECB/Frankfurter reference rate), up +0.30% (+47 pips). It is the second close above 159.23 and the new 10/20-day high. Price is 103 pips above the SMA200 (158.67). The SMA50 (157.31) is still under the SMA200 — mixed alignment. The 1.5-sigma20 floor is 71 pips, so a stop under the SMA200 fits. The 1:2 of that stop lands near 161.76, and the 160.00 round is 30 pips away. The BoJ is still at 1.25%. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close above the SMA200 (158.67), with the SMA50 (157.31) still below — mixed alignment. The 9-month high remains 163.91.",
        "support": "158.67 (the SMA200) and 159.23 (yesterday's high), with the SMA50 at 157.31.",
        "resistance": "159.70 (the 10/20-day high, today's close) and the 160.00 round, with the 9-month high at 163.91.",
        "priceAction": "Second close at the 20-day high, map still mixed. 160.00 blocks the 1:2. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The second close above 159.23 has printed. A long with a stop under the SMA200 runs into 160.00 before the 1:2. A short against the high has no alignment.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The yen gave way again, and the SMA50 still has not crossed. The structural stop fits the floor, but 30 pips of air up to 160.00 is not a 1:2 path."
    })

AUD = pair("0.6821", "BAIXA", "bear",
    pt={
        "fundamental": "O AUD/USD fechou em 0,6821 na sessão de quinta 12/11/2026 (taxa de referência BCE/Frankfurter), caindo -0,56% (-38 pips). É o segundo fechamento sob a antiga mínima de 9 meses (0,6860) e a nova mínima de 9 meses e de 10/20 pregões. O extremo ficou confirmado. A SMA50 (0,7026) está sob a SMA200 (0,7054). O piso de 1,5σ20 é de 57 pips. Um stop sobre 0,6860 fica a 39 pips e não paga o piso. O stop no piso, em 0,6878, joga o 1:2 em 0,6707, e o redondo 0,6800 está a 21 pips. Um stop sobre 0,7024 (~203 pips) atravessa 0,6800, 0,6700 e 0,6600. O RBA está em 4,85%. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (0,7054) com a SMA50 (0,7026) abaixo dela — alinhamento de baixa. O próprio fechamento é a mínima de 10/20 pregões e de 9 meses.",
        "support": "0.6821 (mínima de 9 meses e de 10/20 pregões, 12/11), com o redondo 0.6800 logo abaixo.",
        "resistance": "0.6860 (a mínima antiga) e 0.7024 (máxima de 10 pregões), com a SMA50 (0,7026) e a SMA200 (0,7054) no teto.",
        "priceAction": "Segundo fechamento sob 0,6860, mais 38 pips. Confirmação sem caminho de 1:2. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "O segundo fechamento sob 0,6860 já saiu. O stop no piso esbarra em 0,6800. O stop sobre 0,7024 atravessa três redondos.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O Aussie confirmou a mínima de 9 meses. O stop curto não cobre o piso de 57 pips, e o stop que cobre esbarra em 0,6800."
    },
    en={
        "fundamental": "AUD/USD closed at 0.6821 in the Thursday 12/11/2026 session (ECB/Frankfurter reference rate), down -0.56% (-38 pips). It is the second close under the old 9-month low (0.6860) and the new 9-month and 10/20-day low. The extreme is confirmed. The SMA50 (0.7026) sits under the SMA200 (0.7054). The 1.5-sigma20 floor is 57 pips. A stop over 0.6860 is 39 pips and misses the floor. The floor stop, at 0.6878, puts the 1:2 at 0.6707, and the 0.6800 round is 21 pips away. A stop over 0.7024 (~203 pips) crosses 0.6800, 0.6700 and 0.6600. The RBA cash rate is 4.85%. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (0.7054) with the SMA50 (0.7026) below it — bear alignment. Today's close is the 10/20-day and 9-month low.",
        "support": "0.6821 (the 9-month and 10/20-day low, Nov 12), with the 0.6800 round just below.",
        "resistance": "0.6860 (the old low) and 0.7024 (the 10-day high), with the SMA50 (0.7026) and the SMA200 (0.7054) as the ceiling.",
        "priceAction": "Second close under 0.6860, another 38 pips. Confirmation without a 1:2 path. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The second close under 0.6860 has printed. The floor stop runs into 0.6800. The stop over 0.7024 crosses three rounds.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The Aussie confirmed the 9-month low. The short stop misses the 57-pip floor, and the stop that clears it runs into 0.6800."
    })

GBP = pair("1.3256", "BAIXA", "bear",
    pt={
        "fundamental": "O GBP/USD fechou em 1,3256 na sessão de quinta 12/11/2026 (taxa de referência BCE/Frankfurter), caindo -0,39% (-51 pips). O fechamento ficou sob a mínima de 10 pregões de quarta (1,3307) e é a nova mínima da janela de 10/20 pregões. A mínima de 9 meses segue 1.3160. O PIB do Reino Unido saiu a +0,7% no 3º trimestre (consenso 0,7%, depois de 0,5%) e +0,2% em setembro (ONS, 12/11, 07:00 UTC). Este print já contém o dado, e o cabo caiu mesmo assim. Alinhamento de baixa (fechamento sob a SMA200 1,3420 e sob a SMA50 1,3353). O piso é de 80 pips. Um stop sobre 1.3307 fica a 51 pips e não paga o piso. O stop no piso, em 1.3336, joga o 1:2 em 1.3096, através de 1.3200 e de 1.3160. A Bank Rate está em 4,00%. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (1,3420) e sob a SMA50 (1,3353), com a SMA50 abaixo da SMA200 — alinhamento de baixa. A máxima de 10/20 pregões segue 1.3500.",
        "support": "1.3256 (mínima da janela de 10/20 pregões, 12/11), com 1.3200 e a mínima de 9 meses em 1.3160 abaixo.",
        "resistance": "1.3307 (a mínima de quarta, devolvida) e 1.3353 (a SMA50), com a SMA200 em 1,3420.",
        "priceAction": "PIB em linha com o consenso e o cabo fez nova mínima da janela. O 1:2 atravessa 1.3160. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "O fechamento sob 1,3307 saiu. O stop que respeita o piso de 80 pips coloca 1.3200 e 1.3160 no caminho. Sem gatilho novo.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O PIB de 0,7% não segurou a libra. A venda sob 1.3307 existe no gráfico, mas o alvo de 1:2 cai depois da mínima de 9 meses."
    },
    en={
        "fundamental": "GBP/USD closed at 1.3256 in the Thursday 12/11/2026 session (ECB/Frankfurter reference rate), down -0.39% (-51 pips). The close finished under Wednesday's 10-day low (1.3307) and is the new low of the 10/20-day window. The 9-month low is still 1.3160. UK GDP printed +0.7% in Q3 (consensus 0.7%, after 0.5%) and +0.2% in September (ONS, Nov 12, 07:00 UTC). This print already contains the release, and cable fell anyway. Bear alignment (close under the SMA200 1.3420 and under the SMA50 1.3353). The floor is 80 pips. A stop over 1.3307 is 51 pips and misses the floor. The floor stop, at 1.3336, puts the 1:2 at 1.3096, through 1.3200 and 1.3160. Bank Rate is 4.00%. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (1.3420) and under the SMA50 (1.3353), with the SMA50 below the SMA200 — bear alignment. The 10/20-day high is still 1.3500.",
        "support": "1.3256 (the low of the 10/20-day window, Nov 12), with 1.3200 and the 9-month low at 1.3160 below.",
        "resistance": "1.3307 (Wednesday's low, handed back) and 1.3353 (the SMA50), with the SMA200 at 1.3420.",
        "priceAction": "GDP in line with consensus and cable made a new window low. The 1:2 crosses 1.3160. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The close under 1.3307 has printed. The stop that respects the 80-pip floor puts 1.3200 and 1.3160 in the path. No new trigger.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "GDP at 0.7% did not hold the pound. The short under 1.3307 is on the chart, but the 1:2 target falls past the 9-month low."
    })

EURJPY = pair("176.96", "BAIXA", "bear",
    pt={
        "fundamental": "O EUR/JPY fechou em 176,96 na sessão de quinta 12/11/2026 (taxa de referência BCE/Frankfurter), caindo -0,12% (-22 pips). A mínima de 10 pregões segue 175,68 e a de 9 meses / 20 pregões 175,51. O fechamento ficou 128 pips acima de 175,68, além do piso de 103. Uma venda sob 175,68 com stop sobre 178,30 (~262 pips) joga o 1:2 dentro do cluster de set-out/2025. Alinhamento de baixa (fechamento sob a SMA200 182,96 e a SMA50 177,93). O euro fez mínima contra o dólar; contra o iene, não. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (182,96) com a SMA50 (177,93) abaixo dela — alinhamento de baixa pleno. A máxima de 10/20 pregões está em 178,30 (04/11).",
        "support": "175.68 (mínima de 10 pregões, 30/10) e 175.51 (mínima de 9 meses e de 20 pregões, 23/10), com o redondo 175,00 abaixo.",
        "resistance": "178.30 (máxima de 10/20 pregões, 04/11) e a SMA50 (177,93).",
        "priceAction": "Queda de 22 pips, ainda 128 pips acima do gatilho. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "O fechamento sob 175,68 continua sendo a regra do extremo. O stop sobre 178,30 coloca o alvo no cluster de 2025.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "A mínima do euro não passou para o cruzado. 128 pips separam o preço de 175,68, e o stop estrutural empurra o alvo para 2025."
    },
    en={
        "fundamental": "EUR/JPY closed at 176.96 in the Thursday 12/11/2026 session (ECB/Frankfurter reference rate), down -0.12% (-22 pips). The 10-day low is still 175.68 and the 9-month / 20-day low is 175.51. The close finished 128 pips above 175.68, beyond the 103-pip floor. A short under 175.68 with a stop over 178.30 (~262 pips) puts the 1:2 inside the Sep-Oct 2025 cluster. Bear alignment (close under the SMA200 182.96 and the SMA50 177.93). The euro made a low against the dollar; against the yen, it did not. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (182.96) with the SMA50 (177.93) below it — full bear alignment. The 10/20-day high is 178.30 (Nov 4).",
        "support": "175.68 (the 10-day low, Oct 30) and 175.51 (the 9-month and 20-day low, Oct 23), with the 175.00 round below.",
        "resistance": "178.30 (the 10/20-day high, Nov 4) and the SMA50 (177.93).",
        "priceAction": "A 22-pip dip, still 128 pips above the trigger. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The close under 175.68 is still the extreme's rule. The stop over 178.30 puts the target in the 2025 cluster.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The euro's low did not pass through to the cross. 128 pips separate price from 175.68, and the structural stop pushes the target into 2025."
    })

GBPJPY = pair("211.69", "BAIXA", "bear",
    pt={
        "fundamental": "O GBP/JPY fechou em 211,69 na sessão de quinta 12/11/2026 (taxa de referência BCE/Frankfurter), caindo -0,09% (-20 pips). Ficou 124 pips sob a SMA200 (212,93), pouco além do piso de 116, e acima da SMA50 (210,04). Alinhamento de baixa. A mínima de 10 pregões está em 210,70 e a de 20 pregões em 209,61. Um stop sobre a SMA200 (~124 pips) joga o 1:2 perto de 209,21, através de 210,70 e de 209,61. A mínima de 9 meses segue 207,32. BoE em 4,00%, BoJ em 1,25%. O PIB britânico de 0,7% já está neste print. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (212,93) com a SMA50 (210,04) abaixo dela — alinhamento de baixa. A máxima de 10/20 pregões está em 213,63 (04/11).",
        "support": "210.70 (mínima de 10 pregões) e 209.61 (mínima de 20 pregões), com a mínima de 9 meses em 207,32.",
        "resistance": "212.93 (a SMA200) e 213.63 (máxima de 10/20 pregões). A Fib 50% está em 213,23.",
        "priceAction": "Quase parado, 124 pips sob a média longa. O 1:2 de um stop sobre a SMA200 cruza as duas mínimas da janela. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "Vender aqui com stop sobre 212,93 cabe no piso de 116 pips, mas o alvo atravessa 210,70 e 209,61. Sem gatilho limpo.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O cabo fraco não abriu o cruzado. O stop na SMA200 agora passa do piso, e o caminho até o 1:2 ainda está ocupado pelas mínimas de 10 e de 20 pregões."
    },
    en={
        "fundamental": "GBP/JPY closed at 211.69 in the Thursday 12/11/2026 session (ECB/Frankfurter reference rate), down -0.09% (-20 pips). It finished 124 pips under the SMA200 (212.93), just beyond the 116-pip floor, and above the SMA50 (210.04). Bear alignment. The 10-day low is 210.70 and the 20-day low is 209.61. A stop over the SMA200 (~124 pips) puts the 1:2 near 209.21, through 210.70 and 209.61. The 9-month low is still 207.32. BoE at 4.00%, BoJ at 1.25%. UK GDP at 0.7% is already in this print. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (212.93) with the SMA50 (210.04) below it — bear alignment. The 10/20-day high is 213.63 (Nov 4).",
        "support": "210.70 (the 10-day low) and 209.61 (the 20-day low), with the 9-month low at 207.32.",
        "resistance": "212.93 (the SMA200) and 213.63 (the 10/20-day high). The 50% Fib is at 213.23.",
        "priceAction": "Almost unchanged, 124 pips under the long average. The 1:2 of a stop over the SMA200 crosses both window lows. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "Selling here with a stop over 212.93 fits the 116-pip floor, but the target crosses 210.70 and 209.61. No clean trigger.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "Weak cable did not open the cross. The SMA200 stop now clears the floor, and the path to the 1:2 is still occupied by the 10-day and 20-day lows."
    })

DATA = {
    "EUR/USD": EUR, "USD/JPY": USDJPY, "AUD/USD": AUD,
    "GBP/USD": GBP, "EUR/JPY": EURJPY, "GBP/JPY": GBPJPY,
}
DRIVERS = {
    "EUR/USD": {
        "en": ["Second close under 1.1130", "New 9-month low at 1.1081", "1.1000 blocks the reward"],
        "pt": ["Segundo fechamento sob 1.1130", "Nova mín. de 9m em 1.1081", "1.1000 bloqueia o alvo"],
    },
    "USD/JPY": {
        "en": ["Second close above 159.23", "103 pips over the SMA200, map mixed", "160.00 blocks the long"],
        "pt": ["Segundo fechamento acima de 159.23", "103 pips sobre a SMA200, mapa misto", "160.00 bloqueia a compra"],
    },
    "AUD/USD": {
        "en": ["Second close under 0.6860", "New 9-month low at 0.6821", "0.6800 blocks the reward"],
        "pt": ["Segundo fechamento sob 0.6860", "Nova mín. de 9m em 0.6821", "0.6800 bloqueia o alvo"],
    },
    "GBP/USD": {
        "en": ["UK GDP 0.7%, in line", "Close under Wednesday's 1.3307", "9-month low 1.3160 still below"],
        "pt": ["PIB do Reino Unido 0,7%, em linha", "Fechamento sob 1.3307 de quarta", "Mín. de 9m 1.3160 ainda abaixo"],
    },
    "EUR/JPY": {
        "en": ["128 pips above 175.68", "Euro's low did not travel here", "2025 cluster still blocks"],
        "pt": ["128 pips acima de 175,68", "A mínima do euro não chegou aqui", "Cluster de 2025 ainda bloqueia"],
    },
    "GBP/JPY": {
        "en": ["124 pips under the SMA200", "Just beyond the 116-pip floor", "210.70 and 209.61 still in the path"],
        "pt": ["124 pips sob a SMA200", "Pouco além do piso de 116", "210.70 e 209.61 ainda no caminho"],
    },
}

NEWS_ITEM_JS = r'''                {
                    date: "12/11/2026",
                    category: "macro",
                    impact: "high",
                    pairs: ["EUR/USD", "USD/JPY", "AUD/USD", "GBP/USD", "EUR/JPY", "GBP/JPY"],
                    pt: {
                        headline: "Segundo fechamento nas mínimas do euro e do Aussie — o 1:2 continua sem caminho",
                        summary: "A taxa BCE/Frankfurter de 12/11 estende o dólar. EUR/USD fechou 1,1081 (−0,41%), segundo fechamento sob 1,1130 e nova mínima de 9 meses. AUD/USD fechou 0,6821 (−0,56%), segundo fechamento sob 0,6860. Nos dois, o stop no piso esbarra num redondo (1.1000 e 0.6800). USD/JPY 159,70 (+0,30%) fez o segundo fechamento acima de 159,23, mapa ainda misto, com 160,00 no caminho. GBP/USD 1,3256 (−0,39%) ficou sob 1,3307 depois do PIB britânico a +0,7% no trimestre, em linha com o consenso (ONS, 07:00 UTC); 1.3160 ainda bloqueia o alvo. EUR/JPY 176,96 e GBP/JPY 211,69 sem gatilho. Os seis ficam em AGUARDAR. PPI americano sexta às 13:30 UTC.",
                        take: "A confirmação que a quarta não tinha chegou na quinta. O portão de 1:2 continua fechado pelos redondos e pela mínima de 9 meses da libra. O livro segue vazio."
                    },
                    en: {
                        headline: "Second close at the euro and Aussie lows — the 1:2 still has no path",
                        summary: "The 12/11 ECB/Frankfurter fixing extends the dollar. EUR/USD closed 1.1081 (−0.41%), the second close under 1.1130 and a new 9-month low. AUD/USD closed 0.6821 (−0.56%), the second close under 0.6860. On both, the floor stop runs into a round (1.1000 and 0.6800). USD/JPY 159.70 (+0.30%) printed the second close above 159.23, map still mixed, with 160.00 in the path. GBP/USD 1.3256 (−0.39%) closed under 1.3307 after UK GDP at +0.7% on the quarter, in line with consensus (ONS, 07:00 UTC); 1.3160 still blocks the target. EUR/JPY 176.96 and GBP/JPY 211.69 have no trigger. All six stay on WAIT. US PPI is Friday at 13:30 UTC.",
                        take: "The confirmation Wednesday did not have arrived on Thursday. The 1:2 gate stays shut by the rounds and by cable's 9-month low. The book stays empty."
                    }
                },
'''

NEWS_CARD = r'''                <!-- News 12/11/2026: second closes through the euro and Aussie 9-month lows; all six WAIT -->
                <article class="news-card">
                    <div class="news-card-top">
                        <span class="news-cat"><span class="lang-en">Macro Data</span><span class="lang-pt" style="display:none;">Dados Macro</span></span>
                        <span class="impact-badge high"><span class="lang-en">High Impact</span><span class="lang-pt" style="display:none;">Impacto Alto</span></span>
                        <span class="news-date">12/11/2026</span>
                    </div>
                    <h2 class="news-title">
                        <span class="lang-en">Second close at the euro and Aussie lows — the 1:2 still has no path</span>
                        <span class="lang-pt" style="display:none;">Segundo fechamento nas mínimas do euro e do Aussie — o 1:2 continua sem caminho</span>
                    </h2>
                    <p class="news-summary">
                        <span class="lang-en">The 12/11 ECB/Frankfurter fixing extends the dollar. EUR/USD closed 1.1081 (−0.41%), the second close under 1.1130 and a new 9-month low. AUD/USD closed 0.6821 (−0.56%), the second close under 0.6860. On both, the floor stop runs into a round (1.1000 and 0.6800). USD/JPY 159.70 (+0.30%) printed the second close above 159.23, map still mixed, with 160.00 in the path. GBP/USD 1.3256 (−0.39%) closed under 1.3307 after UK GDP at +0.7% on the quarter, in line with consensus (ONS, 07:00 UTC); 1.3160 still blocks the target. EUR/JPY 176.96 and GBP/JPY 211.69 have no trigger. All six stay on WAIT. US PPI is Friday at 13:30 UTC.</span>
                        <span class="lang-pt" style="display:none;">A taxa BCE/Frankfurter de 12/11 estende o dólar. EUR/USD fechou 1,1081 (−0,41%), segundo fechamento sob 1,1130 e nova mínima de 9 meses. AUD/USD fechou 0,6821 (−0,56%), segundo fechamento sob 0,6860. Nos dois, o stop no piso esbarra num redondo (1.1000 e 0.6800). USD/JPY 159,70 (+0,30%) fez o segundo fechamento acima de 159,23, mapa ainda misto, com 160,00 no caminho. GBP/USD 1,3256 (−0,39%) ficou sob 1,3307 depois do PIB britânico a +0,7% no trimestre, em linha com o consenso (ONS, 07:00 UTC); 1.3160 ainda bloqueia o alvo. EUR/JPY 176,96 e GBP/JPY 211,69 sem gatilho. Os seis ficam em AGUARDAR. PPI americano sexta às 13:30 UTC.</span>
                    </p>
                    <div class="news-take">
                        <span class="take-tag"><span class="lang-en">Desk take</span><span class="lang-pt" style="display:none;">Leitura da mesa</span></span>
                        <span class="lang-en">The confirmation Wednesday did not have arrived on Thursday. The 1:2 gate stays shut by the rounds and by cable's 9-month low. The book stays empty.</span>
                        <span class="lang-pt" style="display:none;">A confirmação que a quarta não tinha chegou na quinta. O portão de 1:2 continua fechado pelos redondos e pela mínima de 9 meses da libra. O livro segue vazio.</span>
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
                    <span class="cal-date">12/11</span>
                    <span class="cal-event"><span class="lang-en">UK GDP +0.7% q/q, in line (ONS)</span><span class="lang-pt" style="display:none;">PIB do Reino Unido +0,7% t/t, em linha (ONS)</span></span>
                    <div class="cal-meta"><span class="cal-impact high" aria-hidden="true"></span><span class="cal-cur">GBP</span></div>
                </div>
                <div class="cal-cell">
                    <span class="cal-date">13/11</span>
                    <span class="cal-event"><span class="lang-en">US PPI, October, 13:30 UTC</span><span class="lang-pt" style="display:none;">PPI dos EUA, outubro, 13:30 UTC</span></span>
                    <div class="cal-meta"><span class="cal-impact med" aria-hidden="true"></span><span class="cal-cur">USD</span></div>
                </div>
                <div class="cal-cell">
                    <span class="cal-date">09/12</span>
                    <span class="cal-event"><span class="lang-en">FOMC decision, hike debate 25 or 50 bp</span><span class="lang-pt" style="display:none;">Decisão do FOMC, debate de alta de 25 ou 50 pb</span></span>
                    <div class="cal-meta"><span class="cal-impact high" aria-hidden="true"></span><span class="cal-cur">USD</span></div>
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
        "EUR/USD": "-0.41%", "USD/JPY": "+0.30%", "AUD/USD": "-0.56%",
        "GBP/USD": "-0.39%", "EUR/JPY": "-0.12%", "GBP/JPY": "-0.09%",
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
    ledger["meta"]["lastUpdated"] = "12/11/2026"
    with open(LEDGER, "w", encoding="utf-8", newline="\n") as f:
        json.dump(ledger, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("ledger lastUpdated only")

    with open(NEWS, encoding="utf-8") as f:
        news = f.read()
    news = news.replace(
        "Market Wire · Post-CPI Dollar, Two New 9-Month Lows",
        "Market Wire · Second Close, Still No Ticket")
    news = news.replace(
        "Telégrafo da Mesa · Dólar Pós-CPI, Duas Mínimas de 9 Meses",
        "Telégrafo da Mesa · Segundo Fechamento, Ainda Sem Ticket")
    news = news.replace(OLD_TS, TS)
    start = news.find('                <div class="cal-cell">')
    end = news.find("            </div>\n        </section>", start)
    if start < 0 or end < 0:
        raise SystemExit("calendar block missing")
    news = news[:start] + NEW_CAL + "\n" + news[end:]
    marker = "                <!-- News 11/11/2026:"
    if marker not in news:
        raise SystemExit("news marker missing")
    news = news.replace(marker, NEWS_CARD + marker, 1)
    with open(NEWS, "w", encoding="utf-8", newline="\n") as f:
        f.write(news)
    print("news.html patched")

    with open(SITEMAP, encoding="utf-8") as f:
        sm = f.read()
    n = sm.count("2026-11-11")
    if n != 9:
        raise SystemExit("expected 9 sitemap dates, found %d" % n)
    sm = sm.replace("2026-11-11", "2026-11-12")
    with open(SITEMAP, "w", encoding="utf-8", newline="\n") as f:
        f.write(sm)
    print("sitemap patched")

    with open(VERIFY, encoding="utf-8") as f:
        v = f.read()
    v = v.replace('TODAY_TS = "11/11/2026 20:25 UTC"', 'TODAY_TS = "%s"' % TS)
    v = v.replace(
        'TODAY_DATE = "11/11/2026"  # basis session date (report edition: 11/11/2026)',
        'TODAY_DATE = "12/11/2026"  # basis session date (report edition: 12/11/2026)')
    old_ticker = '''TICKER = [("EUR/USD","-0.78%"),("USD/JPY","+0.66%"),("AUD/USD","-0.65%"),
          ("GBP/USD","-0.86%"),("EUR/JPY","-0.12%"),("GBP/JPY","-0.20%")]'''
    new_ticker = '''TICKER = [("EUR/USD","-0.41%"),("USD/JPY","+0.30%"),("AUD/USD","-0.56%"),
          ("GBP/USD","-0.39%"),("EUR/JPY","-0.12%"),("GBP/JPY","-0.09%")]'''
    if old_ticker not in v:
        raise SystemExit("ticker block missing")
    v = v.replace(old_ticker, new_ticker)
    with open(VERIFY, "w", encoding="utf-8", newline="\n") as f:
        f.write(v)
    print("verify constants patched")

if __name__ == "__main__":
    main()
