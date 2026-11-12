# -*- coding: utf-8 -*-
import unittest
import threading
import time
import urllib.request
import json
from http.server import HTTPServer
from kampus_rehberi.api import KampusAPIHandler
from kampus_rehberi.core import KampusRehberi

class TestAPI(unittest.TestCase):
    server = None
    server_thread = None
    port = 8765

    @classmethod
    def setUpClass(cls):
        rehber = KampusRehberi()
        KampusAPIHandler.rehber = rehber
        cls.server = HTTPServer(("127.0.0.1", cls.port), KampusAPIHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()
        time.sleep(0.1)

    @classmethod
    def tearDownClass(cls):
        if cls.server:
            cls.server.shutdown()
            cls.server.server_close()

    def test_api_stats(self):
        url = f"http://127.0.0.1:{self.port}/api/stats"
        with urllib.request.urlopen(url) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode('utf-8'))
            self.assertIn("toplam_kampus", data)
            self.assertGreaterEqual(data["toplam_kampus"], 300)

    def test_api_cities(self):
        url = f"http://127.0.0.1:{self.port}/api/cities"
        with urllib.request.urlopen(url) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode('utf-8'))
            self.assertEqual(len(data), 81)

    def test_api_coords(self):
        url = f"http://127.0.0.1:{self.port}/api/coords"
        with urllib.request.urlopen(url) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode('utf-8'))
            self.assertEqual(len(data), 81)
            self.assertIn("06", data)

    def test_api_budget(self):
        url = f"http://127.0.0.1:{self.port}/api/budget?city=Ankara&housing=kyk"
        with urllib.request.urlopen(url) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode('utf-8'))
            self.assertIn("tahmini_aylik_toplam_tl", data)
            self.assertGreater(data["tahmini_aylik_toplam_tl"], 0)

    def test_api_campuses_search(self):
        url = f"http://127.0.0.1:{self.port}/api/campuses?city=Ankara&min_rating=4.5"
        with urllib.request.urlopen(url) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode('utf-8'))
            self.assertIn("kampusler", data)
            self.assertGreater(len(data["kampusler"]), 0)

    def test_api_advisor(self):
        url = f"http://127.0.0.1:{self.port}/api/advisor?q=metro+ve+m%C3%BChendislik&top_k=3"
        with urllib.request.urlopen(url) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode('utf-8'))
            self.assertIn("oneriler", data)
            self.assertEqual(len(data["oneriler"]), 3)

    def test_api_random(self):
        url = f"http://127.0.0.1:{self.port}/api/random"
        with urllib.request.urlopen(url) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode('utf-8'))
            self.assertIn("baslik", data)

if __name__ == '__main__':
    unittest.main()
