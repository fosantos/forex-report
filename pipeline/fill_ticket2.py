"""Set SL/TP rates on the open eToro ticket using FULL keyboard events.
For each: click SL/TP row -> ensure Price mode -> trusted-click input -> Ctrl+A -> type digits -> Set.
Then set amount $9,500 the same way. Verifies row values at the end."""
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

def editor_input():
    ins = json.loads(c.eval('''(function(){
      return JSON.stringify(Array.from(document.querySelectorAll("input")).map(function(e){
        var r=e.getBoundingClientRect();
        return {val:e.value,x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),vis:r.width>0};
      }).filter(function(o){return o.vis&&o.y>380&&o.y<700}));
    })()'''))
    return ins[0] if ins else None

def set_rate(label_re, rate):
    r = json.loads(c.eval(f'''(function(){{
      var els=Array.from(document.querySelectorAll("*")).filter(function(e){{
        return e.childElementCount===0 && /{label_re}/.test(e.textContent||"") && e.getBoundingClientRect().width>0;
      }});
      if(!els.length) return null;
      var b=els[0].getBoundingClientRect();
      return JSON.stringify({{x:Math.round(b.x+b.width/2),y:Math.round(b.y+b.height/2)}});
    }})()'''))
    c.click(r["x"], r["y"]); time.sleep(2.0)
    # Price mode: if a "Price" toggle exists in the editor region, click it
    mode = c.eval('''(function(){
      var els=Array.from(document.querySelectorAll("*")).filter(function(e){
        var r2=e.getBoundingClientRect();
        return e.childElementCount<=1 && (e.textContent||"").trim()==="Price" && r2.width>0 && r2.y>380;
      });
      if(!els.length) return "already-price-or-none";
      els[0].click(); return "price-mode";
    })()''')
    print(f"  [{label_re}] mode:", mode)
    time.sleep(1.2)
    inp = editor_input()
    if not inp:
        raise SystemExit(f"ABORT: no editor input for {label_re}")
    print(f"  [{label_re}] input before:", inp)
    c.click(inp["x"] + inp["w"] // 2, inp["y"] + 10)  # trusted focus
    time.sleep(0.5)
    c.select_all()
    c.type_full(rate)
    time.sleep(1.2)
    inp2 = editor_input()
    print(f"  [{label_re}] input after:", inp2)
    if not inp2 or rate not in inp2["val"].replace(",", "."):
        raise SystemExit(f"ABORT: {label_re} value {inp2 and inp2['val']} != {rate}")
    st = c.eval('(function(){var b=Array.from(document.querySelectorAll("button")).filter(function(e){return (e.innerText||"").trim()==="Set"&&e.getBoundingClientRect().width>0});if(!b.length)return "no Set";b[0].click();return "set"})()')
    print(f"  [{label_re}] Set:", st)
    time.sleep(1.8)

# ticket must be open
kw = c.eval('document.body.innerText.includes("Leverage")')
if not kw:
    c.click(903, 160); time.sleep(4)

set_rate("Stop Loss", "1.3490")
set_rate("Take Profit", "1.3800")

# amount
amt = json.loads(c.eval('''(function(){
  var i=Array.from(document.querySelectorAll("input")).filter(function(e){
    var r=e.getBoundingClientRect(); return r.width>0 && r.y>80 && r.y<160;
  });
  if(!i.length) return null;
  var r=i[0].getBoundingClientRect();
  return JSON.stringify({x:Math.round(r.x+r.width/2),y:Math.round(r.y+r.height/2),val:i[0].value});
})()'''))
print("amount input:", amt)
c.click(amt["x"], amt["y"]); time.sleep(0.5)
c.select_all()
c.type_full("9500")
time.sleep(1.2)
print("amount now:", c.eval('(function(){var i=Array.from(document.querySelectorAll("input")).filter(function(e){var r=e.getBoundingClientRect();return r.width>0&&r.y>80&&r.y<160});return JSON.stringify(i.map(function(e){return e.value}))})()'))
c.shot("../etoro-ticket-keyed.png")
print("screenshot saved")
print("TICKET:", c.eval('document.body.innerText.split(String.fromCharCode(10)).filter(function(s){return s.trim()}).slice(0,60).join(" | ")')[:1200])
