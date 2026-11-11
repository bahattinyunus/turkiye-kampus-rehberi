# -*- coding: utf-8 -*-
"""
Türkiye Kampüs Rehberi - Veri Çıkarıcı & JSON API Oluşturucu
Bu betik depodaki tüm Markdown rehber dosyalarını ayrıştırarak
yapılandırılmış JSON veritabanı (data/kampusler.json ve data/istatistikler.json) üretir.
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

def parse_campus_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract Title: # 🏛️ [Üniversite] - [Kampüs]
    title_match = re.search(r'^#\s*(?:🏛️\s*)?(.*?)$', content, re.MULTILINE)
    title = clean_text(title_match.group(1)) if title_match else os.path.basename(file_path).replace('.md', '')

    # Extract Metadata
    metadata = {}
    for line in content.splitlines()[:20]:
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

    # Extract Highlights
    artilar = re.findall(r'###\s*✅\s*Artıları\s*\n((?:\s*\*\s*.*?\n)+)', content)
    eksiler = re.findall(r'###\s*❌\s*Eksileri\s*\n((?:\s*\*\s*.*?\n)+)', content)
    
    parsed_artilar = []
    if artilar:
        parsed_artilar = [clean_text(item) for item in re.findall(r'\*\s*(.*?)\n', artilar[0])]

    parsed_eksiler = []
    if eksiler:
        parsed_eksiler = [clean_text(item) for item in re.findall(r'\*\s*(.*?)\n', eksiler[0])]

    # Extract Student Tip
    ogrenci_notu_match = re.search(r'>\s*💬\s*\*\*Öğrenci Notu:\*\*\s*\n>\s*"(.*?)"', content, re.DOTALL)
    ogrenci_notu = ogrenci_notu_match.group(1).strip() if ogrenci_notu_match else ""

    # Path parts
    rel_path = os.path.relpath(file_path, os.getcwd()).replace('\\', '/')
    parts = rel_path.split('/')
    il_folder = parts[0] if len(parts) > 1 else ""
    ilce = parts[1] if len(parts) > 2 else "Merkez"
    
    plaka = il_folder[:2] if il_folder and il_folder[:2].isdigit() else ""
    il_adi = il_folder[3:] if len(il_folder) > 3 else il_folder

    return {
        "id": rel_path.replace('.md', ''),
        "baslik": title,
        "dosya_yolu": rel_path,
        "plaka": plaka,
        "il": il_adi,
        "ilce": ilce,
        "universite_turu": metadata.get('üniversite türü', metadata.get('tür', 'Devlet')),
        "ogrenci_dostu_puani": metadata.get('öğrenci dostu endeksi', metadata.get('genel öğrenci dostu puanı', '4.0/5')),
        "son_guncelleme": metadata.get('son güncelleme', 'Kasım 2026'),
        "metrikler": metrics,
        "artilar": parsed_artilar,
        "eksiler": parsed_eksiler,
        "ogrenci_notu": ogrenci_notu
    }

def main():
    root_dir = os.getcwd()
    data_dir = os.path.join(root_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)

    campuses = []
    provinces = {}

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
        "versiyon": "1.0.0"
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
