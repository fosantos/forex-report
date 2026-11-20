#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""20/11/2026 edition, on the Friday 20/11 ECB fixing (covers Thu 19/11 + Fri 20/11).

The yen rallies 133 pips on Japan's October CPI (headline 2.3%, core 2.2%,
core-core 2.2% — all a touch soft, all above 2%) and USD/JPY closes through
the SMA200, flipping the map from mixed to bear. AUD/USD (-46 pips on the
Australian jobs miss: -43.5k, jobless 4.9%), GBP/USD (-27 pips despite UK
retail +0.7%) and EUR/JPY (-149 pips) print new 9-month lows; GBP/JPY prints
a new 10/20-day low 30 pips above the 9-month low; EUR/USD holds above 1.0968
with the dollar at a 19-month high. No ticket clears the gate.
"""
import json
import os
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(BASE, "..", "docs", "index.html")
LEDGER = os.path.join(BASE, "..", "docs", "track-record.json")
NEWS = os.path.join(BASE, "..", "docs", "news.html")
SITEMAP = os.path.join(BASE, "..", "docs", "sitemap.xml")
VERIFY = os.path.join(BASE, "verify_all.py")

TS = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
OLD_TS = "18/11/2026 20:09 UTC"
BASIS = "590 sessions, 01/08/2024 to 20/11/2026"
BASIS_PT = "590 pregões, 01/08/2024 a 20/11/2026"

def pair(quote, bias, bias_type, pt, en):
    return {"quote": quote, "bias": bias, "biasType": bias_type, "pt": pt, "en": en}

EUR = pair("1.0990", "BAIXA", "bear",
    pt={
        "fundamental": "O EUR/USD fechou em 1,0990 na sessão de sexta 20/11/2026 (taxa de referência BCE/Frankfurter), caindo -0,02% (-2 pips) a partir de 1,0992. Depois da ata hawkish de quarta e com o dólar em máxima de 19 meses (≈103,9 no DXY), o euro se recusou a estender: segurou acima da mínima de 9 meses de 1,0968 (18/11), a 22 pips. Até 1.0950 são 40 pips. O piso de 1,5σ20 é de 61 pips, então o stop que paga o piso já atravessa 1,0968 e cai perto de 1.0950. Um stop sobre 1,1000 fica a 10 pips. O Fed segue em 3,75-4,00%, com nova alta como caso-base para 8-9/12. O BCE decide em 17/12, com o depósito em 2,50%. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (1,1507) com a SMA50 (1,1238) abaixo dela — alinhamento de baixa pleno. A mínima de 10/20 pregões e de 9 meses segue 1,0968 (18/11). A máxima de 10 pregões é 1,1214 (10/11). A de 20 pregões segue 1,1267 (04/11).",
        "support": "1,0968 (mínima de 9 meses, 22 pips abaixo) e 1.0950 (40 pips).",
        "resistance": "1,0992 (a mínima de quinta, devolvida) e 1.1000, com a SMA50 em 1,1238.",
        "priceAction": "Dois pips de queda depois da ata. 1,0968 segue 22 pips abaixo, dentro do piso de 61. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "O fechamento sob 1,1000 saiu na quinta e se repetiu. O espaço até 1,0968 é menor que o piso, e o stop legal já atravessa 1,0950. Sem gatilho novo.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O euro segurou acima da mínima mesmo com o dólar em máxima de 19 meses. Vender aqui coloca 1,0968 e 1,0950 dentro do stop."
    },
    en={
        "fundamental": "EUR/USD closed at 1.0990 in the Friday 20/11/2026 session (ECB/Frankfurter reference rate), down -0.02% (-2 pips) from 1.0992. After Wednesday's hawkish minutes and with the dollar at a 19-month high (≈103.9 on the DXY), the euro refused to extend: it held above the 9-month low of 1.0968 (Nov 18), 22 pips away. 1.0950 is 40 pips away. The 1.5-sigma20 floor is 61 pips, so the stop that meets the floor is already through 1.0968 and lands near 1.0950. A stop over 1.1000 is 10 pips. The Fed is still at 3.75-4.00%, with a further hike as the base case for Dec 8-9. The ECB decides on Dec 17, with the deposit rate at 2.50%. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (1.1507) with the SMA50 (1.1238) below it — full bear alignment. The 10/20-day and 9-month low is still 1.0968 (Nov 18). The 10-day high is 1.1214 (Nov 10). The 20-day high is still 1.1267 (Nov 4).",
        "support": "1.0968 (the 9-month low, 22 pips below) and 1.0950 (40 pips).",
        "resistance": "1.0992 (Thursday's low, handed back) and 1.1000, with the SMA50 at 1.1238.",
        "priceAction": "Two pips down after the minutes. 1.0968 is still 22 pips below, inside the 61-pip floor. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The close under 1.1000 printed on Thursday and repeated. The room down to 1.0968 is smaller than the floor, and the legal stop is already through 1.0950. No new trigger.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The euro held above the low even with the dollar at a 19-month high. Selling here puts 1.0968 and 1.0950 inside the stop."
    })

USDJPY = pair("158.64", "BAIXA", "bear",
    pt={
        "fundamental": "O USD/JPY fechou em 158,64 na sessão de sexta 20/11/2026 (taxa de referência BCE/Frankfurter), caindo -0,83% (-133 pips) a partir de 159,97. O CPI do Japão de outubro saiu às 23:30 UTC de quinta (08:30 de sexta em Tóquio): cheio 2,3% (esperado 2,5%, anterior 2,1%), núcleo 2,2% (esperado 2,3%, anterior 2,1%) e núcleo-núcleo 2,2% (esperado 2,3%, anterior 2,4%) — erro para baixo nas três medidas, mas acima de 2%, e a alta do BoJ em dezembro segue na mesa. O iene firmou e o fechamento atravessou a SMA200 (158,77) para baixo, 13 pips abaixo dela: o mapa, misto desde o aviso de Katayama, virou alinhamento de baixa. O aviso de 12-13/11 segue dentro de 30 dias, sem intervenção confirmada, então o piso segue em 2,5σ20: 136 pips. O BoJ está em 1,25% e decide em 17-18/12. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (158,77) com a SMA50 (157,92) abaixo dela — alinhamento de baixa, virado nesta sessão. A máxima de 10/20 pregões segue 160,00 (13/11). A mínima de 10 pregões é 157,95 (09/11); a de 20, 157,25 (30/10). A máxima de 9 meses segue 163,91.",
        "support": "157.95 (mínima de 10 pregões, 69 pips abaixo) e 157.25 (mínima de 20 pregões, 139 pips), com a SMA50 em 157,92.",
        "resistance": "158.77 (a SMA200, perdida por 13 pips) e 160.00 (máxima de 10/20 pregões).",
        "priceAction": "O CPI virou o mapa para baixa, mas 160,00 segue 136 pips acima — exatamente o piso. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "Não há rompimento impresso: 157,95 segue intacta. Vender 158,64 com stop sobre 160,00 paga o piso de 136 por 5 pips, e o alvo de 1 para 2 atravessa 157,95 e 157,25. Sem gatilho limpo. Reavaliar num fechamento sob 157,95, ou depois do BoJ de 17-18/12.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O iene reagiu ao CPI e o alinhamento virou. Mas o caminho do short passa por dentro das mínimas de 10 e 20 pregões."
    },
    en={
        "fundamental": "USD/JPY closed at 158.64 in the Friday 20/11/2026 session (ECB/Frankfurter reference rate), down -0.83% (-133 pips) from 159.97. Japan's October CPI came out at 23:30 UTC on Thursday (08:30 Friday in Tokyo): headline 2.3% (2.5% expected, 2.1% prior), core 2.2% (2.3% expected, 2.1% prior) and core-core 2.2% (2.3% expected, 2.4% prior) — a miss on all three measures, but above 2%, and the December BoJ hike stays on the table. The yen firmed and the close crossed under the SMA200 (158.77), 13 pips below it: the map, mixed since Katayama's warning, flipped to bear alignment. The Nov 12-13 warning is still inside 30 days, with no confirmed intervention, so the floor stays at 2.5-sigma20: 136 pips. The BoJ is at 1.25% and decides on Dec 17-18. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (158.77) with the SMA50 (157.92) below it — bear alignment, flipped this session. The 10/20-day high is still 160.00 (Nov 13). The 10-day low is 157.95 (Nov 9); the 20-day low, 157.25 (Oct 30). The 9-month high is still 163.91.",
        "support": "157.95 (the 10-day low, 69 pips below) and 157.25 (the 20-day low, 139 pips), with the SMA50 at 157.92.",
        "resistance": "158.77 (the SMA200, lost by 13 pips) and 160.00 (the 10/20-day high).",
        "priceAction": "CPI flipped the map to bear, but 160.00 is still 136 pips above — exactly the floor. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "No breakdown has printed: 157.95 is still intact. Selling 158.64 with a stop over 160.00 clears the 136-pip floor by 5 pips, and the one-to-two target runs through 157.95 and 157.25. No clean trigger. Reassess on a close under 157.95, or after the Dec 17-18 BoJ.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The yen reacted to CPI and the alignment flipped. But the short's path runs inside the 10- and 20-day lows."
    })

AUD = pair("0.6666", "BAIXA", "bear",
    pt={
        "fundamental": "O AUD/USD fechou em 0,6666 na sessão de sexta 20/11/2026 (taxa de referência BCE/Frankfurter), caindo -0,68% (-46 pips) a partir de 0,6711. É a nova mínima de 10/20 pregões e de 9 meses, 34 pips através de 0.6700. O emprego da Austrália de outubro, na taxa de quinta: -43.500 vagas (esperado +25.000, setembro -39.300) e desemprego a 4,9% (esperado 4,7%, anterior 4,7%), máxima desde outubro de 2021 (ABS, 19/11). As altas do RBA saíram da conta. O RBA está em 4,85% e decide em 8/12. O piso de 1,5σ20 é de 49 pips, então o stop que paga o piso já volta para cima de 0.6700. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (0,7045) com a SMA50 (0,6969) abaixo dela — alinhamento de baixa. O próprio fechamento é a mínima de 10/20 pregões e de 9 meses. A máxima de 10 pregões é 0,6904 (10/11).",
        "support": "0.6600 (o próximo redondo, 66 pips abaixo). O fechamento de 20/11 (0,6666) é a mínima de 9 meses.",
        "resistance": "0.6700 (o redondo perdido, 34 pips acima) e 0,6711 (a mínima de quinta), com a máxima de 10 pregões em 0,6904.",
        "priceAction": "O emprego australiano quebrou 0.6700 por 34 pips. O stop legal volta para cima do rompimento. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "O fechamento sob 0.6700 saiu, sem confirmação. 34 pips de volta até o redondo são menos que o piso de 49. Sem gatilho novo.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O Aussie fez a nova mínima com o emprego em queda livre. O rompimento é de uma sessão e o piso não cabe."
    },
    en={
        "fundamental": "AUD/USD closed at 0.6666 in the Friday 20/11/2026 session (ECB/Frankfurter reference rate), down -0.68% (-46 pips) from 0.6711. It is the new 10/20-day and 9-month low, 34 pips through 0.6700. Australia's October jobs, in Thursday's fixing: -43,500 jobs (+25,000 expected, September -39,300) and unemployment at 4.9% (4.7% expected, 4.7% prior), the highest since October 2021 (ABS, Nov 19). RBA hikes are off the table. The RBA is at 4.85% and decides on Dec 8. The 1.5-sigma20 floor is 49 pips, so the stop that meets the floor is already back above 0.6700. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (0.7045) with the SMA50 (0.6969) below it — bear alignment. Today's close is the 10/20-day and 9-month low. The 10-day high is 0.6904 (Nov 10).",
        "support": "0.6600 (the next round, 66 pips below). The Nov-20 close (0.6666) is the 9-month low.",
        "resistance": "0.6700 (the round just lost, 34 pips above) and 0.6711 (Thursday's low), with the 10-day high at 0.6904.",
        "priceAction": "The Australian jobs report broke 0.6700 by 34 pips. The legal stop lands back above the breakdown. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The close under 0.6700 has printed, unconfirmed. 34 pips back up to the round is less than the 49-pip floor. No new trigger.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The Aussie made the new low with employment in free fall. The breakdown is one session old and the floor does not fit."
    })

GBP = pair("1.3125", "BAIXA", "bear",
    pt={
        "fundamental": "O GBP/USD fechou em 1,3125 na sessão de sexta 20/11/2026 (taxa de referência BCE/Frankfurter), caindo -0,20% (-27 pips) a partir de 1,3151. É a nova mínima de 10/20 pregões e de 9 meses, 35 pips através de 1.3160. O varejo do Reino Unido de outubro subiu 0,7% no mês (consenso 0,0%, setembro revisto a -0,6%), com o ano a 2,3% (ONS, 20/11, 07:00 UTC) — está neste fixing, e o cabo caiu mesmo assim. A Bank Rate está em 4,00%. O piso de 1,5σ20 é de 70 pips, então o stop que paga o piso já volta para cima de 1.3160. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (1,3406) e sob a SMA50 (1,3310), com a SMA50 abaixo da SMA200 — alinhamento de baixa. O próprio fechamento é a mínima de 10/20 pregões e de 9 meses. A máxima de 10 pregões é 1,3423 (10/11). A de 20 pregões segue 1,3500 (04/11).",
        "support": "1.3100 (o próximo redondo, 25 pips abaixo) e 1.3000 (125 pips). O fechamento de 20/11 (1,3125) é a mínima de 9 meses.",
        "resistance": "1.3160 (a mínima antiga, 35 pips acima) e 1,3310 (a SMA50).",
        "priceAction": "O varejo bateu o consenso e o cabo perdeu 1.3160 mesmo assim. O stop legal volta para cima do rompimento. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "O fechamento sob 1,3160 saiu, sem confirmação. 35 pips de volta até o extremo são menos que o piso de 70. Sem gatilho novo.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "A libra fez nova mínima de 9 meses no dia do varejo forte. O rompimento é de uma sessão e o piso não cabe."
    },
    en={
        "fundamental": "GBP/USD closed at 1.3125 in the Friday 20/11/2026 session (ECB/Frankfurter reference rate), down -0.20% (-27 pips) from 1.3151. It is the new 10/20-day and 9-month low, 35 pips through 1.3160. UK October retail sales rose 0.7% on the month (0.0% consensus, September revised to -0.6%), with the year at 2.3% (ONS, Nov 20, 07:00 UTC) — it is in this fixing, and cable fell anyway. Bank Rate is 4.00%. The 1.5-sigma20 floor is 70 pips, so the stop that meets the floor is already back above 1.3160. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (1.3406) and under the SMA50 (1.3310), with the SMA50 below the SMA200 — bear alignment. Today's close is the 10/20-day and 9-month low. The 10-day high is 1.3423 (Nov 10). The 20-day high is still 1.3500 (Nov 4).",
        "support": "1.3100 (the next round, 25 pips below) and 1.3000 (125 pips). The Nov-20 close (1.3125) is the 9-month low.",
        "resistance": "1.3160 (the prior low, 35 pips above) and 1.3310 (the SMA50).",
        "priceAction": "Retail beat the consensus and cable lost 1.3160 anyway. The legal stop lands back above the breakdown. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The close under 1.3160 has printed, unconfirmed. 35 pips back up to the extreme is less than the 70-pip floor. No new trigger.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "Sterling made a new 9-month low on the day of strong retail. The breakdown is one session old and the floor does not fit."
    })

EURJPY = pair("174.35", "BAIXA", "bear",
    pt={
        "fundamental": "O EUR/JPY fechou em 174,35 na sessão de sexta 20/11/2026 (taxa de referência BCE/Frankfurter), caindo -0,85% (-149 pips) a partir de 175,84. Quinta devolveu 175,00; sexta perdeu de novo e fez a nova mínima de 10/20 pregões e de 9 meses. O CPI do Japão veio abaixo do esperado nas três medidas, mas o iene firmou e a alta do BoJ em dezembro segue na mesa. O próximo redondo, 174,00, está a 35 pips. O aviso do MoF de 12-13/11 mantém o piso em 2,5σ20, aqui 188 pips, então o stop que paga o piso já atravessa 174,00 e cai perto de 173,00. A SMA50 está em 177,45 e a SMA200 em 182,68. Alinhamento de baixa. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (182,68) com a SMA50 (177,45) abaixo dela — alinhamento de baixa pleno. O próprio fechamento é a mínima de 10/20 pregões e de 9 meses. A máxima de 10 pregões está em 177,38 (10/11).",
        "support": "174.00 (o próximo redondo, 35 pips abaixo) e 173.00 (135 pips). O fechamento de 20/11 (174,35) é a nova mínima de 9 meses.",
        "resistance": "174.85 (a mínima de quarta, 51 pips acima) e 175,00, com a SMA50 em 177,45.",
        "priceAction": "Devolveu 175 na quinta e perdeu tudo na sexta, parando 35 pips antes de 174,00. O piso é 188. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "O fechamento sob 175,00 saiu de novo. 35 pips até 174,00 são menos que o piso de 188. Sem gatilho novo.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O cruzado fez nova mínima de 9 meses no dia do CPI. O próximo redondo continua dentro do piso de 188 pips."
    },
    en={
        "fundamental": "EUR/JPY closed at 174.35 in the Friday 20/11/2026 session (ECB/Frankfurter reference rate), down -0.85% (-149 pips) from 175.84. Thursday handed 175.00 back; Friday lost it again and made the new 10/20-day and 9-month low. Japan's CPI came in below expectations on all three measures, but the yen firmed and the December BoJ hike stays on the table. The next round, 174.00, is 35 pips away. The MoF warning of Nov 12-13 keeps the floor at 2.5-sigma20, here 188 pips, so the stop that meets the floor is already through 174.00 and lands near 173.00. The SMA50 is at 177.45 and the SMA200 at 182.68. Bear alignment. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (182.68) with the SMA50 (177.45) below it — full bear alignment. Today's close is the 10/20-day and 9-month low. The 10-day high is 177.38 (Nov 10).",
        "support": "174.00 (the next round, 35 pips below) and 173.00 (135 pips). The Nov-20 close (174.35) is the new 9-month low.",
        "resistance": "174.85 (Wednesday's low, 51 pips above) and 175.00, with the SMA50 at 177.45.",
        "priceAction": "It handed 175 back on Thursday and lost everything on Friday, stopping 35 pips short of 174.00. The floor is 188. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The close under 175.00 has printed again. 35 pips down to 174.00 is less than the 188-pip floor. No new trigger.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The cross made a new 9-month low on CPI day. The next round is still inside the 188-pip floor."
    })

GBPJPY = pair("208.21", "BAIXA", "bear",
    pt={
        "fundamental": "O GBP/JPY fechou em 208,21 na sessão de sexta 20/11/2026 (taxa de referência BCE/Frankfurter), caindo -1,03% (-217 pips) a partir de 210,38. É a nova mínima de 10/20 pregões, através de 209,61, de 209,00 e de 208,50. A mínima de 9 meses agora é 207,91 (09/09) — a de 207,32 (17/02) saiu da janela de 195 pregões — a 30 pips. O varejo britânico forte e o CPI do Japão estão neste fixing, e o cruzado caiu mesmo assim. O piso, ainda aberto pelo jawboning do MoF, é de 202 pips, então o stop que paga o piso já atravessa 207,91. BoE em 4,00%, BoJ em 1,25%. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (212,83) e sob a SMA50 (210,18), com a SMA50 sob a SMA200 — alinhamento de baixa pleno. O próprio fechamento é a mínima de 10/20 pregões. A máxima de 10 pregões está em 212,32 (10/11).",
        "support": "207.91 (mínima de 9 meses, 30 pips abaixo). O fechamento de 20/11 (208,21) é a mínima de 10/20 pregões.",
        "resistance": "209.61 (a mínima antiga de 20 pregões, 140 pips acima) e 210,18 (a SMA50).",
        "priceAction": "Perdeu 209,61 e parou 30 pips antes de 207,91. O piso é 202. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "O fechamento sob 209,61 saiu. 30 pips até 207,91 são menos que o piso de 202. Sem gatilho novo.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O cruzado andou 217 pips e a mínima de 9 meses ficou dentro do piso. Vender aqui atravessa o extremo."
    },
    en={
        "fundamental": "GBP/JPY closed at 208.21 in the Friday 20/11/2026 session (ECB/Frankfurter reference rate), down -1.03% (-217 pips) from 210.38. It is the new 10/20-day low, through 209.61, 209.00 and 208.50. The 9-month low is now 207.91 (Sep 9) — 207.32 (Feb 17) rolled out of the 195-session window — 30 pips away. Strong UK retail and Japan's CPI are both in this fixing, and the cross fell anyway. The floor, still open from the MoF jawboning, is 202 pips, so the stop that meets the floor is already through 207.91. BoE at 4.00%, BoJ at 1.25%. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (212.83) and under the SMA50 (210.18), with the SMA50 under the SMA200 — full bear alignment. Today's close is the 10/20-day low. The 10-day high is 212.32 (Nov 10).",
        "support": "207.91 (the 9-month low, 30 pips below). The Nov-20 close (208.21) is the 10/20-day low.",
        "resistance": "209.61 (the prior 20-day low, 140 pips above) and 210.18 (the SMA50).",
        "priceAction": "It lost 209.61 and stopped 30 pips short of 207.91. The floor is 202. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The close under 209.61 has printed. 30 pips down to 207.91 is less than the 202-pip floor. No new trigger.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The cross moved 217 pips and the 9-month low sits inside the floor. Selling here crosses the extreme."
    })

DATA = {
    "EUR/USD": EUR, "USD/JPY": USDJPY, "AUD/USD": AUD,
    "GBP/USD": GBP, "EUR/JPY": EURJPY, "GBP/JPY": GBPJPY,
}
DRIVERS = {
    "EUR/USD": {
        "en": ["Holds above the 9-month low at 1.0990", "22 pips to 1.0968, floor is 61", "Dollar at a 19-month high"],
        "pt": ["Segura acima da mín. de 9 meses em 1,0990", "22 pips até 1,0968, piso é 61", "Dólar em máxima de 19 meses"],
    },
    "USD/JPY": {
        "en": ["Through the SMA200 to 158.64", "Bear alignment, floor is 136", "Japan CPI missed, Dec hike on"],
        "pt": ["Através da SMA200 até 158,64", "Alinhamento de baixa, piso é 136", "CPI do Japão errou, alta em dez na mesa"],
    },
    "AUD/USD": {
        "en": ["New 9-month low at 0.6666", "34 pips through 0.6700, floor is 49", "Jobs -43.5k, jobless 4.9%"],
        "pt": ["Nova mín. de 9 meses em 0,6666", "34 pips sob 0.6700, piso é 49", "Emprego -43,5 mil, desemprego 4,9%"],
    },
    "GBP/USD": {
        "en": ["New 9-month low at 1.3125", "35 pips through 1.3160, floor is 70", "Retail +0.7% beat, cable fell"],
        "pt": ["Nova mín. de 9 meses em 1,3125", "35 pips sob 1,3160, piso é 70", "Varejo +0,7% e o cabo caiu"],
    },
    "EUR/JPY": {
        "en": ["New 9-month low at 174.35", "35 pips to 174.00, floor is 188", "MoF floor still open"],
        "pt": ["Nova mín. de 9 meses em 174,35", "35 pips até 174,00, piso é 188", "Piso do MoF segue aberto"],
    },
    "GBP/JPY": {
        "en": ["New 10/20-day low at 208.21", "30 pips to 207.91, floor is 202", "9-month low inside the stop"],
        "pt": ["Nova mín. de 10/20 pregões em 208,21", "30 pips até 207,91, piso é 202", "Mín. de 9 meses dentro do stop"],
    },
}

NEWS_ITEM_JS = r'''                {
                    date: "20/11/2026",
                    category: "macro",
                    impact: "high",
                    pairs: ["EUR/USD", "USD/JPY", "AUD/USD", "GBP/USD", "EUR/JPY", "GBP/JPY"],
                    pt: {
                        headline: "O iene atravessa a SMA200 com o CPI do Japão — o Aussie e o cabo fazem novas mínimas de 9 meses, e os seis seguem sem ticket",
                        summary: "A taxa BCE/Frankfurter de 20/11 vira o mapa do iene e estende as mínimas. USD/JPY fechou 158,64 (−0,83%), através da SMA200 (158,77), e o alinhamento misto virou baixa. O CPI do Japão de outubro: cheio 2,3% (esperado 2,5%), núcleo 2,2% (esperado 2,3%), núcleo-núcleo 2,2% (esperado 2,3%) — erro para baixo nas três, mas acima de 2%, e a alta do BoJ em dezembro segue na mesa. O aviso do MoF mantém o piso em 136. AUD/USD fechou 0,6666 (−0,68%), nova mínima de 9 meses, 34 pips através de 0.6700, depois do emprego: -43.500 vagas e desemprego a 4,9%, máxima desde 2021 (ABS, 19/11). Piso de 49. GBP/USD fechou 1,3125 (−0,20%), nova mínima de 9 meses, 35 pips através de 1.3160, mesmo com o varejo a +0,7% (ONS, 07:00 UTC). Piso de 70. EUR/USD fechou 1,0990 (−0,02%) e segurou acima de 1,0968, com o dólar em máxima de 19 meses. EUR/JPY 174,35 (−0,85%) é nova mínima de 9 meses, a 35 pips de 174,00, piso de 188. GBP/JPY 208,21 (−1,03%) é nova mínima de 10/20 pregões, a 30 pips de 207,91, piso de 202. Os seis ficam em AGUARDAR. Thanksgiving em 26/11, RBA e FOMC em 8/12.",
                        take: "O CPI virou o iene, mas o short passa por dentro de 157,95 e 157,25. Os três rompimentos de sexta são de uma sessão e cada stop legal volta para cima do extremo. A mesa segue vazia na semana do Thanksgiving."
                    },
                    en: {
                        headline: "The yen crosses the SMA200 on Japan CPI — the Aussie and cable print new 9-month lows, and all six stay without a ticket",
                        summary: "The 20/11 ECB/Frankfurter fixing flips the yen map and extends the lows. USD/JPY closed 158.64 (−0.83%), through the SMA200 (158.77), and the mixed map flipped to bear. Japan's October CPI: headline 2.3% (2.5% expected), core 2.2% (2.3% expected), core-core 2.2% (2.3% expected) — a miss on all three, but above 2%, and the December BoJ hike stays on the table. The MoF warning keeps the floor at 136. AUD/USD closed 0.6666 (−0.68%), a new 9-month low, 34 pips through 0.6700, after the jobs miss: -43,500 jobs and unemployment at 4.9%, the highest since 2021 (ABS, Nov 19). Floor 49. GBP/USD closed 1.3125 (−0.20%), a new 9-month low, 35 pips through 1.3160, even with retail at +0.7% (ONS, 07:00 UTC). Floor 70. EUR/USD closed 1.0990 (−0.02%) and held above 1.0968, with the dollar at a 19-month high. EUR/JPY 174.35 (−0.85%) is a new 9-month low, 35 pips from 174.00, floor 188. GBP/JPY 208.21 (−1.03%) is a new 10/20-day low, 30 pips from 207.91, floor 202. All six stay on WAIT. Thanksgiving on Nov 26, RBA and FOMC on Dec 8.",
                        take: "CPI flipped the yen, but the short runs inside 157.95 and 157.25. Friday's three breakdowns are one session old and every legal stop lands back above the extreme. The desk stays empty into Thanksgiving week."
                    }
                },
'''

NEWS_CARD = r'''                <!-- News 20/11/2026: Japan CPI flips USD/JPY bear; three new 9-month lows; all six WAIT -->
                <article class="news-card">
                    <div class="news-card-top">
                        <span class="news-cat"><span class="lang-en">Macro Data</span><span class="lang-pt" style="display:none;">Dados Macro</span></span>
                        <span class="impact-badge high"><span class="lang-en">High Impact</span><span class="lang-pt" style="display:none;">Impacto Alto</span></span>
                        <span class="news-date">20/11/2026</span>
                    </div>
                    <h2 class="news-title">
                        <span class="lang-en">The yen crosses the SMA200 on Japan CPI — the Aussie and cable print new 9-month lows, and all six stay without a ticket</span>
                        <span class="lang-pt" style="display:none;">O iene atravessa a SMA200 com o CPI do Japão — o Aussie e o cabo fazem novas mínimas de 9 meses, e os seis seguem sem ticket</span>
                    </h2>
                    <p class="news-summary">
                        <span class="lang-en">The 20/11 ECB/Frankfurter fixing flips the yen map and extends the lows. USD/JPY closed 158.64 (−0.83%), through the SMA200 (158.77), and the mixed map flipped to bear. Japan's October CPI: headline 2.3% (2.5% expected), core 2.2% (2.3% expected), core-core 2.2% (2.3% expected) — a miss on all three, but above 2%, and the December BoJ hike stays on the table. The MoF warning keeps the floor at 136. AUD/USD closed 0.6666 (−0.68%), a new 9-month low, 34 pips through 0.6700, after the jobs miss: -43,500 jobs and unemployment at 4.9%, the highest since 2021 (ABS, Nov 19). Floor 49. GBP/USD closed 1.3125 (−0.20%), a new 9-month low, 35 pips through 1.3160, even with retail at +0.7% (ONS, 07:00 UTC). Floor 70. EUR/USD closed 1.0990 (−0.02%) and held above 1.0968, with the dollar at a 19-month high. EUR/JPY 174.35 (−0.85%) is a new 9-month low, 35 pips from 174.00, floor 188. GBP/JPY 208.21 (−1.03%) is a new 10/20-day low, 30 pips from 207.91, floor 202. All six stay on WAIT. Thanksgiving on Nov 26, RBA and FOMC on Dec 8.</span>
                        <span class="lang-pt" style="display:none;">A taxa BCE/Frankfurter de 20/11 vira o mapa do iene e estende as mínimas. USD/JPY fechou 158,64 (−0,83%), através da SMA200 (158,77), e o alinhamento misto virou baixa. O CPI do Japão de outubro: cheio 2,3% (esperado 2,5%), núcleo 2,2% (esperado 2,3%), núcleo-núcleo 2,2% (esperado 2,3%) — erro para baixo nas três, mas acima de 2%, e a alta do BoJ em dezembro segue na mesa. O aviso do MoF mantém o piso em 136. AUD/USD fechou 0,6666 (−0,68%), nova mínima de 9 meses, 34 pips através de 0.6700, depois do emprego: -43.500 vagas e desemprego a 4,9%, máxima desde 2021 (ABS, 19/11). Piso de 49. GBP/USD fechou 1,3125 (−0,20%), nova mínima de 9 meses, 35 pips através de 1.3160, mesmo com o varejo a +0,7% (ONS, 07:00 UTC). Piso de 70. EUR/USD fechou 1,0990 (−0,02%) e segurou acima de 1,0968, com o dólar em máxima de 19 meses. EUR/JPY 174,35 (−0,85%) é nova mínima de 9 meses, a 35 pips de 174,00, piso de 188. GBP/JPY 208,21 (−1,03%) é nova mínima de 10/20 pregões, a 30 pips de 207,91, piso de 202. Os seis ficam em AGUARDAR. Thanksgiving em 26/11, RBA e FOMC em 8/12.</span>
                    </p>
                    <div class="news-take">
                        <span class="take-tag"><span class="lang-en">Desk take</span><span class="lang-pt" style="display:none;">Leitura da mesa</span></span>
                        <span class="lang-en">CPI flipped the yen, but the short runs inside 157.95 and 157.25. Friday's three breakdowns are one session old and every legal stop lands back above the extreme. The desk stays empty into Thanksgiving week.</span>
                        <span class="lang-pt" style="display:none;">O CPI virou o iene, mas o short passa por dentro de 157,95 e 157,25. Os três rompimentos de sexta são de uma sessão e cada stop legal volta para cima do extremo. A mesa segue vazia na semana do Thanksgiving.</span>
                    </div>
                    <div class="news-pairs">
                        <span class="np-label"><span class="lang-en">Watch</span><span class="lang-pt" style="display:none;">Acompanhar</span></span>
                        <a href="eur-usd.html" class="pair-link-chip">EUR/USD</a><a href="usd-jpy.html" class="pair-link-chip">USD/JPY</a><a href="aud-usd.html" class="pair-link-chip">AUD/USD</a><a href="gbp-usd.html" class="pair-link-chip">GBP/USD</a><a href="eur-jpy.html" class="pair-link-chip">EUR/JPY</a><a href="gbp-jpy.html" class="pair-link-chip">GBP/JPY</a>
                    </div>
                </article>

'''

NEW_CAL = '''                <div class="cal-cell">
                    <span class="cal-date">19/11</span>
                    <span class="cal-event"><span class="lang-en">Australia jobs -43.5k, jobless 4.9% (ABS)</span><span class="lang-pt" style="display:none;">Emprego da Austrália -43,5 mil, desemprego 4,9% (ABS)</span></span>
                    <div class="cal-meta"><span class="cal-impact high" aria-hidden="true"></span><span class="cal-cur">AUD</span></div>
                </div>
                <div class="cal-cell">
                    <span class="cal-date">19/11</span>
                    <span class="cal-event"><span class="lang-en">Japan CPI 23:30 UTC: core 2.2% y/y</span><span class="lang-pt" style="display:none;">CPI do Japão 23:30 UTC: núcleo 2,2% a/a</span></span>
                    <div class="cal-meta"><span class="cal-impact high" aria-hidden="true"></span><span class="cal-cur">JPY</span></div>
                </div>
                <div class="cal-cell">
                    <span class="cal-date">20/11</span>
                    <span class="cal-event"><span class="lang-en">UK retail +0.7% m/m, cable fell anyway</span><span class="lang-pt" style="display:none;">Varejo do Reino Unido +0,7% m/m, cabo caiu mesmo assim</span></span>
                    <div class="cal-meta"><span class="cal-impact high" aria-hidden="true"></span><span class="cal-cur">GBP</span></div>
                </div>
                <div class="cal-cell">
                    <span class="cal-date">26/11</span>
                    <span class="cal-event"><span class="lang-en">US Thanksgiving, thin liquidity</span><span class="lang-pt" style="display:none;">Thanksgiving nos EUA, liquidez fina</span></span>
                    <div class="cal-meta"><span class="cal-impact med" aria-hidden="true"></span><span class="cal-cur">USD</span></div>
                </div>'''

def main():
    print("STAMP", TS)
    with open(INDEX, encoding="utf-8") as f:
        idx = f.read()
    if idx.count(OLD_TS) != 4:
        raise SystemExit("expected 4 old timestamps, found %d" % idx.count(OLD_TS))
    idx = idx.replace(OLD_TS, TS)
    idx = idx.replace(
        "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 588 daily sessions (01/08/2024–18/11/2026).",
        "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 590 daily sessions (01/08/2024–20/11/2026).")
    idx = idx.replace(
        "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, σ20 e Donchian calculados · 588 pregões (01/08/2024 a 18/11/2026).",
        "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, σ20 e Donchian calculados · 590 pregões (01/08/2024 a 20/11/2026).")
    idx = idx.replace(
        'nextEvent: "UK CPI 3.6% · cable 9 pips from 1.3160 · FOMC Dec 8-9"',
        'nextEvent: "Japan CPI 2.2% · three new 9-month lows · Thanksgiving week"')
    idx = idx.replace(
        'nextEvent: "CPI Reino Unido 3,6% · cabo a 9 pips de 1.3160 · FOMC 8-9/12"',
        'nextEvent: "CPI do Japão 2,2% · três novas mínimas de 9 meses · semana de Thanksgiving"')

    start = idx.find("        const forexData = {")
    end = idx.find("        /* ==========================================\n           B. Market metadata")
    if start < 0 or end < 0:
        raise SystemExit("forexData markers missing")
    idx = idx[:start] + "        const forexData = " + json.dumps(DATA, ensure_ascii=False, indent=4) + ";\n\n" + idx[end:]

    d0 = idx.find("        const dailyChanges = {")
    d1 = idx.find("        const macroDrivers = {")
    changes = {
        "EUR/USD": "-0.02%", "USD/JPY": "-0.83%", "AUD/USD": "-0.68%",
        "GBP/USD": "-0.20%", "EUR/JPY": "-0.85%", "GBP/JPY": "-1.03%",
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
    ledger["meta"]["lastUpdated"] = "20/11/2026"
    with open(LEDGER, "w", encoding="utf-8", newline="\n") as f:
        json.dump(ledger, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("ledger lastUpdated only; book still empty")

    with open(NEWS, encoding="utf-8") as f:
        news = f.read()
    news = news.replace(
        "Market Wire · Cable on the 9-Month Low, Still No Ticket",
        "Market Wire · The Yen Turns, Three New Lows, Still No Ticket")
    news = news.replace(
        "Telégrafo da Mesa · A Libra na Mínima de 9 Meses, Ainda Sem Ticket",
        "Telégrafo da Mesa · O Iene Vira, Três Novas Mínimas, Ainda Sem Ticket")
    news = news.replace(OLD_TS, TS)
    news = news.replace(
        "6 pairs · UK CPI 3.6% · minutes after the fix · FOMC Dec 8-9",
        "6 pairs · Japan CPI 2.2% · AU jobs miss · Thanksgiving week")
    news = news.replace(
        "6 pares · CPI do Reino Unido 3,6% · ata depois do fixing · FOMC 8-9/12",
        "6 pares · CPI do Japão 2,2% · emprego da Austrália erra · semana de Thanksgiving")
    start = news.find('                <div class="cal-cell">')
    end = news.find("            </div>\n        </section>", start)
    if start < 0 or end < 0:
        raise SystemExit("calendar block missing")
    news = news[:start] + NEW_CAL + "\n" + news[end:]
    marker = "                <!-- News 18/11/2026:"
    if marker not in news:
        raise SystemExit("news marker missing")
    news = news.replace(marker, NEWS_CARD + marker, 1)
    with open(NEWS, "w", encoding="utf-8", newline="\n") as f:
        f.write(news)
    print("news.html patched")

    with open(SITEMAP, encoding="utf-8") as f:
        sm = f.read()
    n = sm.count("2026-11-18")
    if n != 9:
        raise SystemExit("expected 9 sitemap dates, found %d" % n)
    sm = sm.replace("2026-11-18", "2026-11-20")
    with open(SITEMAP, "w", encoding="utf-8", newline="\n") as f:
        f.write(sm)
    print("sitemap patched")

    with open(VERIFY, encoding="utf-8") as f:
        v = f.read()
    v = v.replace('TODAY_TS = "18/11/2026 20:09 UTC"', 'TODAY_TS = "%s"' % TS)
    v = v.replace(
        'TODAY_DATE = "18/11/2026"  # basis session date (report edition: 18/11/2026)',
        'TODAY_DATE = "20/11/2026"  # basis session date (report edition: 20/11/2026)')
    old_ticker = '''TICKER = [("EUR/USD","-0.19%"),("USD/JPY","+0.08%"),("AUD/USD","-0.05%"),
          ("GBP/USD","-0.17%"),("EUR/JPY","-0.12%"),("GBP/JPY","-0.10%")]'''
    new_ticker = '''TICKER = [("EUR/USD","-0.02%"),("USD/JPY","-0.83%"),("AUD/USD","-0.68%"),
          ("GBP/USD","-0.20%"),("EUR/JPY","-0.85%"),("GBP/JPY","-1.03%")]'''
    if old_ticker not in v:
        raise SystemExit("ticker block missing")
    v = v.replace(old_ticker, new_ticker)
    with open(VERIFY, "w", encoding="utf-8", newline="\n") as f:
        f.write(v)
    print("verify constants patched")

if __name__ == "__main__":
    main()
