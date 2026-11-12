# -*- coding: utf-8 -*-
"""
Türkiye Kampüs Rehberi - Akıllı Tercih Danışmanı & Öneri Motoru
Öğrencilerin doğal dildeki sorularını, istek ve önceliklerini analiz ederek
en uygun üniversite ve kampüsleri puanlayıp tavsiye eder.
"""

import re
from typing import List, Dict, Any, Optional
from .core import KampusRehberi, Campus

class TercihDanismani:
    """Doğal dilde tercih danışmanı ve akıllı öneri motoru."""

    def __init__(self, rehber: KampusRehberi):
        self.rehber = rehber

    def danis(self, soru: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Kullanıcının tercih sorusunu analiz ederek en uyumlu kampüsleri skorlar.
        """
        soru_lower = soru.lower()
        campuses = self.rehber.all()
        scored: List[tuple] = []

        keywords_weights = {
            # Ulaşım
            "metro": ("metro", 5, "🚇 Metro Bağlantısı"),
            "metrobüs": ("metrobüs", 5, "🚍 Metrobüs Erişimi"),
            "tramvay": ("tramvay", 4, "🚊 Tramvay Hattı"),
            "ulaşım": ("ulaşım", 2, "🚌 Kolay Ulaşım"),
            "otobüs": ("otobüs", 2, "🚌 Toplu Taşıma"),
            "otostop": ("otostop", 3, "👍 Otostop Kültürü"),
            
            # Coğrafi / Konum
            "deniz": ("deniz", 5, "🌊 Deniz / Sahil Yakınlığı"),
            "sahil": ("sahil", 5, "🏖️ Sahil Şeridi"),
            "göl": ("göl", 4, "🌅 Göl Manzarası"),
            "doğa": ("doğa", 4, "🌲 Doğa ile İç İçe"),
            "yeşil": ("yeşil", 3, "🌳 Yeşil Kampüs"),
            "orman": ("orman", 4, "🌲 Orman Havası"),
            "merkez": ("merkez", 3, "🏙️ Şehir Merkezinde"),
            
            # Barınma & Yaşam Maliyeti
            "kyk": ("kyk", 5, "🏠 Kampüs İçi / Yakın KYK"),
            "yurt": ("yurt", 4, "🛏️ Zengin Yurt İmkanları"),
            "ucuz": ("uygun", 4, "💰 Uygun Yaşam Maliyeti"),
            "uygun": ("uygun", 3, "💸 Ekonomik Yaşam"),
            "kira": ("kira", 3, "🏘️ Öğrenci Evi Fırsatları"),
            "ekonomik": ("ekonomik", 3, "💳 Bütçe Dostu"),
            
            # Akademik & İmkânlar
            "kütüphane": ("kütüphane", 4, "📚 Zengin Kütüphane"),
            "7/24": ("7/24", 5, "🌙 7/24 Açık Kütüphane/Çalışma"),
            "teknik": ("teknik", 4, "⚙️ Teknik Üniversite / Mühendislik"),
            "mühendislik": ("mühendislik", 5, "💻 Güçlü Mühendislik Kadrosu"),
            "tıp": ("tıp", 5, "🩺 Üniversite Hastanesi / Tıp Fakültesi"),
            "hukuk": ("hukuk", 5, "⚖️ Köklü Hukuk Eğitimi"),
            "mimarlık": ("mimarlık", 4, "📐 Tasarım ve Mimarlık"),
            "teknofest": ("teknofest", 4, "🚀 TEKNOFEST ve Ar-Ge Takımları"),
            "laboratuvar": ("laboratuvar", 3, "🔬 Donanımlı Laboratuvar"),
            "eduroam": ("fiber", 3, "🌐 Hızlı İnternet & Eduroam"),
            "yemekhane": ("yemekhane", 3, "🍽️ Kaliteli / Uygun Yemekhane"),
            "sosyal": ("sosyal", 3, "🎉 Aktif Kulüp ve Sosyal Yaşam")
        }

        # Şehir veya plaka belirtilmiş mi?
        target_city = None
        target_plate = None
        for c in campuses:
            if c.city.lower() in soru_lower:
                target_city = c.city.lower()
                break
            if re.search(rf'\b{c.plate}\b', soru_lower):
                target_plate = c.plate
                break

        # Üniversite türü belirtilmiş mi?
        target_type = None
        if "devlet" in soru_lower:
            target_type = "devlet"
        elif "vakıf" in soru_lower or "özel" in soru_lower:
            target_type = "vakıf"

        for c in campuses:
            score = 0.0
            matched_reasons = []

            # Şehir eşleşmesi ekstra puan
            if target_city and c.city.lower() == target_city:
                score += 15.0
                matched_reasons.append(f"📍 İl Tercihi: {c.city}")
            elif target_plate and c.plate == target_plate:
                score += 15.0
                matched_reasons.append(f"📍 İl Tercihi: {c.city}")

            # Tür eşleşmesi
            if target_type:
                if target_type in c.type.lower():
                    score += 5.0
                    matched_reasons.append(f"🏛️ Tür: {c.type}")
                else:
                    # İstenmeyen tür ise skordan düşür
                    score -= 10.0

            # İçerik taraması
            text_blob = f"{c.title} {c.city} {c.district} {c.type} {' '.join(c.pros)} {' '.join(c.cons)} {' '.join(c.tips)} {c.student_note}".lower()
            for metric_k, metric_v in c.metrics.items():
                text_blob += f" {metric_k} {metric_v.get('degerlendirme', '')} {metric_v.get('detay', '')}".lower()

            for key, (term, weight, label) in keywords_weights.items():
                if key in soru_lower:
                    if term in text_blob:
                        score += weight
                        matched_reasons.append(label)

            # Kampüsün genel öğrenci puanı bonusu
            score += (c.rating_num - 3.0) * 2.0

            if score > 0:
                scored.append((score, c, matched_reasons))

        scored.sort(key=lambda x: x[0], reverse=True)

        results = []
        max_score = scored[0][0] if scored else 1.0

        for score, campus, matched_reasons in scored[:top_k]:
            match_percentage = min(100, int((score / max(max_score, 10.0)) * 100))
            results.append({
                "skor": round(score, 1),
                "uyum_yuzdesi": f"%{match_percentage}",
                "kampus": campus.title,
                "kampus_id": campus.id,
                "sehir": f"{campus.plate} - {campus.city} / {campus.district}",
                "tur": campus.type,
                "puan": campus.rating,
                "puan_sayisal": campus.rating_num,
                "dosya": campus.file_path,
                "ogrenci_notu": campus.student_note,
                "one_cikan_artilar": campus.pros[:3],
                "altin_tavsiyeler": campus.tips[:2],
                "eslesen_kriterler": list(dict.fromkeys(matched_reasons))
            })

        return results
