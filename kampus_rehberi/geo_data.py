# -*- coding: utf-8 -*-
"""
Türkiye Kampüs Rehberi - 81 İl Coğrafi Koordinat ve Yaşam Maliyeti Veri Seti
Harita görselleştirmeleri, mesafe hesapları ve öğrenci bütçe simülasyonları için kullanılır.
"""

from typing import Dict, Any

# 81 İl Merkez Koordinatları (Enlem, Boylam)
PROVINCE_COORDINATES: Dict[str, Dict[str, float]] = {
    "01": {"lat": 37.0000, "lng": 35.3213, "il": "Adana"},
    "02": {"lat": 37.7648, "lng": 38.2786, "il": "Adıyaman"},
    "03": {"lat": 38.7507, "lng": 30.5567, "il": "Afyonkarahisar"},
    "04": {"lat": 39.7191, "lng": 43.0503, "il": "Ağrı"},
    "05": {"lat": 40.6534, "lng": 35.8333, "il": "Amasya"},
    "06": {"lat": 39.9334, "lng": 32.8597, "il": "Ankara"},
    "07": {"lat": 36.8969, "lng": 30.7133, "il": "Antalya"},
    "08": {"lat": 41.1828, "lng": 41.8183, "il": "Artvin"},
    "09": {"lat": 37.8560, "lng": 27.8416, "il": "Aydın"},
    "10": {"lat": 39.6484, "lng": 27.8826, "il": "Balıkesir"},
    "11": {"lat": 40.1451, "lng": 29.9799, "il": "Bilecik"},
    "12": {"lat": 38.8854, "lng": 40.4983, "il": "Bingöl"},
    "13": {"lat": 38.4006, "lng": 42.1095, "il": "Bitlis"},
    "14": {"lat": 40.7358, "lng": 31.6061, "il": "Bolu"},
    "15": {"lat": 37.7203, "lng": 30.2908, "il": "Burdur"},
    "16": {"lat": 40.1885, "lng": 29.0610, "il": "Bursa"},
    "17": {"lat": 40.1553, "lng": 26.4142, "il": "Çanakkale"},
    "18": {"lat": 40.6013, "lng": 33.6134, "il": "Çankırı"},
    "19": {"lat": 40.5506, "lng": 34.9556, "il": "Çorum"},
    "20": {"lat": 37.7765, "lng": 29.0864, "il": "Denizli"},
    "21": {"lat": 37.9144, "lng": 40.2306, "il": "Diyarbakır"},
    "22": {"lat": 41.6772, "lng": 26.5557, "il": "Edirne"},
    "23": {"lat": 38.6810, "lng": 39.2264, "il": "Elazığ"},
    "24": {"lat": 39.7500, "lng": 39.5000, "il": "Erzincan"},
    "25": {"lat": 39.9000, "lng": 41.2700, "il": "Erzurum"},
    "26": {"lat": 39.7767, "lng": 30.5206, "il": "Eskişehir"},
    "27": {"lat": 37.0662, "lng": 37.3833, "il": "Gaziantep"},
    "28": {"lat": 40.9128, "lng": 38.3895, "il": "Giresun"},
    "29": {"lat": 40.4600, "lng": 39.4700, "il": "Gümüşhane"},
    "30": {"lat": 37.5833, "lng": 43.7333, "il": "Hakkari"},
    "31": {"lat": 36.2023, "lng": 36.1613, "il": "Hatay"},
    "32": {"lat": 37.7648, "lng": 30.5566, "il": "Isparta"},
    "33": {"lat": 36.8121, "lng": 34.6415, "il": "Mersin"},
    "34": {"lat": 41.0082, "lng": 28.9784, "il": "İstanbul"},
    "35": {"lat": 38.4192, "lng": 27.1287, "il": "İzmir"},
    "36": {"lat": 40.6167, "lng": 43.1000, "il": "Kars"},
    "37": {"lat": 41.3887, "lng": 33.7827, "il": "Kastamonu"},
    "38": {"lat": 38.7312, "lng": 35.4787, "il": "Kayseri"},
    "39": {"lat": 41.7333, "lng": 27.2167, "il": "Kırklareli"},
    "40": {"lat": 39.1425, "lng": 34.1709, "il": "Kırşehir"},
    "41": {"lat": 40.7654, "lng": 29.9408, "il": "Kocaeli"},
    "42": {"lat": 37.8667, "lng": 32.4833, "il": "Konya"},
    "43": {"lat": 39.4167, "lng": 29.9833, "il": "Kütahya"},
    "44": {"lat": 38.3552, "lng": 38.3095, "il": "Malatya"},
    "45": {"lat": 38.6191, "lng": 27.4289, "il": "Manisa"},
    "46": {"lat": 37.5858, "lng": 36.9371, "il": "Kahramanmaraş"},
    "47": {"lat": 37.3212, "lng": 40.7245, "il": "Mardin"},
    "48": {"lat": 37.2153, "lng": 28.3636, "il": "Muğla"},
    "49": {"lat": 38.7432, "lng": 41.5064, "il": "Muş"},
    "50": {"lat": 38.6244, "lng": 34.7144, "il": "Nevşehir"},
    "51": {"lat": 37.9667, "lng": 34.6833, "il": "Niğde"},
    "52": {"lat": 40.9839, "lng": 37.8764, "il": "Ordu"},
    "53": {"lat": 41.0201, "lng": 40.5234, "il": "Rize"},
    "54": {"lat": 40.7569, "lng": 30.3783, "il": "Sakarya"},
    "55": {"lat": 41.2928, "lng": 36.3313, "il": "Samsun"},
    "56": {"lat": 37.9333, "lng": 41.9500, "il": "Siirt"},
    "57": {"lat": 42.0231, "lng": 35.1531, "il": "Sinop"},
    "58": {"lat": 39.7477, "lng": 37.0179, "il": "Sivas"},
    "59": {"lat": 40.9833, "lng": 27.5167, "il": "Tekirdağ"},
    "60": {"lat": 40.3167, "lng": 36.5500, "il": "Tokat"},
    "61": {"lat": 41.0027, "lng": 39.7167, "il": "Trabzon"},
    "62": {"lat": 39.1079, "lng": 39.5401, "il": "Tunceli"},
    "63": {"lat": 37.1591, "lng": 38.7969, "il": "Şanlıurfa"},
    "64": {"lat": 38.6823, "lng": 29.4082, "il": "Uşak"},
    "65": {"lat": 38.4891, "lng": 43.4089, "il": "Van"},
    "66": {"lat": 39.8181, "lng": 34.8147, "il": "Yozgat"},
    "67": {"lat": 41.4564, "lng": 31.7987, "il": "Zonguldak"},
    "68": {"lat": 38.3687, "lng": 34.0370, "il": "Aksaray"},
    "69": {"lat": 40.2552, "lng": 40.2249, "il": "Bayburt"},
    "70": {"lat": 37.1759, "lng": 33.2287, "il": "Karaman"},
    "71": {"lat": 39.8468, "lng": 33.5153, "il": "Kırıkkale"},
    "72": {"lat": 37.8812, "lng": 41.1293, "il": "Batman"},
    "73": {"lat": 37.5164, "lng": 42.4594, "il": "Şırnak"},
    "74": {"lat": 41.6344, "lng": 32.3375, "il": "Bartın"},
    "75": {"lat": 41.1105, "lng": 42.7022, "il": "Ardahan"},
    "76": {"lat": 39.9196, "lng": 44.0454, "il": "Iğdır"},
    "77": {"lat": 40.6550, "lng": 29.2769, "il": "Yalova"},
    "78": {"lat": 41.2061, "lng": 32.6204, "il": "Karabük"},
    "79": {"lat": 36.7184, "lng": 37.1212, "il": "Kilis"},
    "80": {"lat": 37.0742, "lng": 36.2472, "il": "Osmaniye"},
    "81": {"lat": 40.8438, "lng": 31.1565, "il": "Düzce"}
}

def get_province_geo(plate_or_city: str) -> Dict[str, Any]:
    """Plaka kodu veya il adına göre koordinat bilgisini döndürür."""
    query = plate_or_city.lower().strip()
    for plate, info in PROVINCE_COORDINATES.items():
        if plate == query or info["il"].lower() == query:
            return {"plaka": plate, **info}
    return {}
