(function () {
  // Step 1: switch SL editor to Price mode and return the editor input state
  var NL = String.fromCharCode(10);
  // click the SL row label to open the editor (trusted click coordinates returned)
  var rows = Array.from(document.querySelectorAll("*")).filter(function (e) {
    return e.childElementCount === 0 && /Stop Loss/i.test(e.textContent || "") && e.getBoundingClientRect().width > 0;
  });
  if (!rows.length) return JSON.stringify({ err: "no SL row" });
  var row = rows[0].getBoundingClientRect();
  return JSON.stringify({ slRow: { x: Math.round(row.x + row.width / 2), y: Math.round(row.y + row.height / 2) } });
})()
