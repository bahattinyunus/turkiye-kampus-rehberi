# -*- coding: utf-8 -*-
import os
import json
from typing import List, Dict, Any, Optional

class Campus:
    def __init__(self, data: Dict[str, Any]):
        self.id = data.get("id", "")
        self.title = data.get("baslik", "")
        self.file_path = data.get("dosya_yolu", "")
        self.plate = data.get("plaka", "")
        self.city = data.get("il", "")
        self.district = data.get("ilce", "")
        self.type = data.get("universite_turu", "Devlet")
        self.rating = data.get("ogrenci_dostu_puani", "")
        self.last_updated = data.get("son_guncelleme", "")
        self.metrics = data.get("metrikler", {})
        self.pros = data.get("artilar", [])
        self.cons = data.get("eksiler", [])
        self.student_note = data.get("ogrenci_notu", "")
        self._raw = data

    def to_dict(self) -> Dict[str, Any]:
        return self._raw

    def __repr__(self) -> str:
        return f"<Campus: {self.title} ({self.city}/{self.district})>"


class KampusRehberi:
    def __init__(self, data_path: Optional[str] = None):
        if not data_path:
            # Look in standard locations: package dir, repo data dir
            pkg_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            candidate = os.path.join(pkg_root, "data", "kampusler.json")
            if os.path.exists(candidate):
                data_path = candidate
            else:
                data_path = "data/kampusler.json"
        
        self.data_path = data_path
        self._campuses: List[Campus] = []
        self._load()

    def _load(self):
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Veritabanı dosyası bulunamadı: {self.data_path}")
        with open(self.data_path, "r", encoding="utf-8") as f:
            raw_list = json.load(f)
            self._campuses = [Campus(item) for item in raw_list]

    def all(self) -> List[Campus]:
        """Tüm kampüsleri listeler."""
        return self._campuses

    def get_by_id(self, campus_id: str) -> Optional[Campus]:
        """ID veya dosya yoluna göre kampüs getirir."""
        norm_id = campus_id.replace("\\", "/").replace(".md", "")
        for c in self._campuses:
            if c.id == norm_id or c.file_path.replace(".md", "") == norm_id:
                return c
        return None

    def search(
        self,
        query: str = "",
        city: Optional[str] = None,
        district: Optional[str] = None,
        type_: Optional[str] = None,
        min_rating: Optional[float] = None
    ) -> List[Campus]:
        """Gelişmiş arama ve filtreleme motoru."""
        results = []
        q = query.lower().strip()
        c_filter = city.lower().strip() if city else None
        d_filter = district.lower().strip() if district else None
        t_filter = type_.lower().strip() if type_ else None

        for c in self._campuses:
            if c_filter:
                if c.plate != c_filter and c_filter not in c.city.lower():
                    continue
            if d_filter:
                if d_filter not in c.district.lower():
                    continue
            if t_filter:
                if t_filter not in c.type.lower():
                    continue

            if q:
                search_text = f"{c.title} {c.city} {c.district} {' '.join(c.pros)} {' '.join(c.cons)} {c.student_note}".lower()
                if q not in search_text:
                    continue

            results.append(c)

        return results

    def get_cities(self) -> List[Dict[str, Any]]:
        """81 ilin özet listesi ve kampüs sayıları."""
        cities_map: Dict[str, Dict[str, Any]] = {}
        for c in self._campuses:
            if c.plate not in cities_map:
                cities_map[c.plate] = {
                    "plaka": c.plate,
                    "il": c.city,
                    "kampus_sayisi": 0,
                    "kampusler": []
                }
            cities_map[c.plate]["kampus_sayisi"] += 1
            cities_map[c.plate]["kampusler"].append(c.title)

        return sorted(list(cities_map.values()), key=lambda x: x["plaka"])

    def compare(self, campus_id_1: str, campus_id_2: str) -> Dict[str, Any]:
        """İki kampüsü yan yana kıyaslar."""
        c1 = self.get_by_id(campus_id_1)
        c2 = self.get_by_id(campus_id_2)

        if not c1 or not c2:
            raise ValueError("Kıyaslanacak kampüslerden biri veya her ikisi bulunamadı.")

        return {
            "kampus_1": c1.to_dict(),
            "kampus_2": c2.to_dict(),
            "karsilastirma": {
                "sehirler": f"{c1.city} vs {c2.city}",
                "tur": f"{c1.type} vs {c2.type}",
                "puanlar": f"{c1.rating} vs {c2.rating}",
                "ortak_avantajlar": list(set(c1.pros).intersection(set(c2.pros)))
            }
        }

    def stats(self) -> Dict[str, Any]:
        """Veri tabanı istatistikleri."""
        total = len(self._campuses)
        cities = set(c.city for c in self._campuses)
        types = {}
        for c in self._campuses:
            types[c.type] = types.get(c.type, 0) + 1

        return {
            "toplam_kampus": total,
            "kapsanan_il": len(cities),
            "turler": types
        }
