#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""17/11/2026 edition, on the Tuesday 17/11 ECB fixing.

EUR/USD closes through 1.1000 at 1.0989. AUD/USD makes another 9-month low
at 0.6735, 35 pips from 0.6700. EUR/JPY prints a first close through 175.51
and stops 5 pips above 175.00. US retail sales were +0.2% m/m. The MoF
warning of 13/11 is still inside 30 days. No ticket clears the gate.
"""
import json
from datetime import datetime, timezone

INDEX = r"C:/Projetos/forex-report/docs/index.html"
LEDGER = r"C:/Projetos/forex-report/docs/track-record.json"
NEWS = r"C:/Projetos/forex-report/docs/news.html"
SITEMAP = r"C:/Projetos/forex-report/docs/sitemap.xml"
VERIFY = r"C:/Projetos/forex-report/pipeline/verify_all.py"

TS = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
OLD_TS = "16/11/2026 21:15 UTC"
BASIS = "587 sessions, 01/08/2024 to 17/11/2026"
BASIS_PT = "587 pregões, 01/08/2024 a 17/11/2026"

def pair(quote, bias, bias_type, pt, en):
    return {"quote": quote, "bias": bias, "biasType": bias_type, "pt": pt, "en": en}

EUR = pair("1.0989", "BAIXA", "bear",
    pt={
        "fundamental": "O EUR/USD fechou em 1,0989 na sessão de terça 17/11/2026 (taxa de referência BCE/Frankfurter; o terminal MT5 está logado, mas o Market Watch não tem os pares à vista), caindo -0,23% (-25 pips) a partir de 1,1014. O fechamento atravessou 1.1000 por 11 pips e é a nova mínima de 10/20 pregões e de 9 meses. As vendas no varejo dos EUA em outubro subiram 0,2% no mês (Census, em linha com o esperado; setembro sem revisão em +0,8%) e 6,8% no ano. O grupo de controle subiu 0,6% (esperado 0,4%; setembro revisto de +0,1% para +0,5%) (Reuters, 17/11). O Fed segue em 3,75-4,00%, com a decisão de 8-9/12 ainda no debate de 25 ou 50 pb. O próximo redondo, 1.0950, está a 39 pips. O piso de 1,5σ20 é de 61 pips, então o stop que paga o piso já atravessa 1.0950. Um stop sobre a mínima de segunda (1,1014) fica a 25 pips. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (1,1520) com a SMA50 (1,1276) abaixo dela — alinhamento de baixa pleno. O próprio fechamento é a mínima de 10/20 pregões e de 9 meses. A máxima de 10/20 pregões segue 1.1267 (04/11).",
        "support": "1.0950 (o próximo redondo, 39 pips abaixo) e 1.0900 (89 pips). O fechamento de 17/11 (1,0989) é a mínima de 9 meses.",
        "resistance": "1.1000 (o redondo perdido, 11 pips acima) e 1.1014 (a mínima de segunda), com a SMA50 em 1,1276.",
        "priceAction": "1.1000 cedeu e 1.0950 ficou dentro do piso de 61. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "O fechamento sob 1.1000 saiu. 39 pips até 1.0950 são menos que o piso. O stop legal já cai do outro lado desse redondo. Sem gatilho novo.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O euro fez o que segunda não cabia — perdeu 1.1000 — e o próximo redondo continua curto demais para um stop de 61 pips."
    },
    en={
        "fundamental": "EUR/USD closed at 1.0989 in the Tuesday 17/11/2026 session (ECB/Frankfurter reference rate; the MT5 terminal is logged in, but Market Watch has no spot pairs), down -0.23% (-25 pips) from 1.1014. The close went through 1.1000 by 11 pips and is the new 10/20-day and 9-month low. US October retail sales rose 0.2% on the month (Census, in line with the forecast; September unrevised at +0.8%) and 6.8% on the year. The control group rose 0.6% (expected 0.4%; September revised from +0.1% to +0.5%) (Reuters, Nov 17). The Fed is still at 3.75-4.00%, with the Dec 8-9 decision still a 25-or-50 bp debate. The next round, 1.0950, is 39 pips away. The 1.5-sigma20 floor is 61 pips, so the stop that meets the floor is already through 1.0950. A stop over Monday's low (1.1014) is 25 pips. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (1.1520) with the 50-day (1.1276) below it — full bear alignment. Today's close is the 10/20-day and 9-month low. The 10/20-day high is still 1.1267 (Nov 4).",
        "support": "1.0950 (the next round, 39 pips below) and 1.0900 (89 pips). The Nov-17 close (1.0989) is the 9-month low.",
        "resistance": "1.1000 (the round just lost, 11 pips above) and 1.1014 (Monday's low), with the SMA50 at 1.1276.",
        "priceAction": "1.1000 gave way and 1.0950 sits inside the 61-pip floor. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The close under 1.1000 has printed. 39 pips down to 1.0950 is less than the floor. The legal stop already lands on the other side of that round. No new trigger.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The euro did what Monday could not fit — it lost 1.1000 — and the next round is still too close for a 61-pip stop."
    })

USDJPY = pair("159.30", "NEUTRO", "neutral",
    pt={
        "fundamental": "O USD/JPY fechou em 159,30 na sessão de terça 17/11/2026 (taxa de referência BCE/Frankfurter), caindo -0,19% (-30 pips) a partir de 159,60. É o segundo fechamento seguido sob 160,00. A máxima de 10 pregões segue 160,00 (13/11). O aviso de Katayama de 13/11 continua dentro de 30 dias, e não houve intervenção confirmada. O piso segue em 2,5σ20, aqui 122 pips. O mapa continua misto — fechamento acima da SMA200 (158,72), SMA50 (157,58) ainda abaixo. Daqui até a SMA200 são 58 pips, menos que o piso. Um stop sob a SMA50 (~172 pips) cabe, e o alvo de 1 para 2 atravessa 160, 161 e 162. Não há alinhamento de alta. O BoJ segue em 1,25%. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento acima da SMA200 (158,72), com a SMA50 (157,58) ainda abaixo — alinhamento misto. A máxima de 9 meses segue 163,91. A máxima de 10 pregões é 160,00 (13/11).",
        "support": "158.72 (a SMA200, 58 pips abaixo) e 157.95 (mínima de 10 pregões, 09/11), com a SMA50 em 157,58.",
        "resistance": "160.00 (máxima de 10 pregões, 13/11) e 161.00, com a máxima de 9 meses em 163,91.",
        "priceAction": "Mais 30 pips de devolução, ainda longe de um long legal. 58 pips até a SMA200 não pagam o piso de 122. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "160.00 segue acima. Comprar 159,30 com stop sob a SMA200 falha o piso de 122 pips. O stop que paga o piso esbarra em 160, 161 e 162. Vender não tem alinhamento de baixa. Reavaliar se o MoF agir, ou depois do FOMC de 8-9/12.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O iene ganhou mais 30 pips e o varejo americano saiu em linha. O piso de 2,5σ20 continua mais largo que a distância até a SMA200."
    },
    en={
        "fundamental": "USD/JPY closed at 159.30 in the Tuesday 17/11/2026 session (ECB/Frankfurter reference rate), down -0.19% (-30 pips) from 159.60. It is a second straight close under 160.00. The 10-day high is still 160.00 (Nov 13). Katayama's Nov 13 warning is still inside 30 days, and no intervention has been confirmed. The floor stays at 2.5-sigma20, here 122 pips. The map stays mixed — close above the SMA200 (158.72), the SMA50 (157.58) still below. The SMA200 is 58 pips down, short of the floor. A stop under the SMA50 (~172 pips) fits, and the one-to-two target crosses 160, 161 and 162. There is no bull alignment. The BoJ is still at 1.25%. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close above the SMA200 (158.72), with the SMA50 (157.58) still below — mixed alignment. The 9-month high remains 163.91. The 10-day high is 160.00 (Nov 13).",
        "support": "158.72 (the SMA200, 58 pips below) and 157.95 (the 10-day low, Nov 9), with the SMA50 at 157.58.",
        "resistance": "160.00 (the 10-day high, Nov 13) and 161.00, with the 9-month high at 163.91.",
        "priceAction": "Another 30 pips handed back, still short of a legal long. 58 pips down to the SMA200 does not pay the 122-pip floor. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "160.00 is still overhead. Buying 159.30 with a stop under the SMA200 misses the 122-pip floor. The stop that clears the floor runs into 160, 161 and 162. A short has no bear alignment. Reassess if the MoF acts, or after the Dec 8-9 FOMC.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The yen took another 30 pips and US retail sales printed in line. The 2.5-sigma20 floor is still wider than the distance to the SMA200."
    })

AUD = pair("0.6735", "BAIXA", "bear",
    pt={
        "fundamental": "O AUD/USD fechou em 0,6735 na sessão de terça 17/11/2026 (taxa de referência BCE/Frankfurter), caindo -0,32% (-22 pips) a partir de 0,6757. É mais um fechamento na mínima de 9 meses e de 10/20 pregões. A SMA50 (0,6998) está sob a SMA200 (0,7050). O piso de 1,5σ20 é de 53 pips. Até 0.6700 são 35 pips, então o stop que paga o piso já atravessa esse redondo. Um stop sobre 0.6757 fica a 22 pips e não paga o piso. O RBA está em 4,85%. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (0,7050) com a SMA50 (0,6998) abaixo dela — alinhamento de baixa. O próprio fechamento é a mínima de 10/20 pregões e de 9 meses. A máxima de 10 pregões está em 0.7015 (04/11).",
        "support": "0.6700 (o próximo redondo, 35 pips abaixo). O fechamento de 17/11 (0,6735) é a mínima de 9 meses.",
        "resistance": "0.6757 (a mínima de segunda, devolvida) e 0.6800, com a máxima de 10 pregões em 0.7015.",
        "priceAction": "A mínima estendeu mais 22 pips. 0.6700 ficou dentro do piso de 53. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "O fechamento sob 0,6757 saiu. 35 pips até 0.6700 são menos que o piso. Sem gatilho novo.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O Aussie fez outra mínima e o redondo seguinte continua mais perto do que o piso permite. O livro segue de fora."
    },
    en={
        "fundamental": "AUD/USD closed at 0.6735 in the Tuesday 17/11/2026 session (ECB/Frankfurter reference rate), down -0.32% (-22 pips) from 0.6757. It is another close at the 9-month and 10/20-day low. The SMA50 (0.6998) sits under the SMA200 (0.7050). The 1.5-sigma20 floor is 53 pips. 0.6700 is 35 pips away, so the stop that meets the floor is already through that round. A stop over 0.6757 is 22 pips and misses the floor. The RBA cash rate is 4.85%. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (0.7050) with the SMA50 (0.6998) below it — bear alignment. Today's close is the 10/20-day and 9-month low. The 10-day high is 0.7015 (Nov 4).",
        "support": "0.6700 (the next round, 35 pips below). The Nov-17 close (0.6735) is the 9-month low.",
        "resistance": "0.6757 (Monday's low, handed back) and 0.6800, with the 10-day high at 0.7015.",
        "priceAction": "The low extended another 22 pips. 0.6700 sits inside the 53-pip floor. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The close under 0.6757 has printed. 35 pips down to 0.6700 is less than the floor. No new trigger.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The Aussie made another low and the next round is still closer than the floor allows. The book stays out."
    })

GBP = pair("1.3191", "BAIXA", "bear",
    pt={
        "fundamental": "O GBP/USD fechou em 1,3191 na sessão de terça 17/11/2026 (taxa de referência BCE/Frankfurter), caindo -0,05% (-7 pips) a partir de 1,3198. É a nova mínima de 10/20 pregões por uma margem curta. A mínima de 9 meses segue 1.3160, a 31 pips. O piso de 1,5σ20 é de 73 pips, então o stop que paga o piso já atravessa essa mínima. Um stop sobre 1.3198 fica a 7 pips. A Bank Rate está em 4,00%. O CPI do Reino Unido de outubro sai na quarta 18/11, dentro da janela de 24 horas — e o piso já recusa o ticket antes do dado. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (1,3413) e sob a SMA50 (1,3333), com a SMA50 abaixo da SMA200 — alinhamento de baixa. A máxima de 10/20 pregões segue 1.3500 (04/11).",
        "support": "1.3160 (mínima de 9 meses, 31 pips abaixo). O fechamento de 17/11 é a mínima de 10/20 pregões.",
        "resistance": "1.3198 (a mínima de segunda, devolvida) e 1.3333 (a SMA50), com a SMA200 em 1,3413.",
        "priceAction": "Quase parado, 31 pips acima do extremo de 9 meses e com piso de 73. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "O fechamento sob 1,3198 saiu por 7 pips. O espaço até 1.3160 é menor que o piso. Reavaliar depois do CPI de quarta.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "A libra quase não andou e parou antes de 1.3160. Vender aqui coloca a mínima de 9 meses dentro do stop, e o CPI de quarta está dentro de 24 horas."
    },
    en={
        "fundamental": "GBP/USD closed at 1.3191 in the Tuesday 17/11/2026 session (ECB/Frankfurter reference rate), down -0.05% (-7 pips) from 1.3198. It is the new 10/20-day low by a thin margin. The 9-month low is still 1.3160, 31 pips away. The 1.5-sigma20 floor is 73 pips, so the stop that meets the floor is already through that low. A stop over 1.3198 is 7 pips. Bank Rate is 4.00%. October UK CPI is due Wednesday 18/11, inside the 24-hour window — and the floor already refuses the ticket before the print. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (1.3413) and under the SMA50 (1.3333), with the SMA50 below the SMA200 — bear alignment. The 10/20-day high is still 1.3500 (Nov 4).",
        "support": "1.3160 (the 9-month low, 31 pips below). The Nov-17 close is the 10/20-day low.",
        "resistance": "1.3198 (Monday's low, handed back) and 1.3333 (the SMA50), with the SMA200 at 1.3413.",
        "priceAction": "Almost unchanged, 31 pips above the 9-month extreme and with a 73-pip floor. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The close under 1.3198 printed by 7 pips. The room down to 1.3160 is smaller than the floor. Reassess after Wednesday's CPI.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "Sterling barely moved and stopped short of 1.3160. Selling here puts the 9-month low inside the stop, and Wednesday's CPI is inside 24 hours."
    })

EURJPY = pair("175.05", "BAIXA", "bear",
    pt={
        "fundamental": "O EUR/JPY fechou em 175,05 na sessão de terça 17/11/2026 (taxa de referência BCE/Frankfurter), caindo -0,41% (-73 pips) a partir de 175,78. É o primeiro fechamento através da mínima de 9 meses de 175,51 (23/10), que ficou 46 pips acima. A regra pede um segundo fechamento nesse extremo. O redondo 175,00 está 5 pips abaixo. O aviso do MoF de 13/11 mantém o piso em 2,5σ20, aqui 177 pips, então qualquer stop legal já atravessa 175,00. A SMA50 está em 177,67 (~262 pips acima) e a SMA200 em 182,83. Alinhamento de baixa. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (182,83) com a SMA50 (177,67) abaixo dela — alinhamento de baixa pleno. O próprio fechamento é a mínima de 10/20 pregões e de 9 meses. A máxima de 10 pregões está em 178,30 (04/11).",
        "support": "175.00 (o redondo, 5 pips abaixo). O fechamento de 17/11 (175,05) é a nova mínima de 9 meses.",
        "resistance": "175.51 (a mínima antiga de 9 meses, 23/10, agora 46 pips acima) e 177.67 (a SMA50).",
        "priceAction": "175,51 cedeu e 175,00 ficou dentro do piso de 177. Falta o segundo fechamento, e o stop legal não cabe acima do redondo. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "O primeiro fechamento sob 175,51 saiu. O segundo ainda não, e 5 pips até 175,00 são menos que o piso de 177. Reavaliar se o MoF agir.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O cruzado atravessou o extremo que segunda deixou a 28 pips, e parou em cima de 175,00. Com o piso em 177 pips, não há stop que fique deste lado do redondo."
    },
    en={
        "fundamental": "EUR/JPY closed at 175.05 in the Tuesday 17/11/2026 session (ECB/Frankfurter reference rate), down -0.41% (-73 pips) from 175.78. It is the first close through the 9-month low at 175.51 (Oct 23), which is now 46 pips overhead. The rule asks for a second close through that extreme. The 175.00 round is 5 pips below. The MoF warning of Nov 13 keeps the floor at 2.5-sigma20, here 177 pips, so any legal stop is already through 175.00. The SMA50 is at 177.67 (~262 pips above) and the SMA200 at 182.83. Bear alignment. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (182.83) with the SMA50 (177.67) below it — full bear alignment. Today's close is the 10/20-day and 9-month low. The 10-day high is 178.30 (Nov 4).",
        "support": "175.00 (the round, 5 pips below). The Nov-17 close (175.05) is the new 9-month low.",
        "resistance": "175.51 (the prior 9-month low, Oct 23, now 46 pips above) and 177.67 (the SMA50).",
        "priceAction": "175.51 gave way and 175.00 sits inside the 177-pip floor. The second close is still missing, and a legal stop does not fit above the round. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The first close under 175.51 has printed. The second has not, and 5 pips down to 175.00 is less than the 177-pip floor. Reassess if the MoF acts.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The cross went through the extreme Monday left 28 pips away, and stopped on top of 175.00. With the floor at 177 pips, no stop stays on this side of the round."
    })

GBPJPY = pair("210.14", "BAIXA", "bear",
    pt={
        "fundamental": "O GBP/JPY fechou em 210,14 na sessão de terça 17/11/2026 (taxa de referência BCE/Frankfurter), caindo -0,24% (-51 pips) a partir de 210,65. O fechamento é a nova mínima de 10 pregões. A mínima de 20 pregões segue 209,61, a 52 pips, e a de 9 meses 207,32, a 281 pips. O preço está cerca de 4 pips acima da SMA50 (210,09). O alinhamento segue de baixa porque o fechamento e a SMA50 estão sob a SMA200 (212,89), 275 pips acima. O piso, ainda aberto pelo jawboning do MoF, é de 186 pips. A SMA200 cobre esse piso, e o alvo de um stop de 186 pips (372 pips) atravessa 209,61 e 207,32. O CPI do Reino Unido de quarta está dentro de 24 horas. BoE em 4,00%, BoJ em 1,25%. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (212,89) com a SMA50 (210,09) também sob a SMA200 — alinhamento de baixa, com o preço ainda um fio acima da SMA50. A máxima de 10/20 pregões está em 213,63 (04/11).",
        "support": "209.61 (mínima de 20 pregões, 52 pips abaixo) e 207.32 (mínima de 9 meses, 281 pips). A SMA50 (210,09) ficou sob o preço.",
        "resistance": "212.89 (a SMA200, 275 pips acima) e 213.63 (máxima de 10/20 pregões). 210.65 é o fechamento de segunda, devolvido.",
        "priceAction": "Nova mínima de 10 pregões por 51 pips. 209,61 está dentro do piso de 186, e o alvo que paga o piso atravessa 207,32. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "Vender a perda de 210,65 com stop sobre 212,89 paga o piso e atravessa a mínima de 20 pregões e a de 9 meses. Reavaliar depois do CPI de quarta.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O cruzado desceu 51 pips e o caminho não abriu. 52 pips até 209,61 são menos que o piso, e o alvo legal cai do outro lado de 207,32."
    },
    en={
        "fundamental": "GBP/JPY closed at 210.14 in the Tuesday 17/11/2026 session (ECB/Frankfurter reference rate), down -0.24% (-51 pips) from 210.65. The close is the new 10-day low. The 20-day low is still 209.61, 52 pips away, and the 9-month low is 207.32, 281 pips away. Price is about 4 pips above the SMA50 (210.09). Alignment stays bearish because the close and the SMA50 are both under the SMA200 (212.89), 275 pips above. The floor, still open from the MoF jawboning, is 186 pips. The SMA200 covers that floor, and the target of a 186-pip stop (372 pips) crosses 209.61 and 207.32. Wednesday's UK CPI is inside 24 hours. BoE at 4.00%, BoJ at 1.25%. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (212.89) with the SMA50 (210.09) also under the SMA200 — bear alignment, with price still a thread above the SMA50. The 10/20-day high is 213.63 (Nov 4).",
        "support": "209.61 (the 20-day low, 52 pips below) and 207.32 (the 9-month low, 281 pips). The SMA50 (210.09) is under price.",
        "resistance": "212.89 (the SMA200, 275 pips above) and 213.63 (the 10/20-day high). 210.65 is Monday's close, handed back.",
        "priceAction": "A new 10-day low by 51 pips. 209.61 sits inside the 186-pip floor, and the target that pays the floor crosses 207.32. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "Selling the loss of 210.65 with a stop over 212.89 clears the floor and runs through the 20-day low and the 9-month low. Reassess after Wednesday's CPI.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The cross dropped 51 pips and the path did not open. 52 pips down to 209.61 is less than the floor, and the legal target lands on the other side of 207.32."
    })

DATA = {
    "EUR/USD": EUR, "USD/JPY": USDJPY, "AUD/USD": AUD,
    "GBP/USD": GBP, "EUR/JPY": EURJPY, "GBP/JPY": GBPJPY,
}
DRIVERS = {
    "EUR/USD": {
        "en": ["Through 1.1000 by 11 pips", "39 pips to 1.0950, floor is 61", "Retail sales +0.2% m/m"],
        "pt": ["Através de 1.1000 por 11 pips", "39 pips até 1.0950, piso é 61", "Varejo +0,2% no mês"],
    },
    "USD/JPY": {
        "en": ["Second close under 160, at 159.30", "Floor still 2.5-sigma, 122 pips", "SMA200 is 58 pips away"],
        "pt": ["Segundo fechamento sob 160, em 159,30", "Piso segue 2,5σ, 122 pips", "SMA200 está a 58 pips"],
    },
    "AUD/USD": {
        "en": ["New 9-month low at 0.6735", "35 pips to 0.6700, floor is 53", "RBA still 4.85%"],
        "pt": ["Nova mín. de 9 meses em 0.6735", "35 pips até 0.6700, piso é 53", "RBA ainda 4,85%"],
    },
    "GBP/USD": {
        "en": ["7 pips lower, still above 1.3160", "31 pips to the 9-month low, floor 73", "UK CPI is Wednesday"],
        "pt": ["7 pips abaixo, ainda sobre 1.3160", "31 pips até a mín. de 9m, piso 73", "CPI do Reino Unido é quarta"],
    },
    "EUR/JPY": {
        "en": ["First close through 175.51", "175.00 is 5 pips away", "Floor still 177 pips"],
        "pt": ["Primeiro fechamento sob 175,51", "175,00 está a 5 pips", "Piso segue 177 pips"],
    },
    "GBP/JPY": {
        "en": ["New 10-day low at 210.14", "209.61 is 52 pips, floor is 186", "9-month low inside the target"],
        "pt": ["Nova mín. de 10 pregões em 210,14", "209,61 está a 52 pips, piso é 186", "Mín. de 9 meses dentro do alvo"],
    },
}

NEWS_ITEM_JS = r'''                {
                    date: "17/11/2026",
                    category: "macro",
                    impact: "high",
                    pairs: ["EUR/USD", "USD/JPY", "AUD/USD", "GBP/USD", "EUR/JPY", "GBP/JPY"],
                    pt: {
                        headline: "O euro perde 1.1000 e o Aussie chega a 35 pips de 0.6700 — o varejo saiu em linha, e os seis seguem sem ticket",
                        summary: "A taxa BCE/Frankfurter de 17/11 estende o dólar. EUR/USD fechou 1,0989 (−0,23%), através de 1.1000 por 11 pips, com 1.0950 a 39 pips e piso de 61. AUD/USD fechou 0,6735 (−0,32%), nova mínima de 9 meses, com 0.6700 a 35 pips e piso de 53. GBP/USD 1,3191 (−0,05%) ficou a 31 pips de 1.3160, piso de 73, e o CPI do Reino Unido é quarta, dentro de 24 horas. USD/JPY fechou 159,30 (−0,19%), segundo fechamento sob 160. A SMA200 está a 58 pips e o piso segue em 122, com o aviso de Katayama de 13/11 ainda na janela de 30 dias. EUR/JPY 175,05 fez o primeiro fechamento sob 175,51 e parou 5 pips acima de 175,00, com piso de 177. GBP/JPY 210,14 fez mínima de 10 pregões, e 209,61 está a 52 pips, dentro do piso de 186. As vendas no varejo dos EUA subiram 0,2% no mês e 6,8% no ano (Census); o grupo de controle subiu 0,6% (Reuters). Os seis ficam em AGUARDAR. FOMC em 8-9/12.",
                        take: "1.1000 cedeu e o próximo redondo continua dentro do piso. O mesmo mapa vale para 0.6700 e para 175,00. A mesa segue vazia."
                    },
                    en: {
                        headline: "The euro loses 1.1000 and the Aussie gets within 35 pips of 0.6700 — retail sales printed in line, and all six stay without a ticket",
                        summary: "The 17/11 ECB/Frankfurter fixing extends the dollar. EUR/USD closed 1.0989 (−0.23%), through 1.1000 by 11 pips, with 1.0950 39 pips away and a 61-pip floor. AUD/USD closed 0.6735 (−0.32%), a new 9-month low, with 0.6700 35 pips away and a 53-pip floor. GBP/USD 1.3191 (−0.05%) finished 31 pips from 1.3160, floor 73, and UK CPI is Wednesday, inside 24 hours. USD/JPY closed 159.30 (−0.19%), a second close under 160. The SMA200 is 58 pips away and the floor stays at 122, with Katayama's Nov 13 warning still inside the 30-day window. EUR/JPY 175.05 made the first close under 175.51 and stopped 5 pips above 175.00, with a 177-pip floor. GBP/JPY 210.14 made a 10-day low, and 209.61 is 52 pips away, inside the 186-pip floor. US retail sales rose 0.2% on the month and 6.8% on the year (Census); the control group rose 0.6% (Reuters). All six stay on WAIT. FOMC on Dec 8-9.",
                        take: "1.1000 gave way and the next round is still inside the floor. The same map holds for 0.6700 and for 175.00. The desk stays empty."
                    }
                },
'''

NEWS_CARD = r'''                <!-- News 17/11/2026: euro through 1.1000, Aussie 35 pips from 0.6700; retail sales in line; all six WAIT -->
                <article class="news-card">
                    <div class="news-card-top">
                        <span class="news-cat"><span class="lang-en">Macro Data</span><span class="lang-pt" style="display:none;">Dados Macro</span></span>
                        <span class="impact-badge high"><span class="lang-en">High Impact</span><span class="lang-pt" style="display:none;">Impacto Alto</span></span>
                        <span class="news-date">17/11/2026</span>
                    </div>
                    <h2 class="news-title">
                        <span class="lang-en">The euro loses 1.1000 and the Aussie gets within 35 pips of 0.6700 — retail sales printed in line, and all six stay without a ticket</span>
                        <span class="lang-pt" style="display:none;">O euro perde 1.1000 e o Aussie chega a 35 pips de 0.6700 — o varejo saiu em linha, e os seis seguem sem ticket</span>
                    </h2>
                    <p class="news-summary">
                        <span class="lang-en">The 17/11 ECB/Frankfurter fixing extends the dollar. EUR/USD closed 1.0989 (−0.23%), through 1.1000 by 11 pips, with 1.0950 39 pips away and a 61-pip floor. AUD/USD closed 0.6735 (−0.32%), a new 9-month low, with 0.6700 35 pips away and a 53-pip floor. GBP/USD 1.3191 (−0.05%) finished 31 pips from 1.3160, floor 73, and UK CPI is Wednesday, inside 24 hours. USD/JPY closed 159.30 (−0.19%), a second close under 160. The SMA200 is 58 pips away and the floor stays at 122, with Katayama's Nov 13 warning still inside the 30-day window. EUR/JPY 175.05 made the first close under 175.51 and stopped 5 pips above 175.00, with a 177-pip floor. GBP/JPY 210.14 made a 10-day low, and 209.61 is 52 pips away, inside the 186-pip floor. US retail sales rose 0.2% on the month and 6.8% on the year (Census); the control group rose 0.6% (Reuters). All six stay on WAIT. FOMC on Dec 8-9.</span>
                        <span class="lang-pt" style="display:none;">A taxa BCE/Frankfurter de 17/11 estende o dólar. EUR/USD fechou 1,0989 (−0,23%), através de 1.1000 por 11 pips, com 1.0950 a 39 pips e piso de 61. AUD/USD fechou 0,6735 (−0,32%), nova mínima de 9 meses, com 0.6700 a 35 pips e piso de 53. GBP/USD 1,3191 (−0,05%) ficou a 31 pips de 1.3160, piso de 73, e o CPI do Reino Unido é quarta, dentro de 24 horas. USD/JPY fechou 159,30 (−0,19%), segundo fechamento sob 160. A SMA200 está a 58 pips e o piso segue em 122, com o aviso de Katayama de 13/11 ainda na janela de 30 dias. EUR/JPY 175,05 fez o primeiro fechamento sob 175,51 e parou 5 pips acima de 175,00, com piso de 177. GBP/JPY 210,14 fez mínima de 10 pregões, e 209,61 está a 52 pips, dentro do piso de 186. As vendas no varejo dos EUA subiram 0,2% no mês e 6,8% no ano (Census); o grupo de controle subiu 0,6% (Reuters). Os seis ficam em AGUARDAR. FOMC em 8-9/12.</span>
                    </p>
                    <div class="news-take">
                        <span class="take-tag"><span class="lang-en">Desk take</span><span class="lang-pt" style="display:none;">Leitura da mesa</span></span>
                        <span class="lang-en">1.1000 gave way and the next round is still inside the floor. The same map holds for 0.6700 and for 175.00. The desk stays empty.</span>
                        <span class="lang-pt" style="display:none;">1.1000 cedeu e o próximo redondo continua dentro do piso. O mesmo mapa vale para 0.6700 e para 175,00. A mesa segue vazia.</span>
                    </div>
                    <div class="news-pairs">
                        <span class="np-label"><span class="lang-en">Watch</span><span class="lang-pt" style="display:none;">Acompanhar</span></span>
                        <a href="eur-usd.html" class="pair-link-chip">EUR/USD</a><a href="usd-jpy.html" class="pair-link-chip">USD/JPY</a><a href="aud-usd.html" class="pair-link-chip">AUD/USD</a><a href="gbp-usd.html" class="pair-link-chip">GBP/USD</a><a href="eur-jpy.html" class="pair-link-chip">EUR/JPY</a><a href="gbp-jpy.html" class="pair-link-chip">GBP/JPY</a>
                    </div>
                </article>

'''

NEW_CAL = '''                <div class="cal-cell">
                    <span class="cal-date">17/11</span>
                    <span class="cal-event"><span class="lang-en">US retail sales +0.2% m/m, +6.8% y/y</span><span class="lang-pt" style="display:none;">Varejo dos EUA +0,2% m/m, +6,8% a/a</span></span>
                    <div class="cal-meta"><span class="cal-impact high" aria-hidden="true"></span><span class="cal-cur">USD</span></div>
                </div>
                <div class="cal-cell">
                    <span class="cal-date">17/11</span>
                    <span class="cal-event"><span class="lang-en">EUR/USD through 1.1000, close 1.0989</span><span class="lang-pt" style="display:none;">EUR/USD sob 1.1000, fechamento 1,0989</span></span>
                    <div class="cal-meta"><span class="cal-impact high" aria-hidden="true"></span><span class="cal-cur">EUR</span></div>
                </div>
                <div class="cal-cell">
                    <span class="cal-date">18/11</span>
                    <span class="cal-event"><span class="lang-en">UK CPI, October (inside 24 hours)</span><span class="lang-pt" style="display:none;">CPI do Reino Unido, outubro (dentro de 24 horas)</span></span>
                    <div class="cal-meta"><span class="cal-impact high" aria-hidden="true"></span><span class="cal-cur">GBP</span></div>
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
        "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 586 daily sessions (01/08/2024–16/11/2026).",
        "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 587 daily sessions (01/08/2024–17/11/2026).")
    idx = idx.replace(
        "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, σ20 e Donchian calculados · 586 pregões (01/08/2024 a 16/11/2026).",
        "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, σ20 e Donchian calculados · 587 pregões (01/08/2024 a 17/11/2026).")
    idx = idx.replace(
        'nextEvent: "Japan GDP -0.1% · China retail +0.4% · FOMC Dec 8-9"',
        'nextEvent: "Retail +0.2% · EUR through 1.1000 · FOMC Dec 8-9"')
    idx = idx.replace(
        'nextEvent: "PIB Japão -0,1% · varejo China +0,4% · FOMC 8-9/12"',
        'nextEvent: "Varejo +0,2% · EUR sob 1.1000 · FOMC 8-9/12"')

    start = idx.find("        const forexData = {")
    end = idx.find("        /* ==========================================\n           B. Market metadata")
    if start < 0 or end < 0:
        raise SystemExit("forexData markers missing")
    idx = idx[:start] + "        const forexData = " + json.dumps(DATA, ensure_ascii=False, indent=4) + ";\n\n" + idx[end:]

    d0 = idx.find("        const dailyChanges = {")
    d1 = idx.find("        const macroDrivers = {")
    changes = {
        "EUR/USD": "-0.23%", "USD/JPY": "-0.19%", "AUD/USD": "-0.32%",
        "GBP/USD": "-0.05%", "EUR/JPY": "-0.41%", "GBP/JPY": "-0.24%",
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
    ledger["meta"]["lastUpdated"] = "17/11/2026"
    with open(LEDGER, "w", encoding="utf-8", newline="\n") as f:
        json.dump(ledger, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("ledger lastUpdated only; book still empty")

    with open(NEWS, encoding="utf-8") as f:
        news = f.read()
    news = news.replace(
        "Market Wire · Dollar Extends, Yen Hands 160 Back",
        "Market Wire · Through 1.1000, Still No Ticket")
    news = news.replace(
        "Telégrafo da Mesa · O Dólar Estende, o Iene Devolve 160",
        "Telégrafo da Mesa · Através de 1.1000, Ainda Sem Ticket")
    news = news.replace(OLD_TS, TS)
    news = news.replace(
        "6 pairs · Japan GDP · China data · FOMC Dec 8-9",
        "6 pairs · Retail sales · UK CPI Wed · FOMC Dec 8-9")
    news = news.replace(
        "6 pares · PIB do Japão · dados da China · FOMC 8-9/12",
        "6 pares · Varejo dos EUA · CPI do Reino Unido qua · FOMC 8-9/12")
    start = news.find('                <div class="cal-cell">')
    end = news.find("            </div>\n        </section>", start)
    if start < 0 or end < 0:
        raise SystemExit("calendar block missing")
    news = news[:start] + NEW_CAL + "\n" + news[end:]
    marker = "                <!-- News 16/11/2026:"
    if marker not in news:
        raise SystemExit("news marker missing")
    news = news.replace(marker, NEWS_CARD + marker, 1)
    with open(NEWS, "w", encoding="utf-8", newline="\n") as f:
        f.write(news)
    print("news.html patched")

    with open(SITEMAP, encoding="utf-8") as f:
        sm = f.read()
    n = sm.count("2026-11-16")
    if n != 9:
        raise SystemExit("expected 9 sitemap dates, found %d" % n)
    sm = sm.replace("2026-11-16", "2026-11-17")
    with open(SITEMAP, "w", encoding="utf-8", newline="\n") as f:
        f.write(sm)
    print("sitemap patched")

    with open(VERIFY, encoding="utf-8") as f:
        v = f.read()
    v = v.replace('TODAY_TS = "16/11/2026 21:15 UTC"', 'TODAY_TS = "%s"' % TS)
    v = v.replace(
        'TODAY_DATE = "16/11/2026"  # basis session date (report edition: 16/11/2026)',
        'TODAY_DATE = "17/11/2026"  # basis session date (report edition: 17/11/2026)')
    old_ticker = '''TICKER = [("EUR/USD","-0.34%"),("USD/JPY","-0.25%"),("AUD/USD","-0.42%"),
          ("GBP/USD","-0.21%"),("EUR/JPY","-0.59%"),("GBP/JPY","-0.46%")]'''
    new_ticker = '''TICKER = [("EUR/USD","-0.23%"),("USD/JPY","-0.19%"),("AUD/USD","-0.32%"),
          ("GBP/USD","-0.05%"),("EUR/JPY","-0.41%"),("GBP/JPY","-0.24%")]'''
    if old_ticker not in v:
        raise SystemExit("ticker block missing")
    v = v.replace(old_ticker, new_ticker)
    with open(VERIFY, "w", encoding="utf-8", newline="\n") as f:
        f.write(v)
    print("verify constants patched")

if __name__ == "__main__":
    main()
