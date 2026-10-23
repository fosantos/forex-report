#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""22/10/2026 edition — the yen sweep & the fired fade.

Basis: ECB/Frankfurter daily reference rates, 569 sessions (01/08/2024-22/10/2026),
last close Thursday 22/10/2026. MT5 terminal still returns no FX data.

Headlines of the session:
  - GBP/USD: UK Sep CPI 3.5% y/y (Oct 21, exp 3.4%, prev 3.1%); Oct-21 close 1.3402
    entered the 1.3360-1.3420 shelf, Oct-22 close 1.3376 confirmed under the 1.3390
    midpoint -> the Oct-20 ticket FIRED: short from 1.3376, stop 1.3460, target 1.3250.
  - EUR/JPY: first close under the 9-month low 176.85 (175.97); second confirming
    close is the rule's trigger but the 1:2 path crosses the Oct-2025 shelf
    (175.70-175.92) + rounds -> no ticket into the BoJ.
  - USD/JPY: 10-day low 157.98 broke on the close (157.05), stopped 5 pips over the
    157.00 round; ladder still blocks the 1:2 -> WAIT into the cluster.
  - WTI ~$99 (+2% d/d, +7.7% m/m) feeds the BoJ hike consensus (1.25%, Oct 29-30).
"""
import json, re, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

INDEX = r"C:\Projetos\forex-report\docs\index.html"
NEWS = r"C:\Projetos\forex-report\docs\news.html"
LEDGER = r"C:\Projetos\forex-report\docs\track-record.json"
SITEMAP = r"C:\Projetos\forex-report\docs\sitemap.xml"

STAMP = "22/10/2026 21:57 UTC"
OLD_STAMP = "20/10/2026 20:46 UTC"

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
        "quote": "1.1205",
        "bias": "BAIXA",
        "biasType": "bear",
        "pt": {
            "fundamental": "O EUR/USD fechou em 1,1205 na sessão de quinta 22/10/2026 (taxa de referência BCE/Frankfurter; o terminal MT5 logado segue sem retornar dados de FX), caindo -0,26% — terceira sessão de desgaste dentro do blackout do Fed (FOMC em 27-28/10): o repique de quarta (1,1234) morreu 26 pips abaixo do piso da prateleira e a quinta devolveu tudo sem ameaçar os extremos — a mínima de 9 meses 1.1177 no chão e a prateleira 1.1260-1.1300 a 55 pips. O CPI de setembro (14/10) quente (3,7% a/a, gasolina +34%, núcleo 2,6%) ganhou combustível novo com o WTI a ~US$ 99 (+2% no dia); o shutdown parcial de 1/10 (DHS, segundo mais longo da história) segue com acordo relatado para terminar. Alinhamento de baixa pleno (fechamento sob a SMA200 1,1576, SMA50 1,1447 abaixo dela) — o fade da prateleira 1.1260-1.1300 é rearmado pela terceira vez seguida, sem mudanças. FOMC em 27-28/10. Indicadores (SMA 50/200, σ20, Donchian e Fibonacci) calculados da série diária BCE/Frankfurter (569 pregões, 01/08/2024 a 22/10/2026).",
            "trend": "Fechamento sob a SMA200 (1,1576) com a SMA50 (1,1447) abaixo dela — alinhamento de baixa pleno. A mínima de 9 meses e de 20 pregões (1.1177, 07/10) segue invicta (os fechamentos de 21-22/10 ficaram 29/28 pips acima); o teto imediato é a máxima de 10 pregões (1.1253, 16/10), com a prateleira 1.1260-1.1300 logo acima.",
            "support": "1.1177 (mínima de 9 meses e de 20 pregões, 07/10), com o redondo 1.1150 como único obstáculo até o alvo 1.1120.",
            "resistance": "1.1253 (máxima de 10 pregões, 16/10) e a prateleira 1.1260-1.1300, coroados pelo duplo fechamento 1.1355 (29-30/09).",
            "priceAction": "Fade do repique na prateleira (terceiro rearme): o gatilho é um fechamento diário dentro de 1.1260-1.1300 seguido de um fechamento abaixo do fechamento anterior e do meio da faixa 1.1280 (entrada de referência 1.1280). Stop 1.1360 (80 pips, sobre o duplo fechamento 1.1355 e a Fib 78,6% 1.1348; ≥ piso 1,5σ20 de 58 pips). Alvo 1.1120 (160 pips), sob a mínima de 9 meses e acima do redondo 1.1100, cruzando apenas o redondo 1.1150. Só contam fechamentos depois desta edição; os fechamentos de 27-28/10 (janela do FOMC) não armam.",
            "recommendation": "VENDA (SHORT) NA RETRAÇÃO",
            "trigger": "Fechamento diário dentro de 1.1260-1.1300 e um fechamento seguinte abaixo do anterior e do meio 1.1280 — entrada de referência 1.1280. Os fechamentos de 27-28/10 (janela do FOMC) não armam. Válido até o fechamento de 30/10.",
            "stop": "1.1360 (80 pips, sobre o duplo fechamento de 29-30/09 em 1.1355 e a Fib 78,6% 1.1348; ≥ piso 1,5σ20 de 58 pips) · risco sugerido ≤ 1% por operação.",
            "target": "1.1120 (160 pips), sob a mínima de 9 meses 1.1177 e acima do redondo 1.1100 — cruzando apenas o redondo 1.1150.",
            "rr": "1:2.00",
            "rrValue": 50,
            "justification": "Cinco sessões sem tocar extremo nenhum: a mínima não se persegue por cima e o repique nunca pagou a prateleira — o fade em 1.1260-1.1300 segue sendo o único ticket com localização (stop estrutural sobre o duplo 1.1355, 1:2,00 até 1.1120 cruzando só o redondo 1.1150). O diferencial Fed-BCE (3,75-4,00% contra 2,50% parado) e o WTI a ~US$ 99 alimentando o CPI seguem como pano de fundo; o FOMC de 27-28/10 é o árbitro — e filtra os fechamentos da própria janela."
        },
        "en": {
            "fundamental": "EUR/USD closed at 1.1205 in the Thursday 22/10/2026 session (ECB/Frankfurter reference rate; the logged-in MT5 terminal still returns no FX data), down -0.26% — a third session of grind inside the Fed blackout (FOMC on Oct 27-28): Wednesday's bounce (1.1234) died 26 pips under the shelf floor and Thursday gave it all back without threatening either extreme — the 9-month low 1.1177 on the floor and the 1.1260-1.1300 shelf 55 pips away. September's hot CPI (Oct 14: 3.7% y/y, gasoline +34%, core 2.6%) got fresh fuel from ~$99 WTI (+2% on the day); the partial shutdown (since Oct 1, DHS, second-longest in history) still has a reported deal to end it. Full bear alignment (close under the SMA200 1.1576, 50-day 1.1447 below it) — the 1.1260-1.1300 shelf fade is re-armed a third straight time, unchanged. FOMC on Oct 27-28. Indicators (SMA 50/200, sigma20, Donchian and Fibonacci) computed from the ECB/Frankfurter daily series (569 sessions, 01/08/2024 to 22/10/2026).",
            "trend": "Close under the SMA200 (1.1576) with the 50-day (1.1447) below it — full bear alignment. The 9-month and 20-day low (1.1177, Oct 7) still stands (the Oct 21-22 closes finished 29/28 pips above it); the immediate ceiling is the 10-day high (1.1253, Oct 16), with the 1.1260-1.1300 shelf right above.",
            "support": "1.1177 (the 9-month and 20-day low, Oct 7), with the 1.1150 round as the only obstacle down to the 1.1120 target.",
            "resistance": "1.1253 (the 10-day high, Oct 16) and the 1.1260-1.1300 shelf, crowned by the double close at 1.1355 (Sep 29-30).",
            "priceAction": "Fade the rally on the shelf (third re-arm): the trigger is a daily close inside 1.1260-1.1300 followed by a close below the previous close and the 1.1280 midpoint (entry reference 1.1280). Stop 1.1360 (80 pips, over the 1.1355 double close and the 78.6% Fib 1.1348; >= the 58-pip 1.5-sigma20 floor). Target 1.1120 (160 pips), under the 9-month low and above the 1.1100 round, crossing only the 1.1150 round. Only closes after this edition count; the Oct 27-28 closes (FOMC window) don't arm.",
            "recommendation": "SELL (SHORT) ON PULLBACK",
            "trigger": "A daily close inside 1.1260-1.1300 and a following close below the previous close and the 1.1280 midpoint — entry reference 1.1280. The Oct 27-28 closes (FOMC window) don't arm. Valid through the Oct-30 close.",
            "stop": "1.1360 (80 pips, over the Sep 29-30 double close at 1.1355 and the 78.6% Fib 1.1348; >= the 58-pip 1.5-sigma20 floor) · suggested risk ≤ 1% per trade.",
            "target": "1.1120 (160 pips), under the 9-month low 1.1177 and above the 1.1100 round — crossing only the 1.1150 round.",
            "rr": "1:2.00",
            "rrValue": 50,
            "justification": "Five sessions without touching either extreme: the low is not chased from above and the rally never paid the shelf — the fade at 1.1260-1.1300 remains the only ticket with location (structural stop over the 1.1355 double close, 1:2.00 to 1.1120 crossing only the 1.1150 round). The Fed-ECB differential (3.75-4.00% against a frozen 2.50%) and ~$99 WTI feeding the CPI stay the backdrop; the Oct 27-28 FOMC referees — and filters the closes of its own window."
        }
    },
    "USD/JPY": {
        "quote": "157.05",
        "bias": "BAIXA",
        "biasType": "bear",
        "pt": {
            "fundamental": "O USD/JPY fechou em 157,05 na sessão de quinta 22/10/2026 (taxa de referência BCE/Frankfurter), caindo -0,53% (-83 pips) — a maior queda diária da janela: o iene varreu o tabuleiro com o WTI a ~US$ 99 (+2% no dia, +7,7% no mês) alimentando o consenso de alta do BoJ (29-30/10, para 1,25%, a partir de ~1% desde julho). O fechamento rompeu a mínima de 10 pregões (157,98, 15/10) — o primeiro fechamento de rompimento do canal — mas parou 5 pips acima do redondo 157,00, o último degrau da escada. O blackout do Fed vale (FOMC 27-28/10); a janela formal de 30 dias dos rate checks do MoF de meados de setembro permanece fechada — piso 1,5σ20 (76 pips), com o risco MoF a 158 como narrativa. Alinhamento de baixa pleno (fechamento sob a SMA200 158,55 e a SMA50 157,61, com a SMA50 abaixo dela — cinco fechamentos sob a média). Indicadores calculados da série diária BCE/Frankfurter (569 pregões, 01/08/2024 a 22/10/2026).",
            "trend": "Fechamento sob a SMA200 (158,55) com a SMA50 (157,61) abaixo dela — alinhamento de baixa pleno, cinco fechamentos de idade. O fechamento de 22/10 é o primeiro sob a mínima de 10 pregões (157,98); a mínima de 20 pregões (156,88) e a Fib 61,8% (156,94) formam o degrau seguinte, com o fechamento de 17/09 (155,69) como destino da escada.",
            "support": "157.00 (o redondo, 5 pips abaixo), com a mínima de 20 pregões 156,88 e a Fib 61,8% 156,94 na mesma altura, e o vácuo até o fechamento de 17/09 (155,69).",
            "resistance": "157.61 (a SMA50) e a mínima quebrada de 10 pregões (157,98), com a SMA200 (158,55) e as máximas de 10/20 pregões (158,60) acima.",
            "priceAction": "O rompimento chegou (fechamento 157,05 sob 157,98) e a geometria segue reprovando: a venda no rompimento com stop ≥ 76 pips (sobre 158,00) cai em alvo ~155,40 — atravessando a mínima de 20 pregões (156,88) e o redondo 156,00; o repique à SMA50/zona quebrada (157,60-158,00) também não paga 1:2 contra a mesma escada. Um fechamento sob 157,00 limpa a escada até 155,69 — mas mesmo dali o 1:2 cruza os redondos 156,00/155,50. Sem ticket: o cluster FOMC (27-28/10) + BoJ (29-30/10) reprecifica o corredor.",
            "recommendation": "AGUARDAR OUTRO GATILHO",
            "trigger": "157.00 é o último degrau: um fechamento abaixo limpa a escada até 155,69 — mas o alvo 1:2 dali segue atravessando os redondos 156,00/155,50. Reavaliar após o cluster FOMC (27-28/10) + BoJ (29-30/10).",
            "stop": "N/A (sem operação).",
            "target": "N/A (sem operação).",
            "rr": "N/A",
            "rrValue": 0,
            "justification": "O iene fez o serviço sujo — rompeu o canal por fechamento — e parou no redondo: persegui-lo entre degraus com piso de 76 pips paga menos de 1:2 nos dois lados. O consenso de alta do BoJ (1,25%) já está no preço do movimento; pagar o cluster FOMC-BoJ comprado em rompimento é risco de evento, não setup. A mesa espera os dois bancos."
        },
        "en": {
            "fundamental": "USD/JPY closed at 157.05 in the Thursday 22/10/2026 session (ECB/Frankfurter reference rate), down -0.53% (-83 pips) — the largest daily fall in the window: the yen swept the board as ~$99 WTI (+2% on the day, +7.7% on the month) fed the BoJ hike consensus (Oct 29-30, to 1.25%, from ~1% since July). The close broke the 10-day low (157.98, Oct 15) — the channel's first breakdown close — but stopped 5 pips above the 157.00 round, the ladder's last rung. The Fed blackout is on (FOMC Oct 27-28); the MoF's mid-September rate-check 30-day window remains closed — floor at 1.5-sigma20 (76 pips), with MoF risk at 158 as narrative. Full bear alignment (close under the SMA200 158.55 and the 50-day 157.61, the 50-day below it — five closes under the average). Indicators computed from the ECB/Frankfurter daily series (569 sessions, 01/08/2024 to 22/10/2026).",
            "trend": "Close under the SMA200 (158.55) with the 50-day (157.61) below it — full bear alignment, five closes old. The Oct-22 close is the first under the 10-day low (157.98); the 20-day low (156.88) and the 61.8% Fib (156.94) form the next rung, with the Sep-17 close (155.69) the ladder's destination.",
            "support": "157.00 (the round, 5 pips below), with the 20-day low 156.88 and the 61.8% Fib 156.94 at the same height, and the vacuum down to the Sep-17 close (155.69).",
            "resistance": "157.61 (the SMA50) and the broken 10-day low (157.98), with the SMA200 (158.55) and the 10/20-day highs (158.60) above.",
            "priceAction": "The break arrived (the 157.05 close under 157.98) and the geometry still rejects it: a breakdown short with a >=76-pip stop (over 158.00) targets ~155.40 — crossing the 20-day low (156.88) and the 156.00 round; a pullback to the SMA50/broken zone (157.60-158.00) pays no 1:2 against the same ladder either. A close under 157.00 clears the ladder toward 155.69 — but even from there the 1:2 crosses the 156.00/155.50 rounds. No ticket: the FOMC (Oct 27-28) + BoJ (Oct 29-30) cluster reprices the corridor.",
            "recommendation": "WAIT FOR ANOTHER TRIGGER",
            "trigger": "157.00 is the last rung: a close below clears the ladder toward 155.69 — but the 1:2 target from there still crosses the 156.00/155.50 rounds. Reassess after the FOMC (Oct 27-28) + BoJ (Oct 29-30) cluster.",
            "stop": "N/A (no trade).",
            "target": "N/A (no trade).",
            "rr": "N/A",
            "rrValue": 0,
            "justification": "The yen did the dirty work — broke the channel on a close — and stopped at the round: chasing it between rungs with a 76-pip floor pays under 1:2 on both sides. The BoJ hike consensus (1.25%) is already in the move's price; paying the FOMC-BoJ cluster long-on-breakdown is event risk, not a setup. The desk waits for both banks."
        }
    },
    "AUD/USD": {
        "quote": "0.7012",
        "bias": "NEUTRO",
        "biasType": "neutral",
        "pt": {
            "fundamental": "O AUD/USD fechou em 0,7012 na sessão de quinta 22/10/2026 (taxa de referência BCE/Frankfurter), caindo -0,31% — o falso rompimento da véspera: o fechamento de 21/10 (0,7034) foi o primeiro acima do teto antigo 0.7010 (máxima de 10/20 pregões) mas parou 25 pips sob a SMA200 (0,7044), e a quinta devolveu a borda. A leitura segue NEUTRA: fechamento sob as duas médias (SMA200 0,7044, SMA50 0,7079) com a SMA50 ainda acima da SMA200. O motor commodity acelera (WTI a ~US$ 99, +2% no dia e +7,7% no mês — a mesma energia por trás do CPI australiano a 3,5%) e o CPI do Q3 (≈28/10) é o árbitro local antes da leitura da RBA para novembro. Sem rompimento confirmado não há ticket. Indicadores calculados da série diária BCE/Frankfurter (569 pregões, 01/08/2024 a 22/10/2026).",
            "trend": "Misto por construção: fechamento sob as duas médias com a SMA50 ainda acima da SMA200. O canal reprecifica para 0.6911-0.7034 (novos extremos de 10/20 pregões); a recaptura da SMA200 0,7044 com segundo fechamento resolve para cima, a perda de 0.6911 para baixo.",
            "support": "0.6911 (mínima de 10/20 pregões, 15/10), com o redondo 0,6900 abaixo.",
            "resistance": "0.7034 (a máxima de 10/20 pregões, 21/10), com a SMA200 (0,7044) e a Fib 38,2% (0,7057) formando o teto real.",
            "priceAction": "Sem gatilho: o fechamento de 21/10 acima do teto antigo morreu sob a SMA200 sem o segundo fechamento. Um fechamento sobre 0.7034 e o segundo contra a SMA200 0,7044 resolveria o misto para cima; um fechamento sob 0.6911 abre 0.6900 e o vácuo até o piso de janeiro (0.6733). O CPI do Q3 (≈28/10) escolhe o lado — e a RBA (novembro) lê em seguida.",
            "recommendation": "AGUARDAR OUTRO GATILHO",
            "trigger": "0.7034 é o teto a romper primeiro (com a SMA200 0,7044 logo acima); 0.6911 o piso. Sem rompimento confirmado não há ticket — reavaliar após o CPI australiano do Q3 (≈28/10).",
            "stop": "N/A (sem operação).",
            "target": "N/A (sem operação).",
            "rr": "N/A",
            "rrValue": 0,
            "justification": "O falso rompimento é o argumento do WAIT: a primeira fuga do canal morreu na média que manda. Perseguir direção dentro de 0.6911-0.7034 segue sendo pagar caro por uma escolha de lado que o preço não fez — o CPI do Q3 (≈28/10), no meio do cluster FOMC-BoJ, é o que pode destravar."
        },
        "en": {
            "fundamental": "AUD/USD closed at 0.7012 in the Thursday 22/10/2026 session (ECB/Frankfurter reference rate), down -0.31% — the overnight fakeout: the Oct-21 close (0.7034) was the first over the old 0.7010 ceiling (a 10/20-day high) but stopped 25 pips under the SMA200 (0.7044), and Thursday handed the edge back. The read stays NEUTRAL: close under both averages (SMA200 0.7044, 50-day 0.7079) with the 50-day still above the SMA200. The commodity engine accelerates (WTI ~$99, +2% on the day and +7.7% on the month — the same energy behind Australia's 3.5% CPI) and the Q3 CPI (≈Oct 28) is the local arbiter before the RBA's November read. Without a confirmed breakout there is no ticket. Indicators computed from the ECB/Frankfurter daily series (569 sessions, 01/08/2024 to 22/10/2026).",
            "trend": "Mixed by construction: close under both averages with the 50-day still above the SMA200. The channel re-prices to 0.6911-0.7034 (fresh 10/20-day extremes); reclaiming the SMA200 0.7044 with a second close resolves it up, losing 0.6911 resolves it down.",
            "support": "0.6911 (the 10/20-day low, Oct 15), with the 0.6900 round below.",
            "resistance": "0.7034 (the 10/20-day high, Oct 21), with the SMA200 (0.7044) and the 38.2% Fib (0.7057) forming the real ceiling.",
            "priceAction": "No trigger: the Oct-21 close over the old ceiling died under the SMA200 without the second close. A close over 0.7034 and a second against the SMA200 0.7044 would resolve the mix upward; a close under 0.6911 opens 0.6900 and the vacuum down to the January floor (0.6733). The Q3 CPI (≈Oct 28) picks the side — with the RBA (November) reading next.",
            "recommendation": "WAIT FOR ANOTHER TRIGGER",
            "trigger": "0.7034 is the ceiling to break first (with the SMA200 0.7044 right above); 0.6911 the floor. No confirmed break, no ticket — reassess after the Australian Q3 CPI (≈Oct 28).",
            "stop": "N/A (no trade).",
            "target": "N/A (no trade).",
            "rr": "N/A",
            "rrValue": 0,
            "justification": "The fakeout is the WAIT argument: the channel's first escape died on the average that commands. Chasing direction inside 0.6911-0.7034 remains overpaying for a side-selection price hasn't made — the Q3 CPI (≈Oct 28), inside the FOMC-BoJ cluster, is what can unlock it."
        }
    },
    "GBP/USD": {
        "quote": "1.3376",
        "bias": "BAIXA",
        "biasType": "bear",
        "pt": {
            "fundamental": "O GBP/USD disparou o fade na sessão de quinta 22/10/2026 (taxa de referência BCE/Frankfurter): o CPI de setembro veio em 3,5% a/a (21/10, 07:00 de Londres) — acima dos 3,4% esperados e dos 3,1% de agosto, o maior desde outubro de 2025, com transporte a +6,6% e empréstimos públicos subindo rumo ao primeiro orçamento do chanceler — e comprou a libra por exatamente um pregão: o fechamento de 21/10 (1,3402, +0,41%) cravou a máxima de 10/20 pregões DENTRO da prateleira 1.3360-1.3420, e o fechamento de 22/10 (1,3376, -0,19%) confirmou abaixo do anterior e do meio 1.3390 — o gatilho de dois passos do ticket de 20/10. O livro está vendido de 1,3376 (referência 1,3390), stop 1.3460, alvo 1.3250, 1:2,00 planejado — resolução por fechamento, expiração no 10º pregão (fechamento de 05/11, dia do BoE). O alinhamento de baixa segue pleno (fechamento sob a SMA200 1,3434, SMA50 1,3412 abaixo dela); o BoE decide 05/11 com o mercado precificando altas até dezembro. Indicadores calculados da série diária BCE/Frankfurter (569 pregões, 01/08/2024 a 22/10/2026).",
            "trend": "Fechamento sob a SMA200 (1,3434) com a SMA50 (1,3412) abaixo dela — alinhamento de baixa pleno. O pop do CPI morreu dentro do cluster SMA (1.3411-1.3434: Fib 61,8% + SMA50 + SMA200) exatamente onde o mapa vendia; o fechamento de 22/10 de volta sob o meio da prateleira confirma a recusa.",
            "support": "1.3220 (mínima de 10 pregões, 07/10; a de 20 fica em 1.3201), com a mínima de 9 meses em 1.3160 embaixo.",
            "resistance": "1.3420 (o teto da prateleira: Fib 61,8% 1,3411 + SMA50 1,3412), com o piso 1.3360 atrás e a SMA200 (1,3434), o redondo 1.3450 e o stop 1.3460 acima; a Fib 50% (1,3489) no alto.",
            "priceAction": "Posição aberta (o mapa agora é gestão): short de 1,3376 (disparado no fechamento de 22/10) com stop 1.3460 — um fechamento em/acima encerra a posição a -1R — e alvo 1.3250 — um fechamento em/abaixo banca o ticket — cruzando apenas os redondos 1.3350/1.3300, acima da mínima de 10 pregões. Expiração no 10º pregão (fechamento de 05/11, o dia do BoE); o FOMC de 27-28/10 cavalga dentro da janela da posição como o principal risco de marcação — o filtro de eventos trava novas entradas, não gerencia posições abertas.",
            "recommendation": "VENDA (SHORT) NA RETRAÇÃO",
            "trigger": "DISPARADO no fechamento de 22/10 (21/10 fechou 1.3402 dentro da prateleira; 22/10 confirmou em 1.3376 sob o meio 1.3390). Gestão por fechamento: stop 1.3460 / alvo 1.3250 / expiração 05/11.",
            "stop": "1.3460 (sobre a SMA200 1,3434 e o redondo 1.3450; ≥ piso 1,5σ20 de 57 pips) · risco sugerido ≤ 1% por operação.",
            "target": "1.3250 (140 pips da referência 1.3390; 126 da entrada disparada 1.3376), acima da mínima de 10 pregões 1.3220 — cruzando apenas os redondos 1.3350 e 1.3300.",
            "rr": "1:2.00",
            "rrValue": 50,
            "justification": "O dado quente fez exatamente o que o mapa pedia: comprou a libra até a prateleira e morreu no cluster SMA — o gatilho mecânico disparou no fechamento e agora o trabalho é do ledger (stop/alvo por fechamento, sem discutir com a fita). O BoE de 05/11 (com altas precificadas até dezembro) é o árbitro fundamental e cai justamente no pregão de expiração; o FOMC de 27-28/10 é o risco de marcação dentro da janela. Não se adiciona ticket novo: a continuação abaixo cruzaria a mínima de 9 meses."
        },
        "en": {
            "fundamental": "GBP/USD fired the fade in the Thursday 22/10/2026 session (ECB/Frankfurter reference rate): September's CPI printed 3.5% y/y (Oct 21, 07:00 London) — above the 3.4% expected and August's 3.1%, the highest since October 2025, with transport at +6.6% and public borrowing climbing toward the Chancellor's first budget — and bought sterling for exactly one session: the Oct-21 close (1.3402, +0.41%) pinned the 10/20-day high INSIDE the 1.3360-1.3420 shelf, and the Oct-22 close (1.3376, -0.19%) confirmed below the previous close and the 1.3390 midpoint — the Oct-20 ticket's two-step trigger. The book is short from 1.3376 (reference 1.3390), stop 1.3460, target 1.3250, planned 1:2.00 — close-based resolution, expiry at the 10th session (the Nov-5 close, BoE day). Full bear alignment stands (close under the SMA200 1.3434, 50-day 1.3412 below it); the BoE decides Nov 5 with the market pricing hikes by December. Indicators computed from the ECB/Frankfurter daily series (569 sessions, 01/08/2024 to 22/10/2026).",
            "trend": "Close under the SMA200 (1.3434) with the 50-day (1.3412) below it — full bear alignment. The CPI pop died inside the SMA cluster (1.3411-1.3434: 61.8% Fib + SMA50 + SMA200) exactly where the map sold it; the Oct-22 close back under the shelf midpoint confirms the rejection.",
            "support": "1.3220 (the 10-day low, Oct 7; the 20-day sits at 1.3201), with the 9-month low at 1.3160 below.",
            "resistance": "1.3420 (the shelf top: the 61.8% Fib 1.3411 + SMA50 1.3412), with the shelf floor 1.3360 behind, crowned by the SMA200 (1.3434), the 1.3450 round and the 1.3460 stop; the 50% Fib (1.3489) above.",
            "priceAction": "Position open (the map is now management): short from 1.3376 (fired at the Oct-22 close) with stop 1.3460 — a close at/above ends it at -1R — and target 1.3250 — a close at/below banks the ticket — crossing only the 1.3350/1.3300 rounds, above the 10-day low. Expiry at the 10th session (the Nov-5 close, BoE day); the Oct 27-28 FOMC rides inside the position's window as the main mark-to-market risk — the event filter blocks new entries, it doesn't manage open positions.",
            "recommendation": "SELL (SHORT) ON PULLBACK",
            "trigger": "FIRED at the Oct-22 close (Oct 21 closed 1.3402 inside the shelf; Oct 22 confirmed at 1.3376 under the 1.3390 midpoint). Close-based management: stop 1.3460 / target 1.3250 / expiry Nov 5.",
            "stop": "1.3460 (over the SMA200 1.3434 and the 1.3450 round; >= the 57-pip 1.5-sigma20 floor) · suggested risk ≤ 1% per trade.",
            "target": "1.3250 (140 pips from the 1.3390 reference; 126 from the fired entry 1.3376), above the 10-day low 1.3220 — crossing only the 1.3350 and 1.3300 rounds.",
            "rr": "1:2.00",
            "rrValue": 50,
            "justification": "The hot print did exactly what the map asked: bought sterling up to the shelf and died on the SMA cluster — the mechanical trigger fired on the close and the work is now the ledger's (close-based stop/target, no arguing with the tape). The Nov-5 BoE (with hikes priced by December) is the fundamental arbiter and lands exactly on the expiry session; the Oct 27-28 FOMC is the mark-to-market risk inside the window. No new ticket is added: the continuation below would cross the 9-month low."
        }
    },
    "EUR/JPY": {
        "quote": "175.97",
        "bias": "BAIXA",
        "biasType": "bear",
        "pt": {
            "fundamental": "O EUR/JPY fechou em 175,97 na sessão de quinta 22/10/2026 (taxa de referência BCE/Frankfurter), caindo -0,78% (-139 pips) — a maior queda da janela: o iene varreu os cruzamentos com o WTI a ~US$ 99 (+2% no dia) alimentando o consenso de alta do BoJ (29-30/10, para 1,25%). O fechamento é o PRIMEIRO sob a mínima de 9 meses 176.85 (07/10) — também sob a mínima de 10 pregões (176,91, 13/10) — e, como extremo de 9 meses, exige o segundo fechamento confirmatório da regra. Abaixo, o próximo apoio real da própria série é a prateleira de out/2025 (fechamentos 175,70-175,92). O alinhamento segue de baixa pleno (fechamento sob a SMA200 183,52, SMA50 180,41 abaixo dela). A janela formal de 30 dias dos rate checks do MoF permanece fechada: piso 1,5σ20 (103 pips). Indicadores calculados da série diária BCE/Frankfurter (569 pregões, 01/08/2024 a 22/10/2026).",
            "trend": "Fechamento sob a SMA200 (183,52) com a SMA50 (180,41) abaixo dela — baixa plena. O fechamento de 22/10 cravou a nova mínima de 9 meses e de 10/20 pregões (175,97); a mínima entregue 176.85 e o redondo 177,00 são o primeiro teto, com a máxima de 10 pregões (177,82, 16/10) acima.",
            "support": "175.70-175.92 (a prateleira de out/2025 da própria série), com o redondo 175,00 abaixo — o fechamento de 22/10 (175,97) é a nova mínima de 9 meses.",
            "resistance": "176.85 (a mínima de 9 meses entregue) e o redondo 177,00, com a máxima de 10 pregões 177,82 (16/10) e a de 20 (179,70) acima.",
            "priceAction": "O segundo fechamento sob ~175,95 seria o gatilho mecânico — mas a entrada cairia EM CIMA da prateleira de out/2025 (175,70-175,92) e o piso de 103 pips empurra o stop para ~177,00, deixando o alvo 1:2 em ~173,80: atravessando a própria prateleira e os redondos 175,00/174,00 — caminho bloqueado. O repique até 176,85-177,82 também não paga. Sem ticket até o BoJ (29-30/10): o cluster reprecifica o andar de baixo.",
            "recommendation": "AGUARDAR OUTRO GATILHO",
            "trigger": "O segundo fechamento sob a mínima de 9 meses é o gatilho da regra — mas o alvo 1:2 atravessa a prateleira de out/2025 e dois redondos: caminho bloqueado. Reavaliar após o BoJ (29-30/10).",
            "stop": "N/A (sem operação).",
            "target": "N/A (sem operação).",
            "rr": "N/A",
            "rrValue": 0,
            "justification": "O rompimento que o livro esperava chegou — e não se persegue: comprar a quebra sentado sobre a prateleira de 2025, com stop de 103 pips e três degraus até o alvo, é pagar o evento BoJ (consenso de 1,25% já formado) no pior preço. A mesa deixa a extensão correr e reprecifica após o cluster: se o BoJ entregar, o andar de baixo volta com caminho mais limpo."
        },
        "en": {
            "fundamental": "EUR/JPY closed at 175.97 in the Thursday 22/10/2026 session (ECB/Frankfurter reference rate), down -0.78% (-139 pips) — the window's largest fall: the yen swept the crosses as ~$99 WTI (+2% on the day) fed the BoJ hike consensus (Oct 29-30, to 1.25%). The close is the FIRST under the 9-month low 176.85 (Oct 7) — also under the 10-day low (176.91, Oct 13) — and, as a 9-month extreme, it requires the rule's second confirming close. Below, the next real support of the series itself is the Oct-2025 shelf (closes 175.70-175.92). Full bear alignment stands (close under the SMA200 183.52, 50-day 180.41 below it). The MoF rate-check 30-day window remains closed: floor at 1.5-sigma20 (103 pips). Indicators computed from the ECB/Frankfurter daily series (569 sessions, 01/08/2024 to 22/10/2026).",
            "trend": "Close under the SMA200 (183.52) with the 50-day (180.41) below it — full bear. The Oct-22 close pinned the fresh 9-month and 10/20-day low (175.97); the handed-back 176.85 and the 177.00 round are the first ceiling, with the 10-day high (177.82, Oct 16) above.",
            "support": "175.70-175.92 (the Oct-2025 shelf of the series itself), with the 175.00 round below — the Oct-22 close (175.97) is the new 9-month low.",
            "resistance": "176.85 (the handed-back 9-month low) and the 177.00 round, with the 10-day high 177.82 (Oct 16) and the 20-day (179.70) above.",
            "priceAction": "A second close under ~175.95 would be the mechanical trigger — but the entry would land ON TOP of the Oct-2025 shelf (175.70-175.92) and the 103-pip floor pushes the stop to ~177.00, leaving the 1:2 target at ~173.80: crossing the shelf itself and the 175.00/174.00 rounds — path blocked. The bounce to 176.85-177.82 doesn't pay either. No ticket until the BoJ (Oct 29-30): the cluster reprices the floor below.",
            "recommendation": "WAIT FOR ANOTHER TRIGGER",
            "trigger": "The second close under the 9-month low is the rule's trigger — but the 1:2 target crosses the Oct-2025 shelf and two rounds: path blocked. Reassess after the BoJ (Oct 29-30).",
            "stop": "N/A (no trade).",
            "target": "N/A (no trade).",
            "rr": "N/A",
            "rrValue": 0,
            "justification": "The break the book waited for arrived — and it isn't chased: buying the breakdown sitting on the 2025 shelf, with a 103-pip stop and three rungs to target, is paying the BoJ event (consensus 1.25% already formed) at the worst price. The desk lets the extension run and re-prices after the cluster: if the BoJ delivers, the floor below comes back with a cleaner path."
        }
    },
    "GBP/JPY": {
        "quote": "210.07",
        "bias": "BAIXA",
        "biasType": "bear",
        "pt": {
            "fundamental": "O GBP/JPY fechou em 210,07 na sessão de quinta 22/10/2026 (taxa de referência BCE/Frankfurter), caindo -0,72% (-152 pips) — o CPI britânico de 3,5% a/a (acima do esperado) comprou a libra por um pregão (fechamento de 21/10 em 211,59, máxima de 10/20 pregões) e a quinta devolveu tudo com juros: a varredura do iene (WTI a ~US$ 99 alimentando o consenso de alta do BoJ para 1,25% em 29-30/10) atropelou a SMA50 (211,38) e estacionou o cruzamento 7 pips acima do redondo 210,00. O alinhamento formal segue de baixa (fechamento sob a SMA200 212,98 e a SMA50 211,38, com a SMA50 abaixo dela). Piso 1,5σ20 de 123 pips com a janela do MoF fechada. Indicadores calculados da série diária BCE/Frankfurter (569 pregões, 01/08/2024 a 22/10/2026).",
            "trend": "Fechamento sob a SMA200 (212,98) com a SMA50 (211,38) abaixo dela — baixa plena. Dois fechamentos nas máximas de 10/20 pregões (20-21/10) devolvidos numa sessão: a SMA50 voltou a ser teto, com a Fib 61,8% (211,84) e o redondo 212,00 no caminho e a SMA200 acima.",
            "support": "210.00 (o redondo, 7 pips abaixo), com a Fib 78,6% (209,85), a mínima de 10 pregões (209,21, 09/10) e a de 20 (208,07, 28/09) abaixo.",
            "resistance": "211.38 (a SMA50), com a Fib 61,8% (211,84) e o redondo 212,00 no caminho, e a SMA200 (212,98) acima.",
            "priceAction": "A prateleira da SMA50 segue sendo o único sell com estrutura: entrada ~211,40 com stop 212,65 (127 pips ≥ piso 123) só paga 1:2 em 208,85 — atravessando o redondo 210,00, a Fib 78,6% (209,85), a mínima de 10 pregões (209,21) e a de 20 (208,07): reprovado. O rompimento sob 209,21 cruza a mesma escada (208,07 + redondos). Sem ticket: o CPI respondeu (3,5%) e a resposta durou um pregão — o BoJ (29-30/10) reprecifica o cruzamento.",
            "recommendation": "AGUARDAR OUTRO GATILHO",
            "trigger": "211.38 (a SMA50) é a primeira prateleira de venda, mas segue reprovando no caminho do 1:2 (210,00 + Fib 78,6% + mínimas de 10/20 pregões). Reavaliar após o BoJ (29-30/10).",
            "stop": "N/A (sem operação).",
            "target": "N/A (sem operação).",
            "rr": "N/A",
            "rrValue": 0,
            "justification": "O dado quente britânico não sobreviveu a uma sessão contra o iene: qualquer venda aqui pega o cruzamento colado no redondo 210,00 com o piso de 123 pips e quatro degraus até o alvo — e a compra brigaria com as duas médias. O cluster FOMC-BoJ de 27-30/10 é o árbitro; a mesa espera."
        },
        "en": {
            "fundamental": "GBP/JPY closed at 210.07 in the Thursday 22/10/2026 session (ECB/Frankfurter reference rate), down -0.72% (-152 pips) — the UK's 3.5% y/y CPI (above expected) bought sterling for one session (the Oct-21 close at 211.59, a 10/20-day high) and Thursday returned it all with interest: the yen sweep (WTI ~$99 feeding the BoJ hike consensus to 1.25% on Oct 29-30) ran over the SMA50 (211.38) and parked the cross 7 pips above the 210.00 round. The formal alignment stays bearish (close under the SMA200 212.98 and the 50-day 211.38, the 50-day below it). 1.5-sigma20 floor of 123 pips with the MoF window closed. Indicators computed from the ECB/Frankfurter daily series (569 sessions, 01/08/2024 to 22/10/2026).",
            "trend": "Close under the SMA200 (212.98) with the 50-day (211.38) below it — full bear. Two closes at the 10/20-day highs (Oct 20-21) returned in one session: the SMA50 is the ceiling again, with the 61.8% Fib (211.84) and the 212.00 round in the way and the SMA200 above.",
            "support": "210.00 (the round, 7 pips below), with the 78.6% Fib (209.85), the 10-day low (209.21, Oct 9) and the 20-day (208.07, Sep 28) below.",
            "resistance": "211.38 (the SMA50), with the 61.8% Fib (211.84) and the 212.00 round in the way, and the SMA200 (212.98) above.",
            "priceAction": "The SMA50 shelf remains the only structured sell: an entry ~211.40 with a 212.65 stop (127 pips >= the 123 floor) only pays 1:2 at 208.85 — crossing the 210.00 round, the 78.6% Fib (209.85), the 10-day low (209.21) and the 20-day (208.07): rejected. The breakdown under 209.21 crosses the same ladder (208.07 + rounds). No ticket: the CPI answered (3.5%) and the answer lasted one session — the BoJ (Oct 29-30) reprices the cross.",
            "recommendation": "WAIT FOR ANOTHER TRIGGER",
            "trigger": "211.38 (the SMA50) is the first short shelf, but it still fails the 1:2 path (210.00 + the 78.6% Fib + the 10/20-day lows). Reassess after the BoJ (Oct 29-30).",
            "stop": "N/A (no trade).",
            "target": "N/A (no trade).",
            "rr": "N/A",
            "rrValue": 0,
            "justification": "The hot UK print didn't survive a session against the yen: any short here catches the cross glued to the 210.00 round with the 123-pip floor and four rungs to target — and a long would fight both averages. The Oct 27-30 FOMC-BoJ cluster is the arbiter; the desk waits."
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
    "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 567 daily sessions (01/08/2024–20/10/2026).",
    "Data basis: ECB/Frankfurter reference rates · SMA50/200, sigma20 & Donchian computed · 569 daily sessions (01/08/2024–22/10/2026).",
    "EN dataBasis")
html = sub1(html,
    "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, σ20 e Donchian calculados · 567 pregões (01/08/2024 a 20/10/2026).",
    "Base de dados: taxas de referência BCE/Frankfurter · SMA50/200, σ20 e Donchian calculados · 569 pregões (01/08/2024 a 22/10/2026).",
    "PT dataBasis")
html = sub1(html,
    'nextEvent: "UK CPI Oct 21 · FOMC Oct 27-28 · BoJ Oct 29-30"',
    'nextEvent: "FOMC Oct 27-28 · BoJ Oct 29-30 · BoE Nov 5"',
    "EN nextEvent")
html = sub1(html,
    'nextEvent: "CPI Reino Unido 21/10 · FOMC 27-28/10 · BoJ 29-30/10"',
    'nextEvent: "FOMC 27-28/10 · BoJ 29-30/10 · BoE 05/11"',
    "PT nextEvent")

# --- ticker (dailyChanges) ---
for pair, old, new in [
    ("EUR/USD", "-0.09%", "-0.26%"), ("USD/JPY", "-0.07%", "-0.53%"),
    ("AUD/USD", "-0.02%", "-0.31%"), ("GBP/USD", "+0.12%", "-0.19%"),
    ("EUR/JPY", "-0.16%", "-0.78%"), ("GBP/JPY", "+0.05%", "-0.72%"),
]:
    html = sub1(html, '"%s": "%s"' % (pair, old), '"%s": "%s"' % (pair, new), "ticker " + pair)

# --- macroDrivers block ---
new_drivers = '''        const macroDrivers = {
            "EUR/USD": {
                en: ["Blackout grind, no extreme touched", "Shelf fade 1.126-1.130 re-armed", "FOMC 27-28/10 referees"],
                pt: ["Desgaste no blackout, sem extremo", "Fade 1,126-1,130 rearmado", "FOMC 27-28/10 arbitra"]
            },
            "USD/JPY": {
                en: ["10-day low breaks, 157.00 holds", "Ladder still blocks the R/R", "FOMC 27-28 · BoJ 29-30/10"],
                pt: ["Rompida mín. 10 preg., 157,00 segura", "Escada segue travando o R/R", "FOMC 27-28 · BoJ 29-30/10"]
            },
            "AUD/USD": {
                en: ["Fake break dies under SMA200", "Neutral mix stands", "Q3 CPI ≈28/10 · WTI ~$99"],
                pt: ["Falso rompimento morre sob a SMA200", "Misto segue de pé", "CPI Q3 ≈28/10 · WTI ~US$ 99"]
            },
            "GBP/USD": {
                en: ["UK CPI 3.5% — shelf fade FIRED", "Short from 1.3376 · stop 1.3460", "Target 1.3250 · BoE Nov 5"],
                pt: ["CPI Reino Unido 3,5% — fade DISPAROU", "Short de 1,3376 · stop 1.3460", "Alvo 1.3250 · BoE 05/11"]
            },
            "EUR/JPY": {
                en: ["First close under 9-mo low", "Oct-2025 shelf 175.7-175.9 below", "BoJ 29-30/10 decides"],
                pt: ["1º fechamento sob mín. 9 meses", "Prateleira out/2025 175,7-175,9", "BoJ 29-30/10 decide"]
            },
            "GBP/JPY": {
                en: ["CPI pop returned in one session", "123-pip floor blocks both sides", "BoJ 29-30/10"],
                pt: ["Pop do CPI devolvido num pregão", "Piso de 123 pips trava os dois lados", "BoJ 29-30/10"]
            }
        };'''
md_s = html.find("        const macroDrivers = {")
md_e = html.find("\n        };", md_s)
assert md_s != -1 and md_e != -1, "macroDrivers block not found"
html = html[:md_s] + new_drivers + html[md_e + len("\n        };"):]

# --- newsData: prepend the 22/10 item (updated stamp already swapped above) ---
news_item = '''                {
                    date: "22/10/2026",
                    category: "flow",
                    impact: "high",
                    pairs: ["EUR/USD", "USD/JPY", "GBP/USD", "EUR/JPY", "GBP/JPY"],
                    pt: {
                        headline: "O CPI britânico de 3,5% entrega o fade: o GBP/USD dispara o short da prateleira 1.3360-1.3420 e o livro roda de 1,3376 rumo a 1.3250 — enquanto o WTI a ~US$ 99 varre o iene e o EUR/JPY crava a mínima de 9 meses (175,97)",
                        summary: "O CPI de setembro do Reino Unido veio em 3,5% a/a (21/10, 07:00 de Londres; esperado 3,4%, de 3,1% em agosto — o maior desde outubro de 2025, com transporte a +6,6% e empréstimos públicos subindo rumo ao primeiro orçamento do chanceler) e comprou a libra por exatamente um pregão: o fechamento de 21/10 (1,3402) cravou a máxima de 10/20 pregões dentro da prateleira 1.3360-1.3420 e o de 22/10 (1,3376, -0,19%) confirmou abaixo do meio 1.3390 — o gatilho de dois passos do ticket de 20/10 disparou: short de 1,3376 (referência 1,3390), stop 1.3460, alvo 1.3250, 1:2,00 planejado, resolução por fechamento e expiração no 10º pregão (05/11, dia do BoE — que o mercado precifica com altas até dezembro). Do outro lado do corredor, o WTI a ~US$ 99 (+2% no dia, +7,7% no mês) alimentou o consenso de alta do BoJ (29-30/10, para 1,25%) e o iene varreu: o USD/JPY (-0,53%) fechou 157,05 sob a mínima de 10 pregões (157,98) e parou 5 pips acima do redondo 157,00 — a escada abaixo segue bloqueando o 1:2; o EUR/JPY (-0,78%) cravou 175,97, o primeiro fechamento sob a mínima de 9 meses 176,85 (a prateleira de out/2025, 175,70-175,92, é o apoio seguinte — e o motivo de não haver ticket); o GBP/JPY (-0,72%) devolveu o pop do CPI pela SMA50 (211,38) até 7 pips do redondo 210,00. O EUR/USD (1,1205, -0,26%) não tocou extremo nenhum — o fade da prateleira 1.1260-1.1300 é rearmado pela terceira vez. O FOMC de 27-28/10 abre o cluster.",
                        take: "O dado quente fez o que o mapa pedia: comprou a libra até a prateleira e morreu no cluster SMA — agora é o ledger que trabalha (fechamento contra 1.3460/1.3250). Do lado do iene, o rompimento chegou mas a mesa não paga o BoJ já precificado nem persegue quebra em cima da prateleira de 2025 — o cluster FOMC-BoJ decide os dois capítulos."
                    },
                    en: {
                        headline: "The UK 3.5% CPI delivers the fade: GBP/USD fires the 1.3360-1.3420 shelf short and the book runs from 1.3376 toward 1.3250 — while ~$99 WTI sweeps the yen and EUR/JPY pins the 9-month low (175.97)",
                        summary: "The UK September CPI printed 3.5% y/y (Oct 21, 07:00 London; expected 3.4%, from 3.1% in August — the highest since October 2025, with transport at +6.6% and public borrowing climbing toward the Chancellor's first budget) and bought sterling for exactly one session: the Oct-21 close (1.3402) pinned the 10/20-day high inside the 1.3360-1.3420 shelf and the Oct-22 close (1.3376, -0.19%) confirmed below the 1.3390 midpoint — the Oct-20 ticket's two-step trigger fired: short from 1.3376 (reference 1.3390), stop 1.3460, target 1.3250, planned 1:2.00, close-based resolution with expiry at the 10th session (Nov 5, BoE day — priced with hikes by December). On the other side of the corridor, ~$99 WTI (+2% on the day, +7.7% on the month) fed the BoJ hike consensus (Oct 29-30, to 1.25%) and the yen swept: USD/JPY (-0.53%) closed 157.05 under the 10-day low (157.98) and stopped 5 pips above the 157.00 round — the ladder below still blocks the 1:2; EUR/JPY (-0.78%) pinned 175.97, the first close under the 9-month low 176.85 (the Oct-2025 shelf, 175.70-175.92, is the next support — and the reason there is no ticket); GBP/JPY (-0.72%) returned the CPI pop through the SMA50 (211.38) to 7 pips off the 210.00 round. EUR/USD (1.1205, -0.26%) touched no extreme — the 1.1260-1.1300 shelf fade is re-armed a third time. The Oct 27-28 FOMC opens the cluster.",
                        take: "The hot print did what the map asked: bought sterling up to the shelf and died on the SMA cluster — the ledger works now (close-based vs 1.3460/1.3250). On the yen side the break arrived, but the desk doesn't pay the already-priced BoJ nor chases a breakdown on top of the 2025 shelf — the FOMC-BoJ cluster decides both chapters."
                    }
                },
'''
anchor = "            items: [\n"
assert html.count(anchor) == 1, "newsData items anchor not unique"
html = sub1(html, anchor, anchor + news_item, "newsData prepend")

open(INDEX, "w", encoding="utf-8", newline="").write(html)
print("OK index.html: forexData (6 pairs), stamps, ticker, macroDrivers, newsData updated")

# =====================================================================
# 2. news.html — prepend the same wire item + refresh hero & calendar
# =====================================================================
news = open(NEWS, encoding="utf-8").read()
news = sub1(news, "Wire updated: " + OLD_STAMP, "Wire updated: " + STAMP, "news dateline EN")
news = sub1(news, "Telégrafo atualizado em: " + OLD_STAMP, "Telégrafo atualizado em: " + STAMP, "news dateline PT")
news = sub1(news,
    '<span class="cd-kicker"><span class="lang-en">Market Wire · CPI Eve, Two-Speed Tape</span><span class="lang-pt" style="display:none;">Telégrafo da Mesa · Véspera do CPI, Fita de Duas Velocidades</span></span>',
    '<span class="cd-kicker"><span class="lang-en">Market Wire · Yen Sweep, Fade Fired</span><span class="lang-pt" style="display:none;">Telégrafo da Mesa · Varredura do Iene, Fade Disparado</span></span>',
    "news hero kicker")
news = sub1(news,
    '<span><span class="lang-en">6 pairs · Fed-ECB-BoJ inside 72h (27-30/10)</span><span class="lang-pt" style="display:none;">6 pares · Fed-BCE-BoJ em 72h (27-30/10)</span></span>',
    '<span><span class="lang-en">6 pairs · FOMC + BoJ next week (27-30/10)</span><span class="lang-pt" style="display:none;">6 pares · FOMC + BoJ na semana (27-30/10)</span></span>',
    "news dateline pair count")

# calendar strip: UK CPI done -> FOMC cell; the 72h cluster cell -> BoJ cell
news = sub1(news,
    '''                <div class="cal-cell">
                    <span class="cal-date">21/10</span>
                    <span class="cal-event"><span class="lang-en">UK CPI (Sep) — 07:00 London</span><span class="lang-pt" style="display:none;">CPI Reino Unido (set) — 07:00 Londres</span></span>
                    <div class="cal-meta"><span class="cal-impact high" aria-hidden="true"></span><span class="cal-cur">GBP</span></div>
                </div>''',
    '''                <div class="cal-cell">
                    <span class="cal-date">27-28/10</span>
                    <span class="cal-event"><span class="lang-en">FOMC decision — blackout on</span><span class="lang-pt" style="display:none;">Decisão do FOMC — blackout vigente</span></span>
                    <div class="cal-meta"><span class="cal-impact high" aria-hidden="true"></span><span class="cal-cur">USD</span></div>
                </div>''',
    "calendar cell 1 (UK CPI -> FOMC)")
news = sub1(news,
    '''                <div class="cal-cell">
                    <span class="cal-date">27-30/10</span>
                    <span class="cal-event"><span class="lang-en">Fed, ECB &amp; BoJ inside 72h</span><span class="lang-pt" style="display:none;">Fed, BCE e BoJ em 72h</span></span>
                    <div class="cal-meta"><span class="cal-impact high" aria-hidden="true"></span><span class="cal-cur">FX</span></div>
                </div>''',
    '''                <div class="cal-cell">
                    <span class="cal-date">29-30/10</span>
                    <span class="cal-event"><span class="lang-en">BoJ decision (consensus: 1.25%)</span><span class="lang-pt" style="display:none;">Decisão do BoJ (consenso: 1,25%)</span></span>
                    <div class="cal-meta"><span class="cal-impact high" aria-hidden="true"></span><span class="cal-cur">JPY</span></div>
                </div>''',
    "calendar cell 3 (cluster -> BoJ)")

card = '''                <!-- News 22/10/2026: UK CPI 3.5% fires the GBP/USD shelf fade; ~$99 WTI sweeps the yen, EUR/JPY pins the 9-month low -->
                <article class="news-card">
                    <div class="news-card-top">
                        <span class="news-cat"><span class="lang-en">Market Flow</span><span class="lang-pt" style="display:none;">Fluxo &amp; Mercado</span></span>
                        <span class="impact-badge high"><span class="lang-en">High Impact</span><span class="lang-pt" style="display:none;">Impacto Alto</span></span>
                        <span class="news-date">22/10/2026</span>
                    </div>
                    <h2 class="news-title">
                        <span class="lang-en">The UK 3.5% CPI delivers the fade: GBP/USD fires the 1.3360-1.3420 shelf short and the book runs from 1.3376 toward 1.3250 — while ~$99 WTI sweeps the yen and EUR/JPY pins the 9-month low (175.97)</span>
                        <span class="lang-pt" style="display:none;">O CPI britânico de 3,5% entrega o fade: o GBP/USD dispara o short da prateleira 1.3360-1.3420 e o livro roda de 1,3376 rumo a 1.3250 — enquanto o WTI a ~US$ 99 varre o iene e o EUR/JPY crava a mínima de 9 meses (175,97)</span>
                    </h2>
                    <p class="news-summary">
                        <span class="lang-en">The UK September CPI printed 3.5% y/y (Oct 21, 07:00 London; expected 3.4%, from 3.1% in August — the highest since October 2025, with transport at +6.6% and public borrowing climbing toward the Chancellor's first budget) and bought sterling for exactly one session: the Oct-21 close (1.3402) pinned the 10/20-day high inside the 1.3360-1.3420 shelf and the Oct-22 close (1.3376, -0.19%) confirmed below the 1.3390 midpoint — the Oct-20 ticket's two-step trigger fired: short from 1.3376 (reference 1.3390), stop 1.3460, target 1.3250, planned 1:2.00, close-based resolution with expiry at the 10th session (Nov 5, BoE day — priced with hikes by December). On the other side of the corridor, ~$99 WTI (+2% on the day, +7.7% on the month) fed the BoJ hike consensus (Oct 29-30, to 1.25%) and the yen swept: USD/JPY (-0.53%) closed 157.05 under the 10-day low (157.98) and stopped 5 pips above the 157.00 round — the ladder below still blocks the 1:2; EUR/JPY (-0.78%) pinned 175.97, the first close under the 9-month low 176.85 (the Oct-2025 shelf, 175.70-175.92, is the next support — and the reason there is no ticket); GBP/JPY (-0.72%) returned the CPI pop through the SMA50 (211.38) to 7 pips off the 210.00 round. EUR/USD (1.1205, -0.26%) touched no extreme — the 1.1260-1.1300 shelf fade is re-armed a third time. The Oct 27-28 FOMC opens the cluster.</span>
                        <span class="lang-pt" style="display:none;">O CPI de setembro do Reino Unido veio em 3,5% a/a (21/10, 07:00 de Londres; esperado 3,4%, de 3,1% em agosto — o maior desde outubro de 2025, com transporte a +6,6% e empréstimos públicos subindo rumo ao primeiro orçamento do chanceler) e comprou a libra por exatamente um pregão: o fechamento de 21/10 (1,3402) cravou a máxima de 10/20 pregões dentro da prateleira 1.3360-1.3420 e o de 22/10 (1,3376, -0,19%) confirmou abaixo do meio 1.3390 — o gatilho de dois passos do ticket de 20/10 disparou: short de 1,3376 (referência 1,3390), stop 1.3460, alvo 1.3250, 1:2,00 planejado, resolução por fechamento e expiração no 10º pregão (05/11, dia do BoE — que o mercado precifica com altas até dezembro). Do outro lado do corredor, o WTI a ~US$ 99 (+2% no dia, +7,7% no mês) alimentou o consenso de alta do BoJ (29-30/10, para 1,25%) e o iene varreu: o USD/JPY (-0,53%) fechou 157,05 sob a mínima de 10 pregões (157,98) e parou 5 pips acima do redondo 157,00 — a escada abaixo segue bloqueando o 1:2; o EUR/JPY (-0,78%) cravou 175,97, o primeiro fechamento sob a mínima de 9 meses 176,85 (a prateleira de out/2025, 175,70-175,92, é o apoio seguinte — e o motivo de não haver ticket); o GBP/JPY (-0,72%) devolveu o pop do CPI pela SMA50 (211,38) até 7 pips do redondo 210,00. O EUR/USD (1,1205, -0,26%) não tocou extremo nenhum — o fade da prateleira 1.1260-1.1300 é rearmado pela terceira vez. O FOMC de 27-28/10 abre o cluster.</span>
                    </p>
                    <div class="news-take">
                        <span class="take-tag"><span class="lang-en">Desk take</span><span class="lang-pt" style="display:none;">Leitura da mesa</span></span>
                        <span class="lang-en">The hot print did what the map asked: bought sterling up to the shelf and died on the SMA cluster — the ledger works now (close-based vs 1.3460/1.3250). On the yen side the break arrived, but the desk doesn't pay the already-priced BoJ nor chases a breakdown on top of the 2025 shelf — the FOMC-BoJ cluster decides both chapters.</span>
                        <span class="lang-pt" style="display:none;">O dado quente fez o que o mapa pedia: comprou a libra até a prateleira e morreu no cluster SMA — agora é o ledger que trabalha (fechamento contra 1.3460/1.3250). Do lado do iene, o rompimento chegou mas a mesa não paga o BoJ já precificado nem persegue quebra em cima da prateleira de 2025 — o cluster FOMC-BoJ decide os dois capítulos.</span>
                    </div>
                    <div class="news-pairs">
                        <span class="np-label"><span class="lang-en">Watch</span><span class="lang-pt" style="display:none;">Acompanhar</span></span>
                        <a href="eur-usd.html" class="pair-link-chip">EUR/USD</a><a href="usd-jpy.html" class="pair-link-chip">USD/JPY</a><a href="gbp-usd.html" class="pair-link-chip">GBP/USD</a><a href="eur-jpy.html" class="pair-link-chip">EUR/JPY</a><a href="gbp-jpy.html" class="pair-link-chip">GBP/JPY</a>
                    </div>
                </article>

'''
first_card = '                <!-- News 20/10/2026: Two-speed tape on CPI eve — dollar steadies vs euro, sterling pins 20-day high -->'
assert news.count(first_card) == 1, "first news card anchor not found"
news = sub1(news, first_card, card + first_card, "news card prepend")
open(NEWS, "w", encoding="utf-8", newline="").write(news)
print("OK news.html: wire item prepended, hero dateline/kicker/calendar refreshed")

# =====================================================================
# 3. track-record.json — GBP/USD fired -> open; EUR/USD re-armed
# =====================================================================
led = json.load(open(LEDGER, encoding="utf-8"))
assert led["meta"]["lastUpdated"] == "20/10/2026"
led["meta"]["lastUpdated"] = "22/10/2026"

watching = led["watching"]
assert {t["pair"] for t in watching} == {"EUR/USD", "GBP/USD"}, "unexpected watching set"

eur_old = next(t for t in watching if t["pair"] == "EUR/USD")
gbp_old = next(t for t in watching if t["pair"] == "GBP/USD")

# GBP/USD FIRED at the 22/10 close: 21/10 closed 1.3402 inside the shelf (post-CPI,
# pre-designated to arm), 22/10 closed 1.3376 under the previous close and the 1.3390
# midpoint -> moves to 'open' with entry = the qualifying close (per conventions).
gbp_open = {
    "pair": "GBP/USD",
    "reportDate": "20/10/2026",
    "direction": "short",
    "setup": "pullback",
    "entry": 1.3376,
    "entryDate": "22/10/2026",
    "stop": 1.346,
    "target": 1.325,
    "plannedR": 2.0,
    "triggerRule": gbp_old["triggerRule"],
    "note": ("triggered at the 22/10 close: the 21/10 close 1.3402 (post-UK-CPI 3.5%, pinning the "
             "10/20-day high) entered the 1.3360-1.3420 shelf and the 22/10 close 1.3376 confirmed "
             "below the previous close and the 1.3390 midpoint — close-based stop 1.3460 / target "
             "1.3250, 10-session expiry at the 05/11 close (BoE day)")
}
led["open"].append(gbp_open)

# EUR/USD: no 21-22/10 close entered the shelf (max 1.1234 vs the 1.1260 floor) —
# revoked unfired and re-armed unchanged.
eur_old["note"] = ("revoked in the 22/10 edition and re-armed unchanged on the same shelf: "
                   "no 21-22/10 close entered 1.1260-1.1300 (max 1.1234 vs the 1.1260 floor); "
                   "validity re-stamped through the 30/10 close with the 27-28/10 closes "
                   "(FOMC window) not arming")
eur_old["outcome"] = "revoked"
eur_old["exitDate"] = "22/10/2026"
eur_old["entryDate"] = None
eur_old["realizedR"] = None

led["watching"] = [
    {
        "pair": "EUR/USD",
        "reportDate": "22/10/2026",
        "direction": "short",
        "setup": "pullback",
        "entry": 1.128,
        "stop": 1.136,
        "target": 1.112,
        "plannedR": 2.0,
        "triggerRule": "daily close inside 1.1260-1.1300 (the failed Oct-6 close 1.1269 + the 1.1300 round) followed by a close below the previous close and the 1.1280 midpoint (entry reference 1.1280); only closes after the 22/10 report count and the 27-28/10 closes (FOMC window) don't arm; valid through the 30/10 close",
        "note": "re-armed unchanged for a third straight edition (18->20->22/10): the Oct 21-22 closes (1.1234/1.1205) faded away from the shelf without entering it — stop 1.1360 (80 pips over the 29-30/09 double close 1.1355 and the 78.6% Fib 1.1348, >= the 58-pip 1.5-sigma20 floor), target 1.1120 under the 9-month low crossing only the 1.1150 round"
    }
]
led["closed"].append(eur_old)

json.dump(led, open(LEDGER, "w", encoding="utf-8", newline=""), ensure_ascii=False, indent=2)
open(LEDGER, "a", encoding="utf-8", newline="").write("\n")
print("OK track-record.json: GBP/USD fired -> open (entry 1.3376), EUR/USD re-armed, lastUpdated 22/10")

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
    m = re.search(r"(<loc>%s</loc>\s*<lastmod>)[\d-]+(</lastmod>)" % re.escape(loc), sm)
    assert m, "sitemap: entry not found for %s" % loc
    sm = sm[:m.start()] + m.group(1) + "2026-10-22" + m.group(2) + sm[m.end():]
open(SITEMAP, "w", encoding="utf-8", newline="").write(sm)
print("OK sitemap.xml: lastmod refreshed to 2026-10-22")

print("\nBuild complete. Now run build_static_pages.py + build_track_record_page.py + verify_all.py.")
