# -*- coding: utf-8 -*-
"""
Türkiye Kampüs Rehberi - Gelişmiş Veri Çıkarıcı & JSON API Motoru
Bu betik depodaki tüm Markdown rehber dosyalarını ayrıştırarak
yapılandırılmış, zenginleştirilmiş JSON veritabanı
(data/kampusler.json ve data/istatistikler.json) üretir.
"""

import os
import re
import json
import glob
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # remove md links
    text = re.sub(r'[*_`]', '', text)                     # remove formatting
    return text.strip()

def extract_rating_num(rating_str):
    if not rating_str:
        return 4.0
    m = re.search(r'(\d+(?:[.,]\d+)?)\s*(?:/\s*5)?', rating_str)
    if m:
        try:
            return float(m.group(1).replace(',', '.'))
        except ValueError:
            pass
    return 4.0

def parse_campus_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract Title: # 🏛️ [Üniversite] - [Kampüs]
    title_match = re.search(r'^#\s*(?:🏛️\s*)?(.*?)$', content, re.MULTILINE)
    title = clean_text(title_match.group(1)) if title_match else os.path.basename(file_path).replace('.md', '')

    # Extract Metadata
    metadata = {}
    for line in content.splitlines()[:25]:
        line = line.strip()
        if line.startswith('>') or line.startswith('*'):
            m = re.search(r'[*_]*([A-Za-zÇĞİÖŞÜçğıöşü\s/]+)[*_]*\s*:\s*(.*?)(?:\\s{2,}|$)', line)
            if m:
                key = m.group(1).strip().lower()
                val = clean_text(m.group(2).strip())
                metadata[key] = val

    # Extract Quick Look Table Metrics
    metrics = {}
    table_rows = re.findall(r'\|\s*\*+([^|*]+)\*+\s*\|\s*([^|]+)\|\s*([^|]+)\|', content)
    for row in table_rows:
        metric_name = clean_text(row[0]).lower()
        rating = clean_text(row[1])
        detail = clean_text(row[2])
        metrics[metric_name] = {
            "degerlendirme": rating,
            "detay": detail
        }

    # Extract Pros & Cons
    # 1. Classical Format (### ✅ Artıları / ### ❌ Eksileri)
    artilar_match = re.findall(r'###\s*✅\s*Artıları[^\n]*\n((?:\s*[\*\-]\s*.*?\n)+)', content)
    eksiler_match = re.findall(r'###\s*❌\s*Eksileri[^\n]*\n((?:\s*[\*\-]\s*.*?\n)+)', content)
    
    parsed_artilar = []
    if artilar_match:
        parsed_artilar = [clean_text(item) for item in re.findall(r'[\*\-]\s*(.*?)\n', artilar_match[0])]

    parsed_eksiler = []
    if eksiler_match:
        parsed_eksiler = [clean_text(item) for item in re.findall(r'[\*\-]\s*(.*?)\n', eksiler_match[0])]

    # 2. Section Format (## 5. ❌ Eksileri ve Kronik Sorunları)
    if not parsed_eksiler:
        sec5_match = re.search(r'##\s*(?:\d+\.\s*)?❌\s*Eksileri[^\n]*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
        if sec5_match:
            sec5_text = sec5_match.group(1)
            # Find bullet points
            items = re.findall(r'^\s*[\*\-]\s*(?:\*\*(.*?)\*\*:?\s*)?(.*?)(?=^\s*[\*\-]|\Z)', sec5_text, re.MULTILINE | re.DOTALL)
            for title_sub, desc in items:
                t_clean = clean_text(title_sub).rstrip(':').strip()
                d_clean = clean_text(desc).strip()
                bullet = f"{t_clean}: {d_clean}" if t_clean else d_clean
                bullet_clean = bullet.replace('\n', ' ')
                bullet_clean = re.sub(r'\s+', ' ', bullet_clean)
                if bullet_clean:
                    parsed_eksiler.append(bullet_clean[:200])

    # 3. Gold Tips / Altın Tavsiyeler (## 6. 💡 Altın Tavsiyeler)
    altin_tavsiyeler = []
    sec6_match = re.search(r'##\s*(?:\d+\.\s*)?💡\s*Altın Tavsiyeler[^\n]*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
    if sec6_match:
        sec6_text = sec6_match.group(1)
        # Match numbered or bullet points: 1. **Title:** text or * **Title:** text
        items = re.findall(r'^\s*(?:\d+\.|\*|\-)\s*(?:\*\*(.*?)\*\*:?\s*)?(.*?)(?=^\s*(?:\d+\.|\*|\-)|\Z)', sec6_text, re.MULTILINE | re.DOTALL)
        for t_sub, desc in items:
            t_clean = clean_text(t_sub).rstrip(':').strip()
            d_clean = clean_text(desc).strip()
            tip = f"{t_clean}: {d_clean}" if t_clean else d_clean
            tip_clean = tip.replace('\n', ' ')
            tip_clean = re.sub(r'\s+', ' ', tip_clean)
            if tip_clean:
                altin_tavsiyeler.append(tip_clean)

    # If artilar is empty, derive from metrics and positive tips
    if not parsed_artilar:
        derived_pros = []
        for m_name, m_val in metrics.items():
            deg = m_val.get("degerlendirme", "")
            det = m_val.get("detay", "")
            if any(good in deg.lower() for good in ["çok yüksek", "yüksek", "çok başarılı", "başarılı", "ücretsiz", "7/24", "modern", "fiber"]):
                clean_m = m_name.replace("🚇", "").replace("🏠", "").replace("🍽️", "").replace("📚", "").replace("🌐", "").strip()
                derived_pros.append(f"{clean_m.capitalize()}: {deg}")
        if altin_tavsiyeler:
            for tip in altin_tavsiyeler[:2]:
                derived_pros.append(tip[:120])
        parsed_artilar = derived_pros[:5]

    # Extract Student Tip / Note
    ogrenci_notu_match = re.search(r'>\s*💬\s*\*\*Öğrenci Notu:\*\*\s*\n>\s*"(.*?)"', content, re.DOTALL)
    if ogrenci_notu_match:
        ogrenci_notu = ogrenci_notu_match.group(1).strip()
    elif altin_tavsiyeler:
        ogrenci_notu = altin_tavsiyeler[0]
    else:
        ogrenci_notu = ""

    # Path parts
    rel_path = os.path.relpath(file_path, os.getcwd()).replace('\\', '/')
    parts = rel_path.split('/')
    if parts and parts[0] == 'iller':
        parts = parts[1:]
    il_folder = parts[0] if len(parts) > 1 else ""
    ilce = parts[1] if len(parts) > 2 else "Merkez"
    
    plaka = il_folder[:2] if il_folder and il_folder[:2].isdigit() else ""
    il_adi = il_folder[3:] if len(il_folder) > 3 else il_folder

    rating_raw = metadata.get('öğrenci dostu endeksi', metadata.get('genel öğrenci dostu puanı', '⭐️⭐️⭐️⭐️☆ (4.0/5)'))
    puan_num = extract_rating_num(rating_raw)

    # Detailed section summaries for rich views
    ulasim_match = re.search(r'##\s*(?:\d+\.\s*)?🚌\s*Ulaşım[^\n]*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
    barinma_match = re.search(r'##\s*(?:\d+\.\s*)?🏠\s*Barınma[^\n]*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
    beslenme_match = re.search(r'##\s*(?:\d+\.\s*)?🍽️\s*Beslenme[^\n]*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
    akademik_match = re.search(r'##\s*(?:\d+\.\s*)?📚\s*Akademik[^\n]*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)

    def extract_preview(sec_match, max_len=300):
        if not sec_match:
            return ""
        txt = clean_text(sec_match.group(1)).replace('\n', ' ')
        txt = re.sub(r'\s+', ' ', txt).strip()
        return txt[:max_len] + '...' if len(txt) > max_len else txt

    bolum_ozetleri = {
        "ulasim": extract_preview(ulasim_match),
        "barinma": extract_preview(barinma_match),
        "beslenme": extract_preview(beslenme_match),
        "akademik": extract_preview(akademik_match)
    }

    return {
        "id": rel_path.replace('.md', ''),
        "baslik": title,
        "dosya_yolu": rel_path,
        "plaka": plaka,
        "il": il_adi,
        "ilce": ilce,
        "universite_turu": metadata.get('üniversite türü', metadata.get('tür', 'Devlet')),
        "ogrenci_dostu_puani": rating_raw,
        "puan_sayisal": puan_num,
        "son_guncelleme": metadata.get('son güncelleme', 'Kasım 2026'),
        "metrikler": metrics,
        "artilar": parsed_artilar,
        "eksiler": parsed_eksiler,
        "altin_tavsiyeler": altin_tavsiyeler,
        "ogrenci_notu": ogrenci_notu,
        "bolum_ozetleri": bolum_ozetleri
    }

def main():
    root_dir = os.getcwd()
    data_dir = os.path.join(root_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)

    campuses = []
    provinces = {}

    md_files = glob.glob(os.path.join(root_dir, 'iller', '[0-8][0-9]-*/**/*.md'), recursive=True)
    if not md_files:
        md_files = glob.glob(os.path.join(root_dir, '[0-8][0-9]-*/**/*.md'), recursive=True)
    
    for f in md_files:
        filename = os.path.basename(f)
        if filename == 'README.md':
            continue
        try:
            campus_data = parse_campus_file(f)
            campuses.append(campus_data)
            
            p_code = campus_data['plaka']
            if p_code not in provinces:
                provinces[p_code] = {
                    "plaka": p_code,
                    "il": campus_data['il'],
                    "kampus_sayisi": 0,
                    "kampusler": []
                }
            provinces[p_code]["kampus_sayisi"] += 1
            provinces[p_code]["kampusler"].append(campus_data['id'])
        except Exception as e:
            print(f"Hata ({f}): {e}")

    # Sort campuses by city plate then title
    campuses.sort(key=lambda x: (x['plaka'], x['baslik']))

    # Statistics
    stats = {
        "toplam_il_sayisi": len(provinces),
        "toplam_kampus_sayisi": len(campuses),
        "kapsanan_iller": sorted(list(provinces.keys())),
        "guncelleme_tarihi": "Kasım 2026",
        "versiyon": "2.0.0"
    }

    # Write data/kampusler.json
    out_campuses = os.path.join(data_dir, 'kampusler.json')
    with open(out_campuses, 'w', encoding='utf-8') as f:
        json.dump(campuses, f, ensure_ascii=False, indent=2)
    print(f"✓ {len(campuses)} adet kampüs {out_campuses} dosyasına kaydedildi.")

    # Write data/istatistikler.json
    out_stats = os.path.join(data_dir, 'istatistikler.json')
    with open(out_stats, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    print(f"✓ İstatistikler {out_stats} dosyasına kaydedildi.")

    # Mirror to web/data/ for GitHub Pages / web viewer
    web_data_dir = os.path.join(root_dir, 'web', 'data')
    os.makedirs(web_data_dir, exist_ok=True)
    with open(os.path.join(web_data_dir, 'kampusler.json'), 'w', encoding='utf-8') as f:
        json.dump(campuses, f, ensure_ascii=False, indent=2)
    with open(os.path.join(web_data_dir, 'istatistikler.json'), 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    print(f"✓ web/data/ kopyası başarıyla güncellendi.")

if __name__ == '__main__':
    main()
