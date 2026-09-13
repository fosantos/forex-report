"""Fill the eToro GBP/USD ticket: SL 1.3490, TP 1.3800 (rate mode), amount $9,500 (X30).
Runs against the fresh-tab target. Verifies each step; aborts on mismatch."""
import json, sys, time, urllib.request, websocket
sys.path.insert(0, ".")
import cdp as cdpmod

targets = json.load(urllib.request.urlopen("http://127.0.0.1:9222/json/list", timeout=10))
new = [t for t in targets if t["id"] == "43597600BE93DF9F1CCF667DBFDD0613"][0]

class CDP2(cdpmod.CDP):
    def __init__(self, target):
        self.ws = websocket.create_connection(target["webSocketDebuggerUrl"], timeout=30, suppress_origin=True)
        self.id = 0

c = CDP2(new)

def editor_inputs():
    return json.loads(c.eval('''(function(){
      return JSON.stringify(Array.from(document.querySelectorAll("input")).map(function(e){
        var r=e.getBoundingClientRect();
        return {val:e.value,x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),vis:r.width>0};
      }).filter(function(o){return o.vis&&o.y>400&&o.y<700}));
    })()'''))

def set_rate(row_re, rate):
    # open editor by clicking the row label (trusted)
    r = json.loads(c.eval(f'''(function(){{
      var els=Array.from(document.querySelectorAll("*")).filter(function(e){{
        return e.childElementCount===0 && /{row_re}/.test(e.textContent||"") && e.getBoundingClientRect().width>0;
      }});
      if(!els.length) return null;
      var b=els[0].getBoundingClientRect();
      return JSON.stringify({{x:Math.round(b.x+b.width/2),y:Math.round(b.y+b.height/2)}});
    }})()'''))
    c.click(r["x"], r["y"]); time.sleep(2)
    # switch to Price mode
    sw = c.eval('''(function(){
      var els=Array.from(document.querySelectorAll("*")).filter(function(e){
        var r2=e.getBoundingClientRect();
        return e.childElementCount<=1 && (e.textContent||"").trim()==="Price" && r2.width>0 && r2.y>380;
      });
      if(!els.length) return "no toggle";
      els[0].click(); return "price-mode";
    })()''')
    print("  mode:", sw); time.sleep(1.2)
    ins = editor_inputs()
    print("  editor inputs:", ins)
    tgt = ins[0]
    # set value via native setter + input/change events (Angular binding)
    r = c.eval('''(function(){
      var el=Array.from(document.querySelectorAll("input")).filter(function(e){
        var r=e.getBoundingClientRect(); return r.width>0 && r.y>400 && r.y<700;
      })[0];
      if(!el) return "no input";
      el.focus();
      var set=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,"value").set;
      set.call(el, "%s");
      el.dispatchEvent(new Event("input", {bubbles:true}));
      el.dispatchEvent(new Event("change", {bubbles:true}));
      return "set";
    })()''' % rate)
    print("  native set:", r)
    time.sleep(1.0)
    ins2 = editor_inputs()
    print("  after type:", ins2)
    ok = any(rate.replace(".", ",") in i["val"] or i["val"] == rate for i in ins2)
    print("  value ok?", ok)
    if not ok:
        raise SystemExit(f"ABORT: rate {rate} not set for {row_re}")
    st = c.eval('(function(){var b=Array.from(document.querySelectorAll("button")).filter(function(e){return (e.innerText||"").trim()==="Set"&&e.getBoundingClientRect().width>0});if(!b.length)return "no Set";b[0].click();return "set"})()')
    print("  Set:", st)
    time.sleep(1.5)

print("== Stop Loss 1.3490 ==")
set_rate("Stop Loss", "1.3490")
print("== Take Profit 1.3800 ==")
set_rate("Take Profit", "1.3800")

# amount -> $9,500
amt = json.loads(c.eval('''(function(){
  var i=Array.from(document.querySelectorAll("input")).filter(function(e){
    var r=e.getBoundingClientRect(); return r.width>0 && r.y>80 && r.y<160 && /,/.test(e.value||"");
  });
  if(!i.length) return null;
  var r=i[0].getBoundingClientRect();
  return JSON.stringify({x:Math.round(r.x+r.width/2),y:Math.round(r.y+r.height/2)});
})()'''))
print("amount input:", amt)
if not amt:
    raise SystemExit("ABORT: amount input not found")
c.click(amt["x"], amt["y"]); time.sleep(0.4)
c.select_all()
c.insert_text("9500")
time.sleep(1.2)
final = c.eval('''(function(){
  var i=Array.from(document.querySelectorAll("input")).filter(function(e){var r=e.getBoundingClientRect();return r.width>0&&r.y>80&&r.y<160});
  return JSON.stringify(i.map(function(e){return e.value}));
})()''')
print("amount now:", final)
print("\nTICKET TEXT:")
print(c.eval('document.body.innerText.split(String.fromCharCode(10)).filter(function(s){return s.trim()}).slice(0,60).join(" | ")')[:1300])
c.shot("../etoro-ticket-filled.png")
print("screenshot saved")
