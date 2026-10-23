#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""23/10/2026 edition — yen through 157, second break on EUR/JPY, shelf still the only ticket.

Basis: ECB/Frankfurter daily reference rates, 570 sessions (01/08/2024-23/10/2026),
last close Friday 23/10/2026. MT5 package unavailable (MetaTrader5._core missing).

Headlines of the session:
  - USD/JPY closed 156.80, through the 157.00 round and the 61.8% Fib 156.94.
    The close IS the new 10-day and 20-day low. A 1:2 before the 156.00 round
    needs a stop of <=40 pips; the 1.5-sigma20 floor is 64. No ticket.
  - EUR/JPY 175.51 is the second close under the old 9-month low 176.85 and
    the first through the Oct-2025 shelf (175.70-175.92). The new extreme still
    wants a confirming close, and the structural stop over 177.00 puts the 1:2
    inside the Sep-2025 cluster (~172.3-172.9). No ticket.
  - BoJ policy rate is already 1.25% (September hike). Bloomberg (Oct 21-22):
    no surveyed economist expects a hike on Oct 30; 83% look for December,
    to 1.50%. Reuters poll (Oct 13-19) is the same shape. October is a hold.
  - GBP/USD open short (entry 1.3376 on 22/10) extended to 1.3368. UK retail
    sales -0.4% m/m (exp -0.1%); flash composite PMI 53.1 (exp ~51.8).
    Neither stop 1.3460 nor target 1.3250 was close-crossed. Session 1 of 10.
  - EUR/USD 1.1193 never entered 1.1260-1.1300. Shelf fade re-armed a fourth time.
  - Eurozone flash composite PMI 51.9 (exp 52.7); France composite 48.4.
  - US flash composite 57.6; selling prices sharpest since Aug 2022 (TheStreet).
  - WTI ~$103 (about +3.5% on the day, from ~$99). MUFG: NYT reports of
    US-Israel strike planning on Iran after the midterms; Nasdaq -2.6%.
"""
import json, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

INDEX = r"C:\Projetos\forex-report\docs\index.html"
NEWS = r"C:\Projetos\forex-report\docs\news.html"
LEDGER = r"C:\Projetos\forex-report\docs\track-record.json"
SITEMAP = r"C:\Projetos\forex-report\docs\sitemap.xml"
VERIFY = r"C:\Projetos\forex-report\pipeline\verify_all.py"

STAMP = "23/10/2026 18:10 UTC"
OLD_STAMP = "22/10/2026 21:57 UTC"

def sub1(text, old, new, name, count=None):
    n = text.count(old)
    expected = count if count is not None else 1
    assert n == expected, "%s: found %d occurrences of %r (expected %d)" % (name, n, old[:80], expected)
    return text.replace(old, new)

forex = {
    "EUR/USD": {
        "quote": "1.1193",
        "bias": "BAIXA",
        "biasType": "bear",
        "pt": {
            "fundamental": "O EUR/USD fechou em 1,1193 na sessão de sexta 23/10/2026 (taxa de referência BCE/Frankfurter; o pacote MetaTrader 5 segue indisponível nesta máquina), caindo -0,11% — quarto pregão de desgaste sob a prateleira. O flash de outubro da zona do euro decepcionou: composto 51,9 (esperado 52,7; 53,1 em setembro), com a França de volta à contração (composto 48,4), e o juro de 10 anos francês passou de 5% na semana (máxima de 5,14%, MUFG). O WTI fechou a ~US$ 103 (~+3,5% no dia, de ~US$ 99), com relatos do New York Times — citados pela MUFG — de planos americanos e israelenses de ataques ao Irã depois das eleições de meio de mandato. O fechamento ficou 12 pips acima da mínima de 10 pregões (1.1181, 12/10) e 16 pips acima da mínima de 9 meses (1.1177, 07/10); a prateleira 1.1260-1.1300 segue intocada (a máxima recente é 1.1253, 16/10). Alinhamento de baixa pleno (fechamento sob a SMA200 1,1574, SMA50 1,1440 abaixo dela). O fade 1.1260-1.1300 é rearmado pela quarta edição seguida. O FOMC decide 28/10 (manutenção em 3,75-4,00% é o caso-base; o flash americano veio em 57,6, com preços de venda no ritmo mais alto desde agosto de 2022) e o BCE decide 29/10 com a taxa em 2,50%. Indicadores (SMA 50/200, σ20, Donchian e Fibonacci) calculados da série diária BCE/Frankfurter (570 pregões, 01/08/2024 a 23/10/2026).",
            "trend": "Fechamento sob a SMA200 (1,1574) com a SMA50 (1,1440) abaixo dela — alinhamento de baixa pleno. A mínima de 9 meses (1.1177, 07/10) e a de 20 pregões seguem invictas; o teto imediato é a máxima de 10 pregões (1.1253, 16/10), com a prateleira 1.1260-1.1300 logo acima.",
            "support": "1.1177 (mínima de 9 meses e de 20 pregões, 07/10), com o redondo 1.1150 como único obstáculo até o alvo 1.1120.",
            "resistance": "1.1253 (máxima de 10 pregões, 16/10) e a prateleira 1.1260-1.1300, coroados pelo duplo fechamento 1.1355 (29-30/09).",
            "priceAction": "Fade do repique na prateleira (quarto rearme): o gatilho é um fechamento diário dentro de 1.1260-1.1300 seguido de um fechamento abaixo do fechamento anterior e do meio da faixa 1.1280 (entrada de referência 1.1280). Stop 1.1360 (80 pips, sobre o duplo fechamento 1.1355 e a Fib 78,6% 1.1348; ≥ piso 1,5σ20 de 55 pips). Alvo 1.1120 (160 pips), sob a mínima de 9 meses e acima do redondo 1.1100, cruzando apenas o redondo 1.1150. Só contam fechamentos depois desta edição; os fechamentos de 27-29/10 (janelas do FOMC e do BCE) não armam.",
            "recommendation": "VENDA (SHORT) NA RETRAÇÃO",
            "trigger": "Fechamento diário dentro de 1.1260-1.1300 e um fechamento seguinte abaixo do anterior e do meio 1.1280 — entrada de referência 1.1280. Os fechamentos de 27-29/10 (janelas do FOMC e do BCE) não armam. Válido até o fechamento de 30/10.",
            "stop": "1.1360 (80 pips, sobre o duplo fechamento de 29-30/09 em 1.1355 e a Fib 78,6% 1.1348; ≥ piso 1,5σ20 de 55 pips) · risco sugerido ≤ 1% por operação.",
            "target": "1.1120 (160 pips), sob a mínima de 9 meses 1.1177 e acima do redondo 1.1100 — cruzando apenas o redondo 1.1150.",
            "rr": "1:2.00",
            "rrValue": 50,
            "justification": "O preço segue sem entregar extremo nem prateleira: perseguir a mínima de 16 pips de distância paga o pior ponto do corredor, e o único ticket com localização continua sendo o fade em 1.1260-1.1300 (stop estrutural sobre o duplo 1.1355, 1:2,00 até 1.1120 cruzando só o redondo 1.1150). O PMI fraco e o juro francês acima de 5% reforçam o viés; o FOMC de 28/10 e o BCE de 29/10 filtram os fechamentos da própria janela."
        },
        "en": {
            "fundamental": "EUR/USD closed at 1.1193 in the Friday 23/10/2026 session (ECB/Frankfurter reference rate; the MetaTrader 5 package is still unavailable on this machine), down -0.11% — a fourth session of grind under the shelf. The eurozone October flash disappointed: composite 51.9 (expected 52.7; 53.1 in September), with France back in contraction (composite 48.4), and the French 10-year yield pushed through 5% this week (a 5.14% high, MUFG). WTI closed near $103 (about +3.5% on the day, from ~$99), alongside New York Times reports — cited by MUFG — of US and Israeli planning for strikes on Iran after the midterm elections. The close finished 12 pips above the 10-day low (1.1181, Oct 12) and 16 pips above the 9-month low (1.1177, Oct 7); the 1.1260-1.1300 shelf is still untouched (the recent high is 1.1253, Oct 16). Full bear alignment (close under the SMA200 1.1574, 50-day 1.1440 below it). The 1.1260-1.1300 fade is re-armed for a fourth straight edition. The FOMC decides Oct 28 (a hold at 3.75-4.00% is the base case; the US flash composite printed 57.6, with selling prices rising at the sharpest pace since August 2022) and the ECB decides Oct 29 with the rate at 2.50%. Indicators (SMA 50/200, sigma20, Donchian and Fibonacci) computed from the ECB/Frankfurter daily series (570 sessions, 01/08/2024 to 23/10/2026).",
            "trend": "Close under the SMA200 (1.1574) with the 50-day (1.1440) below it — full bear alignment. The 9-month low (1.1177, Oct 7) and the 20-day low still stand; the immediate ceiling is the 10-day high (1.1253, Oct 16), with the 1.1260-1.1300 shelf right above.",
            "support": "1.1177 (the 9-month and 20-day low, Oct 7), with the 1.1150 round as the only obstacle down to the 1.1120 target.",
            "resistance": "1.1253 (the 10-day high, Oct 16) and the 1.1260-1.1300 shelf, crowned by the double close at 1.1355 (Sep 29-30).",
            "priceAction": "Fade the rally on the shelf (fourth re-arm): the trigger is a daily close inside 1.1260-1.1300 followed by a close below the previous close and the 1.1280 midpoint (entry reference 1.1280). Stop 1.1360 (80 pips, over the 1.1355 double close and the 78.6% Fib 1.1348; >= the 55-pip 1.5-sigma20 floor). Target 1.1120 (160 pips), under the 9-month low and above the 1.1100 round, crossing only the 1.1150 round. Only closes after this edition count; the Oct 27-29 closes (FOMC and ECB windows) don't arm.",
            "recommendation": "SELL (SHORT) ON PULLBACK",
            "trigger": "A daily close inside 1.1260-1.1300 and a following close below the previous close and the 1.1280 midpoint — entry reference 1.1280. The Oct 27-29 closes (FOMC and ECB windows) don't arm. Valid through the Oct-30 close.",
            "stop": "1.1360 (80 pips, over the Sep 29-30 double close at 1.1355 and the 78.6% Fib 1.1348; >= the 55-pip 1.5-sigma20 floor) · suggested risk ≤ 1% per trade.",
            "target": "1.1120 (160 pips), under the 9-month low 1.1177 and above the 1.1100 round — crossing only the 1.1150 round.",
            "rr": "1:2.00",
            "rrValue": 50,
            "justification": "Price is still delivering neither extreme nor shelf: chasing the low from 16 pips away pays the corridor's worst price, and the only ticket with location remains the fade at 1.1260-1.1300 (structural stop over the 1.1355 double close, 1:2.00 to 1.1120 crossing only the 1.1150 round). The soft PMI and French yields above 5% reinforce the bias; the Oct-28 FOMC and the Oct-29 ECB filter the closes of their own window."
        }
    },
    "USD/JPY": {
        "quote": "156.80",
        "bias": "BAIXA",
        "biasType": "bear",
        "pt": {
            "fundamental": "O USD/JPY fechou em 156,80 na sessão de sexta 23/10/2026 (taxa de referência BCE/Frankfurter), caindo -0,16% (-25 pips) — o fechamento atravessou o redondo 157,00 e a Fib 61,8% (156,94) e é, ele mesmo, a nova mínima de 10 e de 20 pregões. O iene estendeu o movimento de risco-off (o Nasdaq caiu 2,6% com a atualização de capex da Meta, MUFG) e de energia (WTI a ~US$ 103). A correção de premissa: a taxa do BoJ já está em 1,25% desde a alta de setembro; a reunião de 29-30/10 é uma manutenção (pesquisa Bloomberg de 21-22/10: nenhum economista espera alta em 30/10; 83% apontam dezembro, para 1,50% — o poll da Reuters de 13-19/10 tem o mesmo desenho). A janela formal de 30 dias dos rate checks do MoF de meados de setembro segue fechada: piso 1,5σ20 (64 pips). Alinhamento de baixa pleno (fechamento sob a SMA200 158,54 e a SMA50 157,57, com a SMA50 abaixo dela). Indicadores calculados da série diária BCE/Frankfurter (570 pregões, 01/08/2024 a 23/10/2026).",
            "trend": "Fechamento sob a SMA200 (158,54) com a SMA50 (157,57) abaixo dela — alinhamento de baixa pleno. O fechamento de 23/10 cravou a mínima de 10 e de 20 pregões (156,80); o degrau seguinte da série é o fechamento de 04/09 (156,25) e o de 03/09 (156,01), com o redondo 156,00 e o fechamento de 17/09 (155,69) abaixo.",
            "support": "156.25 (fechamento de 04/09) e 156.01 (03/09), com o redondo 156,00 e o fechamento de 17/09 (155,69) como destino da escada. O fechamento de 23/10 (156,80) é a mínima de 10/20 pregões.",
            "resistance": "156.94 (Fib 61,8%, entregue) e o redondo 157,00, com a SMA50 (157,57) e a SMA200 (158,54) acima; as máximas de 10/20 pregões ficam em 158,60.",
            "priceAction": "O rompimento do canal está no fechamento e a geometria continua reprovando. De 156,80 até o redondo 156,00 há 80 pips: um 1:2 que pare antes desse redondo exige stop de no máximo 40 pips, e o piso é 64. O stop estrutural sobre a SMA50 (157,70, 90 pips) empurra o alvo 1:2 para ~155,00 — atravessando 156,25, 156,01, o redondo 156,00 e o fechamento de 17/09 (155,69). O repique a 157,00-157,57 esbarra na mesma escada. Sem ticket: o cluster FOMC (28/10) + BoJ (30/10, manutenção hawkish em 1,25%) reprecifica o corredor.",
            "recommendation": "AGUARDAR OUTRO GATILHO",
            "trigger": "156.00 é o degrau que trava a conta: 80 pips abaixo do fechamento, contra um piso de 64 — não cabe 1:2 antes dele. Reavaliar após o FOMC (28/10) e o BoJ (30/10, manutenção em 1,25%; a alta para 1,50% é o consenso de dezembro).",
            "stop": "N/A (sem operação).",
            "target": "N/A (sem operação).",
            "rr": "N/A",
            "rrValue": 0,
            "justification": "O iene fez o segundo serviço — atravessou o redondo e cravou a mínima do canal — e a distância até o próximo redondo não paga o piso de volatilidade. Pagar o cluster FOMC-BoJ em rompimento, com a alta de outubro já fora da mesa (a taxa está em 1,25% e a reunião é manutenção), é risco de evento. A mesa espera os dois bancos."
        },
        "en": {
            "fundamental": "USD/JPY closed at 156.80 in the Friday 23/10/2026 session (ECB/Frankfurter reference rate), down -0.16% (-25 pips) — the close went through the 157.00 round and the 61.8% Fib (156.94) and is itself the new 10-day and 20-day low. The yen extended the move on risk-off (the Nasdaq fell 2.6% on Meta's capex update, MUFG) and on energy (WTI near $103). Premise correction: the BoJ rate is already 1.25% after the September hike; the Oct 29-30 meeting is a hold (Bloomberg survey of Oct 21-22: no economist expects a hike on Oct 30; 83% point to December, to 1.50% — the Reuters poll of Oct 13-19 has the same shape). The MoF's mid-September rate-check 30-day window remains closed: floor at 1.5-sigma20 (64 pips). Full bear alignment (close under the SMA200 158.54 and the 50-day 157.57, the 50-day below it). Indicators computed from the ECB/Frankfurter daily series (570 sessions, 01/08/2024 to 23/10/2026).",
            "trend": "Close under the SMA200 (158.54) with the 50-day (157.57) below it — full bear alignment. The Oct-23 close pinned the 10-day and 20-day low (156.80); the next rung on the series is the Sep-4 close (156.25) and the Sep-3 close (156.01), with the 156.00 round and the Sep-17 close (155.69) below.",
            "support": "156.25 (the Sep-4 close) and 156.01 (Sep 3), with the 156.00 round and the Sep-17 close (155.69) as the ladder's destination. The Oct-23 close (156.80) is the 10/20-day low.",
            "resistance": "156.94 (the 61.8% Fib, handed back) and the 157.00 round, with the SMA50 (157.57) and the SMA200 (158.54) above; the 10/20-day highs sit at 158.60.",
            "priceAction": "The channel break is on the close and the geometry still rejects it. From 156.80 down to the 156.00 round is 80 pips: a 1:2 that stops before that round needs a stop of 40 pips at most, and the floor is 64. A structural stop over the SMA50 (157.70, 90 pips) pushes the 1:2 target to ~155.00 — crossing 156.25, 156.01, the 156.00 round and the Sep-17 close (155.69). A bounce to 157.00-157.57 hits the same ladder. No ticket: the FOMC (Oct 28) + BoJ (Oct 30, a hawkish hold at 1.25%) cluster reprices the corridor.",
            "recommendation": "WAIT FOR ANOTHER TRIGGER",
            "trigger": "156.00 is the rung that breaks the arithmetic: 80 pips under the close, against a 64-pip floor — a 1:2 does not fit before it. Reassess after the FOMC (Oct 28) and the BoJ (Oct 30, a hold at 1.25%; the hike to 1.50% is the December consensus).",
            "stop": "N/A (no trade).",
            "target": "N/A (no trade).",
            "rr": "N/A",
            "rrValue": 0,
            "justification": "The yen did the second job — went through the round and pinned the channel low — and the distance to the next round does not pay the volatility floor. Paying the FOMC-BoJ cluster on a breakdown, with the October hike already off the table (the rate is 1.25% and the meeting is a hold), is event risk. The desk waits for both banks."
        }
    },
    "AUD/USD": {
        "quote": "0.7022",
        "bias": "NEUTRO",
        "biasType": "neutral",
        "pt": {
            "fundamental": "O AUD/USD fechou em 0,7022 na sessão de sexta 23/10/2026 (taxa de referência BCE/Frankfurter), subindo +0,15% — o dólar australiano acompanhou as moedas de commodity na semana (MUFG: NOK, AUD e CAD na frente, com o mercado aumentando a probabilidade de alta da RBA em 03/11) e o WTI a ~US$ 103, mas o fechamento parou 11 pips abaixo da máxima de 10/20 pregões (0.7034, 21/10) e 23 pips abaixo da SMA200 (0,7046). A leitura segue NEUTRA: fechamento sob as duas médias (SMA200 0,7046, SMA50 0,7078) com a SMA50 ainda acima da SMA200. Sem o segundo fechamento sobre a SMA200 não há resolução do misto. O CPI do Q3 (≈28/10) é o árbitro local, no meio do cluster FOMC-BoJ. Indicadores calculados da série diária BCE/Frankfurter (570 pregões, 01/08/2024 a 23/10/2026).",
            "trend": "Misto por construção: fechamento sob as duas médias com a SMA50 ainda acima da SMA200. O canal segue 0.6911-0.7034; a recaptura da SMA200 0,7046 com segundo fechamento resolve para cima, a perda de 0.6911 para baixo.",
            "support": "0.6911 (mínima de 10/20 pregões, 15/10), com o redondo 0,6900 abaixo.",
            "resistance": "0.7034 (a máxima de 10/20 pregões, 21/10), com a SMA200 (0,7046) e a Fib 38,2% (0,7057) formando o teto real. O fechamento sentou sobre a Fib 50% (0,7013).",
            "priceAction": "Sem gatilho: 0,7022 não rompeu 0.7034 nem devolveu 0.6911. Um fechamento sobre 0.7034 e o segundo contra a SMA200 0,7046 resolveria o misto para cima; um fechamento sob 0.6911 abre 0.6900 e o vácuo até o piso de janeiro (0.6733). O CPI do Q3 (≈28/10) escolhe o lado — e a RBA (03/11) lê em seguida.",
            "recommendation": "AGUARDAR OUTRO GATILHO",
            "trigger": "0.7034 é o teto a romper primeiro (com a SMA200 0,7046 logo acima); 0.6911 o piso. Sem rompimento confirmado não há ticket — reavaliar após o CPI australiano do Q3 (≈28/10).",
            "stop": "N/A (sem operação).",
            "target": "N/A (sem operação).",
            "rr": "N/A",
            "rrValue": 0,
            "justification": "O petróleo e a reprecificação da RBA compraram o australiano de volta acima de 0,70 e não compraram a média que manda. Direção dentro de 0.6911-0.7034 segue sendo pagar uma escolha de lado que o fechamento não fez — o CPI do Q3 (≈28/10) é o que pode destravar."
        },
        "en": {
            "fundamental": "AUD/USD closed at 0.7022 in the Friday 23/10/2026 session (ECB/Frankfurter reference rate), up +0.15% — the Aussie tracked the week's commodity currencies (MUFG: NOK, AUD and CAD in front, with the market raising the odds of an RBA hike on Nov 3) and WTI near $103, but the close stopped 11 pips under the 10/20-day high (0.7034, Oct 21) and 23 pips under the SMA200 (0.7046). The read stays NEUTRAL: close under both averages (SMA200 0.7046, 50-day 0.7078) with the 50-day still above the SMA200. Without a second close over the SMA200 the mix is unresolved. Q3 CPI (≈Oct 28) is the local arbiter, inside the FOMC-BoJ cluster. Indicators computed from the ECB/Frankfurter daily series (570 sessions, 01/08/2024 to 23/10/2026).",
            "trend": "Mixed by construction: close under both averages with the 50-day still above the SMA200. The channel is still 0.6911-0.7034; reclaiming the SMA200 0.7046 with a second close resolves it up, losing 0.6911 resolves it down.",
            "support": "0.6911 (the 10/20-day low, Oct 15), with the 0.6900 round below.",
            "resistance": "0.7034 (the 10/20-day high, Oct 21), with the SMA200 (0.7046) and the 38.2% Fib (0.7057) forming the real ceiling. The close sat on the 50% Fib (0.7013).",
            "priceAction": "No trigger: 0.7022 neither broke 0.7034 nor gave back 0.6911. A close over 0.7034 and a second against the SMA200 0.7046 would resolve the mix upward; a close under 0.6911 opens 0.6900 and the vacuum down to the January floor (0.6733). Q3 CPI (≈Oct 28) picks the side — with the RBA (Nov 3) reading next.",
            "recommendation": "WAIT FOR ANOTHER TRIGGER",
            "trigger": "0.7034 is the ceiling to break first (with the SMA200 0.7046 right above); 0.6911 the floor. No confirmed break, no ticket — reassess after the Australian Q3 CPI (≈Oct 28).",
            "stop": "N/A (no trade).",
            "target": "N/A (no trade).",
            "rr": "N/A",
            "rrValue": 0,
            "justification": "Oil and the RBA repricing bought the Aussie back above 0.70 and did not buy the average that commands. Direction inside 0.6911-0.7034 remains paying for a side-selection the close has not made — Q3 CPI (≈Oct 28) is what can unlock it."
        }
    },
    "GBP/USD": {
        "quote": "1.3368",
        "bias": "BAIXA",
        "biasType": "bear",
        "pt": {
            "fundamental": "O GBP/USD fechou em 1,3368 na sessão de sexta 23/10/2026 (taxa de referência BCE/Frankfurter), caindo -0,06% (-8 pips) — o short aberto no fechamento de 22/10 (entrada 1,3376, stop 1.3460, alvo 1.3250) completou o 1º dos 10 pregões e o dado do dia não o ameaçou. As vendas no varejo de setembro caíram 0,4% no mês (ONS, 23/10; esperado -0,1%; agosto revisado para +0,7%) e o flash de outubro veio no sentido oposto: composto 53,1 (manufatura 52,8, serviços 53,1), acima do consenso ~51,8, a oito dias do orçamento. O fechamento ficou sob o meio da prateleira 1.3390. Nem o stop nem o alvo foram cruzados por fechamento. O alinhamento de baixa segue pleno (fechamento sob a SMA200 1,3433, SMA50 1,3408 abaixo dela). O BoE decide 05/11, no pregão de expiração; o FOMC de 28/10 segue como risco de marcação dentro da janela — o filtro trava entradas novas, não gere posição aberta. Indicadores calculados da série diária BCE/Frankfurter (570 pregões, 01/08/2024 a 23/10/2026).",
            "trend": "Fechamento sob a SMA200 (1,3433) com a SMA50 (1,3408) abaixo dela — alinhamento de baixa pleno. O short vive sob o meio da prateleira; a máxima de 10 pregões agora é o próprio pop do CPI (1.3402, 21/10), com a Fib 61,8% (1,3411) e a SMA50 logo acima.",
            "support": "1.3220 (mínima de 10 pregões, 07/10; a de 20 fica em 1.3201), com a mínima de 9 meses em 1.3160 embaixo e o alvo 1.3250 acima desses pisos.",
            "resistance": "1.3420 (o teto da prateleira: Fib 61,8% 1,3411 + SMA50 1,3408), com a SMA200 (1,3433), o redondo 1.3450 e o stop 1.3460 acima.",
            "priceAction": "Posição aberta (o mapa é gestão): short de 1,3376 com stop 1.3460 — um fechamento em/acima encerra a -1R — e alvo 1.3250 — um fechamento em/abaixo banca o ticket. Do ponto disparado o R planejado na referência 1,3390 (1:2,00, 140 pips) vira ~1:1,50 (126 pips contra 84 de stop): o livro não mexe em ticket aberto. Expiração no 10º pregão (fechamento de 05/11, dia do BoE); esta sexta foi o 1º. Não se adiciona ticket novo.",
            "recommendation": "VENDA (SHORT) NA RETRAÇÃO",
            "trigger": "DISPARADO no fechamento de 22/10 (entrada 1,3376). Gestão por fechamento: stop 1.3460 / alvo 1.3250 / expiração 05/11. O fechamento de 23/10 (1,3368) não cruzou nenhum dos dois níveis.",
            "stop": "1.3460 (sobre a SMA200 1,3433 e o redondo 1.3450; ≥ piso 1,5σ20 de 57 pips) · risco sugerido ≤ 1% por operação.",
            "target": "1.3250 (140 pips da referência 1.3390; 126 da entrada disparada 1.3376), acima da mínima de 10 pregões 1.3220 — cruzando apenas os redondos 1.3350 e 1.3300.",
            "rr": "1:2.00",
            "rrValue": 50,
            "justification": "Varejo fraco e PMI forte se anularam no fechamento: 8 pips a favor do short, a 92 pips do stop e a 118 do alvo. O trabalho é do ledger até 05/11. O R realizado, se o alvo bater, sai da entrada disparada (~1:1,50) e não da referência — está escrito no ticket desde 22/10 e não se reescreve. Sem ticket novo: a continuação abaixo cruzaria a mínima de 9 meses, e o FOMC de 28/10 é marcação, não entrada."
        },
        "en": {
            "fundamental": "GBP/USD closed at 1.3368 in the Friday 23/10/2026 session (ECB/Frankfurter reference rate), down -0.06% (-8 pips) — the short opened at the Oct-22 close (entry 1.3376, stop 1.3460, target 1.3250) completed the 1st of its 10 sessions and the day's data did not threaten it. September retail sales fell 0.4% on the month (ONS, Oct 23; expected -0.1%; August revised to +0.7%) and the October flash pointed the other way: composite 53.1 (manufacturing 52.8, services 53.1), above the ~51.8 consensus, eight days out from the Budget. The close held under the 1.3390 shelf midpoint. Neither the stop nor the target was close-crossed. Full bear alignment stands (close under the SMA200 1.3433, 50-day 1.3408 below it). The BoE decides Nov 5, on the expiry session; the Oct-28 FOMC remains mark-to-market risk inside the window — the filter blocks new entries, it does not manage an open position. Indicators computed from the ECB/Frankfurter daily series (570 sessions, 01/08/2024 to 23/10/2026).",
            "trend": "Close under the SMA200 (1.3433) with the 50-day (1.3408) below it — full bear alignment. The short lives under the shelf midpoint; the 10-day high is now the CPI pop itself (1.3402, Oct 21), with the 61.8% Fib (1.3411) and the SMA50 just above.",
            "support": "1.3220 (the 10-day low, Oct 7; the 20-day sits at 1.3201), with the 9-month low at 1.3160 below and the 1.3250 target above those floors.",
            "resistance": "1.3420 (the shelf top: the 61.8% Fib 1.3411 + SMA50 1.3408), with the SMA200 (1.3433), the 1.3450 round and the 1.3460 stop above.",
            "priceAction": "Position open (the map is management): short from 1.3376 with stop 1.3460 — a close at/above ends it at -1R — and target 1.3250 — a close at/below banks the ticket. From the fired price the R planned at the 1.3390 reference (1:2.00, 140 pips) becomes ~1:1.50 (126 pips against an 84-pip stop): the book does not amend an open ticket. Expiry at the 10th session (the Nov-5 close, BoE day); this Friday was the 1st. No new ticket is added.",
            "recommendation": "SELL (SHORT) ON PULLBACK",
            "trigger": "FIRED at the Oct-22 close (entry 1.3376). Close-based management: stop 1.3460 / target 1.3250 / expiry Nov 5. The Oct-23 close (1.3368) crossed neither level.",
            "stop": "1.3460 (over the SMA200 1.3433 and the 1.3450 round; >= the 57-pip 1.5-sigma20 floor) · suggested risk ≤ 1% per trade.",
            "target": "1.3250 (140 pips from the 1.3390 reference; 126 from the fired entry 1.3376), above the 10-day low 1.3220 — crossing only the 1.3350 and 1.3300 rounds.",
            "rr": "1:2.00",
            "rrValue": 50,
            "justification": "Weak retail sales and a hot PMI cancelled out on the close: 8 pips in the short's favour, 92 pips from the stop and 118 from the target. The work is the ledger's until Nov 5. Realized R, if the target prints, comes off the fired entry (~1:1.50) and not the reference — written into the ticket since Oct 22 and not rewritten. No new ticket: the continuation below would cross the 9-month low, and the Oct-28 FOMC is mark-to-market, not an entry."
        }
    },
    "EUR/JPY": {
        "quote": "175.51",
        "bias": "BAIXA",
        "biasType": "bear",
        "pt": {
            "fundamental": "O EUR/JPY fechou em 175,51 na sessão de sexta 23/10/2026 (taxa de referência BCE/Frankfurter), caindo -0,27% (-47 pips) — o segundo fechamento sob a mínima de 9 meses antiga (176,85, 07/10) e o primeiro através da prateleira de out/2025 (fechamentos 175,70-175,92). O fechamento de 23/10 é a nova mínima de 9 meses e de 10/20 pregões, então a regra ainda pede o fechamento confirmatório seguinte. Abaixo, o próximo apoio real da série é o fechamento de 06/10/2025 (175,22) e, depois de um vácuo, o cluster de set-out/2025 (172,35-172,90). O BoJ já está em 1,25% e a reunião de 30/10 é manutenção (consenso de alta para 1,50% em dezembro). Alinhamento de baixa pleno (fechamento sob a SMA200 183,48, SMA50 180,25 abaixo dela). Janela do MoF fechada: piso 1,5σ20 (101 pips). Indicadores calculados da série diária BCE/Frankfurter (570 pregões, 01/08/2024 a 23/10/2026).",
            "trend": "Fechamento sob a SMA200 (183,48) com a SMA50 (180,25) abaixo dela — baixa plena. A mínima de 9 meses e de 10/20 pregões é o próprio fechamento (175,51); a prateleira entregue 175,70-175,92 e o redondo 176,00 são o primeiro teto, com 176,85 e a máxima de 10 pregões (177,82, 16/10) acima.",
            "support": "175.22 (fechamento de 06/10/2025), com o redondo 175,00 logo abaixo e o cluster de set-out/2025 (172,35-172,90) depois do vácuo. O fechamento de 23/10 (175,51) é a nova mínima de 9 meses.",
            "resistance": "175.70 (o piso da prateleira de out/2025, entregue) e o redondo 176,00, com a mínima antiga 176,85 e a máxima de 10 pregões 177,82 acima.",
            "priceAction": "O próximo fechamento sob 175,51 seria o confirmatório do extremo de 9 meses — e ainda assim não há ticket. O piso de 101 pips não cabe sob a prateleira quebrada; o stop estrutural tem de passar de 176,85/177,00 (~160 pips a partir de ~175,40), e o alvo 1:2 cai em ~172,20, dentro do cluster de set/2025, cruzando 175,22 e o redondo 175,00. O repique a 175,70-176,85 também não limpa esse caminho. Sem ticket até depois do BoJ (30/10).",
            "recommendation": "AGUARDAR OUTRO GATILHO",
            "trigger": "O fechamento confirmatório sob 175,51 é o gatilho da regra para o extremo novo — mas o stop estrutural sobre 177,00 coloca o alvo 1:2 dentro do cluster de 2025. Caminho bloqueado. Reavaliar após o BoJ (30/10, manutenção em 1,25%).",
            "stop": "N/A (sem operação).",
            "target": "N/A (sem operação).",
            "rr": "N/A",
            "rrValue": 0,
            "justification": "A prateleira de 2025 cedeu e o livro continua sem comprar a quebra: o stop que protege de verdade (sobre 176,85) empurra o alvo para dentro do próximo suporte, não para além dele. A manutenção do BoJ em 1,25% — e não uma alta nesta reunião — é o que o cluster ainda pode reprecificar. A mesa espera."
        },
        "en": {
            "fundamental": "EUR/JPY closed at 175.51 in the Friday 23/10/2026 session (ECB/Frankfurter reference rate), down -0.27% (-47 pips) — the second close under the old 9-month low (176.85, Oct 7) and the first through the Oct-2025 shelf (closes 175.70-175.92). The Oct-23 close is the new 9-month and 10/20-day low, so the rule still wants the next confirming close. Below, the next real support on the series is the Oct 6 2025 close (175.22) and, after a vacuum, the Sep-Oct 2025 cluster (172.35-172.90). The BoJ is already at 1.25% and the Oct-30 meeting is a hold (hike consensus to 1.50% in December). Full bear alignment (close under the SMA200 183.48, 50-day 180.25 below it). MoF window closed: floor at 1.5-sigma20 (101 pips). Indicators computed from the ECB/Frankfurter daily series (570 sessions, 01/08/2024 to 23/10/2026).",
            "trend": "Close under the SMA200 (183.48) with the 50-day (180.25) below it — full bear. The 9-month and 10/20-day low is the close itself (175.51); the handed-back shelf 175.70-175.92 and the 176.00 round are the first ceiling, with 176.85 and the 10-day high (177.82, Oct 16) above.",
            "support": "175.22 (the Oct 6 2025 close), with the 175.00 round just below and the Sep-Oct 2025 cluster (172.35-172.90) after the vacuum. The Oct-23 close (175.51) is the new 9-month low.",
            "resistance": "175.70 (the floor of the Oct-2025 shelf, handed back) and the 176.00 round, with the old low 176.85 and the 10-day high 177.82 above.",
            "priceAction": "The next close under 175.51 would confirm the 9-month extreme — and there is still no ticket. The 101-pip floor does not fit under the broken shelf; the structural stop has to clear 176.85/177.00 (~160 pips from ~175.40), and the 1:2 target lands near 172.20, inside the Sep-2025 cluster, crossing 175.22 and the 175.00 round. The bounce to 175.70-176.85 does not clear that path either. No ticket until after the BoJ (Oct 30).",
            "recommendation": "WAIT FOR ANOTHER TRIGGER",
            "trigger": "The confirming close under 175.51 is the rule's trigger for the new extreme — but the structural stop over 177.00 puts the 1:2 target inside the 2025 cluster. Path blocked. Reassess after the BoJ (Oct 30, a hold at 1.25%).",
            "stop": "N/A (no trade).",
            "target": "N/A (no trade).",
            "rr": "N/A",
            "rrValue": 0,
            "justification": "The 2025 shelf gave way and the book still does not buy the break: the stop that actually protects (over 176.85) pushes the target into the next support, not beyond it. The BoJ hold at 1.25% — not a hike at this meeting — is what the cluster can still reprice. The desk waits."
        }
    },
    "GBP/JPY": {
        "quote": "209.61",
        "bias": "BAIXA",
        "biasType": "bear",
        "pt": {
            "fundamental": "O GBP/JPY fechou em 209,61 na sessão de sexta 23/10/2026 (taxa de referência BCE/Frankfurter), caindo -0,22% (-46 pips) — o cruzamento perdeu o redondo 210,00 e a Fib 78,6% (209,85) e parou 34 pips acima da mínima de 10 pregões (209,27, 15/10). O PMI britânico forte (composto 53,1) não segurou o cruzamento contra o iene, com o WTI a ~US$ 103 e o BoJ já em 1,25% (manutenção em 30/10; consenso de alta para 1,50% em dezembro). Alinhamento de baixa pleno (fechamento sob a SMA200 212,96 e a SMA50 211,27, com a SMA50 abaixo dela). Janela do MoF fechada: piso 1,5σ20 de 117 pips. Indicadores calculados da série diária BCE/Frankfurter (570 pregões, 01/08/2024 a 23/10/2026).",
            "trend": "Fechamento sob a SMA200 (212,96) com a SMA50 (211,27) abaixo dela — baixa plena. O redondo 210,00 virou teto; a mínima de 10 pregões (209,27) é o piso imediato e a de 20 (208,07, 28/09) o seguinte, com a SMA50 e a Fib 61,8% (211,84) acima.",
            "support": "209.27 (mínima de 10 pregões, 15/10), com a mínima de 20 pregões em 208,07 (28/09) e o redondo 208,00 abaixo.",
            "resistance": "210.00 (o redondo, entregue no fechamento) e a Fib 78,6% (209,85), com a SMA50 (211,27), a Fib 61,8% (211,84) e a SMA200 (212,96) acima.",
            "priceAction": "Nenhum dos dois lados paga. A venda na perda de 209,27, com stop estrutural sobre 210,00, fica curta do piso de 117 pips; o stop que cabe (sobre a SMA50, ~211,50, mais de 180 pips a partir de 209,20) empurra o alvo 1:2 para debaixo de 208,07 e do redondo 208,00. O repique a 210,00-211,27 cruza a mesma escada no caminho de volta. Sem ticket: o BoJ (30/10) reprecifica o cruzamento.",
            "recommendation": "AGUARDAR OUTRO GATILHO",
            "trigger": "209.27 é o piso de 10 pregões, mas o stop que respeita o piso de 117 pips não cabe acima de 210,00 sem atravessar 208,07 no alvo. Reavaliar após o BoJ (30/10, manutenção em 1,25%).",
            "stop": "N/A (sem operação).",
            "target": "N/A (sem operação).",
            "rr": "N/A",
            "rrValue": 0,
            "justification": "Perder 210,00 não é um mapa: o cruzamento sentou entre o redondo e a mínima de 10 pregões, e o piso de 117 pips é maior do que o espaço até o próximo suporte de verdade. Comprar brigaria com as duas médias. A mesa espera o BoJ."
        },
        "en": {
            "fundamental": "GBP/JPY closed at 209.61 in the Friday 23/10/2026 session (ECB/Frankfurter reference rate), down -0.22% (-46 pips) — the cross lost the 210.00 round and the 78.6% Fib (209.85) and stopped 34 pips above the 10-day low (209.27, Oct 15). The hot UK PMI (composite 53.1) did not hold the cross against the yen, with WTI near $103 and the BoJ already at 1.25% (a hold on Oct 30; hike consensus to 1.50% in December). Full bear alignment (close under the SMA200 212.96 and the 50-day 211.27, the 50-day below it). MoF window closed: 1.5-sigma20 floor of 117 pips. Indicators computed from the ECB/Frankfurter daily series (570 sessions, 01/08/2024 to 23/10/2026).",
            "trend": "Close under the SMA200 (212.96) with the 50-day (211.27) below it — full bear. The 210.00 round is the ceiling now; the 10-day low (209.27) is the immediate floor and the 20-day (208.07, Sep 28) the next, with the SMA50 and the 61.8% Fib (211.84) above.",
            "support": "209.27 (the 10-day low, Oct 15), with the 20-day low at 208.07 (Sep 28) and the 208.00 round below.",
            "resistance": "210.00 (the round, handed back on the close) and the 78.6% Fib (209.85), with the SMA50 (211.27), the 61.8% Fib (211.84) and the SMA200 (212.96) above.",
            "priceAction": "Neither side pays. A short on a loss of 209.27, with a structural stop over 210.00, comes in short of the 117-pip floor; the stop that fits (over the SMA50, ~211.50, more than 180 pips from 209.20) pushes the 1:2 target under 208.07 and the 208.00 round. A bounce to 210.00-211.27 crosses the same ladder on the way down. No ticket: the BoJ (Oct 30) reprices the cross.",
            "recommendation": "WAIT FOR ANOTHER TRIGGER",
            "trigger": "209.27 is the 10-day floor, but the stop that respects the 117-pip floor does not fit above 210.00 without crossing 208.07 on the target. Reassess after the BoJ (Oct 30, a hold at 1.25%).",
            "stop": "N/A (no trade).",
            "target": "N/A (no trade).",
            "rr": "N/A",
            "rrValue": 0,
            "justification": "Losing 210.00 is not a map: the cross sat between the round and the 10-day low, and the 117-pip floor is wider than the room to the next real support. A long would fight both averages. The desk waits for the BoJ."
        }
    }
}

html = open(INDEX, encoding="utf-8").read()

s = html.find("const forexData = {")
assert s != -1
e = html.find("\n};", s)
assert e != -1
new_block = "const forexData = " + json.dumps(forex, ensure_ascii=False, indent=4)[:-1].rstrip() + "\n};"
html = html[:s] + new_block + html[e + len("\n};"):]

html = sub1(html, OLD_STAMP, STAMP, "report stamp", count=4)

html = sub1(html,
    "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 569 daily sessions (01/08/2024–22/10/2026).",
    "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 570 daily sessions (01/08/2024–23/10/2026).",
    "EN dataBasis")
html = sub1(html,
    "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, σ20 e Donchian calculados · 569 pregões (01/08/2024 a 22/10/2026).",
    "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, σ20 e Donchian calculados · 570 pregões (01/08/2024 a 23/10/2026).",
    "PT dataBasis")
html = sub1(html,
    'nextEvent: "FOMC Oct 27-28 · BoJ Oct 29-30 · BoE Nov 5"',
    'nextEvent: "FOMC Oct 28 · ECB Oct 29 · BoJ Oct 30"',
    "EN nextEvent")
html = sub1(html,
    'nextEvent: "FOMC 27-28/10 · BoJ 29-30/10 · BoE 05/11"',
    'nextEvent: "FOMC 28/10 · BCE 29/10 · BoJ 30/10"',
    "PT nextEvent")

for pair, old, new in [
    ("EUR/USD", "-0.26%", "-0.11%"), ("USD/JPY", "-0.53%", "-0.16%"),
    ("AUD/USD", "-0.31%", "+0.15%"), ("GBP/USD", "-0.19%", "-0.06%"),
    ("EUR/JPY", "-0.78%", "-0.27%"), ("GBP/JPY", "-0.72%", "-0.22%"),
]:
    html = sub1(html, '"%s": "%s"' % (pair, old), '"%s": "%s"' % (pair, new), "ticker " + pair)

new_drivers = '''        const macroDrivers = {
            "EUR/USD": {
                en: ["Euro flash PMI 51.9, France contracts", "Shelf fade 1.126-1.130 re-armed", "FOMC 28/10 · ECB 29/10"],
                pt: ["PMI euro 51,9, França contrai", "Fade 1,126-1,130 rearmado", "FOMC 28/10 · BCE 29/10"]
            },
            "USD/JPY": {
                en: ["Close through 157.00, new 10-day low", "156.00 still blocks the R/R", "BoJ hold at 1.25% · Dec hike"],
                pt: ["Fechou sob 157,00, nova mín. de 10d", "156,00 segue travando o R/R", "BoJ parado em 1,25% · alta em dez"]
            },
            "AUD/USD": {
                en: ["Still under the SMA200", "Neutral mix stands", "Q3 CPI ≈28/10 · WTI ~$103"],
                pt: ["Segue sob a SMA200", "Misto segue de pé", "CPI Q3 ≈28/10 · WTI ~US$ 103"]
            },
            "GBP/USD": {
                en: ["Short live from 1.3376", "Close 1.3368 · stop 1.3460", "PMI 53.1 vs sales -0.4%"],
                pt: ["Short vivo de 1,3376", "Fechou 1,3368 · stop 1.3460", "PMI 53,1 contra vendas -0,4%"]
            },
            "EUR/JPY": {
                en: ["Second close under the old low", "175.51 is the new 9-month low", "Path into 172.5 still blocked"],
                pt: ["2º fechamento sob a mínima antiga", "175,51 é a nova mín. de 9 meses", "Caminho até 172,5 segue travado"]
            },
            "GBP/JPY": {
                en: ["Closed under 210.00", "117-pip floor blocks both sides", "BoJ hold at 1.25%"],
                pt: ["Fechou sob 210,00", "Piso de 117 pips trava os dois lados", "BoJ parado em 1,25%"]
            }
        };'''
md_s = html.find("        const macroDrivers = {")
md_e = html.find("\n        };", md_s)
assert md_s != -1 and md_e != -1, "macroDrivers block not found"
html = html[:md_s] + new_drivers + html[md_e + len("\n        };"):]

news_item = r'''                {
                    date: "23/10/2026",
                    category: "flow",
                    impact: "high",
                    pairs: ["EUR/USD", "USD/JPY", "AUD/USD", "GBP/USD", "EUR/JPY", "GBP/JPY"],
                    pt: {
                        headline: "O iene fecha sob 157,00 e o EUR/JPY crava a segunda mínima (175,51) — sem ticket: o BoJ de 30/10 é manutenção em 1,25%, e o único livro direcional segue o short do GBP/USD em 1,3376",
                        summary: "Sexta de dados divididos e de iene. O flash da zona do euro veio em 51,9 (esperado 52,7), com a França de volta à contração (48,4) e o juro de 10 anos francês acima de 5% na semana (máxima de 5,14%, MUFG); o flash americano segurou 57,6, com preços de venda no ritmo mais alto desde agosto de 2022. No Reino Unido, as vendas no varejo caíram 0,4% (esperado -0,1%) e o PMI composto surpreendeu em 53,1. O WTI fechou a ~US$ 103. No livro: o USD/JPY fechou 156,80 (-0,16%), através de 157,00, e o próprio fechamento é a mínima de 10/20 pregões — até 156,00 são 80 pips, contra piso de 64, então o 1:2 não cabe; o EUR/JPY fechou 175,51 (-0,27%), segundo fechamento sob 176,85 e primeiro através da prateleira de out/2025, mas o stop estrutural sobre 177,00 joga o alvo dentro do cluster de set/2025 (~172,3-172,9); o GBP/JPY perdeu 210,00 (209,61) e parou 34 pips acima da mínima de 10 pregões, com piso de 117 pips. O GBP/USD (1,3368) apenas estendeu o short aberto em 22/10: 1º dos 10 pregões, stop 1.3460 e alvo 1.3250 intocados, expiração em 05/11. O EUR/USD (1,1193) não entrou em 1.1260-1.1300 — fade rearmado pela quarta vez. A premissa do BoJ é corrigida: a taxa já está em 1,25% desde setembro; Bloomberg (21-22/10) não tem economista esperando alta em 30/10, e 83% apontam dezembro para 1,50%.",
                        take: "O rompimento do iene chegou ao redondo e a mesa não o persegue: a distância até o próximo suporte é menor que o piso. O short da libra segue sendo gestão de ledger, não entrada nova. O cluster de quarta a sexta (FOMC, BCE, BoJ em manutenção) é o árbitro."
                    },
                    en: {
                        headline: "The yen closes under 157.00 and EUR/JPY pins a second low (175.51) — no ticket: the Oct-30 BoJ is a hold at 1.25%, and the only directional book is still the GBP/USD short from 1.3376",
                        summary: "A Friday of split data and of yen. The eurozone flash printed 51.9 (expected 52.7), with France back in contraction (48.4) and the French 10-year above 5% this week (a 5.14% high, MUFG); the US flash held at 57.6, with selling prices rising at the sharpest pace since August 2022. In the UK, retail sales fell 0.4% (expected -0.1%) and the composite PMI surprised at 53.1. WTI closed near $103. In the book: USD/JPY closed 156.80 (-0.16%), through 157.00, and the close itself is the 10/20-day low — 156.00 is 80 pips away, against a 64-pip floor, so the 1:2 does not fit; EUR/JPY closed 175.51 (-0.27%), the second close under 176.85 and the first through the Oct-2025 shelf, but the structural stop over 177.00 drops the target inside the Sep-2025 cluster (~172.3-172.9); GBP/JPY lost 210.00 (209.61) and stopped 34 pips above the 10-day low, with a 117-pip floor. GBP/USD (1.3368) only extended the short opened on Oct 22: 1st of 10 sessions, stop 1.3460 and target 1.3250 untouched, expiry Nov 5. EUR/USD (1.1193) did not enter 1.1260-1.1300 — the fade is re-armed a fourth time. The BoJ premise is corrected: the rate is already 1.25% since September; Bloomberg (Oct 21-22) has no economist expecting a hike on Oct 30, and 83% point to December for 1.50%.",
                        take: "The yen break reached the round and the desk does not chase it: the distance to the next support is shorter than the floor. The sterling short remains ledger management, not a new entry. The Wednesday-to-Friday cluster (FOMC, ECB, BoJ on hold) is the arbiter."
                    }
                },
'''
anchor = "            items: [\n"
assert html.count(anchor) == 1
html = sub1(html, anchor, anchor + news_item, "newsData prepend")

open(INDEX, "w", encoding="utf-8", newline="").write(html)
print("OK index.html")

news = open(NEWS, encoding="utf-8").read()
news = sub1(news, "Wire updated: " + OLD_STAMP, "Wire updated: " + STAMP, "news dateline EN")
news = sub1(news, "Telégrafo atualizado em: " + OLD_STAMP, "Telégrafo atualizado em: " + STAMP, "news dateline PT")
news = sub1(news,
    '<span class="cd-kicker"><span class="lang-en">Market Wire · Yen Sweep, Fade Fired</span><span class="lang-pt" style="display:none;">Telégrafo da Mesa · Varredura do Iene, Fade Disparado</span></span>',
    '<span class="cd-kicker"><span class="lang-en">Market Wire · Yen Under 157, Shelf Re-armed</span><span class="lang-pt" style="display:none;">Telégrafo da Mesa · Iene Sob 157, Prateleira Rearmada</span></span>',
    "news hero kicker")
news = sub1(news,
    '<span><span class="lang-en">6 pairs · FOMC + BoJ next week (27-30/10)</span><span class="lang-pt" style="display:none;">6 pares · FOMC + BoJ na semana (27-30/10)</span></span>',
    '<span><span class="lang-en">6 pairs · FOMC Wed 28 · ECB Thu 29 · BoJ Fri 30</span><span class="lang-pt" style="display:none;">6 pares · FOMC qua 28 · BCE qui 29 · BoJ sex 30</span></span>',
    "news dateline pair count")
news = sub1(news,
    '<span class="cal-event"><span class="lang-en">FOMC decision — blackout on</span><span class="lang-pt" style="display:none;">Decisão do FOMC — blackout vigente</span></span>',
    '<span class="cal-event"><span class="lang-en">FOMC — hold at 3.75-4.00% is the base case</span><span class="lang-pt" style="display:none;">FOMC — manutenção em 3,75-4,00% é o caso-base</span></span>',
    "calendar FOMC")
news = sub1(news,
    '<span class="cal-event"><span class="lang-en">BoJ decision (consensus: 1.25%)</span><span class="lang-pt" style="display:none;">Decisão do BoJ (consenso: 1,25%)</span></span>',
    '<span class="cal-event"><span class="lang-en">BoJ — hold at 1.25% (Dec hike to 1.50%)</span><span class="lang-pt" style="display:none;">BoJ — manutenção em 1,25% (alta a 1,50% em dez)</span></span>',
    "calendar BoJ")

card = '''                <!-- News 23/10/2026: yen closes under 157, EUR/JPY second break still fails the path; BoJ is a hold at 1.25% -->
                <article class="news-card">
                    <div class="news-card-top">
                        <span class="news-cat"><span class="lang-en">Market Flow</span><span class="lang-pt" style="display:none;">Fluxo &amp; Mercado</span></span>
                        <span class="impact-badge high"><span class="lang-en">High Impact</span><span class="lang-pt" style="display:none;">Impacto Alto</span></span>
                        <span class="news-date">23/10/2026</span>
                    </div>
                    <h2 class="news-title">
                        <span class="lang-en">The yen closes under 157.00 and EUR/JPY pins a second low (175.51) — no ticket: the Oct-30 BoJ is a hold at 1.25%, and the only directional book is still the GBP/USD short from 1.3376</span>
                        <span class="lang-pt" style="display:none;">O iene fecha sob 157,00 e o EUR/JPY crava a segunda mínima (175,51) — sem ticket: o BoJ de 30/10 é manutenção em 1,25%, e o único livro direcional segue o short do GBP/USD em 1,3376</span>
                    </h2>
                    <p class="news-summary">
                        <span class="lang-en">A Friday of split data and of yen. The eurozone flash printed 51.9 (expected 52.7), with France back in contraction (48.4) and the French 10-year above 5% this week (a 5.14% high, MUFG); the US flash held at 57.6, with selling prices rising at the sharpest pace since August 2022. In the UK, retail sales fell 0.4% (expected -0.1%) and the composite PMI surprised at 53.1. WTI closed near $103. In the book: USD/JPY closed 156.80 (-0.16%), through 157.00, and the close itself is the 10/20-day low — 156.00 is 80 pips away, against a 64-pip floor, so the 1:2 does not fit; EUR/JPY closed 175.51 (-0.27%), the second close under 176.85 and the first through the Oct-2025 shelf, but the structural stop over 177.00 drops the target inside the Sep-2025 cluster (~172.3-172.9); GBP/JPY lost 210.00 (209.61) and stopped 34 pips above the 10-day low, with a 117-pip floor. GBP/USD (1.3368) only extended the short opened on Oct 22: 1st of 10 sessions, stop 1.3460 and target 1.3250 untouched, expiry Nov 5. EUR/USD (1.1193) did not enter 1.1260-1.1300 — the fade is re-armed a fourth time. The BoJ premise is corrected: the rate is already 1.25% since September; Bloomberg (Oct 21-22) has no economist expecting a hike on Oct 30, and 83% point to December for 1.50%.</span>
                        <span class="lang-pt" style="display:none;">Sexta de dados divididos e de iene. O flash da zona do euro veio em 51,9 (esperado 52,7), com a França de volta à contração (48,4) e o juro de 10 anos francês acima de 5% na semana (máxima de 5,14%, MUFG); o flash americano segurou 57,6, com preços de venda no ritmo mais alto desde agosto de 2022. No Reino Unido, as vendas no varejo caíram 0,4% (esperado -0,1%) e o PMI composto surpreendeu em 53,1. O WTI fechou a ~US$ 103. No livro: o USD/JPY fechou 156,80 (-0,16%), através de 157,00, e o próprio fechamento é a mínima de 10/20 pregões — até 156,00 são 80 pips, contra piso de 64, então o 1:2 não cabe; o EUR/JPY fechou 175,51 (-0,27%), segundo fechamento sob 176,85 e primeiro através da prateleira de out/2025, mas o stop estrutural sobre 177,00 joga o alvo dentro do cluster de set/2025 (~172,3-172,9); o GBP/JPY perdeu 210,00 (209,61) e parou 34 pips acima da mínima de 10 pregões, com piso de 117 pips. O GBP/USD (1,3368) apenas estendeu o short aberto em 22/10: 1º dos 10 pregões, stop 1.3460 e alvo 1.3250 intocados, expiração em 05/11. O EUR/USD (1,1193) não entrou em 1.1260-1.1300 — fade rearmado pela quarta vez. A premissa do BoJ é corrigida: a taxa já está em 1,25% desde setembro; Bloomberg (21-22/10) não tem economista esperando alta em 30/10, e 83% apontam dezembro para 1,50%.</span>
                    </p>
                    <div class="news-take">
                        <span class="take-tag"><span class="lang-en">Desk take</span><span class="lang-pt" style="display:none;">Leitura da mesa</span></span>
                        <span class="lang-en">The yen break reached the round and the desk does not chase it: the distance to the next support is shorter than the floor. The sterling short remains ledger management, not a new entry. The Wednesday-to-Friday cluster (FOMC, ECB, BoJ on hold) is the arbiter.</span>
                        <span class="lang-pt" style="display:none;">O rompimento do iene chegou ao redondo e a mesa não o persegue: a distância até o próximo suporte é menor que o piso. O short da libra segue sendo gestão de ledger, não entrada nova. O cluster de quarta a sexta (FOMC, BCE, BoJ em manutenção) é o árbitro.</span>
                    </div>
                    <div class="news-pairs">
                        <span class="np-label"><span class="lang-en">Watch</span><span class="lang-pt" style="display:none;">Acompanhar</span></span>
                        <a href="eur-usd.html" class="pair-link-chip">EUR/USD</a><a href="usd-jpy.html" class="pair-link-chip">USD/JPY</a><a href="aud-usd.html" class="pair-link-chip">AUD/USD</a><a href="gbp-usd.html" class="pair-link-chip">GBP/USD</a><a href="eur-jpy.html" class="pair-link-chip">EUR/JPY</a><a href="gbp-jpy.html" class="pair-link-chip">GBP/JPY</a>
                    </div>
                </article>

'''
first_card = '                <!-- News 22/10/2026: UK CPI 3.5% fires the GBP/USD shelf fade; ~$99 WTI sweeps the yen, EUR/JPY pins the 9-month low -->'
assert news.count(first_card) == 1, "first news card anchor not found"
news = sub1(news, first_card, card + first_card, "news card prepend")
open(NEWS, "w", encoding="utf-8", newline="").write(news)
print("OK news.html")

led = json.load(open(LEDGER, encoding="utf-8"))
assert led["meta"]["lastUpdated"] == "22/10/2026"
led["meta"]["lastUpdated"] = "23/10/2026"

watching = led["watching"]
assert {t["pair"] for t in watching} == {"EUR/USD"}, "unexpected watching set: %s" % [t["pair"] for t in watching]
assert [t["pair"] for t in led["open"]] == ["GBP/USD"]

gbp = led["open"][0]
assert gbp["entry"] == 1.3376 and gbp["stop"] == 1.346 and gbp["target"] == 1.325
gbp_close = 1.33683
assert gbp_close < gbp["stop"], "GBP stop crossed"
assert gbp_close > gbp["target"], "GBP target crossed"
# open tickets are never modified

eur_old = watching[0]
eur_old["note"] = ("revoked in the 23/10 edition and re-armed on the same shelf: the 23/10 close "
                   "1.1193 did not enter 1.1260-1.1300 (12 pips above the 10-day low 1.1181); "
                   "validity re-stamped through the 30/10 close, with the 27-29/10 closes "
                   "(FOMC and ECB windows) not arming")
eur_old["outcome"] = "revoked"
eur_old["exitDate"] = "23/10/2026"
eur_old["entryDate"] = None
eur_old["realizedR"] = None
led["closed"].append(eur_old)
led["watching"] = [
    {
        "pair": "EUR/USD",
        "reportDate": "23/10/2026",
        "direction": "short",
        "setup": "pullback",
        "entry": 1.128,
        "stop": 1.136,
        "target": 1.112,
        "plannedR": 2.0,
        "triggerRule": "daily close inside 1.1260-1.1300 followed by a close below the previous close and the 1.1280 midpoint (entry reference 1.1280); only closes after the 23/10 report count and the 27-29/10 closes (FOMC and ECB windows) don't arm; valid through the 30/10 close",
        "note": "re-armed a fourth straight edition (18->20->22->23/10): the 23/10 close 1.1193 stayed 12 pips above the 10-day low and outside the shelf — stop 1.1360 (80 pips over the 29-30/09 double close 1.1355 and the 78.6% Fib 1.1348, >= the 55-pip 1.5-sigma20 floor), target 1.1120 under the 9-month low crossing only the 1.1150 round"
    }
]

json.dump(led, open(LEDGER, "w", encoding="utf-8", newline=""), ensure_ascii=False, indent=2)
open(LEDGER, "a", encoding="utf-8", newline="").write("\n")
print("OK track-record.json: EUR/USD re-armed, GBP/USD open unchanged (1.3368 neither stop nor target)")

sm = open(SITEMAP, encoding="utf-8").read()
for loc in ["https://newsforextrading.com/",
            "https://newsforextrading.com/news.html",
            "https://newsforextrading.com/eur-usd.html",
            "https://newsforextrading.com/usd-jpy.html",
            "https://newsforextrading.com/aud-usd.html",
            "https://newsforextrading.com/gbp-usd.html",
            "https://newsforextrading.com/eur-jpy.html",
            "https://newsforextrading.com/gbp-jpy.html",
            "https://newsforextrading.com/track-record.html"]:
    m = re.search(r"(<loc>%s</loc>\s*<lastmod>)[\d-]+(</lastmod>)" % re.escape(loc), sm)
    assert m, "sitemap missing %s" % loc
    sm = sm[:m.start()] + m.group(1) + "2026-10-23" + m.group(2) + sm[m.end():]
open(SITEMAP, "w", encoding="utf-8", newline="").write(sm)
print("OK sitemap")

ver = open(VERIFY, encoding="utf-8").read()
ver = sub1(ver, 'TODAY_TS = "22/10/2026 21:57 UTC"', 'TODAY_TS = "23/10/2026 18:10 UTC"', "verify ts")
ver = sub1(ver, 'TODAY_DATE = "22/10/2026"  # basis session date (report edition: 22/10/2026)',
           'TODAY_DATE = "23/10/2026"  # basis session date (report edition: 23/10/2026)', "verify date")
ver = sub1(ver,
    '''TICKER = [("EUR/USD","-0.26%"),("USD/JPY","-0.53%"),("AUD/USD","-0.31%"),
          ("GBP/USD","-0.19%"),("EUR/JPY","-0.78%"),("GBP/JPY","-0.72%")]''',
    '''TICKER = [("EUR/USD","-0.11%"),("USD/JPY","-0.16%"),("AUD/USD","+0.15%"),
          ("GBP/USD","-0.06%"),("EUR/JPY","-0.27%"),("GBP/JPY","-0.22%")]''',
    "verify ticker")
open(VERIFY, "w", encoding="utf-8", newline="").write(ver)
print("OK verify_all.py constants")
print("Build data written. Run build_static_pages.py + build_track_record_page.py + verify_all.py.")
