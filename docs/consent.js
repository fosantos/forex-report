/* ==========================================================================
   Forex Report — shared cookie consent (Google AdSense NPA gating)
   --------------------------------------------------------------------------
   Loaded (deferred) ONLY on pages that serve ads. Works together with the
   inline block in each page's <head>:

       try { if (localStorage.getItem('forexCookieConsent') === 'declined')
           (window.adsbygoogle = window.adsbygoogle || []).requestNonPersonalizedAds = 1; } catch (e) {}

   The NPA flag only takes effect if set BEFORE the AdSense loader runs, so
   whenever the stored choice changes the page is reloaded to apply it:
   - "accepted"  -> personalized ads (default loader behaviour)
   - "declined"  -> non-personalized ads only (no personalization cookies)
   The choice lives in localStorage (key: forexCookieConsent) and can be
   changed at any time via the "Cookie Settings" link injected in the footer.
   ========================================================================== */
(function () {
    'use strict';

    var KEY = 'forexCookieConsent';

    function readConsent() {
        try { return localStorage.getItem(KEY); } catch (e) { return null; }
    }

    function writeConsent(value) {
        try { localStorage.setItem(KEY, value); } catch (e) { /* private mode: banner-only */ }
    }

    function detectLang() {
        var m = location.search.match(/[?&]lang=(pt|en)/i);
        if (m) return m[1].toLowerCase();
        var langs = navigator.languages || [navigator.language || ''];
        for (var i = 0; i < langs.length; i++) {
            var l = String(langs[i]).toLowerCase();
            if (l === 'pt' || l === 'pt-br' || l === 'pt-pt') return 'pt';
        }
        return 'en';
    }

    function privacyHref(lang) {
        var base = /\/guides\//.test(location.pathname) ? '../privacy.html' : 'privacy.html';
        return base + (lang === 'pt' ? '?lang=pt' : '');
    }

    var T = {
        en: {
            text: 'We use cookies to personalize content and ads, and to analyze our traffic. We also share information about your use of our site with our advertising and analytics partners (such as Google AdSense). Click "Accept All" to allow personalized ads, or "Decline" for non-personalized ads only. Read our <a href="{privacy}">Privacy Policy</a> for more details.',
            accept: 'Accept All',
            decline: 'Decline',
            settings: 'Cookie Settings'
        },
        pt: {
            text: 'Utilizamos cookies para personalizar conte&uacute;dos e an&uacute;ncios e para analisar o nosso tr&aacute;fego. Tamb&eacute;m partilhamos informa&ccedil;&otilde;es sobre a sua utiliza&ccedil;&atilde;o do site com os nossos parceiros de publicidade e an&aacute;lise (como o Google AdSense). Clique em "Aceitar Todos" para permitir an&uacute;ncios personalizados, ou "Recusar" para ver apenas an&uacute;ncios n&atilde;o personalizados. Leia a nossa <a href="{privacy}">Pol&iacute;tica de Privacidade</a> para mais detalhes.',
            accept: 'Aceitar Todos',
            decline: 'Recusar',
            settings: 'Configura&ccedil;&otilde;es de Cookies'
        }
    };

    var bannerEl = null;

    function buildBanner(lang) {
        var t = T[lang];
        var banner = document.createElement('div');
        banner.className = 'cookie-banner';
        banner.id = 'cookieBanner';
        banner.setAttribute('role', 'dialog');
        banner.setAttribute('aria-live', 'polite');
        banner.style.display = 'block';
        banner.innerHTML =
            '<div class="cookie-content container">' +
            '<p>' + t.text.replace('{privacy}', privacyHref(lang)) + '</p>' +
            '<div class="cookie-buttons">' +
            '<button type="button" class="btn-cookie btn-cookie-secondary">' + t.decline + '</button>' +
            '<button type="button" class="btn-cookie btn-cookie-primary">' + t.accept + '</button>' +
            '</div>' +
            '</div>';

        banner.querySelector('.btn-cookie-secondary').addEventListener('click', function () {
            writeConsent('declined');
            // NPA flag must be set before the loader runs — reload to apply it.
            location.reload();
        });
        banner.querySelector('.btn-cookie-primary').addEventListener('click', function () {
            var previous = readConsent();
            writeConsent('accepted');
            if (previous === 'declined') {
                // Loader ran with NPA=1 for this pageview — reload to personalize.
                location.reload();
            } else {
                removeBanner();
            }
        });
        return banner;
    }

    function removeBanner() {
        if (bannerEl && bannerEl.parentNode) bannerEl.parentNode.removeChild(bannerEl);
        bannerEl = null;
    }

    function showBanner(force) {
        if (bannerEl) return;
        if (!force && readConsent()) return;
        bannerEl = buildBanner(detectLang());
        document.body.insertBefore(bannerEl, document.body.firstChild);
    }

    function settingsLink() {
        return document.querySelector('.footer-links [data-cookie-settings]');
    }

    function injectSettingsLink() {
        var container = document.querySelector('.footer-links');
        if (!container) return;
        var link = settingsLink();
        if (!link) {
            link = document.createElement('a');
            link.href = '#';
            link.className = 'footer-link';
            link.setAttribute('data-cookie-settings', '');
            link.addEventListener('click', function (e) {
                e.preventDefault();
                showBanner(true);
            });
            container.appendChild(link);
        }
        link.innerHTML = '<span class="lang-en">' + T.en.settings + '</span>' +
                         '<span class="lang-pt" style="display:none;">' + T.pt.settings + '</span>';
        syncSettingsLang(detectLang());
    }

    function syncSettingsLang(lang) {
        var link = settingsLink();
        if (!link) return;
        var en = link.querySelector('.lang-en');
        var pt = link.querySelector('.lang-pt');
        if (en) en.style.display = lang === 'pt' ? 'none' : 'inline';
        if (pt) pt.style.display = lang === 'pt' ? 'inline' : 'none';
    }

    // Keep the footer link in sync with the site's language selector.
    var langSelect = document.getElementById('langSelect');
    if (langSelect) {
        langSelect.addEventListener('change', function (e) {
            syncSettingsLang(e.target.value === 'pt' ? 'pt' : 'en');
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function () {
            injectSettingsLink();
            showBanner(false);
        });
    } else {
        injectSettingsLink();
        showBanner(false);
    }
})();
