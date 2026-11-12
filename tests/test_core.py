# -*- coding: utf-8 -*-
import unittest
import json
import os
from kampus_rehberi import KampusRehberi, Campus, TercihDanismani

class TestKampusRehberi(unittest.TestCase):
    def setUp(self):
        self.rehber = KampusRehberi()

    def test_total_campuses(self):
        campuses = self.rehber.all()
        self.assertGreaterEqual(len(campuses), 300)

    def test_all_81_provinces_covered(self):
        cities = self.rehber.get_cities()
        self.assertEqual(len(cities), 81)

    def test_get_by_id(self):
        campus = self.rehber.get_by_id("06-Ankara/Cankaya/ODTU-Merkez-Kampusu")
        self.assertIsNotNone(campus)
        self.assertEqual(campus.plate, "06")
        self.assertIn("ODTÜ", campus.title)
        self.assertGreaterEqual(campus.rating_num, 4.0)

    def test_search_by_city(self):
        results = self.rehber.search(city="35")
        self.assertGreater(len(results), 0)
        for r in results:
            self.assertEqual(r.plate, "35")

    def test_search_with_min_rating_and_sorting(self):
        results = self.rehber.search(min_rating=4.5, sort_by="rating_desc")
        self.assertGreater(len(results), 0)
        prev_rating = 5.0
        for r in results:
            self.assertGreaterEqual(r.rating_num, 4.5)
            self.assertLessEqual(r.rating_num, prev_rating)
            prev_rating = r.rating_num

    def test_get_random(self):
        c_single = self.rehber.get_random()
        self.assertIsInstance(c_single, Campus)
        c_multi = self.rehber.get_random(count=3)
        self.assertEqual(len(c_multi), 3)

    def test_get_top_rated(self):
        top5 = self.rehber.get_top_rated(n=5)
        self.assertEqual(len(top5), 5)
        self.assertGreaterEqual(top5[0].rating_num, top5[1].rating_num)

    def test_has_feature(self):
        odtu = self.rehber.get_by_id("06-Ankara/Cankaya/ODTU-Merkez-Kampusu")
        self.assertIsNotNone(odtu)
        self.assertTrue(odtu.has_feature("metro") or odtu.has_feature("ankara"))

    def test_compare(self):
        res = self.rehber.compare(
            "06-Ankara/Cankaya/ODTU-Merkez-Kampusu",
            "34-Istanbul/Sariyer/ITU-Ayazaga-ve-Macka-Taskisla-Kampusleri"
        )
        self.assertIn("kampus_1", res)
        self.assertIn("kampus_2", res)
        self.assertIn("karsilastirma", res)

    def test_export_formats(self):
        csv_out = self.rehber.export(format="csv")
        self.assertIn("Plaka,İl,İlçe", csv_out)
        self.assertIn("ODTÜ", csv_out)

        md_out = self.rehber.export(format="markdown")
        self.assertIn("| Plaka | İl |", md_out)

        json_out = self.rehber.export(format="json")
        loaded = json.loads(json_out)
        self.assertIsInstance(loaded, list)
        self.assertGreaterEqual(len(loaded), 300)

    def test_advisor_recommendations(self):
        advisor = TercihDanismani(self.rehber)
        recommendations = advisor.danis("Deniz kıyısında olan tıp veya mühendislik fakülteleri", top_k=3)
        self.assertEqual(len(recommendations), 3)
        self.assertGreater(recommendations[0]["skor"], 0)
        self.assertIn("uyum_yuzdesi", recommendations[0])

if __name__ == '__main__':
    unittest.main()
