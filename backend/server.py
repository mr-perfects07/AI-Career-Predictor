"""Dependency-free local server for the website and its JSON API."""

from __future__ import annotations

import json
import mimetypes
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FRONTEND_ROOT = PROJECT_ROOT / "frontend"
sys.path.insert(0, str(PROJECT_ROOT))
from backend.app.core import CAREERS, QUESTIONS, public_career, recommend  # noqa: E402


class SiteHandler(BaseHTTPRequestHandler):
    server_version = "CareerPredictor/1.0"

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        path = unquote(urlparse(self.path).path)
        if path == "/health":
            return self.send_json(200, {"status": "ok"})
        if path == "/questions":
            return self.send_json(200, QUESTIONS)
        if path == "/careers":
            return self.send_json(200, [public_career(career) for career in CAREERS])
        if path.startswith("/careers/"):
            career_id = path.removeprefix("/careers/")
            career = next((item for item in CAREERS if item["id"] == career_id), None)
            if career is None:
                return self.send_json(404, {"detail": "Career not found"})
            return self.send_json(200, public_career(career, include_details=True))
        return self.send_static(path)

    def do_POST(self):
        if urlparse(self.path).path != "/recommend":
            return self.send_json(404, {"detail": "Not found"})
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 65536:
                raise ValueError("Request body is empty or too large")
            answers = json.loads(self.rfile.read(length))
            result = recommend(answers)
        except (ValueError, TypeError, json.JSONDecodeError) as exc:
            return self.send_json(422, {"detail": str(exc)})
        return self.send_json(200, result)

    def send_json(self, status, value):
        body = json.dumps(value, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def send_static(self, url_path):
        requested = "index.html" if url_path in ("", "/") else url_path.lstrip("/")
        candidate = (FRONTEND_ROOT / requested).resolve()
        if not candidate.is_relative_to(FRONTEND_ROOT.resolve()) or not candidate.is_file():
            return self.send_json(404, {"detail": "Page not found"})
        content_type = mimetypes.guess_type(candidate.name)[0] or "application/octet-stream"
        body = candidate.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8" if content_type.startswith("text/") or content_type in ("application/javascript", "application/json") else content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        # Requests contain only paths and status metadata; never log quiz answers.
        super().log_message(fmt, *args)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer(("127.0.0.1", port), SiteHandler)
    print(f"AI Career Predictor is running at http://127.0.0.1:{port}")
    print("Press Ctrl+C to stop the server.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server…")
    finally:
        server.server_close()
