# -*- coding: utf-8 -*-
"""Daily report build — 20/10/2026 edition.

Basis: Frankfurter/ECB daily reference rates, last close 20/10/2026 (567 sessions
since 01/08/2024). MT5 terminal unavailable (no FX data) — ECB fallback source.

Market summary of the two new sessions (19-20/10):
- EUR/USD 1.1215 (-0.09%): second down close after Friday's dollar sweep; no extreme
  threatened (9-mo low 1.1177 intact, shelf 1.1260-1.1300 untouched). Ticket re-armed unchanged.
- USD/JPY 158.13 (-0.07%): sideways under the SMA200; bear alignment 3 closes old. WAIT stands.
- AUD/USD 0.6985 (-0.02%): dead session inside 0.6911-0.7010; mixed alignment. WAIT stands.
- GBP/USD 1.3347 (+0.12%): close AT the 10- AND 20-day highs (first breakout close) —
  overran the 1.3290-1.3330 band into Wednesday's UK CPI (21/10 07:00 London, ONS-confirmed).
  Ticket re-priced one shelf up: 1.3360-1.3420 (broken 22/09 close + SMA50/Fib 61.8%/1.3400),
  stop 1.3460 (over SMA200 1.3434 + 1.3450 round; >= 65-pip 1.5-sigma20 floor),
  target 1.3250 (above the 10-day low, crossing only rounds).
- EUR/JPY 177.34 (-0.16%): bounce died at the 10-day high 177.82. WAIT stands (BoJ 29-30/10).
- GBP/JPY 211.05 (+0.05%): second straight 10/20-day-high close; SMA50 211.55 shelf still
  fails the 1:2 path gate. WAIT stands.
"""
import json, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

INDEX = r"C:\Projetos\forex-report\docs\index.html"
NEWS = r"C:\Projetos\forex-report\docs\news.html"
LEDGER = r"C:\Projetos\forex-report\docs\track-record.json"
SITEMAP = r"C:\Projetos\forex-report\docs\sitemap.xml"

STAMP = "20/10/2026 20:46 UTC"
OLD_STAMP = "18/10/2026 19:11 UTC"

def sub1(text, old, new, name, count=None):
    n = text.count(old)
    expected = count if count is not None else 1
    assert n == expected, "%s: found %d occurrences of %r (expected %d)" % (name, n, old[:60], expected)
    return text.replace(old, new)

# =====================================================================
# 1. forexData — full six-pair replacement (canonical order preserved)
# =====================================================================
forex = {
    "EUR/USD": {
        "quote": "1.1215",
        "bias": "BAIXA",
        "biasType": "bear",
        "pt": {
            "fundamental": "O EUR/USD fechou em 1,1215 na sessão de terça 20/10/2026 (taxa de referência BCE/Frankfurter; o terminal MT5 logado segue sem retornar dados de FX), caindo -0,09% — o segundo fechamento de queda seguido depois da varredura de sexta: o dólar estabilizou contra o euro dentro do blackout do Fed (FOMC em 27-28/10) e o par devolveu 38 pips do repique sem ameaçar nenhum dos dois extremos — a mínima de 9 meses 1.1177 no chão e a prateleira 1.1260-1.1300 a mais de 45 pips de distância. O CPI de setembro (14/10) quente (3,7% a/a, gasolina +34%, núcleo 2,6%) e o discurso de sexta do chairman seguem como pano de fundo; o shutdown parcial de 1/10 (DHS, segundo mais longo da história) tem acordo relatado para terminar. Alinhamento de baixa pleno (fechamento sob a SMA200 1,1581, SMA50 1,1460 abaixo dela) — o mapa mantém o fade da prateleira 1.1260-1.1300 armado desde 18/10, rearmado sem mudanças. FOMC em 27-28/10. Indicadores (SMA 50/200, σ20, Donchian e Fibonacci) calculados da série diária BCE/Frankfurter (567 pregões, 01/08/2024 a 20/10/2026).",
            "trend": "Fechamento sob a SMA200 (1,1581) com a SMA50 (1,1460) abaixo dela — alinhamento de baixa pleno. A mínima de 9 meses e de 10/20 pregões (1.1177, 07/10) segue invicta (dois erros por pouco em 12-13/10); o teto imediato é a máxima de 10 pregões (1.1253, 16/10), com a prateleira 1.1260-1.1300 logo acima.",
            "support": "1.1177 (mínima de 9 meses e de 10/20 pregões, 07/10), com o redondo 1.1150 como único obstáculo até o alvo 1.1120.",
            "resistance": "1.1253 (máxima de 10 pregões, 16/10) e a prateleira 1.1260-1.1300, coroados pelo duplo fechamento 1.1355 (29-30/09).",
            "priceAction": "Fade do repique na prateleira: o gatilho é um fechamento diário dentro de 1.1260-1.1300 seguido de um fechamento abaixo do fechamento anterior e do meio da faixa 1.1280 (entrada de referência 1.1280). Stop 1.1360 (80 pips, sobre o duplo fechamento 1.1355 e a Fib 78,6% 1.1348; ≥ piso 1,5σ20 de 59 pips). Alvo 1.1120 (160 pips), sob a mínima de 9 meses e acima do redondo 1.1100, cruzando apenas o redondo 1.1150. Só contam fechamentos depois desta edição; o fechamento de 28/10 (FOMC) não arma.",
            "recommendation": "VENDA (SHORT) NA RETRAÇÃO",
            "trigger": "Fechamento diário dentro de 1.1260-1.1300 e um fechamento seguinte abaixo do anterior e do meio 1.1280 — entrada de referência 1.1280. O fechamento de 28/10 (FOMC) não arma. Válido até o fechamento de 30/10.",
            "stop": "1.1360 (80 pips, sobre o duplo fechamento de 29-30/09 em 1.1355 e a Fib 78,6% 1.1348; ≥ piso 1,5σ20 de 59 pips) · risco sugerido ≤ 1% por operação.",
            "target": "1.1120 (160 pips), sob a mínima de 9 meses 1.1177 e acima do redondo 1.1100 — cruzando apenas o redondo 1.1150.",
            "rr": "1:2.00",
            "rrValue": 50,
            "justification": "Dois fechamentos de queda deram ao dólar a estabilização que faltava, mas nenhum tocou nos extremos: a mínima não se persegue por cima e o repique nunca pagou a prateleira. O fade em 1.1260-1.1300 mantém a localização — stop estrutural sobre o duplo 1.1355, 1:2,00 até 1.1120 cruzando só o redondo 1.1150. O diferencial Fed-BCE (3,75-4,00% contra 2,50% parado) segue como argumento de fundo; o FOMC de 27-28/10 é o árbitro e filtra o fechamento de 28/10."
        },
        "en": {
            "fundamental": "EUR/USD closed at 1.1215 in the Tuesday 20/10/2026 session (ECB/Frankfurter reference rate; the logged-in MT5 terminal still returns no FX data), down -0.09% — the second down close in a row after Friday's sweep: the dollar steadied against the euro inside the Fed blackout (FOMC on Oct 27-28) and the pair gave back 38 pips of the bounce without threatening either extreme — the 9-month low 1.1177 on the floor and the 1.1260-1.1300 shelf more than 45 pips away. September's hot CPI (Oct 14: 3.7% y/y, gasoline +34%, core 2.6%) and Friday's chair speech stay the backdrop; the partial shutdown (since Oct 1, DHS, second-longest in history) has a reported deal to end it. Full bear alignment (close under the SMA200 1.1581, 50-day 1.1460 below it) — the map keeps the 1.1260-1.1300 shelf fade armed from Oct 18, re-armed unchanged. FOMC on Oct 27-28. Indicators (SMA 50/200, sigma20, Donchian and Fibonacci) computed from the ECB/Frankfurter daily series (567 sessions, 01/08/2024 to 20/10/2026).",
            "trend": "Close under the SMA200 (1.1581) with the 50-day (1.1460) below it — full bear alignment. The 9-month and 10/20-day low (1.1177, Oct 7) still stands (two near-misses on Oct 12-13); the immediate ceiling is the 10-day high (1.1253, Oct 16), with the 1.1260-1.1300 shelf right above.",
            "support": "1.1177 (the 9-month and 10/20-day low, Oct 7), with the 1.1150 round as the only obstacle down to the 1.1120 target.",
            "resistance": "1.1253 (the 10-day high, Oct 16) and the 1.1260-1.1300 shelf, crowned by the double close at 1.1355 (Sep 29-30).",
            "priceAction": "Fade the rally on the shelf: the trigger is a daily close inside 1.1260-1.1300 followed by a close below the previous close and the 1.1280 midpoint (entry reference 1.1280). Stop 1.1360 (80 pips, over the 1.1355 double close and the 78.6% Fib 1.1348; >= the 59-pip 1.5-sigma20 floor). Target 1.1120 (160 pips), under the 9-month low and above the 1.1100 round, crossing only the 1.1150 round. Only closes after this edition count; the Oct-28 close (FOMC) doesn't arm.",
            "recommendation": "SELL (SHORT) ON PULLBACK",
            "trigger": "A daily close inside 1.1260-1.1300 and a following close below the previous close and the 1.1280 midpoint — entry reference 1.1280. The Oct-28 close (FOMC) doesn't arm. Valid through the Oct-30 close.",
            "stop": "1.1360 (80 pips, over the Sep 29-30 double close at 1.1355 and the 78.6% Fib 1.1348; >= the 59-pip 1.5-sigma20 floor) · suggested risk ≤ 1% per trade.",
            "target": "1.1120 (160 pips), under the 9-month low 1.1177 and above the 1.1100 round — crossing only the 1.1150 round.",
            "rr": "1:2.00",
            "rrValue": 50,
            "justification": "Two down closes gave the dollar the steadying it lacked, but neither touched the extremes: the low is not chased from above and the rally never paid the shelf. The fade at 1.1260-1.1300 keeps the location — structural stop over the 1.1355 double close, 1:2.00 to 1.1120 crossing only the 1.1150 round. The Fed-ECB differential (3.75-4.00% against a frozen 2.50%) stays the background argument; the Oct 27-28 FOMC referees and filters the Oct-28 close."
        }
    },
    "USD/JPY": {
        "quote": "158.13",
        "bias": "BAIXA",
        "biasType": "bear",
        "pt": {
            "fundamental": "O USD/JPY fechou em 158,13 na sessão de terça 20/10/2026 (taxa de referência BCE/Frankfurter), caindo -0,07% — segunda sessão lateral sob a SMA200 (158,55): o alinhamento de baixa criado na sexta (fechamento sob a SMA200 com a SMA50 157,68 abaixo dela) completou três fechamentos sem devolver a média. O blackout do Fed já vale (FOMC 27-28/10) e o consenso para o BoJ de 29-30/10 segue em alta para 1,25% (política a ~1% desde setembro). O CPI dos EUA (14/10) quente (3,7% a/a, gasolina +34%, núcleo 2,6%) é o dado que o dólar carrega; a janela formal de 30 dias dos rate checks do MoF de meados de setembro permanece fechada — piso 1,5σ20 (82 pips), com o risco MoF a 158 como narrativa. Indicadores calculados da série diária BCE/Frankfurter (567 pregões, 01/08/2024 a 20/10/2026).",
            "trend": "Fechamento sob a SMA200 (158,55) com a SMA50 (157,68) abaixo dela — alinhamento de baixa com três fechamentos de idade. As máximas de 10 pregões (158,60) e de 20 (158,85) tampam por cima junto com a Fib 50% (158,27); a mínima de 10 (157,98, 15/10) está a 15 pips.",
            "support": "157.98 (mínima de 10 pregões, 15/10), com o fechamento de 02/10 (157,67), o redondo 157,00 e a mínima de 20 pregões (156,88) na escada abaixo.",
            "resistance": "158.60 (máxima de 10 pregões, 12/10) e a SMA200 (158,55), com a máxima de 20 pregões em 158,85.",
            "priceAction": "O rompimento da mínima de 10 pregões 157,98 segue sendo o gatilho natural, mas o piso de 1,5σ20 (82 pips) força stop sobre a SMA200 e o alvo de 1:2 cai perto de 156,15 — atravessando o fechamento de 02/10 (157,67), o redondo 157,00 e a mínima de 20 pregões (156,88): caminho bloqueado. O repique até a região 158,55-158,85 (SMA200 + máxima de 20) tampouco paga 1:2 limpo contra a mesma escada. Ou o preço perde 157,00 com fechamento (limpando a escada até 155,69, fechamento de 17/09), ou não há ticket. FOMC 27-28/10 e BoJ 29-30/10 na sequência.",
            "recommendation": "AGUARDAR OUTRO GATILHO",
            "trigger": "157.98 — a mínima de 10 pregões — é o rompimento natural, mas o caminho do 1:2 está bloqueado pelo fechamento 157,67, pelo redondo 157,00 e pela mínima de 20 pregões 156,88. Reavaliar após o cluster FOMC (27-28/10) + BoJ (29-30/10).",
            "stop": "N/A (sem operação).",
            "target": "N/A (sem operação).",
            "rr": "N/A",
            "rrValue": 0,
            "justification": "A baixa sob a SMA200 fez três fechamentos sem acelerar: o preço respingou na SMA50 (157,68) e devolveu. A geometria segue reprovando os dois lados — o 1:2 da venda atravessa três degraus (157,67, 157,00 e 156,88) e a compra brigaria com a média de 200. O cluster Fed-BoJ de 27-30/10 reprecifica o corredor: a alta consensada do BoJ para 1,25% é o que pode limpar um dos lados."
        },
        "en": {
            "fundamental": "USD/JPY closed at 158.13 in the Tuesday 20/10/2026 session (ECB/Frankfurter reference rate), down -0.07% — a second sideways session under the SMA200 (158.55): the bear alignment created on Friday (close under the SMA200 with the 50-day 157.68 below it) is now three closes old without giving the average back. The Fed blackout is on (FOMC Oct 27-28) and the consensus for the Oct 29-30 BoJ stays a hike to 1.25% (policy at ~1% since September). The hot US CPI (Oct 14: 3.7% y/y, gasoline +34%, core 2.6%) is the print the dollar carries; the MoF's mid-September rate-check 30-day window remains closed — floor at 1.5-sigma20 (82 pips), with MoF risk at 158 as narrative. Indicators computed from the ECB/Frankfurter daily series (567 sessions, 01/08/2024 to 20/10/2026).",
            "trend": "Close under the SMA200 (158.55) with the 50-day (157.68) below it — a bear alignment three closes old. The 10-day high (158.60) and the 20-day (158.85) cap above alongside the 50% Fib (158.27); the 10-day low (157.98, Oct 15) sits 15 pips below.",
            "support": "157.98 (the 10-day low, Oct 15), with the Oct-2 close (157.67), the 157.00 round and the 20-day low (156.88) down the ladder.",
            "resistance": "158.60 (the 10-day high, Oct 12) and the SMA200 (158.55), with the 20-day high at 158.85.",
            "priceAction": "A break of the 10-day low 157.98 remains the natural trigger, but the 1.5-sigma20 floor (82 pips) forces the stop over the SMA200 and the 1:2 target lands near 156.15 — crossing the Oct-2 close (157.67), the 157.00 round and the 20-day low (156.88): path blocked. A pullback into the 158.55-158.85 area (SMA200 + 20-day high) pays no clean 1:2 against the same ladder either. Either price loses 157.00 on a close (clearing the ladder toward 155.69, the Sep-17 close), or there is no ticket. FOMC Oct 27-28 and BoJ Oct 29-30 in sequence.",
            "recommendation": "WAIT FOR ANOTHER TRIGGER",
            "trigger": "157.98 — the 10-day low — is the natural break, but the 1:2 path is blocked by the 157.67 close, the 157.00 round and the 20-day low 156.88. Reassess after the FOMC (Oct 27-28) + BoJ (Oct 29-30) cluster.",
            "stop": "N/A (no trade).",
            "target": "N/A (no trade).",
            "rr": "N/A",
            "rrValue": 0,
            "justification": "The bear flip under the SMA200 is three closes old without accelerating: price bounced on the 50-day (157.68) and gave it back. Geometry still rejects both sides — the short's 1:2 crosses three rungs (157.67, 157.00, 156.88) and a long would fight the 200-day. The Fed-BoJ cluster of Oct 27-30 reprices the corridor: the consensus BoJ hike to 1.25% is what can clear one side."
        }
    },
    "AUD/USD": {
        "quote": "0.6985",
        "bias": "NEUTRO",
        "biasType": "neutral",
        "pt": {
            "fundamental": "O AUD/USD fechou em 0,6985 na sessão de terça 20/10/2026 (taxa de referência BCE/Frankfurter), estável em -0,02% — segunda sessão de tédio dentro do canal 0.6911-0.7010. A leitura segue NEUTRA: preço sob a SMA200 (0,7041) e a SMA50 (0,7081), mas a SMA50 continua acima da SMA200, e nenhum fechamento foi além dos extremos de 10 pregões. O motor commodity segue de pé (CPI australiano a 3,5%, WTI ~US$ 83 — a mesma energia que imprimiu 3,7% no CPI americano) e o CPI do Q3 (≈28/10) é o árbitro local antes da leitura da RBA para novembro. Sem rompimento confirmado não há ticket. Indicadores calculados da série diária BCE/Frankfurter (567 pregões, 01/08/2024 a 20/10/2026).",
            "trend": "Misto por construção: fechamento sob as duas médias com a SMA50 ainda acima da SMA200. A faixa 0.6911-0.7010 (extremos de 10/20 pregões) trancou mais uma semana; a recaptura da SMA200 com segundo fechamento resolve para cima, a perda de 0.6911 para baixo.",
            "support": "0.6911 (mínima de 10/20 pregões, 15/10), com o redondo 0,6900 abaixo.",
            "resistance": "0.7010 (máxima de 10 pregões, 14/10), com a SMA200 (0,7041) e a Fib 38,2% (0,7043) formando o teto real.",
            "priceAction": "Sem gatilho: nenhum fechamento além dos extremos do canal. Um fechamento sobre 0.7010 seria o primeiro passo (o segundo, contra a SMA200 0,7041, resolveria o misto); um fechamento sob 0.6911 abre 0.6900 e o vácuo até a mínima de 9 meses (0.6698). O CPI do Q3 (≈28/10) escolhe o lado.",
            "recommendation": "AGUARDAR OUTRO GATILHO",
            "trigger": "0.7010 é o teto a romper primeiro; 0.6911 o piso. Sem rompimento confirmado não há ticket — reavaliar após o CPI australiano do Q3 (≈28/10).",
            "stop": "N/A (sem operação).",
            "target": "N/A (sem operação).",
            "rr": "N/A",
            "rrValue": 0,
            "justification": "Outra sessão dentro do canal com o alinhamento misto intacto: perseguir direção dentro de 0.6911-0.7010 é pagar caro por uma escolha de lado que o preço ainda não fez. O CPI do Q3 (≈28/10) e a leitura da RBA para novembro são o que pode destravar."
        },
        "en": {
            "fundamental": "AUD/USD closed at 0.6985 in the Tuesday 20/10/2026 session (ECB/Frankfurter reference rate), flat at -0.02% — a second dull session inside the 0.6911-0.7010 channel. The read stays NEUTRAL: price under the SMA200 (0.7041) and the 50-day (0.7081), but the 50-day still holds above the SMA200, and no close has gone beyond the 10-day extremes. The commodity engine still stands (Australian CPI at 3.5%, WTI ~$83 — the same energy that printed 3.7% on US CPI) and the Q3 CPI (≈Oct 28) is the local arbiter before the RBA's November read. Without a confirmed breakout there is no ticket. Indicators computed from the ECB/Frankfurter daily series (567 sessions, 01/08/2024 to 20/10/2026).",
            "trend": "Mixed by construction: close under both averages with the 50-day still above the SMA200. The 0.6911-0.7010 range (10/20-day extremes) locked another week; reclaiming the SMA200 with a second close resolves it up, losing 0.6911 resolves it down.",
            "support": "0.6911 (the 10/20-day low, Oct 15), with the 0.6900 round below.",
            "resistance": "0.7010 (the 10-day high, Oct 14), with the SMA200 (0.7041) and the 38.2% Fib (0.7043) forming the real ceiling.",
            "priceAction": "No trigger: no close beyond the channel's extremes. A close over 0.7010 would be the first step (the second, against the SMA200 at 0.7041, would resolve the mix); a close under 0.6911 opens 0.6900 and the vacuum down to the 9-month low (0.6698). The Q3 CPI (≈Oct 28) picks the side.",
            "recommendation": "WAIT FOR ANOTHER TRIGGER",
            "trigger": "0.7010 is the ceiling to break first; 0.6911 the floor. No confirmed break, no ticket — reassess after the Australian Q3 CPI (≈Oct 28).",
            "stop": "N/A (no trade).",
            "target": "N/A (no trade).",
            "rr": "N/A",
            "rrValue": 0,
            "justification": "Another session inside the channel with the mixed alignment intact: chasing direction inside 0.6911-0.7010 is overpaying for a side-selection price hasn't made. The Q3 CPI (≈Oct 28) and the RBA's November read are what can unlock it."
        }
    },
    "GBP/USD": {
        "quote": "1.3347",
        "bias": "BAIXA",
        "biasType": "bear",
        "pt": {
            "fundamental": "O GBP/USD fechou em 1,3347 na sessão de terça 20/10/2026 (taxa de referência BCE/Frankfurter), subindo +0,12% — fechamento NAS máximas de 10 e 20 pregões, o primeiro além do extremo do canal: terceiro ganho diário seguido rumo ao CPI de setembro, que decide quarta 21/10 às 07:00 de Londres (agosto veio em 3,1%, o maior em cinco meses, com a carta do governador projetando ~3¾% no Q4 e o mercado precificando altas do BoE até dezembro; o BoE decide em 05/11). A faixa 1.3290-1.3330 foi atropelada — o ticket de 18/10 foi revogado sem disparar e a prateleira sobe para o cluster SMA: 1.3360-1.3420 (fechamento quebrado de 22/09 em 1.3363 + SMA50 1,3416 / Fib 61,8% 1,3411 / redondo 1.3400). O alinhamento de baixa segue pleno (fechamento sob a SMA200 1,3434 e a SMA50 1,3416). Indicadores calculados da série diária BCE/Frankfurter (567 pregões, 01/08/2024 a 20/10/2026).",
            "trend": "Fechamento sob a SMA200 (1,3434) com a SMA50 (1,3416) abaixo dela — alinhamento de baixa pleno, agora testado: o fechamento nas máximas de 10/20 pregões (1.3347) é o primeiro rompimento de alta em três semanas, e o cluster SMA (1,3411-1,3434) é o teto estrutural imediato.",
            "support": "1.3205 (mínima de 10 pregões, 07/10; a de 20 fica em 1.3201), com a mínima de 9 meses em 1.3160 embaixo.",
            "resistance": "O cluster 1.3360-1.3420 (fechamento quebrado de 22/09 + Fib 61,8% 1,3411 + SMA50 1,3416 + redondo 1.3400), coroado pela SMA200 (1,3434) e pela Fib 50% (1,3489).",
            "priceAction": "Fade da prateleira reprecificada 1.3360-1.3420: o gatilho é um fechamento diário dentro da prateleira seguido de fechamento abaixo do anterior e do meio 1.3390 (entrada de referência 1.3390). Stop 1.3460 (70 pips, sobre a SMA200 1,3434 e o redondo 1.3450; ≥ piso 1,5σ20 de 65 pips). Alvo 1.3250 (140 pips), acima da mínima de 10 pregões e cruzando apenas os redondos 1.3350 e 1.3300. O fechamento de 21/10 já é pós-CPI e arma; o de 28/10 (FOMC) não arma.",
            "recommendation": "VENDA (SHORT) NA RETRAÇÃO",
            "trigger": "Fechamento diário dentro de 1.3360-1.3420 e um fechamento seguinte abaixo do anterior e do meio 1.3390 — entrada de referência 1.3390. O fechamento de 21/10 (pós-CPI) arma; o de 28/10 (FOMC) não arma. Válido até o fechamento de 30/10.",
            "stop": "1.3460 (70 pips, sobre a SMA200 1,3434 e o redondo 1.3450; ≥ piso 1,5σ20 de 65 pips) · risco sugerido ≤ 1% por operação.",
            "target": "1.3250 (140 pips), acima da mínima de 10 pregões 1.3205 — cruzando apenas os redondos 1.3350 e 1.3300.",
            "rr": "1:2.00",
            "rrValue": 50,
            "justification": "A libra atropelou a faixa e cravou a máxima de 20 pregões na véspera do CPI — o fade sobe de andar em vez de perseguir: a prateleira 1.3360-1.3420 encosta no cluster SMA50/Fib 61,8%/SMA200, o teto estrutural da baixa. Vender ali com stop 1.3460 (acima da SMA200) paga 1:2,00 até 1.3250 cruzando só redondos. Se o CPI de quarta atropelar o cluster com fechamento, o mapa de baixa se quebra — até lá, localização é tudo."
        },
        "en": {
            "fundamental": "GBP/USD closed at 1.3347 in the Tuesday 20/10/2026 session (ECB/Frankfurter reference rate), up +0.12% — a close AT the 10- and 20-day highs, the first beyond the channel extreme: a third daily gain in a row into September's CPI, which decides Wednesday Oct 21 at 07:00 London (August printed 3.1%, the highest in five months, with the governor's letter projecting ~3¾% in Q4 and the market pricing BoE hikes by December; the BoE decides Nov 5). The 1.3290-1.3330 band was overrun — the Oct-18 ticket was revoked unfired and the shelf moves up to the SMA cluster: 1.3360-1.3420 (the broken Sep-22 close at 1.3363 + SMA50 1.3416 / 61.8% Fib 1.3411 / the 1.3400 round). Bear alignment still full (close under the SMA200 1.3434 and the 50-day 1.3416). Indicators computed from the ECB/Frankfurter daily series (567 sessions, 01/08/2024 to 20/10/2026).",
            "trend": "Close under the SMA200 (1.3434) with the 50-day (1.3416) below it — full bear alignment, now tested: the close at the 10/20-day highs (1.3347) is the first upside breakout close in three weeks, and the SMA cluster (1.3411-1.3434) is the immediate structural ceiling.",
            "support": "1.3205 (the 10-day low, Oct 7; the 20-day sits at 1.3201), with the 9-month low at 1.3160 below.",
            "resistance": "The 1.3360-1.3420 cluster (the broken Sep-22 close + the 61.8% Fib 1.3411 + the SMA50 1.3416 + the 1.3400 round), crowned by the SMA200 (1.3434) and the 50% Fib (1.3489).",
            "priceAction": "Fade the re-priced 1.3360-1.3420 shelf: the trigger is a daily close inside the shelf followed by a close below the previous close and the 1.3390 midpoint (entry reference 1.3390). Stop 1.3460 (70 pips, over the SMA200 1.3434 and the 1.3450 round; >= the 65-pip 1.5-sigma20 floor). Target 1.3250 (140 pips), above the 10-day low and crossing only the 1.3350 and 1.3300 rounds. The Oct-21 close is already post-CPI and arms; the Oct-28 close (FOMC) doesn't arm.",
            "recommendation": "SELL (SHORT) ON PULLBACK",
            "trigger": "A daily close inside 1.3360-1.3420 and a following close below the previous close and the 1.3390 midpoint — entry reference 1.3390. The Oct-21 close (post-CPI) arms; the Oct-28 close (FOMC) doesn't. Valid through the Oct-30 close.",
            "stop": "1.3460 (70 pips, over the SMA200 1.3434 and the 1.3450 round; >= the 65-pip 1.5-sigma20 floor) · suggested risk ≤ 1% per trade.",
            "target": "1.3250 (140 pips), above the 10-day low 1.3205 — crossing only the 1.3350 and 1.3300 rounds.",
            "rr": "1:2.00",
            "rrValue": 50,
            "justification": "Sterling overran the band and pinned the 20-day high on CPI eve — the fade moves up a floor instead of chasing: the 1.3360-1.3420 shelf leans on the SMA50/61.8% Fib/SMA200 cluster, the structural ceiling of the bear. Selling there with a 1.3460 stop (over the SMA200) pays 1:2.00 to 1.3250 crossing only rounds. If Wednesday's CPI overruns the cluster on a close, the bear map breaks — until then, location is everything."
        }
    },
    "EUR/JPY": {
        "quote": "177.34",
        "bias": "BAIXA",
        "biasType": "bear",
        "pt": {
            "fundamental": "O EUR/JPY fechou em 177,34 na sessão de terça 20/10/2026 (taxa de referência BCE/Frankfurter), caindo -0,16% — segundo fechamento de queda seguido: o repique de sexta morreu na máxima de 10 pregões (177,82) e devolveu 48 pips sem testar a mínima de 9 meses (176,85, 07/10). O alinhamento segue de baixa pleno (fechamento sob a SMA200 183,60, SMA50 180,70 abaixo dela). A janela formal de 30 dias dos rate checks do MoF permanece fechada: piso 1,5σ20 (97 pips) — mas a geometria continua sem pagar. O BoJ de 29-30/10 (consenso: alta para 1,25%) é o árbitro do capítulo. Indicadores calculados da série diária BCE/Frankfurter (567 pregões, 01/08/2024 a 20/10/2026).",
            "trend": "Fechamento sob a SMA200 (183,60) com a SMA50 (180,70) abaixo dela — baixa plena. A mínima de 9 meses e de 10/20 pregões (176,85) no chão; a máxima de 10 pregões (177,82, 16/10) é o teto imediato, recusado nos dois fechamentos seguintes.",
            "support": "176.85 (mínima de 9 meses e de 10/20 pregões, 07/10), com os redondos 176,00 e 175,00 abaixo.",
            "resistance": "177.82 (máxima de 10 pregões, 16/10), com a máxima de 20 pregões em 180,56 e a SMA50 (180,70) acima.",
            "priceAction": "O piso de 97 pips viabilizaria o rompimento sob 176,85 com stop sobre 177,82 — mas o alvo de 1:2 cai perto de 174,85, atravessando os redondos 176,00 e 175,00: caminho bloqueado. O repique também não paga: vender em 177,82+ brigaria com uma máxima de 10 pregões ainda não rompida para cima. Sem ticket até o BoJ (29-30/10).",
            "recommendation": "AGUARDAR OUTRO GATILHO",
            "trigger": "176.85 é a linha que importa, mas o alvo 1:2 do rompimento cai além de dois redondos — caminho bloqueado. Reavaliar após o BoJ (29-30/10).",
            "stop": "N/A (sem operação).",
            "target": "N/A (sem operação).",
            "rr": "N/A",
            "rrValue": 0,
            "justification": "O repique de sexta já foi devolvido pela metade e a mínima de 9 meses segue sem o segundo fechamento de rompimento — a matemática não mudou: de 176,80 com stop sobre 177,85, o 1:2 precisa de ~174,70 cruzando dois redondos. A mesa deixa o repique correr — se o BoJ entregar os 1,25%, a mínima volta ao foco com caminho mais limpo."
        },
        "en": {
            "fundamental": "EUR/JPY closed at 177.34 in the Tuesday 20/10/2026 session (ECB/Frankfurter reference rate), down -0.16% — a second down close in a row: Friday's bounce died at the 10-day high (177.82) and gave back 48 pips without testing the 9-month low (176.85, Oct 7). Full bear alignment stands (close under the SMA200 183.60, 50-day 180.70 below it). The MoF rate-check 30-day window remains closed: floor at 1.5-sigma20 (97 pips) — but the geometry still doesn't pay. The Oct 29-30 BoJ (consensus: a hike to 1.25%) referees the chapter. Indicators computed from the ECB/Frankfurter daily series (567 sessions, 01/08/2024 to 20/10/2026).",
            "trend": "Close under the SMA200 (183.60) with the 50-day (180.70) below it — full bear. The 9-month and 10/20-day low (176.85) floors it; the 10-day high (177.82, Oct 16) is the immediate ceiling, refused on the two closes since.",
            "support": "176.85 (the 9-month and 10/20-day low, Oct 7), with the 176.00 and 175.00 rounds below.",
            "resistance": "177.82 (the 10-day high, Oct 16), with the 20-day high at 180.56 and the 50-day (180.70) above.",
            "priceAction": "The 97-pip floor would allow the break under 176.85 with a stop over 177.82 — but the 1:2 target lands near 174.85, crossing the 176.00 and 175.00 rounds: path blocked. The bounce doesn't pay either: selling at 177.82+ would fight a 10-day high not yet broken upward. No ticket until the BoJ (Oct 29-30).",
            "recommendation": "WAIT FOR ANOTHER TRIGGER",
            "trigger": "176.85 is the line that matters, but a break's 1:2 target lands beyond two round numbers — path blocked. Reassess after the BoJ (Oct 29-30).",
            "stop": "N/A (no trade).",
            "target": "N/A (no trade).",
            "rr": "N/A",
            "rrValue": 0,
            "justification": "Friday's bounce has already been half-returned and the 9-month low still lacks its second breakout close — the math didn't change: from 176.80 with a stop over 177.85, 1:2 needs ~174.70 across two rounds. The desk lets the bounce run — if the BoJ delivers the 1.25%, the low comes back into focus with a cleaner path."
        }
    },
    "GBP/JPY": {
        "quote": "211.05",
        "bias": "BAIXA",
        "biasType": "bear",
        "pt": {
            "fundamental": "O GBP/JPY fechou em 211,05 na sessão de terça 20/10/2026 (taxa de referência BCE/Frankfurter), subindo +0,05% — segundo fechamento seguido NAS máximas de 10 e 20 pregões, com a libra comprando o CPI de quarta (21/10, 07:00 de Londres) e o iene no horizonte do BoJ (29-30/10, consenso: alta para 1,25%). O alinhamento formal segue de baixa (fechamento sob a SMA200 212,99 e a SMA50 211,55) — mas vender máximas de canal cravadas dois dias seguidos não tem estrutura, e comprar brigaria com as duas médias. Piso 1,5σ20 de 112 pips com a janela do MoF fechada. Indicadores calculados da série diária BCE/Frankfurter (567 pregões, 01/08/2024 a 20/10/2026).",
            "trend": "Fechamento sob a SMA200 (212,99) com a SMA50 (211,55) abaixo dela — baixa plena. O preço cravou as máximas de 10/20 pregões (211,05) e recuperou o redondo 211,00; a SMA50 a ~50 pips é a primeira média, com a Fib 61,8% (211,84) no meio do caminho.",
            "support": "210.00 (o redondo), com a Fib 78,6% (209,85), a mínima de 10 pregões (208,94, 07/10) e a de 20 (208,07, 28/09) abaixo.",
            "resistance": "211.55 (a SMA50), com a Fib 61,8% (211,84) e o redondo 212,00 no caminho, e a SMA200 (212,99) acima.",
            "priceAction": "A prateleira de venda segue sendo a SMA50: entrada ~211,55 com stop 212,75 (120 pips ≥ piso 112) só paga 1:2 em 209,15 — atravessando o redondo 210,00 e a Fib 78,6% (209,85): reprovado. Sem estrutura para vender máximas cravadas nem para comprar contra as médias — o par espera o CPI britânico (21/10) e o BoJ (29-30/10).",
            "recommendation": "AGUARDAR OUTRO GATILHO",
            "trigger": "211.55 (a SMA50) é a primeira prateleira de venda, mas não paga 1:2 limpo. Reavaliar após o CPI do Reino Unido (21/10) e o BoJ (29-30/10).",
            "stop": "N/A (sem operação).",
            "target": "N/A (sem operação).",
            "rr": "N/A",
            "rrValue": 0,
            "justification": "Segundo fechamento na máxima de 10/20 pregões com as duas médias acima: qualquer venda aqui é contra estrutura, e a prateleira da SMA50 reprova no caminho (210,00 + Fib 78,6%). O cluster CPI-BoJ da semana reprecifica o cruzamento — a mesa espera."
        },
        "en": {
            "fundamental": "GBP/JPY closed at 211.05 in the Tuesday 20/10/2026 session (ECB/Frankfurter reference rate), up +0.05% — a second straight close AT the 10- and 20-day highs, with sterling bid into Wednesday's CPI (Oct 21, 07:00 London) and the yen eyeing the BoJ (Oct 29-30, consensus: a hike to 1.25%). The formal alignment stays bearish (close under the SMA200 212.99 and the 50-day 211.55) — but shorting channel highs pinned two days running has no structure, and buying fights both averages. 1.5-sigma20 floor of 112 pips with the MoF window closed. Indicators computed from the ECB/Frankfurter daily series (567 sessions, 01/08/2024 to 20/10/2026).",
            "trend": "Close under the SMA200 (212.99) with the 50-day (211.55) below it — full bear. Price pinned the 10/20-day highs (211.05) and reclaimed the 211.00 round; the SMA50 ~50 pips above is the first average, with the 61.8% Fib (211.84) in between.",
            "support": "210.00 (the round), with the 78.6% Fib (209.85), the 10-day low (208.94, Oct 7) and the 20-day low (208.07, Sep 28) below.",
            "resistance": "211.55 (the SMA50), with the 61.8% Fib (211.84) and the 212.00 round in the way, and the SMA200 (212.99) above.",
            "priceAction": "The sell shelf remains the SMA50: an entry around 211.55 with a 212.75 stop (120 pips >= the 112 floor) only pays 1:2 at 209.15 — crossing the 210.00 round and the 78.6% Fib (209.85): rejected. No structure to short pinned highs or buy against the averages — the pair waits for UK CPI (Oct 21) and the BoJ (Oct 29-30).",
            "recommendation": "WAIT FOR ANOTHER TRIGGER",
            "trigger": "211.55 (the SMA50) is the first short shelf, but it pays no clean 1:2. Reassess after the UK CPI (Oct 21) and the BoJ (Oct 29-30).",
            "stop": "N/A (no trade).",
            "target": "N/A (no trade).",
            "rr": "N/A",
            "rrValue": 0,
            "justification": "A second close at the 10/20-day high with both averages above: any short here fights structure, and the SMA50 shelf fails the path gate (210.00 + the 78.6% Fib). The CPI-BoJ cluster reprices the cross this week — the desk waits."
        }
    }
}

html = open(INDEX, encoding="utf-8").read()

# --- replace the forexData block ---
s = html.find("const forexData = {")
assert s != -1
e = html.find("\n};", s)
assert e != -1
new_block = "const forexData = " + json.dumps(forex, ensure_ascii=False, indent=4)[:-1].rstrip() + "\n};"
html = html[:s] + new_block + html[e + len("\n};"):]

# --- timestamps: badge + generatedAt EN/PT + newsData.updated (4 spots) ---
html = sub1(html, OLD_STAMP, STAMP, "report stamp", count=4)

# --- dataBasis + nextEvent (i18n EN/PT) ---
html = sub1(html,
    "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 557 daily sessions (01/08/2024–06/10/2026).",
    "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 567 daily sessions (01/08/2024–20/10/2026).",
    "EN dataBasis")
html = sub1(html,
    "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, σ20 e Donchian calculados · 557 pregões (01/08/2024 a 06/10/2026).",
    "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, σ20 e Donchian calculados · 567 pregões (01/08/2024 a 20/10/2026).",
    "PT dataBasis")
html = sub1(html,
    'nextEvent: "FOMC minutes Oct 7 · Fed/ECB/BoJ Oct 27-30"',
    'nextEvent: "UK CPI Oct 21 · FOMC Oct 27-28 · BoJ Oct 29-30"',
    "EN nextEvent")
html = sub1(html,
    'nextEvent: "Ata do FOMC 07/10 · Fed/BCE/BoJ 27-30/10"',
    'nextEvent: "CPI Reino Unido 21/10 · FOMC 27-28/10 · BoJ 29-30/10"',
    "PT nextEvent")

# --- ticker (dailyChanges) ---
for pair, old, new in [
    ("EUR/USD", "+0.40%", "-0.09%"), ("USD/JPY", "+0.03%", "-0.07%"),
    ("AUD/USD", "+0.70%", "-0.02%"), ("GBP/USD", "+0.67%", "+0.12%"),
    ("EUR/JPY", "+0.43%", "-0.16%"), ("GBP/JPY", "+0.69%", "+0.05%"),
]:
    html = sub1(html, '"%s": "%s"' % (pair, old), '"%s": "%s"' % (pair, new), "ticker " + pair)

# --- macroDrivers block ---
new_drivers = '''        const macroDrivers = {
            "EUR/USD": {
                en: ["Dollar steadies in blackout", "Shelf fade 1.126-1.130 held", "9-mo low 1.1177 intact"],
                pt: ["Dólar estabiliza no blackout", "Fade 1,126-1,130 mantido", "Mín. 9 meses 1,1177 intacta"]
            },
            "USD/JPY": {
                en: ["Bear under SMA200, 3 closes", "157.67-156.88 ladder blocks", "FOMC 27-28 · BoJ 29-30/10"],
                pt: ["Baixa sob a SMA200, 3 fech.", "Escada 157,67-156,88 bloqueia", "FOMC 27-28 · BoJ 29-30/10"]
            },
            "AUD/USD": {
                en: ["Range 0.6911-0.7010 holds", "Neutral, no breakout", "Q3 CPI ≈28/10"],
                pt: ["Faixa 0,6911-0,7010 segura", "Neutro, sem rompimento", "CPI Q3 ≈28/10"]
            },
            "GBP/USD": {
                en: ["20-day high close into CPI", "Shelf up to 1.336-1.342", "UK CPI Wed 21/10"],
                pt: ["Máx. 20 preg. rumo ao CPI", "Prateleira sobe 1,336-1,342", "CPI Reino Unido qua 21/10"]
            },
            "EUR/JPY": {
                en: ["Bounce fades off 177.82", "Break path still blocked", "BoJ 29-30/10 decides"],
                pt: ["Repique morre em 177,82", "Caminho do rompimento travado", "BoJ 29-30/10 decide"]
            },
            "GBP/JPY": {
                en: ["2nd 10/20-day high close", "SMA50 211.55 shelf fails R/R", "CPI 21/10 · BoJ 29-30/10"],
                pt: ["2º fech. máx. 10/20 preg.", "SMA50 211,55 reprova o R/R", "CPI 21/10 · BoJ 29-30/10"]
            }
        };'''
md_s = html.find("        const macroDrivers = {")
md_e = html.find("\n        };", md_s)
assert md_s != -1 and md_e != -1, "macroDrivers block not found"
html = html[:md_s] + new_drivers + html[md_e + len("\n        };"):]

# --- newsData: prepend the 20/10 item + updated stamp already swapped above ---
news_item = '''                {
                    date: "20/10/2026",
                    category: "flow",
                    impact: "high",
                    pairs: ["EUR/USD", "GBP/USD", "GBP/JPY"],
                    pt: {
                        headline: "Fita de duas velocidades na véspera do CPI: o dólar estabiliza contra o euro (dois fechamentos de queda) enquanto a libra crava as máximas de 10/20 pregões — a prateleira do GBP/USD sobe para o cluster SMA 1.3360-1.3420",
                        summary: "O blackout do Fed (FOMC 27-28/10) esvaziou o tape americano e o EUR/USD devolveu 38 pips do repique de sexta sem tocar extremo nenhum (1.1215; a mínima de 9 meses 1.1177 segue invicta e a prateleira 1.1260-1.1300 intacta — o fade de 18/10 é rearmado sem mudanças). Do outro lado, o GBP/USD fechou 1.3347 (+0,12%) NAS máximas de 10 e 20 pregões — terceiro ganho diário seguido — e atropelou a faixa 1.3290-1.3330: o ticket de 18/10 foi revogado sem disparar e a mesa reprecifica o fade uma casa acima, em 1.3360-1.3420 (fechamento quebrado de 22/09 + SMA50/Fib 61,8%), stop 1.3460, alvo 1.3250, 1:2,00 — o fechamento de 21/10 já é pós-CPI (07:00 de Londres) e arma. O GBP/JPY acompanhou com o segundo fechamento seguido nas máximas de 10/20 pregões (211,05), com a SMA50 211,55 como primeira prateleira — que segue reprovando no caminho do 1:2.",
                        take: "O CPI de quarta decide o capítulo da libra: ou atropela o cluster SMA com fechamento (quebrando o mapa de baixa), ou entrega o fade na prateleira nova — o livro não persegue máxima cravada."
                    },
                    en: {
                        headline: "Two-speed tape on CPI eve: the dollar steadies against the euro (two down closes) while sterling pins the 10/20-day highs — the GBP/USD shelf moves up to the 1.3360-1.3420 SMA cluster",
                        summary: "The Fed blackout (FOMC Oct 27-28) emptied the US tape and EUR/USD gave back 38 pips of Friday's bounce without touching either extreme (1.1215; the 9-month low 1.1177 stands and the 1.1260-1.1300 shelf is intact — the Oct-18 fade is re-armed unchanged). On the other side, GBP/USD closed 1.3347 (+0.12%) AT the 10- and 20-day highs — a third daily gain — and overran the 1.3290-1.3330 band: the Oct-18 ticket was revoked unfired and the desk re-prices the fade one shelf higher, at 1.3360-1.3420 (the broken Sep-22 close + SMA50/61.8% Fib), stop 1.3460, target 1.3250, 1:2.00 — the Oct-21 close is already post-CPI (07:00 London) and arms. GBP/JPY followed with a second straight close at the 10/20-day highs (211.05), the SMA50 211.55 the first shelf — which still fails the 1:2 path gate.",
                        take: "Wednesday's CPI decides sterling's chapter: either it overruns the SMA cluster on a close (breaking the bear map) or it delivers the fade on the new shelf — the book doesn't chase a pinned high."
                    }
                },
'''
anchor = "            items: [\n"
assert html.count(anchor) == 1, "newsData items anchor not unique"
html = sub1(html, anchor, anchor + news_item, "newsData prepend")

open(INDEX, "w", encoding="utf-8", newline="").write(html)
print("OK index.html: forexData (6 pairs), stamps, ticker, macroDrivers, newsData updated")

# =====================================================================
# 2. news.html — prepend the same wire item + refresh hero
# =====================================================================
news = open(NEWS, encoding="utf-8").read()
news = sub1(news, "Wire updated: 18/10/2026 19:11 UTC", "Wire updated: " + STAMP, "news dateline EN")
news = sub1(news, "Telégrafo atualizado em: 18/10/2026 19:11 UTC", "Telégrafo atualizado em: " + STAMP, "news dateline PT")
news = sub1(news,
    '<span class="lang-en">Market Wire · The Post-CPI Reversal</span><span class="lang-pt" style="display:none;">Telégrafo da Mesa · A Reversão Pós-CPI</span>',
    '<span class="lang-en">Market Wire · CPI Eve, Two-Speed Tape</span><span class="lang-pt" style="display:none;">Telégrafo da Mesa · Véspera do CPI, Fita de Duas Velocidades</span>',
    "news hero kicker")

card = '''                <!-- News 20/10/2026: Two-speed tape on CPI eve — dollar steadies vs euro, sterling pins 20-day high -->
                <article class="news-card">
                    <div class="news-card-top">
                        <span class="news-cat"><span class="lang-en">Market Flow</span><span class="lang-pt" style="display:none;">Fluxo &amp; Mercado</span></span>
                        <span class="impact-badge high"><span class="lang-en">High Impact</span><span class="lang-pt" style="display:none;">Impacto Alto</span></span>
                        <span class="news-date">20/10/2026</span>
                    </div>
                    <h2 class="news-title">
                        <span class="lang-en">Two-speed tape on CPI eve: the dollar steadies against the euro (two down closes) while sterling pins the 10/20-day highs — the GBP/USD shelf moves up to the 1.3360-1.3420 SMA cluster</span>
                        <span class="lang-pt" style="display:none;">Fita de duas velocidades na véspera do CPI: o dólar estabiliza contra o euro (dois fechamentos de queda) enquanto a libra crava as máximas de 10/20 pregões — a prateleira do GBP/USD sobe para o cluster SMA 1.3360-1.3420</span>
                    </h2>
                    <p class="news-summary">
                        <span class="lang-en">The Fed blackout (FOMC Oct 27-28) emptied the US tape and EUR/USD gave back 38 pips of Friday's bounce without touching either extreme (1.1215; the 9-month low 1.1177 stands and the 1.1260-1.1300 shelf is intact — the Oct-18 fade is re-armed unchanged). On the other side, GBP/USD closed 1.3347 (+0.12%) AT the 10- and 20-day highs — a third daily gain — and overran the 1.3290-1.3330 band: the Oct-18 ticket was revoked unfired and the desk re-prices the fade one shelf higher, at 1.3360-1.3420 (the broken Sep-22 close + SMA50/61.8% Fib), stop 1.3460, target 1.3250, 1:2.00 — the Oct-21 close is already post-CPI (07:00 London) and arms. GBP/JPY followed with a second straight close at the 10/20-day highs (211.05), the SMA50 211.55 the first shelf — which still fails the 1:2 path gate.</span>
                        <span class="lang-pt" style="display:none;">O blackout do Fed (FOMC 27-28/10) esvaziou o tape americano e o EUR/USD devolveu 38 pips do repique de sexta sem tocar extremo nenhum (1.1215; a mínima de 9 meses 1.1177 segue invicta e a prateleira 1.1260-1.1300 intacta — o fade de 18/10 é rearmado sem mudanças). Do outro lado, o GBP/USD fechou 1.3347 (+0,12%) NAS máximas de 10 e 20 pregões — terceiro ganho diário seguido — e atropelou a faixa 1.3290-1.3330: o ticket de 18/10 foi revogado sem disparar e a mesa reprecifica o fade uma casa acima, em 1.3360-1.3420 (fechamento quebrado de 22/09 + SMA50/Fib 61,8%), stop 1.3460, alvo 1.3250, 1:2,00 — o fechamento de 21/10 já é pós-CPI (07:00 de Londres) e arma. O GBP/JPY acompanhou com o segundo fechamento seguido nas máximas de 10/20 pregões (211,05), com a SMA50 211,55 como primeira prateleira — que segue reprovando no caminho do 1:2.</span>
                    </p>
                    <div class="news-take">
                        <span class="take-tag"><span class="lang-en">Desk take</span><span class="lang-pt" style="display:none;">Leitura da mesa</span></span>
                        <span class="lang-en">Wednesday's CPI decides sterling's chapter: either it overruns the SMA cluster on a close (breaking the bear map) or it delivers the fade on the new shelf — the book doesn't chase a pinned high.</span>
                        <span class="lang-pt" style="display:none;">O CPI de quarta decide o capítulo da libra: ou atropela o cluster SMA com fechamento (quebrando o mapa de baixa), ou entrega o fade na prateleira nova — o livro não persegue máxima cravada.</span>
                    </div>
                    <div class="news-pairs">
                        <span class="np-label"><span class="lang-en">Watch</span><span class="lang-pt" style="display:none;">Acompanhar</span></span>
                        <a href="eur-usd.html" class="pair-link-chip">EUR/USD</a><a href="gbp-usd.html" class="pair-link-chip">GBP/USD</a><a href="gbp-jpy.html" class="pair-link-chip">GBP/JPY</a>
                    </div>
                </article>

'''
first_card = '                <!-- News 16/10/2026: Friday sweeps the dollar: the Fed chair refuses to “prejudge -->'
assert news.count(first_card) == 1, "first news card anchor not found"
news = sub1(news, first_card, card + first_card, "news card prepend")
open(NEWS, "w", encoding="utf-8", newline="").write(news)
print("OK news.html: wire item prepended, hero dateline/kicker refreshed")

# =====================================================================
# 3. track-record.json — resolve/replace tickets
# =====================================================================
led = json.load(open(LEDGER, encoding="utf-8"))
assert led["meta"]["lastUpdated"] == "18/10/2026"
led["meta"]["lastUpdated"] = "20/10/2026"

watching = led["watching"]
assert {t["pair"] for t in watching} == {"EUR/USD", "GBP/USD"}, "unexpected watching set"

eur_old = next(t for t in watching if t["pair"] == "EUR/USD")
gbp_old = next(t for t in watching if t["pair"] == "GBP/USD")

# neither 19-20/10 close triggered: EUR never entered 1.1260-1.1300 (1.1225/1.1215);
# GBP never entered 1.3290-1.3330 (1.33305 closed above the top; 1.3347 overran it) —
# and the 20/10 close was pre-designated not to arm (UK CPI inside 24h).
eur_old["note"] = ("revoked in the 20/10 edition and re-armed unchanged on the same shelf: "
                   "no 19-20/10 close entered 1.1260-1.1300 (Oct 20 closed 1.1215, 45 pips below it); "
                   "validity re-stamped through the 30/10 close with the 28/10 close (FOMC) still not arming")
eur_old["outcome"] = "revoked"
eur_old["exitDate"] = "20/10/2026"
eur_old["entryDate"] = None
eur_old["realizedR"] = None

gbp_old["note"] = ("revoked in the 20/10 edition: the Oct-20 close 1.3347 overran the band top (first 10/20-day "
                   "high close, third daily gain into the Oct-21 UK CPI) — re-armed one shelf higher at "
                   "1.3360-1.3420 (stop 1.3460, target 1.3250)")
gbp_old["outcome"] = "revoked"
gbp_old["exitDate"] = "20/10/2026"
gbp_old["entryDate"] = None
gbp_old["realizedR"] = None

led["watching"] = [
    {
        "pair": "EUR/USD",
        "reportDate": "20/10/2026",
        "direction": "short",
        "setup": "pullback",
        "entry": 1.128,
        "stop": 1.136,
        "target": 1.112,
        "plannedR": 2.0,
        "triggerRule": "daily close inside 1.1260-1.1300 (the failed Oct-6 close 1.1269 + the 1.1300 round) followed by a close below the previous close and the 1.1280 midpoint (entry reference 1.1280); only closes after the 20/10 report count and the 28/10 close (FOMC) doesn't arm; valid through the 30/10 close",
        "note": "re-armed unchanged from the 18/10 edition: the Oct 19-20 closes (1.1225/1.1215) faded away from the shelf without entering it — stop 1.1360 (80 pips over the 29-30/09 double close 1.1355 and the 78.6% Fib 1.1348, >= the 59-pip 1.5-sigma20 floor), target 1.1120 under the 9-month low crossing only the 1.1150 round"
    },
    {
        "pair": "GBP/USD",
        "reportDate": "20/10/2026",
        "direction": "short",
        "setup": "pullback",
        "entry": 1.339,
        "stop": 1.346,
        "target": 1.325,
        "plannedR": 2.0,
        "triggerRule": "daily close inside 1.3360-1.3420 (the broken Sep-22 close 1.3363 + the SMA50 1.3416 / 61.8% Fib 1.3411 / 1.3400 round cluster) followed by a close below the previous close and the 1.3390 midpoint (entry reference 1.3390); only closes after the 20/10 report count — the 21/10 close is already post-CPI (07:00 London) and arms, the 28/10 close (FOMC) doesn't; valid through the 30/10 close",
        "note": "re-priced one shelf up after the Oct-20 close 1.3347 overran the 1.3290-1.3330 band: stop 1.3460 (70 pips over the SMA200 1.3434 and the 1.3450 round, >= the 65-pip 1.5-sigma20 floor), target 1.3250 above the 10-day low 1.3205 crossing only the 1.3350/1.3300 rounds"
    }
]
led["closed"].append(eur_old)
led["closed"].append(gbp_old)

json.dump(led, open(LEDGER, "w", encoding="utf-8", newline=""), ensure_ascii=False, indent=2)
open(LEDGER, "a", encoding="utf-8", newline="").write("\n")
print("OK track-record.json: 2 tickets replaced (revoked unfired), 2 new watching, lastUpdated 20/10")

# =====================================================================
# 4. sitemap — refresh lastmod of touched URLs
# =====================================================================
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
    pat = "<loc>%s</loc>\n        <lastmod>2026-10-18</lastmod>" % loc
    if loc == "https://newsforextrading.com/track-record.html":
        pass  # may carry a different current lastmod; handled below generically
    if pat in sm:
        sm = sm.replace(pat, "<loc>%s</loc>\n        <lastmod>2026-10-20</lastmod>" % loc)
    else:
        # generic fallback: locate the loc block and swap whatever lastmod it carries
        m = re.search(r"(<loc>%s</loc>\s*<lastmod>)[\d-]+(</lastmod>)" % re.escape(loc), sm)
        assert m, "sitemap: entry not found for %s" % loc
        sm = sm[:m.start()] + m.group(1) + "2026-10-20" + m.group(2) + sm[m.end():]
open(SITEMAP, "w", encoding="utf-8", newline="").write(sm)
print("OK sitemap.xml: lastmod refreshed to 2026-10-20")

print("\nBuild complete. Now run build_static_pages.py + build_track_record_page.py + verify_all.py.")
