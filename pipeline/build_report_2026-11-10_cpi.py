#!/usr/bin/env python3
"""10/11/2026 evening edition. Replaces the morning pre-CPI book with the
Tuesday 10/11 ECB fixing, which already contains the October CPI (0.4% m/m,
core 0.3%). All six pairs stay WAIT. Static pages are regenerated separately."""
import json

INDEX = r"C:/Projetos/forex-report/docs/index.html"
LEDGER = r"C:/Projetos/forex-report/docs/track-record.json"
NEWS = r"C:/Projetos/forex-report/docs/news.html"
VERIFY = r"C:/Projetos/forex-report/pipeline/verify_all.py"
TS = "10/11/2026 23:10 UTC"
OLD_TS = "10/11/2026 09:10 UTC"
BASIS = "582 sessions, 01/08/2024 to 10/11/2026"
BASIS_PT = "582 pregões, 01/08/2024 a 10/11/2026"

def pair(quote, bias, bias_type, pt, en):
    return {"quote": quote, "bias": bias, "biasType": bias_type, "pt": pt, "en": en}

EUR = pair("1.1214", "BAIXA", "bear",
    pt={
        "fundamental": "O EUR/USD fechou em 1,1214 na sessão de terça 10/11/2026 (taxa de referência BCE/Frankfurter), subindo +0,19% (+21 pips) a partir de 1,1193. Este print já contém o CPI de outubro: +0,4% no mês (consenso 0,3%, depois de 0,6% em setembro) e núcleo +0,3% (consenso 0,2%), o terceiro mês seguido nesse ritmo (BLS, 10/11, 13:30 UTC). O BLS não publicou a variação anual. O dado saiu acima do esperado e mesmo assim o euro fechou mais alto — o dólar não atravessou 1.1267 nem renovou 1.1130. O Fed segue em 3,75-4,00%; o BCE em 2,50%. Alinhamento de baixa pleno (fechamento sob a SMA200 1,1540, SMA50 1,1332 abaixo dela). Um short sob 1.1130 com stop sobre 1.1267 (~149 pips, piso de 55) joga o 1:2 em 1.0832, através de 1.1100, 1.1050, 1.1000 e 1.0950. A janela do CPI fechou; a geometria continua sem caminho. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (1,1540) com a SMA50 (1,1332) abaixo dela — alinhamento de baixa pleno. O range de 10/20 pregões segue 1.1130 / 1.1267.",
        "support": "1.1130 (mínima de 9 meses e de 10/20 pregões, 29/10), com o redondo 1.1100 abaixo.",
        "resistance": "1.1267 (máxima de 10/20 pregões, 04/11), com a Fib 78,6% em 1,1295 e a SMA50 (1,1332) acima.",
        "priceAction": "CPI quente e o euro subiu 21 pips no meio da faixa. Sem rompimento e sem retração na resistência. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "1.1130 segue o extremo a confirmar por um segundo fechamento sob ele. O stop que cobre 1.1267 atravessa quatro redondos. Sem retração estrutural em 1.1220-1.1267.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O CPI acima do consenso não virou um fechamento de dólar. A baixa está alinhada, mas o 1:2 estrutural continua bloqueado pela escada de redondos."
    },
    en={
        "fundamental": "EUR/USD closed at 1.1214 in the Tuesday 10/11/2026 session (ECB/Frankfurter reference rate), up +0.19% (+21 pips) from 1.1193. This print already contains the October CPI: +0.4% m/m (consensus 0.3%, after 0.6% in September) and core +0.3% (consensus 0.2%), a third straight month at that pace (BLS, Nov 10, 13:30 UTC). The BLS published no year-on-year rate. The print beat the forecast and the euro still closed higher — the dollar neither took 1.1267 nor renewed 1.1130. The Fed is still at 3.75-4.00%; the ECB at 2.50%. Full bear alignment (close under the SMA200 1.1540, SMA50 1.1332 below it). A short under 1.1130 with a stop over 1.1267 (~149 pips, 55-pip floor) puts the 1:2 at 1.0832, through 1.1100, 1.1050, 1.1000 and 1.0950. The CPI window is closed; the geometry still has no path. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (1.1540) with the 50-day (1.1332) below it — full bear alignment. The 10/20-day range is still 1.1130 / 1.1267.",
        "support": "1.1130 (the 9-month and 10/20-day low, Oct 29), with the 1.1100 round below.",
        "resistance": "1.1267 (the 10/20-day high, Nov 4), with the 78.6% Fib at 1.1295 and the SMA50 (1.1332) above.",
        "priceAction": "Hot CPI, and the euro rose 21 pips in the middle of the range. No break and no pullback into resistance. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "1.1130 remains the extreme to confirm with a second close under it. The stop that covers 1.1267 crosses four rounds. No structural pullback in 1.1220-1.1267.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "A CPI beat did not become a dollar close. The bear stack is aligned, but the structural 1:2 stays blocked by the round-number ladder."
    })

USDJPY = pair("158.18", "BAIXA", "bear",
    pt={
        "fundamental": "O USD/JPY fechou em 158,18 na sessão de terça 10/11/2026 (taxa de referência BCE/Frankfurter), subindo +0,15% (+23 pips). O CPI de outubro (+0,4% no mês, núcleo +0,3%) já está neste print e o iene só cedeu 23 pips. O preço ficou 44 pips sob a SMA200 (158,62) — dentro do piso de 63 pips do 1,5σ20 — e acima da SMA50 (157,25). Alinhamento de baixa. A mínima de 10 pregões está em 157,25 e a de 20 pregões em 156,80. Um stop sobre a SMA200 a partir de 158,18 não cobre o piso. Num rompimento sob 157,25 o stop que cobre o fechamento de hoje (~105 pips até 158,30) joga o 1:2 perto de 155,15, através de 156,80 e 156,00. O BoJ segue em 1,25%. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (158,62) com a SMA50 (157,25) também sob ela — alinhamento de baixa. A máxima de 10/20 pregões está em 158,46, ainda abaixo da média longa.",
        "support": "157.25 (mínima de 10 pregões, 30/10), com 156,80 (mínima de 20 pregões) e a escada 156,00 abaixo.",
        "resistance": "158.62 (a SMA200), com a Fib 50% em 158,51 e a máxima de 10/20 pregões em 158,46.",
        "priceAction": "CPI quente, alta de 23 pips, e o preço continua dentro do piso da SMA200. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "157,25 é o piso de 10 pregões, mas o stop que cobre 158,18 atravessa 156,80 no alvo. Vender aqui, 44 pips sob a SMA200, não paga o piso de 63.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O CPI acima do consenso não tirou o par da sombra da SMA200. 44 pips cabem no piso de 63, e o 1:2 de um rompimento ainda cruza 156,00."
    },
    en={
        "fundamental": "USD/JPY closed at 158.18 in the Tuesday 10/11/2026 session (ECB/Frankfurter reference rate), up +0.15% (+23 pips). October CPI (+0.4% m/m, core +0.3%) is already in this print and the yen gave up only 23 pips. Price finished 44 pips under the SMA200 (158.62) — inside the 63-pip 1.5-sigma20 floor — and above the SMA50 (157.25). Bear alignment. The 10-day low is 157.25 and the 20-day low is 156.80. A stop over the SMA200 from 158.18 does not clear the floor. On a break under 157.25 a stop that covers today's close (~105 pips up to 158.30) puts the 1:2 near 155.15, through 156.80 and 156.00. The BoJ is still at 1.25%. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (158.62) with the SMA50 (157.25) also under it — bear alignment. The 10/20-day high is 158.46, still under the long average.",
        "support": "157.25 (the 10-day low, Oct 30), with 156.80 (the 20-day low) and the 156.00 ladder below.",
        "resistance": "158.62 (the SMA200), with the 50% Fib at 158.51 and the 10/20-day high at 158.46.",
        "priceAction": "Hot CPI, a 23-pip rise, and price is still inside the SMA200's floor. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "157.25 is the 10-day floor, but the stop that covers 158.18 crosses 156.80 on the target. Selling here, 44 pips under the SMA200, does not pay the 63-pip floor.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "A CPI beat did not pull the pair out from under the SMA200. 44 pips fit inside the 63-pip floor, and a breakout's 1:2 still crosses 156.00."
    })

AUD = pair("0.6904", "BAIXA", "bear",
    pt={
        "fundamental": "O AUD/USD fechou em 0,6904 na sessão de terça 10/11/2026 (taxa de referência BCE/Frankfurter), subindo +0,14% (+10 pips). O CPI americano quente não renovou a mínima de sexta: o par segue 33 pips acima de 0,6871 (mínima de 10/20 pregões) e 44 pips acima da mínima de 9 meses (0,6860), dentro do piso de 65 pips. A SMA50 (0,7039) está sob a SMA200 (0,7056) e o preço está sob as duas — alinhamento de baixa. O RBA está em 4,85%. Um short sob 0,6860 com stop sobre 0,7033 (~173 pips) joga o 1:2 através de 0,6800 e 0,6700. Sem segundo fechamento no extremo. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (0,7056) com a SMA50 (0,7039) abaixo dela — alinhamento de baixa. A mínima de 10/20 pregões segue 0,6871 (06/11); a máxima de 10 pregões está em 0,7033.",
        "support": "0.6871 (mínima de 10/20 pregões, 06/11) e 0.6860 (mínima de 9 meses), com o redondo 0.6800 abaixo.",
        "resistance": "0.7033 (máxima de 10 pregões), com a SMA50 (0,7039) e a SMA200 (0,7056) no teto. A Fib 61,8% está em 0,7012.",
        "priceAction": "Alta de 10 pips no dia do CPI, ainda sem o segundo fechamento sob 0,6860. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "0,6860 é o extremo de 9 meses a confirmar. O stop que cobre 0,7033 não entrega 1:2 com caminho limpo, e 33 pips até 0,6871 cabem no piso de 65.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O CPI quente não empurrou o Aussie para a mínima. O preço continua dentro do piso e o extremo de 9 meses ainda não tem o segundo fechamento."
    },
    en={
        "fundamental": "AUD/USD closed at 0.6904 in the Tuesday 10/11/2026 session (ECB/Frankfurter reference rate), up +0.14% (+10 pips). The hot US CPI did not renew Friday's low: the pair is still 33 pips above 0.6871 (the 10/20-day low) and 44 pips above the 9-month low (0.6860), inside the 65-pip floor. The SMA50 (0.7039) sits under the SMA200 (0.7056) and price is under both — bear alignment. The RBA cash rate is 4.85%. A short under 0.6860 with a stop over 0.7033 (~173 pips) puts the 1:2 through 0.6800 and 0.6700. No second close at the extreme. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (0.7056) with the SMA50 (0.7039) below it — bear alignment. The 10/20-day low remains 0.6871 (Nov 6); the 10-day high is 0.7033.",
        "support": "0.6871 (the 10/20-day low, Nov 6) and 0.6860 (the 9-month low), with the 0.6800 round below.",
        "resistance": "0.7033 (the 10-day high), with the SMA50 (0.7039) and the SMA200 (0.7056) as the ceiling. The 61.8% Fib is at 0.7012.",
        "priceAction": "A 10-pip rise on CPI day, still no second close under 0.6860. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "0.6860 is the 9-month extreme to confirm. The stop that covers 0.7033 does not deliver a 1:2 with a clear path, and 33 pips down to 0.6871 fit inside the 65-pip floor.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The hot CPI did not push the Aussie into the low. Price is still inside the floor and the 9-month extreme still lacks the second close."
    })

GBP = pair("1.3423", "BAIXA", "bear",
    pt={
        "fundamental": "O GBP/USD fechou em 1,3423 na sessão de terça 10/11/2026 (taxa de referência BCE/Frankfurter), subindo +0,05% (+7 pips). Ficou 2 pips sob a SMA200 (1,3425) — dentro do piso de 67 pips — e acima da SMA50 (1,3361). Alinhamento de baixa. O CPI americano quente quase não moveu o cabo. O short de 22/10 já foi resolvido no stop em 04/11 (1,3500, −1,00R). A máxima de 10/20 pregões segue 1.3500 e a mínima de 10 pregões 1.3288. Um stop sobre 1.3500 a partir de 1,3423 (~77 pips) joga o 1:2 através de 1.3288. A Bank Rate está em 4,00%. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (1,3425) com a SMA50 (1,3361) abaixo dela — alinhamento de baixa. Dois pips separam o preço da média longa.",
        "support": "1.3288 (mínima de 10 pregões, 28/10), com a mínima de 20 pregões em 1.3247 e a mínima de 9 meses em 1.3160.",
        "resistance": "1.3425 (a SMA200) e 1.3500 (máxima de 10/20 pregões, 04/11). A Fib 50% está em 1,3420.",
        "priceAction": "Colado na SMA200. Dois pips de ar cabem no piso de 67, e o alvo de um stop sobre 1.3500 cruza 1.3288. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "Sem gatilho novo. Vender a 2 pips da SMA200 não paga o piso, e um stop sobre 1.3500 atravessa a mínima de 10 pregões no alvo.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O CPI quente deixou o cabo 2 pips sob a SMA200. Isso não é uma venda: o piso é mais largo que o ar, e o 1:2 estrutural cruza 1.3288."
    },
    en={
        "fundamental": "GBP/USD closed at 1.3423 in the Tuesday 10/11/2026 session (ECB/Frankfurter reference rate), up +0.05% (+7 pips). It finished 2 pips under the SMA200 (1.3425) — inside the 67-pip floor — and above the SMA50 (1.3361). Bear alignment. The hot US CPI barely moved cable. The Oct 22 short was already resolved at the stop on Nov 4 (1.3500, −1.00R). The 10/20-day high is still 1.3500 and the 10-day low is 1.3288. A stop over 1.3500 from 1.3423 (~77 pips) puts the 1:2 through 1.3288. Bank Rate is 4.00%. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (1.3425) with the SMA50 (1.3361) below it — bear alignment. Two pips separate price from the long average.",
        "support": "1.3288 (the 10-day low, Oct 28), with the 20-day low at 1.3247 and the 9-month low at 1.3160.",
        "resistance": "1.3425 (the SMA200) and 1.3500 (the 10/20-day high, Nov 4). The 50% Fib is at 1.3420.",
        "priceAction": "Pinned under the SMA200. Two pips of air fit inside the 67-pip floor, and the target of a stop over 1.3500 crosses 1.3288. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "No new trigger. Selling 2 pips under the SMA200 does not pay the floor, and a stop over 1.3500 crosses the 10-day low on the target.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The hot CPI left cable 2 pips under the SMA200. That is not a short: the floor is wider than the air, and the structural 1:2 crosses 1.3288."
    })

EURJPY = pair("177.38", "BAIXA", "bear",
    pt={
        "fundamental": "O EUR/JPY fechou em 177,38 na sessão de terça 10/11/2026 (taxa de referência BCE/Frankfurter), subindo +0,33% (+59 pips). Afastou-se da mínima: 170 pips acima de 175,68 (mínima de 10 pregões) e a mínima de 9 meses / 20 pregões segue 175,51. O piso de 1,5σ20 é de 105 pips. Uma venda sob 175,68 com stop sobre 178,30 (~262 pips) joga o 1:2 dentro do cluster de set-out/2025. Alinhamento de baixa (fechamento sob a SMA200 183,03 e a SMA50 178,17). BCE em 2,50%, BoJ em 1,25%. O CPI americano quente não mudou esse mapa. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (183,03) com a SMA50 (178,17) abaixo dela — alinhamento de baixa pleno. A máxima de 10/20 pregões está em 178,30 (04/11).",
        "support": "175.68 (mínima de 10 pregões, 30/10) e 175.51 (mínima de 9 meses e de 20 pregões, 23/10), com o redondo 175,00 abaixo.",
        "resistance": "178.30 (máxima de 10/20 pregões, 04/11) e a SMA50 (178,17), com a Fib 78,6% em 178,12.",
        "priceAction": "Alta de 59 pips, para longe do gatilho. Sem renovar 175,68 e com o 1:2 ainda no cluster de 2025. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "O fechamento sob 175,68 continua sendo a regra do extremo, mas o stop sobre 178,30 coloca o alvo no cluster de 2025. O preço de hoje está 170 pips acima desse piso.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O cruzado subiu 59 pips e ficou mais longe da mínima. O piso de 105 ainda cabe no caminho, e o stop estrutural empurra o alvo para 2025."
    },
    en={
        "fundamental": "EUR/JPY closed at 177.38 in the Tuesday 10/11/2026 session (ECB/Frankfurter reference rate), up +0.33% (+59 pips). It stepped away from the low: 170 pips above 175.68 (the 10-day low), and the 9-month / 20-day low is still 175.51. The 1.5-sigma20 floor is 105 pips. A short under 175.68 with a stop over 178.30 (~262 pips) puts the 1:2 inside the Sep-Oct 2025 cluster. Bear alignment (close under the SMA200 183.03 and the SMA50 178.17). ECB at 2.50%, BoJ at 1.25%. The hot US CPI did not redraw this map. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (183.03) with the SMA50 (178.17) below it — full bear alignment. The 10/20-day high is 178.30 (Nov 4).",
        "support": "175.68 (the 10-day low, Oct 30) and 175.51 (the 9-month and 20-day low, Oct 23), with the 175.00 round below.",
        "resistance": "178.30 (the 10/20-day high, Nov 4) and the SMA50 (178.17), with the 78.6% Fib at 178.12.",
        "priceAction": "A 59-pip rise, away from the trigger. No renewal of 175.68, and the 1:2 still lands in the 2025 cluster. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The close under 175.68 is still the extreme's rule, but the stop over 178.30 puts the target in the 2025 cluster. Today's price is 170 pips above that floor.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The cross rose 59 pips and moved further from the low. The 105-pip floor still fits on the way down, and the structural stop pushes the target into 2025."
    })

GBPJPY = pair("212.32", "BAIXA", "bear",
    pt={
        "fundamental": "O GBP/JPY fechou em 212,32 na sessão de terça 10/11/2026 (taxa de referência BCE/Frankfurter), subindo +0,20% (+41 pips). Ficou 61 pips sob a SMA200 (212,93) — dentro do piso de 122 pips — e acima da SMA50 (210,09). Alinhamento de baixa. A mínima de 10 pregões está em 209,89 e a de 20 pregões em 209,27. Um stop sobre a SMA200 a partir de 209,89 joga o 1:2 para baixo da mínima de 9 meses (207,32). BoE em 4,00%, BoJ em 1,25%. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (212,93) com a SMA50 (210,09) abaixo dela — alinhamento de baixa. A máxima de 10/20 pregões está em 213,63 (04/11).",
        "support": "209.89 (mínima de 10 pregões, 28/10), com 209,27 (mínima de 20 pregões) e a mínima de 9 meses em 207,32.",
        "resistance": "212.93 (a SMA200), com a Fib 50% em 213,23 e a máxima de 10/20 pregões em 213,63.",
        "priceAction": "Alta de 41 pips e ainda dentro do piso da SMA200. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "209,89 é o piso de 10 pregões, mas o stop que respeita o piso de 122 pips e a SMA200 não cabe sem cruzar 207,32 no alvo. Vender aqui, a 61 pips da média, também não paga o piso.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "Sessenta e um pips sob a SMA200 cabem no piso de 122. O stop estrutural joga o 1:2 para baixo da mínima de 9 meses. A mesa espera."
    },
    en={
        "fundamental": "GBP/JPY closed at 212.32 in the Tuesday 10/11/2026 session (ECB/Frankfurter reference rate), up +0.20% (+41 pips). It finished 61 pips under the SMA200 (212.93) — inside the 122-pip floor — and above the SMA50 (210.09). Bear alignment. The 10-day low is 209.89 and the 20-day low is 209.27. A stop over the SMA200 from 209.89 throws the 1:2 under the 9-month low (207.32). BoE at 4.00%, BoJ at 1.25%. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (212.93) with the SMA50 (210.09) below it — bear alignment. The 10/20-day high is 213.63 (Nov 4).",
        "support": "209.89 (the 10-day low, Oct 28), with 209.27 (the 20-day low) and the 9-month low at 207.32.",
        "resistance": "212.93 (the SMA200), with the 50% Fib at 213.23 and the 10/20-day high at 213.63.",
        "priceAction": "A 41-pip rise and still inside the SMA200's floor. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "209.89 is the 10-day floor, but the stop that respects the 122-pip floor and the SMA200 does not fit without crossing 207.32 on the target. Selling here, 61 pips under the average, does not pay the floor either.",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "Sixty-one pips under the SMA200 fit inside the 122-pip floor. The structural stop throws the 1:2 under the 9-month low. The desk waits."
    })

DATA = {
    "EUR/USD": EUR, "USD/JPY": USDJPY, "AUD/USD": AUD,
    "GBP/USD": GBP, "EUR/JPY": EURJPY, "GBP/JPY": GBPJPY,
}
DRIVERS = {
    "EUR/USD": {
        "en": ["CPI 0.4% and the euro still rose", "Range 1.1130 to 1.1267 holds", "1:2 still crosses four rounds"],
        "pt": ["CPI 0,4% e o euro ainda subiu", "Faixa 1.1130 a 1.1267 segue", "O 1:2 ainda cruza quatro redondos"],
    },
    "USD/JPY": {
        "en": ["44 pips under the SMA200", "Inside the 63-pip floor", "156.80 still blocks the path"],
        "pt": ["44 pips sob a SMA200", "Dentro do piso de 63", "156.80 ainda bloqueia o caminho"],
    },
    "AUD/USD": {
        "en": ["+10 pips, Friday's low holds", "33 pips of air inside a 65-pip floor", "9-month low 0.6860 unconfirmed"],
        "pt": ["+10 pips, mínima de sexta segura", "33 pips de ar num piso de 65", "Mín. de 9m 0.6860 sem confirmação"],
    },
    "GBP/USD": {
        "en": ["2 pips under the SMA200", "Inside the 67-pip floor", "Prior short already stopped out"],
        "pt": ["2 pips sob a SMA200", "Dentro do piso de 67", "Short anterior já stopado"],
    },
    "EUR/JPY": {
        "en": ["+59 pips, further from 175.68", "105-pip floor still binds", "2025 cluster still blocks"],
        "pt": ["+59 pips, mais longe de 175,68", "Piso de 105 pips segue valendo", "Cluster de 2025 ainda bloqueia"],
    },
    "GBP/JPY": {
        "en": ["61 pips under the SMA200", "Inside the 122-pip floor", "BoE at 4.00%, BoJ at 1.25%"],
        "pt": ["61 pips sob a SMA200", "Dentro do piso de 122", "BoE a 4,00%, BoJ a 1,25%"],
    },
}

# Chip text must not contain "word:" or "number:" — "1:2" would break
# build_static_pages.py. Rewrite those two chips without a colon.
DRIVERS["EUR/USD"]["en"][2] = "Structural reward still crosses four rounds"
DRIVERS["EUR/USD"]["pt"][2] = "O alvo estrutural ainda cruza quatro redondos"

NEWS_ITEM_JS = r'''                {
                    date: "10/11/2026",
                    category: "macro",
                    impact: "high",
                    pairs: ["EUR/USD", "USD/JPY", "AUD/USD", "GBP/USD", "EUR/JPY", "GBP/JPY"],
                    pt: {
                        headline: "CPI a 0,4% e o dólar não rompe — os seis pares ficam em AGUARDAR",
                        summary: "O CPI de outubro saiu a +0,4% no mês (consenso 0,3%) e o núcleo a +0,3% (consenso 0,2%), o terceiro mês seguido nesse ritmo (BLS, 10/11, 13:30 UTC). Sem variação anual. A taxa BCE/Frankfurter de terça já contém o dado. No livro: EUR/USD 1,1214 (+0,19%), ainda entre 1.1130 e 1.1267. USD/JPY 158,18 (+0,15%), 44 pips sob a SMA200, dentro do piso de 63. AUD/USD 0,6904 (+0,14%), 33 pips acima da mínima de sexta. GBP/USD 1,3423 (+0,05%), 2 pips sob a SMA200. EUR/JPY 177,38 (+0,33%) afastou-se de 175,68. GBP/JPY 212,32 (+0,20%), 61 pips sob a SMA200. A janela do CPI fechou e nenhum par paga 1:2 com caminho limpo.",
                        take: "Inflação acima do consenso, reação mansa no fechamento de referência. A geometria continua mandando esperar. O livro segue vazio."
                    },
                    en: {
                        headline: "CPI at 0.4% and the dollar does not break — all six pairs stay on WAIT",
                        summary: "October CPI printed +0.4% m/m (consensus 0.3%) and the core +0.3% (consensus 0.2%), a third straight month at that pace (BLS, Nov 10, 13:30 UTC). No year-on-year rate. Tuesday's ECB/Frankfurter fixing already contains the print. In the book: EUR/USD 1.1214 (+0.19%), still between 1.1130 and 1.1267. USD/JPY 158.18 (+0.15%), 44 pips under the SMA200, inside the 63-pip floor. AUD/USD 0.6904 (+0.14%), 33 pips above Friday's low. GBP/USD 1.3423 (+0.05%), 2 pips under the SMA200. EUR/JPY 177.38 (+0.33%) stepped away from 175.68. GBP/JPY 212.32 (+0.20%), 61 pips under the SMA200. The CPI window is closed and no pair pays a 1:2 with a clean path.",
                        take: "Inflation above consensus, a tame reaction in the reference close. The geometry still says wait. The book stays empty."
                    }
                },
'''

NEWS_CARD = r'''                <!-- News 10/11/2026 evening: CPI 0.4% is in the fixing; all six pairs stay on WAIT -->
                <article class="news-card">
                    <div class="news-card-top">
                        <span class="news-cat"><span class="lang-en">Macro Data</span><span class="lang-pt" style="display:none;">Dados Macro</span></span>
                        <span class="impact-badge high"><span class="lang-en">High Impact</span><span class="lang-pt" style="display:none;">Impacto Alto</span></span>
                        <span class="news-date">10/11/2026</span>
                    </div>
                    <h2 class="news-title">
                        <span class="lang-en">CPI at 0.4% and the dollar does not break — all six pairs stay on WAIT</span>
                        <span class="lang-pt" style="display:none;">CPI a 0,4% e o dólar não rompe — os seis pares ficam em AGUARDAR</span>
                    </h2>
                    <p class="news-summary">
                        <span class="lang-en">October CPI printed +0.4% m/m (consensus 0.3%) and the core +0.3% (consensus 0.2%), a third straight month at that pace (BLS, Nov 10, 13:30 UTC). No year-on-year rate. Tuesday's ECB/Frankfurter fixing already contains the print. In the book: EUR/USD 1.1214 (+0.19%), still between 1.1130 and 1.1267. USD/JPY 158.18 (+0.15%), 44 pips under the SMA200, inside the 63-pip floor. AUD/USD 0.6904 (+0.14%), 33 pips above Friday's low. GBP/USD 1.3423 (+0.05%), 2 pips under the SMA200. EUR/JPY 177.38 (+0.33%) stepped away from 175.68. GBP/JPY 212.32 (+0.20%), 61 pips under the SMA200. The CPI window is closed and no pair pays a 1:2 with a clean path.</span>
                        <span class="lang-pt" style="display:none;">O CPI de outubro saiu a +0,4% no mês (consenso 0,3%) e o núcleo a +0,3% (consenso 0,2%), o terceiro mês seguido nesse ritmo (BLS, 10/11, 13:30 UTC). Sem variação anual. A taxa BCE/Frankfurter de terça já contém o dado. No livro: EUR/USD 1,1214 (+0,19%), ainda entre 1.1130 e 1.1267. USD/JPY 158,18 (+0,15%), 44 pips sob a SMA200, dentro do piso de 63. AUD/USD 0,6904 (+0,14%), 33 pips acima da mínima de sexta. GBP/USD 1,3423 (+0,05%), 2 pips sob a SMA200. EUR/JPY 177,38 (+0,33%) afastou-se de 175,68. GBP/JPY 212,32 (+0,20%), 61 pips sob a SMA200. A janela do CPI fechou e nenhum par paga 1:2 com caminho limpo.</span>
                    </p>
                    <div class="news-take">
                        <span class="take-tag"><span class="lang-en">Desk take</span><span class="lang-pt" style="display:none;">Leitura da mesa</span></span>
                        <span class="lang-en">Inflation above consensus, a tame reaction in the reference close. The geometry still says wait. The book stays empty.</span>
                        <span class="lang-pt" style="display:none;">Inflação acima do consenso, reação mansa no fechamento de referência. A geometria continua mandando esperar. O livro segue vazio.</span>
                    </div>
                    <div class="news-pairs">
                        <span class="np-label"><span class="lang-en">Watch</span><span class="lang-pt" style="display:none;">Acompanhar</span></span>
                        <a href="eur-usd.html" class="pair-link-chip">EUR/USD</a><a href="usd-jpy.html" class="pair-link-chip">USD/JPY</a><a href="aud-usd.html" class="pair-link-chip">AUD/USD</a><a href="gbp-usd.html" class="pair-link-chip">GBP/USD</a><a href="eur-jpy.html" class="pair-link-chip">EUR/JPY</a><a href="gbp-jpy.html" class="pair-link-chip">GBP/JPY</a>
                    </div>
                </article>

'''

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
        "EUR/USD": "+0.19%", "USD/JPY": "+0.15%", "AUD/USD": "+0.14%",
        "GBP/USD": "+0.05%", "EUR/JPY": "+0.33%", "GBP/JPY": "+0.20%",
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

    # newsData.updated was the morning stamp and is now TS. generationTime
    # and both generatedAt strings were replaced above. Confirm four.
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
    ledger["meta"]["lastUpdated"] = "10/11/2026"
    with open(LEDGER, "w", encoding="utf-8", newline="\n") as f:
        json.dump(ledger, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("ledger unchanged except lastUpdated")

    with open(NEWS, encoding="utf-8") as f:
        news = f.read()
    news = news.replace(
        "Market Wire · Monday Book, CPI Still Ahead",
        "Market Wire · CPI 0.4%, Dollar Does Not Break")
    news = news.replace(
        "Telégrafo da Mesa · Livro de Segunda, CPI Ainda à Frente",
        "Telégrafo da Mesa · CPI 0,4%, Dólar Não Rompe")
    news = news.replace(OLD_TS, TS)
    old_cpi = 'US CPI due 13:30 UTC, consensus 0.3% m/m — not in the 09/11 fixing'
    new_cpi = 'US CPI +0.4% m/m, core +0.3% — in the 10/11 fixing'
    old_cpi_pt = 'CPI dos EUA às 13:30 UTC, consenso 0,3% m/m — fora do fechamento de 09/11'
    new_cpi_pt = 'CPI dos EUA +0,4% m/m, núcleo +0,3% — no fechamento de 10/11'
    if old_cpi not in news or old_cpi_pt not in news:
        raise SystemExit("CPI calendar cell missing")
    news = news.replace(old_cpi, new_cpi, 1).replace(old_cpi_pt, new_cpi_pt, 1)
    marker = "                <!-- News 10/11/2026: Monday fixing"
    if marker not in news:
        raise SystemExit("news marker missing")
    news = news.replace(marker, NEWS_CARD + marker, 1)
    with open(NEWS, "w", encoding="utf-8", newline="\n") as f:
        f.write(news)
    print("news.html patched")

    with open(VERIFY, encoding="utf-8") as f:
        v = f.read()
    v = v.replace('TODAY_TS = "10/11/2026 09:10 UTC"', 'TODAY_TS = "%s"' % TS)
    v = v.replace(
        'TODAY_DATE = "09/11/2026"  # basis session date (report edition: 10/11/2026)',
        'TODAY_DATE = "10/11/2026"  # basis session date (report edition: 10/11/2026 evening)')
    old_ticker = '''TICKER = [("EUR/USD","+0.25%"),("USD/JPY","-0.24%"),("AUD/USD","+0.34%"),
          ("GBP/USD","+0.23%"),("EUR/JPY","+0.01%"),("GBP/JPY","-0.01%")]'''
    new_ticker = '''TICKER = [("EUR/USD","+0.19%"),("USD/JPY","+0.15%"),("AUD/USD","+0.14%"),
          ("GBP/USD","+0.05%"),("EUR/JPY","+0.33%"),("GBP/JPY","+0.20%")]'''
    if old_ticker not in v:
        raise SystemExit("ticker block missing")
    v = v.replace(old_ticker, new_ticker)
    with open(VERIFY, "w", encoding="utf-8", newline="\n") as f:
        f.write(v)
    print("verify constants patched")

if __name__ == "__main__":
    main()
