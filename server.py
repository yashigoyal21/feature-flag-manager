"""
server.py — Feature Flag HTTP Server
Wraps your existing main.py functions in a web server so the
Flutter app can read/update flags.json over HTTP instead of
needing direct file access.

Does NOT replace ui.py or main.py — both still work exactly
as before. This is an ADDITIONAL file.

Run with: python server.py
"""

import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

# Reuse your existing backend functions — no duplicate logic
from main import load_flags, save_flags, toggle_flag, set_config


class FlagHandler(BaseHTTPRequestHandler):

    def _send_json(self, code, payload):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        # CORS headers — required so the Flutter web app (running on
        # a different port) is allowed to call this server
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length)) if length else {}

    def do_OPTIONS(self):
        # Browsers send this automatically before PUT/POST requests.
        self._send_json(200, {})

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/":
            self._send_json(200, {"status": "Feature Flag Server is running"})

        elif path == "/all":
            data = load_flags()
            self._send_json(200, data)

        else:
            self._send_json(404, {"error": "Not found"})

    def do_PUT(self):
        path = urlparse(self.path).path

        if path.startswith("/flags/") and path.endswith("/toggle"):
            name = path[len("/flags/"):-len("/toggle")]
            data = load_flags()
            found = any(f["name"] == name for f in data["flags"])
            if not found:
                self._send_json(404, {"error": f"Flag '{name}' not found"})
                return
            toggle_flag(name)
            data = load_flags()
            self._send_json(200, {"message": f"Toggled '{name}'", "data": data})

        elif path.startswith("/configs/"):
            key = path[len("/configs/"):]
            body = self._read_body()
            value = body.get("value")
            if value is None:
                self._send_json(400, {"error": "Missing 'value' in request"})
                return
            set_config(key, value)
            data = load_flags()
            self._send_json(200, {"message": f"Updated '{key}'", "data": data})

        else:
            self._send_json(404, {"error": "Not found"})

    def log_message(self, format, *args):
        print(f"[HTTP] {self.address_string()} - {format % args}")


if __name__ == "__main__":
    PORT = 8000
    httpd = HTTPServer(("0.0.0.0", PORT), FlagHandler)
    print("=" * 50)
    print("FEATURE FLAG SERVER STARTED")
    print("=" * 50)
    print(f"  Server running at: http://localhost:{PORT}")
    print()
    print("  Endpoints:")
    print("    GET  /all                  - get everything")
    print("    PUT  /flags/<name>/toggle  - toggle a flag on/off")
    print("    PUT  /configs/<key>        - update a config value")
    print("=" * 50)
    print("  Press Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
