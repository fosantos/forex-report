#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""16/11/2026 edition, on the Monday 16/11 ECB fixing.

The dollar extends: EUR/USD 1.1014 and AUD/USD 0.6757 make a second close
through Friday's 9-month lows, and both stops that meet the floor run through
the next round. USD/JPY gives 160 back to 159.60 after Japan's Q3 GDP
contracts. MoF jawboning of 12-13/11 is still inside 30 days, so the yen
floor stays at 2.5-sigma20. No ticket clears the gate.
"""
import json
from datetime import datetime, timezone

INDEX = r"C:/Projetos/forex-report/docs/index.html"
LEDGER = r"C:/Projetos/forex-report/docs/track-record.json"
NEWS = r"C:/Projetos/forex-report/docs/news.html"
SITEMAP = r"C:/Projetos/forex-report/docs/sitemap.xml"
VERIFY = r"C:/Projetos/forex-report/pipeline/verify_all.py"

TS = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
OLD_TS = "14/11/2026 23:20 UTC"
BASIS = "586 sessions, 01/08/2024 to 16/11/2026"
BASIS_PT = "586 pregões, 01/08/2024 a 16/11/2026"

def pair(quote, bias, bias_type, pt, en):
    return {"quote": quote, "bias": bias, "biasType": bias_type, "pt": pt, "en": en}

EUR = pair("1.1014", "BAIXA", "bear",
    pt={
        "fundamental": "O EUR/USD fechou em 1,1014 na sessão de segunda 16/11/2026 (taxa de referência BCE/Frankfurter; o terminal MT5 está logado, mas o Market Watch não tem os pares à vista), caindo -0,34% (-38 pips) a partir de 1,1052. É o segundo fechamento através da mínima de 9 meses de sexta, e o próprio fechamento é a nova mínima de 10/20 pregões e de 9 meses. O Fed segue em 3,75-4,00%, com a decisão de 8-9/12 ainda no debate de 25 ou 50 pb. Até o redondo 1.1000 são 14 pips. O piso de 1,5σ20 é de 61 pips, então o stop que paga o piso já atravessa 1.1000. Um 1:2 que pare antes do redondo exigiria um stop de no máximo 7 pips. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (1,1524) com a SMA50 (1,1289) abaixo dela — alinhamento de baixa pleno. O próprio fechamento é a mínima de 10/20 pregões e de 9 meses. A máxima de 10/20 pregões segue 1.1267 (04/11).",
        "support": "1.1000 (o redondo, 14 pips abaixo). O fechamento de 16/11 (1,1014) é a mínima de 9 meses.",
        "resistance": "1.1052 (a mínima de sexta, devolvida) e 1.1081 (a mínima de quinta), com a máxima de 10/20 pregões em 1.1267 e a SMA50 em 1,1289.",
        "priceAction": "O segundo fechamento sob 1,1052 encurtou o ar até 1.1000 para 14 pips, dentro do piso de 61. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "A confirmação da mínima de 9 meses saiu. 1.1000 está mais perto do que o piso permite: o stop de 61 pips já cai do outro lado do redondo. Sem gatilho novo.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O euro entregou o segundo fechamento que a regra pede e o livro continua sem vender. O espaço até 1.1000 não cabe um stop legal."
    },
    en={
        "fundamental": "EUR/USD closed at 1.1014 in the Monday 16/11/2026 session (ECB/Frankfurter reference rate; the MT5 terminal is logged in, but Market Watch has no spot pairs), down -0.34% (-38 pips) from 1.1052. It is the second close through Friday's 9-month low, and today's close is the new 10/20-day and 9-month low. The Fed is still at 3.75-4.00%, with the Dec 8-9 decision still a 25-or-50 bp debate. The 1.1000 round is 14 pips away. The 1.5-sigma20 floor is 61 pips, so the stop that meets the floor is already through 1.1000. A 1:2 that stops before the round would need a stop of 7 pips at most. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (1.1524) with the 50-day (1.1289) below it — full bear alignment. Today's close is the 10/20-day and 9-month low. The 10/20-day high is still 1.1267 (Nov 4).",
        "support": "1.1000 (the round, 14 pips below). The Nov-16 close (1.1014) is the 9-month low.",
        "resistance": "1.1052 (Friday's low, handed back) and 1.1081 (Thursday's low), with the 10/20-day high at 1.1267 and the SMA50 at 1.1289.",
        "priceAction": "The second close under 1.1052 cut the air down to 1.1000 to 14 pips, inside the 61-pip floor. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The confirming close through the 9-month low has printed. 1.1000 is closer than the floor allows: the 61-pip stop already lands on the other side of the round. No new trigger.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The euro delivered the second close the rule asks for and the book still does not sell. The room to 1.1000 does not fit a legal stop."
    })

USDJPY = pair("159.60", "NEUTRO", "neutral",
    pt={
        "fundamental": "O USD/JPY fechou em 159,60 na sessão de segunda 16/11/2026 (taxa de referência BCE/Frankfurter), caindo -0,25% (-40 pips) a partir de 160,00. O fechamento devolveu o redondo. A máxima de 10 pregões segue 160,00 (sexta). O PIB do Japão no 3º trimestre caiu 0,02% no trimestre e -0,1% anualizado, a primeira contração em quatro trimestres, com o consumo privado a -0,3% (Gabinete, 16/11). O aviso de Katayama de 13/11 continua dentro de 30 dias: o piso dos pares com iene segue em 2,5σ20, aqui 121 pips. O mapa continua misto — fechamento acima da SMA200 (158,71), SMA50 (157,48) ainda abaixo. Daqui até a SMA200 são 89 pips, menos que o piso. Um stop sob a SMA50 (~212 pips) cabe, e o 1:2 atravessa 160, 161 e 162 até a máxima de 9 meses em 163,91. Não há alinhamento de alta, e segunda não fechou acima de 160. O BoJ segue em 1,25%. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento acima da SMA200 (158,71), com a SMA50 (157,48) ainda abaixo — alinhamento misto. A máxima de 9 meses segue 163,91. A máxima de 10 pregões é 160,00 (13/11).",
        "support": "158.71 (a SMA200, 89 pips abaixo) e 157.95 (mínima de 10 pregões, 09/11), com a SMA50 em 157,48.",
        "resistance": "160.00 (máxima de 10 pregões, o fechamento de sexta) e 161.00, com a máxima de 9 meses em 163,91.",
        "priceAction": "O redondo foi devolvido. 89 pips até a SMA200 não pagam o piso de 121. O 1:2 de um stop que paga cruza 160, 161 e 162. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "160.00 não foi sustentado. Comprar 159,60 com stop sob a SMA200 falha o piso de 121 pips. O stop que paga o piso esbarra em três redondos. Vender contra o fechamento não tem alinhamento de baixa. Reavaliar se o MoF agir, ou depois do FOMC de 8-9/12.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O iene recuperou 40 pips e o PIB veio negativo, mas o livro não compra a devolução de 160. O piso de 2,5σ20 continua mais largo que a distância até a SMA200."
    },
    en={
        "fundamental": "USD/JPY closed at 159.60 in the Monday 16/11/2026 session (ECB/Frankfurter reference rate), down -0.25% (-40 pips) from 160.00. The close handed the round back. The 10-day high is still 160.00 (Friday). Japan's Q3 GDP fell 0.02% on the quarter and -0.1% annualized, the first contraction in four quarters, with private consumption at -0.3% (Cabinet Office, Nov 16). Katayama's Nov 13 warning is still inside 30 days: the yen pairs' floor stays at 2.5-sigma20, here 121 pips. The map stays mixed — close above the SMA200 (158.71), the SMA50 (157.48) still below. The SMA200 is 89 pips down, short of the floor. A stop under the SMA50 (~212 pips) fits, and the 1:2 crosses 160, 161 and 162 into the 9-month high at 163.91. There is no bull alignment, and Monday did not close above 160. The BoJ is still at 1.25%. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close above the SMA200 (158.71), with the SMA50 (157.48) still below — mixed alignment. The 9-month high remains 163.91. The 10-day high is 160.00 (Nov 13).",
        "support": "158.71 (the SMA200, 89 pips below) and 157.95 (the 10-day low, Nov 9), with the SMA50 at 157.48.",
        "resistance": "160.00 (the 10-day high, Friday's close) and 161.00, with the 9-month high at 163.91.",
        "priceAction": "The round was handed back. 89 pips down to the SMA200 does not pay the 121-pip floor. The 1:2 of a stop that does crosses 160, 161 and 162. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "160.00 was not held. Buying 159.60 with a stop under the SMA200 misses the 121-pip floor. The stop that clears the floor runs into three rounds. A short against the close has no bear alignment. Reassess if the MoF acts, or after the Dec 8-9 FOMC.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The yen took back 40 pips and GDP printed negative, but the book does not buy the give-back of 160. The 2.5-sigma20 floor is still wider than the distance to the SMA200."
    })

AUD = pair("0.6757", "BAIXA", "bear",
    pt={
        "fundamental": "O AUD/USD fechou em 0,6757 na sessão de segunda 16/11/2026 (taxa de referência BCE/Frankfurter), caindo -0,42% (-28 pips) a partir de 0,6785. É o segundo fechamento através da mínima de 9 meses de sexta, e o próprio fechamento é a nova mínima de 10/20 pregões e de 9 meses. A produção industrial da China em outubro subiu 4,8% no ano (esperado 5,3%) e as vendas no varejo 0,4% (esperado 0,8%) (NBS, Reuters, 16/11). A SMA50 (0,7008) está sob a SMA200 (0,7052). O piso de 1,5σ20 é de 53 pips. Até 0.6700 são 57 pips: um 1:2 contra o piso pede 106 pips e atravessa esse redondo. Um stop sobre 0.6785 fica a 28 pips e não paga o piso. O RBA está em 4,85%. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (0,7052) com a SMA50 (0,7008) abaixo dela — alinhamento de baixa. O próprio fechamento é a mínima de 10/20 pregões e de 9 meses. A máxima de 10 pregões está em 0.7015 (04/11).",
        "support": "0.6700 (o próximo redondo, 57 pips abaixo). O fechamento de 16/11 (0,6757) é a mínima de 9 meses.",
        "resistance": "0.6785 (a mínima de sexta, devolvida) e 0.6800 (o redondo perdido na sexta), com a máxima de 10 pregões em 0.7015.",
        "priceAction": "Segundo fechamento na mínima. 57 pips até 0.6700 não pagam um 1:2 contra o piso de 53. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "A confirmação sob a mínima de sexta saiu. O alvo que respeita o piso cai do outro lado de 0.6700. Sem gatilho novo.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O Aussie fez o segundo fechamento e os dados da China vieram fracos. O livro continua de fora porque 0.6700 bloqueia o 1:2."
    },
    en={
        "fundamental": "AUD/USD closed at 0.6757 in the Monday 16/11/2026 session (ECB/Frankfurter reference rate), down -0.42% (-28 pips) from 0.6785. It is the second close through Friday's 9-month low, and today's close is the new 10/20-day and 9-month low. China's October industrial output rose 4.8% on the year (expected 5.3%) and retail sales rose 0.4% (expected 0.8%) (NBS, Reuters, Nov 16). The SMA50 (0.7008) sits under the SMA200 (0.7052). The 1.5-sigma20 floor is 53 pips. 0.6700 is 57 pips away: a 1:2 against the floor needs 106 pips and crosses that round. A stop over 0.6785 is 28 pips and misses the floor. The RBA cash rate is 4.85%. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (0.7052) with the SMA50 (0.7008) below it — bear alignment. Today's close is the 10/20-day and 9-month low. The 10-day high is 0.7015 (Nov 4).",
        "support": "0.6700 (the next round, 57 pips below). The Nov-16 close (0.6757) is the 9-month low.",
        "resistance": "0.6785 (Friday's low, handed back) and 0.6800 (the round lost on Friday), with the 10-day high at 0.7015.",
        "priceAction": "A second close at the low. 57 pips down to 0.6700 does not pay a 1:2 against the 53-pip floor. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The confirming close under Friday's low has printed. The target that respects the floor lands on the other side of 0.6700. No new trigger.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The Aussie printed the second close and China's data came in soft. The book stays out because 0.6700 blocks the 1:2."
    })

GBP = pair("1.3198", "BAIXA", "bear",
    pt={
        "fundamental": "O GBP/USD fechou em 1,3198 na sessão de segunda 16/11/2026 (taxa de referência BCE/Frankfurter), caindo -0,21% (-28 pips) a partir de 1,3227. É a nova mínima de 10/20 pregões. A mínima de 9 meses segue 1.3160, a 38 pips. O piso de 1,5σ20 é de 74 pips, então o stop que paga o piso já atravessa essa mínima. Um stop sobre 1.3227 fica a 28 pips e não paga o piso. A Bank Rate está em 4,00%. O CPI do Reino Unido de outubro sai na quarta 18/11, fora da janela de 24 horas, e não é o que trava o ticket. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (1,3415) e sob a SMA50 (1,3340), com a SMA50 abaixo da SMA200 — alinhamento de baixa. A máxima de 10/20 pregões segue 1.3500 (04/11).",
        "support": "1.3160 (mínima de 9 meses, 38 pips abaixo), com o redondo 1.3200 no meio. O fechamento de 16/11 é a mínima de 10/20 pregões.",
        "resistance": "1.3227 (a mínima de sexta, devolvida) e 1.3340 (a SMA50), com a SMA200 em 1,3415.",
        "priceAction": "Nova mínima da janela, 38 pips acima do extremo de 9 meses e com piso de 74. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "O fechamento sob 1,3227 saiu. O espaço até 1.3160 é menor que o piso. Sem gatilho novo.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "A libra fez outra mínima e parou antes do extremo que importa. Vender aqui coloca 1.3160 dentro do stop."
    },
    en={
        "fundamental": "GBP/USD closed at 1.3198 in the Monday 16/11/2026 session (ECB/Frankfurter reference rate), down -0.21% (-28 pips) from 1.3227. It is the new 10/20-day low. The 9-month low is still 1.3160, 38 pips away. The 1.5-sigma20 floor is 74 pips, so the stop that meets the floor is already through that low. A stop over 1.3227 is 28 pips and misses the floor. Bank Rate is 4.00%. October UK CPI is due Wednesday 18/11, outside the 24-hour window, and it is not what blocks the ticket. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (1.3415) and under the SMA50 (1.3340), with the SMA50 below the SMA200 — bear alignment. The 10/20-day high is still 1.3500 (Nov 4).",
        "support": "1.3160 (the 9-month low, 38 pips below), with the 1.3200 round in between. The Nov-16 close is the 10/20-day low.",
        "resistance": "1.3227 (Friday's low, handed back) and 1.3340 (the SMA50), with the SMA200 at 1.3415.",
        "priceAction": "A new window low, 38 pips above the 9-month extreme and with a 74-pip floor. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The close under 1.3227 has printed. The room down to 1.3160 is smaller than the floor. No new trigger.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "Sterling made another low and stopped short of the extreme that matters. Selling here puts 1.3160 inside the stop."
    })

EURJPY = pair("175.78", "BAIXA", "bear",
    pt={
        "fundamental": "O EUR/JPY fechou em 175,78 na sessão de segunda 16/11/2026 (taxa de referência BCE/Frankfurter), caindo -0,59% (-105 pips) a partir de 176,83. O fechamento atravessou a mínima de 10 pregões de 176,77 (06/11). A mínima de 9 meses e de 20 pregões segue 175,51 (23/10), 28 pips abaixo. O aviso do MoF de 13/11 mantém o piso em 2,5σ20: 175 pips. Um stop sobre a SMA50 (177,76, ~198 pips) cabe no piso e joga o 1:2 através de 175,51 e de 175,00. Alinhamento de baixa (fechamento sob a SMA200 182,88 e a SMA50 abaixo dela). Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (182,88) com a SMA50 (177,76) abaixo dela — alinhamento de baixa pleno. A máxima de 10/20 pregões está em 178,30 (04/11).",
        "support": "175.51 (mínima de 9 meses e de 20 pregões, 23/10, 28 pips abaixo). O fechamento de 16/11 atravessou 176,77.",
        "resistance": "176.77 (a mínima de 10 pregões de 06/11, agora acima) e 177.76 (a SMA50), com a máxima de 10/20 pregões em 178,30.",
        "priceAction": "O canal de 10 pregões cedeu 105 pips. 175,51 está dentro de qualquer alvo que respeite o piso de 175. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "O fechamento sob 176,77 saiu. O stop que paga 175 pips coloca 175,51 e 175,00 no caminho do 1:2. Reavaliar se o MoF agir.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O cruzado finalmente perdeu 176,77, e o piso de 2,5σ20 continua a empurrar o alvo para dentro de 2025. A mesa não vende com 175,51 a 28 pips."
    },
    en={
        "fundamental": "EUR/JPY closed at 175.78 in the Monday 16/11/2026 session (ECB/Frankfurter reference rate), down -0.59% (-105 pips) from 176.83. The close went through the 10-day low at 176.77 (Nov 6). The 9-month and 20-day low is still 175.51 (Oct 23), 28 pips below. The MoF warning of Nov 13 keeps the floor at 2.5-sigma20: 175 pips. A stop over the SMA50 (177.76, ~198 pips) fits the floor and puts the 1:2 through 175.51 and 175.00. Bear alignment (close under the SMA200 182.88 and the SMA50 below it). Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (182.88) with the SMA50 (177.76) below it — full bear alignment. The 10/20-day high is 178.30 (Nov 4).",
        "support": "175.51 (the 9-month and 20-day low, Oct 23, 28 pips below). The Nov-16 close went through 176.77.",
        "resistance": "176.77 (the Nov-6 10-day low, now overhead) and 177.76 (the SMA50), with the 10/20-day high at 178.30.",
        "priceAction": "The 10-day channel gave up 105 pips. 175.51 sits inside any target that respects the 175-pip floor. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The close under 176.77 has printed. The stop that clears 175 pips puts 175.51 and 175.00 on the path to the 1:2. Reassess if the MoF acts.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The cross finally lost 176.77, and the 2.5-sigma20 floor still pushes the target into 2025 prices. The desk does not sell with 175.51 only 28 pips away."
    })

GBPJPY = pair("210.65", "BAIXA", "bear",
    pt={
        "fundamental": "O GBP/JPY fechou em 210,65 na sessão de segunda 16/11/2026 (taxa de referência BCE/Frankfurter), caindo -0,46% (-98 pips) a partir de 211,63. O fechamento é a nova mínima de 10 pregões. A mínima de 20 pregões segue 209,61 (103 pips abaixo) e a de 9 meses 207,32 (332 pips). O preço voltou para cima da SMA50 (210,07), mas o alinhamento segue de baixa: o fechamento e a SMA50 estão sob a SMA200 (212,90). A SMA200 está 226 pips acima e cobre o piso de 185 pips, reaberto pelo jawboning do MoF. O 1:2 desse stop atravessa 210,00, 209,61 e 207,32 — 2×185 pips são 370, mais do que os 332 até a mínima de 9 meses. BoE em 4,00%, BoJ em 1,25%. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (212,90) com a SMA50 (210,07) também sob a SMA200 — alinhamento de baixa, mesmo com o preço de volta acima da SMA50. A máxima de 10/20 pregões está em 213,63 (04/11).",
        "support": "209.61 (mínima de 20 pregões, 103 pips abaixo) e 207.32 (mínima de 9 meses). A SMA50 (210,07) ficou sob o preço.",
        "resistance": "212.90 (a SMA200, 226 pips acima) e 213.63 (máxima de 10/20 pregões). 211.63 é o fechamento de sexta, devolvido.",
        "priceAction": "Nova mínima de 10 pregões por 98 pips. O piso de 185 pips cabe sob a SMA200, e o alvo não cabe antes de 207,32. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "Vender a perda de 211,63 com stop sobre 212,90 paga o piso e atravessa a mínima de 20 pregões e a de 9 meses. Sem gatilho limpo.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O cruzado andou, e o caminho não abriu. 226 pips até a SMA200 pagam o piso de 185, mas o 1:2 cai do outro lado de 207,32. A mesa espera um mapa mais largo."
    },
    en={
        "fundamental": "GBP/JPY closed at 210.65 in the Monday 16/11/2026 session (ECB/Frankfurter reference rate), down -0.46% (-98 pips) from 211.63. The close is the new 10-day low. The 20-day low is still 209.61 (103 pips below) and the 9-month low is 207.32 (332 pips). Price is back above the SMA50 (210.07), but the alignment stays bearish: the close and the SMA50 are both under the SMA200 (212.90). The SMA200 is 226 pips above and covers the 185-pip floor, still open because of the MoF jawboning. The 1:2 of that stop crosses 210.00, 209.61 and 207.32 — 2×185 pips is 370, more than the 332 down to the 9-month low. BoE at 4.00%, BoJ at 1.25%. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (212.90) with the SMA50 (210.07) also under the SMA200 — bear alignment, even with price back above the SMA50. The 10/20-day high is 213.63 (Nov 4).",
        "support": "209.61 (the 20-day low, 103 pips below) and 207.32 (the 9-month low). The SMA50 (210.07) is now under price.",
        "resistance": "212.90 (the SMA200, 226 pips above) and 213.63 (the 10/20-day high). 211.63 is Friday's close, handed back.",
        "priceAction": "A new 10-day low by 98 pips. The 185-pip floor fits under the SMA200, and the target does not fit before 207.32. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "Selling the loss of 211.63 with a stop over 212.90 clears the floor and runs through the 20-day low and the 9-month low. No clean trigger.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The cross moved, and the path did not open. 226 pips up to the SMA200 pay the 185-pip floor, but the 1:2 lands on the other side of 207.32. The desk waits for a wider map."
    })

DATA = {
    "EUR/USD": EUR, "USD/JPY": USDJPY, "AUD/USD": AUD,
    "GBP/USD": GBP, "EUR/JPY": EURJPY, "GBP/JPY": GBPJPY,
}
DRIVERS = {
    "EUR/USD": {
        "en": ["Second close through the 9-month low", "14 pips to 1.1000, floor is 61", "Fed still 3.75-4.00%"],
        "pt": ["Segundo fechamento sob a mín. de 9 meses", "14 pips até 1.1000, piso é 61", "Fed ainda 3,75-4,00%"],
    },
    "USD/JPY": {
        "en": ["160.00 handed back, close 159.60", "Floor still 2.5-sigma, 121 pips", "Japan Q3 GDP -0.1% annualized"],
        "pt": ["160,00 devolvido, fechamento 159,60", "Piso segue 2,5σ, 121 pips", "PIB do Japão 3º tri -0,1% anualizado"],
    },
    "AUD/USD": {
        "en": ["Second close at the 9-month low", "57 pips to 0.6700, need 106", "China retail +0.4%, IP +4.8%"],
        "pt": ["Segundo fechamento na mín. de 9 meses", "57 pips até 0.6700, precisa 106", "Varejo China +0,4%, produção +4,8%"],
    },
    "GBP/USD": {
        "en": ["New 10/20-day low at 1.3198", "38 pips to the 9-month low, floor 74", "Bank Rate still 4.00%"],
        "pt": ["Nova mín. de 10/20 pregões em 1.3198", "38 pips até a mín. de 9m, piso 74", "Bank Rate ainda 4,00%"],
    },
    "EUR/JPY": {
        "en": ["Through the 10-day low 176.77", "175.51 is only 28 pips away", "Floor still 175 pips"],
        "pt": ["Através da mín. de 10 pregões 176,77", "175,51 está a só 28 pips", "Piso segue 175 pips"],
    },
    "GBP/JPY": {
        "en": ["New 10-day low, 98 pips lower", "SMA200 covers the 185-pip floor", "9-month low sits inside the target"],
        "pt": ["Nova mín. de 10 pregões, -98 pips", "SMA200 cobre o piso de 185", "Mín. de 9 meses fica dentro do alvo"],
    },
}

NEWS_ITEM_JS = r'''                {
                    date: "16/11/2026",
                    category: "macro",
                    impact: "high",
                    pairs: ["EUR/USD", "USD/JPY", "AUD/USD", "GBP/USD", "EUR/JPY", "GBP/JPY"],
                    pt: {
                        headline: "O dólar estende as mínimas e o iene devolve 160 — o piso de 2,5σ segue, e os seis continuam sem ticket",
                        summary: "A taxa BCE/Frankfurter de 16/11 empurra o dólar. EUR/USD fechou 1,1014 (−0,34%), segundo fechamento sob a mínima de 9 meses, a 14 pips de 1.1000, com piso de 61. AUD/USD fechou 0,6757 (−0,42%), também segundo fechamento na mínima, com 0.6700 a 57 pips e um 1:2 pedindo 106. A China mostrou produção industrial de outubro a +4,8% no ano (esperado 5,3%) e varejo a +0,4% (esperado 0,8%) (NBS, Reuters). GBP/USD 1,3198 (−0,21%) ficou a 38 pips de 1.3160, piso de 74. USD/JPY devolveu o redondo e fechou 159,60 (−0,25%). O PIB do Japão no 3º trimestre caiu 0,1% anualizado, a primeira contração em quatro trimestres (Gabinete, 16/11). O aviso de Katayama de 13/11 mantém o piso em 2,5σ20: 121 pips no USD/JPY, 175 no EUR/JPY, 185 no GBP/JPY. EUR/JPY 175,78 perdeu 176,77 e parou 28 pips acima de 175,51. GBP/JPY 210,65 fez mínima de 10 pregões, e o 1:2 atravessa 207,32. Os seis ficam em AGUARDAR. Varejo dos EUA na terça 17/11. FOMC em 8-9/12.",
                        take: "As mínimas do euro e do Aussie confirmaram, e o caminho até o próximo redondo continua curto demais. O iene recuperou 160 sem abrir um long legal. A mesa segue vazia."
                    },
                    en: {
                        headline: "The dollar extends the lows and the yen hands 160 back — the 2.5-sigma floor stays, and all six remain without a ticket",
                        summary: "The 16/11 ECB/Frankfurter fixing pushes the dollar. EUR/USD closed 1.1014 (−0.34%), a second close under the 9-month low, 14 pips from 1.1000, with a 61-pip floor. AUD/USD closed 0.6757 (−0.42%), also a second close at the low, with 0.6700 57 pips away and a 1:2 asking for 106. China printed October industrial output at +4.8% on the year (expected 5.3%) and retail sales at +0.4% (expected 0.8%) (NBS, Reuters). GBP/USD 1.3198 (−0.21%) finished 38 pips from 1.3160, floor 74. USD/JPY handed the round back and closed 159.60 (−0.25%). Japan's Q3 GDP fell 0.1% annualized, the first contraction in four quarters (Cabinet Office, Nov 16). Katayama's Nov 13 warning keeps the floor at 2.5-sigma20: 121 pips on USD/JPY, 175 on EUR/JPY, 185 on GBP/JPY. EUR/JPY 175.78 lost 176.77 and stopped 28 pips above 175.51. GBP/JPY 210.65 made a 10-day low, and the 1:2 crosses 207.32. All six stay on WAIT. US retail sales on Tuesday 17/11. FOMC on Dec 8-9.",
                        take: "The euro and Aussie lows confirmed, and the path to the next round is still too short. The yen took 160 back without opening a legal long. The desk stays empty."
                    }
                },
'''

NEWS_CARD = r'''                <!-- News 16/11/2026: dollar extends the lows, yen hands 160 back; all six WAIT -->
                <article class="news-card">
                    <div class="news-card-top">
                        <span class="news-cat"><span class="lang-en">Macro Data</span><span class="lang-pt" style="display:none;">Dados Macro</span></span>
                        <span class="impact-badge high"><span class="lang-en">High Impact</span><span class="lang-pt" style="display:none;">Impacto Alto</span></span>
                        <span class="news-date">16/11/2026</span>
                    </div>
                    <h2 class="news-title">
                        <span class="lang-en">The dollar extends the lows and the yen hands 160 back — the 2.5-sigma floor stays, and all six remain without a ticket</span>
                        <span class="lang-pt" style="display:none;">O dólar estende as mínimas e o iene devolve 160 — o piso de 2,5σ segue, e os seis continuam sem ticket</span>
                    </h2>
                    <p class="news-summary">
                        <span class="lang-en">The 16/11 ECB/Frankfurter fixing pushes the dollar. EUR/USD closed 1.1014 (−0.34%), a second close under the 9-month low, 14 pips from 1.1000, with a 61-pip floor. AUD/USD closed 0.6757 (−0.42%), also a second close at the low, with 0.6700 57 pips away and a 1:2 asking for 106. China printed October industrial output at +4.8% on the year (expected 5.3%) and retail sales at +0.4% (expected 0.8%) (NBS, Reuters). GBP/USD 1.3198 (−0.21%) finished 38 pips from 1.3160, floor 74. USD/JPY handed the round back and closed 159.60 (−0.25%). Japan's Q3 GDP fell 0.1% annualized, the first contraction in four quarters (Cabinet Office, Nov 16). Katayama's Nov 13 warning keeps the floor at 2.5-sigma20: 121 pips on USD/JPY, 175 on EUR/JPY, 185 on GBP/JPY. EUR/JPY 175.78 lost 176.77 and stopped 28 pips above 175.51. GBP/JPY 210.65 made a 10-day low, and the 1:2 crosses 207.32. All six stay on WAIT. US retail sales on Tuesday 17/11. FOMC on Dec 8-9.</span>
                        <span class="lang-pt" style="display:none;">A taxa BCE/Frankfurter de 16/11 empurra o dólar. EUR/USD fechou 1,1014 (−0,34%), segundo fechamento sob a mínima de 9 meses, a 14 pips de 1.1000, com piso de 61. AUD/USD fechou 0,6757 (−0,42%), também segundo fechamento na mínima, com 0.6700 a 57 pips e um 1:2 pedindo 106. A China mostrou produção industrial de outubro a +4,8% no ano (esperado 5,3%) e varejo a +0,4% (esperado 0,8%) (NBS, Reuters). GBP/USD 1,3198 (−0,21%) ficou a 38 pips de 1.3160, piso de 74. USD/JPY devolveu o redondo e fechou 159,60 (−0,25%). O PIB do Japão no 3º trimestre caiu 0,1% anualizado, a primeira contração em quatro trimestres (Gabinete, 16/11). O aviso de Katayama de 13/11 mantém o piso em 2,5σ20: 121 pips no USD/JPY, 175 no EUR/JPY, 185 no GBP/JPY. EUR/JPY 175,78 perdeu 176,77 e parou 28 pips acima de 175,51. GBP/JPY 210,65 fez mínima de 10 pregões, e o 1:2 atravessa 207,32. Os seis ficam em AGUARDAR. Varejo dos EUA na terça 17/11. FOMC em 8-9/12.</span>
                    </p>
                    <div class="news-take">
                        <span class="take-tag"><span class="lang-en">Desk take</span><span class="lang-pt" style="display:none;">Leitura da mesa</span></span>
                        <span class="lang-en">The euro and Aussie lows confirmed, and the path to the next round is still too short. The yen took 160 back without opening a legal long. The desk stays empty.</span>
                        <span class="lang-pt" style="display:none;">As mínimas do euro e do Aussie confirmaram, e o caminho até o próximo redondo continua curto demais. O iene recuperou 160 sem abrir um long legal. A mesa segue vazia.</span>
                    </div>
                    <div class="news-pairs">
                        <span class="np-label"><span class="lang-en">Watch</span><span class="lang-pt" style="display:none;">Acompanhar</span></span>
                        <a href="eur-usd.html" class="pair-link-chip">EUR/USD</a><a href="usd-jpy.html" class="pair-link-chip">USD/JPY</a><a href="aud-usd.html" class="pair-link-chip">AUD/USD</a><a href="gbp-usd.html" class="pair-link-chip">GBP/USD</a><a href="eur-jpy.html" class="pair-link-chip">EUR/JPY</a><a href="gbp-jpy.html" class="pair-link-chip">GBP/JPY</a>
                    </div>
                </article>

'''

NEW_CAL = '''                <div class="cal-cell">
                    <span class="cal-date">16/11</span>
                    <span class="cal-event"><span class="lang-en">Japan Q3 GDP −0.1% annualized (Cabinet Office)</span><span class="lang-pt" style="display:none;">PIB do Japão 3º tri −0,1% anualizado (Gabinete)</span></span>
                    <div class="cal-meta"><span class="cal-impact high" aria-hidden="true"></span><span class="cal-cur">JPY</span></div>
                </div>
                <div class="cal-cell">
                    <span class="cal-date">16/11</span>
                    <span class="cal-event"><span class="lang-en">China Oct: IP +4.8% y/y, retail +0.4%</span><span class="lang-pt" style="display:none;">China out: produção +4,8% a/a, varejo +0,4%</span></span>
                    <div class="cal-meta"><span class="cal-impact high" aria-hidden="true"></span><span class="cal-cur">AUD</span></div>
                </div>
                <div class="cal-cell">
                    <span class="cal-date">17/11</span>
                    <span class="cal-event"><span class="lang-en">US retail sales, October (13:30 UTC)</span><span class="lang-pt" style="display:none;">Vendas no varejo dos EUA, outubro (13:30 UTC)</span></span>
                    <div class="cal-meta"><span class="cal-impact high" aria-hidden="true"></span><span class="cal-cur">USD</span></div>
                </div>
                <div class="cal-cell">
                    <span class="cal-date">09/12</span>
                    <span class="cal-event"><span class="lang-en">FOMC decision, hike debate 25 or 50 bp</span><span class="lang-pt" style="display:none;">Decisão do FOMC, debate de alta de 25 ou 50 pb</span></span>
                    <div class="cal-meta"><span class="cal-impact high" aria-hidden="true"></span><span class="cal-cur">USD</span></div>
                </div>'''

def main():
    print("STAMP", TS)
    with open(INDEX, encoding="utf-8") as f:
        idx = f.read()
    if idx.count(OLD_TS) != 4:
        raise SystemExit("expected 4 old timestamps, found %d" % idx.count(OLD_TS))
    idx = idx.replace(OLD_TS, TS)
    idx = idx.replace(
        "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 585 daily sessions (01/08/2024–13/11/2026).",
        "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 586 daily sessions (01/08/2024–16/11/2026).")
    idx = idx.replace(
        "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, σ20 e Donchian calculados · 585 pregões (01/08/2024 a 13/11/2026).",
        "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, σ20 e Donchian calculados · 586 pregões (01/08/2024 a 16/11/2026).")
    idx = idx.replace(
        'nextEvent: "PPI 6.5% y/y · MoF at 160 · FOMC Dec 8-9"',
        'nextEvent: "Japan GDP -0.1% · China retail +0.4% · FOMC Dec 8-9"')
    idx = idx.replace(
        'nextEvent: "PPI 6,5% a/a · MoF em 160 · FOMC 8-9/12"',
        'nextEvent: "PIB Japão -0,1% · varejo China +0,4% · FOMC 8-9/12"')

    start = idx.find("        const forexData = {")
    end = idx.find("        /* ==========================================\n           B. Market metadata")
    if start < 0 or end < 0:
        raise SystemExit("forexData markers missing")
    idx = idx[:start] + "        const forexData = " + json.dumps(DATA, ensure_ascii=False, indent=4) + ";\n\n" + idx[end:]

    d0 = idx.find("        const dailyChanges = {")
    d1 = idx.find("        const macroDrivers = {")
    changes = {
        "EUR/USD": "-0.34%", "USD/JPY": "-0.25%", "AUD/USD": "-0.42%",
        "GBP/USD": "-0.21%", "EUR/JPY": "-0.59%", "GBP/JPY": "-0.46%",
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
    with open(INDEX, "w", encoding="utf-8", newline="\n") as f:
        f.write(idx)
    print("index.html patched")

    with open(LEDGER, encoding="utf-8") as f:
        ledger = json.load(f)
    assert ledger["watching"] == [] and ledger["open"] == []
    ledger["meta"]["lastUpdated"] = "16/11/2026"
    with open(LEDGER, "w", encoding="utf-8", newline="\n") as f:
        json.dump(ledger, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("ledger lastUpdated only; book still empty")

    with open(NEWS, encoding="utf-8") as f:
        news = f.read()
    news = news.replace(
        "Market Wire · 160 and a Warning, Still No Ticket",
        "Market Wire · Dollar Extends, Yen Hands 160 Back")
    news = news.replace(
        "Telégrafo da Mesa · 160 e um Aviso, Ainda Sem Ticket",
        "Telégrafo da Mesa · O Dólar Estende, o Iene Devolve 160")
    news = news.replace(OLD_TS, TS)
    news = news.replace(
        "6 pairs · MoF at 160 · FOMC Dec 8-9",
        "6 pairs · Japan GDP · China data · FOMC Dec 8-9")
    news = news.replace(
        "6 pares · MoF em 160 · FOMC 8-9/12",
        "6 pares · PIB do Japão · dados da China · FOMC 8-9/12")
    start = news.find('                <div class="cal-cell">')
    end = news.find("            </div>\n        </section>", start)
    if start < 0 or end < 0:
        raise SystemExit("calendar block missing")
    news = news[:start] + NEW_CAL + "\n" + news[end:]
    marker = "                <!-- News 13/11/2026:"
    if marker not in news:
        raise SystemExit("news marker missing")
    news = news.replace(marker, NEWS_CARD + marker, 1)
    with open(NEWS, "w", encoding="utf-8", newline="\n") as f:
        f.write(news)
    print("news.html patched")

    with open(SITEMAP, encoding="utf-8") as f:
        sm = f.read()
    n = sm.count("2026-11-14")
    if n != 9:
        raise SystemExit("expected 9 sitemap dates, found %d" % n)
    sm = sm.replace("2026-11-14", "2026-11-16")
    with open(SITEMAP, "w", encoding="utf-8", newline="\n") as f:
        f.write(sm)
    print("sitemap patched")

    with open(VERIFY, encoding="utf-8") as f:
        v = f.read()
    v = v.replace('TODAY_TS = "14/11/2026 23:20 UTC"', 'TODAY_TS = "%s"' % TS)
    v = v.replace(
        'TODAY_DATE = "13/11/2026"  # basis session date (report edition: 13/11/2026)',
        'TODAY_DATE = "16/11/2026"  # basis session date (report edition: 16/11/2026)')
    old_ticker = '''TICKER = [("EUR/USD","-0.26%"),("USD/JPY","+0.19%"),("AUD/USD","-0.52%"),
          ("GBP/USD","-0.22%"),("EUR/JPY","-0.07%"),("GBP/JPY","-0.03%")]'''
    new_ticker = '''TICKER = [("EUR/USD","-0.34%"),("USD/JPY","-0.25%"),("AUD/USD","-0.42%"),
          ("GBP/USD","-0.21%"),("EUR/JPY","-0.59%"),("GBP/JPY","-0.46%")]'''
    if old_ticker not in v:
        raise SystemExit("ticker block missing")
    v = v.replace(old_ticker, new_ticker)
    with open(VERIFY, "w", encoding="utf-8", newline="\n") as f:
        f.write(v)
    print("verify constants patched")

if __name__ == "__main__":
    main()
