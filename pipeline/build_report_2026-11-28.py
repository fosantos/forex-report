#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""28/11/2026 Saturday week-ahead edition, on the Friday 27/11 ECB fixing
(595 sessions — no weekend session, so all levels are Friday's).

The holiday bounce repaired what the wall broke: AUD/USD (+99 pips in two
sessions) reclaimed the 0.6666 breakdown, GBP/USD (+62) reclaimed 1.3100,
EUR/USD faded back under 1.0968 after Thursday's reclaim, and GBP/JPY
(+127) retook 209.00. USD/JPY notched a fifth close over the SMA200 but
the map is still MIXED. The ECB minutes were hawkish (Dec 17 ≈93%) while
France (2.9%) and Spain (4.1%) flashes both missed big on fuel — Tuesday's
EZ flash (4.0% eyed) plus ISM/JOLTS, then payrolls Friday, gate every
trigger: all six stay on WAIT.
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
OLD_TS = "25/11/2026 20:11 UTC"
BASIS = "595 sessions, 01/08/2024 to 27/11/2026"
BASIS_PT = "595 pregões, 01/08/2024 a 27/11/2026"

def pair(quote, bias, bias_type, pt, en):
    return {"quote": quote, "bias": bias, "biasType": bias_type, "pt": pt, "en": en}

EUR = pair("1.0957", "BAIXA", "bear",
    pt={
        "fundamental": "Edição de sábado 28/11/2026, sobre a taxa de referência BCE/Frankfurter de sexta 27/11/2026 (sem pregão no fim de semana): o EUR/USD fechou a sexta em 1,0957, caindo -0,16% (-18 pips) a partir de 1,0975. O repique de +40 pips de quinta retomou o 1,0968 rompido na ata do BCE; a sexta devolveu na hora, fechando sob 1,0968 mas sobre o redondo 1.0950 — 22 pips acima da mínima de 9 meses de quarta em 1,0935, então o segundo fechamento sob ela que o gatilho pedia nunca saiu. A ata (quinta 12:30 UTC) veio hawkish — um número grande já bancaria alta em outubro — firmando 17/12 em ≈93%; depois os flashes de sexta furaram por baixo: França 2,9% (esperado 3,2%, outubro 3,4%, HICP 3,2%) e Espanha 4,1% (esperado 4,6%, outubro 4,9%, núcleo 2,6%), ambos no combustível barato. A semana abre no CPI prévio da Alemanha segunda e se decide na terça: flash do CPI da zona do euro (4,0% esperado, estável) mais ISM da indústria dos EUA (≈55 esperado) e JOLTS, com ADP quarta, ISM de serviços quinta e payroll sexta. O Fed está em 3,75-4,00% com 8-9/12 a ≈98% e o DXY perto de 104 (≈103,8-104,0 na sexta, ganho semanal). O piso de 1,5σ20 é de 63 pips. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (1,1484) com a SMA50 (1,1182) abaixo dela — alinhamento de baixa pleno. A mínima de 10/20 pregões e de 9 meses segue 1,0935 (25/11), 22 pips abaixo. A máxima de 10 pregões é 1,1014 (16/11). A de 20 pregões segue 1,1267 (04/11).",
        "support": "1.0950 (o redondo, 7 pips abaixo) e 1,0935 (a mínima de 9 meses de quarta).",
        "resistance": "1.0968 (a mínima rompida, retomada na quinta, 11 pips acima) e 1.1000.",
        "priceAction": "Quinta retomou 1,0968 na ata; sexta devolveu nos flashes fracos de FR/ES. O rompimento nunca ganhou o segundo fechamento. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "Nenhum gatilho impresso: quinta fechou sobre o rompimento, sexta fechou dentro da prateleira. Um short pede fechamento de segunda de volta para baixo — direto no CPI da Alemanha segunda e na muralha do flash ZE + ISM terça. Sem gatilho novo — reavaliar depois de terça.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O euro passou a semana de feriado testando o próprio rompimento e fechou dentro dele. Com o CPI alemão segunda e o flash ZE terça, não há entrada antes da muralha de inflação."
    },
    en={
        "fundamental": "Saturday 28/11/2026 edition, on the Friday 27/11/2026 ECB/Frankfurter reference rate (no weekend fixing): EUR/USD closed Friday at 1.0957, down -0.16% (-18 pips) from 1.0975. Thursday's +40-pip bounce reclaimed the broken 1.0968 on the ECB minutes; Friday handed it straight back, closing under 1.0968 but over the 1.0950 round — 22 pips above Wednesday's 9-month low of 1.0935, so the second close under it that the trigger needed never printed. The minutes (Thu 12:30 UTC) were hawkish — a large number could have backed an October hike — firming Dec 17 at ≈93%; then Friday's flashes undercut them: France 2.9% (3.2% eyed, October 3.4%, HICP 3.2%) and Spain 4.1% (4.6% eyed, October 4.9%, core 2.6%), both on cheaper fuel. The week opens on Germany's prelim CPI Monday and is decided Tuesday: eurozone flash CPI (4.0% eyed, unchanged) plus US ISM manufacturing (≈55 eyed) and JOLTS, with ADP Wednesday, ISM services Thursday and payrolls Friday. The Fed is at 3.75-4.00% with Dec 8-9 at ≈98% and the DXY near 104 (≈103.8-104.0 Friday, weekly gain). The 1.5-sigma20 floor is 63 pips. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (1.1484) with the SMA50 (1.1182) below it — full bear alignment. The 10/20-day and 9-month low is still 1.0935 (Nov 25), 22 pips below. The 10-day high is 1.1014 (Nov 16). The 20-day high is still 1.1267 (Nov 4).",
        "support": "1.0950 (the round, 7 pips below) and 1.0935 (Wednesday's 9-month low).",
        "resistance": "1.0968 (the broken 9-month low, reclaimed Thursday, 11 pips above) and 1.1000.",
        "priceAction": "Thursday reclaimed 1.0968 on the minutes; Friday handed it back on soft FR/ES flashes. The breakdown never got its second close. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "No trigger printed: Thursday closed over the breakdown, Friday closed inside the shelf. A short needs a Monday close back under Friday's — straight into Germany's CPI Monday and the EZ flash + ISM wall Tuesday. No new trigger — reassess after Tuesday.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The euro spent the holiday week testing its own breakdown and closed inside it. With German CPI Monday and the EZ flash Tuesday, there is no entry before the inflation wall."
    })

USDJPY = pair("159.54", "NEUTRO", "neutral",
    pt={
        "fundamental": "Edição de sábado 28/11/2026, sobre a taxa de referência BCE/Frankfurter de sexta 27/11/2026 (sem pregão no fim de semana): o USD/JPY fechou a sexta em 159,54, subindo +0,18% (+28 pips) a partir de 159,26 — o quinto fechamento seguido acima da SMA200 (158,92), 62 pips acima dela. Com a SMA50 (158,28) ainda abaixo da SMA200, o mapa segue MISTO pela segunda edição. A máxima de 10 pregões rolou para 159,97 (19/11) com a saída dos 160,00 de 13/11 — 43 pips acima, com a Fib 38,2% em 159,85 na frente — e a máxima de 20 pregões segue o teto 160,00; nenhum rompimento impresso para nenhum lado. O CPI de Tóquio de novembro veio como esperado: núcleo 2,9% (mais rápido desde julho de 2025), cheio 2,8% estável, núcleo-núcleo aliviando a 2,5% — a alta do BoJ a 1,50% em dezembro (BoJ em 1,25%) segue ≈85-86% para 17-18/12. Os avisos do MoF de 12-13/11 seguem dentro de 30 dias sem intervenção confirmada, então o piso segue em 2,5σ20: 124 pips. Ueda fala na segunda; a semana de emprego dos EUA (ISM + JOLTS terça, ADP quarta, ISM de serviços quinta, payroll sexta) decide a perna do dólar até o FOMC de 8-9/12 (≈98%). Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento acima da SMA200 (158,92) com a SMA50 (158,28) abaixo dela — MISTO, sem alinhamento, cinco pregões em sequência. A máxima de 10 pregões agora é 159,97 (19/11); a de 20 segue 160,00. A mínima de 10 pregões é 158,64 (20/11); a de 20 agora é 157,90. O intervalo de 9 meses segue 163,91/153,27.",
        "support": "158.92 (a SMA200, 62 pips abaixo) e 158,64 (a mínima de 10 pregões).",
        "resistance": "159.97 (a máxima de 10 pregões, 43 pips acima) e 160,00 (a máxima de 20 pregões).",
        "priceAction": "Cinco fechamentos sobre a SMA200, moendo 43 pips sob uma máxima cadente de 10 pregões. O CPI de Tóquio passou em linha; Ueda fala segunda. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "Nenhum rompimento impresso: 159,97 trava o topo, 158,64 segura o fundo. O mapa misto pede um fechamento além de um deles — com Ueda segunda e ISM terça, nenhum é operável contra a muralha. Sem gatilho.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O par segue batendo sob 159,97 com o mapa misto por definição. Comprar o teto antes de Ueda e do ISM, ou vender cinco fechamentos sobre a SMA200, brigam com o manual."
    },
    en={
        "fundamental": "Saturday 28/11/2026 edition, on the Friday 27/11/2026 ECB/Frankfurter reference rate (no weekend fixing): USD/JPY closed Friday at 159.54, up +0.18% (+28 pips) from 159.26 — the fifth straight close above the SMA200 (158.92), 62 pips above it. With the SMA50 (158.28) still below the SMA200, the map is MIXED for a second edition. The 10-day high rolled down to 159.97 (Nov 19) as Nov 13's 160.00 aged out — 43 pips above, with the 38.2% Fib at 159.85 in front of it — and the 20-day high is still the 160.00 cap; no breakout has printed either way. November Tokyo CPI landed as eyed: core 2.9% (fastest since July 2025), headline 2.8% unchanged, core-core easing to 2.5% — the December BoJ hike to 1.50% (BoJ at 1.25%) stays ≈85-86% for Dec 17-18. The MoF's Nov 12-13 warnings are still inside 30 days with no confirmed intervention, so the floor stays at 2.5-sigma20: 124 pips. Governor Ueda speaks Monday; the US jobs week (ISM + JOLTS Tue, ADP Wed, ISM services Thu, payrolls Fri) decides the dollar leg into the Dec 8-9 FOMC (≈98%). Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close above the SMA200 (158.92) with the SMA50 (158.28) below it — MIXED, neither alignment, five closes running. The 10-day high is now 159.97 (Nov 19); the 20-day high is still 160.00. The 10-day low is 158.64 (Nov 20); the 20-day low is now 157.90. The 9-month range is still 163.91/153.27.",
        "support": "158.92 (the SMA200, 62 pips below) and 158.64 (the 10-day low).",
        "resistance": "159.97 (the 10-day high, 43 pips above) and 160.00 (the 20-day high).",
        "priceAction": "Five closes over the SMA200, grinding 43 pips under a falling 10-day high. Tokyo CPI passed in line; Ueda speaks Monday. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "No breakout has printed: 159.97 caps the top, 158.64 holds the bottom. The mixed map needs a daily close beyond one of them — with Ueda Monday and ISM Tuesday, none is tradeable into the wall. No trigger.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The pair keeps knocking under 159.97 with the map mixed by definition. Buying the cap into Ueda and ISM, or selling five closes over the SMA200, both fight the rulebook."
    })

AUD = pair("0.6668", "BAIXA", "bear",
    pt={
        "fundamental": "Edição de sábado 28/11/2026, sobre a taxa de referência BCE/Frankfurter de sexta 27/11/2026 (sem pregão no fim de semana): o AUD/USD fechou a sexta em 0,6668, subindo +0,50% (+33 pips) a partir de 0,6635 — quinta +65 pips, sexta +33: um repique de +99 pips em dois pregões que retomou o rompimento de 0,6666 — o gatilho de venda está anulado e pede nova prova. A cascata elevou o σ20 a 42 pips, então o piso de 1,5σ20 agora é de 63 pips. A batida do CPI de outubro (4,9%, núcleo aparado 3,8%) está digerida; o RBA está em 4,85% e decide em 8/12 com manutenção a ≈80-100%. Segunda traz os PMIs de novembro da China — dado da China dentro de 24 horas do próximo pregão — e quarta traz o PIB do 3º tri da Austrália; sexta é payroll dos EUA. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (0,7034) com a SMA50 (0,6919) abaixo dela — alinhamento de baixa pleno. A mínima de 10/20 pregões e de 9 meses segue 0,6570 (25/11), 99 pips abaixo. A máxima de 10 pregões é 0,6757 (16/11). A de 20 pregões segue 0,7015.",
        "support": "0.6600 (o redondo, 68 pips abaixo) e 0,6570 (a mínima de 9 meses de quarta).",
        "resistance": "0.6700 (o redondo, 32 pips acima).",
        "priceAction": "Um repique de feriado de 99 pips retomou o rompimento de 0,6666 e anulou o gatilho de venda. Os PMIs da China saem segunda. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "O rompimento está reparado: sexta fechou de volta acima de 0,6666. Um short novo pede fechamento de segunda de volta sob o de sexta — direto nos PMIs da China. Sem gatilho novo — reavaliar depois do dado de segunda e do PIB australiano de quarta.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O Aussie retomou em duas sessões finas o que a muralha tomou na quarta. Vender o reparo antes dos PMIs da China, com o piso reprecificado a 63, não é ticket."
    },
    en={
        "fundamental": "Saturday 28/11/2026 edition, on the Friday 27/11/2026 ECB/Frankfurter reference rate (no weekend fixing): AUD/USD closed Friday at 0.6668, up +0.50% (+33 pips) from 0.6635 — Thursday +65 pips, Friday +33: a +99-pip two-day bounce that reclaimed the 0.6666 breakdown — the short trigger is void and needs re-proof. The cascade lifted sigma20 to 42 pips, so the 1.5-sigma20 floor is now 63 pips. October CPI's beat (4.9%, trimmed 3.8%) is digested; the RBA is at 4.85% and decides Dec 8 with a hold at ≈80-100%. Monday brings China's November PMIs — China data inside 24 hours of the next session — and Wednesday brings Australia's Q3 GDP; Friday is US payrolls. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (0.7034) with the SMA50 (0.6919) below it — full bear alignment. The 10/20-day and 9-month low is still 0.6570 (Nov 25), 99 pips below. The 10-day high is 0.6757 (Nov 16). The 20-day high is still 0.7015.",
        "support": "0.6600 (the round, 68 pips below) and 0.6570 (Wednesday's 9-month low).",
        "resistance": "0.6700 (the round, 32 pips above).",
        "priceAction": "A 99-pip holiday bounce reclaimed the 0.6666 breakdown and voided the short trigger. China PMIs land Monday. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The breakdown is repaired: Friday closed back above 0.6666. A fresh short needs a Monday close back under Friday's — straight into China's PMIs. No new trigger — reassess after Monday's data and Wednesday's AU GDP.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The Aussie took back in two thin sessions what the wall took on Wednesday. Shorting the repair into China PMIs, with the floor repriced to 63, is not a ticket."
    })

GBP = pair("1.3121", "BAIXA", "bear",
    pt={
        "fundamental": "Edição de sábado 28/11/2026, sobre a taxa de referência BCE/Frankfurter de sexta 27/11/2026 (sem pregão no fim de semana): o GBP/USD fechou a sexta em 1,3121, subindo +0,14% (+18 pips) a partir de 1,3104 — quinta +44 pips, sexta +18: um repique de +62 pips em dois pregões desde a mínima de 9 meses de quarta, que retomou o redondo 1.3100 e parou 4 pips sob a mínima de 1,3125 (20/11). O Relatório de Estabilidade Financeira do BoE (quinta) alertou sobre endividamento em IA e valuations esticados, sem sinal de política; a Bank Rate está em 4,00% e o Banco decide em 17/12. O CPI de outubro (3,6%) e os salários suaves estão digeridos. O short pede fechamento de segunda de volta para baixo — contra o ISM da indústria + JOLTS dos EUA terça (≈24h depois de uma entrada de segunda), ADP quarta e payroll sexta, com o flash do CPI da ZE terça movendo todo o bloco europeu. O piso de 1,5σ20 é de 67 pips. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (1,3393) e sob a SMA50 (1,3276), com a SMA50 abaixo da SMA200 — alinhamento de baixa pleno. A mínima de 10/20 pregões e de 9 meses segue 1,3060 (25/11), 62 pips abaixo. A máxima de 10 pregões é 1,3198 (16/11). A de 20 pregões segue 1,3500 (04/11).",
        "support": "1.3100 (o redondo retomado, 21 pips abaixo) e 1,3060 (a mínima de 9 meses de quarta).",
        "resistance": "1.3125 (a mínima de 20/11, 4 pips acima) e 1,3198 (a máxima de 10 pregões).",
        "priceAction": "Um repique de 62 pips retomou 1,3100 e estacionou 4 pips sob 1,3125. O FSR passou sem sinal; o ISM de terça manda no próximo movimento. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "O rompimento está meio reparado: sexta fechou de volta sobre 1,3100. Um short novo pede fechamento de segunda de volta sob o de sexta — contra ISM + JOLTS terça. Sem gatilho novo — reavaliar depois de terça.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "A libra reparou o rompimento na fita fina. A tese de venda pede nova prova depois do ISM, não perseguição antes dele."
    },
    en={
        "fundamental": "Saturday 28/11/2026 edition, on the Friday 27/11/2026 ECB/Frankfurter reference rate (no weekend fixing): GBP/USD closed Friday at 1.3121, up +0.14% (+18 pips) from 1.3104 — Thursday +44 pips, Friday +18: a +62-pip two-day bounce off Wednesday's 9-month low that reclaimed the 1.3100 round and stopped 4 pips under the Nov-20 low of 1.3125. The BoE's Financial Stability Report (Thu) warned on AI borrowing and stretched valuations with no policy signal; Bank Rate is 4.00% and the Bank decides Dec 17. October CPI (3.6%) and soft pay are digested. The short needs a Monday close back down — into US ISM manufacturing + JOLTS Tuesday (≈24h after a Monday entry), ADP Wednesday and payrolls Friday, with Tuesday's EZ flash CPI moving the whole European bloc. The 1.5-sigma20 floor is 67 pips. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (1.3393) and under the SMA50 (1.3276), with the SMA50 below the SMA200 — full bear alignment. The 10/20-day and 9-month low is still 1.3060 (Nov 25), 62 pips below. The 10-day high is 1.3198 (Nov 16). The 20-day high is still 1.3500 (Nov 4).",
        "support": "1.3100 (the reclaimed round, 21 pips below) and 1.3060 (Wednesday's 9-month low).",
        "resistance": "1.3125 (the Nov-20 low, 4 pips above) and 1.3198 (the 10-day high).",
        "priceAction": "A 62-pip bounce reclaimed 1.3100 and parked 4 pips under 1.3125. The FSR passed without a signal; ISM Tuesday owns the next move. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The breakdown is half-repaired: Friday closed back over 1.3100. A fresh short needs a Monday close back under Friday's — into ISM + JOLTS Tuesday. No new trigger — reassess after Tuesday.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "Sterling repaired its breakdown on thin tape. The short thesis needs re-proof after ISM, not a chase into it."
    })

EURJPY = pair("174.81", "BAIXA", "bear",
    pt={
        "fundamental": "Edição de sábado 28/11/2026, sobre a taxa de referência BCE/Frankfurter de sexta 27/11/2026 (sem pregão no fim de semana): o EUR/JPY fechou a sexta em 174,81, subindo +0,01% (+2 pips) a partir de 174,79 — os +57 pips de quinta fizeram o trabalho: +80 pips desde a mínima de 9 meses de segunda em 174,01, estacionado 19 pips sob o redondo 175,00. A ata do BCE (hawkish, 17/12 a ≈93%) e o CPI de Tóquio (núcleo 2,9% como esperado) já passaram; o painel zera segunda com o CPI prévio da Alemanha e Ueda falando, depois o flash do CPI da zona do euro terça (4,0% esperado) — os dois lados do cruzado encaram eventos top dentro de 48 horas. Os flashes fracos de sexta na França (2,9%) e Espanha (4,1%) sugerem que o flash ZE pode errar. O aviso do MoF mantém o piso em 2,5σ20: 190 pips — qualquer stop legal já atravessa 176,00. O BCE decide em 17/12 (depósito 2,50%); o BoJ decide em 17-18/12 (1,25%, ≈86% para 1,50%). A SMA50 está em 176,98 e a SMA200 em 182,49. Alinhamento de baixa. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (182,49) com a SMA50 (176,98) abaixo dela — alinhamento de baixa pleno. A mínima de 10/20 pregões e de 9 meses segue 174,01 (23/11), 80 pips abaixo. A máxima de 10 pregões é 175,84 (19/11).",
        "support": "174.01 (a mínima de 10/20 pregões e de 9 meses, 80 pips abaixo).",
        "resistance": "175.00 (o redondo, 19 pips acima), com a SMA50 em 176,98.",
        "priceAction": "Os 57 pips de quinta tiraram o cruzado 80 pips da mínima; sexta somou 2. CPI alemão segunda, flash ZE terça. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "Nenhum rompimento por perto: sexta fechou 80 pips sobre 174,01. O CPI da Alemanha segunda e o flash ZE terça caem dentro de 48 horas. Sem gatilho — reavaliar depois de terça.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O cruzado repicou com a fita de feriado e agora encara dois números de inflação em dois dias. Não há gatilho que sobreviva aos dois."
    },
    en={
        "fundamental": "Saturday 28/11/2026 edition, on the Friday 27/11/2026 ECB/Frankfurter reference rate (no weekend fixing): EUR/JPY closed Friday at 174.81, up +0.01% (+2 pips) from 174.79 — Thursday's +57 pips did the work: +80 pips off Monday's 9-month low of 174.01, parked 19 pips under the 175.00 round. The ECB minutes (hawkish, Dec 17 ≈93%) and Tokyo CPI (core 2.9% as eyed) both passed; the board resets Monday with Germany's prelim CPI and Ueda speaking, then Tuesday's eurozone flash CPI (4.0% eyed) — both sides of the cross face top-tier events inside 48 hours. Friday's soft French (2.9%) and Spanish (4.1%) flashes argue the EZ flash can miss. The MoF warning keeps the floor at 2.5-sigma20: 190 pips — any legal stop is already through 176.00. The ECB decides Dec 17 (deposit 2.50%); the BoJ decides Dec 17-18 (1.25%, ≈86% for 1.50%). The SMA50 is at 176.98 and the SMA200 at 182.49. Bear alignment. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (182.49) with the SMA50 (176.98) below it — full bear alignment. The 10/20-day and 9-month low is still 174.01 (Nov 23), 80 pips below. The 10-day high is 175.84 (Nov 19).",
        "support": "174.01 (the 10/20-day and 9-month low, 80 pips below).",
        "resistance": "175.00 (the round, 19 pips above), with the SMA50 at 176.98.",
        "priceAction": "Thursday's 57 pips lifted the cross 80 pips off its low; Friday added 2. German CPI Monday, EZ flash Tuesday. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "No breakdown is near: Friday closed 80 pips over 174.01. Germany's CPI Monday and the EZ flash Tuesday both land inside 48 hours. No trigger — reassess after Tuesday.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The cross bounced with the holiday tape and now faces two inflation prints in two days. There is no trigger that survives both."
    })

GBPJPY = pair("209.34", "BAIXA", "bear",
    pt={
        "fundamental": "Edição de sábado 28/11/2026, sobre a taxa de referência BCE/Frankfurter de sexta 27/11/2026 (sem pregão no fim de semana): o GBP/JPY fechou a sexta em 209,34, subindo +0,31% (+65 pips) a partir de 208,69 — quinta +62, sexta +65: um repique de +127 pips em dois pregões que retomou o redondo 209,00 (+34 pips acima) e anulou o rompimento; a mínima de 9 meses de 207,91 (09/09) está 143 pips abaixo. O CPI de Tóquio passou como esperado (núcleo 2,9%) com a alta do BoJ em 17-18/12 a ≈86% (BoJ em 1,25%); Ueda fala segunda. O FSR do BoE passou sem sinal de política (BoE em 4,00%, decide 17/12). A cascata reprecificou o piso de 2,5σ20 a 205 pips — um stop legal daqui cruza 210,00 e a máxima de 10 pregões. O payroll de sexta e o FOMC de 8-9/12 (≈98%) mandam na semana. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (212,82) e sob a SMA50 (210,12), com a SMA50 sob a SMA200 — alinhamento de baixa pleno. A mínima de 10/20 pregões segue 207,96 (23/11); a mínima de 9 meses é 207,91 (09/09), 143 pips abaixo. A máxima de 10 pregões é 210,65 (16/11).",
        "support": "209.00 (o redondo retomado, 34 pips abaixo) e 207,91 (a mínima de 9 meses).",
        "resistance": "210.00 (o redondo, 66 pips acima) e 210,65 (a máxima de 10 pregões).",
        "priceAction": "Um repique de 127 pips em dois pregões retomou 209,00 e anulou o rompimento. Ueda fala segunda; payroll sexta. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "O rompimento está reparado: sexta fechou 127 pips sobre o fechamento de quarta. Nenhum gatilho por perto, e o piso de 205 não cabe em nada. Sem gatilho — reavaliar num novo fechamento de rompimento.",
        "stop": "N/A (sem operação).",
        "target": "N/A (sem operação).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O cruzado retomou o rompimento em duas sessões finas. O short pede um rompimento novo, não perseguição do reparo."
    },
    en={
        "fundamental": "Saturday 28/11/2026 edition, on the Friday 27/11/2026 ECB/Frankfurter reference rate (no weekend fixing): GBP/JPY closed Friday at 209.34, up +0.31% (+65 pips) from 208.69 — Thursday +62, Friday +65: a +127-pip two-day bounce that reclaimed the 209.00 round (+34 pips over it) and voided the breakdown; the 9-month low of 207.91 (Sep 9) is 143 pips below. Tokyo CPI passed as eyed (core 2.9%) with the BoJ Dec 17-18 hike at ≈86% (BoJ at 1.25%); Ueda speaks Monday. The BoE's FSR passed without a policy signal (BoE at 4.00%, decides Dec 17). The cascade repriced the 2.5-sigma20 floor to 205 pips — a legal stop from here crosses 210.00 and the 10-day high. Friday's payrolls and the Dec 8-9 FOMC (≈98%) own the week after. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (212.82) and under the SMA50 (210.12), with the SMA50 under the SMA200 — full bear alignment. The 10/20-day low is still 207.96 (Nov 23); the 9-month low is 207.91 (Sep 9), 143 pips below. The 10-day high is 210.65 (Nov 16).",
        "support": "209.00 (the reclaimed round, 34 pips below) and 207.91 (the 9-month low).",
        "resistance": "210.00 (the round, 66 pips above) and 210.65 (the 10-day high).",
        "priceAction": "A 127-pip two-day bounce reclaimed 209.00 and voided the breakdown. Ueda speaks Monday; payrolls Friday. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The breakdown is repaired: Friday closed 127 pips over Wednesday's close. No trigger is near, and the 205-pip floor fits nothing. No trigger — reassess on a fresh breakdown close.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The cross took back the breakdown in two thin sessions. The short needs a new breakdown, not a chase of the repair."
    })

DATA = {
    "EUR/USD": EUR, "USD/JPY": USDJPY, "AUD/USD": AUD,
    "GBP/USD": GBP, "EUR/JPY": EURJPY, "GBP/JPY": GBPJPY,
}
DRIVERS = {
    "EUR/USD": {
        "en": ["1.0957 fades back under 1.0968", "Hawkish minutes vs soft FR/ES CPI", "EZ flash CPI Tue, NFP Fri"],
        "pt": ["1,0957 devolve 1,0968", "Ata hawkish vs CPI fraco FR/ES", "CPI da ZE 3ª, payroll 6ª"],
    },
    "USD/JPY": {
        "en": ["159.54, 5th close over the SMA200", "Still MIXED, 159.97 caps, floor 124", "Tokyo CPI 2.9% in line, Ueda Mon"],
        "pt": ["159,54, 5º pregão sobre a SMA200", "Ainda MISTO, 159,97 trava, piso 124", "CPI Tóquio 2,9% em linha, Ueda 2ª"],
    },
    "AUD/USD": {
        "en": ["0.6668 reclaims the breakdown", "+99 pips off Wed low, floor now 63", "China PMI Mon, AU GDP Wed"],
        "pt": ["0,6668 retoma o rompimento", "+99 pips da mínima, piso agora 63", "PMI China 2ª, PIB Austrália 4ª"],
    },
    "GBP/USD": {
        "en": ["1.3121 reclaims 1.3100, tests 1.3125", "FSR is AI-debt warning, no signal", "ISM Tue, NFP Fri gate the short"],
        "pt": ["1,3121 retoma 1,3100, testa 1,3125", "FSR alerta IA, sem sinal", "ISM 3ª, payroll 6ª travam o short"],
    },
    "EUR/JPY": {
        "en": ["174.81, +80 pips off Monday low", "German CPI Mon, EZ flash Tue", "Floor 190, both events within 48h"],
        "pt": ["174,81, +80 pips da mínima de 2ª", "CPI alemão 2ª, flash ZE 3ª", "Piso 190, dois eventos em 48h"],
    },
    "GBP/JPY": {
        "en": ["209.34 reclaims 209.00, +127 pips", "Breakdown void, floor now 205", "Ueda Mon, NFP Fri"],
        "pt": ["209,34 retoma 209,00, +127 pips", "Rompimento anulado, piso agora 205", "Ueda 2ª, payroll 6ª"],
    },
}

NEWS_ITEM_JS = r'''                {
                    date: "28/11/2026",
                    category: "macro",
                    impact: "high",
                    pairs: ["EUR/USD", "USD/JPY", "AUD/USD", "GBP/USD", "EUR/JPY", "GBP/JPY"],
                    pt: {
                        headline: "Edição de sábado para a semana: o repique de feriado repara três rompimentos no fixing de sexta; ata hawkish do BCE encontra flashes fracos de FR/ES antes do CPI da ZE terça — os seis em AGUARDAR",
                        summary: "Edição de sábado 28/11/2026, sobre o fixing BCE/Frankfurter de sexta 27/11 (595 pregões) — sem pregão no fim de semana, então os níveis são os de sexta. EUR/USD 1,0957 (−0,16%) devolveu para sob 1,0968 depois da retomada de quinta no dia da ata, 22 pips sobre a mínima de 9 meses de quarta; nenhum segundo fechamento sob 1,0935 saiu. USD/JPY 159,54 (+0,18%) marcou o quinto fechamento sobre a SMA200 (158,92) — ainda MISTO — 43 pips sob a nova máxima de 10 pregões 159,97, com o núcleo do CPI de Tóquio em 2,9% como esperado. AUD/USD 0,6668 (+0,50%) repicou 99 pips em dois pregões e retomou o rompimento de 0,6666, anulando o short; piso reprecificado a 63. GBP/USD 1,3121 (+0,14%) repicou 62 pips, retomou 1,3100 e estacionou 4 pips sob 1,3125; o FSR do BoE alertou sobre dívida de IA sem sinal de política. EUR/JPY 174,81 (+0,01%) segue 80 pips fora da mínima de segunda; GBP/JPY 209,34 (+0,31%) retomou 209,00 com repique de 127 pips em dois pregões. A ata firmou a alta do BCE em 17/12 a ≈93%, mas os flashes de França (2,9%) e Espanha (4,1%) erraram feio no combustível — o flash ZE de terça (4,0% esperado) está vivo. A semana: PMIs da China + CPI alemão + Ueda segunda, CPI ZE + ISM + JOLTS terça, ADP + PIB da Austrália quarta, payroll sexta. Fed 8-9/12 ≈98%, RBA 8/12, BoE/BCE/BoJ em meados de dezembro. Cada gatilho pede nova prova depois da muralha: os seis ficam em AGUARDAR.",
                        take: "A fita fina reparou o que a muralha quebrou — mas reparo feito no volume do Thanksgiving não ganha ticket. A mesa espera a trinca de inflação de terça e o payroll de sexta embaralhar o mapa."
                    },
                    en: {
                        headline: "Saturday week-ahead edition: the holiday bounce repairs three breakdowns on Friday's fixing; hawkish ECB minutes meet soft FR/ES flashes into Tuesday's EZ CPI — all six WAIT",
                        summary: "Saturday 28/11/2026 edition, on the Friday 27/11 ECB/Frankfurter fixing (595 sessions) — no weekend session, so the levels are Friday's. EUR/USD 1.0957 (−0.16%) faded back under 1.0968 after Thursday's minutes-day reclaim, 22 pips over Wednesday's 9-month low; no second close under 1.0935 printed. USD/JPY 159.54 (+0.18%) notched a fifth close over the SMA200 (158.92) — still MIXED — 43 pips under the new 10-day high 159.97, with Tokyo core CPI at 2.9% as eyed. AUD/USD 0.6668 (+0.50%) bounced 99 pips in two sessions and reclaimed the 0.6666 breakdown, voiding the short; floor repriced to 63. GBP/USD 1.3121 (+0.14%) bounced 62 pips, reclaimed 1.3100 and parked 4 pips under 1.3125; the BoE FSR warned on AI debt with no policy signal. EUR/JPY 174.81 (+0.01%) sits 80 pips off Monday's low; GBP/JPY 209.34 (+0.31%) reclaimed 209.00 with a 127-pip two-day bounce. The minutes firmed the ECB Dec 17 hike at ≈93%, but France (2.9%) and Spain (4.1%) flashes both missed big on fuel — Tuesday's EZ flash (4.0% eyed) is live. The week: China PMIs + German CPI + Ueda Monday, EZ CPI + ISM + JOLTS Tuesday, ADP + AU GDP Wednesday, payrolls Friday. Fed Dec 8-9 ≈98%, RBA Dec 8, BoE/ECB/BoJ mid-December. Every trigger needs re-proof after the wall: all six stay on WAIT.",
                        take: "Thin tape repaired what the wall broke — but repairs made on Thanksgiving volume earn no tickets. The desk waits for Tuesday's inflation double-header and Friday's payrolls to re-deal the map."
                    }
                },
'''

NEWS_CARD = r'''                <!-- News 28/11/2026: Saturday week-ahead edition; holiday bounce repairs breakdowns; EZ flash Tuesday; all six WAIT -->
                <article class="news-card">
                    <div class="news-card-top">
                        <span class="news-cat"><span class="lang-en">Macro Data</span><span class="lang-pt" style="display:none;">Dados Macro</span></span>
                        <span class="impact-badge high"><span class="lang-en">High Impact</span><span class="lang-pt" style="display:none;">Impacto Alto</span></span>
                        <span class="news-date">28/11/2026</span>
                    </div>
                    <h2 class="news-title">
                        <span class="lang-en">Saturday week-ahead edition: the holiday bounce repairs three breakdowns on Friday's fixing; hawkish ECB minutes meet soft FR/ES flashes into Tuesday's EZ CPI — all six WAIT</span>
                        <span class="lang-pt" style="display:none;">Edição de sábado para a semana: o repique de feriado repara três rompimentos no fixing de sexta; ata hawkish do BCE encontra flashes fracos de FR/ES antes do CPI da ZE terça — os seis em AGUARDAR</span>
                    </h2>
                    <p class="news-summary">
                        <span class="lang-en">Saturday 28/11/2026 edition, on the Friday 27/11 ECB/Frankfurter fixing (595 sessions) — no weekend session, so the levels are Friday's. EUR/USD 1.0957 (−0.16%) faded back under 1.0968 after Thursday's minutes-day reclaim, 22 pips over Wednesday's 9-month low; no second close under 1.0935 printed. USD/JPY 159.54 (+0.18%) notched a fifth close over the SMA200 (158.92) — still MIXED — 43 pips under the new 10-day high 159.97, with Tokyo core CPI at 2.9% as eyed. AUD/USD 0.6668 (+0.50%) bounced 99 pips in two sessions and reclaimed the 0.6666 breakdown, voiding the short; floor repriced to 63. GBP/USD 1.3121 (+0.14%) bounced 62 pips, reclaimed 1.3100 and parked 4 pips under 1.3125; the BoE FSR warned on AI debt with no policy signal. EUR/JPY 174.81 (+0.01%) sits 80 pips off Monday's low; GBP/JPY 209.34 (+0.31%) reclaimed 209.00 with a 127-pip two-day bounce. The minutes firmed the ECB Dec 17 hike at ≈93%, but France (2.9%) and Spain (4.1%) flashes both missed big on fuel — Tuesday's EZ flash (4.0% eyed) is live. The week: China PMIs + German CPI + Ueda Monday, EZ CPI + ISM + JOLTS Tuesday, ADP + AU GDP Wednesday, payrolls Friday. Fed Dec 8-9 ≈98%, RBA Dec 8, BoE/ECB/BoJ mid-December. Every trigger needs re-proof after the wall: all six stay on WAIT.</span>
                        <span class="lang-pt" style="display:none;">Edição de sábado 28/11/2026, sobre o fixing BCE/Frankfurter de sexta 27/11 (595 pregões) — sem pregão no fim de semana, então os níveis são os de sexta. EUR/USD 1,0957 (−0,16%) devolveu para sob 1,0968 depois da retomada de quinta no dia da ata, 22 pips sobre a mínima de 9 meses de quarta; nenhum segundo fechamento sob 1,0935 saiu. USD/JPY 159,54 (+0,18%) marcou o quinto fechamento sobre a SMA200 (158,92) — ainda MISTO — 43 pips sob a nova máxima de 10 pregões 159,97, com o núcleo do CPI de Tóquio em 2,9% como esperado. AUD/USD 0,6668 (+0,50%) repicou 99 pips em dois pregões e retomou o rompimento de 0,6666, anulando o short; piso reprecificado a 63. GBP/USD 1,3121 (+0,14%) repicou 62 pips, retomou 1,3100 e estacionou 4 pips sob 1,3125; o FSR do BoE alertou sobre dívida de IA sem sinal de política. EUR/JPY 174,81 (+0,01%) segue 80 pips fora da mínima de segunda; GBP/JPY 209,34 (+0,31%) retomou 209,00 com repique de 127 pips em dois pregões. A ata firmou a alta do BCE em 17/12 a ≈93%, mas os flashes de França (2,9%) e Espanha (4,1%) erraram feio no combustível — o flash ZE de terça (4,0% esperado) está vivo. A semana: PMIs da China + CPI alemão + Ueda segunda, CPI ZE + ISM + JOLTS terça, ADP + PIB da Austrália quarta, payroll sexta. Fed 8-9/12 ≈98%, RBA 8/12, BoE/BCE/BoJ em meados de dezembro. Cada gatilho pede nova prova depois da muralha: os seis ficam em AGUARDAR.</span>
                    </p>
                    <div class="news-take">
                        <span class="take-tag"><span class="lang-en">Desk take</span><span class="lang-pt" style="display:none;">Leitura da mesa</span></span>
                        <span class="lang-en">Thin tape repaired what the wall broke — but repairs made on Thanksgiving volume earn no tickets. The desk waits for Tuesday's inflation double-header and Friday's payrolls to re-deal the map.</span>
                        <span class="lang-pt" style="display:none;">A fita fina reparou o que a muralha quebrou — mas reparo feito no volume do Thanksgiving não ganha ticket. A mesa espera a trinca de inflação de terça e o payroll de sexta embaralhar o mapa.</span>
                    </div>
                    <div class="news-pairs">
                        <span class="np-label"><span class="lang-en">Watch</span><span class="lang-pt" style="display:none;">Acompanhar</span></span>
                        <a href="eur-usd.html" class="pair-link-chip">EUR/USD</a><a href="usd-jpy.html" class="pair-link-chip">USD/JPY</a><a href="aud-usd.html" class="pair-link-chip">AUD/USD</a><a href="gbp-usd.html" class="pair-link-chip">GBP/USD</a><a href="eur-jpy.html" class="pair-link-chip">EUR/JPY</a><a href="gbp-jpy.html" class="pair-link-chip">GBP/JPY</a>
                    </div>
                </article>

'''

NEW_CAL = '''                <div class="cal-cell">
                    <span class="cal-date">30/11</span>
                    <span class="cal-event"><span class="lang-en">China PMIs · German prelim CPI · Ueda speaks</span><span class="lang-pt" style="display:none;">PMIs da China · CPI prévio alemão · Ueda fala</span></span>
                    <div class="cal-meta"><span class="cal-impact high" aria-hidden="true"></span><span class="cal-cur">EUR</span></div>
                </div>
                <div class="cal-cell">
                    <span class="cal-date">01/12</span>
                    <span class="cal-event"><span class="lang-en">EZ flash CPI 4.0% eyed · ISM mfg · JOLTS</span><span class="lang-pt" style="display:none;">Flash CPI ZE 4,0% esperado · ISM ind. · JOLTS</span></span>
                    <div class="cal-meta"><span class="cal-impact high" aria-hidden="true"></span><span class="cal-cur">EUR</span></div>
                </div>
                <div class="cal-cell">
                    <span class="cal-date">02/12</span>
                    <span class="cal-event"><span class="lang-en">US ADP · Australia Q3 GDP</span><span class="lang-pt" style="display:none;">ADP dos EUA · PIB da Austrália 3º tri</span></span>
                    <div class="cal-meta"><span class="cal-impact med" aria-hidden="true"></span><span class="cal-cur">AUD</span></div>
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
        'nextEvent: "Thanksgiving Thursday · ECB minutes · Tokyo CPI"',
        'nextEvent: "EZ flash CPI Tue · ISM + JOLTS · NFP Friday"')
    idx = idx.replace(
        'nextEvent: "Thanksgiving na quinta · ata do BCE · CPI de Tóquio"',
        'nextEvent: "CPI da ZE 3ª · ISM + JOLTS · payroll 6ª"')

    start = idx.find("        const forexData = {")
    end = idx.find("        /* ==========================================\n           B. Market metadata")
    if start < 0 or end < 0:
        raise SystemExit("forexData markers missing")
    idx = idx[:start] + "        const forexData = " + json.dumps(DATA, ensure_ascii=False, indent=4) + ";\n\n" + idx[end:]

    d0 = idx.find("        const dailyChanges = {")
    d1 = idx.find("        const macroDrivers = {")
    changes = {
        "EUR/USD": "-0.16%", "USD/JPY": "+0.18%", "AUD/USD": "+0.50%",
        "GBP/USD": "+0.14%", "EUR/JPY": "+0.01%", "GBP/JPY": "+0.31%",
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
    ledger["meta"]["lastUpdated"] = "28/11/2026"
    with open(LEDGER, "w", encoding="utf-8", newline="\n") as f:
        json.dump(ledger, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("ledger lastUpdated only; book still empty")

    with open(NEWS, encoding="utf-8") as f:
        news = f.read()
    news = news.replace(
        "Market Wire · Hot GDP + PCE, Three New 9-Month Lows, Still No Ticket",
        "Market Wire · Holiday Bounce, Hawkish Minutes, Soft FR/ES CPI, Still No Ticket")
    news = news.replace(
        "Telégrafo da Mesa · PIB + PCE Quentes, Três Novas Mínimas de 9 Meses, Ainda Sem Ticket",
        "Telégrafo da Mesa · Repique de Feriado, Ata Hawkish, CPI Fraco FR/ES, Ainda Sem Ticket")
    news = news.replace(OLD_TS, TS)
    news = news.replace(
        "6 pairs · GDP 4.3% + core PCE 3.3% · AU CPI 4.9% · Thanksgiving Thursday",
        "6 pairs · Friday's bounce · ECB minutes · Tokyo CPI 2.9% · NFP week")
    news = news.replace(
        "6 pares · PIB 4,3% + PCE núcleo 3,3% · CPI da Austrália 4,9% · Thanksgiving na quinta",
        "6 pares · repique de sexta · ata do BCE · CPI de Tóquio 2,9% · semana de payroll")
    start = news.find('                <div class="cal-cell">')
    end = news.find("            </div>\n        </section>", start)
    if start < 0 or end < 0:
        raise SystemExit("calendar block missing")
    news = news[:start] + NEW_CAL + "\n" + news[end:]
    marker = "                <!-- News 25/11/2026:"
    if marker not in news:
        raise SystemExit("news marker missing")
    news = news.replace(marker, NEWS_CARD + marker, 1)
    with open(NEWS, "w", encoding="utf-8", newline="\n") as f:
        f.write(news)
    print("news.html patched")

    with open(SITEMAP, encoding="utf-8") as f:
        sm = f.read()
    n = sm.count("2026-11-25")
    if n != 9:
        raise SystemExit("expected 9 sitemap dates, found %d" % n)
    sm = sm.replace("2026-11-25", "2026-11-28")
    with open(SITEMAP, "w", encoding="utf-8", newline="\n") as f:
        f.write(sm)
    print("sitemap patched")

    with open(VERIFY, encoding="utf-8") as f:
        v = f.read()
    v = v.replace('TODAY_TS = "25/11/2026 20:11 UTC"', 'TODAY_TS = "%s"' % TS)
    v = v.replace(
        'TODAY_DATE = "25/11/2026"  # report edition: 25/11/2026, on the 25/11/2026 basis session',
        'TODAY_DATE = "28/11/2026"  # report edition: 28/11/2026, on the 27/11/2026 basis session')
    v = v.replace(
        'TICKER = [("EUR/USD","-0.25%"),("USD/JPY","+0.16%"),("AUD/USD","-1.08%"),\n'
        '          ("GBP/USD","-0.29%"),("EUR/JPY","-0.10%"),("GBP/JPY","-0.13%")]',
        'TICKER = [("EUR/USD","-0.16%"),("USD/JPY","+0.18%"),("AUD/USD","+0.50%"),\n'
        '          ("GBP/USD","+0.14%"),("EUR/JPY","+0.01%"),("GBP/JPY","+0.31%")]')
    with open(VERIFY, "w", encoding="utf-8", newline="\n") as f:
        f.write(v)
    print("verify constants patched")

if __name__ == "__main__":
    main()

