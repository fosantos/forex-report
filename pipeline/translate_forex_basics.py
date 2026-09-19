# -*- coding: utf-8 -*-
"""One-off: convert guides/forex-basics.html to the site's bilingual block model.
The whole guide content (breadcrumb → related links) is wrapped in a lang-en div and
duplicated as a translated lang-pt div (ids suffixed -pt so PT anchors still jump)."""
import re

PATH = "docs/guides/forex-basics.html"
TITLE_EN = "Forex Basics: A Beginner's Guide to Currency Trading - Forex Report"
TITLE_PT = "Básico de Forex: Guia de Iniciante para Negociação de Moedas - Forex Report"

with open(PATH, encoding="utf-8") as f:
    s = f.read()

assert 'lang-en' not in s and 'lang-pt' not in s, "already converted"

m = re.search(r'( *)<div class="breadcrumb">.*?← Back to Dashboard</a>\s*<p style="margin-top: 1rem;.*?</p>\s*</div>', s, re.S)
assert m, "content region not found"
en_block = m.group(0)
indent = m.group(1)

PT_BLOCK = indent + '''<div class="breadcrumb">
                <a href="../index.html">Início</a> &gt; <a href="index.html">Guias</a> &gt; <span>Básico de Forex</span>
            </div>

            <h1 style="margin-bottom: 1rem;">Básico de Forex: Guia de Iniciante para Negociação de Moedas</h1>
            <p style="font-size: 1.1rem; color: var(--text-secondary); margin-bottom: 2rem;">Aprenda os fundamentos do mercado de câmbio: o que ele é, como funciona, quem participa e o que move os preços das moedas.</p>

            <div class="toc">
                <h3>📑 Índice</h3>
                <ul>
                    <li><a href="#definition-pt">O que é Forex?</a></li>
                    <li><a href="#history-pt">Breve História do Forex</a></li>
                    <li><a href="#how-works-pt">Como o Forex Funciona</a></li>
                    <li><a href="#pairs-pt">Entendendo os Pares de Moedas</a></li>
                    <li><a href="#participants-pt">Participantes do Mercado</a></li>
                    <li><a href="#drivers-pt">O que Move os Preços do Forex?</a></li>
                    <li><a href="#why-trade-pt">Por que Negociar Forex?</a></li>
                    <li><a href="#risks-pt">Riscos do Trading em Forex</a></li>
                </ul>
            </div>

            <!-- DEFINITION -->
            <section class="guide-section" id="definition-pt">
                <h2>O que é Forex?</h2>
                <p><strong>Forex (ou FX) é o mercado global de negociação de moedas.</strong> É onde o Dólar americano (USD), o Euro (EUR), a Libra esterlina (GBP), o Iene japonês (JPY) e outras moedas são comprados e vendidos.</p>

                <p>Diferente das ações (em que você é dono de uma fração de uma empresa) ou das commodities (em que você é dono de bens físicos), o trading em forex é sempre sobre a *taxa de câmbio* entre duas moedas. Você especula se uma moeda vai se fortalecer ou enfraquecer em relação à outra.</p>

                <h3>Dados-chave sobre o Forex</h3>
                <ul>
                    <li><strong>Maior mercado do mundo:</strong> ~US$ 6,6 trilhões negociados por dia (a partir de 2024)</li>
                    <li><strong>Altamente líquido:</strong> fácil entrar e sair de posições a qualquer momento</li>
                    <li><strong>Mercado 24/5:</strong> abre domingo à noite (Ásia) e fecha sexta à noite (horário dos EUA)</li>
                    <li><strong>De balcão (OTC):</strong> sem bolsa central; as operações ocorrem eletronicamente entre bancos, corretoras e instituições</li>
                    <li><strong>Alavancagem disponível:</strong> você pode controlar posições grandes com pouco capital (mas isso amplia as perdas)</li>
                </ul>

                <div class="example-box">
                    <strong>Exemplo simples:</strong> você acredita que o Euro vai se fortalecer contra o Dólar americano. Você "compra EUR/USD" a 1,10. Se subir para 1,12, você lucra. Se cair para 1,08, você perde. A diferença (0,02 neste caso) é seu ganho ou perda por unidade de moeda mantida.
                </div>
            </section>

            <!-- HISTORY -->
            <section class="guide-section" id="history-pt">
                <h2>Breve História do Forex</h2>

                <h3>A Era de Bretton Woods (1944–1971)</h3>
                <p>Após a Segunda Guerra Mundial, as moedas eram atreladas ao Dólar americano, que por sua vez era atrelado ao ouro. Esse sistema de taxas fixas mantinha o forex relativamente estático. O trading era mínimo porque as taxas quase não se moviam.</p>

                <h3>A Era das Taxas Flutuantes (1971–presente)</h3>
                <p>Em 1971, os EUA abandonaram o padrão-ouro. As moedas passaram a flutuar livremente com base em oferta e demanda. Essa volatilidade criou a oportunidade para o trading em forex como o conhecemos hoje.</p>

                <h3>Forex moderno (1995–presente)</h3>
                <p>As plataformas eletrônicas de negociação democratizaram o forex. No fim dos anos 1990 e início dos 2000, traders de varejo passaram a acessar o mercado via corretoras. Hoje, o varejo representa uma parcela significativa do volume, embora bancos centrais, hedge funds e grandes instituições ainda dominem.</p>
            </section>

            <!-- HOW WORKS -->
            <section class="guide-section" id="how-works-pt">
                <h2>Como o Forex Funciona</h2>

                <h3>A mecânica de uma operação de câmbio</h3>
                <p>Quando você opera forex, executa uma troca simples:</p>
                <ul>
                    <li>Você vende uma moeda (a "base")</li>
                    <li>Você compra outra moeda (a "de cotação")</li>
                    <li>Você lucra se o preço se mover a seu favor</li>
                </ul>

                <h3>Spread bid-ask</h3>
                <p>Toda moeda tem um <strong>preço bid</strong> (o que você recebe ao vender) e um <strong>preço ask</strong> (o que você paga ao comprar). A diferença é o spread — o lucro da corretora e o seu custo para entrar/sair.</p>

                <div class="example-box">
                    <strong>Exemplo de bid/ask:</strong><br>
                    EUR/USD Bid: 1,1050 | Ask: 1,1052<br>
                    Spread: 0,0002 (2 pips)<br>
                    <br>
                    Se você COMPRAR EUR/USD, paga o ask (1,1052).<br>
                    Se você VENDER EUR/USD, recebe o bid (1,1050).
                </div>

                <h3>Pips: a unidade de movimento do preço</h3>
                <p>Um <strong>pip</strong> (percentage in point) é o menor movimento padrão de preço para a maioria dos pares. Para o EUR/USD, um pip = 0,0001 (a quarta casa decimal).</p>

                <ul>
                    <li>Se o EUR/USD move de 1,1050 para 1,1052, é um movimento de 2 pips</li>
                    <li>Um movimento de 50 pips = 0,0050 de variação de preço</li>
                    <li>O valor do pip em reais/dólares depende do tamanho da posição</li>
                </ul>

                <h3>Alavancagem</h3>
                <p>Corretoras oferecem alavancagem — a capacidade de controlar posições grandes com depósitos pequenos. Proporções comuns: 50:1, 100:1 ou até 500:1 (varia conforme a regulação).</p>

                <div class="example-box">
                    <strong>Exemplo de alavancagem:</strong> com alavancagem de 100:1 e uma conta de US$ 1.000, você controla ~US$ 100.000 em moeda. Um movimento de 1% a seu favor = 100% de lucro. Mas 1% contra você = 100% de perda (conta queimada).
                </div>

                <p style="color: var(--color-alert); font-weight: 600;">⚠️ A alavancagem amplia ganhos E perdas. A maioria dos traders de varejo perde dinheiro justamente por usar alavancagem de forma errada.</p>
            </section>

            <!-- PAIRS -->
            <section class="guide-section" id="pairs-pt">
                <h2>Entendendo os Pares de Moedas</h2>

                <h3>Estrutura: base/cotação</h3>
                <p>Todo par forex é escrito como BASE/COTAÇÃO. A moeda da esquerda é o que você compra ou vende; a da direita é a moeda pela qual você a compra ou vende.</p>

                <div class="example-box">
                    <strong>EUR/USD = 1,1050</strong><br>
                    Isso significa 1 Euro = 1,1050 Dólares americanos.
                </div>

                <h3>Pares majors (mais negociados)</h3>
                <p>Envolvem o Dólar americano e são altamente líquidos:</p>
                <ul>
                    <li><strong>EUR/USD:</strong> Euro vs Dólar</li>
                    <li><strong>USD/JPY:</strong> Dólar vs Iene japonês</li>
                    <li><strong>GBP/USD:</strong> Libra esterlina vs Dólar</li>
                    <li><strong>USD/CHF:</strong> Dólar vs Franco suíço</li>
                    <li><strong>AUD/USD:</strong> Dólar australiano vs Dólar</li>
                </ul>

                <h3>Pares cruzados (sem USD)</h3>
                <p>Não envolvem o dólar. Menos líquidos, mas oferecem diversificação:</p>
                <ul>
                    <li><strong>EUR/JPY:</strong> Euro vs Iene</li>
                    <li><strong>GBP/JPY:</strong> Libra vs Iene</li>
                    <li><strong>EUR/GBP:</strong> Euro vs Libra</li>
                    <li><strong>AUD/JPY:</strong> Dólar australiano vs Iene</li>
                </ul>

                <h3>Pares exóticos</h3>
                <p>Pares com moedas menores ou de mercados emergentes (SGD, MXN, ZAR etc.). Spreads largos e pouca liquidez; não são ideais para iniciantes.</p>
            </section>

            <!-- PARTICIPANTS -->
            <section class="guide-section" id="participants-pt">
                <h2>Participantes do Mercado</h2>

                <h3>Bancos centrais</h3>
                <p>Os maiores jogadores. Bancos centrais compram/vendem moedas para influenciar a política ou estabilizar a própria moeda. Uma única intervenção pode mover as taxas 5-10% em minutos.</p>

                <h3>Grandes bancos e instituições financeiras</h3>
                <p>JPMorgan, Goldman Sachs, Deutsche Bank e outros movimentam trilhões em forex diariamente para clientes, trading proprietário e hedge.</p>

                <h3>Hedge funds e CTAs</h3>
                <p>Traders sofisticados que usam teses macroeconômicas, estratégias algorítmicas e muito capital para lucrar com movimentos de curto e longo prazo do forex.</p>

                <h3>Empresas e negócios de importação/exportação</h3>
                <p>Empresas que recebem receita em moeda estrangeira fazem hedge da exposição operando forex. Exemplo: um exportador americano que recebe em euros precisa converter para dólares; ele trava as taxas via forex.</p>

                <h3>Traders de varejo (nós!)</h3>
                <p>Traders individuais que usam corretoras para especular nos pares de moedas. Somos uma fração pequena do volume total, mas crescente. Risco: a maioria dos traders de varejo perde dinheiro.</p>
            </section>

            <!-- DRIVERS -->
            <section class="guide-section" id="drivers-pt">
                <h2>O que Move os Preços do Forex?</h2>

                <h3>Diferenciais de juros</h3>
                <p>Se o Fed sobe os juros para 3,5% e o BCE segura em 2,25%, investidores em busca de retorno maior compram ativos em USD. Isso aumenta a demanda por dólares, fortalecendo-o.</p>

                <h3>Dados de inflação</h3>
                <p>Inflação alta costuma levar bancos centrais a subir juros para combatê-la. Juros mais altos atraem capital estrangeiro → a moeda se fortalece.</p>

                <h3>Crescimento econômico (PIB, PMI, emprego)</h3>
                <p>Crescimento econômico forte sinaliza oportunidades de investimento e retornos futuros maiores → a demanda por aquela moeda aumenta.</p>

                <h3>Risco geopolítico e fluxos para ativos seguros</h3>
                <p>Guerras, instabilidade política ou recessões disparam fluxos para moedas de refúgio: Dólar americano, Iene japonês, Franco suíço. Essas moedas sobem enquanto moedas de risco caem.</p>

                <h3>Anúncios e comunicação de bancos centrais</h3>
                <p>Quando o Fed sinaliza altas de juros ou o BCE sugere pausa nas altas, os mercados reagem imediatamente. O "forward guidance" dos bancos centrais molda expectativas e move os pares.</p>

                <h3>Balanças comerciais e fluxos de capital</h3>
                <p>Se um país tem déficit comercial grande (importações &gt; exportações), precisa comprar moeda estrangeira para pagar as importações. Isso enfraquece a moeda doméstica. O superávit, ao contrário, a fortalece.</p>

                <h3>Sentimento de mercado e apetite a risco</h3>
                <p>Em períodos de otimismo, investidores compram ativos mais arriscados (moedas de mercados emergentes, moedas ligadas a commodities como o AUD). Em períodos de medo, vendem os ativos de risco e compram refúgios.</p>

                <div class="example-box">
                    <strong>Exemplo multifator:</strong> o Fed sobe juros para 4,0% (surpresa hawkish). A inflação americana está alta, mas a economia cresce 3% ao ano. O USD sobe 3% sobre o EUR/USD em 24 horas porque múltiplos drivers se alinham: juros mais altos atraem capital, as expectativas de crescimento dão suporte e o viés hawkish do banco central reconfigura as expectativas.
                </div>
            </section>

            <!-- WHY TRADE -->
            <section class="guide-section" id="why-trade-pt">
                <h2>Por que Negociar Forex?</h2>

                <h3>Vantagens</h3>
                <ul>
                    <li><strong>Alta liquidez:</strong> entre/saia de posições grandes sem slippage</li>
                    <li><strong>Disponibilidade 24/5:</strong> opere na hora que couber na sua rotina (sessões asiática, europeia e americana)</li>
                    <li><strong>Barreiras baixas de entrada:</strong> comece com contas pequenas; algumas corretoras aceitam mínimo de US$ 100</li>
                    <li><strong>Alavancagem:</strong> controle posições grandes com pouco capital (espada de dois gumes)</li>
                    <li><strong>Precificação transparente:</strong> spreads bid-ask mínimos e visíveis</li>
                    <li><strong>Oportunidades de hedge:</strong> empresas protegem risco cambial; traders protegem carteiras</li>
                </ul>

                <h3>Por que NÃO negociar forex (resposta honesta)</h3>
                <ul>
                    <li><strong>Alta taxa de fracasso:</strong> 80-90% dos traders de varejo em forex perdem dinheiro</li>
                    <li><strong>Alavancagem amplia perdas:</strong> é fácil queimar uma conta rapidamente</li>
                    <li><strong>Fundamentos complexos:</strong> política de bancos centrais, geopolítica e macro exigem conhecimento profundo</li>
                    <li><strong>Desafio emocional:</strong> disciplina, gestão de risco e psicologia são mais difíceis que análise</li>
                </ul>
            </section>

            <!-- RISKS -->
            <section class="guide-section" id="risks-pt">
                <h2>Riscos do Trading em Forex</h2>

                <div style="background-color: var(--color-danger-bg); border-left: 4px solid var(--color-alert); padding: 1.2rem; margin: 1.5rem 0; border-radius: 4px;">
                    <h3 style="margin-top: 0; color: var(--color-alert);">⚠️ Riscos principais</h3>

                    <p><strong>Risco de alavancagem:</strong> a alavancagem amplia perdas. Um movimento adverso de 10% com alavancagem 100:1 = conta zerada.</p>

                    <p><strong>Risco de gaps:</strong> o forex fecha sexta à noite e reabre domingo à noite. Notícias relevantes no fim de semana podem causar gaps grandes; seu stop pode não executar no preço alvo.</p>

                    <p><strong>Risco de intervenção:</strong> bancos centrais podem intervir para estabilizar ou enfraquecer suas moedas, causando movimentos-relâmpago que disparam stops em cascata.</p>

                    <p><strong>Choque geopolítico:</strong> guerras inesperadas, sanções ou convulsões políticas podem mover pares 5-10% em segundos.</p>

                    <p><strong>Risco de contraparte:</strong> sua corretora pode falir. Corretoras reguladas têm proteção de fundos de clientes, mas sempre verifique a regulação.</p>

                    <p><strong>Alargamento de spread:</strong> em eventos voláteis de notícias, os spreads se alargam drasticamente, elevando seus custos de transação.</p>

                    <p><strong>Risco psicológico:</strong> excesso de confiança, medo e emoção levam a decisões ruins (alavancagem excessiva, segurar posições perdedoras por muito tempo, revenge trading).</p>
                </div>

                <h3>Melhores práticas de gestão de risco</h3>
                <ul>
                    <li><strong>Nunca arrisque mais de 1-2% por operação:</strong> se sua conta tem US$ 10.000, perda máxima por trade = US$ 100-200</li>
                    <li><strong>Use stop loss:</strong> sempre defina antes de entrar. Nunca mova um stop para "dar mais espaço"</li>
                    <li><strong>Evite alavancagem excessiva:</strong> mesmo que a corretora ofereça 500:1, use 10:1 ou 20:1 por segurança</li>
                    <li><strong>Tenha um plano:</strong> entrada, saída, stop e alvo ANTES de operar</li>
                    <li><strong>Registre suas operações:</strong> anote cada trade e analise por que os vencedores venceram e os perdedores perderam</li>
                    <li><strong>Eduque-se:</strong> entenda fundamentos, técnica e risco antes de arriscar dinheiro de verdade</li>
                </ul>
            </section>

            <div style="margin-top: 3rem; padding-top: 2rem; border-top: 1px solid var(--border-color);">
                <a href="../index.html" class="back-link">← Voltar ao Painel</a>
                <p style="margin-top: 1rem; color: var(--text-muted); font-size: 0.9rem;">Relacionados: <a href="our-methodology.html" style="color: var(--color-primary);">Nossa Metodologia</a> | <a href="technical-analysis.html" style="color: var(--color-primary);">Análise Técnica em Profundidade</a> | <a href="risk-management.html" style="color: var(--color-primary);">Guia de Gestão de Risco</a></p>
            </div>'''

en_wrapped = indent + '<div class="lang-en">\n' + en_block + '\n' + indent + '</div>'
pt_wrapped = indent + '<div class="lang-pt" style="display:none;">\n' + PT_BLOCK + '\n' + indent + '</div>'
s = s[:m.start()] + en_wrapped + '\n\n' + pt_wrapped + s[m.end():]

TOGGLE = '''    <script>
        let currentLang = 'en';

        function initLanguage() {
            const languages = navigator.languages || [navigator.language || ''];
            for (const lang of languages) {
                const cleanLang = lang.toLowerCase();
                if (cleanLang === 'pt-br' || cleanLang === 'pt-pt') { currentLang = 'pt'; break; }
            }
            const urlParams = new URLSearchParams(window.location.search);
            if (urlParams.has('lang')) {
                const langParam = urlParams.get('lang').toLowerCase();
                if (langParam === 'pt' || langParam === 'en') currentLang = langParam;
            }
            document.getElementById('langSelect').value = currentLang;
            updateLangDisplay();
        }

        function updateLangDisplay() {
            if (currentLang === 'pt') {
                document.querySelectorAll('.lang-en').forEach(el => el.style.display = 'none');
                document.querySelectorAll('.lang-pt').forEach(el => el.style.display = 'block');
                document.title = "TITLE_PT";
            } else {
                document.querySelectorAll('.lang-pt').forEach(el => el.style.display = 'none');
                document.querySelectorAll('.lang-en').forEach(el => el.style.display = 'block');
                document.title = "TITLE_EN";
            }
            document.querySelectorAll('a').forEach(link => {
                const href = link.getAttribute('href');
                if (href && href.endsWith('.html') && !href.includes('?')) {
                    link.setAttribute('href', href + '?lang=' + currentLang);
                } else if (href && href.includes('.html?') && href.includes('lang=')) {
                    const cleanHref = href.split('?')[0];
                    link.setAttribute('href', cleanHref + '?lang=' + currentLang);
                }
            });
        }

        window.addEventListener('DOMContentLoaded', () => {
            initLanguage();
            document.getElementById('langSelect').addEventListener('change', (e) => {
                currentLang = e.target.value;
                updateLangDisplay();
            });
        });
    </script>
</body>'''
TOGGLE = TOGGLE.replace("TITLE_PT", TITLE_PT).replace("TITLE_EN", TITLE_EN)

assert s.count("</body>") == 1
s = s.replace("</body>", TOGGLE, 1)

# the PT block display is toggled as 'block'; guide-container children are block-level already
assert s.count('class="lang-en"') == 1 and s.count('class="lang-pt"') == 1
open(PATH, "w", encoding="utf-8").write(s)
print("OK forex-basics.html converted to bilingual blocks")
