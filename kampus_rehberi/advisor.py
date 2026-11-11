# -*- coding: utf-8 -*-
import re
from typing import List, Dict, Any
from .core import KampusRehberi, Campus

class TercihDanismani:
    """Doğal dilde tercih danışmanı ve akıllı öneri motoru."""

    def __init__(self, rehber: KampusRehberi):
        self.rehber = rehber

    def danis(self, soru: str, top_k: int = 5) -> List[Dict[str, Any]]:
        soru_lower = soru.lower()
        campuses = self.rehber.all()
        scored: List[tuple] = []

        keywords_weights = {
            "metro": ("metro", 4),
            "deniz": ("deniz", 4),
            "sahil": ("sahil", 4),
            "kyk": ("kyk", 3),
            "yurt": ("yurt", 3),
            "kütüphane": ("kütüphane", 3),
            "7/24": ("7/24", 4),
            "ucuz": ("uygun", 3),
            "kira": ("kira", 2),
            "tıp": ("tıp", 4),
            "mühendislik": ("mühendislik", 4),
            "hukuk": ("hukuk", 4),
            "teknik": ("teknik", 3),
            "doğa": ("doğa", 3),
            "yeşil": ("yeşil", 2),
            "orman": ("orman", 3),
        }

        # Check if question specifies a city
        target_city = None
        for c in campuses:
            if c.city.lower() in soru_lower or c.plate in soru_lower:
                target_city = c.city.lower()
                break

        for c in campuses:
            score = 0
            matches = []

            # City match boost
            if target_city and c.city.lower() == target_city:
                score += 10
                matches.append(f"İl: {c.city}")

            # Text content analysis
            text_blob = f"{c.title} {c.city} {c.district} {c.type} {' '.join(c.pros)} {' '.join(c.cons)} {c.student_note}".lower()
            for metric_k, metric_v in c.metrics.items():
                text_blob += f" {metric_k} {metric_v.get('degerlendirme', '')} {metric_v.get('detay', '')}".lower()

            for key, (term, weight) in keywords_weights.items():
                if key in soru_lower:
                    if term in text_blob:
                        score += weight
                        matches.append(term)

            # Rating boost
            if "⭐️⭐️⭐️⭐️⭐️" in c.rating or "4.8" in c.rating or "4.9" in c.rating or "5.0" in c.rating:
                score += 2

            if score > 0:
                scored.append((score, c, matches))

        scored.sort(key=lambda x: x[0], reverse=True)

        results = []
        for score, campus, matched_terms in scored[:top_k]:
            results.append({
                "skor": score,
                "kampus": campus.title,
                "sehir": f"{campus.plate} - {campus.city} / {campus.district}",
                "tur": campus.type,
                "puan": campus.rating,
                "dosya": campus.file_path,
                "ogrenci_notu": campus.student_note,
                "one_cikan_artilar": campus.pros[:3],
                "eslesen_kriterler": list(set(matched_terms))
            })

        return results
