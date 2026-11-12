# -*- coding: utf-8 -*-
import unittest
import io
from contextlib import redirect_stdout
from kampus_rehberi.core import KampusRehberi
from kampus_rehberi.cli import (
    cmd_stats, cmd_search, cmd_city, cmd_top, cmd_random, cmd_compare, cmd_ask, cmd_budget
)

class DummyArgs:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

class TestCLI(unittest.TestCase):
    def setUp(self):
        self.rehber = KampusRehberi()

    def test_cmd_stats(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            cmd_stats(self.rehber, DummyArgs())
        output = buf.getvalue()
        self.assertIn("KAMPÜS REHBERİ", output.upper())
        self.assertIn("81 İL", output.upper())

    def test_cmd_search(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            cmd_search(self.rehber, DummyArgs(query="ODTÜ", city=None, type=None, min_rating=None, sort="default", limit=5))
        output = buf.getvalue()
        self.assertIn("ODTÜ", output)

    def test_cmd_city(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            cmd_city(self.rehber, DummyArgs(city="06"))
        output = buf.getvalue()
        self.assertIn("Ankara Kampüsleri", output)

    def test_cmd_top(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            cmd_top(self.rehber, DummyArgs(n=5, city=None))
        output = buf.getvalue()
        self.assertIn("EN YÜKSEK PUANLI", output)

    def test_cmd_random(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            cmd_random(self.rehber, DummyArgs())
        output = buf.getvalue()
        self.assertIn("RASTGELE KAMPÜS KEŞFİ", output)

    def test_cmd_compare(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            cmd_compare(self.rehber, DummyArgs(
                campus1="06-Ankara/Cankaya/ODTU-Merkez-Kampusu",
                campus2="34-Istanbul/Sariyer/ITU-Ayazaga-ve-Macka-Taskisla-Kampusleri"
            ))
        output = buf.getvalue()
        self.assertIn("KARŞILAŞTIRMA", output)

    def test_cmd_ask(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            cmd_ask(self.rehber, DummyArgs(question="Metro ve doğa", top_k=2))
        output = buf.getvalue()
        self.assertIn("AKILLI TERCİH DANIŞMANI", output)

    def test_cmd_budget(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            cmd_budget(self.rehber, DummyArgs(city="Ankara", housing="kyk", meals=1, lifestyle="moderate"))
        output = buf.getvalue()
        self.assertIn("YAŞAM MALİYETİ RAPORU", output)
        self.assertIn("TAHMİNİ TOPLAM AYLIK", output)

if __name__ == '__main__':
    unittest.main()
