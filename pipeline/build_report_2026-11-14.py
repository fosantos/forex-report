#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""14/11/2026 edition, on the Friday 13/11 ECB fixing.

EUR/USD 1.1052 and AUD/USD 0.6785 extend the 9-month lows. USD/JPY fixes at
160.00 the day Katayama calls the move one-sided. MoF jawboning on 12-13/11
reopens the 2.5-sigma20 floor on the yen pairs. No ticket clears the gate.
"""
import json
from datetime import datetime, timezone

INDEX = r"C:/Projetos/forex-report/docs/index.html"
LEDGER = r"C:/Projetos/forex-report/docs/track-record.json"
NEWS = r"C:/Projetos/forex-report/docs/news.html"
SITEMAP = r"C:/Projetos/forex-report/docs/sitemap.xml"
VERIFY = r"C:/Projetos/forex-report/pipeline/verify_all.py"

TS = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
OLD_TS = "12/11/2026 23:20 UTC"
BASIS = "585 sessions, 01/08/2024 to 13/11/2026"
BASIS_PT = "585 pregões, 01/08/2024 a 13/11/2026"

def pair(quote, bias, bias_type, pt, en):
    return {"quote": quote, "bias": bias, "biasType": bias_type, "pt": pt, "en": en}

EUR = pair("1.1052", "BAIXA", "bear",
    pt={
        "fundamental": "O EUR/USD fechou em 1,1052 na sessão de sexta 13/11/2026 (taxa de referência BCE/Frankfurter; o terminal MT5 está logado, mas o Market Watch não tem os pares à vista), caindo -0,26% (-29 pips) a partir de 1,1081. É mais um fechamento na mínima de 9 meses e de 10/20 pregões. O PPI americano de outubro saiu a +0,3% no mês (esperado +0,4%; setembro revisado para +1,4%) e +6,5% no ano, a maior leitura anual desde novembro de 2022 (BLS, 13/11). O Fed segue em 3,75-4,00%, com a decisão de 8-9/12 ainda no debate de 25 ou 50 pb. Até o redondo 1.1000 são 52 pips. O piso de 1,5σ20 é de 61 pips, então um 1:2 que pare antes de 1.1000 exigiria um stop de no máximo 26 pips. Um stop sobre 1.1130 (~78 pips) joga o alvo através de 1.1000, 1.0950 e 1.0900. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (1,1528) com a SMA50 (1,1301) abaixo dela — alinhamento de baixa pleno. O próprio fechamento é a mínima de 10/20 pregões e de 9 meses. A máxima de 10/20 pregões segue 1.1267 (04/11).",
        "support": "1.1000 (o redondo, 52 pips abaixo). O fechamento de 13/11 (1,1052) é a mínima de 9 meses.",
        "resistance": "1.1081 (a mínima de quinta, devolvida) e 1.1130 (a mínima antiga), com a máxima de 10/20 pregões em 1.1267 e a SMA50 em 1,1301.",
        "priceAction": "A extensão de sexta encurtou o ar até 1.1000 para 52 pips, abaixo do piso de 61. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "1.1000 está mais perto do que o piso permite. O stop que cobre 61 pips coloca o redondo no meio do caminho até o 1:2. Sem gatilho novo.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O dólar ganhou mais 29 pips e o livro continua sem comprar a mínima. O espaço até 1.1000 não paga o piso, e o stop que paga o piso atravessa o redondo."
    },
    en={
        "fundamental": "EUR/USD closed at 1.1052 in the Friday 13/11/2026 session (ECB/Frankfurter reference rate; the MT5 terminal is logged in, but Market Watch has no spot pairs), down -0.26% (-29 pips) from 1.1081. It is another close at the 9-month and 10/20-day low. US October PPI printed +0.3% on the month (expected +0.4%; September revised to +1.4%) and +6.5% on the year, the largest annual gain since November 2022 (BLS, Nov 13). The Fed is still at 3.75-4.00%, with the Dec 8-9 decision still a 25-or-50 bp debate. The 1.1000 round is 52 pips away. The 1.5-sigma20 floor is 61 pips, so a 1:2 that stops before 1.1000 would need a stop of 26 pips at most. A stop over 1.1130 (~78 pips) puts the target through 1.1000, 1.0950 and 1.0900. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (1.1528) with the 50-day (1.1301) below it — full bear alignment. Today's close is the 10/20-day and 9-month low. The 10/20-day high is still 1.1267 (Nov 4).",
        "support": "1.1000 (the round, 52 pips below). The Nov-13 close (1.1052) is the 9-month low.",
        "resistance": "1.1081 (Thursday's low, handed back) and 1.1130 (the prior low), with the 10/20-day high at 1.1267 and the SMA50 at 1.1301.",
        "priceAction": "Friday's extension cut the air down to 1.1000 to 52 pips, inside the 61-pip floor. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "1.1000 is closer than the floor allows. The stop that clears 61 pips puts the round in the middle of the path to the 1:2. No new trigger.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The dollar took another 29 pips and the book still does not buy the low. The room to 1.1000 does not pay the floor, and the stop that pays the floor runs through the round."
    })

USDJPY = pair("160.00", "NEUTRO", "neutral",
    pt={
        "fundamental": "O USD/JPY fechou em 160,00 na sessão de sexta 13/11/2026 (taxa de referência BCE/Frankfurter), subindo +0,19% (+30 pips). O fechamento é a máxima de 10 e de 20 pregões, cravado no redondo. No spot o iene passou de 160 na sexta e a ministra das Finanças Satsuki Katayama chamou o movimento de unilateral e rápido, dizendo que Tóquio responderia (Reuters, 13/11). Na véspera, Atsushi Mimura tinha dito que ainda era cedo para esquecer a intervenção do verão. Jawboning oficial dentro de 30 dias: o piso dos pares com iene volta a 2,5σ20, aqui 119 pips. O mapa segue misto — fechamento acima da SMA200 (158,69), SMA50 (157,39) ainda abaixo. Um stop sob a SMA200 cabe nos 119 pips, e o 1:2 atravessa 161,00 e 162,00, com a máxima de 9 meses em 163,91. Comprar o nível que o MoF acabou de marcar não é um ticket. O BoJ segue em 1,25%. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento acima da SMA200 (158,69), com a SMA50 (157,39) ainda abaixo — alinhamento misto. A máxima de 9 meses segue 163,91.",
        "support": "158.69 (a SMA200, 131 pips abaixo) e 159.70 (a máxima de quinta), com a SMA50 em 157,39.",
        "resistance": "160.00 (máxima de 10/20 pregões, o próprio fechamento) e 161.00, com a máxima de 9 meses em 163,91.",
        "priceAction": "O rompimento do canal parou no redondo que o MoF avisou. O piso agora é 119 pips. O 1:2 para cima cruza dois redondos. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "160.00 é o fechamento e o aviso. Um long com stop sob a SMA200 cabe no piso de 119 pips e esbarra em 161 e 162. Vender contra a máxima não tem alinhamento. Reavaliar se o MoF agir, ou depois do FOMC de 8-9/12.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O iene entregou o redondo no mesmo dia em que Katayama prometeu resposta. O piso subiu para 2,5σ20 e o caminho de 1:2 fica ocupado por 161 e 162. A mesa não compra 160."
    },
    en={
        "fundamental": "USD/JPY closed at 160.00 in the Friday 13/11/2026 session (ECB/Frankfurter reference rate), up +0.19% (+30 pips). The close is the 10-day and 20-day high, pinned on the round. In the spot market the yen went through 160 on Friday and Finance Minister Satsuki Katayama called the move one-sided and rapid, saying Tokyo would respond (Reuters, Nov 13). The day before, Atsushi Mimura said it was still too early to forget the summer intervention. Official jawboning inside 30 days: the yen pairs' floor returns to 2.5-sigma20, here 119 pips. The map stays mixed — close above the SMA200 (158.69), the SMA50 (157.39) still below. A stop under the SMA200 fits the 119-pip floor, and the 1:2 crosses 161.00 and 162.00, with the 9-month high at 163.91. Buying the level the MoF just marked is not a ticket. The BoJ is still at 1.25%. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close above the SMA200 (158.69), with the SMA50 (157.39) still below — mixed alignment. The 9-month high remains 163.91.",
        "support": "158.69 (the SMA200, 131 pips below) and 159.70 (Thursday's high), with the SMA50 at 157.39.",
        "resistance": "160.00 (the 10/20-day high, today's close) and 161.00, with the 9-month high at 163.91.",
        "priceAction": "The channel break stopped on the round the MoF flagged. The floor is now 119 pips. The 1:2 higher crosses two rounds. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "160.00 is both the close and the warning. A long with a stop under the SMA200 fits the 119-pip floor and runs into 161 and 162. A short against the high has no alignment. Reassess if the MoF acts, or after the Dec 8-9 FOMC.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The yen delivered the round on the same day Katayama promised a response. The floor is back at 2.5-sigma20 and the 1:2 path is occupied by 161 and 162. The desk does not buy 160."
    })

AUD = pair("0.6785", "BAIXA", "bear",
    pt={
        "fundamental": "O AUD/USD fechou em 0,6785 na sessão de sexta 13/11/2026 (taxa de referência BCE/Frankfurter), caindo -0,52% (-36 pips). O fechamento atravessou o redondo 0.6800 que bloqueava o 1:2 na quinta e é a nova mínima de 9 meses e de 10/20 pregões. A SMA50 (0,7017) está sob a SMA200 (0,7053). O piso de 1,5σ20 é de 55 pips. Até 0.6700 são 85 pips: um 1:2 contra o piso (110 pips, alvo ~0,6675) tem de atravessar esse redondo. Um stop sobre 0.6821 fica a 36 pips e não paga o piso. O RBA está em 4,85%. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (0,7053) com a SMA50 (0,7017) abaixo dela — alinhamento de baixa. O próprio fechamento é a mínima de 10/20 pregões e de 9 meses. A máxima de 10 pregões está em 0.7015.",
        "support": "0.6700 (o próximo redondo, 85 pips abaixo). O fechamento de 13/11 (0,6785) é a mínima de 9 meses.",
        "resistance": "0.6821 (a mínima de quinta, devolvida) e 0.6860 (a mínima antiga), com a máxima de 10 pregões em 0.7015.",
        "priceAction": "0.6800 cedeu e o próximo redondo não paga 1:2 contra o piso de 55 pips. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "O fechamento sob 0.6800 saiu. 85 pips até 0.6700 são menos que os 110 de um 1:2 no piso. Sem gatilho novo.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O Aussie fez o que a quinta pedia — perdeu 0.6800 — e o livro continua de fora. O alvo que respeita o piso cai do outro lado de 0.6700."
    },
    en={
        "fundamental": "AUD/USD closed at 0.6785 in the Friday 13/11/2026 session (ECB/Frankfurter reference rate), down -0.52% (-36 pips). The close went through the 0.6800 round that blocked the 1:2 on Thursday and is the new 9-month and 10/20-day low. The SMA50 (0.7017) sits under the SMA200 (0.7053). The 1.5-sigma20 floor is 55 pips. 0.6700 is 85 pips away: a 1:2 against the floor (110 pips, target ~0.6675) has to cross that round. A stop over 0.6821 is 36 pips and misses the floor. The RBA cash rate is 4.85%. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (0.7053) with the SMA50 (0.7017) below it — bear alignment. Today's close is the 10/20-day and 9-month low. The 10-day high is 0.7015.",
        "support": "0.6700 (the next round, 85 pips below). The Nov-13 close (0.6785) is the 9-month low.",
        "resistance": "0.6821 (Thursday's low, handed back) and 0.6860 (the prior low), with the 10-day high at 0.7015.",
        "priceAction": "0.6800 gave way and the next round does not pay 1:2 against the 55-pip floor. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The close under 0.6800 has printed. 85 pips down to 0.6700 is less than the 110 of a 1:2 on the floor. No new trigger.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The Aussie did what Thursday asked — it lost 0.6800 — and the book stays out. The target that respects the floor lands on the other side of 0.6700."
    })

GBP = pair("1.3227", "BAIXA", "bear",
    pt={
        "fundamental": "O GBP/USD fechou em 1,3227 na sessão de sexta 13/11/2026 (taxa de referência BCE/Frankfurter), caindo -0,22% (-29 pips). É a nova mínima de 10/20 pregões. A mínima de 9 meses segue 1.3160, a 66 pips. O piso de 1,5σ20 é de 74 pips, então o alvo não cabe antes dessa mínima. Um stop sobre 1.3256 fica a 29 pips e não paga o piso. O stop no piso atravessa 1.3200 e 1.3160. A Bank Rate está em 4,00%. O PPI americano de sexta não segurou o cabo. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (1,3418) e sob a SMA50 (1,3347), com a SMA50 abaixo da SMA200 — alinhamento de baixa. A máxima de 10/20 pregões segue 1.3500 (04/11).",
        "support": "1.3160 (mínima de 9 meses, 66 pips abaixo), com o redondo 1.3200 no meio. O fechamento de 13/11 é a mínima de 10/20 pregões.",
        "resistance": "1.3256 (a mínima de quinta, devolvida) e 1.3347 (a SMA50), com a SMA200 em 1,3418.",
        "priceAction": "Nova mínima da janela, 66 pips acima do extremo de 9 meses e com piso de 74. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "O fechamento sob 1,3256 saiu. O espaço até 1.3160 é menor que o piso. Sem gatilho novo.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "A libra fez outra mínima e parou antes do extremo que importa. Vender aqui coloca 1.3160 dentro do stop ou no meio do alvo."
    },
    en={
        "fundamental": "GBP/USD closed at 1.3227 in the Friday 13/11/2026 session (ECB/Frankfurter reference rate), down -0.22% (-29 pips). It is the new 10/20-day low. The 9-month low is still 1.3160, 66 pips away. The 1.5-sigma20 floor is 74 pips, so the target does not fit before that low. A stop over 1.3256 is 29 pips and misses the floor. The floor stop crosses 1.3200 and 1.3160. Bank Rate is 4.00%. Friday's US PPI did not hold cable. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (1.3418) and under the SMA50 (1.3347), with the SMA50 below the SMA200 — bear alignment. The 10/20-day high is still 1.3500 (Nov 4).",
        "support": "1.3160 (the 9-month low, 66 pips below), with the 1.3200 round in between. The Nov-13 close is the 10/20-day low.",
        "resistance": "1.3256 (Thursday's low, handed back) and 1.3347 (the SMA50), with the SMA200 at 1.3418.",
        "priceAction": "A new window low, 66 pips above the 9-month extreme and with a 74-pip floor. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The close under 1.3256 has printed. The room down to 1.3160 is smaller than the floor. No new trigger.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "Sterling made another low and stopped short of the extreme that matters. Selling here puts 1.3160 inside the stop or in the middle of the target."
    })

EURJPY = pair("176.83", "BAIXA", "bear",
    pt={
        "fundamental": "O EUR/JPY fechou em 176,83 na sessão de sexta 13/11/2026 (taxa de referência BCE/Frankfurter), caindo -0,07% (-13 pips). A mínima de 10 pregões segue 176,77 (06/11), 6 pips abaixo, e a de 9 meses / 20 pregões segue 175,51. O aviso do MoF de 12-13/11 recoloca o piso em 2,5σ20: 167 pips. Uma venda sob 176,77 com stop que respeite 167 pips (~178,50, acima da máxima de 10 pregões 178,30) joga o 1:2 através de 175,51 e de 175,00, para dentro do cluster de 2025. Alinhamento de baixa (fechamento sob a SMA200 182,93 e a SMA50 177,84). Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (182,93) com a SMA50 (177,84) abaixo dela — alinhamento de baixa pleno. A máxima de 10/20 pregões está em 178,30 (04/11).",
        "support": "176.77 (mínima de 10 pregões, 06/11) e 175.51 (mínima de 9 meses e de 20 pregões, 23/10).",
        "resistance": "177.84 (a SMA50) e 178.30 (máxima de 10/20 pregões, 04/11).",
        "priceAction": "Quase parado, 6 pips acima da mínima de 10 pregões. O piso novo de 167 pips empurra o alvo para 2025. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "O fechamento sob 176,77 ainda não saiu. Mesmo que saia, o stop de 167 pips coloca 175,51 e 175,00 no caminho. Reavaliar se o MoF agir.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O euro fez mínima contra o dólar e não contra o iene. Com o piso de volta a 2,5σ20, o cruzado fica ainda mais longe de um 1:2 limpo."
    },
    en={
        "fundamental": "EUR/JPY closed at 176.83 in the Friday 13/11/2026 session (ECB/Frankfurter reference rate), down -0.07% (-13 pips). The 10-day low is still 176.77 (Nov 6), 6 pips below, and the 9-month / 20-day low is still 175.51. The MoF warning of Nov 12-13 puts the floor back at 2.5-sigma20: 167 pips. A short under 176.77 with a stop that respects 167 pips (~178.50, above the 10-day high 178.30) puts the 1:2 through 175.51 and 175.00, into the 2025 cluster. Bear alignment (close under the SMA200 182.93 and the SMA50 177.84). Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (182.93) with the SMA50 (177.84) below it — full bear alignment. The 10/20-day high is 178.30 (Nov 4).",
        "support": "176.77 (the 10-day low, Nov 6) and 175.51 (the 9-month and 20-day low, Oct 23).",
        "resistance": "177.84 (the SMA50) and 178.30 (the 10/20-day high, Nov 4).",
        "priceAction": "Almost unchanged, 6 pips above the 10-day low. The new 167-pip floor pushes the target into 2025. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The close under 176.77 has not printed. Even if it does, the 167-pip stop puts 175.51 and 175.00 in the path. Reassess if the MoF acts.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The euro made a low against the dollar and not against the yen. With the floor back at 2.5-sigma20, the cross is further from a clean 1:2."
    })

GBPJPY = pair("211.63", "BAIXA", "bear",
    pt={
        "fundamental": "O GBP/JPY fechou em 211,63 na sessão de sexta 13/11/2026 (taxa de referência BCE/Frankfurter), caindo -0,03% (-7 pips). O fechamento é a nova mínima de 10 pregões. A mínima de 20 pregões segue 209,61 e a de 9 meses 207,32. A SMA200 está 129 pips acima (212,92). O piso, reaberto pelo jawboning do MoF, é de 177 pips — a SMA200 não cobre. O stop que cobre (sobre a máxima de 10 pregões 213,63, ~200 pips) joga o 1:2 através de 210,00, 209,61 e 208,00. Alinhamento de baixa (fechamento sob a SMA200, SMA50 210,05 abaixo dela). BoE em 4,00%, BoJ em 1,25%. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (212,92) com a SMA50 (210,05) abaixo dela — alinhamento de baixa. A máxima de 10/20 pregões está em 213,63 (04/11).",
        "support": "209.61 (mínima de 20 pregões, 23/10) e 207.32 (mínima de 9 meses). O fechamento de 13/11 é a mínima de 10 pregões.",
        "resistance": "212.92 (a SMA200, 129 pips acima) e 213.63 (máxima de 10/20 pregões). A SMA50 está em 210,05, abaixo do preço.",
        "priceAction": "Mínima de 10 pregões por 7 pips. O piso de 177 pips é mais largo que a distância até a SMA200. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "Vender a perda de 211,63 com stop sobre 212,92 não paga o piso de 177 pips. O stop que paga atravessa 209,61. Sem gatilho limpo.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O cruzado quase não andou, e o piso mudou. 129 pips até a SMA200 ficaram curtos diante de 177. A mesa espera o MoF ou um caminho mais largo."
    },
    en={
        "fundamental": "GBP/JPY closed at 211.63 in the Friday 13/11/2026 session (ECB/Frankfurter reference rate), down -0.03% (-7 pips). The close is the new 10-day low. The 20-day low is still 209.61 and the 9-month low is 207.32. The SMA200 is 129 pips above (212.92). The floor, reopened by the MoF jawboning, is 177 pips — the SMA200 does not cover it. The stop that does (over the 10-day high 213.63, ~200 pips) puts the 1:2 through 210.00, 209.61 and 208.00. Bear alignment (close under the SMA200, SMA50 210.05 below it). BoE at 4.00%, BoJ at 1.25%. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (212.92) with the SMA50 (210.05) below it — bear alignment. The 10/20-day high is 213.63 (Nov 4).",
        "support": "209.61 (the 20-day low, Oct 23) and 207.32 (the 9-month low). The Nov-13 close is the 10-day low.",
        "resistance": "212.92 (the SMA200, 129 pips above) and 213.63 (the 10/20-day high). The SMA50 is at 210.05, under price.",
        "priceAction": "A 10-day low by 7 pips. The 177-pip floor is wider than the distance to the SMA200. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "Selling a loss of 211.63 with a stop over 212.92 misses the 177-pip floor. The stop that clears it crosses 209.61. No clean trigger.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The cross barely moved, and the floor changed. 129 pips up to the SMA200 came up short of 177. The desk waits for the MoF or a wider path."
    })

DATA = {
    "EUR/USD": EUR, "USD/JPY": USDJPY, "AUD/USD": AUD,
    "GBP/USD": GBP, "EUR/JPY": EURJPY, "GBP/JPY": GBPJPY,
}
DRIVERS = {
    "EUR/USD": {
        "en": ["Another close at the 9-month low", "52 pips to 1.1000, floor is 61", "PPI 6.5% y/y, Fed still 3.75-4.00%"],
        "pt": ["Outro fechamento na mín. de 9 meses", "52 pips até 1.1000, piso é 61", "PPI 6,5% a/a, Fed ainda 3,75-4,00%"],
    },
    "USD/JPY": {
        "en": ["Fix at 160.00, Katayama warns", "Floor back to 2.5-sigma, 119 pips", "161 and 162 block the long"],
        "pt": ["Fixing em 160,00, Katayama avisa", "Piso de volta a 2,5σ, 119 pips", "161 e 162 bloqueiam a compra"],
    },
    "AUD/USD": {
        "en": ["Through 0.6800, new 9-month low", "85 pips to 0.6700, need 110", "RBA still 4.85%"],
        "pt": ["Através de 0.6800, nova mín. de 9m", "85 pips até 0.6700, precisa 110", "RBA ainda 4,85%"],
    },
    "GBP/USD": {
        "en": ["New 10/20-day low at 1.3227", "66 pips to the 9-month low, floor 74", "Bank Rate still 4.00%"],
        "pt": ["Nova mín. de 10/20 pregões em 1.3227", "66 pips até a mín. de 9m, piso 74", "Bank Rate ainda 4,00%"],
    },
    "EUR/JPY": {
        "en": ["6 pips above the 10-day low", "Floor now 167 pips", "2025 cluster still blocks"],
        "pt": ["6 pips acima da mín. de 10 pregões", "Piso agora 167 pips", "Cluster de 2025 ainda bloqueia"],
    },
    "GBP/JPY": {
        "en": ["New 10-day low by 7 pips", "SMA200 is 129 pips, floor is 177", "209.61 still in the path"],
        "pt": ["Nova mín. de 10 pregões por 7 pips", "SMA200 a 129 pips, piso é 177", "209.61 ainda no caminho"],
    },
}

NEWS_ITEM_JS = r'''                {
                    date: "13/11/2026",
                    category: "macro",
                    impact: "high",
                    pairs: ["EUR/USD", "USD/JPY", "AUD/USD", "GBP/USD", "EUR/JPY", "GBP/JPY"],
                    pt: {
                        headline: "O iene fixa em 160 e Katayama avisa — o piso dos cruzados volta a 2,5σ, e os seis seguem sem ticket",
                        summary: "A taxa BCE/Frankfurter de 13/11 estende o dólar e crava o redondo. USD/JPY fechou 160,00 (+0,19%). No spot o iene passou de 160 e a ministra Satsuki Katayama chamou o movimento de unilateral e rápido (Reuters, 13/11), um dia depois de Mimura lembrar a intervenção do verão. O piso dos pares com iene volta a 2,5σ20: 119 pips no USD/JPY, 167 no EUR/JPY, 177 no GBP/JPY. O 1:2 do USD/JPY atravessa 161 e 162. EUR/USD fechou 1,1052 (−0,26%), a 52 pips de 1.1000, com piso de 61. AUD/USD fechou 0,6785 (−0,52%), através de 0.6800, com 0.6700 a 85 pips e um 1:2 pedindo 110. GBP/USD 1,3227 (−0,22%) ficou a 66 pips da mínima de 9 meses 1.3160, piso de 74. EUR/JPY 176,83 e GBP/JPY 211,63 sem caminho. O PPI de outubro saiu a +0,3% no mês (esperado +0,4%) e +6,5% no ano (BLS). Os seis ficam em AGUARDAR. FOMC em 8-9/12.",
                        take: "160 chegou junto com o aviso. O livro não compra o redondo que o MoF marcou, e não vende as mínimas do dólar com o próximo redondo dentro do piso. A mesa segue vazia."
                    },
                    en: {
                        headline: "The yen fixes at 160 and Katayama warns — the crosses' floor returns to 2.5-sigma, and all six stay without a ticket",
                        summary: "The 13/11 ECB/Frankfurter fixing extends the dollar and pins the round. USD/JPY closed 160.00 (+0.19%). In the spot market the yen went through 160 and Finance Minister Satsuki Katayama called the move one-sided and rapid (Reuters, Nov 13), a day after Mimura recalled the summer intervention. The yen pairs' floor returns to 2.5-sigma20: 119 pips on USD/JPY, 167 on EUR/JPY, 177 on GBP/JPY. The USD/JPY 1:2 crosses 161 and 162. EUR/USD closed 1.1052 (−0.26%), 52 pips from 1.1000, with a 61-pip floor. AUD/USD closed 0.6785 (−0.52%), through 0.6800, with 0.6700 85 pips away and a 1:2 asking for 110. GBP/USD 1.3227 (−0.22%) finished 66 pips from the 9-month low 1.3160, floor 74. EUR/JPY 176.83 and GBP/JPY 211.63 have no path. October PPI printed +0.3% on the month (expected +0.4%) and +6.5% on the year (BLS). All six stay on WAIT. FOMC on Dec 8-9.",
                        take: "160 arrived with the warning. The book does not buy the round the MoF marked, and it does not sell the dollar lows with the next round inside the floor. The desk stays empty."
                    }
                },
'''

NEWS_CARD = r'''                <!-- News 13/11/2026: yen fixes at 160, Katayama warns, 2.5-sigma floor returns; all six WAIT -->
                <article class="news-card">
                    <div class="news-card-top">
                        <span class="news-cat"><span class="lang-en">Macro Data</span><span class="lang-pt" style="display:none;">Dados Macro</span></span>
                        <span class="impact-badge high"><span class="lang-en">High Impact</span><span class="lang-pt" style="display:none;">Impacto Alto</span></span>
                        <span class="news-date">13/11/2026</span>
                    </div>
                    <h2 class="news-title">
                        <span class="lang-en">The yen fixes at 160 and Katayama warns — the crosses' floor returns to 2.5-sigma, and all six stay without a ticket</span>
                        <span class="lang-pt" style="display:none;">O iene fixa em 160 e Katayama avisa — o piso dos cruzados volta a 2,5σ, e os seis seguem sem ticket</span>
                    </h2>
                    <p class="news-summary">
                        <span class="lang-en">The 13/11 ECB/Frankfurter fixing extends the dollar and pins the round. USD/JPY closed 160.00 (+0.19%). In the spot market the yen went through 160 and Finance Minister Satsuki Katayama called the move one-sided and rapid (Reuters, Nov 13), a day after Mimura recalled the summer intervention. The yen pairs' floor returns to 2.5-sigma20: 119 pips on USD/JPY, 167 on EUR/JPY, 177 on GBP/JPY. The USD/JPY 1:2 crosses 161 and 162. EUR/USD closed 1.1052 (−0.26%), 52 pips from 1.1000, with a 61-pip floor. AUD/USD closed 0.6785 (−0.52%), through 0.6800, with 0.6700 85 pips away and a 1:2 asking for 110. GBP/USD 1.3227 (−0.22%) finished 66 pips from the 9-month low 1.3160, floor 74. EUR/JPY 176.83 and GBP/JPY 211.63 have no path. October PPI printed +0.3% on the month (expected +0.4%) and +6.5% on the year (BLS). All six stay on WAIT. FOMC on Dec 8-9.</span>
                        <span class="lang-pt" style="display:none;">A taxa BCE/Frankfurter de 13/11 estende o dólar e crava o redondo. USD/JPY fechou 160,00 (+0,19%). No spot o iene passou de 160 e a ministra Satsuki Katayama chamou o movimento de unilateral e rápido (Reuters, 13/11), um dia depois de Mimura lembrar a intervenção do verão. O piso dos pares com iene volta a 2,5σ20: 119 pips no USD/JPY, 167 no EUR/JPY, 177 no GBP/JPY. O 1:2 do USD/JPY atravessa 161 e 162. EUR/USD fechou 1,1052 (−0,26%), a 52 pips de 1.1000, com piso de 61. AUD/USD fechou 0,6785 (−0,52%), através de 0.6800, com 0.6700 a 85 pips e um 1:2 pedindo 110. GBP/USD 1,3227 (−0,22%) ficou a 66 pips da mínima de 9 meses 1.3160, piso de 74. EUR/JPY 176,83 e GBP/JPY 211,63 sem caminho. O PPI de outubro saiu a +0,3% no mês (esperado +0,4%) e +6,5% no ano (BLS). Os seis ficam em AGUARDAR. FOMC em 8-9/12.</span>
                    </p>
                    <div class="news-take">
                        <span class="take-tag"><span class="lang-en">Desk take</span><span class="lang-pt" style="display:none;">Leitura da mesa</span></span>
                        <span class="lang-en">160 arrived with the warning. The book does not buy the round the MoF marked, and it does not sell the dollar lows with the next round inside the floor. The desk stays empty.</span>
                        <span class="lang-pt" style="display:none;">160 chegou junto com o aviso. O livro não compra o redondo que o MoF marcou, e não vende as mínimas do dólar com o próximo redondo dentro do piso. A mesa segue vazia.</span>
                    </div>
                    <div class="news-pairs">
                        <span class="np-label"><span class="lang-en">Watch</span><span class="lang-pt" style="display:none;">Acompanhar</span></span>
                        <a href="eur-usd.html" class="pair-link-chip">EUR/USD</a><a href="usd-jpy.html" class="pair-link-chip">USD/JPY</a><a href="aud-usd.html" class="pair-link-chip">AUD/USD</a><a href="gbp-usd.html" class="pair-link-chip">GBP/USD</a><a href="eur-jpy.html" class="pair-link-chip">EUR/JPY</a><a href="gbp-jpy.html" class="pair-link-chip">GBP/JPY</a>
                    </div>
                </article>

'''

NEW_CAL = '''                <div class="cal-cell">
                    <span class="cal-date">13/11</span>
                    <span class="cal-event"><span class="lang-en">US PPI +0.3% m/m, +6.5% y/y</span><span class="lang-pt" style="display:none;">PPI dos EUA +0,3% m/m, +6,5% a/a</span></span>
                    <div class="cal-meta"><span class="cal-impact high" aria-hidden="true"></span><span class="cal-cur">USD</span></div>
                </div>
                <div class="cal-cell">
                    <span class="cal-date">13/11</span>
                    <span class="cal-event"><span class="lang-en">MoF: yen at 160, Katayama vows action</span><span class="lang-pt" style="display:none;">MoF: iene em 160, Katayama promete ação</span></span>
                    <div class="cal-meta"><span class="cal-impact high" aria-hidden="true"></span><span class="cal-cur">JPY</span></div>
                </div>
                <div class="cal-cell">
                    <span class="cal-date">12/11</span>
                    <span class="cal-event"><span class="lang-en">UK GDP +0.7% q/q, in line (ONS)</span><span class="lang-pt" style="display:none;">PIB do Reino Unido +0,7% t/t, em linha (ONS)</span></span>
                    <div class="cal-meta"><span class="cal-impact med" aria-hidden="true"></span><span class="cal-cur">GBP</span></div>
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
        "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 570 daily sessions (01/08/2024–23/10/2026).",
        "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 585 daily sessions (01/08/2024–13/11/2026).")
    idx = idx.replace(
        "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, σ20 e Donchian calculados · 570 pregões (01/08/2024 a 23/10/2026).",
        "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, σ20 e Donchian calculados · 585 pregões (01/08/2024 a 13/11/2026).")
    idx = idx.replace(
        'nextEvent: "FOMC Oct 28 · ECB Oct 29 · BoJ Oct 30"',
        'nextEvent: "PPI 6.5% y/y · MoF at 160 · FOMC Dec 8-9"')
    idx = idx.replace(
        'nextEvent: "FOMC 28/10 · BCE 29/10 · BoJ 30/10"',
        'nextEvent: "PPI 6,5% a/a · MoF em 160 · FOMC 8-9/12"')

    start = idx.find("        const forexData = {")
    end = idx.find("        /* ==========================================\n           B. Market metadata")
    if start < 0 or end < 0:
        raise SystemExit("forexData markers missing")
    idx = idx[:start] + "        const forexData = " + json.dumps(DATA, ensure_ascii=False, indent=4) + ";\n\n" + idx[end:]

    d0 = idx.find("        const dailyChanges = {")
    d1 = idx.find("        const macroDrivers = {")
    changes = {
        "EUR/USD": "-0.26%", "USD/JPY": "+0.19%", "AUD/USD": "-0.52%",
        "GBP/USD": "-0.22%", "EUR/JPY": "-0.07%", "GBP/JPY": "-0.03%",
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
    ledger["meta"]["lastUpdated"] = "13/11/2026"
    with open(LEDGER, "w", encoding="utf-8", newline="\n") as f:
        json.dump(ledger, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("ledger lastUpdated only; book still empty")

    with open(NEWS, encoding="utf-8") as f:
        news = f.read()
    news = news.replace(
        "Market Wire · Second Close, Still No Ticket",
        "Market Wire · 160 and a Warning, Still No Ticket")
    news = news.replace(
        "Telégrafo da Mesa · Segundo Fechamento, Ainda Sem Ticket",
        "Telégrafo da Mesa · 160 e um Aviso, Ainda Sem Ticket")
    news = news.replace(OLD_TS, TS)
    news = news.replace(
        "6 pairs · FOMC Wed 28 · ECB Thu 29 · BoJ Fri 30",
        "6 pairs · MoF at 160 · FOMC Dec 8-9")
    news = news.replace(
        "6 pares · FOMC qua 28 · BCE qui 29 · BoJ sex 30",
        "6 pares · MoF em 160 · FOMC 8-9/12")
    start = news.find('                <div class="cal-cell">')
    end = news.find("            </div>\n        </section>", start)
    if start < 0 or end < 0:
        raise SystemExit("calendar block missing")
    news = news[:start] + NEW_CAL + "\n" + news[end:]
    marker = "                <!-- News 12/11/2026:"
    if marker not in news:
        raise SystemExit("news marker missing")
    news = news.replace(marker, NEWS_CARD + marker, 1)
    with open(NEWS, "w", encoding="utf-8", newline="\n") as f:
        f.write(news)
    print("news.html patched")

    with open(SITEMAP, encoding="utf-8") as f:
        sm = f.read()
    n = sm.count("2026-11-12")
    if n != 9:
        raise SystemExit("expected 9 sitemap dates, found %d" % n)
    sm = sm.replace("2026-11-12", "2026-11-14")
    with open(SITEMAP, "w", encoding="utf-8", newline="\n") as f:
        f.write(sm)
    print("sitemap patched")

    with open(VERIFY, encoding="utf-8") as f:
        v = f.read()
    v = v.replace('TODAY_TS = "12/11/2026 23:20 UTC"', 'TODAY_TS = "%s"' % TS)
    v = v.replace(
        'TODAY_DATE = "12/11/2026"  # basis session date (report edition: 12/11/2026)',
        'TODAY_DATE = "13/11/2026"  # basis session date (report edition: 13/11/2026)')
    old_ticker = '''TICKER = [("EUR/USD","-0.41%"),("USD/JPY","+0.30%"),("AUD/USD","-0.56%"),
          ("GBP/USD","-0.39%"),("EUR/JPY","-0.12%"),("GBP/JPY","-0.09%")]'''
    new_ticker = '''TICKER = [("EUR/USD","-0.26%"),("USD/JPY","+0.19%"),("AUD/USD","-0.52%"),
          ("GBP/USD","-0.22%"),("EUR/JPY","-0.07%"),("GBP/JPY","-0.03%")]'''
    if old_ticker not in v:
        raise SystemExit("ticker block missing")
    v = v.replace(old_ticker, new_ticker)
    with open(VERIFY, "w", encoding="utf-8", newline="\n") as f:
        f.write(v)
    print("verify constants patched")

if __name__ == "__main__":
    main()
