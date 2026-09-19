# -*- coding: utf-8 -*-
"""One-off: expand the evergreen 'Understanding [PAIR]' sections in the 6 static pair pages
with a pair-specific 'How the desk trades it' subsection + guide/track-record links, in EN and PT.
Content is methodology-only (no market data) so it never goes stale."""
import re, os

DOCS = os.path.join(os.path.dirname(__file__), "..", "docs")

EXTRA = {
 "eur-usd.html": ("""
                <h3>How the desk trades EUR/USD</h3>
                <p>Every EUR/USD ticket on this page follows one mechanical framework: the bias only turns bearish when the daily close sits under the 200-day SMA <em>and</em> the 50-day SMA is below it (bullish is the mirror); entries are close-based — a pullback into an anchor zone or a daily close beyond the 10-day Donchian extreme — never a candlestick shape. Because EUR/USD is the deepest of the six books, its 20-day volatility (sigma20) is usually the smallest, so the 1.5 x sigma20 minimum stop distance is rarely the binding constraint; the round 00/50 levels and the ECB/Fed event calendar usually are. New tickets are paused inside the 24h window before FOMC, ECB, US CPI and NFP releases.</p>
                <h3>Go deeper</h3>
                <p>The full rule set is documented in <a href="guides/our-methodology.html">Our Methodology</a>, and the sizing math behind the "risk &le; 1% per trade" suffix in <a href="guides/risk-management.html">Risk Management</a>. Every ticket published here is tracked after the fact, win or lose, in the <a href="track-record.html">performance track record</a>.</p>
""", """
                <h3>Como a mesa opera o EUR/USD</h3>
                <p>Todo ticket de EUR/USD desta página segue um único framework mecânico: o viés só vira de baixa quando o fechamento diário fica sob a SMA de 200 dias <em>e</em> a SMA de 50 dias está abaixo dela (alta é o espelho disso); as entradas são baseadas em fechamento — retração à zona de ancoragem ou fechamento diário além do extremo de Donchian de 10 pregões — nunca em formatos de candle. Como o EUR/USD é o mais profundo dos seis livros, sua volatilidade de 20 dias (sigma20) costuma ser a menor, então o piso de stop de 1,5 x sigma20 raramente é a restrição binding; os redondos 00/50 e o calendário BCE/Fed normalmente são. Novos tickets ficam suspensos na janela de 24h antes de FOMC, BCE, CPI e NFP dos EUA.</p>
                <h3>Para aprofundar</h3>
                <p>O conjunto completo de regras está documentado em <a href="guides/our-methodology.html">Nossa Metodologia</a>, e a matemática de dimensionamento por trás do sufixo "risco &le; 1% por operação" em <a href="guides/risk-management.html">Gestão de Risco</a>. Cada ticket publicado aqui é acompanhado depois dos fatos, no lucro ou no prejuízo, no <a href="track-record.html">registro de desempenho</a>.</p>
"""),
 "usd-jpy.html": ("""
                <h3>How the desk trades USD/JPY</h3>
                <p>USD/JPY is the one book where policy risk can override the chart: when Japanese authorities have intervened or jawboned within the last 30 days, the desk doubles the volatility floor, demanding stops of at least 2.5 x sigma20 instead of the usual 1.5 x. Mechanically the rest is identical — bias from SMA 50/200 alignment, close-based entries through the 10-day Donchian channel, a minimum 1:2 reward-to-risk — but ticket sizes shrink with the wider stop. The pair is also the cleanest expression of the interest-rate differential trade, so BoJ meetings and Fed turns tend to reprice it in gaps rather than grinds, which is exactly why the event filter matters more here than anywhere else.</p>
                <h3>Go deeper</h3>
                <p>The complete framework, including the intervention-risk clause, lives in <a href="guides/our-methodology.html">Our Methodology</a>; position-sizing under wider stops is covered in <a href="guides/risk-management.html">Risk Management</a>. How these rules have actually played out is public: see the <a href="track-record.html">performance track record</a>.</p>
""", """
                <h3>Como a mesa opera o USD/JPY</h3>
                <p>O USD/JPY é o único livro em que o risco de política pode sobrepor-se ao gráfico: quando as autoridades japonesas intervieram ou fizeram jawboning nos últimos 30 dias, a mesa dobra o piso de volatilidade, exigindo stops de pelo menos 2,5 x sigma20 em vez dos 1,5 x habituais. Mecanicamente, o restante é idêntico — viés pelo alinhamento das SMA 50/200, entradas por fechamento no canal de Donchian de 10 pregões, mínimo de 1:2 de relação risco/retorno —, mas o tamanho da posição encolhe com o stop mais largo. O par também é a expressão mais limpa do trade de diferencial de juros, então reuniões do BoJ e viradas do Fed tendem a reprecificá-lo em gaps e não em desgaste — é exatamente por isso que o filtro de eventos pesa mais aqui do que em qualquer outro par.</p>
                <h3>Para aprofundar</h3>
                <p>O framework completo, incluindo a cláusula de risco de intervenção, está em <a href="guides/our-methodology.html">Nossa Metodologia</a>; o dimensionamento com stops mais largos está coberto em <a href="guides/risk-management.html">Gestão de Risco</a>. Como essas regras funcionaram na prática é público: veja o <a href="track-record.html">registro de desempenho</a>.</p>
"""),
 "aud-usd.html": ("""
                <h3>How the desk trades AUD/USD</h3>
                <p>AUD/USD is the desk's risk-sentiment proxy: when global growth expectations and commodity prices rise, the Australian dollar usually follows, and when they crack, it sells off harder than the majors. That makes the technical framework — SMA 50/200 alignment for bias, close-based entries off the 10-day Donchian channel, 1.5 x sigma20 minimum stop, 1:2 minimum reward-to-risk — especially dependent on the event filter: RBA decisions and Chinese data (PMIs, trade balance, stimulus headlines) are treated as top-tier events for this pair, alongside the US releases that move the dollar side. Sessions matter too — the pair is most active through the Asian and London mornings, and its cleanest trends often start at the London open.</p>
                <h3>Go deeper</h3>
                <p>Start with <a href="guides/our-methodology.html">Our Methodology</a> for the full rule set and <a href="guides/fundamental-analysis.html">Fundamental Analysis</a> for how commodity and China data feed the bias. Published tickets are graded after the fact in the <a href="track-record.html">performance track record</a>.</p>
""", """
                <h3>Como a mesa opera o AUD/USD</h3>
                <p>O AUD/USD é o proxy de sentimento de risco da mesa: quando as expectativas de crescimento global e os preços de commodities sobem, o dólar australiano costuma acompanhar; quando elas racham, ele cai mais forte que os majors. Por isso o framework técnico — alinhamento das SMA 50/200 para o viés, entradas por fechamento no canal de Donchian de 10 pregões, stop mínimo de 1,5 x sigma20, relação risco/retorno mínima de 1:2 — depende ainda mais do filtro de eventos: decisões do RBA e dados chineses (PMIs, balança comercial, manchetes de estímulo) são tratados como eventos de primeira linha neste par, junto com os releases americanos que movem o lado do dólar. Sessões também importam — o par é mais ativo nas manhãs da Ásia e de Londres, e suas tendências mais limpas costumam começar na abertura de Londres.</p>
                <h3>Para aprofundar</h3>
                <p>Comece por <a href="guides/our-methodology.html">Nossa Metodologia</a> para o conjunto completo de regras e por <a href="guides/fundamental-analysis.html">Análise Fundamentalista</a> para entender como commodities e dados da China alimentam o viés. Os tickets publicados são avaliados depois dos fatos no <a href="track-record.html">registro de desempenho</a>.</p>
"""),
 "gbp-usd.html": ("""
                <h3>How the desk trades GBP/USD</h3>
                <p>"Cable" earns its reputation: UK data drops (CPI, jobs, retail sales) routinely move the pair 50-80 pips in minutes, so the desk treats BoE meetings and UK inflation prints with the same 24h pre-event freeze it applies to FOMC for the dollar side. The framework itself is unchanged from the other majors — bias only from SMA 50/200 alignment, entries only on daily closes (pullback to an anchor zone or a break of the 10-day Donchian extreme), stops at least 1.5 x sigma20 wide, reward-to-risk at least 1:2. What differs is the tape: liquidity concentrates in the London session, the New York overlap can extend moves, and fake breakouts around the London open are common enough that the close-based trigger rule exists precisely to filter them out.</p>
                <h3>Go deeper</h3>
                <p><a href="guides/technical-analysis.html">Technical Analysis</a> explains why daily closes — not intraday pokes — validate a level, and <a href="guides/risk-management.html">Risk Management</a> covers the sizing. Every published ticket is tracked in the <a href="track-record.html">performance track record</a>.</p>
""", """
                <h3>Como a mesa opera o GBP/USD</h3>
                <p>O "Cable" justifica sua fama: dados do Reino Unido (CPI, emprego, varejo) movem o par 50-80 pips em minutos com frequência, então a mesa trata reuniões do BoE e impressões de inflação britânica com o mesmo congelamento de 24h pré-evento que aplica ao FOMC no lado do dólar. O framework em si é o mesmo dos outros majors — viés apenas pelo alinhamento das SMA 50/200, entradas apenas em fechamentos diários (retração à zona de ancoragem ou rompimento do extremo de Donchian de 10 pregões), stops de pelo menos 1,5 x sigma20, risco/retorno de no mínimo 1:2. O que muda é o tape: a liquidez se concentra na sessão de Londres, a sobreposição com Nova York pode estender os movimentos, e falsos rompimentos na abertura londrina são comuns o bastante para a regra do gatilho por fechamento existir precisamente para filtrá-los.</p>
                <h3>Para aprofundar</h3>
                <p><a href="guides/technical-analysis.html">Análise Técnica</a> explica por que fechamentos diários — e não pontuações intradia — validam um nível, e <a href="guides/risk-management.html">Gestão de Risco</a> cobre o dimensionamento. Cada ticket publicado é acompanhado no <a href="track-record.html">registro de desempenho</a>.</p>
"""),
 "eur-jpy.html": ("""
                <h3>How the desk trades EUR/JPY</h3>
                <p>As a dollar-less cross, EUR/JPY compresses two stories into one price: the euro's rate path against the yen's. In practice it trades as a risk-appetite barometer — grinding higher when markets feel constructive, selling off fast when they don't — and it inherits the same intervention clause as the other yen pairs: while the MoF or BoJ has acted within the last 30 days, stops must clear 2.5 x sigma20 instead of 1.5 x. Everything else stays mechanical: SMA 50/200 alignment defines the bias, daily closes through the 10-day Donchian channel trigger entries, and any setup that cannot pay 1:2 after widening the stop is published as WAIT instead.</p>
                <h3>Go deeper</h3>
                <p>The full framework is in <a href="guides/our-methodology.html">Our Methodology</a>; how central-bank divergence drives crosses like this one is covered in <a href="guides/fundamental-analysis.html">Fundamental Analysis</a>. Results are public in the <a href="track-record.html">performance track record</a>.</p>
""", """
                <h3>Como a mesa opera o EUR/JPY</h3>
                <p>Por ser um cross sem dólar, o EUR/JPY comprime duas histórias num único preço: a trajetória de juros do euro contra a do iene. Na prática, ele funciona como termômetro de apetite a risco — sobe devagar quando o mercado está construtivo, cai rápido quando não está — e herda a mesma cláusula de intervenção dos outros pares de iene: enquanto o MoF ou o BoJ tiverem atuado nos últimos 30 dias, os stops precisam cobrir 2,5 x sigma20 em vez de 1,5 x. Todo o resto permanece mecânico: o alinhamento das SMA 50/200 define o viés, fechamentos diários no canal de Donchian de 10 pregões disparam as entradas, e qualquer setup que não pague 1:2 depois de alargar o stop é publicado como AGUARDAR.</p>
                <h3>Para aprofundar</h3>
                <p>O framework completo está em <a href="guides/our-methodology.html">Nossa Metodologia</a>; como a divergência de bancos centrais move crosses como este está coberto em <a href="guides/fundamental-analysis.html">Análise Fundamentalista</a>. Os resultados são públicos no <a href="track-record.html">registro de desempenho</a>.</p>
"""),
 "gbp-jpy.html": ("""
                <h3>How the desk trades GBP/JPY</h3>
                <p>GBP/JPY is the widest-range book on the desk: its sigma20 is routinely two to three times EUR/USD's, so a "normal" day here can be a 150-pip day. The framework absorbs that by design — stops must sit at least 2.5 x sigma20 away whenever Japanese intervention risk is active (and 1.5 x otherwise), entries trigger only on daily closes beyond the 10-day Donchian extreme, and the bias comes strictly from SMA 50/200 alignment. The combination of sterling's data drops and the yen's policy pivots makes this the pair where the 1:2 reward-to-risk gate and the event filter do the most work: a setup that survives both is published, and anything thinner is a WAIT.</p>
                <h3>Go deeper</h3>
                <p><a href="guides/risk-management.html">Risk Management</a> shows why position size, not conviction, survives a volatile book, and <a href="guides/our-methodology.html">Our Methodology</a> documents the full rule set. Published tickets and their outcomes are in the <a href="track-record.html">performance track record</a>.</p>
""", """
                <h3>Como a mesa opera o GBP/JPY</h3>
                <p>O GBP/JPY é o livro de maior amplitude da mesa: seu sigma20 costuma ser duas a três vezes o do EUR/USD, então um dia "normal" aqui pode ser um dia de 150 pips. O framework absorve isso por desenho — stops a pelo menos 2,5 x sigma20 sempre que o risco de intervenção japonesa estiver ativo (e 1,5 x caso contrário), entradas apenas em fechamentos diários além do extremo de Donchian de 10 pregões, e viés estritamente pelo alinhamento das SMA 50/200. A combinação dos dados britânicos com as viradas de política do iene faz deste o par em que o portão de 1:2 de risco/retorno e o filtro de eventos trabalham mais: o setup que sobrevive aos dois é publicado; qualquer coisa mais frágil é AGUARDAR.</p>
                <h3>Para aprofundar</h3>
                <p><a href="guides/risk-management.html">Gestão de Risco</a> mostra por que o tamanho da posição, e não a convicção, sobrevive a um livro volátil, e <a href="guides/our-methodology.html">Nossa Metodologia</a> documenta o conjunto completo de regras. Tickets publicados e seus desfechos estão no <a href="track-record.html">registro de desempenho</a>.</p>
"""),
}

for fname, (en_add, pt_add) in EXTRA.items():
    path = os.path.join(DOCS, fname)
    with open(path, encoding="utf-8") as f:
        s = f.read()
    m = re.search(r'(<section class="compliance-container">)(.*?)(</section>)', s, re.S)
    assert m, fname + ": compliance-container not found"
    block = m.group(2)
    assert "How the desk trades" not in block and "Como a mesa opera" not in block, fname + ": already expanded"
    me = re.search(r'(<div class="lang-en">)(.*?)(</div>)\s*(<div class="lang-pt")', block, re.S)
    assert me, fname + ": lang-en block not found"
    mp = re.search(r'(<div class="lang-pt"[^>]*>)(.*?)(</div>)\s*$', block.rstrip(), re.S)
    assert mp, fname + ": lang-pt block not found"
    stripped = block.rstrip()
    new_block = stripped[:me.start(3)] + en_add.rstrip() + "\n            " + stripped[me.start(3):mp.start(3)] + pt_add.rstrip() + "\n            " + stripped[mp.start(3):]
    s = s[:m.start(2)] + new_block + "\n        " + s[m.end(2):]
    with open(path, "w", encoding="utf-8") as f:
        f.write(s)
    print("OK", fname)
print("\nAll 6 pair-profile sections expanded.")
