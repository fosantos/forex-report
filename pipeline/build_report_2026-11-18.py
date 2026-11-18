#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""18/11/2026 edition, on the Wednesday 18/11 ECB fixing.

Cable closes at 1.3169, 9 pips above the 9-month low, after UK CPI at 3.6%.
EUR/USD extends to 1.0968, 18 pips from 1.0950. EUR/JPY prints the second
close through 175.51 and through 175.00. The Oct 28 FOMC minutes came out
at 19:00 UTC, after this fixing. No ticket clears the gate.
"""
import json
from datetime import datetime, timezone

INDEX = r"C:/Projetos/forex-report/docs/index.html"
LEDGER = r"C:/Projetos/forex-report/docs/track-record.json"
NEWS = r"C:/Projetos/forex-report/docs/news.html"
SITEMAP = r"C:/Projetos/forex-report/docs/sitemap.xml"
VERIFY = r"C:/Projetos/forex-report/pipeline/verify_all.py"

TS = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
OLD_TS = "17/11/2026 23:07 UTC"
BASIS = "588 sessions, 01/08/2024 to 18/11/2026"
BASIS_PT = "588 pregões, 01/08/2024 a 18/11/2026"

def pair(quote, bias, bias_type, pt, en):
    return {"quote": quote, "bias": bias, "biasType": bias_type, "pt": pt, "en": en}

EUR = pair("1.0968", "BAIXA", "bear",
    pt={
        "fundamental": "O EUR/USD fechou em 1,0968 na sessão de quarta 18/11/2026 (taxa de referência BCE/Frankfurter; o terminal MT5 está logado, mas o Market Watch não tem os pares à vista), caindo -0,19% (-21 pips) a partir de 1,0989. É mais uma mínima de 10/20 pregões e de 9 meses. Até 1.0950 são 18 pips. O piso de 1,5σ20 é de 60 pips, então o stop que paga o piso já atravessa 1.0950. Até 1.0900 são 68 pips, menos que os 120 de um alvo de 1 para 2 no piso. Um stop sobre 1.0989 fica a 21 pips. O Fed segue em 3,75-4,00%. A ata do FOMC de 28/10 saiu às 19:00 UTC, depois deste fixing: quase todos os participantes viram nova alta como provavelmente adequada, e um par deles notou que uma alta de mais de 25 pb poderia ser considerada se a inflação viesse desfavorável (AP, 18/11). O fechamento de quarta não contém essa reação. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (1,1516) com a SMA50 (1,1262) abaixo dela — alinhamento de baixa pleno. O próprio fechamento é a mínima de 10/20 pregões e de 9 meses. A máxima de 10 pregões é 1.1224 (05/11). A de 20 pregões segue 1.1267 (04/11).",
        "support": "1.0950 (o próximo redondo, 18 pips abaixo) e 1.0900 (68 pips). O fechamento de 18/11 (1,0968) é a mínima de 9 meses.",
        "resistance": "1.0989 (a mínima de terça, devolvida) e 1.1000, com a SMA50 em 1,1262.",
        "priceAction": "A extensão de quarta deixou 1.0950 dentro do piso de 60. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "O fechamento sob 1,0989 saiu. 18 pips até 1.0950 são menos que o piso. O stop legal já cai do outro lado desse redondo. Sem gatilho novo.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O euro fez outra mínima e 1.0950 ficou mais perto do que o piso permite. A ata saiu depois do fixing e não abre um short legal."
    },
    en={
        "fundamental": "EUR/USD closed at 1.0968 in the Wednesday 18/11/2026 session (ECB/Frankfurter reference rate; the MT5 terminal is logged in, but Market Watch has no spot pairs), down -0.19% (-21 pips) from 1.0989. It is another 10/20-day and 9-month low. 1.0950 is 18 pips away. The 1.5-sigma20 floor is 60 pips, so the stop that meets the floor is already through 1.0950. 1.0900 is 68 pips away, less than the 120 of a one-to-two target on the floor. A stop over 1.0989 is 21 pips. The Fed is still at 3.75-4.00%. The minutes of the Oct 28 FOMC came out at 19:00 UTC, after this fixing: almost all participants saw a further hike as likely appropriate, and a couple noted that a rise of more than 25 bp could be considered if inflation data were unfavorable (AP, Nov 18). Wednesday's close does not contain that reaction. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (1.1516) with the 50-day (1.1262) below it — full bear alignment. Today's close is the 10/20-day and 9-month low. The 10-day high is 1.1224 (Nov 5). The 20-day high is still 1.1267 (Nov 4).",
        "support": "1.0950 (the next round, 18 pips below) and 1.0900 (68 pips). The Nov-18 close (1.0968) is the 9-month low.",
        "resistance": "1.0989 (Tuesday's low, handed back) and 1.1000, with the SMA50 at 1.1262.",
        "priceAction": "Wednesday's extension left 1.0950 inside the 60-pip floor. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The close under 1.0989 has printed. 18 pips down to 1.0950 is less than the floor. The legal stop already lands on the other side of that round. No new trigger.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The euro made another low and 1.0950 is closer than the floor allows. The minutes came out after the fixing and do not open a legal short."
    })

USDJPY = pair("159.42", "NEUTRO", "neutral",
    pt={
        "fundamental": "O USD/JPY fechou em 159,42 na sessão de quarta 18/11/2026 (taxa de referência BCE/Frankfurter), subindo +0,08% (+12 pips) a partir de 159,30. O fechamento segue sob 160,00. A máxima de 10 pregões continua 160,00 (13/11). O aviso de Katayama de 13/11 continua dentro de 30 dias, sem intervenção confirmada. O piso segue em 2,5σ20, aqui 121 pips. O mapa continua misto — fechamento acima da SMA200 (158,73), SMA50 (157,71) ainda abaixo. Daqui até a SMA200 são 69 pips, menos que o piso. Um stop sob a SMA50 (~171 pips) cabe, e o alvo atravessa 160, 161 e 162. Não há alinhamento de alta. A ata do FOMC saiu depois deste fixing. O BoJ segue em 1,25%. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento acima da SMA200 (158,73), com a SMA50 (157,71) ainda abaixo — alinhamento misto. A máxima de 9 meses segue 163,91. A máxima de 10 pregões é 160,00 (13/11).",
        "support": "158.73 (a SMA200, 69 pips abaixo) e 157.95 (mínima de 10 pregões, 09/11), com a SMA50 em 157,71.",
        "resistance": "160.00 (máxima de 10 pregões, 13/11) e 161.00, com a máxima de 9 meses em 163,91.",
        "priceAction": "Doze pips de volta para 160, ainda longe de um long legal. 69 pips até a SMA200 não pagam o piso de 121. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "160.00 segue acima. Comprar 159,42 com stop sob a SMA200 falha o piso de 121 pips. O stop que paga o piso esbarra em 160, 161 e 162. Vender não tem alinhamento de baixa. Reavaliar se o MoF agir, ou depois do FOMC de 8-9/12.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O iene devolveu 12 pips e a ata saiu depois do fixing. O piso de 2,5σ20 continua mais largo que a distância até a SMA200."
    },
    en={
        "fundamental": "USD/JPY closed at 159.42 in the Wednesday 18/11/2026 session (ECB/Frankfurter reference rate), up +0.08% (+12 pips) from 159.30. The close is still under 160.00. The 10-day high remains 160.00 (Nov 13). Katayama's Nov 13 warning is still inside 30 days, with no confirmed intervention. The floor stays at 2.5-sigma20, here 121 pips. The map stays mixed — close above the SMA200 (158.73), the SMA50 (157.71) still below. The SMA200 is 69 pips down, short of the floor. A stop under the SMA50 (~171 pips) fits, and the target crosses 160, 161 and 162. There is no bull alignment. The FOMC minutes came out after this fixing. The BoJ is still at 1.25%. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close above the SMA200 (158.73), with the SMA50 (157.71) still below — mixed alignment. The 9-month high remains 163.91. The 10-day high is 160.00 (Nov 13).",
        "support": "158.73 (the SMA200, 69 pips below) and 157.95 (the 10-day low, Nov 9), with the SMA50 at 157.71.",
        "resistance": "160.00 (the 10-day high, Nov 13) and 161.00, with the 9-month high at 163.91.",
        "priceAction": "Twelve pips back toward 160, still short of a legal long. 69 pips down to the SMA200 does not pay the 121-pip floor. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "160.00 is still overhead. Buying 159.42 with a stop under the SMA200 misses the 121-pip floor. The stop that clears the floor runs into 160, 161 and 162. A short has no bear alignment. Reassess if the MoF acts, or after the Dec 8-9 FOMC.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The yen gave back 12 pips and the minutes came out after the fixing. The 2.5-sigma20 floor is still wider than the distance to the SMA200."
    })

AUD = pair("0.6731", "BAIXA", "bear",
    pt={
        "fundamental": "O AUD/USD fechou em 0,6731 na sessão de quarta 18/11/2026 (taxa de referência BCE/Frankfurter), caindo -0,05% (-4 pips) a partir de 0,6735. É mais um fechamento na mínima de 9 meses e de 10/20 pregões. A SMA50 (0,6989) está sob a SMA200 (0,7049). O piso de 1,5σ20 é de 49 pips. Até 0.6700 são 31 pips, então o stop que paga o piso já atravessa esse redondo. Um stop sobre 0.6735 fica a 4 pips. O RBA está em 4,85%. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (0,7049) com a SMA50 (0,6989) abaixo dela — alinhamento de baixa. O próprio fechamento é a mínima de 10/20 pregões e de 9 meses. A máxima de 10 pregões está em 0.7000 (05/11).",
        "support": "0.6700 (o próximo redondo, 31 pips abaixo). O fechamento de 18/11 (0,6731) é a mínima de 9 meses.",
        "resistance": "0.6735 (a mínima de terça, devolvida) e 0.6757, com a máxima de 10 pregões em 0.7000.",
        "priceAction": "Quase parado, 31 pips acima de 0.6700 e com piso de 49. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "O fechamento sob 0,6735 saiu por 4 pips. 31 pips até 0.6700 são menos que o piso. Sem gatilho novo.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O Aussie fez outra mínima por uma margem curta. 0.6700 continua dentro do piso de 49 pips."
    },
    en={
        "fundamental": "AUD/USD closed at 0.6731 in the Wednesday 18/11/2026 session (ECB/Frankfurter reference rate), down -0.05% (-4 pips) from 0.6735. It is another close at the 9-month and 10/20-day low. The SMA50 (0.6989) sits under the SMA200 (0.7049). The 1.5-sigma20 floor is 49 pips. 0.6700 is 31 pips away, so the stop that meets the floor is already through that round. A stop over 0.6735 is 4 pips. The RBA cash rate is 4.85%. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (0.7049) with the SMA50 (0.6989) below it — bear alignment. Today's close is the 10/20-day and 9-month low. The 10-day high is 0.7000 (Nov 5).",
        "support": "0.6700 (the next round, 31 pips below). The Nov-18 close (0.6731) is the 9-month low.",
        "resistance": "0.6735 (Tuesday's low, handed back) and 0.6757, with the 10-day high at 0.7000.",
        "priceAction": "Almost unchanged, 31 pips above 0.6700 and with a 49-pip floor. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The close under 0.6735 printed by 4 pips. 31 pips down to 0.6700 is less than the floor. No new trigger.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The Aussie made another low by a thin margin. 0.6700 is still inside the 49-pip floor."
    })

GBP = pair("1.3169", "BAIXA", "bear",
    pt={
        "fundamental": "O GBP/USD fechou em 1,3169 na sessão de quarta 18/11/2026 (taxa de referência BCE/Frankfurter), caindo -0,17% (-23 pips) a partir de 1,3191. É a nova mínima de 10/20 pregões. A mínima de 9 meses segue 1.3160, a 9 pips. O piso de 1,5σ20 é de 70 pips, então o stop que paga o piso já atravessa esse extremo. O CPI do Reino Unido em outubro subiu para 3,6% no ano, de 3,5%, em linha com a pesquisa e abaixo dos 3,7% que o BoE projetou. O núcleo ficou em 2,8% e os serviços em 3,7%, ambos sem mudança (ONS, 18/11, 07:00 UTC). O dado está neste fixing, e a libra mesmo assim caiu. A Bank Rate está em 4,00%. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (1,3411) e sob a SMA50 (1,3325), com a SMA50 abaixo da SMA200 — alinhamento de baixa. A máxima de 10 pregões é 1.3459 (05/11). A de 20 pregões segue 1.3500 (04/11).",
        "support": "1.3160 (mínima de 9 meses, 9 pips abaixo). O fechamento de 18/11 é a mínima de 10/20 pregões.",
        "resistance": "1.3191 (a mínima de terça, devolvida) e 1.3325 (a SMA50), com a SMA200 em 1,3411.",
        "priceAction": "O CPI saiu e o cabo desceu até 9 pips da mínima de 9 meses. O piso é 70. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "O fechamento sob 1,3191 saiu. O espaço até 1.3160 é menor que o piso. Sem gatilho novo.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "A libra fez o que o CPI não segurou. Vender aqui coloca 1.3160 dentro do stop."
    },
    en={
        "fundamental": "GBP/USD closed at 1.3169 in the Wednesday 18/11/2026 session (ECB/Frankfurter reference rate), down -0.17% (-23 pips) from 1.3191. It is the new 10/20-day low. The 9-month low is still 1.3160, 9 pips away. The 1.5-sigma20 floor is 70 pips, so the stop that meets the floor is already through that extreme. UK October CPI rose to 3.6% on the year, from 3.5%, in line with the poll and below the 3.7% the BoE had forecast. Core held at 2.8% and services at 3.7%, both unchanged (ONS, Nov 18, 07:00 UTC). The print is in this fixing, and cable fell anyway. Bank Rate is 4.00%. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (1.3411) and under the SMA50 (1.3325), with the SMA50 below the SMA200 — bear alignment. The 10-day high is 1.3459 (Nov 5). The 20-day high is still 1.3500 (Nov 4).",
        "support": "1.3160 (the 9-month low, 9 pips below). The Nov-18 close is the 10/20-day low.",
        "resistance": "1.3191 (Tuesday's low, handed back) and 1.3325 (the SMA50), with the SMA200 at 1.3411.",
        "priceAction": "CPI printed and cable dropped to 9 pips from the 9-month low. The floor is 70. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The close under 1.3191 has printed. The room down to 1.3160 is smaller than the floor. No new trigger.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "Sterling did what the CPI print did not hold. Selling here puts 1.3160 inside the stop."
    })

EURJPY = pair("174.85", "BAIXA", "bear",
    pt={
        "fundamental": "O EUR/JPY fechou em 174,85 na sessão de quarta 18/11/2026 (taxa de referência BCE/Frankfurter), caindo -0,12% (-20 pips) a partir de 175,05. É o segundo fechamento através de 175,51 e também através de 175,00, por 15 pips. A confirmação do extremo de 9 meses saiu. O próximo redondo, 174,00, está a 85 pips. O aviso do MoF de 13/11 mantém o piso em 2,5σ20, aqui 177 pips, então o stop que paga o piso já atravessa 174,00. A SMA50 está em 177,60 e a SMA200 em 182,78. Alinhamento de baixa. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (182,78) com a SMA50 (177,60) abaixo dela — alinhamento de baixa pleno. O próprio fechamento é a mínima de 10/20 pregões e de 9 meses. A máxima de 10 pregões está em 177,86 (05/11).",
        "support": "174.00 (o próximo redondo, 85 pips abaixo). O fechamento de 18/11 (174,85) é a nova mínima de 9 meses.",
        "resistance": "175.00 (o redondo perdido, 15 pips acima) e 175.51 (a mínima antiga), com a SMA50 em 177,60.",
        "priceAction": "O segundo fechamento sob 175,51 atravessou 175,00 e parou 85 pips antes de 174,00. O piso é 177. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "A confirmação sob 175,51 saiu. 85 pips até 174,00 são menos que o piso de 177. Sem gatilho novo.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O cruzado entregou o segundo fechamento e perdeu 175,00. O próximo redondo continua dentro do piso de 177 pips."
    },
    en={
        "fundamental": "EUR/JPY closed at 174.85 in the Wednesday 18/11/2026 session (ECB/Frankfurter reference rate), down -0.12% (-20 pips) from 175.05. It is the second close through 175.51 and also through 175.00, by 15 pips. The confirming close of the 9-month extreme has printed. The next round, 174.00, is 85 pips away. The MoF warning of Nov 13 keeps the floor at 2.5-sigma20, here 177 pips, so the stop that meets the floor is already through 174.00. The SMA50 is at 177.60 and the SMA200 at 182.78. Bear alignment. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (182.78) with the SMA50 (177.60) below it — full bear alignment. Today's close is the 10/20-day and 9-month low. The 10-day high is 177.86 (Nov 5).",
        "support": "174.00 (the next round, 85 pips below). The Nov-18 close (174.85) is the new 9-month low.",
        "resistance": "175.00 (the round just lost, 15 pips above) and 175.51 (the prior low), with the SMA50 at 177.60.",
        "priceAction": "The second close under 175.51 went through 175.00 and stopped 85 pips short of 174.00. The floor is 177. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The confirming close under 175.51 has printed. 85 pips down to 174.00 is less than the 177-pip floor. No new trigger.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The cross delivered the second close and lost 175.00. The next round is still inside the 177-pip floor."
    })

GBPJPY = pair("209.93", "BAIXA", "bear",
    pt={
        "fundamental": "O GBP/JPY fechou em 209,93 na sessão de quarta 18/11/2026 (taxa de referência BCE/Frankfurter), caindo -0,10% (-20 pips) a partir de 210,14. O fechamento perdeu 210,00 e a SMA50 (210,14) e é a nova mínima de 10 pregões. A mínima de 20 pregões segue 209,61, a 32 pips, e a de 9 meses 207,32, a 261 pips. O alinhamento é de baixa: o fechamento e a SMA50 estão sob a SMA200 (212,87), 294 pips acima. O piso, ainda aberto pelo jawboning do MoF, é de 183 pips. A SMA200 cobre esse piso, e o alvo de um stop de 183 pips (366 pips) atravessa 209,61 e 207,32. BoE em 4,00%, BoJ em 1,25%. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (212,87) e agora também sob a SMA50 (210,14), com a SMA50 sob a SMA200 — alinhamento de baixa pleno. A máxima de 10 pregões está em 213,27 (05/11).",
        "support": "209.61 (mínima de 20 pregões, 32 pips abaixo) e 207.32 (mínima de 9 meses, 261 pips). O fechamento de 18/11 é a mínima de 10 pregões.",
        "resistance": "210.14 (a SMA50, agora acima) e 212.87 (a SMA200, 294 pips acima). 210.00 foi devolvido.",
        "priceAction": "Perdeu 210 e a SMA50. 209,61 está dentro do piso de 183, e o alvo que paga o piso atravessa 207,32. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "Vender a perda de 210,14 com stop sobre 212,87 paga o piso e atravessa a mínima de 20 pregões e a de 9 meses. Sem gatilho limpo.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O cruzado perdeu 210 e a SMA50, e o caminho não abriu. 32 pips até 209,61 são menos que o piso de 183."
    },
    en={
        "fundamental": "GBP/JPY closed at 209.93 in the Wednesday 18/11/2026 session (ECB/Frankfurter reference rate), down -0.10% (-20 pips) from 210.14. The close lost 210.00 and the SMA50 (210.14) and is the new 10-day low. The 20-day low is still 209.61, 32 pips away, and the 9-month low is 207.32, 261 pips away. Alignment is bearish: the close and the SMA50 are both under the SMA200 (212.87), 294 pips above. The floor, still open from the MoF jawboning, is 183 pips. The SMA200 covers that floor, and the target of a 183-pip stop (366 pips) crosses 209.61 and 207.32. BoE at 4.00%, BoJ at 1.25%. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (212.87) and now also under the SMA50 (210.14), with the SMA50 under the SMA200 — full bear alignment. The 10-day high is 213.27 (Nov 5).",
        "support": "209.61 (the 20-day low, 32 pips below) and 207.32 (the 9-month low, 261 pips). The Nov-18 close is the 10-day low.",
        "resistance": "210.14 (the SMA50, now overhead) and 212.87 (the SMA200, 294 pips above). 210.00 was handed back.",
        "priceAction": "It lost 210 and the SMA50. 209.61 sits inside the 183-pip floor, and the target that pays the floor crosses 207.32. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "Selling the loss of 210.14 with a stop over 212.87 clears the floor and runs through the 20-day low and the 9-month low. No clean trigger.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The cross lost 210 and the SMA50, and the path did not open. 32 pips down to 209.61 is less than the 183-pip floor."
    })

DATA = {
    "EUR/USD": EUR, "USD/JPY": USDJPY, "AUD/USD": AUD,
    "GBP/USD": GBP, "EUR/JPY": EURJPY, "GBP/JPY": GBPJPY,
}
DRIVERS = {
    "EUR/USD": {
        "en": ["New 9-month low at 1.0968", "18 pips to 1.0950, floor is 60", "Minutes came after the fix"],
        "pt": ["Nova mín. de 9 meses em 1.0968", "18 pips até 1.0950, piso é 60", "Ata saiu depois do fixing"],
    },
    "USD/JPY": {
        "en": ["Back to 159.42, still under 160", "Floor still 2.5-sigma, 121 pips", "SMA200 is 69 pips away"],
        "pt": ["De volta a 159,42, ainda sob 160", "Piso segue 2,5σ, 121 pips", "SMA200 está a 69 pips"],
    },
    "AUD/USD": {
        "en": ["New 9-month low at 0.6731", "31 pips to 0.6700, floor is 49", "RBA still 4.85%"],
        "pt": ["Nova mín. de 9 meses em 0.6731", "31 pips até 0.6700, piso é 49", "RBA ainda 4,85%"],
    },
    "GBP/USD": {
        "en": ["9 pips above the 9-month low", "CPI 3.6%, cable still fell", "Floor is 70 pips"],
        "pt": ["9 pips acima da mín. de 9 meses", "CPI 3,6%, a libra mesmo assim caiu", "Piso é 70 pips"],
    },
    "EUR/JPY": {
        "en": ["Second close through 175.00", "85 pips to 174.00, floor is 177", "MoF floor still open"],
        "pt": ["Segundo fechamento sob 175,00", "85 pips até 174,00, piso é 177", "Piso do MoF segue aberto"],
    },
    "GBP/JPY": {
        "en": ["Under 210 and under the SMA50", "209.61 is 32 pips, floor is 183", "9-month low inside the target"],
        "pt": ["Sob 210 e sob a SMA50", "209,61 está a 32 pips, piso é 183", "Mín. de 9 meses dentro do alvo"],
    },
}

NEWS_ITEM_JS = r'''                {
                    date: "18/11/2026",
                    category: "macro",
                    impact: "high",
                    pairs: ["EUR/USD", "USD/JPY", "AUD/USD", "GBP/USD", "EUR/JPY", "GBP/JPY"],
                    pt: {
                        headline: "A libra para a 9 pips de 1.3160 depois do CPI a 3,6% — o euro fica a 18 pips de 1.0950, e os seis seguem sem ticket",
                        summary: "A taxa BCE/Frankfurter de 18/11 estende as mínimas. GBP/USD fechou 1,3169 (−0,17%), nova mínima de 10/20 pregões, a 9 pips de 1.3160, com piso de 70. O CPI do Reino Unido em outubro subiu para 3,6%, de 3,5%, em linha e abaixo dos 3,7% do BoE. Núcleo 2,8% e serviços 3,7%, sem mudança (ONS, 07:00 UTC). O dado está no fixing e a libra caiu. EUR/USD fechou 1,0968 (−0,19%), a 18 pips de 1.0950, piso de 60. AUD/USD 0,6731 (−0,05%) ficou a 31 pips de 0.6700, piso de 49. USD/JPY 159,42 (+0,08%) segue sob 160, com a SMA200 a 69 pips e o piso em 121. EUR/JPY 174,85 fez o segundo fechamento sob 175,51 e perdeu 175,00. Até 174,00 são 85 pips, piso de 177. GBP/JPY 209,93 perdeu 210 e a SMA50. 209,61 está a 32 pips, dentro do piso de 183. A ata do FOMC de 28/10 saiu às 19:00 UTC, depois do fixing: quase todos viram nova alta como provavelmente adequada (AP). Os seis ficam em AGUARDAR. FOMC em 8-9/12.",
                        take: "O CPI não segurou a libra, e 1.3160 ficou dentro do piso. O mesmo mapa vale para 1.0950, 0.6700 e 174,00. A ata não entra neste fechamento. A mesa segue vazia."
                    },
                    en: {
                        headline: "Cable stops 9 pips from 1.3160 after CPI at 3.6% — the euro is 18 pips from 1.0950, and all six stay without a ticket",
                        summary: "The 18/11 ECB/Frankfurter fixing extends the lows. GBP/USD closed 1.3169 (−0.17%), a new 10/20-day low, 9 pips from 1.3160, with a 70-pip floor. UK October CPI rose to 3.6%, from 3.5%, in line and below the BoE's 3.7%. Core 2.8% and services 3.7%, both unchanged (ONS, 07:00 UTC). The print is in the fixing and cable fell. EUR/USD closed 1.0968 (−0.19%), 18 pips from 1.0950, floor 60. AUD/USD 0.6731 (−0.05%) finished 31 pips from 0.6700, floor 49. USD/JPY 159.42 (+0.08%) is still under 160, with the SMA200 69 pips away and the floor at 121. EUR/JPY 174.85 made the second close under 175.51 and lost 175.00. 174.00 is 85 pips away, floor 177. GBP/JPY 209.93 lost 210 and the SMA50. 209.61 is 32 pips away, inside the 183-pip floor. The Oct 28 FOMC minutes came out at 19:00 UTC, after the fixing: almost all participants saw a further hike as likely appropriate (AP). All six stay on WAIT. FOMC on Dec 8-9.",
                        take: "CPI did not hold cable, and 1.3160 sits inside the floor. The same map holds for 1.0950, 0.6700 and 174.00. The minutes are not in this close. The desk stays empty."
                    }
                },
'''

NEWS_CARD = r'''                <!-- News 18/11/2026: UK CPI 3.6%, cable 9 pips from 1.3160; minutes after the fix; all six WAIT -->
                <article class="news-card">
                    <div class="news-card-top">
                        <span class="news-cat"><span class="lang-en">Macro Data</span><span class="lang-pt" style="display:none;">Dados Macro</span></span>
                        <span class="impact-badge high"><span class="lang-en">High Impact</span><span class="lang-pt" style="display:none;">Impacto Alto</span></span>
                        <span class="news-date">18/11/2026</span>
                    </div>
                    <h2 class="news-title">
                        <span class="lang-en">Cable stops 9 pips from 1.3160 after CPI at 3.6% — the euro is 18 pips from 1.0950, and all six stay without a ticket</span>
                        <span class="lang-pt" style="display:none;">A libra para a 9 pips de 1.3160 depois do CPI a 3,6% — o euro fica a 18 pips de 1.0950, e os seis seguem sem ticket</span>
                    </h2>
                    <p class="news-summary">
                        <span class="lang-en">The 18/11 ECB/Frankfurter fixing extends the lows. GBP/USD closed 1.3169 (−0.17%), a new 10/20-day low, 9 pips from 1.3160, with a 70-pip floor. UK October CPI rose to 3.6%, from 3.5%, in line and below the BoE's 3.7%. Core 2.8% and services 3.7%, both unchanged (ONS, 07:00 UTC). The print is in the fixing and cable fell. EUR/USD closed 1.0968 (−0.19%), 18 pips from 1.0950, floor 60. AUD/USD 0.6731 (−0.05%) finished 31 pips from 0.6700, floor 49. USD/JPY 159.42 (+0.08%) is still under 160, with the SMA200 69 pips away and the floor at 121. EUR/JPY 174.85 made the second close under 175.51 and lost 175.00. 174.00 is 85 pips away, floor 177. GBP/JPY 209.93 lost 210 and the SMA50. 209.61 is 32 pips away, inside the 183-pip floor. The Oct 28 FOMC minutes came out at 19:00 UTC, after the fixing: almost all participants saw a further hike as likely appropriate (AP). All six stay on WAIT. FOMC on Dec 8-9.</span>
                        <span class="lang-pt" style="display:none;">A taxa BCE/Frankfurter de 18/11 estende as mínimas. GBP/USD fechou 1,3169 (−0,17%), nova mínima de 10/20 pregões, a 9 pips de 1.3160, com piso de 70. O CPI do Reino Unido em outubro subiu para 3,6%, de 3,5%, em linha e abaixo dos 3,7% do BoE. Núcleo 2,8% e serviços 3,7%, sem mudança (ONS, 07:00 UTC). O dado está no fixing e a libra caiu. EUR/USD fechou 1,0968 (−0,19%), a 18 pips de 1.0950, piso de 60. AUD/USD 0,6731 (−0,05%) ficou a 31 pips de 0.6700, piso de 49. USD/JPY 159,42 (+0,08%) segue sob 160, com a SMA200 a 69 pips e o piso em 121. EUR/JPY 174,85 fez o segundo fechamento sob 175,51 e perdeu 175,00. Até 174,00 são 85 pips, piso de 177. GBP/JPY 209,93 perdeu 210 e a SMA50. 209,61 está a 32 pips, dentro do piso de 183. A ata do FOMC de 28/10 saiu às 19:00 UTC, depois do fixing: quase todos viram nova alta como provavelmente adequada (AP). Os seis ficam em AGUARDAR. FOMC em 8-9/12.</span>
                    </p>
                    <div class="news-take">
                        <span class="take-tag"><span class="lang-en">Desk take</span><span class="lang-pt" style="display:none;">Leitura da mesa</span></span>
                        <span class="lang-en">CPI did not hold cable, and 1.3160 sits inside the floor. The same map holds for 1.0950, 0.6700 and 174.00. The minutes are not in this close. The desk stays empty.</span>
                        <span class="lang-pt" style="display:none;">O CPI não segurou a libra, e 1.3160 ficou dentro do piso. O mesmo mapa vale para 1.0950, 0.6700 e 174,00. A ata não entra neste fechamento. A mesa segue vazia.</span>
                    </div>
                    <div class="news-pairs">
                        <span class="np-label"><span class="lang-en">Watch</span><span class="lang-pt" style="display:none;">Acompanhar</span></span>
                        <a href="eur-usd.html" class="pair-link-chip">EUR/USD</a><a href="usd-jpy.html" class="pair-link-chip">USD/JPY</a><a href="aud-usd.html" class="pair-link-chip">AUD/USD</a><a href="gbp-usd.html" class="pair-link-chip">GBP/USD</a><a href="eur-jpy.html" class="pair-link-chip">EUR/JPY</a><a href="gbp-jpy.html" class="pair-link-chip">GBP/JPY</a>
                    </div>
                </article>

'''

NEW_CAL = '''                <div class="cal-cell">
                    <span class="cal-date">18/11</span>
                    <span class="cal-event"><span class="lang-en">UK CPI 3.6% y/y, from 3.5% (ONS)</span><span class="lang-pt" style="display:none;">CPI do Reino Unido 3,6% a/a, de 3,5% (ONS)</span></span>
                    <div class="cal-meta"><span class="cal-impact high" aria-hidden="true"></span><span class="cal-cur">GBP</span></div>
                </div>
                <div class="cal-cell">
                    <span class="cal-date">18/11</span>
                    <span class="cal-event"><span class="lang-en">Cable 1.3169, 9 pips from the 9-month low</span><span class="lang-pt" style="display:none;">Libra 1,3169, a 9 pips da mín. de 9 meses</span></span>
                    <div class="cal-meta"><span class="cal-impact high" aria-hidden="true"></span><span class="cal-cur">GBP</span></div>
                </div>
                <div class="cal-cell">
                    <span class="cal-date">18/11</span>
                    <span class="cal-event"><span class="lang-en">FOMC minutes 19:00 UTC, after the fix</span><span class="lang-pt" style="display:none;">Ata do FOMC 19:00 UTC, depois do fixing</span></span>
                    <div class="cal-meta"><span class="cal-impact high" aria-hidden="true"></span><span class="cal-cur">USD</span></div>
                </div>
                <div class="cal-cell">
                    <span class="cal-date">09/12</span>
                    <span class="cal-event"><span class="lang-en">FOMC decision, hike still the base case</span><span class="lang-pt" style="display:none;">Decisão do FOMC, alta segue como caso-base</span></span>
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
        "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 587 daily sessions (01/08/2024–17/11/2026).",
        "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 588 daily sessions (01/08/2024–18/11/2026).")
    idx = idx.replace(
        "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, σ20 e Donchian calculados · 587 pregões (01/08/2024 a 17/11/2026).",
        "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, σ20 e Donchian calculados · 588 pregões (01/08/2024 a 18/11/2026).")
    idx = idx.replace(
        'nextEvent: "Retail +0.2% · EUR through 1.1000 · FOMC Dec 8-9"',
        'nextEvent: "UK CPI 3.6% · cable 9 pips from 1.3160 · FOMC Dec 8-9"')
    idx = idx.replace(
        'nextEvent: "Varejo +0,2% · EUR sob 1.1000 · FOMC 8-9/12"',
        'nextEvent: "CPI Reino Unido 3,6% · cabo a 9 pips de 1.3160 · FOMC 8-9/12"')

    start = idx.find("        const forexData = {")
    end = idx.find("        /* ==========================================\n           B. Market metadata")
    if start < 0 or end < 0:
        raise SystemExit("forexData markers missing")
    idx = idx[:start] + "        const forexData = " + json.dumps(DATA, ensure_ascii=False, indent=4) + ";\n\n" + idx[end:]

    d0 = idx.find("        const dailyChanges = {")
    d1 = idx.find("        const macroDrivers = {")
    changes = {
        "EUR/USD": "-0.19%", "USD/JPY": "+0.08%", "AUD/USD": "-0.05%",
        "GBP/USD": "-0.17%", "EUR/JPY": "-0.12%", "GBP/JPY": "-0.10%",
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
    ledger["meta"]["lastUpdated"] = "18/11/2026"
    with open(LEDGER, "w", encoding="utf-8", newline="\n") as f:
        json.dump(ledger, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("ledger lastUpdated only; book still empty")

    with open(NEWS, encoding="utf-8") as f:
        news = f.read()
    news = news.replace(
        "Market Wire · Through 1.1000, Still No Ticket",
        "Market Wire · Cable on the 9-Month Low, Still No Ticket")
    news = news.replace(
        "Telégrafo da Mesa · Através de 1.1000, Ainda Sem Ticket",
        "Telégrafo da Mesa · A Libra na Mínima de 9 Meses, Ainda Sem Ticket")
    news = news.replace(OLD_TS, TS)
    news = news.replace(
        "6 pairs · Retail sales · UK CPI Wed · FOMC Dec 8-9",
        "6 pairs · UK CPI 3.6% · minutes after the fix · FOMC Dec 8-9")
    news = news.replace(
        "6 pares · Varejo dos EUA · CPI do Reino Unido qua · FOMC 8-9/12",
        "6 pares · CPI do Reino Unido 3,6% · ata depois do fixing · FOMC 8-9/12")
    start = news.find('                <div class="cal-cell">')
    end = news.find("            </div>\n        </section>", start)
    if start < 0 or end < 0:
        raise SystemExit("calendar block missing")
    news = news[:start] + NEW_CAL + "\n" + news[end:]
    marker = "                <!-- News 17/11/2026:"
    if marker not in news:
        raise SystemExit("news marker missing")
    news = news.replace(marker, NEWS_CARD + marker, 1)
    with open(NEWS, "w", encoding="utf-8", newline="\n") as f:
        f.write(news)
    print("news.html patched")

    with open(SITEMAP, encoding="utf-8") as f:
        sm = f.read()
    n = sm.count("2026-11-17")
    if n != 9:
        raise SystemExit("expected 9 sitemap dates, found %d" % n)
    sm = sm.replace("2026-11-17", "2026-11-18")
    with open(SITEMAP, "w", encoding="utf-8", newline="\n") as f:
        f.write(sm)
    print("sitemap patched")

    with open(VERIFY, encoding="utf-8") as f:
        v = f.read()
    v = v.replace('TODAY_TS = "17/11/2026 23:07 UTC"', 'TODAY_TS = "%s"' % TS)
    v = v.replace(
        'TODAY_DATE = "17/11/2026"  # basis session date (report edition: 17/11/2026)',
        'TODAY_DATE = "18/11/2026"  # basis session date (report edition: 18/11/2026)')
    old_ticker = '''TICKER = [("EUR/USD","-0.23%"),("USD/JPY","-0.19%"),("AUD/USD","-0.32%"),
          ("GBP/USD","-0.05%"),("EUR/JPY","-0.41%"),("GBP/JPY","-0.24%")]'''
    new_ticker = '''TICKER = [("EUR/USD","-0.19%"),("USD/JPY","+0.08%"),("AUD/USD","-0.05%"),
          ("GBP/USD","-0.17%"),("EUR/JPY","-0.12%"),("GBP/JPY","-0.10%")]'''
    if old_ticker not in v:
        raise SystemExit("ticker block missing")
    v = v.replace(old_ticker, new_ticker)
    with open(VERIFY, "w", encoding="utf-8", newline="\n") as f:
        f.write(v)
    print("verify constants patched")

if __name__ == "__main__":
    main()
