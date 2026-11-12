# -*- coding: utf-8 -*-
"""
Türkiye Kampüs Rehberi - YKS Tercih Listesi Simülatörü ve Yönetim Motoru
Adayların 24 tercihe kadar kişisel üniversite tercih listesi hazırlamasını,
sıralamasını, analiz etmesini ve dışa aktarmasını sağlar.
"""

from typing import List, Dict, Any, Optional
from .core import KampusRehberi, Campus

class TercihListesi:
    """YKS Adayı Kişisel Tercih Sepeti ve Sıralama Motoru."""

    def __init__(self, rehber: Optional[KampusRehberi] = None, aday_adi: str = "Aday"):
        self.rehber = rehber or KampusRehberi()
        self.aday_adi = aday_adi
        self.tercihler: List[Campus] = []

    def ekle(self, campus_id: str) -> bool:
        """Tercih listesine kampüs ekler (Maks 24 tercih)."""
        if len(self.tercihler) >= 24:
            raise ValueError("YKS Tercih kılavuzu gereği en fazla 24 tercih yapabilirsiniz.")
        campus = self.rehber.get_by_id(campus_id)
        if not campus:
            raise ValueError(f"Kampüs bulunamadı: {campus_id}")
        if campus in self.tercihler:
            return False
        self.tercihler.append(campus)
        return True

    def cikar(self, sira_no: int) -> bool:
        """Belirtilen sıra numarasındaki tercihi listeden siler."""
        idx = sira_no - 1
        if 0 <= idx < len(self.tercihler):
            self.tercihler.pop(idx)
            return True
        return False

    def yer_degistir(self, sira1: int, sira2: int):
        """İki tercihin sırasını takas eder."""
        idx1, idx2 = sira1 - 1, sira2 - 1
        if 0 <= idx1 < len(self.tercihler) and 0 <= idx2 < len(self.tercihler):
            self.tercihler[idx1], self.tercihler[idx2] = self.tercihler[idx2], self.tercihler[idx1]

    def analiz(self) -> Dict[str, Any]:
        """Hazırlanan tercih listesinin coğrafi, tür ve puan dağılım analizini çıkarır."""
        if not self.tercihler:
            return {"toplam_tercih": 0, "mesaj": "Listeniz henüz boş."}

        sehirler: Dict[str, int] = {}
        turler: Dict[str, int] = {}
        toplam_puan = 0.0

        for c in self.tercihler:
            sehirler[c.city] = sehirler.get(c.city, 0) + 1
            turler[c.type] = turler.get(c.type, 0) + 1
            toplam_puan += c.rating_num

        ortalama_puan = round(toplam_puan / len(self.tercihler), 2)

        return {
            "aday": self.aday_adi,
            "toplam_tercih": len(self.tercihler),
            "kalan_hak": 24 - len(self.tercihler),
            "ortalama_ogrenci_puani": ortalama_puan,
            "sehir_dagilimi": sehirler,
            "tur_dagilimi": turler
        }

    def to_markdown(self) -> str:
        """Tercih listesini resmi şablon formatında Markdown tablosuna dönüştürür."""
        lines = [
            f"# 🎓 YKS 2026 Tercih Listesi Taslağı",
            f"> **Aday:** {self.aday_adi} | **Toplam Tercih:** {len(self.tercihler)} / 24\n",
            "| Sıra | İl / İlçe | Üniversite & Kampüs | Tür | Öğrenci Puanı |",
            "| :--- | :--- | :--- | :--- | :--- |"
        ]
        for i, c in enumerate(self.tercihler, 1):
            lines.append(f"| {i:02d} | {c.plate} - {c.city} / {c.district} | {c.title} | {c.type} | ⭐ {c.rating_num}/5.0 |")

        analysis = self.analiz()
        lines.append(f"\n### 📊 Tercih Sepeti Özeti")
        lines.append(f"- **Ortalama Öğrenci Puanı:** {analysis['ortalama_ogrenci_puani']}/5.0")
        lines.append(f"- **Kapsanan Şehir Sayısı:** {len(analysis['sehir_dagilimi'])}")
        return "\n".join(lines)
