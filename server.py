"""
Kanal sunucusu -- web oyunlari ile masaustu tracker arasindaki "bulut gizli kanal".

Su an lokalde (localhost) calisir; ayni kod bir host'a deploy edilince internetten
de erisilir. Harici bagimlilik YOK (yalnizca Python standart kutuphanesi).

Iki taraf da OTURUM KODLU odalari kullanir (ornek: DEMO):
  - Oyun (tarayici)  -> POST /api/state?room=DEMO      (sonucu yayinla)
                        GET  /api/command?room=DEMO     (tracker komutunu oku)
  - Tracker (PC)     -> GET  /api/state?room=DEMO       (sonucu oku)
                        POST /api/command?room=DEMO      (AUTO komutu yolla)

Ayrica web/ klasorundeki oyun dosyalarini statik sunar (ornek: /aviator).

Calistir:  python server.py           (varsayilan port 8000)
           python server.py 9000       (baska port)
"""

import os
import re
import sys
import json
import time
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

WEB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")

# Oda basina paylasilan durum. rooms[oda] = {"state": {...}, "command": {...}}
_rooms = {}
_lock = threading.Lock()

# Basit statik dosya tipi eslemesi
MIME = {
    ".html": "text/html; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".json": "application/json",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".svg": "image/svg+xml",
    ".ico": "image/x-icon",
}

ROOM_RE = re.compile(r"^[A-Za-z0-9_-]{1,24}$")


def _room_of(qs):
    room = (qs.get("room", ["DEMO"])[0] or "DEMO").strip()
    return room if ROOM_RE.match(room) else "DEMO"


class Handler(BaseHTTPRequestHandler):
    server_version = "CupGameChannel/1.0"

    # -- yardimcilar -------------------------------------------------------
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _json(self, obj, code=200):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self._cors()
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0) or 0)
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        try:
            return json.loads(raw.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            return {}

    def _serve_static(self, path):
        # /aviator -> web/aviator.html gibi
        rel = path.strip("/")
        if rel == "" or rel == "index":
            rel = "index.html"
        if "." not in os.path.basename(rel):
            rel = rel + ".html"
        # yol guvenligi: web/ disina cikma
        full = os.path.normpath(os.path.join(WEB_DIR, rel))
        if not full.startswith(WEB_DIR) or not os.path.isfile(full):
            self._json({"error": "not found", "path": rel}, 404)
            return
        ext = os.path.splitext(full)[1].lower()
        with open(full, "rb") as f:
            data = f.read()
        self.send_response(200)
        self.send_header("Content-Type", MIME.get(ext, "application/octet-stream"))
        self.send_header("Content-Length", str(len(data)))
        self._cors()
        self.end_headers()
        self.wfile.write(data)

    # -- HTTP metodlari ----------------------------------------------------
    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        u = urlparse(self.path)
        qs = parse_qs(u.query)
        if u.path == "/api/health":
            self._json({"ok": True, "rooms": list(_rooms.keys()), "ts": time.time()})
            return
        if u.path == "/api/state":
            room = _room_of(qs)
            with _lock:
                self._json(_rooms.get(room, {}).get("state") or {})
            return
        if u.path == "/api/command":
            room = _room_of(qs)
            with _lock:
                self._json(_rooms.get(room, {}).get("command") or {})
            return
        # statik oyun dosyalari
        self._serve_static(u.path)

    def do_POST(self):
        u = urlparse(self.path)
        qs = parse_qs(u.query)
        if u.path == "/api/state":
            room = _room_of(qs)
            data = self._read_body()
            with _lock:
                _rooms.setdefault(room, {})["state"] = data
            self._json({"ok": True})
            return
        if u.path == "/api/command":
            room = _room_of(qs)
            data = self._read_body()
            with _lock:
                _rooms.setdefault(room, {})["command"] = data
            self._json({"ok": True})
            return
        self._json({"error": "not found"}, 404)

    # gurultuyu azalt
    def log_message(self, fmt, *args):
        pass


def main():
    # Port onceligi: komut satiri > PORT ortam degiskeni (host'lar bunu verir) > 8000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = int(os.environ.get("PORT", 8000))
    httpd = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print("Kanal sunucusu calisiyor:  http://localhost:%d" % port)
    print("  Web oyun (ornek):        http://localhost:%d/aviator" % port)
    print("  Durum API:               http://localhost:%d/api/state?room=DEMO" % port)
    print("Durdurmak icin Ctrl+C")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nKapatiliyor...")
        httpd.shutdown()


if __name__ == "__main__":
    main()
