"""Minimal CDP driver for the dedicated debugging Chrome (127.0.0.1:9222).
Used by the forex-report agent to operate the eToro virtual account UI.
Requires: pip websocket-client. Usage: python cdp.py <command> [args]
Commands: eval <js> | title | shot <file.png> | click <x> <y> | key <key> | type <text> | goto <url> | tabs"""
import json, sys, time, base64, re
import urllib.request
import websocket  # websocket-client

def http_json(path):
    req = urllib.request.Request(f"http://127.0.0.1:9222{path}")
    return json.load(urllib.request.urlopen(req, timeout=10))

def find_tab(url_substr="etoro"):
    for t in http_json("/json/list"):
        if t["type"] == "page" and url_substr in t["url"]:
            return t
    return None

class CDP:
    def __init__(self, url_substr="etoro"):
        t = find_tab(url_substr)
        if not t:
            raise SystemExit(f"ERROR: no tab matching '{url_substr}'")
        self.ws = websocket.create_connection(t["webSocketDebuggerUrl"], timeout=30, suppress_origin=True)
        self.id = 0
        self.pending = {}

    def call(self, method, params=None):
        self.id += 1
        mid = self.id
        self.ws.send(json.dumps({"id": mid, "method": method, "params": params or {}}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == mid:
                if "error" in msg:
                    raise RuntimeError(f"CDP error: {msg['error']}")
                return msg.get("result", {})

    def eval(self, js, await_promise=False):
        r = self.call("Runtime.evaluate", {"expression": js, "returnByValue": True, "awaitPromise": await_promise})
        if r.get("exceptionDetails"):
            raise RuntimeError(f"JS error: {r['exceptionDetails'].get('exception', {}).get('description', r['exceptionDetails'])}")
        return r.get("result", {}).get("value")

    def shot(self, path):
        r = self.call("Page.captureScreenshot", {"format": "png"})
        with open(path, "wb") as f:
            f.write(base64.b64decode(r["data"]))

    def click(self, x, y):
        base = {"x": x, "y": y, "button": "left", "pointerType": "mouse", "clickCount": 1}
        for etype in ["mousePressed", "mouseReleased"]:
            self.call("Input.dispatchMouseEvent", dict(base, type=etype))

    def dblclick(self, x, y):
        for etype in ["mousePressed", "mouseReleased", "mousePressed", "mouseReleased"]:
            self.call("Input.dispatchMouseEvent", {"type": etype, "x": x, "y": y, "button": "left", "clickCount": 2})

    def key(self, text):
        for ch in text:
            self.call("Input.dispatchKeyEvent", {"type": "keyDown", "text": ch})
            self.call("Input.dispatchKeyEvent", {"type": "keyUp", "text": ch})

    def insert_text(self, text):
        self.call("Input.insertText", {"text": text})

    def press_enter(self):
        for params in [
            {"type": "rawKeyDown", "key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13, "nativeVirtualKeyCode": 13},
            {"type": "keyUp", "key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13, "nativeVirtualKeyCode": 13},
        ]:
            self.call("Input.dispatchKeyEvent", params)

    def select_all(self):
        a = {"key": "a", "code": "KeyA", "windowsVirtualKeyCode": 65, "nativeVirtualKeyCode": 65}
        ctrl = {"key": "Control", "code": "ControlLeft", "windowsVirtualKeyCode": 17, "nativeVirtualKeyCode": 17}
        self.call("Input.dispatchKeyEvent", dict(ctrl, type="rawKeyDown", modifiers=2))
        self.call("Input.dispatchKeyEvent", dict(a, type="rawKeyDown", modifiers=2))
        self.call("Input.dispatchKeyEvent", dict(a, type="keyUp", modifiers=2))
        self.call("Input.dispatchKeyEvent", dict(ctrl, type="keyUp", modifiers=0))

    DIGITS = {
        "0": (48, "Digit0"), "1": (49, "Digit1"), "2": (50, "Digit2"), "3": (51, "Digit3"),
        "4": (52, "Digit4"), "5": (53, "Digit5"), "6": (54, "Digit6"), "7": (55, "Digit7"),
        "8": (56, "Digit8"), "9": (57, "Digit9"), ".": (190, "Period"), ",": (188, "Comma"),
    }

    def type_full(self, text):
        """Type text with full key events (key/code/keyCode) — most keyboard-faithful."""
        for ch in text:
            if ch not in self.DIGITS:
                continue
            code, name = self.DIGITS[ch]
            params = {"key": ch, "code": name, "windowsVirtualKeyCode": code, "nativeVirtualKeyCode": code}
            self.call("Input.dispatchKeyEvent", dict(params, type="keyDown", text=ch))
            self.call("Input.dispatchKeyEvent", dict(params, type="keyUp"))

    def wheel(self, x, y, dy=300):
        self.call("Input.dispatchMouseEvent", {"type": "mouseWheel", "x": x, "y": y,
                                               "deltaX": 0, "deltaY": dy, "pointerType": "mouse"})

    def goto(self, url):
        self.call("Page.navigate", {"url": url})

    def click_watch(self, x, y, secs=4.0):
        """Click and collect console entries / exceptions for a window of time."""
        logs = []
        def on_message(ws, raw):
            try:
                msg = json.loads(raw)
            except Exception:
                return
            if msg.get("method") == "Runtime.consoleAPICalled":
                entry = f"console.{msg['params']['type']}: " + " ".join(
                    str(a.get("value", a.get("description", ""))) for a in msg["params"].get("args", []))
                logs.append(entry[:300])
            elif msg.get("method") == "Runtime.exceptionThrown":
                d = msg["params"]["exceptionDetails"]
                logs.append("EXCEPTION: " + str(d.get("exception", {}).get("description", d))[:300])
        self.ws.on_message = on_message
        self.call("Runtime.enable")
        self.click(x, y)
        end = time.time() + secs
        while time.time() < end:
            try:
                self.ws.settimeout(max(0.2, end - time.time()))
                self.ws.recv()
            except Exception:
                pass
        self.ws.settimeout(30)
        self.ws.on_message = None
        return logs

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    cmd = sys.argv[1]
    c = CDP()
    if cmd == "eval":
        print(json.dumps(c.eval(sys.argv[2]), ensure_ascii=False))
    elif cmd == "evalfile":
        with open(sys.argv[2], encoding="utf-8") as f:
            print(json.dumps(c.eval(f.read(), await_promise="--await" in sys.argv), ensure_ascii=False))
    elif cmd == "title":
        print(c.eval("document.title + ' ||| ' + location.href"))
    elif cmd == "shot":
        c.shot(sys.argv[2]); print("saved", sys.argv[2])
    elif cmd == "click":
        c.click(float(sys.argv[2]), float(sys.argv[3])); print("clicked", sys.argv[2], sys.argv[3])
    elif cmd == "key":
        c.key(sys.argv[2]); print("typed")
    elif cmd == "goto":
        c.goto(sys.argv[2]); print("navigating")
    elif cmd == "tabs":
        for t in http_json("/json/list"):
            if t["type"] == "page":
                print(f"[{t['id']}] {t['title'][:60]} :: {t['url'][:90]}")
    else:
        raise SystemExit("unknown command: " + cmd)
