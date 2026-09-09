// Locate S/B rate buttons in the GBPUSD instrument header
(function () {
  var cands = Array.from(document.querySelectorAll("button,[role=button],div,span")).filter(function (e) {
    var r = e.getBoundingClientRect();
    var t = (e.innerText || "").trim();
    return /^1\.35\d+$/.test(t) && r.width > 30 && r.width < 220 && r.y > 80 && r.y < 460;
  });
  var out = cands.map(function (e) {
    var r = e.getBoundingClientRect();
    return {
      t: (e.innerText || "").trim(),
      tag: e.tagName,
      cls: String(e.className).slice(0, 40),
      x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)
    };
  });
  return JSON.stringify(out.slice(0, 10));
})()
