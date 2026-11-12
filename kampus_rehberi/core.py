# -*- coding: utf-8 -*-
"""
Türkiye Kampüs Rehberi - Çekirdek Python SDK Modülü
Tüm üniversite kampüslerinin taranması, filtrelenmesi, kıyaslanması
ve analiz edilmesi için kapsamlı veri erişim katmanı.
"""

import os
import json
import random
import csv
import io
from typing import List, Dict, Any, Optional, Union

class Campus:
    """Tek bir üniversite kampüsü veya yerleşkesini temsil eden nesne."""

    def __init__(self, data: Dict[str, Any]):
        self.id: str = data.get("id", "")
        self.title: str = data.get("baslik", "")
        self.file_path: str = data.get("dosya_yolu", "")
        self.plate: str = data.get("plaka", "")
        self.city: str = data.get("il", "")
        self.district: str = data.get("ilce", "")
        self.type: str = data.get("universite_turu", "Devlet")
        self.rating: str = data.get("ogrenci_dostu_puani", "⭐️⭐️⭐️⭐️☆ (4.0/5)")
        self.rating_num: float = float(data.get("puan_sayisal", 4.0))
        self.last_updated: str = data.get("son_guncelleme", "Kasım 2026")
        self.metrics: Dict[str, Dict[str, str]] = data.get("metrikler", {})
        self.pros: List[str] = data.get("artilar", [])
        self.cons: List[str] = data.get("eksiler", [])
        self.tips: List[str] = data.get("altin_tavsiyeler", [])
        self.student_note: str = data.get("ogrenci_notu", "")
        self.summaries: Dict[str, str] = data.get("bolum_ozetleri", {})
        self._raw = data

    def has_feature(self, keyword: str) -> bool:
        """Kampüste aranan özelliğin (metro, yurt, deniz, 7/24, fiber vb.) bulunup bulunmadığını kontrol eder."""
        kw = keyword.lower()
        search_blob = f"{self.title} {self.city} {self.district} {' '.join(self.pros)} {' '.join(self.cons)} {' '.join(self.tips)} {self.student_note}".lower()
        for k, v in self.metrics.items():
            search_blob += f" {k} {v.get('degerlendirme', '')} {v.get('detay', '')}".lower()
        return kw in search_blob

    def to_dict(self) -> Dict[str, Any]:
        """Kampüs verisini sözlük formatında döndürür."""
        return self._raw

    def to_markdown(self) -> str:
        """Kampüsün özet Markdown kartını oluşturur."""
        md = [
            f"### 🏛️ {self.title}",
            f"- **Konum:** {self.plate} - {self.city} / {self.district}",
            f"- **Üniversite Türü:** {self.type}",
            f"- **Öğrenci Dostu Puanı:** {self.rating}",
            f"- **Rehber Dosyası:** `{self.file_path}`",
            ""
        ]
        if self.student_note:
            md.append(f"> 💬 *Öğrenci Notu:* \"{self.student_note}\"\n")
        if self.pros:
            md.append("**Öne Çıkan Artıları:**")
            for pro in self.pros[:3]:
                md.append(f"- ✅ {pro}")
            md.append("")
        if self.cons:
            md.append("**Bilinmesi Gereken Zorlukları:**")
            for con in self.cons[:3]:
                md.append(f"- ❌ {con}")
            md.append("")
        return "\n".join(md)

    def __repr__(self) -> str:
        return f"<Campus: {self.title} ({self.city}/{self.district}) - {self.rating_num}/5>"


class KampusRehberi:
    """Türkiye Kampüs Rehberi ana yönetim ve arama motoru."""

    def __init__(self, data_path: Optional[str] = None):
        if not data_path:
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

    def count(self) -> int:
        """Kayıtlı toplam kampüs sayısı."""
        return len(self._campuses)

    def get_by_id(self, campus_id: str) -> Optional[Campus]:
        """ID veya dosya yoluna göre kampüs getirir."""
        norm_id = campus_id.replace("\\", "/").replace(".md", "").strip("/")
        if norm_id.startswith("iller/"):
            clean_id = norm_id[6:]
        else:
            clean_id = norm_id

        for c in self._campuses:
            c_norm = c.id.replace("\\", "/").replace(".md", "").strip("/")
            c_clean = c_norm[6:] if c_norm.startswith("iller/") else c_norm
            
            if c_norm == norm_id or c_clean == clean_id or c.file_path.replace(".md", "") == norm_id:
                return c
        return None

    def search(
        self,
        query: str = "",
        city: Optional[str] = None,
        district: Optional[str] = None,
        type_: Optional[str] = None,
        min_rating: Optional[float] = None,
        sort_by: str = "default"
    ) -> List[Campus]:
        """
        Gelişmiş arama ve filtreleme motoru.
        
        sort_by seçenekleri:
          - 'default': Plaka ve isme göre
          - 'rating_desc': En yüksek puandan düşüğe
          - 'rating_asc': En düşük puandan yükseğe
          - 'title_asc': Alfabetik
          - 'city_asc': Şehir adına göre
        """
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
            if min_rating is not None:
                if c.rating_num < min_rating:
                    continue

            if q:
                search_text = f"{c.title} {c.city} {c.district} {' '.join(c.pros)} {' '.join(c.cons)} {' '.join(c.tips)} {c.student_note}".lower()
                if q not in search_text:
                    continue

            results.append(c)

        # Sıralama
        if sort_by == "rating_desc":
            results.sort(key=lambda x: x.rating_num, reverse=True)
        elif sort_by == "rating_asc":
            results.sort(key=lambda x: x.rating_num)
        elif sort_by == "title_asc":
            results.sort(key=lambda x: x.title)
        elif sort_by == "city_asc":
            results.sort(key=lambda x: (x.city, x.title))

        return results

    def get_random(self, count: int = 1) -> Union[Campus, List[Campus]]:
        """Rastgele bir veya birden fazla kampüs seçer."""
        if not self._campuses:
            raise ValueError("Kayıtlı kampüs bulunamadı.")
        if count == 1:
            return random.choice(self._campuses)
        return random.sample(self._campuses, min(count, len(self._campuses)))

    def get_top_rated(self, n: int = 10, city: Optional[str] = None) -> List[Campus]:
        """En yüksek öğrenci dostu puanına sahip n kampüsü listeler."""
        filtered = self.search(city=city) if city else self._campuses
        sorted_campuses = sorted(filtered, key=lambda x: x.rating_num, reverse=True)
        return sorted_campuses[:n]

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
                "puanlar": f"{c1.rating} ({c1.rating_num}) vs {c2.rating} ({c2.rating_num})",
                "ortak_avantajlar": list(set(c1.pros).intersection(set(c2.pros))),
                "farkli_yonler": {
                    f"{c1.title}_artilari": c1.pros,
                    f"{c2.title}_artilari": c2.pros
                }
            }
        }

    def stats(self) -> Dict[str, Any]:
        """Veri tabanı istatistikleri ve analizleri."""
        total = len(self._campuses)
        cities = set(c.city for c in self._campuses)
        types: Dict[str, int] = {}
        total_rating = 0.0

        for c in self._campuses:
            types[c.type] = types.get(c.type, 0) + 1
            total_rating += c.rating_num

        avg_rating = round(total_rating / total, 2) if total > 0 else 0.0

        return {
            "toplam_kampus": total,
            "kapsanan_il": len(cities),
            "ortalama_puan": avg_rating,
            "turler": types
        }

    def export(self, format: str = "json", output_path: Optional[str] = None) -> str:
        """Kampüs listesini JSON, CSV veya Markdown formatında dışa aktarır."""
        format_lower = format.lower()

        if format_lower == "json":
            data = [c.to_dict() for c in self._campuses]
            content = json.dumps(data, ensure_ascii=False, indent=2)
        elif format_lower == "csv":
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["Plaka", "İl", "İlçe", "Üniversite/Kampüs", "Tür", "Puan", "Dosya Yolu"])
            for c in self._campuses:
                writer.writerow([c.plate, c.city, c.district, c.title, c.type, c.rating_num, c.file_path])
            content = output.getvalue()
        elif format_lower in ["md", "markdown"]:
            lines = ["# 🎓 Türkiye Üniversite Kampüsleri Listesi\n\n"]
            lines.append("| Plaka | İl | İlçe | Üniversite & Kampüs | Tür | Puan |\n")
            lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |\n")
            for c in self._campuses:
                lines.append(f"| {c.plate} | {c.city} | {c.district} | [{c.title}]({c.file_path}) | {c.type} | {c.rating_num} |\n")
            content = "".join(lines)
        else:
            raise ValueError(f"Desteklenmeyen format: {format}. 'json', 'csv' veya 'markdown' kullanın.")

        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"✓ Veriler başarıyla kaydedildi: {output_path}"

        return content
