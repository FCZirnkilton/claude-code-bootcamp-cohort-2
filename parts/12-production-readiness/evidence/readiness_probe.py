import json, urllib.request, threading, sys
sys.path.insert(0, '.')
from notes_api.server import create_server
srv = create_server(host="127.0.0.1", port=0, db_path=":memory:")
threading.Thread(target=srv.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{srv.server_address[1]}"
def call(m, p, payload=None, headers=None):
    req = urllib.request.Request(base + p, data=json.dumps(payload).encode() if payload is not None else None, method=m, headers=headers or {})
    try:
        with urllib.request.urlopen(req) as r: return r.status, dict(r.headers), r.read().decode()
    except urllib.error.HTTPError as e: return e.code, dict(e.headers), e.read().decode()
print("1. stored payload:", call("POST", "/api/notes", {"title": "hi", "body": "<img src=x onerror=alert(document.cookie)>"})[0])
s, h, b = call("GET", "/api/notes")
print("   served back unescaped:", '<img src=x onerror=' in b, "| CORS header:", h.get("Access-Control-Allow-Origin"))
print("2. bind address default:", create_server.__defaults__[0])
req = urllib.request.Request(base + "/api/notes", data=b"{", method="POST", headers={"Content-Length": "5000000"})
try:
    urllib.request.urlopen(req, timeout=3)
except Exception as e:
    print("3. Content-Length 5,000,000 with 1-byte body: server blocks waiting for body ->", type(e).__name__)
srv.shutdown()
