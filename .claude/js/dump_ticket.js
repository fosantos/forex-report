// Dump the trade ticket structure: containers, inputs, buttons, texts
(function () {
  var NL = String.fromCharCode(10);
  function info(e) {
    var r = e.getBoundingClientRect();
    return {
      tag: e.tagName.toLowerCase(),
      cls: String(e.className).slice(0, 45),
      t: (e.innerText || e.value || "").trim().split(NL).join(" ").slice(0, 45),
      x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)
    };
  }
  // find the biggest overlay/dialog container
  var conts = Array.from(document.querySelectorAll("div")).filter(function (e) {
    var r = e.getBoundingClientRect();
    var cls = String(e.className || "").toLowerCase();
    return r.width > 300 && r.height > 250 && /dialog|modal|ticket|trade|drawer/.test(cls);
  });
  if (!conts.length) return JSON.stringify({ error: "no ticket container" });
  conts.sort(function (a, b) {
    var ra = a.getBoundingClientRect(), rb = b.getBoundingClientRect();
    return rb.width * rb.height - ra.width * ra.height;
  });
  var root = conts[0];
  var out = { container: info(root), texts: [], inputs: [], buttons: [] };
  root.querySelectorAll("*").forEach(function (e) {
    var r = e.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return;
    var tag = e.tagName.toLowerCase();
    if (tag === "input" || tag === "textarea") out.inputs.push(info(e));
    else if (tag === "button" || e.getAttribute("role") === "button") out.buttons.push(info(e));
  });
  out.texts = (root.innerText || "").split(NL).filter(function (s) { return s.trim(); }).slice(0, 45);
  return JSON.stringify(out);
})()
