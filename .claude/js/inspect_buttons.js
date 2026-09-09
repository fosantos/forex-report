// Inspect buy/sell button components, shadow DOM, and the account switcher state
(function () {
  var NL = String.fromCharCode(10);
  function dig(el, depth, out) {
    if (!el || depth > 3) return;
    var kids = el.shadowRoot ? el.shadowRoot.querySelectorAll("*") : [];
    Array.from(kids).slice(0, 60).forEach(function (k) {
      var r = k.getBoundingClientRect();
      if (r.width > 20 && r.height > 15) {
        out.push({
          comp: el.tagName.toLowerCase(), tag: k.tagName.toLowerCase(),
          t: (k.textContent || "").trim().slice(0, 25),
          x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)
        });
      }
    });
  }
  var btnInfo = [];
  ["et-market-page-trade-button", "et-buy-sell-button"].forEach(function (sel) {
    Array.from(document.querySelectorAll(sel)).forEach(function (e) {
      var r = e.getBoundingClientRect();
      btnInfo.push({
        comp: sel, x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height),
        hasShadow: !!e.shadowRoot, text: (e.textContent || "").trim().slice(0, 40)
      });
      dig(e, 1, btnInfo);
    });
  });
  var switcher = document.querySelector("et-sidenav-account-switcher");
  var swInfo = null;
  if (switcher) {
    var swText = (switcher.shadowRoot ? switcher.shadowRoot.textContent : switcher.textContent) || "";
    swInfo = { hasShadow: !!switcher.shadowRoot, text: swText.replace(/\s+/g, " ").trim().slice(0, 200) };
  }
  return JSON.stringify({ buttons: btnInfo.slice(0, 15), switcher: swInfo });
})()
