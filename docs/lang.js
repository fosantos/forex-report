/* ==========================================================================
   Forex Report — shared bilingual language switcher (static pages)
   --------------------------------------------------------------------------
   Loaded (deferred) by every static page that uses the .lang-en / .lang-pt
   duplicate-DOM mechanism: the 6 pair pages, news, about, contact,
   track-record, the guides hub and the 6 education guides. It replaces the
   per-page inline switchers (previously duplicated ~60 lines per page).

   Per-page inputs:
   - the EN <title> is simply the page's own <title> (captured at load);
   - the PT <title> lives in <html data-title-pt="...">.
   Pages whose chrome is single-copy (about, contact) also get their nav and
   footer labels translated here — guarded, so it is a no-op elsewhere.
   The track-record ledger's bilingual <tr class="tr-pt"> rows are toggled
   here too (no-op on pages without tables).
   index.html does NOT load this file — its dashboard i18n engine lives inline.
   ========================================================================== */
(function () {
    'use strict';

    var currentLang = 'en';
    var enTitle = document.title;
    var ptTitle = document.documentElement.getAttribute('data-title-pt') || enTitle;

    // Single-copy chrome labels (about, contact) — id-driven, null-guarded
    var uiStrings = {
        en: {
            navHome: "Dashboard", navNews: "News", navGuides: "Education", navAbout: "About Us", navContact: "Contact",
            footerDisclaimer: "Disclaimer: Forex trading involves significant risk. Leverage can work against you. Past results do not guarantee future performance. Content is purely educational and does not constitute financial advice.",
            footerContact: "Have questions? Contact us:",
            footerLinkAbout: "About Us", footerLinkContact: "Contact",
            footerLinkDisclaimer: "Legal Disclaimer", footerLinkPrivacy: "Privacy Policy", footerLinkTerms: "Terms of Service",
            footerRights: "All rights reserved."
        },
        pt: {
            navHome: "Painel", navNews: "Notícias", navGuides: "Educação", navAbout: "Quem Somos", navContact: "Contato",
            footerDisclaimer: "Aviso: O mercado de câmbio (Forex) envolve riscos significativos. A alavancagem pode funcionar contra si. Resultados passados não garantem lucros futuros. O conteúdo é meramente educativo e não constitui aconselhamento financeiro.",
            footerContact: "Dúvidas ou sugestões? Contacte-nos:",
            footerLinkAbout: "Quem Somos", footerLinkContact: "Contato",
            footerLinkDisclaimer: "Aviso Legal", footerLinkPrivacy: "Política de Privacidade", footerLinkTerms: "Termos de Serviço",
            footerRights: "Todos os direitos reservados."
        }
    };

    var chromeIds = ['navHome', 'navNews', 'navGuides', 'navAbout', 'navContact',
                     'footerDisclaimerText', 'footerContactText',
                     'footerLinkAbout', 'footerLinkContact',
                     'footerLinkDisclaimer', 'footerLinkPrivacy',
                     'footerLinkTerms', 'footerRightsText'];

    function setLangClass(selector, show) {
        // SPAN-level duplicates must return to inline, containers to block
        document.querySelectorAll(selector).forEach(function (el) {
            el.style.display = show ? (el.tagName === 'SPAN' ? 'inline' : 'block') : 'none';
        });
    }

    function updateLangDisplay() {
        setLangClass('.lang-en', currentLang === 'en');
        setLangClass('.lang-pt', currentLang === 'pt');
        document.title = currentLang === 'pt' ? ptTitle : enTitle;

        // Bilingual ledger rows (track-record): table rows and header groups
        var showPt = currentLang === 'pt';
        document.querySelectorAll('tr.tr-pt').forEach(function (el) {
            el.style.display = showPt ? 'table-row' : 'none';
        });
        document.querySelectorAll('thead.tr-pt').forEach(function (el) {
            el.style.display = showPt ? 'table-header-group' : 'none';
        });

        var t = uiStrings[currentLang];
        chromeIds.forEach(function (id) {
            var el = document.getElementById(id);
            if (el && t[id]) el.textContent = t[id];
        });

        // Propagate the active language through every internal .html link
        document.querySelectorAll('a').forEach(function (link) {
            var href = link.getAttribute('href');
            if (!href) return;
            if (href.indexOf('index.html?pair=') === 0) {
                link.setAttribute('href', href.split('&')[0] + '&lang=' + currentLang);
            } else if (href.slice(-5) === '.html' && href.indexOf('?') === -1) {
                link.setAttribute('href', href + '?lang=' + currentLang);
            } else if (href.indexOf('.html?') !== -1 && href.indexOf('lang=') !== -1) {
                link.setAttribute('href', href.split('?')[0] + '?lang=' + currentLang);
            }
        });
    }

    function initLanguage() {
        // PT only for pt-br / pt-pt headers; otherwise default EN
        var languages = navigator.languages || [navigator.language || ''];
        for (var i = 0; i < languages.length; i++) {
            var clean = String(languages[i]).toLowerCase();
            if (clean === 'pt-br' || clean === 'pt-pt') { currentLang = 'pt'; break; }
        }

        // URL override (?lang=pt / ?lang=en) for CRO/marketing links
        var m = location.search.match(/[?&]lang=(pt|en)/i);
        if (m) currentLang = m[1].toLowerCase();

        var sel = document.getElementById('langSelect');
        if (sel) sel.value = currentLang;
        updateLangDisplay();
    }

    var langSelect = document.getElementById('langSelect');
    if (langSelect) {
        langSelect.addEventListener('change', function (e) {
            currentLang = e.target.value === 'pt' ? 'pt' : 'en';
            updateLangDisplay();
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initLanguage);
    } else {
        initLanguage();
    }
})();
