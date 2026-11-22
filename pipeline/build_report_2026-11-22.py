#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""22/11/2026 Sunday week-ahead edition, on the Friday 20/11 ECB fixing
(no weekend session, so all levels are Friday's: 590 sessions).

Friday's lows stand: EUR/USD holds above 1.0968 with the dollar at a
19-month high; USD/JPY sits under the SMA200 after Japan CPI; AUD/USD,
GBP/USD and EUR/JPY hold new 9-month lows; GBP/JPY holds a new 10/20-day
low 30 pips above 207.91. The week-ahead wall (Monday flash PMIs, Wednesday
US PCE + Q3 GDP + AU CPI + Beige Book, Thursday Thanksgiving with ECB
minutes + Tokyo CPI) leaves no fresh trigger: all six stay on WAIT.
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
OLD_TS = "20/11/2026 20:52 UTC"
BASIS = "590 sessions, 01/08/2024 to 20/11/2026"
BASIS_PT = "590 pregões, 01/08/2024 a 20/11/2026"

def pair(quote, bias, bias_type, pt, en):
    return {"quote": quote, "bias": bias, "biasType": bias_type, "pt": pt, "en": en}

EUR = pair("1.0990", "BAIXA", "bear",
    pt={
        "fundamental": "Edição de domingo 22/11/2026, sobre a taxa de referência BCE/Frankfurter de sexta 20/11/2026 (sem pregão no fim de semana): o EUR/USD fechou a sexta em 1,0990, caindo -0,02% (-2 pips) a partir de 1,0992, e segurou acima da mínima de 9 meses de 1,0968 (18/11), a 22 pips, com o dólar em máxima de 19 meses (≈103,9 no DXY, quarto ganho semanal). Até 1.0950 são 40 pips, e o piso de 1,5σ20 é de 61 pips: o stop que paga o piso já atravessa 1,0968 e cai perto de 1.0950. A semana abre com os PMIs flash de segunda (zona do euro, Alemanha, Reino Unido, EUA) e a muralha cai na quarta: PIB dos EUA do 3º tri (2ª leitura, esperado 3,5% vs 3,4%) e PCE de outubro (cheio esperado +0,3% no mês vs +0,5% em setembro) às 13:30 UTC, mais claims e Beige Book; quinta é Thanksgiving (EUA fechados) com a ata do BCE. O Fed segue em 3,75-4,00%, com a alta de 8-9/12 precificada em ≈95% depois da ata hawkish (quase todos viram nova alta como adequada; dois ventilaram mais de 25 pb). O BCE decide em 17/12, com o depósito em 2,50% e alta de 25 pb a ≈96% (última do ciclo, com a inflação de outubro em 4,0%). Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (1,1507) com a SMA50 (1,1238) abaixo dela — alinhamento de baixa pleno. A mínima de 10/20 pregões e de 9 meses segue 1,0968 (18/11). A máxima de 10 pregões é 1,1214 (10/11). A de 20 pregões segue 1,1267 (04/11).",
        "support": "1,0968 (mínima de 9 meses, 22 pips abaixo) e 1.0950 (40 pips).",
        "resistance": "1,0992 (a mínima de quinta, devolvida) e 1.1000, com a SMA50 em 1,1238.",
        "priceAction": "Dois pips de queda na sexta depois da ata. 1,0968 segue 22 pips abaixo, dentro do piso de 61. A semana abre nos PMIs e se decide na muralha de quarta. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "O fechamento sob 1,1000 saiu na quinta e se repetiu na sexta. O espaço até 1,0968 é menor que o piso, e o stop legal já atravessa 1,0950. Sem gatilho novo — reavaliar depois de quarta (PCE, PIB, claims, Beige Book) e da ata do BCE de quinta.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O euro segurou acima da mínima mesmo com o dólar em máxima de 19 meses. Vender aqui coloca 1,0968 e 1,0950 dentro do stop — e a quarta decide o dólar."
    },
    en={
        "fundamental": "Sunday 22/11/2026 edition, on the Friday 20/11/2026 ECB/Frankfurter reference rate (no weekend fixing): EUR/USD closed Friday at 1.0990, down -0.02% (-2 pips) from 1.0992, and held above the 9-month low of 1.0968 (Nov 18), 22 pips away, with the dollar at a 19-month high (≈103.9 on the DXY, a fourth weekly gain). 1.0950 is 40 pips away, and the 1.5-sigma20 floor is 61 pips: the stop that meets the floor is already through 1.0968 and lands near 1.0950. The week opens with Monday's flash PMIs (eurozone, Germany, UK, US) and the wall lands Wednesday: US Q3 GDP (second estimate, 3.5% eyed vs 3.4%) and October PCE (headline +0.3% m/m eyed vs +0.5% in September) at 13:30 UTC, plus claims and the Beige Book; Thursday is Thanksgiving (US shut) with the ECB minutes. The Fed is still at 3.75-4.00%, with the Dec 8-9 hike priced at ≈95% after the hawkish minutes (almost all saw a further hike as appropriate; two floated more than 25bp). The ECB decides on Dec 17, with the deposit rate at 2.50% and a 25bp hike at ≈96% (the last of the cycle, with October inflation at 4.0%). Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (1.1507) with the SMA50 (1.1238) below it — full bear alignment. The 10/20-day and 9-month low is still 1.0968 (Nov 18). The 10-day high is 1.1214 (Nov 10). The 20-day high is still 1.1267 (Nov 4).",
        "support": "1.0968 (the 9-month low, 22 pips below) and 1.0950 (40 pips).",
        "resistance": "1.0992 (Thursday's low, handed back) and 1.1000, with the SMA50 at 1.1238.",
        "priceAction": "Two pips down on Friday after the minutes. 1.0968 is still 22 pips below, inside the 61-pip floor. The week opens on PMIs and is decided on Wednesday's wall. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The close under 1.1000 printed on Thursday and repeated on Friday. The room down to 1.0968 is smaller than the floor, and the legal stop is already through 1.0950. No new trigger — reassess after Wednesday (PCE, GDP, claims, Beige Book) and Thursday's ECB minutes.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The euro held above the low even with the dollar at a 19-month high. Selling here puts 1.0968 and 1.0950 inside the stop — and Wednesday decides the dollar."
    })

USDJPY = pair("158.64", "BAIXA", "bear",
    pt={
        "fundamental": "Edição de domingo 22/11/2026, sobre a taxa de referência BCE/Frankfurter de sexta 20/11/2026 (sem pregão no fim de semana): o USD/JPY fechou a sexta em 158,64, caindo -0,83% (-133 pips) a partir de 159,97. O CPI do Japão de outubro (cheio 2,3% — esperado 2,5%, anterior 2,1%; núcleo 2,2% — esperado 2,3%, anterior 2,1%; núcleo-núcleo 2,2% — esperado 2,3%, anterior 2,4%) firmou o iene e o fechamento atravessou a SMA200 (158,77) para baixo, 13 pips abaixo dela: o mapa, misto desde o aviso de Katayama, virou alinhamento de baixa na sexta. O aviso de 12-13/11 segue dentro de 30 dias, sem intervenção confirmada, então o piso segue em 2,5σ20: 136 pips. O BoJ está em 1,25% e decide em 17-18/12, com 86% dos economistas (Reuters, 61 de 71) vendo alta a 1,50%. O Japão fecha na segunda (feriado) e o CPI de Tóquio de novembro sai na quinta, com os EUA no Thanksgiving. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (158,77) com a SMA50 (157,92) abaixo dela — alinhamento de baixa, virado na sexta. A máxima de 10/20 pregões segue 160,00 (13/11). A mínima de 10 pregões é 157,95 (09/11); a de 20, 157,25 (30/10). A máxima de 9 meses segue 163,91.",
        "support": "157.95 (mínima de 10 pregões, 69 pips abaixo) e 157.25 (mínima de 20 pregões, 139 pips), com a SMA50 em 157,92.",
        "resistance": "158.77 (a SMA200, perdida por 13 pips) e 160.00 (máxima de 10/20 pregões).",
        "priceAction": "O CPI virou o mapa para baixa na sexta, mas 160,00 segue 136 pips acima — exatamente o piso. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "Não há rompimento impresso: 157,95 segue intacta. Vender 158,64 com stop sobre 160,00 paga o piso de 136 por 5 pips, e o alvo de 1 para 2 atravessa 157,95 e 157,25. Sem gatilho limpo. Reavaliar num fechamento sob 157,95 — depois da muralha de quarta e do CPI de Tóquio de quinta — ou depois do BoJ de 17-18/12.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O iene reagiu ao CPI e o alinhamento virou. Mas o caminho do short passa por dentro das mínimas de 10 e 20 pregões."
    },
    en={
        "fundamental": "Sunday 22/11/2026 edition, on the Friday 20/11/2026 ECB/Frankfurter reference rate (no weekend fixing): USD/JPY closed Friday at 158.64, down -0.83% (-133 pips) from 159.97. Japan's October CPI (headline 2.3% — 2.5% expected, 2.1% prior; core 2.2% — 2.3% expected, 2.1% prior; core-core 2.2% — 2.3% expected, 2.4% prior) firmed the yen and the close crossed under the SMA200 (158.77), 13 pips below it: the map, mixed since Katayama's warning, flipped to bear alignment on Friday. The Nov 12-13 warning is still inside 30 days, with no confirmed intervention, so the floor stays at 2.5-sigma20: 136 pips. The BoJ is at 1.25% and decides on Dec 17-18, with 86% of economists (Reuters, 61 of 71) seeing a hike to 1.50%. Japan is shut on Monday (holiday) and November Tokyo CPI lands Thursday, with the US on Thanksgiving. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (158.77) with the SMA50 (157.92) below it — bear alignment, flipped on Friday. The 10/20-day high is still 160.00 (Nov 13). The 10-day low is 157.95 (Nov 9); the 20-day low, 157.25 (Oct 30). The 9-month high is still 163.91.",
        "support": "157.95 (the 10-day low, 69 pips below) and 157.25 (the 20-day low, 139 pips), with the SMA50 at 157.92.",
        "resistance": "158.77 (the SMA200, lost by 13 pips) and 160.00 (the 10/20-day high).",
        "priceAction": "CPI flipped the map to bear on Friday, but 160.00 is still 136 pips above — exactly the floor. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "No breakdown has printed: 157.95 is still intact. Selling 158.64 with a stop over 160.00 clears the 136-pip floor by 5 pips, and the one-to-two target runs through 157.95 and 157.25. No clean trigger. Reassess on a close under 157.95 — after Wednesday's wall and Thursday's Tokyo CPI — or after the Dec 17-18 BoJ.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The yen reacted to CPI and the alignment flipped. But the short's path runs inside the 10- and 20-day lows."
    })

AUD = pair("0.6666", "BAIXA", "bear",
    pt={
        "fundamental": "Edição de domingo 22/11/2026, sobre a taxa de referência BCE/Frankfurter de sexta 20/11/2026 (sem pregão no fim de semana): o AUD/USD fechou a sexta em 0,6666, caindo -0,68% (-46 pips) a partir de 0,6711. É a nova mínima de 10/20 pregões e de 9 meses, 34 pips através de 0.6700. O emprego da Austrália de outubro: -43.500 vagas (esperado +25.000, setembro -39.300) e desemprego a 4,9% (esperado 4,7%, anterior 4,7%), máxima desde outubro de 2021 (ABS, 19/11). O RBA está em 4,85% (alta de 3/11, 6-3) e decide em 8/12, com a ata dividida (seis viram 4,85% como 'não claramente suficiente', três alertaram para desaceleração mais forte). O CPI de outubro sai na quarta às 00:30 UTC: o cheio é esperado em ≈4,7% (setembro 4,3%), máxima desde 2023, com o núcleo aparado em 3,6%. O piso de 1,5σ20 é de 49 pips, então o stop que paga o piso já volta para cima de 0.6700. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (0,7045) com a SMA50 (0,6969) abaixo dela — alinhamento de baixa. O fechamento de sexta é a mínima de 10/20 pregões e de 9 meses. A máxima de 10 pregões é 0,6904 (10/11).",
        "support": "0.6600 (o próximo redondo, 66 pips abaixo). O fechamento de 20/11 (0,6666) é a mínima de 9 meses.",
        "resistance": "0.6700 (o redondo perdido, 34 pips acima) e 0,6711 (a mínima de quinta), com a máxima de 10 pregões em 0,6904.",
        "priceAction": "O emprego australiano quebrou 0.6700 por 34 pips na sexta. O stop legal volta para cima do rompimento. Quarta tem CPI. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "O fechamento sob 0.6700 saiu na sexta, sem confirmação. 34 pips de volta até o redondo são menos que o piso de 49. Sem gatilho novo — reavaliar depois do CPI de quarta (00:30 UTC).",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O Aussie fez a nova mínima com o emprego em queda livre. O rompimento é de uma sessão e o piso não cabe — e o CPI de quarta vem antes de qualquer entrada."
    },
    en={
        "fundamental": "Sunday 22/11/2026 edition, on the Friday 20/11/2026 ECB/Frankfurter reference rate (no weekend fixing): AUD/USD closed Friday at 0.6666, down -0.68% (-46 pips) from 0.6711. It is the new 10/20-day and 9-month low, 34 pips through 0.6700. Australia's October jobs: -43,500 jobs (+25,000 expected, September -39,300) and unemployment at 4.9% (4.7% expected, 4.7% prior), the highest since October 2021 (ABS, Nov 19). The RBA is at 4.85% (Nov 3 hike, 6-3) and decides on Dec 8, with a split minutes (six saw 4.85% as 'not clearly sufficient', three warned of a sharper downturn). October CPI lands Wednesday at 00:30 UTC: headline eyed at ≈4.7% (September 4.3%), the highest since 2023, with trimmed mean at 3.6%. The 1.5-sigma20 floor is 49 pips, so the stop that meets the floor is already back above 0.6700. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (0.7045) with the SMA50 (0.6969) below it — bear alignment. Friday's close is the 10/20-day and 9-month low. The 10-day high is 0.6904 (Nov 10).",
        "support": "0.6600 (the next round, 66 pips below). The Nov-20 close (0.6666) is the 9-month low.",
        "resistance": "0.6700 (the round just lost, 34 pips above) and 0.6711 (Thursday's low), with the 10-day high at 0.6904.",
        "priceAction": "The Australian jobs report broke 0.6700 by 34 pips on Friday. The legal stop lands back above the breakdown. CPI is Wednesday. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The close under 0.6700 printed on Friday, unconfirmed. 34 pips back up to the round is less than the 49-pip floor. No new trigger — reassess after Wednesday's CPI (00:30 UTC).",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The Aussie made the new low with employment in free fall. The breakdown is one session old and the floor does not fit — and Wednesday's CPI comes before any entry."
    })

GBP = pair("1.3125", "BAIXA", "bear",
    pt={
        "fundamental": "Edição de domingo 22/11/2026, sobre a taxa de referência BCE/Frankfurter de sexta 20/11/2026 (sem pregão no fim de semana): o GBP/USD fechou a sexta em 1,3125, caindo -0,20% (-27 pips) a partir de 1,3151. É a nova mínima de 10/20 pregões e de 9 meses, 35 pips através de 1.3160. O varejo do Reino Unido de outubro subiu 0,7% no mês (consenso 0,0%, setembro revisto a -0,6%), com o ano a 2,3% (ONS, 20/11, 07:00 UTC) — está no fixing de sexta, e o cabo caiu mesmo assim. O CPI de outubro (3,6%, em linha) e os salários vieram suaves, e Bailey disse na quarta que o pico da inflação deve ficar abaixo dos 5% projetados. A Bank Rate está em 4,00%. A segunda traz o PMI flash de novembro às 09:30 UTC (outubro: composto 52,9, serviços 52,8) e Pill às 13:00 UTC. O piso de 1,5σ20 é de 70 pips, então o stop que paga o piso já volta para cima de 1.3160. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (1,3406) e sob a SMA50 (1,3310), com a SMA50 abaixo da SMA200 — alinhamento de baixa. O fechamento de sexta é a mínima de 10/20 pregões e de 9 meses. A máxima de 10 pregões é 1,3423 (10/11). A de 20 pregões segue 1,3500 (04/11).",
        "support": "1.3100 (o próximo redondo, 25 pips abaixo) e 1.3000 (125 pips). O fechamento de 20/11 (1,3125) é a mínima de 9 meses.",
        "resistance": "1.3160 (a mínima antiga, 35 pips acima) e 1,3310 (a SMA50).",
        "priceAction": "O varejo bateu o consenso na sexta e o cabo perdeu 1.3160 mesmo assim. O stop legal volta para cima do rompimento. Segunda tem PMI e Pill. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "O fechamento sob 1,3160 saiu na sexta, sem confirmação. 35 pips de volta até o extremo são menos que o piso de 70. Sem gatilho novo — reavaliar depois do PMI de segunda e do PCE de quarta.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "A libra fez nova mínima de 9 meses no dia do varejo forte. O rompimento é de uma sessão e o piso não cabe."
    },
    en={
        "fundamental": "Sunday 22/11/2026 edition, on the Friday 20/11/2026 ECB/Frankfurter reference rate (no weekend fixing): GBP/USD closed Friday at 1.3125, down -0.20% (-27 pips) from 1.3151. It is the new 10/20-day and 9-month low, 35 pips through 1.3160. UK October retail sales rose 0.7% on the month (0.0% consensus, September revised to -0.6%), with the year at 2.3% (ONS, Nov 20, 07:00 UTC) — it is in Friday's fixing, and cable fell anyway. October CPI (3.6%, in line) and pay came in soft, and Bailey said on Wednesday the inflation peak should land below the projected 5%. Bank Rate is 4.00%. Monday brings the November flash PMI at 09:30 UTC (October: composite 52.9, services 52.8) and Pill at 13:00 UTC. The 1.5-sigma20 floor is 70 pips, so the stop that meets the floor is already back above 1.3160. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (1.3406) and under the SMA50 (1.3310), with the SMA50 below the SMA200 — bear alignment. Friday's close is the 10/20-day and 9-month low. The 10-day high is 1.3423 (Nov 10). The 20-day high is still 1.3500 (Nov 4).",
        "support": "1.3100 (the next round, 25 pips below) and 1.3000 (125 pips). The Nov-20 close (1.3125) is the 9-month low.",
        "resistance": "1.3160 (the prior low, 35 pips above) and 1.3310 (the SMA50).",
        "priceAction": "Retail beat the consensus on Friday and cable lost 1.3160 anyway. The legal stop lands back above the breakdown. PMI and Pill are Monday. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The close under 1.3160 printed on Friday, unconfirmed. 35 pips back up to the extreme is less than the 70-pip floor. No new trigger — reassess after Monday's PMI and Wednesday's PCE.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "Sterling made a new 9-month low on the day of strong retail. The breakdown is one session old and the floor does not fit."
    })

EURJPY = pair("174.35", "BAIXA", "bear",
    pt={
        "fundamental": "Edição de domingo 22/11/2026, sobre a taxa de referência BCE/Frankfurter de sexta 20/11/2026 (sem pregão no fim de semana): o EUR/JPY fechou a sexta em 174,35, caindo -0,85% (-149 pips) a partir de 175,84. Quinta devolveu 175,00; sexta perdeu de novo e fez a nova mínima de 10/20 pregões e de 9 meses. O CPI do Japão veio abaixo do esperado nas três medidas, mas o iene firmou e a alta do BoJ em dezembro segue na mesa (86% dos economistas veem 1,50% em 17-18/12). O próximo redondo, 174,00, está a 35 pips. O aviso do MoF de 12-13/11 mantém o piso em 2,5σ20, aqui 188 pips, então o stop que paga o piso já atravessa 174,00 e cai perto de 173,00. A quinta traz a ata do BCE e o CPI de Tóquio, com os EUA no Thanksgiving. A SMA50 está em 177,45 e a SMA200 em 182,68. Alinhamento de baixa. O BCE decide em 17/12 (≈96% para +25 pb, a 2,75%). Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (182,68) com a SMA50 (177,45) abaixo dela — alinhamento de baixa pleno. O fechamento de sexta é a mínima de 10/20 pregões e de 9 meses. A máxima de 10 pregões está em 177,38 (10/11).",
        "support": "174.00 (o próximo redondo, 35 pips abaixo) e 173.00 (135 pips). O fechamento de 20/11 (174,35) é a nova mínima de 9 meses.",
        "resistance": "174.85 (a mínima de quarta, 51 pips acima) e 175,00, com a SMA50 em 177,45.",
        "priceAction": "Devolveu 175 na quinta e perdeu tudo na sexta, parando 35 pips antes de 174,00. O piso é 188. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "O fechamento sob 175,00 saiu de novo na sexta. 35 pips até 174,00 são menos que o piso de 188. Sem gatilho novo — reavaliar depois da ata do BCE e do CPI de Tóquio de quinta.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O cruzado fez nova mínima de 9 meses no dia do CPI. O próximo redondo continua dentro do piso de 188 pips."
    },
    en={
        "fundamental": "Sunday 22/11/2026 edition, on the Friday 20/11/2026 ECB/Frankfurter reference rate (no weekend fixing): EUR/JPY closed Friday at 174.35, down -0.85% (-149 pips) from 175.84. Thursday handed 175.00 back; Friday lost it again and made the new 10/20-day and 9-month low. Japan's CPI came in below expectations on all three measures, but the yen firmed and the December BoJ hike stays on the table (86% of economists see 1.50% on Dec 17-18). The next round, 174.00, is 35 pips away. The MoF warning of Nov 12-13 keeps the floor at 2.5-sigma20, here 188 pips, so the stop that meets the floor is already through 174.00 and lands near 173.00. Thursday brings the ECB minutes and Tokyo CPI, with the US on Thanksgiving. The SMA50 is at 177.45 and the SMA200 at 182.68. Bear alignment. The ECB decides on Dec 17 (≈96% for +25bp, to 2.75%). Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (182.68) with the SMA50 (177.45) below it — full bear alignment. Friday's close is the 10/20-day and 9-month low. The 10-day high is 177.38 (Nov 10).",
        "support": "174.00 (the next round, 35 pips below) and 173.00 (135 pips). The Nov-20 close (174.35) is the new 9-month low.",
        "resistance": "174.85 (Wednesday's low, 51 pips above) and 175.00, with the SMA50 at 177.45.",
        "priceAction": "It handed 175 back on Thursday and lost everything on Friday, stopping 35 pips short of 174.00. The floor is 188. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The close under 175.00 printed again on Friday. 35 pips down to 174.00 is less than the 188-pip floor. No new trigger — reassess after Thursday's ECB minutes and Tokyo CPI.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The cross made a new 9-month low on CPI day. The next round is still inside the 188-pip floor."
    })

GBPJPY = pair("208.21", "BAIXA", "bear",
    pt={
        "fundamental": "Edição de domingo 22/11/2026, sobre a taxa de referência BCE/Frankfurter de sexta 20/11/2026 (sem pregão no fim de semana): o GBP/JPY fechou a sexta em 208,21, caindo -1,03% (-217 pips) a partir de 210,38. É a nova mínima de 10/20 pregões, através de 209,61, de 209,00 e de 208,50. A mínima de 9 meses agora é 207,91 (09/09), a 30 pips. O varejo britânico forte e o CPI do Japão estão no fixing de sexta, e o cruzado caiu mesmo assim. A segunda traz o PMI flash do Reino Unido (09:30 UTC) e Pill (13:00 UTC); a quinta, o CPI de Tóquio com os EUA no Thanksgiving. O piso, ainda aberto pelo jawboning do MoF, é de 202 pips, então o stop que paga o piso já atravessa 207,91. BoE em 4,00%, BoJ em 1,25%. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (212,83) e sob a SMA50 (210,18), com a SMA50 sob a SMA200 — alinhamento de baixa pleno. O fechamento de sexta é a mínima de 10/20 pregões. A máxima de 10 pregões está em 212,32 (10/11).",
        "support": "207.91 (mínima de 9 meses, 30 pips abaixo). O fechamento de 20/11 (208,21) é a mínima de 10/20 pregões.",
        "resistance": "209.61 (a mínima antiga de 20 pregões, 140 pips acima) e 210,18 (a SMA50).",
        "priceAction": "Perdeu 209,61 na sexta e parou 30 pips antes de 207,91. O piso é 202. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "O fechamento sob 209,61 saiu na sexta. 30 pips até 207,91 são menos que o piso de 202. Sem gatilho novo — reavaliar depois do PMI de segunda e do CPI de Tóquio de quinta.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O cruzado andou 217 pips na sexta e a mínima de 9 meses ficou dentro do piso. Vender aqui atravessa o extremo."
    },
    en={
        "fundamental": "Sunday 22/11/2026 edition, on the Friday 20/11/2026 ECB/Frankfurter reference rate (no weekend fixing): GBP/JPY closed Friday at 208.21, down -1.03% (-217 pips) from 210.38. It is the new 10/20-day low, through 209.61, 209.00 and 208.50. The 9-month low is now 207.91 (Sep 9), 30 pips away. Strong UK retail and Japan's CPI are both in Friday's fixing, and the cross fell anyway. Monday brings the UK flash PMI (09:30 UTC) and Pill (13:00 UTC); Thursday, Tokyo CPI with the US on Thanksgiving. The floor, still open from the MoF jawboning, is 202 pips, so the stop that meets the floor is already through 207.91. BoE at 4.00%, BoJ at 1.25%. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (212.83) and under the SMA50 (210.18), with the SMA50 under the SMA200 — full bear alignment. Friday's close is the 10/20-day low. The 10-day high is 212.32 (Nov 10).",
        "support": "207.91 (the 9-month low, 30 pips below). The Nov-20 close (208.21) is the 10/20-day low.",
        "resistance": "209.61 (the prior 20-day low, 140 pips above) and 210.18 (the SMA50).",
        "priceAction": "It lost 209.61 on Friday and stopped 30 pips short of 207.91. The floor is 202. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The close under 209.61 printed on Friday. 30 pips down to 207.91 is less than the 202-pip floor. No new trigger — reassess after Monday's PMI and Thursday's Tokyo CPI.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The cross moved 217 pips on Friday and the 9-month low sits inside the floor. Selling here crosses the extreme."
    })

DATA = {
    "EUR/USD": EUR, "USD/JPY": USDJPY, "AUD/USD": AUD,
    "GBP/USD": GBP, "EUR/JPY": EURJPY, "GBP/JPY": GBPJPY,
}
DRIVERS = {
    "EUR/USD": {
        "en": ["Holds 1.0990 above the 9-month low", "PCE + GDP Wednesday, Thanksgiving Thu", "Fed Dec hike ~95%, ECB ~96%"],
        "pt": ["Segura 1,0990 acima da mín. de 9 meses", "PCE + PIB na quarta, Thanksgiving na quinta", "Alta do Fed ~95%, do BCE ~96%"],
    },
    "USD/JPY": {
        "en": ["158.64 under the SMA200, bear map", "Tokyo CPI Thu, Japan shut Mon", "Dec BoJ hike 86%, floor still 136"],
        "pt": ["158,64 sob a SMA200, mapa de baixa", "CPI de Tóquio na quinta, Japão fecha 2ª", "Alta do BoJ 86%, piso segue 136"],
    },
    "AUD/USD": {
        "en": ["9-month low 0.6666, floor is 49", "AU CPI Wed, ~4.7% eyed", "RBA at 4.85%, decides Dec 8"],
        "pt": ["Mín. de 9 meses 0,6666, piso é 49", "CPI da Austrália 4ª, ~4,7%", "RBA em 4,85%, decide 8/12"],
    },
    "GBP/USD": {
        "en": ["9-month low 1.3125, floor is 70", "UK flash PMI Mon + Pill 1pm UTC", "Bailey sees peak below 5%"],
        "pt": ["Mín. de 9 meses 1,3125, piso é 70", "PMI do Reino Unido 2ª + Pill às 13h", "Bailey vê pico abaixo de 5%"],
    },
    "EUR/JPY": {
        "en": ["9-month low 174.35, floor is 188", "ECB minutes Thu, Tokyo CPI Thu", "ECB + BoJ both decide mid-Dec"],
        "pt": ["Mín. de 9 meses 174,35, piso é 188", "Ata do BCE e CPI de Tóquio na 5ª", "BCE e BoJ decidem em dez"],
    },
    "GBP/JPY": {
        "en": ["10/20-day low 208.21, floor 202", "207.91 30 pips below", "UK PMI Mon, Tokyo CPI Thu"],
        "pt": ["Mín. de 10/20 pregões 208,21, piso 202", "207,91 30 pips abaixo", "PMI do RU 2ª, CPI de Tóquio 5ª"],
    },
}

NEWS_ITEM_JS = r'''                {
                    date: "22/11/2026",
                    category: "macro",
                    impact: "high",
                    pairs: ["EUR/USD", "USD/JPY", "AUD/USD", "GBP/USD", "EUR/JPY", "GBP/JPY"],
                    pt: {
                        headline: "Edição de domingo para a semana: as mínimas de sexta seguem de pé, e a muralha de quarta (PCE, PIB, CPI da Austrália) mantém os seis em AGUARDAR",
                        summary: "Edição de domingo 22/11/2026, sobre a taxa BCE/Frankfurter de sexta 20/11 — sem pregão no fim de semana, então os níveis são os de sexta. EUR/USD 1,0990 (−0,02%) segurou acima da mínima de 9 meses 1,0968, com o dólar em máxima de 19 meses (≈103,9 no DXY, quarto ganho semanal). USD/JPY 158,64 (−0,83%) segue sob a SMA200 (158,77) depois do CPI do Japão de outubro (cheio 2,3%, núcleo 2,2%, núcleo-núcleo 2,2%), com o aviso do MoF mantendo o piso em 136. AUD/USD 0,6666 (−0,68%) é a nova mínima de 9 meses, 34 pips através de 0.6700, depois do emprego (−43.500 vagas, desemprego 4,9%, máxima desde 2021); o CPI de outubro sai na quarta às 00:30 UTC (≈4,7% esperado vs 4,3% em setembro). GBP/USD 1,3125 (−0,20%) é a nova mínima de 9 meses, 35 pips através de 1.3160, mesmo com o varejo a +0,7%; o PMI flash do Reino Unido é segunda às 09:30 UTC, mais Pill às 13:00 UTC. EUR/JPY 174,35 (−0,85%) é a nova mínima de 9 meses, a 35 pips de 174,00, piso de 188. GBP/JPY 208,21 (−1,03%) é a nova mínima de 10/20 pregões, a 30 pips de 207,91, piso de 202. A muralha de quarta — 2ª leitura do PIB dos EUA do 3º tri (≈3,5% esperado), PCE de outubro (+0,3% no mês esperado), claims e Beige Book — mais o fechamento do Thanksgiving na quinta com ata do BCE e CPI de Tóquio, não deixa gatilho novo: os seis ficam em AGUARDAR. Fed 8-9/12 ≈95%, BCE 17/12 ≈96%, RBA e BoJ em dezembro.",
                        take: "Mesmos fechamentos, mesmo mapa: cada stop legal ainda atravessa o extremo que deveria proteger. A mesa fica de fora da muralha de dados e da liquidez fina do Thanksgiving."
                    },
                    en: {
                        headline: "Sunday week-ahead edition: Friday's lows stand, and Wednesday's PCE-GDP-AU-CPI wall keeps all six on WAIT",
                        summary: "Sunday 22/11/2026 edition, on the Friday 20/11 ECB/Frankfurter fixing — no weekend session, so the levels are Friday's. EUR/USD 1.0990 (−0.02%) held above the 9-month low 1.0968, with the dollar at a 19-month high (≈103.9 on the DXY, a fourth weekly gain). USD/JPY 158.64 (−0.83%) sits under the SMA200 (158.77) after Japan's October CPI (headline 2.3%, core 2.2%, core-core 2.2%), with the MoF warning keeping the floor at 136. AUD/USD 0.6666 (−0.68%) is the new 9-month low, 34 pips through 0.6700, after jobs (−43,500, jobless 4.9%, highest since 2021); October CPI lands Wednesday at 00:30 UTC (≈4.7% eyed vs 4.3% in September). GBP/USD 1.3125 (−0.20%) is the new 9-month low, 35 pips through 1.3160, even with retail at +0.7%; the UK flash PMI is Monday at 09:30 UTC, plus Pill at 13:00 UTC. EUR/JPY 174.35 (−0.85%) is the new 9-month low, 35 pips from 174.00, floor 188. GBP/JPY 208.21 (−1.03%) is the new 10/20-day low, 30 pips from 207.91, floor 202. Wednesday's wall — the US Q3 GDP second estimate (≈3.5% eyed), October PCE (+0.3% m/m eyed), claims and the Beige Book — plus Thursday's Thanksgiving shutdown with ECB minutes and Tokyo CPI, leaves no fresh trigger: all six stay on WAIT. Fed Dec 8-9 ≈95%, ECB Dec 17 ≈96%, RBA and BoJ in December.",
                        take: "Same closes, same map: every legal stop still crosses the extreme it is meant to protect. The desk sits out the data wall and Thanksgiving-thin liquidity."
                    }
                },
'''

NEWS_CARD = r'''                <!-- News 22/11/2026: Sunday week-ahead edition; Wednesday's data wall; all six WAIT -->
                <article class="news-card">
                    <div class="news-card-top">
                        <span class="news-cat"><span class="lang-en">Macro Data</span><span class="lang-pt" style="display:none;">Dados Macro</span></span>
                        <span class="impact-badge high"><span class="lang-en">High Impact</span><span class="lang-pt" style="display:none;">Impacto Alto</span></span>
                        <span class="news-date">22/11/2026</span>
                    </div>
                    <h2 class="news-title">
                        <span class="lang-en">Sunday week-ahead edition: Friday's lows stand, and Wednesday's PCE-GDP-AU-CPI wall keeps all six on WAIT</span>
                        <span class="lang-pt" style="display:none;">Edição de domingo para a semana: as mínimas de sexta seguem de pé, e a muralha de quarta (PCE, PIB, CPI da Austrália) mantém os seis em AGUARDAR</span>
                    </h2>
                    <p class="news-summary">
                        <span class="lang-en">Sunday 22/11/2026 edition, on the Friday 20/11 ECB/Frankfurter fixing — no weekend session, so the levels are Friday's. EUR/USD 1.0990 (−0.02%) held above the 9-month low 1.0968, with the dollar at a 19-month high (≈103.9 on the DXY, a fourth weekly gain). USD/JPY 158.64 (−0.83%) sits under the SMA200 (158.77) after Japan's October CPI (headline 2.3%, core 2.2%, core-core 2.2%), with the MoF warning keeping the floor at 136. AUD/USD 0.6666 (−0.68%) is the new 9-month low, 34 pips through 0.6700, after jobs (−43,500, jobless 4.9%, highest since 2021); October CPI lands Wednesday at 00:30 UTC (≈4.7% eyed vs 4.3% in September). GBP/USD 1.3125 (−0.20%) is the new 9-month low, 35 pips through 1.3160, even with retail at +0.7%; the UK flash PMI is Monday at 09:30 UTC, plus Pill at 13:00 UTC. EUR/JPY 174.35 (−0.85%) is the new 9-month low, 35 pips from 174.00, floor 188. GBP/JPY 208.21 (−1.03%) is the new 10/20-day low, 30 pips from 207.91, floor 202. Wednesday's wall — the US Q3 GDP second estimate (≈3.5% eyed), October PCE (+0.3% m/m eyed), claims and the Beige Book — plus Thursday's Thanksgiving shutdown with ECB minutes and Tokyo CPI, leaves no fresh trigger: all six stay on WAIT. Fed Dec 8-9 ≈95%, ECB Dec 17 ≈96%, RBA and BoJ in December.</span>
                        <span class="lang-pt" style="display:none;">Edição de domingo 22/11/2026, sobre a taxa BCE/Frankfurter de sexta 20/11 — sem pregão no fim de semana, então os níveis são os de sexta. EUR/USD 1,0990 (−0,02%) segurou acima da mínima de 9 meses 1,0968, com o dólar em máxima de 19 meses (≈103,9 no DXY, quarto ganho semanal). USD/JPY 158,64 (−0,83%) segue sob a SMA200 (158,77) depois do CPI do Japão de outubro (cheio 2,3%, núcleo 2,2%, núcleo-núcleo 2,2%), com o aviso do MoF mantendo o piso em 136. AUD/USD 0,6666 (−0,68%) é a nova mínima de 9 meses, 34 pips através de 0.6700, depois do emprego (−43.500 vagas, desemprego 4,9%, máxima desde 2021); o CPI de outubro sai na quarta às 00:30 UTC (≈4,7% esperado vs 4,3% em setembro). GBP/USD 1,3125 (−0,20%) é a nova mínima de 9 meses, 35 pips através de 1.3160, mesmo com o varejo a +0,7%; o PMI flash do Reino Unido é segunda às 09:30 UTC, mais Pill às 13:00 UTC. EUR/JPY 174,35 (−0,85%) é a nova mínima de 9 meses, a 35 pips de 174,00, piso de 188. GBP/JPY 208,21 (−1,03%) é a nova mínima de 10/20 pregões, a 30 pips de 207,91, piso de 202. A muralha de quarta — 2ª leitura do PIB dos EUA do 3º tri (≈3,5% esperado), PCE de outubro (+0,3% no mês esperado), claims e Beige Book — mais o fechamento do Thanksgiving na quinta com ata do BCE e CPI de Tóquio, não deixa gatilho novo: os seis ficam em AGUARDAR. Fed 8-9/12 ≈95%, BCE 17/12 ≈96%, RBA e BoJ em dezembro.</span>
                    </p>
                    <div class="news-take">
                        <span class="take-tag"><span class="lang-en">Desk take</span><span class="lang-pt" style="display:none;">Leitura da mesa</span></span>
                        <span class="lang-en">Same closes, same map: every legal stop still crosses the extreme it is meant to protect. The desk sits out the data wall and Thanksgiving-thin liquidity.</span>
                        <span class="lang-pt" style="display:none;">Mesmos fechamentos, mesmo mapa: cada stop legal ainda atravessa o extremo que deveria proteger. A mesa fica de fora da muralha de dados e da liquidez fina do Thanksgiving.</span>
                    </div>
                    <div class="news-pairs">
                        <span class="np-label"><span class="lang-en">Watch</span><span class="lang-pt" style="display:none;">Acompanhar</span></span>
                        <a href="eur-usd.html" class="pair-link-chip">EUR/USD</a><a href="usd-jpy.html" class="pair-link-chip">USD/JPY</a><a href="aud-usd.html" class="pair-link-chip">AUD/USD</a><a href="gbp-usd.html" class="pair-link-chip">GBP/USD</a><a href="eur-jpy.html" class="pair-link-chip">EUR/JPY</a><a href="gbp-jpy.html" class="pair-link-chip">GBP/JPY</a>
                    </div>
                </article>

'''

NEW_CAL = '''                <div class="cal-cell">
                    <span class="cal-date">23/11</span>
                    <span class="cal-event"><span class="lang-en">Flash PMIs (EZ, UK, US) + Pill 13:00 UTC</span><span class="lang-pt" style="display:none;">PMIs flash (ZE, RU, EUA) + Pill 13:00 UTC</span></span>
                    <div class="cal-meta"><span class="cal-impact med" aria-hidden="true"></span><span class="cal-cur">GBP</span></div>
                </div>
                <div class="cal-cell">
                    <span class="cal-date">25/11</span>
                    <span class="cal-event"><span class="lang-en">US PCE + Q3 GDP + claims + Beige Book</span><span class="lang-pt" style="display:none;">PCE + PIB 3º tri + claims + Beige Book dos EUA</span></span>
                    <div class="cal-meta"><span class="cal-impact high" aria-hidden="true"></span><span class="cal-cur">USD</span></div>
                </div>
                <div class="cal-cell">
                    <span class="cal-date">25/11</span>
                    <span class="cal-event"><span class="lang-en">Australia Oct CPI 00:30 UTC, ≈4.7% eyed</span><span class="lang-pt" style="display:none;">CPI da Austrália de out 00:30 UTC, ≈4,7% esperado</span></span>
                    <div class="cal-meta"><span class="cal-impact high" aria-hidden="true"></span><span class="cal-cur">AUD</span></div>
                </div>
                <div class="cal-cell">
                    <span class="cal-date">26/11</span>
                    <span class="cal-event"><span class="lang-en">Thanksgiving (US shut) · ECB minutes · Tokyo CPI</span><span class="lang-pt" style="display:none;">Thanksgiving (EUA fechados) · ata do BCE · CPI de Tóquio</span></span>
                    <div class="cal-meta"><span class="cal-impact high" aria-hidden="true"></span><span class="cal-cur">EUR</span></div>
                </div>'''

def main():
    print("STAMP", TS)
    with open(INDEX, encoding="utf-8") as f:
        idx = f.read()
    if idx.count(OLD_TS) != 4:
        raise SystemExit("expected 4 old timestamps, found %d" % idx.count(OLD_TS))
    idx = idx.replace(OLD_TS, TS)
    # Data basis unchanged: still the Friday 20/11 fixing (590 sessions) — no weekend session.
    idx = idx.replace(
        'nextEvent: "Japan CPI 2.2% · three new 9-month lows · Thanksgiving week"',
        'nextEvent: "PCE + GDP Wednesday · AU CPI · Thanksgiving Thursday"')
    idx = idx.replace(
        'nextEvent: "CPI do Japão 2,2% · três novas mínimas de 9 meses · semana de Thanksgiving"',
        'nextEvent: "PCE + PIB na quarta · CPI da Austrália · Thanksgiving na quinta"')

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
    ledger["meta"]["lastUpdated"] = "22/11/2026"
    with open(LEDGER, "w", encoding="utf-8", newline="\n") as f:
        json.dump(ledger, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("ledger lastUpdated only; book still empty")

    with open(NEWS, encoding="utf-8") as f:
        news = f.read()
    news = news.replace(
        "Market Wire · The Yen Turns, Three New Lows, Still No Ticket",
        "Market Wire · Week-Ahead Edition: Wednesday's Data Wall, Still No Ticket")
    news = news.replace(
        "Telégrafo da Mesa · O Iene Vira, Três Novas Mínimas, Ainda Sem Ticket",
        "Telégrafo da Mesa · Edição da Semana: Muralha de Dados na Quarta, Ainda Sem Ticket")
    news = news.replace(OLD_TS, TS)
    news = news.replace(
        "6 pairs · Japan CPI 2.2% · AU jobs miss · Thanksgiving week",
        "6 pairs · Friday's lows stand · PCE + GDP + AU CPI Wednesday")
    news = news.replace(
        "6 pares · CPI do Japão 2,2% · emprego da Austrália erra · semana de Thanksgiving",
        "6 pares · mínimas de sexta mantidas · PCE + PIB + CPI da Austrália na quarta")
    start = news.find('                <div class="cal-cell">')
    end = news.find("            </div>\n        </section>", start)
    if start < 0 or end < 0:
        raise SystemExit("calendar block missing")
    news = news[:start] + NEW_CAL + "\n" + news[end:]
    marker = "                <!-- News 20/11/2026:"
    if marker not in news:
        raise SystemExit("news marker missing")
    news = news.replace(marker, NEWS_CARD + marker, 1)
    with open(NEWS, "w", encoding="utf-8", newline="\n") as f:
        f.write(news)
    print("news.html patched")

    with open(SITEMAP, encoding="utf-8") as f:
        sm = f.read()
    n = sm.count("2026-11-20")
    if n != 9:
        raise SystemExit("expected 9 sitemap dates, found %d" % n)
    sm = sm.replace("2026-11-20", "2026-11-22")
    with open(SITEMAP, "w", encoding="utf-8", newline="\n") as f:
        f.write(sm)
    print("sitemap patched")

    with open(VERIFY, encoding="utf-8") as f:
        v = f.read()
    v = v.replace('TODAY_TS = "20/11/2026 20:52 UTC"', 'TODAY_TS = "%s"' % TS)
    v = v.replace(
        'TODAY_DATE = "20/11/2026"  # basis session date (report edition: 20/11/2026)',
        'TODAY_DATE = "22/11/2026"  # report edition: 22/11/2026, on the 20/11/2026 basis session')
    # Ticker unchanged: same Friday daily moves (no weekend session).
    with open(VERIFY, "w", encoding="utf-8", newline="\n") as f:
        f.write(v)
    print("verify constants patched")

if __name__ == "__main__":
    main()
