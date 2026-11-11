# -*- coding: utf-8 -*-
import unittest
from kampus_rehberi import KampusRehberi, TercihDanismani

class TestKampusRehberi(unittest.TestCase):
    def setUp(self):
        self.rehber = KampusRehberi()

    def test_total_campuses(self):
        campuses = self.rehber.all()
        self.assertGreaterEqual(len(campuses), 250)

    def test_all_81_provinces_covered(self):
        cities = self.rehber.get_cities()
        self.assertEqual(len(cities), 81)

    def test_get_by_id(self):
        campus = self.rehber.get_by_id("06-Ankara/Cankaya/ODTU-Merkez-Kampusu")
        self.assertIsNotNone(campus)
        self.assertEqual(campus.plate, "06")
        self.assertIn("ODTÜ", campus.title)

    def test_search_by_city(self):
        results = self.rehber.search(city="35")
        self.assertGreater(len(results), 0)
        for r in results:
            self.assertEqual(r.plate, "35")

    def test_compare(self):
        res = self.rehber.compare(
            "06-Ankara/Cankaya/ODTU-Merkez-Kampusu",
            "34-Istanbul/Sariyer/ITU-Ayazaga-ve-Macka-Taskisla-Kampusleri"
        )
        self.assertIn("kampus_1", res)
        self.assertIn("kampus_2", res)

    def test_advisor_recommendations(self):
        advisor = TercihDanismani(self.rehber)
        recommendations = advisor.danis("Deniz kıyısında olan tıp veya mühendislik fakülteleri", top_k=3)
        self.assertEqual(len(recommendations), 3)
        self.assertGreater(recommendations[0]["skor"], 0)

if __name__ == '__main__':
    unittest.main()
