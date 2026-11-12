# -*- coding: utf-8 -*-
import unittest
from kampus_rehberi import KampusRehberi, CostCalculator, TercihListesi, PROVINCE_COORDINATES, get_province_geo

class TestBudgetAndYKS(unittest.TestCase):
    def setUp(self):
        self.rehber = KampusRehberi()
        self.calc = CostCalculator(self.rehber)

    def test_budget_calculation(self):
        res = self.calc.calculate_monthly("Eskişehir", housing_type="kyk", meals_on_campus=1, lifestyle="budget")
        self.assertEqual(res["sehir"], "Eskişehir")
        self.assertGreater(res["tahmini_aylik_toplam_tl"], 0)
        self.assertIn("barinma_kira", res["kalemler"])

    def test_budget_tier1_vs_tier3(self):
        res_ist = self.calc.calculate_monthly("İstanbul", housing_type="studio")
        res_esk = self.calc.calculate_monthly("Erzincan", housing_type="studio")
        self.assertGreater(res_ist["tahmini_aylik_toplam_tl"], res_esk["tahmini_aylik_toplam_tl"])

    def test_yks_preference_list(self):
        yks = TercihListesi(self.rehber, aday_adi="Bahattin")
        success1 = yks.ekle("06-Ankara/Cankaya/ODTU-Merkez-Kampusu")
        success2 = yks.ekle("34-Istanbul/Sariyer/ITU-Ayazaga-ve-Macka-Taskisla-Kampusleri")
        self.assertTrue(success1)
        self.assertTrue(success2)

        analiz = yks.analiz()
        self.assertEqual(analiz["toplam_tercih"], 2)
        self.assertEqual(analiz["kalan_hak"], 22)
        self.assertGreaterEqual(analiz["ortalama_ogrenci_puani"], 4.0)

        md = yks.to_markdown()
        self.assertIn("YKS 2026 Tercih Listesi", md)
        self.assertIn("ODTÜ", md)

        # Çıkarma
        removed = yks.cikar(1)
        self.assertTrue(removed)
        self.assertEqual(len(yks.tercihler), 1)

    def test_geo_data(self):
        self.assertEqual(len(PROVINCE_COORDINATES), 81)
        ankara = get_province_geo("06")
        self.assertEqual(ankara["il"], "Ankara")
        self.assertAlmostEqual(ankara["lat"], 39.9334, places=2)

if __name__ == '__main__':
    unittest.main()
