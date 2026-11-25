#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""25/11/2026 Wednesday edition, on the 25/11 ECB fixing (593 sessions).

The wall landed hot on both fronts: Q3 GDP revised to 4.3% (3.4% advance,
3.5% eyed) and October PCE at 3.8% headline / 3.3% core (3.2% eyed) — the
fixing, published after the 13:30 UTC data, already holds the dollar's
answer (DXY ≈104.1). EUR/USD, AUD/USD and GBP/USD printed new 9-month
lows; USD/JPY closed a third session back above the SMA200 (map MIXED
again → NEUTRAL); EUR/JPY and GBP/JPY held just above their lows. AU CPI
beat (4.9% vs 4.8%) but the Aussie crashed 72 pips anyway. Every breakdown
is one session old, every legal stop crosses its extreme, and the next
24h belong to the ECB minutes + Tokyo CPI + Thanksgiving: all six WAIT.
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
OLD_TS = "22/11/2026 10:50 UTC"
BASIS = "593 sessions, 01/08/2024 to 25/11/2026"
BASIS_PT = "593 pregões, 01/08/2024 a 25/11/2026"

def pair(quote, bias, bias_type, pt, en):
    return {"quote": quote, "bias": bias, "biasType": bias_type, "pt": pt, "en": en}

EUR = pair("1.0935", "BAIXA", "bear",
    pt={
        "fundamental": "Edição de quarta 25/11/2026, sobre a taxa de referência BCE/Frankfurter de 25/11/2026: o EUR/USD fechou em 1,0935, caindo -0,25% (-28 pips) a partir de 1,0963. É a nova mínima de 10/20 pregões e de 9 meses, 33 pips através da anterior 1,0968 (18/11) e 15 pips sob o redondo 1.0950. A muralha veio quente nas duas frentes: o PIB do 3º tri revisto a 4,3% (prévia 3,4%, esperado 3,5%, 2º tri 2,2%), o mais forte em três anos, com investimento, consumo e gasto público; o PCE de outubro em 3,8% no cheio como esperado, com o núcleo em 3,3% (esperado 3,2%, setembro 3,1%) e +0,3% no mês em linha (BEA, 13:30 UTC) — e o fixing, publicado depois dos dados, mostra a resposta do dólar: ≈104,1 no DXY (+0,2% a 104,06, Reuters), de volta à máxima de 19 meses de segunda perto de 104,5. Os PMIs flash de segunda dividiram suaves nos serviços: composto da zona do euro em 51,7 inalterado (indústria 52,9 batendo, serviços 51,2 na mínima de cinco meses), composto dos EUA em 54,6 (outubro 55,9, mínima de quatro meses). O Fed segue em 3,75-4,00% com a alta de 8-9/12 a ≈96%; quinta é Thanksgiving (EUA fechados) com a ata do BCE, sexta traz os CPIs flash de França e Espanha, e o payroll sai em 4/12. O BCE decide em 17/12 com o depósito em 2,50% e +25 pb a ≈96% (inflação de outubro final 4,0%, núcleo revisto a 2,6%). O piso de 1,5σ20 é de 63 pips. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (1,1493) com a SMA50 (1,1202) abaixo dela — alinhamento de baixa pleno. O fechamento de hoje é a mínima de 10/20 pregões e de 9 meses. A máxima de 10 pregões é 1,1081 (12/11). A de 20 pregões segue 1,1267 (04/11).",
        "support": "1.0900 (o próximo redondo, 35 pips abaixo). O fechamento de 25/11 (1,0935) é a mínima de 9 meses.",
        "resistance": "1.0950 (o redondo recém-perdido, 15 pips acima) e 1,0968 (a mínima anterior de 9 meses), com a SMA50 em 1,1202.",
        "priceAction": "A muralha quente imprimiu nova mínima de 9 meses, 33 pips através de 1,0968, e o fixing já carrega a resposta do dólar. 1.0900 está 35 pips abaixo, dentro do piso de 63. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "O rompimento sob 1,0968 saiu hoje, sem confirmação — o gatilho pede um segundo fechamento sob 1,0935, e não pode disparar antes da ata do BCE de quinta. Sem gatilho novo — reavaliar depois da ata, na liquidez fina do Thanksgiving.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O dólar mereceu o rompimento no PIB quente e no núcleo pegajoso. Mas o rompimento tem uma sessão, a ata do BCE cai dentro de 24 horas, e o stop legal já volta para cima de 1,0968."
    },
    en={
        "fundamental": "Wednesday 25/11/2026 edition, on the 25/11/2026 ECB/Frankfurter reference rate: EUR/USD closed at 1.0935, down -0.25% (-28 pips) from 1.0963. It is the new 10/20-day and 9-month low, 33 pips through the prior 1.0968 (Nov 18) and 15 pips under the 1.0950 round. The wall landed hot on both fronts: Q3 GDP revised to 4.3% (3.4% advance, 3.5% eyed, Q2 2.2%), the strongest in three years on investment, consumption and government spending; October PCE printed 3.8% headline as expected with core at 3.3% (3.2% eyed, September 3.1%) and +0.3% m/m in line (BEA, 13:30 UTC) — and the fixing, published after the data, shows the dollar's answer: ≈104.1 on the DXY (+0.2% to 104.06, Reuters), back toward Monday's 19-month high near 104.5. Monday's flash PMIs split soft on services: eurozone composite 51.7 unchanged (manufacturing 52.9 beat, services 51.2 a five-month low), US composite 54.6 (October 55.9, a four-month low). The Fed is still at 3.75-4.00% with the Dec 8-9 hike at ≈96%; Thursday is Thanksgiving (US shut) with the ECB minutes, Friday brings French and Spanish flash CPI, and payrolls land Dec 4. The ECB decides Dec 17 with the deposit rate at 2.50% and +25bp at ≈96% (October inflation final 4.0%, core revised up to 2.6%). The 1.5-sigma20 floor is 63 pips. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (1.1493) with the SMA50 (1.1202) below it — full bear alignment. Today's close is the 10/20-day and 9-month low. The 10-day high is 1.1081 (Nov 12). The 20-day high is still 1.1267 (Nov 4).",
        "support": "1.0900 (the next round, 35 pips below). The Nov-25 close (1.0935) is the 9-month low.",
        "resistance": "1.0950 (the round just lost, 15 pips above) and 1.0968 (the prior 9-month low), with the SMA50 at 1.1202.",
        "priceAction": "The hot wall printed a fresh 9-month low, 33 pips through 1.0968, and the fixing already holds the dollar's answer. 1.0900 is 35 pips below, inside the 63-pip floor. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The breakdown under 1.0968 printed today, unconfirmed — the trigger needs a second daily close under 1.0935, and it cannot fire before Thursday's ECB minutes clear. No new trigger — reassess after the minutes, on Thanksgiving-thin tape.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The dollar earned the breakdown on hot GDP and sticky core PCE. But the breakdown is one session old, the ECB minutes land inside 24 hours, and the legal stop already reaches back above 1.0968."
    })

USDJPY = pair("159.32", "NEUTRO", "neutral",
    pt={
        "fundamental": "Edição de quarta 25/11/2026, sobre a taxa de referência BCE/Frankfurter de 25/11/2026: o USD/JPY fechou em 159,32, subindo +0,16% (+25 pips) a partir de 159,07. É o terceiro fechamento seguido de volta acima da SMA200 (158,85) — 47 pips acima dela — depois do mergulho de sexta no CPI do Japão: com a SMA50 (158,17) ainda abaixo da SMA200, o mapa voltou a MISTO, nem alta nem baixa. 160,00, a máxima de 10/20 pregões, trava todo fechamento desde 13/11 sob os avisos do MoF de 12-13/11 (Katayama: movimentos 'unilaterais e rápidos', em contato com o Tesouro dos EUA; Mimura; Takaichi) — ainda dentro de 30 dias, sem intervenção confirmada — então o piso segue em 2,5σ20: 134 pips. O par está encaixotado: a alta do Fed em 8-9/12 a ≈96% sustenta o dólar enquanto a alta do BoJ a 1,50% em 17-18/12 a ≈86% (BoJ em 1,25%) sustenta o iene, e o diferencial segue parado. O CPI de Tóquio de novembro sai na quinta às 23:30 UTC (cheio esperado 3,1% vs 2,8% em outubro, núcleo 2,9% vs 2,6%), com os EUA no Thanksgiving. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento acima da SMA200 (158,85) com a SMA50 (158,17) abaixo dela — MISTO, sem alinhamento; a virada de baixa de sexta durou uma sessão. A máxima de 10/20 pregões segue 160,00 (13/11). A mínima de 10 pregões é 158,64 (20/11); a de 20, 157,25 (30/10). O intervalo de 9 meses segue 163,91/153,27.",
        "support": "158.85 (a SMA200, retomada por 47 pips) e 158,64 (a mínima de 10 pregões, 68 pips abaixo).",
        "resistance": "160.00 (a máxima de 10/20 pregões, 68 pips acima, travando desde 13/11).",
        "priceAction": "Três fechamentos de volta acima da SMA200, mas 160,00 trava o topo e o CPI de Tóquio cai em menos de 24 horas. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "Nenhum rompimento impresso para nenhum lado: 160,00 trava o topo, 158,64 segura o fundo. O mapa misto pede um fechamento além de um deles — depois do CPI de Tóquio e do Thanksgiving. Sem gatilho.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O mergulho do iene no CPI já falhou e o mapa é misto por definição. Comprar a trava antes do CPI de Tóquio, ou vender a SMA200 retomada, brigam com o manual."
    },
    en={
        "fundamental": "Wednesday 25/11/2026 edition, on the 25/11/2026 ECB/Frankfurter reference rate: USD/JPY closed at 159.32, up +0.16% (+25 pips) from 159.07. It is the third straight close back above the SMA200 (158.85) — 47 pips above it — after Friday's dip under on Japan CPI: with the SMA50 (158.17) still below the SMA200, the map is MIXED again, neither bull nor bear. 160.00, the 10/20-day high, has capped every close since Nov 13 under the MoF's Nov 12-13 warnings (Katayama: 'one-sided, rapid moves', in contact with the US Treasury; Mimura; Takaichi) — still inside 30 days, no confirmed intervention — so the floor stays at 2.5-sigma20: 134 pips. The pair is boxed: a ≈96%-priced Fed hike on Dec 8-9 supports the dollar while an ≈86%-priced BoJ hike to 1.50% on Dec 17-18 (BoJ at 1.25%) supports the yen, and the rate gap holds. November Tokyo CPI lands Thursday at 23:30 UTC (headline 3.1% eyed vs 2.8% in October, core 2.9% vs 2.6%), with the US on Thanksgiving. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close above the SMA200 (158.85) with the SMA50 (158.17) below it — MIXED, neither alignment; Friday's bear flip lasted one session. The 10/20-day high is still 160.00 (Nov 13). The 10-day low is 158.64 (Nov 20); the 20-day low, 157.25 (Oct 30). The 9-month range is still 163.91/153.27.",
        "support": "158.85 (the SMA200, reclaimed by 47 pips) and 158.64 (the 10-day low, 68 pips below).",
        "resistance": "160.00 (the 10/20-day high, 68 pips above, capped since Nov 13).",
        "priceAction": "Three closes back above the SMA200, but 160.00 caps the top and Tokyo CPI lands in under 24 hours. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "No breakout has printed either way: 160.00 caps the top, 158.64 holds the bottom. The mixed map needs a daily close beyond one of them — after Tokyo CPI and Thanksgiving. No trigger.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The yen's CPI dip already failed and the map is mixed by definition. Buying the cap into Tokyo CPI, or selling the reclaimed SMA200, both fight the rulebook."
    })

AUD = pair("0.6570", "BAIXA", "bear",
    pt={
        "fundamental": "Edição de quarta 25/11/2026, sobre a taxa de referência BCE/Frankfurter de 25/11/2026: o AUD/USD fechou em 0,6570, caindo -1,08% (-72 pips) a partir de 0,6641 — o maior movimento do dia. É a nova mínima de 10/20 pregões e de 9 meses, 96 pips através da anterior 0,6666 (20/11) e 30 pips sob o redondo 0.6600. O CPI de outubro bateu em todas as linhas — cheio 4,9% (esperado 4,8%, setembro 4,3%), máxima desde 2023, núcleo aparado 3,8% (esperado 3,6%), +0,5% no mês (ABS, 00:30 UTC) — e o Aussie saltou, para depois ser enterrado pela muralha quente dos EUA: o PIB a 4,3% e o núcleo do PCE a 3,3% reprecificaram o dólar contra tudo. O RBA está em 4,85% (3/11, 6-3, máxima em 18 anos) e decide em 8/12, com manutenção a ≈80-100% e a sexta alta perto de 9% — o mercado lê o CPI como já no preço depois de cinco altas em 2026, com o emprego em -43.500 vagas e 4,9% de desemprego. Os lucros industriais da China de outubro saem na quinta, com os EUA no Thanksgiving. O piso de 1,5σ20 é de 52 pips. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (0,7038) com a SMA50 (0,6938) abaixo dela — alinhamento de baixa pleno. O fechamento de hoje é a mínima de 10/20 pregões e de 9 meses. A máxima de 10 pregões é 0,6821 (12/11). A de 20 pregões segue 0,7025.",
        "support": "0.6500 (o próximo redondo, 70 pips abaixo). O fechamento de 25/11 (0,6570) é a mínima de 9 meses.",
        "resistance": "0.6600 (o redondo recém-perdido, 30 pips acima) e 0,6641 (o fechamento de terça).",
        "priceAction": "Cascata de 72 pips através de 0.6600 no dia em que o CPI bateu — a muralha do dólar atropelou o dado local. O stop legal volta para cima de 0.6600. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "O rompimento sob 0.6600 saiu hoje, sem confirmação — o gatilho pede um segundo fechamento sob 0,6570, e a fita de quinta é fina de Thanksgiving com dado da China. Sem gatilho novo — reavaliar depois do feriado.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O Aussie fez a mínima do ano no dia em que seu próprio CPI bateu. Perseguir 72 pips num feriado dos EUA, com o stop de volta acima do rompimento, não é ticket."
    },
    en={
        "fundamental": "Wednesday 25/11/2026 edition, on the 25/11/2026 ECB/Frankfurter reference rate: AUD/USD closed at 0.6570, down -1.08% (-72 pips) from 0.6641 — the day's biggest mover. It is the new 10/20-day and 9-month low, 96 pips through the prior 0.6666 (Nov 20) and 30 pips under the 0.6600 round. October CPI beat on every line — headline 4.9% (4.8% eyed, September 4.3%), the highest since 2023, trimmed mean 3.8% (3.6% eyed), +0.5% m/m (ABS, 00:30 UTC) — and the Aussie jumped, then got buried by the hot US wall: GDP at 4.3% and core PCE at 3.3% re-priced the dollar against everything. The RBA is at 4.85% (Nov 3, 6-3, an 18-year high) and decides Dec 8, with a hold at ≈80-100% and a sixth hike near 9% — the market reads the CPI beat as already in the price after five 2026 hikes, with jobs at -43,500 and 4.9% jobless. China's October industrial profits land Thursday, with the US on Thanksgiving. The 1.5-sigma20 floor is 52 pips. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (0.7038) with the SMA50 (0.6938) below it — full bear alignment. Today's close is the 10/20-day and 9-month low. The 10-day high is 0.6821 (Nov 12). The 20-day high is still 0.7025.",
        "support": "0.6500 (the next round, 70 pips below). The Nov-25 close (0.6570) is the 9-month low.",
        "resistance": "0.6600 (the round just lost, 30 pips above) and 0.6641 (Tuesday's close).",
        "priceAction": "A 72-pip cascade through 0.6600 on the day CPI beat — the dollar wall overruled the local data. The legal stop lands back above 0.6600. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The breakdown under 0.6600 printed today, unconfirmed — the trigger needs a second daily close under 0.6570, and Thursday's tape is Thanksgiving-thin with China data due. No new trigger — reassess after the holiday.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The Aussie made the low of the year on a day its own CPI beat. Chasing 72 pips into a US holiday, with the stop back above the breakdown, is not a ticket."
    })

GBP = pair("1.3060", "BAIXA", "bear",
    pt={
        "fundamental": "Edição de quarta 25/11/2026, sobre a taxa de referência BCE/Frankfurter de 25/11/2026: o GBP/USD fechou em 1,3060, caindo -0,29% (-38 pips) a partir de 1,3098. É a nova mínima de 10/20 pregões e de 9 meses, 65 pips através da anterior 1,3125 (20/11) e 40 pips sob o redondo 1.3100. O PMI flash de segunda veio suave — composto 52,3 (outubro 52,9), serviços 52,0 (esperado 53,0, mínima de cinco meses) — e a muralha quente dos EUA (PIB 4,3%, núcleo do PCE 3,3%) fez o resto. O CPI de outubro (3,6%, em linha) e os salários suaves mantêm viva a decisão de dezembro do BoE: a Bank Rate está em 4,00% e o Banco decide em 17/12. Quinta traz o Relatório de Estabilidade Financeira do BoE com os EUA no Thanksgiving; sexta traz os CPIs flash de França e Espanha e fechamento antecipado nos EUA; o payroll sai em 4/12. O piso de 1,5σ20 é de 72 pips, então o stop que paga o piso volta para cima de 1.3100. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (1,3397) e sob a SMA50 (1,3286), com a SMA50 abaixo da SMA200 — alinhamento de baixa pleno. O fechamento de hoje é a mínima de 10/20 pregões e de 9 meses. A máxima de 10 pregões é 1,3256 (12/11). A de 20 pregões segue 1,3500 (04/11).",
        "support": "1.3000 (o figurão, 60 pips abaixo). O fechamento de 25/11 (1,3060) é a mínima de 9 meses.",
        "resistance": "1.3100 (o redondo recém-perdido, 40 pips acima) e 1,3125 (a mínima de sexta).",
        "priceAction": "PMI suave mais muralha quente imprimiram nova mínima de 9 meses. O figurão 1.3000 está 60 pips abaixo, dentro de qualquer caminho 1 para 2. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "O rompimento sob 1,3100 saiu hoje, sem confirmação — o gatilho pede um segundo fechamento sob 1,3060, depois do FSR e do Thanksgiving. Sem gatilho novo — reavaliar depois do feriado.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "A libra rompeu com todo o bloco do dólar. Mas o rompimento tem uma sessão, 1.3000 bloqueia o caminho 1 para 2, e o FSR mais o Thanksgiving dominam as próximas 24 horas."
    },
    en={
        "fundamental": "Wednesday 25/11/2026 edition, on the 25/11/2026 ECB/Frankfurter reference rate: GBP/USD closed at 1.3060, down -0.29% (-38 pips) from 1.3098. It is the new 10/20-day and 9-month low, 65 pips through the prior 1.3125 (Nov 20) and 40 pips under the 1.3100 round. Monday's flash PMI leaned soft — composite 52.3 (October 52.9), services 52.0 (53.0 eyed, a five-month low) — and then the hot US wall (GDP 4.3%, core PCE 3.3%) did the rest. October CPI (3.6%, in line) and soft pay keep the BoE's December decision live: Bank Rate is 4.00% and the Bank decides Dec 17. Thursday brings the BoE Financial Stability Report with the US on Thanksgiving; Friday brings French and Spanish flash CPI and a US early close; payrolls land Dec 4. The 1.5-sigma20 floor is 72 pips, so the stop that meets the floor reaches back above 1.3100. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (1.3397) and under the SMA50 (1.3286), with the SMA50 below the SMA200 — full bear alignment. Today's close is the 10/20-day and 9-month low. The 10-day high is 1.3256 (Nov 12). The 20-day high is still 1.3500 (Nov 4).",
        "support": "1.3000 (the big figure, 60 pips below). The Nov-25 close (1.3060) is the 9-month low.",
        "resistance": "1.3100 (the round just lost, 40 pips above) and 1.3125 (Friday's low).",
        "priceAction": "Soft PMI plus the hot US wall printed a fresh 9-month low. The big 1.3000 figure sits 60 pips below, inside any 1:2 path. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The breakdown under 1.3100 printed today, unconfirmed — the trigger needs a second daily close under 1.3060, past the FSR and Thanksgiving. No new trigger — reassess after the holiday.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "Sterling broke with the whole dollar bloc. But the breakdown is one session old, 1.3000 blocks the 1:2 path, and the FSR plus Thanksgiving own the next 24 hours."
    })

EURJPY = pair("174.22", "BAIXA", "bear",
    pt={
        "fundamental": "Edição de quarta 25/11/2026, sobre a taxa de referência BCE/Frankfurter de 25/11/2026: o EUR/JPY fechou em 174,22, caindo -0,10% (-17 pips) a partir de 174,39. Segura 21 pips acima da mínima de 9 meses de 174,01 (23/11) e 22 pips acima do redondo 174,00 — o mais quieto dos seis no dia da muralha, com a fraqueza do euro e a firmeza do iene se anulando. Os dois lados do cruzado encaram eventos top dentro de 24 horas: a ata do BCE na quinta, e o CPI de Tóquio de novembro às 23:30 UTC (cheio esperado 3,1% vs 2,8%, núcleo 2,9% vs 2,6%), com os EUA no Thanksgiving. O aviso do MoF de 12-13/11 mantém o piso em 2,5σ20: 186 pips — qualquer stop legal já atravessa 175,00 rumo a 176,00. O BCE decide em 17/12 (≈96% para +25 pb a 2,75%, inflação de outubro final 4,0%); o BoJ decide em 17-18/12 (≈86% para +25 pb a 1,50%, em 1,25%). A SMA50 está em 177,18 e a SMA200 em 182,56. Alinhamento de baixa. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (182,56) com a SMA50 (177,18) abaixo dela — alinhamento de baixa pleno. A mínima de 10/20 pregões e de 9 meses é 174,01 (23/11), 21 pips abaixo. A máxima de 10 pregões é 176,96 (12/11).",
        "support": "174.01 (a mínima de 10/20 pregões e de 9 meses, 21 pips abaixo) e 174,00.",
        "resistance": "175.00 (o redondo, 78 pips acima), com a SMA50 em 177,18.",
        "priceAction": "Dezessete pips no dia da muralha — o cruzado ficou de fora dos fogos 21 pips acima da mínima. Os dois calendários disparam dentro de 24 horas. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "Nenhum rompimento impresso: 174,01 segurou pela segunda sessão. A ata do BCE e o CPI de Tóquio caem dentro de 24 horas. Sem gatilho — reavaliar depois que os dois passarem.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O cruzado está preso 21 pips acima da mínima com dois eventos de banco central dentro de um dia. Não há gatilho que sobreviva aos dois."
    },
    en={
        "fundamental": "Wednesday 25/11/2026 edition, on the 25/11/2026 ECB/Frankfurter reference rate: EUR/JPY closed at 174.22, down -0.10% (-17 pips) from 174.39. It holds 21 pips above the 9-month low of 174.01 (Nov 23) and 22 pips above the 174.00 round — the quietest of the six on wall day, with euro softness and yen firmness cancelling out. Both sides of the cross face top-tier events inside 24 hours: the ECB minutes on Thursday, and November Tokyo CPI at 23:30 UTC (headline 3.1% eyed vs 2.8%, core 2.9% vs 2.6%), with the US on Thanksgiving. The MoF's Nov 12-13 warning keeps the floor at 2.5-sigma20: 186 pips — any legal stop is already through 175.00 and toward 176.00. The ECB decides Dec 17 (≈96% for +25bp to 2.75%, October inflation final 4.0%); the BoJ decides Dec 17-18 (≈86% for +25bp to 1.50%, at 1.25%). The SMA50 is at 177.18 and the SMA200 at 182.56. Bear alignment. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (182.56) with the SMA50 (177.18) below it — full bear alignment. The 10/20-day and 9-month low is 174.01 (Nov 23), 21 pips below. The 10-day high is 176.96 (Nov 12).",
        "support": "174.01 (the 10/20-day and 9-month low, 21 pips below) and 174.00.",
        "resistance": "175.00 (the round, 78 pips above), with the SMA50 at 177.18.",
        "priceAction": "Seventeen pips on wall day — the cross sat out the fireworks 21 pips above its low. Both event calendars fire inside 24 hours. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "No breakdown has printed: 174.01 held for a second session. The ECB minutes and Tokyo CPI both land inside 24 hours. No trigger — reassess after both clear.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The cross is pinned 21 pips above its low with two central-bank events inside a day. There is no trigger that survives both."
    })

GBPJPY = pair("208.07", "BAIXA", "bear",
    pt={
        "fundamental": "Edição de quarta 25/11/2026, sobre a taxa de referência BCE/Frankfurter de 25/11/2026: o GBP/JPY fechou em 208,07, caindo -0,13% (-28 pips) a partir de 208,35. Segura 16 pips acima da mínima de 9 meses de 207,91 (09/09) — a margem mais apertada do painel — depois que os 207,96 de segunda imprimiram a nova mínima de 10/20 pregões. O PMI suave do Reino Unido (composto 52,3, serviços 52,0 errando) e a muralha quente dos EUA empurraram pelo lado da libra; o lado do iene espera o CPI de Tóquio de novembro às 23:30 UTC de quinta (cheio esperado 3,1% vs 2,8%, núcleo 2,9% vs 2,6%), com os EUA no Thanksgiving. O jawboning do MoF mantém o piso em 2,5σ20: 200 pips — o stop que paga já atravessa 209,00 rumo a 210,00. BoE em 4,00% (decide 17/12, FSR na quinta); BoJ em 1,25% (decide 17-18/12, ≈86% para 1,50%). Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (212,82) e sob a SMA50 (210,14), com a SMA50 sob a SMA200 — alinhamento de baixa pleno. O fechamento de segunda é a mínima de 10/20 pregões (207,96); a mínima de 9 meses é 207,91 (09/09), 16 pips abaixo. A máxima de 10 pregões é 211,69 (12/11).",
        "support": "207.91 (a mínima de 9 meses, 16 pips abaixo).",
        "resistance": "209.00 (o redondo, 93 pips acima) e 210,14 (a SMA50).",
        "priceAction": "Dezesseis pips acima da mínima de 9 meses antes do CPI de Tóquio — o ponto mais apertado do painel, com piso de 200. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "Nenhum rompimento impresso: 207,91 segurou de novo. O CPI de Tóquio cai dentro de 24 horas na fita fina do Thanksgiving. Sem gatilho — reavaliar depois do número.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O cruzado está 16 pips da mínima do ano com o CPI de Tóquio a horas. Qualquer stop legal cruza 209,00 — não há ticket hoje."
    },
    en={
        "fundamental": "Wednesday 25/11/2026 edition, on the 25/11/2026 ECB/Frankfurter reference rate: GBP/JPY closed at 208.07, down -0.13% (-28 pips) from 208.35. It holds 16 pips above the 9-month low of 207.91 (Sep 9) — the closest shave on the board — after Monday's 207.96 printed the new 10/20-day low. Soft UK PMI (composite 52.3, services 52.0 miss) and the hot US wall pushed from the sterling side; the yen side waits on November Tokyo CPI at 23:30 UTC Thursday (headline 3.1% eyed vs 2.8%, core 2.9% vs 2.6%), with the US on Thanksgiving. The MoF jawboning keeps the floor at 2.5-sigma20: 200 pips — the stop that meets it is already through 209.00 and toward 210.00. BoE at 4.00% (decides Dec 17, FSR Thursday); BoJ at 1.25% (decides Dec 17-18, ≈86% for 1.50%). Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (212.82) and under the SMA50 (210.14), with the SMA50 under the SMA200 — full bear alignment. Monday's close is the 10/20-day low (207.96); the 9-month low is 207.91 (Sep 9), 16 pips below. The 10-day high is 211.69 (Nov 12).",
        "support": "207.91 (the 9-month low, 16 pips below).",
        "resistance": "209.00 (the round, 93 pips above) and 210.14 (the SMA50).",
        "priceAction": "Sixteen pips above the 9-month low into Tokyo CPI — the tightest spot on the board, with a 200-pip floor. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "No breakdown has printed: 207.91 held again. Tokyo CPI lands inside 24 hours on Thanksgiving-thin tape. No trigger — reassess after the print.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The cross is 16 pips from the low of the year with Tokyo CPI hours away. Any legal stop crosses 209.00 — there is no ticket tonight."
    })

DATA = {
    "EUR/USD": EUR, "USD/JPY": USDJPY, "AUD/USD": AUD,
    "GBP/USD": GBP, "EUR/JPY": EURJPY, "GBP/JPY": GBPJPY,
}
DRIVERS = {
    "EUR/USD": {
        "en": ["9-month low 1.0935, floor is 63", "GDP 4.3% + core PCE 3.3% hot", "ECB minutes Thu, NFP Dec 4"],
        "pt": ["Mín. de 9 meses 1,0935, piso é 63", "PIB 4,3% + núcleo do PCE 3,3%", "Ata do BCE na 5ª, payroll 4/12"],
    },
    "USD/JPY": {
        "en": ["159.32 back over the SMA200, MIXED", "160.00 caps since Nov 13, floor 134", "Tokyo CPI Thu 23h30 UTC"],
        "pt": ["159,32 de volta sobre a SMA200, MISTO", "160,00 trava desde 13/11, piso 134", "CPI de Tóquio 5ª 23h30 UTC"],
    },
    "AUD/USD": {
        "en": ["9-month low 0.6570, -72 pips", "AU CPI 4.9% beat, dollar won", "China IP Thu, Thanksgiving tape"],
        "pt": ["Mín. de 9 meses 0,6570, -72 pips", "CPI 4,9% bateu, dólar venceu", "China 5ª, fita de feriado"],
    },
    "GBP/USD": {
        "en": ["9-month low 1.3060, floor is 72", "UK PMI soft, US wall hot", "BoE FSR Thu, NFP Dec 4"],
        "pt": ["Mín. de 9 meses 1,3060, piso é 72", "PMI suave, muralha quente", "FSR do BoE 5ª, payroll 4/12"],
    },
    "EUR/JPY": {
        "en": ["174.22, 21 pips over the low", "ECB minutes + Tokyo CPI <24h", "Floor 186, both sides boxed"],
        "pt": ["174,22, 21 pips sobre a mínima", "Ata do BCE + CPI Tóquio <24h", "Piso 186, cruzado encaixotado"],
    },
    "GBP/JPY": {
        "en": ["208.07, 16 pips over 207.91", "Tokyo CPI <24h, floor 200", "UK PMI soft, FSR Thu"],
        "pt": ["208,07, 16 pips sobre 207,91", "CPI de Tóquio <24h, piso 200", "PMI suave, FSR na 5ª"],
    },
}

NEWS_ITEM_JS = r'''                {
                    date: "25/11/2026",
                    category: "macro",
                    impact: "high",
                    pairs: ["EUR/USD", "USD/JPY", "AUD/USD", "GBP/USD", "EUR/JPY", "GBP/JPY"],
                    pt: {
                        headline: "Muralha quente: PIB revisto a 4,3% e núcleo do PCE a 3,3% imprimem três novas mínimas de 9 meses; Thanksgiving + ata do BCE + CPI de Tóquio mantêm os seis em AGUARDAR",
                        summary: "Edição de quarta 25/11/2026, sobre o fixing BCE/Frankfurter de 25/11 (593 pregões) — publicado depois dos dados das 13:30 UTC, então a resposta do dólar está nos níveis. EUR/USD 1,0935 (−0,25%) é a nova mínima de 9 meses, 33 pips através de 1,0968, com o DXY em ≈104,1 (+0,2% a 104,06, Reuters) rumo à máxima de 19 meses de segunda perto de 104,5. USD/JPY 159,32 (+0,16%) fechou a terceira sessão de volta acima da SMA200 (158,85) — o mapa voltou a MISTO — com 160,00 travando desde 13/11 e o piso do MoF em 134. AUD/USD 0,6570 (−1,08%, −72 pips) desabou à nova mínima de 9 meses mesmo com o CPI de outubro batendo em 4,9% (núcleo aparado 3,8%); RBA em 4,85% decide em 8/12 com manutenção a ≈80-100%. GBP/USD 1,3060 (−0,29%) é a nova mínima de 9 meses no PMI flash suave (composto 52,3, serviços 52,0 errando) mais a muralha quente. EUR/JPY 174,22 (−0,10%) segurou 21 pips acima da mínima; GBP/JPY 208,07 (−0,13%) segurou 16 pips acima de 207,91. Quinta é Thanksgiving (EUA fechados) com ata do BCE, CPI de Tóquio (3,1% esperado) e FSR do BoE; sexta traz os CPIs flash de França e Espanha; o payroll sai em 4/12. Fed 8-9/12 ≈96%, BCE 17/12 ≈96%, BoJ 17-18/12 ≈86%. Cada rompimento tem uma sessão e cada stop legal cruza seu extremo: os seis ficam em AGUARDAR.",
                        take: "A muralha veio quente e os níveis já precificam — mas cada gatilho pede um segundo fechamento, e as próximas 24 horas pertencem à ata do BCE, ao CPI de Tóquio e ao feriado dos EUA. A mesa espera a fita clarear."
                    },
                    en: {
                        headline: "Hot wall: GDP revised to 4.3% and core PCE at 3.3% print three new 9-month lows; Thanksgiving + ECB minutes + Tokyo CPI keep all six on WAIT",
                        summary: "Wednesday 25/11/2026 edition, on the 25/11 ECB/Frankfurter fixing (593 sessions) — published after the 13:30 UTC data, so the dollar's answer is in the levels. EUR/USD 1.0935 (−0.25%) is the new 9-month low, 33 pips through 1.0968, with the DXY at ≈104.1 (+0.2% to 104.06, Reuters) toward Monday's 19-month high near 104.5. USD/JPY 159.32 (+0.16%) closed a third session back above the SMA200 (158.85) — the map is MIXED again — with 160.00 capping since Nov 13 and the MoF floor at 134. AUD/USD 0.6570 (−1.08%, −72 pips) crashed to a new 9-month low even as October CPI beat at 4.9% (trimmed 3.8%); RBA at 4.85% decides Dec 8 with a hold at ≈80-100%. GBP/USD 1.3060 (−0.29%) is the new 9-month low on soft flash PMI (composite 52.3, services 52.0 miss) plus the hot wall. EUR/JPY 174.22 (−0.10%) held 21 pips above its low; GBP/JPY 208.07 (−0.13%) held 16 pips above 207.91. Thursday is Thanksgiving (US shut) with the ECB minutes, Tokyo CPI (3.1% eyed) and the BoE FSR; Friday brings French and Spanish flash CPI; payrolls land Dec 4. Fed Dec 8-9 ≈96%, ECB Dec 17 ≈96%, BoJ Dec 17-18 ≈86%. Every breakdown is one session old and every legal stop crosses its extreme: all six stay on WAIT.",
                        take: "The wall landed hot and the levels already price it — but every trigger needs a second close, and the next 24 hours belong to the ECB minutes, Tokyo CPI and a US holiday. The desk waits for the tape to clear."
                    }
                },
'''

NEWS_CARD = r'''                <!-- News 25/11/2026: hot GDP + PCE; three new 9-month lows; USD/JPY back to MIXED; all six WAIT -->
                <article class="news-card">
                    <div class="news-card-top">
                        <span class="news-cat"><span class="lang-en">Macro Data</span><span class="lang-pt" style="display:none;">Dados Macro</span></span>
                        <span class="impact-badge high"><span class="lang-en">High Impact</span><span class="lang-pt" style="display:none;">Impacto Alto</span></span>
                        <span class="news-date">25/11/2026</span>
                    </div>
                    <h2 class="news-title">
                        <span class="lang-en">Hot wall: GDP revised to 4.3% and core PCE at 3.3% print three new 9-month lows; Thanksgiving + ECB minutes + Tokyo CPI keep all six on WAIT</span>
                        <span class="lang-pt" style="display:none;">Muralha quente: PIB revisto a 4,3% e núcleo do PCE a 3,3% imprimem três novas mínimas de 9 meses; Thanksgiving + ata do BCE + CPI de Tóquio mantêm os seis em AGUARDAR</span>
                    </h2>
                    <p class="news-summary">
                        <span class="lang-en">Wednesday 25/11/2026 edition, on the 25/11 ECB/Frankfurter fixing (593 sessions) — published after the 13:30 UTC data, so the dollar's answer is in the levels. EUR/USD 1.0935 (−0.25%) is the new 9-month low, 33 pips through 1.0968, with the DXY at ≈104.1 (+0.2% to 104.06, Reuters) toward Monday's 19-month high near 104.5. USD/JPY 159.32 (+0.16%) closed a third session back above the SMA200 (158.85) — the map is MIXED again — with 160.00 capping since Nov 13 and the MoF floor at 134. AUD/USD 0.6570 (−1.08%, −72 pips) crashed to a new 9-month low even as October CPI beat at 4.9% (trimmed 3.8%); RBA at 4.85% decides Dec 8 with a hold at ≈80-100%. GBP/USD 1.3060 (−0.29%) is the new 9-month low on soft flash PMI (composite 52.3, services 52.0 miss) plus the hot wall. EUR/JPY 174.22 (−0.10%) held 21 pips above its low; GBP/JPY 208.07 (−0.13%) held 16 pips above 207.91. Thursday is Thanksgiving (US shut) with the ECB minutes, Tokyo CPI (3.1% eyed) and the BoE FSR; Friday brings French and Spanish flash CPI; payrolls land Dec 4. Fed Dec 8-9 ≈96%, ECB Dec 17 ≈96%, BoJ Dec 17-18 ≈86%. Every breakdown is one session old and every legal stop crosses its extreme: all six stay on WAIT.</span>
                        <span class="lang-pt" style="display:none;">Edição de quarta 25/11/2026, sobre o fixing BCE/Frankfurter de 25/11 (593 pregões) — publicado depois dos dados das 13:30 UTC, então a resposta do dólar está nos níveis. EUR/USD 1,0935 (−0,25%) é a nova mínima de 9 meses, 33 pips através de 1,0968, com o DXY em ≈104,1 (+0,2% a 104,06, Reuters) rumo à máxima de 19 meses de segunda perto de 104,5. USD/JPY 159,32 (+0,16%) fechou a terceira sessão de volta acima da SMA200 (158,85) — o mapa voltou a MISTO — com 160,00 travando desde 13/11 e o piso do MoF em 134. AUD/USD 0,6570 (−1,08%, −72 pips) desabou à nova mínima de 9 meses mesmo com o CPI de outubro batendo em 4,9% (núcleo aparado 3,8%); RBA em 4,85% decide em 8/12 com manutenção a ≈80-100%. GBP/USD 1,3060 (−0,29%) é a nova mínima de 9 meses no PMI flash suave (composto 52,3, serviços 52,0 errando) mais a muralha quente. EUR/JPY 174,22 (−0,10%) segurou 21 pips acima da mínima; GBP/JPY 208,07 (−0,13%) segurou 16 pips acima de 207,91. Quinta é Thanksgiving (EUA fechados) com ata do BCE, CPI de Tóquio (3,1% esperado) e FSR do BoE; sexta traz os CPIs flash de França e Espanha; o payroll sai em 4/12. Fed 8-9/12 ≈96%, BCE 17/12 ≈96%, BoJ 17-18/12 ≈86%. Cada rompimento tem uma sessão e cada stop legal cruza seu extremo: os seis ficam em AGUARDAR.</span>
                    </p>
                    <div class="news-take">
                        <span class="take-tag"><span class="lang-en">Desk take</span><span class="lang-pt" style="display:none;">Leitura da mesa</span></span>
                        <span class="lang-en">The wall landed hot and the levels already price it — but every trigger needs a second close, and the next 24 hours belong to the ECB minutes, Tokyo CPI and a US holiday. The desk waits for the tape to clear.</span>
                        <span class="lang-pt" style="display:none;">A muralha veio quente e os níveis já precificam — mas cada gatilho pede um segundo fechamento, e as próximas 24 horas pertencem à ata do BCE, ao CPI de Tóquio e ao feriado dos EUA. A mesa espera a fita clarear.</span>
                    </div>
                    <div class="news-pairs">
                        <span class="np-label"><span class="lang-en">Watch</span><span class="lang-pt" style="display:none;">Acompanhar</span></span>
                        <a href="eur-usd.html" class="pair-link-chip">EUR/USD</a><a href="usd-jpy.html" class="pair-link-chip">USD/JPY</a><a href="aud-usd.html" class="pair-link-chip">AUD/USD</a><a href="gbp-usd.html" class="pair-link-chip">GBP/USD</a><a href="eur-jpy.html" class="pair-link-chip">EUR/JPY</a><a href="gbp-jpy.html" class="pair-link-chip">GBP/JPY</a>
                    </div>
                </article>

'''

NEW_CAL = '''                <div class="cal-cell">
                    <span class="cal-date">26/11</span>
                    <span class="cal-event"><span class="lang-en">Thanksgiving (US shut) · ECB minutes · Tokyo CPI · BoE FSR</span><span class="lang-pt" style="display:none;">Thanksgiving (EUA fechados) · ata do BCE · CPI de Tóquio · FSR do BoE</span></span>
                    <div class="cal-meta"><span class="cal-impact high" aria-hidden="true"></span><span class="cal-cur">USD</span></div>
                </div>
                <div class="cal-cell">
                    <span class="cal-date">27/11</span>
                    <span class="cal-event"><span class="lang-en">FR + ES flash CPI · US early close</span><span class="lang-pt" style="display:none;">CPIs flash de FR + ES · fechamento antecipado nos EUA</span></span>
                    <div class="cal-meta"><span class="cal-impact med" aria-hidden="true"></span><span class="cal-cur">EUR</span></div>
                </div>
                <div class="cal-cell">
                    <span class="cal-date">04/12</span>
                    <span class="cal-event"><span class="lang-en">US nonfarm payrolls</span><span class="lang-pt" style="display:none;">Payroll dos EUA</span></span>
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
        'nextEvent: "PCE + GDP Wednesday · AU CPI · Thanksgiving Thursday"',
        'nextEvent: "Thanksgiving Thursday · ECB minutes · Tokyo CPI"')
    idx = idx.replace(
        'nextEvent: "PCE + PIB na quarta · CPI da Austrália · Thanksgiving na quinta"',
        'nextEvent: "Thanksgiving na quinta · ata do BCE · CPI de Tóquio"')

    start = idx.find("        const forexData = {")
    end = idx.find("        /* ==========================================\n           B. Market metadata")
    if start < 0 or end < 0:
        raise SystemExit("forexData markers missing")
    idx = idx[:start] + "        const forexData = " + json.dumps(DATA, ensure_ascii=False, indent=4) + ";\n\n" + idx[end:]

    d0 = idx.find("        const dailyChanges = {")
    d1 = idx.find("        const macroDrivers = {")
    changes = {
        "EUR/USD": "-0.25%", "USD/JPY": "+0.16%", "AUD/USD": "-1.08%",
        "GBP/USD": "-0.29%", "EUR/JPY": "-0.10%", "GBP/JPY": "-0.13%",
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
    ledger["meta"]["lastUpdated"] = "25/11/2026"
    with open(LEDGER, "w", encoding="utf-8", newline="\n") as f:
        json.dump(ledger, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("ledger lastUpdated only; book still empty")

    with open(NEWS, encoding="utf-8") as f:
        news = f.read()
    news = news.replace(
        "Market Wire · Week-Ahead Edition: Wednesday's Data Wall, Still No Ticket",
        "Market Wire · Hot GDP + PCE, Three New 9-Month Lows, Still No Ticket")
    news = news.replace(
        "Telégrafo da Mesa · Edição da Semana: Muralha de Dados na Quarta, Ainda Sem Ticket",
        "Telégrafo da Mesa · PIB + PCE Quentes, Três Novas Mínimas de 9 Meses, Ainda Sem Ticket")
    news = news.replace(OLD_TS, TS)
    news = news.replace(
        "6 pairs · Friday's lows stand · PCE + GDP + AU CPI Wednesday",
        "6 pairs · GDP 4.3% + core PCE 3.3% · AU CPI 4.9% · Thanksgiving Thursday")
    news = news.replace(
        "6 pares · mínimas de sexta mantidas · PCE + PIB + CPI da Austrália na quarta",
        "6 pares · PIB 4,3% + PCE núcleo 3,3% · CPI da Austrália 4,9% · Thanksgiving na quinta")
    start = news.find('                <div class="cal-cell">')
    end = news.find("            </div>\n        </section>", start)
    if start < 0 or end < 0:
        raise SystemExit("calendar block missing")
    news = news[:start] + NEW_CAL + "\n" + news[end:]
    marker = "                <!-- News 22/11/2026:"
    if marker not in news:
        raise SystemExit("news marker missing")
    news = news.replace(marker, NEWS_CARD + marker, 1)
    with open(NEWS, "w", encoding="utf-8", newline="\n") as f:
        f.write(news)
    print("news.html patched")

    with open(SITEMAP, encoding="utf-8") as f:
        sm = f.read()
    n = sm.count("2026-11-22")
    if n != 9:
        raise SystemExit("expected 9 sitemap dates, found %d" % n)
    sm = sm.replace("2026-11-22", "2026-11-25")
    with open(SITEMAP, "w", encoding="utf-8", newline="\n") as f:
        f.write(sm)
    print("sitemap patched")

    with open(VERIFY, encoding="utf-8") as f:
        v = f.read()
    v = v.replace('TODAY_TS = "22/11/2026 10:50 UTC"', 'TODAY_TS = "%s"' % TS)
    v = v.replace(
        'TODAY_DATE = "22/11/2026"  # report edition: 22/11/2026, on the 20/11/2026 basis session',
        'TODAY_DATE = "25/11/2026"  # report edition: 25/11/2026, on the 25/11/2026 basis session')
    v = v.replace(
        'TICKER = [("EUR/USD","-0.02%"),("USD/JPY","-0.83%"),("AUD/USD","-0.68%"),\n'
        '          ("GBP/USD","-0.20%"),("EUR/JPY","-0.85%"),("GBP/JPY","-1.03%")]',
        'TICKER = [("EUR/USD","-0.25%"),("USD/JPY","+0.16%"),("AUD/USD","-1.08%"),\n'
        '          ("GBP/USD","-0.29%"),("EUR/JPY","-0.10%"),("GBP/JPY","-0.13%")]')
    with open(VERIFY, "w", encoding="utf-8", newline="\n") as f:
        f.write(v)
    print("verify constants patched")

if __name__ == "__main__":
    main()

