"""Definitive SL/TP set: read editor state WITHOUT toggling blindly.
Verify mode by input content (a rate ~1.3xxx = price mode; $-like number = dollar mode).
After each Set, verify via the ticket's SL/TP dollar previews (risk/reward math).
Expected with $9,500 @ X30 (units ~210.7k, entry ~1.3526):
  SL 1.3490 -> preview approx -760 dollars; TP 1.3800 -> approx +5,770 dollars."""
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

def previews():
    """Return the dollar previews shown on the ticket's SL/TP rows."""
    return c.eval('''(function(){
      var NL=String.fromCharCode(10);
      var els=Array.from(document.querySelectorAll("*")).filter(function(e){
        return e.childElementCount===0 && /Stop Loss|Take Profit/i.test(e.textContent||"") && e.getBoundingClientRect().width>0;
      });
      var out={};
      els.forEach(function(e){
        var p=e.parentElement;var txt=(p?p.innerText:"")||"";
        var m=txt.match(/-?\\$[0-9,]+\\.?\\d*/);
        out[(e.textContent||"").trim()]=m?m[0]:"?";
      });
      return JSON.stringify(out);
    })()''')

def editor_input():
    ins = json.loads(c.eval('''(function(){
      return JSON.stringify(Array.from(document.querySelectorAll("input")).map(function(e){
        var r=e.getBoundingClientRect();
        return {val:e.value,x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),vis:r.width>0};
      }).filter(function(o){return o.vis&&o.y>380&&o.y<700}));
    })()'''))
    return ins[0] if ins else None

def set_rate(label_re, rate):
    print(f"== {label_re} -> {rate} ==")
    print("  previews before:", previews())
    r = json.loads(c.eval(f'''(function(){{
      var els=Array.from(document.querySelectorAll("*")).filter(function(e){{
        return e.childElementCount===0 && /{label_re}/.test(e.textContent||"") && e.getBoundingClientRect().width>0;
      }});
      if(!els.length) return null;
      var b=els[0].getBoundingClientRect();
      return JSON.stringify({{x:Math.round(b.x+b.width/2),y:Math.round(b.y+b.height/2)}});
    }})()'''))
    c.click(r["x"], r["y"]); time.sleep(2.0)
    inp = editor_input()
    if not inp:
        print("  editor did not open; retrying row click")
        c.click(r["x"], r["y"]); time.sleep(2.0)
        inp = editor_input()
        if not inp:
            raise SystemExit("ABORT: editor never opened")
    print("  editor input:", inp)
    # mode detection: value like 1.3xxx = price mode; like "3,800" = dollar mode
    v = inp["val"].replace(",", "")
    looks_rate = v.startswith("1.3")
    if not looks_rate:
        m = c.eval('(function(){var els=Array.from(document.querySelectorAll("*")).filter(function(e){var r2=e.getBoundingClientRect();return e.childElementCount<=1&&(e.textContent||"").trim()==="Price"&&r2.width>0&&r2.y>380});if(!els.length)return "no toggle";els[0].click();return "switched"})()')
        print("  switched to price mode:", m)
        time.sleep(1.2)
        inp = editor_input()
        print("  editor input now:", inp)
    c.click(inp["x"] + inp["w"] // 2, inp["y"] + 10)
    time.sleep(0.5)
    c.select_all()
    c.type_full(rate)
    time.sleep(1.2)
    inp2 = editor_input()
    print("  after typing:", inp2)
    if not inp2 or rate not in inp2["val"]:
        raise SystemExit(f"ABORT: typing failed for {label_re}: {inp2}")
    # Set: try trusted click if visible, else DOM click
    setpos = json.loads(c.eval('(function(){var b=Array.from(document.querySelectorAll("button")).filter(function(e){return (e.innerText||"").trim()==="Set"&&e.getBoundingClientRect().width>0});if(!b.length)return null;var r=b[0].getBoundingClientRect();return JSON.stringify({x:Math.round(r.x+r.width/2),y:Math.round(r.y+r.height/2),h:Math.round(r.height)})})()'))
    print("  Set button:", setpos)
    if setpos and setpos["y"] < 550 and setpos["y"] > 0:
        c.click(setpos["x"], setpos["y"])
        print("  Set: trusted click")
    else:
        c.eval('(function(){var b=Array.from(document.querySelectorAll("button")).filter(function(e){return (e.innerText||"").trim()==="Set"&&e.getBoundingClientRect().width>0});if(b.length){b[0].click();return "dom"}})()')
        print("  Set: dom click")
    time.sleep(2.0)
    print("  previews after:", previews())

set_rate("Stop Loss", "1.3490")
set_rate("Take Profit", "1.3800")
c.shot("../etoro-ticket-verified.png")
print("screenshot saved")
