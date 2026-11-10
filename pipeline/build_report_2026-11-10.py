#!/usr/bin/env python3
"""10/11/2026 edition. Last completed ECB fixing is Monday 09/11 — before
today's US CPI (13:30 UTC). Patches forexData, ticker, chips, wire and
news.html. Ledger has nothing open to resolve. Static pages are regenerated
by build_static_pages.py."""
import json

INDEX = r"C:/Projetos/forex-report/docs/index.html"
LEDGER = r"C:/Projetos/forex-report/docs/track-record.json"
NEWS = r"C:/Projetos/forex-report/docs/news.html"
SITEMAP = r"C:/Projetos/forex-report/docs/sitemap.xml"
VERIFY = r"C:/Projetos/forex-report/pipeline/verify_all.py"
TS = "10/11/2026 09:10 UTC"
OLD_TS = "06/11/2026 20:10 UTC"
BASIS = "581 sessions, 01/08/2024 to 09/11/2026"
BASIS_PT = "581 pregões, 01/08/2024 a 09/11/2026"

def pair(quote, bias, bias_type, pt, en):
    return {"quote": quote, "bias": bias, "biasType": bias_type, "pt": pt, "en": en}

EUR = pair("1.1193", "BAIXA", "bear",
    pt={
        "fundamental": "O EUR/USD fechou em 1,1193 na sessão de segunda 09/11/2026 (taxa de referência BCE/Frankfurter), subindo +0,25% (+28 pips) a partir de 1,1165. Este print é anterior ao CPI de outubro dos EUA, marcado para hoje 10/11 às 13:30 UTC (consenso 0,3% m/m depois de 0,6% em setembro; núcleo 0,2% depois de 0,3%; o BLS não publica a variação anual deste mês). O Fed segue em 3,75-4,00% e o BCE em 2,50%. A mínima de 9 meses e de 10/20 pregões continua 1.1130; a máxima de 10/20 pregões continua 1.1267. Alinhamento de baixa pleno (fechamento sob a SMA200 1,1543, SMA50 1,1339 abaixo dela). Um short sob 1.1130 com stop sobre 1.1267 (~149 pips) joga o 1:2 em 1.0832, através de 1.1100, 1.1050, 1.1000 e 1.0950. O filtro de eventos fecha a janela até o CPI sair. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (1,1543) com a SMA50 (1,1339) abaixo dela — alinhamento de baixa pleno. O range de 10/20 pregões segue 1.1130 / 1.1267.",
        "support": "1.1130 (mínima de 9 meses e de 10/20 pregões, 29/10), com o redondo 1.1100 abaixo.",
        "resistance": "1.1267 (máxima de 10/20 pregões, 04/11), com a Fib 78,6% em 1,1295 e a SMA50 (1,1339) acima.",
        "priceAction": "Repique de 28 pips no meio da faixa, sem rompimento. O CPI de hoje não está neste print. Sem ticket.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "1.1130 segue o extremo a confirmar por um segundo fechamento sob ele, mas o stop que cobre 1.1267 atravessa quatro redondos. Reavaliar após o CPI (10/11, 13:30 UTC).",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "A baixa está alinhada, mas o livro de segunda não contém o CPI e o 1:2 estrutural continua bloqueado pela escada de redondos. A mesa espera o dado."
    },
    en={
        "fundamental": "EUR/USD closed at 1.1193 in the Monday 09/11/2026 session (ECB/Frankfurter reference rate), up +0.25% (+28 pips) from 1.1165. This print predates the US October CPI, due today Nov 10 at 13:30 UTC (consensus 0.3% m/m after 0.6% in September; core 0.2% after 0.3%; the BLS is not publishing a year-on-year rate this month). The Fed is still at 3.75-4.00% and the ECB at 2.50%. The 9-month and 10/20-day low is still 1.1130; the 10/20-day high is still 1.1267. Full bear alignment (close under the SMA200 1.1543, SMA50 1.1339 below it). A short under 1.1130 with a stop over 1.1267 (~149 pips) puts the 1:2 at 1.0832, through 1.1100, 1.1050, 1.1000 and 1.0950. The event filter closes the window until CPI prints. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (1.1543) with the 50-day (1.1339) below it — full bear alignment. The 10/20-day range is still 1.1130 / 1.1267.",
        "support": "1.1130 (the 9-month and 10/20-day low, Oct 29), with the 1.1100 round below.",
        "resistance": "1.1267 (the 10/20-day high, Nov 4), with the 78.6% Fib at 1.1295 and the SMA50 (1.1339) above.",
        "priceAction": "A 28-pip bounce in the middle of the range, no break. Today's CPI is not in this print. No ticket.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "1.1130 remains the extreme to confirm with a second close under it, but the stop that covers 1.1267 still crosses four rounds. Reassess after CPI (Nov 10, 13:30 UTC).",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The bear stack is aligned, but Monday's book does not contain CPI and the structural 1:2 stays blocked by the round-number ladder. The desk waits for the print."
    })

USDJPY = pair("157.95", "BAIXA", "bear",
    pt={
        "fundamental": "O USD/JPY fechou em 157,95 na sessão de segunda 09/11/2026 (taxa de referência BCE/Frankfurter), caindo -0,24% (-38 pips). Ficou 65 pips sob a SMA200 (158,60) — um pip além do piso de 64 do 1,5σ20 — e acima da SMA50 (157,29). Alinhamento de baixa. A mínima de 10 pregões está em 157,25 e a de 20 pregões em 156,80. Um stop sobre a SMA200 a partir de 157,95 (~77 pips até 158,72) joga o 1:2 perto de 156,41, através de 157,25 e 156,80. O BoJ mantém 1,25%. Este print é anterior ao CPI de hoje. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (158,60) com a SMA50 (157,29) também sob ela — alinhamento de baixa. A máxima de 10/20 pregões está em 158,46, logo abaixo da média longa.",
        "support": "157.25 (mínima de 10 pregões, 30/10), com 156,80 (mínima de 20 pregões) e a escada 156,00 abaixo.",
        "resistance": "158.60 (a SMA200), com a Fib 50% em 158,51 e a máxima de 10/20 pregões em 158,46.",
        "priceAction": "Afastou-se 38 pips da média longa e ainda assim o alvo estrutural atravessa 156,80. Sem ticket antes do CPI.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "157,25 é o piso de 10 pregões, mas um stop que cubra 157,95 e a SMA200 não cabe num 1:2 antes de 156,80. Reavaliar após o CPI (10/11, 13:30 UTC).",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "65 pips até a SMA200 mal saem do piso de 64, e o 1:2 ainda cruza a escada de 156. O CPI de hoje fecha a janela que a geometria já fechava."
    },
    en={
        "fundamental": "USD/JPY closed at 157.95 in the Monday 09/11/2026 session (ECB/Frankfurter reference rate), down -0.24% (-38 pips). It finished 65 pips under the SMA200 (158.60) — one pip beyond the 64-pip 1.5-sigma20 floor — and above the SMA50 (157.29). Bear alignment. The 10-day low is 157.25 and the 20-day low is 156.80. A stop over the SMA200 from 157.95 (~77 pips up to 158.72) puts the 1:2 near 156.41, through 157.25 and 156.80. The BoJ is still at 1.25%. This print predates today's CPI. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (158.60) with the SMA50 (157.29) also under it — bear alignment. The 10/20-day high is 158.46, just under the long average.",
        "support": "157.25 (the 10-day low, Oct 30), with 156.80 (the 20-day low) and the 156.00 ladder below.",
        "resistance": "158.60 (the SMA200), with the 50% Fib at 158.51 and the 10/20-day high at 158.46.",
        "priceAction": "It stepped 38 pips away from the long average and the structural target still crosses 156.80. No ticket ahead of CPI.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "157.25 is the 10-day floor, but a stop that covers 157.95 and the SMA200 does not fit a 1:2 before 156.80. Reassess after CPI (Nov 10, 13:30 UTC).",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "65 pips up to the SMA200 barely clears the 64-pip floor, and the 1:2 still crosses the 156 ladder. Today's CPI closes a window the geometry had already closed."
    })

AUD = pair("0.6894", "BAIXA", "bear",
    pt={
        "fundamental": "O AUD/USD fechou em 0,6894 na sessão de segunda 09/11/2026 (taxa de referência BCE/Frankfurter), subindo +0,34% (+23 pips) a partir da mínima de 10/20 pregões de sexta (0,6871). Continua 34 pips acima da mínima de 9 meses (0,6860) e dentro do piso de 64 pips. A SMA50 (0,7044) está sob a SMA200 (0,7056) e o preço está sob as duas — alinhamento de baixa. O RBA está em 4,85%. Um short sob 0,6860 com stop sobre 0,7033 (~173 pips) joga o 1:2 através de 0,6800 e 0,6700, e o extremo de 9 meses ainda não tem o segundo fechamento. Este print é anterior ao CPI americano. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (0,7056) com a SMA50 (0,7044) abaixo dela — alinhamento de baixa. A mínima de 10/20 pregões segue 0,6871 (06/11); a máxima de 10 pregões está em 0,7033.",
        "support": "0.6871 (mínima de 10/20 pregões, 06/11) e 0.6860 (mínima de 9 meses), com o redondo 0.6800 abaixo.",
        "resistance": "0.7033 (máxima de 10 pregões), com a SMA50 (0,7044) e a SMA200 (0,7056) no teto. A Fib 61,8% está em 0,7012.",
        "priceAction": "Repique de 23 pips, ainda sem o segundo fechamento sob 0,6860. Sem ticket antes do CPI.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "0,6860 é o extremo de 9 meses a confirmar. O stop que cobre 0,7033 não entrega 1:2 com caminho limpo. Reavaliar após o CPI (10/11, 13:30 UTC).",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "O Aussie saiu 23 pips da mínima de sexta e continua dentro do piso. Sem segundo fechamento no extremo de 9 meses e com o CPI hoje, a mesa não vende."
    },
    en={
        "fundamental": "AUD/USD closed at 0.6894 in the Monday 09/11/2026 session (ECB/Frankfurter reference rate), up +0.34% (+23 pips) from Friday's 10/20-day low (0.6871). It is still 34 pips above the 9-month low (0.6860) and inside the 64-pip floor. The SMA50 (0.7044) sits under the SMA200 (0.7056) and price is under both — bear alignment. The RBA cash rate is 4.85%. A short under 0.6860 with a stop over 0.7033 (~173 pips) puts the 1:2 through 0.6800 and 0.6700, and the 9-month extreme still lacks a second close. This print predates the US CPI. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (0.7056) with the SMA50 (0.7044) below it — bear alignment. The 10/20-day low remains 0.6871 (Nov 6); the 10-day high is 0.7033.",
        "support": "0.6871 (the 10/20-day low, Nov 6) and 0.6860 (the 9-month low), with the 0.6800 round below.",
        "resistance": "0.7033 (the 10-day high), with the SMA50 (0.7044) and the SMA200 (0.7056) as the ceiling. The 61.8% Fib is at 0.7012.",
        "priceAction": "A 23-pip bounce, still no second close under 0.6860. No ticket ahead of CPI.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "0.6860 is the 9-month extreme to confirm. The stop that covers 0.7033 does not deliver a 1:2 with a clear path. Reassess after CPI (Nov 10, 13:30 UTC).",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "The Aussie bounced 23 pips off Friday's low and is still inside the floor. With no second close at the 9-month extreme and CPI today, the desk does not sell."
    })

GBP = pair("1.3416", "BAIXA", "bear",
    pt={
        "fundamental": "O GBP/USD fechou em 1,3416 na sessão de segunda 09/11/2026 (taxa de referência BCE/Frankfurter), subindo +0,23% (+31 pips). Ficou 11 pips sob a SMA200 (1,3427) — dentro do piso de 67 pips — e acima da SMA50 (1,3363). Alinhamento de baixa. O short de 22/10 já foi resolvido no stop em 04/11 (1,3500, −1,00R). A máxima de 10/20 pregões segue 1.3500 e a mínima de 10 pregões 1.3288. Um stop sobre 1.3500 a partir de 1,3416 (~84 pips) joga o 1:2 através de 1.3288. A Bank Rate está em 4,00%. Este print é anterior ao CPI. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (1,3427) com a SMA50 (1,3363) abaixo dela — alinhamento de baixa. O preço voltou para debaixo da média longa, a 11 pips.",
        "support": "1.3288 (mínima de 10 pregões, 28/10), com a mínima de 20 pregões em 1.3246 e a mínima de 9 meses em 1.3160.",
        "resistance": "1.3427 (a SMA200) e 1.3500 (máxima de 10/20 pregões, 04/11). A Fib 50% está em 1,3420.",
        "priceAction": "Sem rearme. Onze pips de ar até a SMA200 cabem no piso, e o alvo de um stop sobre 1.3500 cruza 1.3288. Sem ticket antes do CPI.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "O short anterior fechou no stop em 04/11. Sem gatilho novo enquanto o stop estrutural sobre 1.3500 atravessar 1.3288. Reavaliar após o CPI (10/11, 13:30 UTC).",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "Voltar para 11 pips da SMA200 não abre operação: o piso de 67 pips é mais largo que esse ar, e o 1:2 estrutural cruza a mínima de 10 pregões. O CPI fecha o resto."
    },
    en={
        "fundamental": "GBP/USD closed at 1.3416 in the Monday 09/11/2026 session (ECB/Frankfurter reference rate), up +0.23% (+31 pips). It finished 11 pips under the SMA200 (1.3427) — inside the 67-pip floor — and above the SMA50 (1.3363). Bear alignment. The Oct 22 short was already resolved at the stop on Nov 4 (1.3500, −1.00R). The 10/20-day high is still 1.3500 and the 10-day low is 1.3288. A stop over 1.3500 from 1.3416 (~84 pips) puts the 1:2 through 1.3288. Bank Rate is 4.00%. This print predates CPI. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (1.3427) with the SMA50 (1.3363) below it — bear alignment. Price is back under the long average, 11 pips away.",
        "support": "1.3288 (the 10-day low, Oct 28), with the 20-day low at 1.3246 and the 9-month low at 1.3160.",
        "resistance": "1.3427 (the SMA200) and 1.3500 (the 10/20-day high, Nov 4). The 50% Fib is at 1.3420.",
        "priceAction": "No re-arm. Eleven pips of air up to the SMA200 fit inside the floor, and the target of a stop over 1.3500 crosses 1.3288. No ticket ahead of CPI.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The prior short closed at the stop on Nov 4. No new trigger while the structural stop over 1.3500 crosses 1.3288. Reassess after CPI (Nov 10, 13:30 UTC).",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "Returning to within 11 pips of the SMA200 does not open a trade: the 67-pip floor is wider than that air, and the structural 1:2 crosses the 10-day low. CPI closes the rest."
    })

EURJPY = pair("176.79", "BAIXA", "bear",
    pt={
        "fundamental": "O EUR/JPY fechou em 176,79 na sessão de segunda 09/11/2026 (taxa de referência BCE/Frankfurter), subindo +0,01% (+2 pips). A mínima de 10 pregões segue 175,68 e a de 9 meses / 20 pregões 175,51. O fechamento ficou 111 pips acima de 175,68, pouco além do piso de 104. Uma venda sob 175,68 com stop sobre 178,30 (~262 pips) joga o 1:2 dentro do cluster de set-out/2025. Alinhamento de baixa (fechamento sob a SMA200 183,06 e a SMA50 178,34). BCE em 2,50%, BoJ em 1,25%. Este print é anterior ao CPI. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (183,06) com a SMA50 (178,34) abaixo dela — alinhamento de baixa pleno. A máxima de 10/20 pregões está em 178,30 (04/11).",
        "support": "175.68 (mínima de 10 pregões, 30/10) e 175.51 (mínima de 9 meses e de 20 pregões, 23/10), com o redondo 175,00 abaixo.",
        "resistance": "178.30 (máxima de 10/20 pregões, 04/11) e a SMA50 (178,34), com a Fib 78,6% em 178,12.",
        "priceAction": "Quase parado. Sem renovar 175,68 e com o 1:2 ainda no cluster de 2025. Sem ticket antes do CPI.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "O fechamento sob 175,68 continua sendo a regra do extremo, mas o stop sobre 178,30 coloca o alvo no cluster de 2025. Reavaliar após o CPI (10/11, 13:30 UTC).",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "Dois pips de variação não mudam o mapa. O piso de 104 ainda cabe no caminho até 175,68, e o stop estrutural empurra o alvo para 2025."
    },
    en={
        "fundamental": "EUR/JPY closed at 176.79 in the Monday 09/11/2026 session (ECB/Frankfurter reference rate), up +0.01% (+2 pips). The 10-day low is still 175.68 and the 9-month / 20-day low is 175.51. The close finished 111 pips above 175.68, just beyond the 104-pip floor. A short under 175.68 with a stop over 178.30 (~262 pips) puts the 1:2 inside the Sep-Oct 2025 cluster. Bear alignment (close under the SMA200 183.06 and the SMA50 178.34). ECB at 2.50%, BoJ at 1.25%. This print predates CPI. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (183.06) with the SMA50 (178.34) below it — full bear alignment. The 10/20-day high is 178.30 (Nov 4).",
        "support": "175.68 (the 10-day low, Oct 30) and 175.51 (the 9-month and 20-day low, Oct 23), with the 175.00 round below.",
        "resistance": "178.30 (the 10/20-day high, Nov 4) and the SMA50 (178.34), with the 78.6% Fib at 178.12.",
        "priceAction": "Almost unchanged. No renewal of 175.68, and the 1:2 still lands in the 2025 cluster. No ticket ahead of CPI.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "The close under 175.68 is still the extreme's rule, but the stop over 178.30 puts the target in the 2025 cluster. Reassess after CPI (Nov 10, 13:30 UTC).",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "A two-pip change does not redraw the map. The 104-pip floor still fits on the way down to 175.68, and the structural stop pushes the target into 2025."
    })

GBPJPY = pair("211.91", "BAIXA", "bear",
    pt={
        "fundamental": "O GBP/JPY fechou em 211,91 na sessão de segunda 09/11/2026 (taxa de referência BCE/Frankfurter), caindo -0,01% (-1 pip). Segue 102 pips sob a SMA200 (212,93) — dentro do piso de 123 pips — e acima da SMA50 (210,17). Alinhamento de baixa. A mínima de 10 pregões está em 209,89 e a de 20 pregões em 209,27. Um stop sobre a SMA200 a partir de 209,89 joga o 1:2 para baixo da mínima de 9 meses (207,32). BoE em 4,00%, BoJ em 1,25%. Este print é anterior ao CPI. Indicadores calculados da série diária BCE/Frankfurter (" + BASIS_PT + ").",
        "trend": "Fechamento sob a SMA200 (212,93) com a SMA50 (210,17) abaixo dela — alinhamento de baixa. A máxima de 10/20 pregões está em 213,63 (04/11).",
        "support": "209.89 (mínima de 10 pregões, 28/10), com 209,27 (mínima de 20 pregões) e a mínima de 9 meses em 207,32.",
        "resistance": "212.93 (a SMA200), com a Fib 50% em 213,23 e a máxima de 10/20 pregões em 213,63.",
        "priceAction": "Parado sob a média longa, dentro do piso. Sem ticket antes do CPI.",
        "recommendation": "AGUARDAR OUTRO GATILHO",
        "trigger": "209,89 é o piso de 10 pregões, mas o stop que respeita o piso de 123 pips e a SMA200 não cabe sem cruzar 207,32 no alvo. Reavaliar após o CPI (10/11, 13:30 UTC).",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "Cento e dois pips sob a SMA200 cabem no piso de 123. O stop estrutural joga o 1:2 para baixo da mínima de 9 meses. A mesa espera o CPI."
    },
    en={
        "fundamental": "GBP/JPY closed at 211.91 in the Monday 09/11/2026 session (ECB/Frankfurter reference rate), down -0.01% (-1 pip). It is still 102 pips under the SMA200 (212.93) — inside the 123-pip floor — and above the SMA50 (210.17). Bear alignment. The 10-day low is 209.89 and the 20-day low is 209.27. A stop over the SMA200 from 209.89 throws the 1:2 under the 9-month low (207.32). BoE at 4.00%, BoJ at 1.25%. This print predates CPI. Indicators computed from the ECB/Frankfurter daily series (" + BASIS + ").",
        "trend": "Close under the SMA200 (212.93) with the SMA50 (210.17) below it — bear alignment. The 10/20-day high is 213.63 (Nov 4).",
        "support": "209.89 (the 10-day low, Oct 28), with 209.27 (the 20-day low) and the 9-month low at 207.32.",
        "resistance": "212.93 (the SMA200), with the 50% Fib at 213.23 and the 10/20-day high at 213.63.",
        "priceAction": "Unchanged under the long average, inside the floor. No ticket ahead of CPI.",
        "recommendation": "WAIT FOR ANOTHER TRIGGER",
        "trigger": "209.89 is the 10-day floor, but the stop that respects the 123-pip floor and the SMA200 does not fit without crossing 207.32 on the target. Reassess after CPI (Nov 10, 13:30 UTC).",
        "stop": "N/A (no trade).",
        "target": "N/A (no trade).",
        "rr": "N/A",
        "rrValue": 0,
        "justification": "One hundred two pips under the SMA200 fit inside the 123-pip floor. The structural stop throws the 1:2 under the 9-month low. The desk waits for CPI."
    })

DATA = {
    "EUR/USD": EUR, "USD/JPY": USDJPY, "AUD/USD": AUD,
    "GBP/USD": GBP, "EUR/JPY": EURJPY, "GBP/JPY": GBPJPY,
}
DRIVERS = {
    "EUR/USD": {
        "en": ["Monday close 1.1193, pre-CPI", "9-month low 1.1130 still holds", "US CPI today at 1330 UTC"],
        "pt": ["Fechamento de segunda 1,1193, pré-CPI", "Mín. de 9m 1.1130 ainda segura", "CPI dos EUA hoje às 1330 UTC"],
    },
    "USD/JPY": {
        "en": ["65 pips under the SMA200", "Just outside the 64-pip floor", "156.80 still blocks the path"],
        "pt": ["65 pips sob a SMA200", "Um pip fora do piso de 64", "156.80 ainda bloqueia o caminho"],
    },
    "AUD/USD": {
        "en": ["+23 pips off Friday's low", "Still inside the 64-pip floor", "9-month low 0.6860 unconfirmed"],
        "pt": ["+23 pips da mínima de sexta", "Ainda dentro do piso de 64", "Mín. de 9m 0.6860 sem confirmação"],
    },
    "GBP/USD": {
        "en": ["11 pips under the SMA200", "Inside the 67-pip floor", "Prior short already stopped out"],
        "pt": ["11 pips sob a SMA200", "Dentro do piso de 67", "Short anterior já stopado"],
    },
    "EUR/JPY": {
        "en": ["+2 pips, still 111 above 175.68", "104-pip floor still binds", "2025 cluster still blocks"],
        "pt": ["+2 pips, ainda 111 acima de 175,68", "Piso de 104 pips segue valendo", "Cluster de 2025 ainda bloqueia"],
    },
    "GBP/JPY": {
        "en": ["102 pips under the SMA200", "Inside the 123-pip floor", "BoE at 4.00%, BoJ at 1.25%"],
        "pt": ["102 pips sob a SMA200", "Dentro do piso de 123", "BoE a 4,00%, BoJ a 1,25%"],
    },
}

NEWS_ITEM_JS = r'''                {
                    date: "10/11/2026",
                    category: "macro",
                    impact: "high",
                    pairs: ["EUR/USD", "USD/JPY", "AUD/USD", "GBP/USD", "EUR/JPY", "GBP/JPY"],
                    pt: {
                        headline: "O livro de segunda é anterior ao CPI — os seis pares ficam em AGUARDAR",
                        summary: "A taxa BCE/Frankfurter de 09/11 saiu antes do CPI de outubro dos EUA (10/11, 13:30 UTC). O consenso é 0,3% m/m depois de 0,6% em setembro, e 0,2% no núcleo depois de 0,3%. O BLS não publica a variação anual deste mês. No print: EUR/USD 1,1193 (+0,25%), ainda entre 1.1130 e 1.1267. USD/JPY 157,95 (−0,24%), 65 pips sob a SMA200. AUD/USD 0,6894 (+0,34%), 23 pips acima da mínima de sexta e dentro do piso de 64. GBP/USD 1,3416 (+0,23%), 11 pips sob a SMA200; o short de 22/10 já fechou no stop em 04/11. EUR/JPY 176,79 e GBP/JPY 211,91 quase parados. Nenhum par passa no portão de 1:2 com caminho limpo, e o filtro de eventos fecha a janela até o dado.",
                        take: "Segunda não contém o CPI. A geometria já mandava esperar; o calendário só confirma. A mesa reavalia depois das 13:30 UTC."
                    },
                    en: {
                        headline: "Monday's book predates CPI — all six pairs stay on WAIT",
                        summary: "The 09/11 ECB/Frankfurter fixing was set before the US October CPI (Nov 10, 13:30 UTC). Consensus is 0.3% m/m after 0.6% in September, and 0.2% on the core after 0.3%. The BLS is not publishing a year-on-year rate this month. In the print: EUR/USD 1.1193 (+0.25%), still between 1.1130 and 1.1267. USD/JPY 157.95 (−0.24%), 65 pips under the SMA200. AUD/USD 0.6894 (+0.34%), 23 pips off Friday's low and inside the 64-pip floor. GBP/USD 1.3416 (+0.23%), 11 pips under the SMA200; the Oct 22 short already stopped out on Nov 4. EUR/JPY 176.79 and GBP/JPY 211.91 barely moved. No pair clears the 1:2 gate with a clean path, and the event filter closes the window until the print.",
                        take: "Monday does not contain CPI. The geometry already said wait; the calendar only confirms it. The desk reassesses after 13:30 UTC."
                    }
                },
'''

NEWS_CARD = r'''                <!-- News 10/11/2026: Monday fixing predates US CPI; all six pairs stay on WAIT -->
                <article class="news-card">
                    <div class="news-card-top">
                        <span class="news-cat"><span class="lang-en">Macro Data</span><span class="lang-pt" style="display:none;">Dados Macro</span></span>
                        <span class="impact-badge high"><span class="lang-en">High Impact</span><span class="lang-pt" style="display:none;">Impacto Alto</span></span>
                        <span class="news-date">10/11/2026</span>
                    </div>
                    <h2 class="news-title">
                        <span class="lang-en">Monday's book predates CPI — all six pairs stay on WAIT</span>
                        <span class="lang-pt" style="display:none;">O livro de segunda é anterior ao CPI — os seis pares ficam em AGUARDAR</span>
                    </h2>
                    <p class="news-summary">
                        <span class="lang-en">The 09/11 ECB/Frankfurter fixing was set before the US October CPI (Nov 10, 13:30 UTC). Consensus is 0.3% m/m after 0.6% in September, and 0.2% on the core after 0.3%. The BLS is not publishing a year-on-year rate this month. In the print: EUR/USD 1.1193 (+0.25%), still between 1.1130 and 1.1267. USD/JPY 157.95 (−0.24%), 65 pips under the SMA200. AUD/USD 0.6894 (+0.34%), 23 pips off Friday's low and inside the 64-pip floor. GBP/USD 1.3416 (+0.23%), 11 pips under the SMA200; the Oct 22 short already stopped out on Nov 4. EUR/JPY 176.79 and GBP/JPY 211.91 barely moved. No pair clears the 1:2 gate with a clean path, and the event filter closes the window until the print.</span>
                        <span class="lang-pt" style="display:none;">A taxa BCE/Frankfurter de 09/11 saiu antes do CPI de outubro dos EUA (10/11, 13:30 UTC). O consenso é 0,3% m/m depois de 0,6% em setembro, e 0,2% no núcleo depois de 0,3%. O BLS não publica a variação anual deste mês. No print: EUR/USD 1,1193 (+0,25%), ainda entre 1.1130 e 1.1267. USD/JPY 157,95 (−0,24%), 65 pips sob a SMA200. AUD/USD 0,6894 (+0,34%), 23 pips acima da mínima de sexta e dentro do piso de 64. GBP/USD 1,3416 (+0,23%), 11 pips sob a SMA200; o short de 22/10 já fechou no stop em 04/11. EUR/JPY 176,79 e GBP/JPY 211,91 quase parados. Nenhum par passa no portão de 1:2 com caminho limpo, e o filtro de eventos fecha a janela até o dado.</span>
                    </p>
                    <div class="news-take">
                        <span class="take-tag"><span class="lang-en">Desk take</span><span class="lang-pt" style="display:none;">Leitura da mesa</span></span>
                        <span class="lang-en">Monday does not contain CPI. The geometry already said wait; the calendar only confirms it. The desk reassesses after 13:30 UTC.</span>
                        <span class="lang-pt" style="display:none;">Segunda não contém o CPI. A geometria já mandava esperar; o calendário só confirma. A mesa reavalia depois das 13:30 UTC.</span>
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
        "EUR/USD": "+0.25%", "USD/JPY": "-0.24%", "AUD/USD": "+0.34%",
        "GBP/USD": "+0.23%", "EUR/JPY": "+0.01%", "GBP/JPY": "-0.01%",
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

    s = idx.find("const forexData = {"); s2 = idx.find("{", s)
    e = idx.find("\n};", s) + len("\n};")
    parsed = json.loads(idx[s2:e][:-1].rstrip())
    assert list(parsed) == list(DATA)
    if idx.count(TS) != 4:
        raise SystemExit("timestamp count %d" % idx.count(TS))
    with open(INDEX, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(idx)
    print("index.html patched")

    with open(LEDGER, encoding="utf-8") as f:
        ledger = json.load(f)
    assert ledger["watching"] == []
    assert ledger["open"] == []
    ledger["meta"]["lastUpdated"] = "10/11/2026"
    with open(LEDGER, "w", encoding="utf-8", newline="\n") as f:
        json.dump(ledger, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("ledger lastUpdated only; watching and open stay empty")

    with open(NEWS, encoding="utf-8") as f:
        news = f.read()
    news = news.replace("Market Wire · NFP 165k, Aussie Makes a 20-Day Low", "Market Wire · Monday Book, CPI Still Ahead")
    news = news.replace("Telégrafo da Mesa · NFP 165k, Aussie Faz a Mínima de 20 Pregões", "Telégrafo da Mesa · Livro de Segunda, CPI Ainda à Frente")
    news = news.replace(OLD_TS, TS)
    old_cpi = '''                    <span class="cal-date">10/11</span>
                    <span class="cal-event"><span class="lang-en">US CPI — 13:30 UTC (BLS)</span><span class="lang-pt" style="display:none;">CPI dos EUA — 13:30 UTC (BLS)</span></span>'''
    new_cpi = '''                    <span class="cal-date">10/11</span>
                    <span class="cal-event"><span class="lang-en">US CPI due 13:30 UTC, consensus 0.3% m/m — not in the 09/11 fixing</span><span class="lang-pt" style="display:none;">CPI dos EUA às 13:30 UTC, consenso 0,3% m/m — fora do fechamento de 09/11</span></span>'''
    if old_cpi not in news:
        raise SystemExit("CPI calendar cell missing")
    news = news.replace(old_cpi, new_cpi, 1)
    marker = "                <!-- News 06/11/2026:"
    if marker not in news:
        raise SystemExit("news marker missing")
    news = news.replace(marker, NEWS_CARD + marker, 1)
    with open(NEWS, "w", encoding="utf-8", newline="\n") as f:
        f.write(news)
    print("news.html patched")

    with open(SITEMAP, encoding="utf-8") as f:
        sm = f.read()
    n = sm.count("2026-11-06")
    if n != 9:
        raise SystemExit("expected 9 sitemap dates, found %d" % n)
    sm = sm.replace("2026-11-06", "2026-11-10")
    with open(SITEMAP, "w", encoding="utf-8", newline="\n") as f:
        f.write(sm)
    print("sitemap patched")

    with open(VERIFY, encoding="utf-8") as f:
        v = f.read()
    v = v.replace('TODAY_TS = "06/11/2026 20:10 UTC"', 'TODAY_TS = "%s"' % TS)
    v = v.replace(
        'TODAY_DATE = "06/11/2026"  # basis session date (report edition: 06/11/2026)',
        'TODAY_DATE = "09/11/2026"  # basis session date (report edition: 10/11/2026)')
    old_ticker = '''TICKER = [("EUR/USD","-0.53%"),("USD/JPY","-0.08%"),("AUD/USD","-1.85%"),
          ("GBP/USD","-0.55%"),("EUR/JPY","-0.61%"),("GBP/JPY","-0.63%")]'''
    new_ticker = '''TICKER = [("EUR/USD","+0.25%"),("USD/JPY","-0.24%"),("AUD/USD","+0.34%"),
          ("GBP/USD","+0.23%"),("EUR/JPY","+0.01%"),("GBP/JPY","-0.01%")]'''
    if old_ticker not in v:
        raise SystemExit("ticker block missing")
    v = v.replace(old_ticker, new_ticker)
    with open(VERIFY, "w", encoding="utf-8", newline="\n") as f:
        f.write(v)
    print("verify constants patched")

if __name__ == "__main__":
    main()
