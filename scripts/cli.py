# -*- coding: utf-8 -*-
"""
Türkiye Kampüs Rehberi - İnteraktif Terminal Komut Satırı Aracı (CLI)
Kullanım:
  python scripts/cli.py stats
  python scripts/cli.py search "ODTÜ"
  python scripts/cli.py city 06
  python scripts/cli.py city Izmir
  python scripts/cli.py validate
"""

import sys
import os
import json
import re
import argparse
import glob

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT_DIR, 'data', 'kampusler.json')
STATS_PATH = os.path.join(ROOT_DIR, 'data', 'istatistikler.json')

def load_data():
    if not os.path.exists(DATA_PATH):
        print("Hata: data/kampusler.json bulunamadı. Lütfen önce `python scripts/export_json.py` çalıştırın.")
        sys.exit(1)
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def cmd_stats(args):
    data = load_data()
    print("=" * 60)
    print("🎓 TÜRKİYE KAMPÜS REHBERİ - DEPO İSTATİSTİKLERİ")
    print("=" * 60)
    print(f"Toplam İncelenen Kampüs / Fakülte / MYO: {len(data)}")
    
    cities = set(c['il'] for c in data)
    print(f"Kapsanan İl Sayısı: {len(cities)} / 81 İl")
    
    types = {}
    for c in data:
        t = c.get('universite_turu', 'Belirtilmemiş')
        types[t] = types.get(t, 0) + 1
    
    print("\nÜniversite Türleri Dağılımı:")
    for t, cnt in types.items():
        print(f"  • {t}: {cnt} yerleşke")
        
    md_count = len(glob.glob(os.path.join(ROOT_DIR, '**/*.md'), recursive=True))
    print(f"\nToplam Rehber Belgesi (.md): {md_count}")
    print("=" * 60)

def cmd_search(args):
    data = load_data()
    q = args.query.lower().strip()
    results = []
    
    for c in data:
        haystack = f"{c['baslik']} {c['il']} {c['ilce']} {' '.join(c['artilar'])} {' '.join(c['eksiler'])}".lower()
        if q in haystack:
            results.append(c)
            
    print(f"\n🔍 '{args.query}' için bulunan sonuçlar ({len(results)} kayıt):\n")
    if not results:
        print("  Eşleşen kampüs bulunamadı.")
        return
        
    for r in results[:15]:
        print(f"🏛️  {r['baslik']}")
        print(f"   📍 İl/İlçe: {r['il']} / {r['ilce']} (Plaka: {r['plaka']})")
        print(f"   ⭐ Puan: {r['ogrenci_dostu_puani']} | Tür: {r['universite_turu']}")
        if r['ogrenci_notu']:
            print(f"   💬 Tavsiye: \"{r['ogrenci_notu'][:120]}...\"")
        print(f"   📄 Dosya: {r['dosya_yolu']}")
        print("-" * 50)
        
    if len(results) > 15:
        print(f"\n... ve {len(results) - 15} sonuç daha. Aramanızı daraltabilirsiniz.")

def cmd_city(args):
    data = load_data()
    city_input = args.city.lower().strip()
    
    matched = [
        c for c in data 
        if c['plaka'] == city_input or c['il'].lower() == city_input or city_input in c['il'].lower()
    ]
    
    if not matched:
        print(f"Hata: '{args.city}' için kampüs bulunamadı.")
        return
        
    city_name = matched[0]['il']
    plate = matched[0]['plaka']
    print(f"\n📍 {plate} - {city_name} Kampüsleri ({len(matched)} Yerleşke):\n")
    
    for c in matched:
        print(f"  • {c['baslik']}")
        print(f"    İlçe: {c['ilce']} | Tür: {c['universite_turu']} | Endeks: {c['ogrenci_dostu_puani']}")
        print(f"    Rehber Dosyası: {c['dosya_yolu']}")
        print()

def cmd_validate(args):
    print("🔍 Depo link ve kodlama bütünlüğü taranıyor...")
    broken = 0
    checked_files = 0
    
    for root, dirs, files in os.walk(ROOT_DIR):
        if '.git' in root or 'node_modules' in root:
            continue
        for file in files:
            if not file.endswith('.md'):
                continue
            checked_files += 1
            fpath = os.path.join(root, file)
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            for m in re.finditer(r'\]\(([^)\s]+)\)', content):
                link = m.group(1)
                if link.startswith(('http://', 'https://', 'mailto:', '#')):
                    continue
                clean_target = link.split('#')[0]
                if not clean_target:
                    continue
                target_path = os.path.normpath(os.path.join(root, clean_target))
                if not os.path.exists(target_path):
                    broken += 1
                    rel_src = os.path.relpath(fpath, ROOT_DIR)
                    print(f"  ❌ Kırık Link: {rel_src} -> {link}")
                    
    print(f"\nKontrol tamamlandı:")
    print(f"  • Toplam taranan dosya: {checked_files}")
    print(f"  • Kırık bağlantı sayısı: {broken}")
    if broken == 0:
        print("  ✓ TÜM BAĞLANTILAR GEÇERLİ! Depo 100% sağlıklı.")
    else:
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Türkiye Kampüs Rehberi CLI")
    subparsers = parser.add_subparsers(dest="subcommand", help="Komutlar")
    
    subparsers.add_parser("stats", help="Genel depo istatistiklerini gösterir")
    
    search_p = subparsers.add_parser("search", help="Kampüs ve üniversite ara")
    search_p.add_argument("query", help="Arama terimi (örn: ODTÜ, Tıp, Metro)")
    
    city_p = subparsers.add_parser("city", help="Şehre göre yerleşkeleri listele")
    city_p.add_argument("city", help="Plaka kodu veya şehir adı (örn: 06, Ankara, 35, Izmir)")
    
    subparsers.add_parser("validate", help="Depodaki bağlantıları doğrula")
    
    args = parser.parse_args()
    
    if args.subcommand == "stats":
        cmd_stats(args)
    elif args.subcommand == "search":
        cmd_search(args)
    elif args.subcommand == "city":
        cmd_city(args)
    elif args.subcommand == "validate":
        cmd_validate(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
