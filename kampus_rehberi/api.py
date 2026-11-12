# -*- coding: utf-8 -*-
"""
Türkiye Kampüs Rehberi - REST API Sunucusu
Harici kütüphane bağımlılığı gerektirmeyen, hafif, CORS uyumlu JSON REST API.
"""

import json
import urllib.parse
from http.server import SimpleHTTPRequestHandler, HTTPServer
from typing import Optional
from .core import KampusRehberi
from .advisor import TercihDanismani

class KampusAPIHandler(SimpleHTTPRequestHandler):
    rehber: Optional[KampusRehberi] = None
    advisor: Optional[TercihDanismani] = None

    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Requested-With")

    def _send_json_response(self, data, status_code=200):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        qs = urllib.parse.parse_qs(parsed.query)

        if self.rehber is None:
            self.rehber = KampusRehberi()
        if self.advisor is None:
            self.advisor = TercihDanismani(self.rehber)

        # /api/stats
        if path == "/api/stats":
            self._send_json_response(self.rehber.stats())
            return

        # /api/cities
        if path == "/api/cities":
            self._send_json_response(self.rehber.get_cities())
            return

        # /api/random
        if path == "/api/random":
            count = int(qs.get("count", [1])[0])
            res = self.rehber.get_random(count=count)
            if isinstance(res, list):
                self._send_json_response([c.to_dict() for c in res])
            else:
                self._send_json_response(res.to_dict())
            return

        # /api/advisor
        if path == "/api/advisor":
            q = qs.get("q", [""])[0]
            top_k = int(qs.get("top_k", [5])[0])
            if not q:
                self._send_json_response({"error": "Lütfen 'q' parametresi ile bir soru girin."}, 400)
                return
            results = self.advisor.danis(q, top_k=top_k)
            self._send_json_response({"soru": q, "oneriler": results})
            return

        # /api/compare
        if path == "/api/compare":
            c1 = qs.get("c1", [""])[0]
            c2 = qs.get("c2", [""])[0]
            if not c1 or not c2:
                self._send_json_response({"error": "Lütfen c1 ve c2 parametrelerini girin."}, 400)
                return
            try:
                res = self.rehber.compare(c1, c2)
                self._send_json_response(res)
            except Exception as e:
                self._send_json_response({"error": str(e)}, 404)
            return

        # /api/campuses/{id} or /api/campuses
        if path.startswith("/api/campuses"):
            sub_id = path[len("/api/campuses"):].strip("/")
            if sub_id:
                campus = self.rehber.get_by_id(sub_id)
                if campus:
                    self._send_json_response(campus.to_dict())
                else:
                    self._send_json_response({"error": f"Kampüs bulunamadı: {sub_id}"}, 404)
                return

            # List & search
            q = qs.get("q", [""])[0]
            city = qs.get("city", [None])[0]
            type_ = qs.get("type", [None])[0]
            sort_by = qs.get("sort_by", ["default"])[0]
            min_rating_str = qs.get("min_rating", [None])[0]
            min_rating = float(min_rating_str) if min_rating_str else None
            limit_str = qs.get("limit", [None])[0]
            limit = int(limit_str) if limit_str else None

            results = self.rehber.search(
                query=q,
                city=city,
                type_=type_,
                min_rating=min_rating,
                sort_by=sort_by
            )
            if limit:
                results = results[:limit]

            self._send_json_response({
                "toplam": len(results),
                "kampusler": [c.to_dict() for c in results]
            })
            return

        # If static file requested from web portal
        super().do_GET()


def run_api_server(port: int = 8000, rehber: Optional[KampusRehberi] = None):
    """API ve web sunucusunu başlatır."""
    if rehber:
        KampusAPIHandler.rehber = rehber
        KampusAPIHandler.advisor = TercihDanismani(rehber)

    server_address = ("", port)
    httpd = HTTPServer(server_address, KampusAPIHandler)
    print(f"🚀 Türkiye Kampüs Rehberi REST API & Web Sunucusu çalışıyor: http://localhost:{port}")
    print(f"📡 API Endpoints:")
    print(f"   • http://localhost:{port}/api/stats")
    print(f"   • http://localhost:{port}/api/cities")
    print(f"   • http://localhost:{port}/api/campuses?city=Ankara&min_rating=4.5")
    print(f"   • http://localhost:{port}/api/advisor?q=Deniz+ve+t%C4%B1p")
    print(f"   • http://localhost:{port}/api/random")
    print(f"   • http://localhost:{port}/web/index.html (Web Portalı)\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nSunucu durduruldu.")
