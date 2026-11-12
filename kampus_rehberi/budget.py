# -*- coding: utf-8 -*-
"""
Türkiye Kampüs Rehberi - Öğrenci Yaşam Maliyeti & Bütçe Hesaplama Motoru
Şehirlere ve yerleşkelere göre aylık tahmini barınma, beslenme, ulaşım
ve genel yaşam giderlerini hesaplar.
"""

from typing import Dict, Any, Optional
from .core import KampusRehberi

# 2026 Türkiye Şehir Kategori Tabanlı Öğrenci Yaşam Maliyeti Katsayıları
TIER_1_CITIES = ["İstanbul"]
TIER_2_CITIES = ["Ankara", "İzmir", "Antalya", "Muğla", "Bursa", "Eskişehir", "Kocaeli"]
TIER_3_CITIES = ["Adana", "Gaziantep", "Konya", "Trabzon", "Samsun", "Aydın", "Çanakkale", "Sakarya", "Mersin", "Denizli", "Kayseri"]

class CostCalculator:
    """Öğrenci aylık bütçe ve yaşam maliyeti simülatörü."""

    def __init__(self, rehber: Optional[KampusRehberi] = None):
        self.rehber = rehber or KampusRehberi()

    def calculate_monthly(
        self,
        city_or_plate: str,
        housing_type: str = "kyk",  # "kyk", "shared_flat", "studio", "private_dorm"
        meals_on_campus: int = 1,   # Günde kaç öğün yemekhane (0, 1, 2)
        lifestyle: str = "moderate" # "budget", "moderate", "comfortable"
    ) -> Dict[str, Any]:
        """Aylık tahmini öğrenci giderlerini kalem kalem hesaplar."""
        # Şehir tespiti
        campus_sample = self.rehber.search(city=city_or_plate)
        city_name = campus_sample[0].city if campus_sample else city_or_plate.capitalize()

        # Taban kira belirleme
        if city_name in TIER_1_CITIES:
            base_rent_1plus1 = 22000
            transport_pass = 250
            social_base = 4000
        elif city_name in TIER_2_CITIES:
            base_rent_1plus1 = 15000
            transport_pass = 220
            social_base = 3000
        elif city_name in TIER_3_CITIES:
            base_rent_1plus1 = 11000
            transport_pass = 180
            social_base = 2200
        else:
            base_rent_1plus1 = 8000
            transport_pass = 140
            social_base = 1600

        # Barınma türüne göre kira payı
        if housing_type == "kyk":
            housing_cost = 850  # KYK ortalama aylık yurt ücreti (kahvaltı + akşam dahil)
            bills_cost = 0
        elif housing_type == "shared_flat":
            housing_cost = int(base_rent_1plus1 * 0.55) # 2-3 kişi paylaşımlı
            bills_cost = 1200
        elif housing_type == "studio":
            housing_cost = base_rent_1plus1
            bills_cost = 1800
        elif housing_type == "private_dorm":
            housing_cost = int(base_rent_1plus1 * 0.85)
            bills_cost = 0
        else:
            housing_cost = int(base_rent_1plus1 * 0.55)
            bills_cost = 1200

        # Beslenme maliyeti
        campus_meal_price = 30 # ortalama yemekhane menü fiyatı
        monthly_campus_meals = meals_on_campus * 22 * campus_meal_price
        
        if housing_type == "kyk":
            extra_food = 1500 # KYK akşam ve kahvaltıyı karşılıyor, ara öğün/haftasonu
        elif lifestyle == "budget":
            extra_food = 2500
        elif lifestyle == "moderate":
            extra_food = 4000
        else:
            extra_food = 6500

        food_cost = monthly_campus_meals + extra_food

        # Sosyal harcama
        lifestyle_multiplier = {"budget": 0.6, "moderate": 1.0, "comfortable": 1.7}.get(lifestyle, 1.0)
        social_cost = int(social_base * lifestyle_multiplier)

        total_monthly = housing_cost + bills_cost + food_cost + transport_pass + social_cost

        return {
            "sehir": city_name,
            "barinma_turu": housing_type,
            "yasam_tarzi": lifestyle,
            "tahmini_aylik_toplam_tl": total_monthly,
            "kalemler": {
                "barinma_kira": housing_cost,
                "faturalar_aidat": bills_cost,
                "yemekhane_ve_gida": food_cost,
                "ulasim_abonman": transport_pass,
                "sosyal_ve_kisisel": social_cost
            },
            "ogrenci_butce_yorumu": self._get_budget_comment(total_monthly, city_name)
        }

    def _get_budget_comment(self, total: int, city: str) -> str:
        if total < 6000:
            return f"{city}, Türkiye standartlarında öğrenci için oldukça ekonomik ve bütçe dostu bir şehirdir."
        elif total < 12000:
            return f"{city}, dengeli bir bütçeyle rahatça öğrencilik yapılabilecek ortalama maliyetli bir ildir."
        elif total < 18000:
            return f"{city}, büyükşehir avantajlarına sahip ancak kira ve sosyal harcamalar için planlama gerektiren bir şehirdir."
        else:
            return f"{city}, yaşam maliyeti yüksek bir metropoldür; burs, KYK yurdu veya ev arkadaşlığı kritik önem taşır."
