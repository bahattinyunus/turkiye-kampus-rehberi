# -*- coding: utf-8 -*-
import sys
import os
import argparse
import json
import http.server
import socketserver
import webbrowser

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from .core import KampusRehberi
from .advisor import TercihDanismani

def cmd_stats(rehber, args):
    st = rehber.stats()
    print("=" * 60)
    print("🎓 TÜRKİYE KAMPÜS REHBERİ - DEPO İSTATİSTİKLERİ")
    print("=" * 60)
    print(f"Toplam İncelenen Kampüs / Fakülte / MYO: {st['toplam_kampus']}")
    print(f"Kapsanan İl Sayısı: {st['kapsanan_il']} / 81 İl")
    print("\nÜniversite Türleri Dağılımı:")
    for t, cnt in st['turler'].items():
        print(f"  • {t}: {cnt} yerleşke")
    print("=" * 60)

def cmd_search(rehber, args):
    results = rehber.search(
        query=args.query or "",
        city=args.city,
        type_=args.type
    )
    print(f"\n🔍 Arama Sonuçları ({len(results)} kayıt):\n")
    if not results:
        print("  Eşleşen kampüs bulunamadı.")
        return

    for c in results[:15]:
        print(f"🏛️  {c.title}")
        print(f"   📍 İl/İlçe: {c.city} / {c.district} (Plaka: {c.plate})")
        print(f"   ⭐ Puan: {c.rating} | Tür: {c.type}")
        if c.student_note:
            print(f"   💬 Tavsiye: \"{c.student_note[:120]}...\"")
        print(f"   📄 Dosya: {c.file_path}")
        print("-" * 50)

    if len(results) > 15:
        print(f"\n... ve {len(results) - 15} sonuç daha.")

def cmd_city(rehber, args):
    results = rehber.search(city=args.city)
    if not results:
        print(f"Hata: '{args.city}' için kampüs bulunamadı.")
        return

    city_name = results[0].city
    plate = results[0].plate
    print(f"\n📍 {plate} - {city_name} Kampüsleri ({len(results)} Yerleşke):\n")
    for c in results:
        print(f"  • {c.title}")
        print(f"    İlçe: {c.district} | Tür: {c.type} | Endeks: {c.rating}")
        print(f"    Rehber Dosyası: {c.file_path}\n")

def cmd_compare(rehber, args):
    try:
        res = rehber.compare(args.campus1, args.campus2)
        c1 = res["kampus_1"]
        c2 = res["kampus_2"]
        print("=" * 70)
        print(f"⚖️  KARŞILAŞTIRMA: {c1['baslik']} VS {c2['baslik']}")
        print("=" * 70)
        print(f"İl / İlçe:        {c1['il']} / {c1['ilce']}  vs  {c2['il']} / {c2['ilce']}")
        print(f"Tür:              {c1['universite_turu']}  vs  {c2['universite_turu']}")
        print(f"Puan:             {c1['ogrenci_dostu_puani']}  vs  {c2['ogrenci_dostu_puani']}")
        print("\nÖne Çıkan Artılar:")
        print(f"  • {c1['baslik'][:30]}: {', '.join(c1['artilar'][:2])}")
        print(f"  • {c2['baslik'][:30]}: {', '.join(c2['artilar'][:2])}")
        print("=" * 70)
    except Exception as e:
        print(f"Hata: {e}")

def cmd_ask(rehber, args):
    advisor = TercihDanismani(rehber)
    results = advisor.danis(args.question, top_k=args.top_k)
    print("=" * 70)
    print(f"🤖 TERCİH DANIŞMANI: \"{args.question}\"")
    print("=" * 70)
    if not results:
        print("Uygun eşleşme bulunamadı. Lütfen sorunuzu farklı anahtar kelimelerle deneyin.")
        return

    for i, r in enumerate(results, 1):
        print(f"\n{i}. 🏛️  {r['kampus']}")
        print(f"   📍 Konum: {r['sehir']} | {r['tur']}")
        print(f"   ⭐ Puan: {r['puan']}")
        if r['eslesen_kriterler']:
            print(f"   🎯 Eşleşen Nedenler: {', '.join(r['eslesen_kriterler'])}")
        if r['one_cikan_artilar']:
            print(f"   ✅ Avantajlar: {'; '.join(r['one_cikan_artilar'])}")
        if r['ogrenci_notu']:
            print(f"   💬 Öğrenci Tavsiyesi: \"{r['ogrenci_notu']}\"")
    print("\n" + "=" * 70)

def cmd_validate():
    print("🔍 Depo bağlantı ve bütünlüğü taranıyor...")
    broken = 0
    checked_files = 0
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    for r, dirs, files in os.walk(root):
        if '.git' in r or 'node_modules' in r or '__pycache__' in r:
            continue
        for file in files:
            if not file.endswith('.md'):
                continue
            checked_files += 1
            fpath = os.path.join(r, file)
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()

            import re
            for m in re.finditer(r'\]\(([^)\s]+)\)', content):
                link = m.group(1)
                if link.startswith(('http://', 'https://', 'mailto:', '#')):
                    continue
                clean_target = link.split('#')[0]
                if not clean_target:
                    continue
                target_path = os.path.normpath(os.path.join(r, clean_target))
                if not os.path.exists(target_path):
                    broken += 1
                    rel_src = os.path.relpath(fpath, root)
                    print(f"  ❌ Kırık Link: {rel_src} -> {link}")

    print(f"\nKontrol tamamlandı:")
    print(f"  • Toplam taranan dosya: {checked_files}")
    print(f"  • Kırık bağlantı sayısı: {broken}")
    if broken == 0:
        print("  ✓ TÜM BAĞLANTILAR GEÇERLİ! Depo 100% sağlıklı.")
    else:
        sys.exit(1)

def cmd_serve(args):
    port = args.port
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(root)
    
    class Handler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
            super().end_headers()

    with socketserver.TCPServer(("", port), Handler) as httpd:
        url = f"http://localhost:{port}/web/index.html"
        print(f"🚀 Kampüs Rehberi Yerel Sunucusu Açıldı: {url}")
        print("Durdurmak için Ctrl+C tuşlarına basın.")
        if not args.no_browser:
            webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nSunucu kapatıldı.")

def main():
    parser = argparse.ArgumentParser(description="Türkiye Kampüs Rehberi CLI ve Tercih Danışmanı")
    subparsers = parser.add_subparsers(dest="subcommand", help="Komutlar")

    subparsers.add_parser("stats", help="Genel depo istatistikleri")

    search_p = subparsers.add_parser("search", help="Kampüs ara")
    search_p.add_argument("query", nargs="?", default="", help="Arama metni")
    search_p.add_argument("--city", help="Şehir filtresi")
    search_p.add_argument("--type", help="Tür filtresi (Devlet / Vakıf)")

    city_p = subparsers.add_parser("city", help="Şehre göre yerleşkeleri listele")
    city_p.add_argument("city", help="Plaka kodu veya şehir adı")

    compare_p = subparsers.add_parser("compare", help="İki kampüsü kıyasla")
    compare_p.add_argument("campus1", help="1. Kampüs ID'si")
    compare_p.add_argument("campus2", help="2. Kampüs ID'si")

    ask_p = subparsers.add_parser("ask", help="Akıllı tercih danışmanına sor")
    ask_p.add_argument("question", help="Sorunuz (örn: 'Deniz kıyısında olan mühendislikler')")
    ask_p.add_argument("--top-k", type=int, default=5, help="Döndürülecek sonuç sayısı")

    serve_p = subparsers.add_parser("serve", help="Web arayüzünü ve REST API'yi yerel sunucuda başlat")
    serve_p.add_argument("--port", type=int, default=8000, help="Port numarası")
    serve_p.add_argument("--no-browser", action="store_true", help="Tarayıcıyı otomatik açma")

    subparsers.add_parser("validate", help="Depodaki bağlantıları ve dosya bütünlüğünü doğrula")

    args = parser.parse_args()

    if args.subcommand == "serve":
        cmd_serve(args)
        return

    if args.subcommand == "validate":
        cmd_validate()
        return

    rehber = KampusRehberi()

    if args.subcommand == "stats":
        cmd_stats(rehber, args)
    elif args.subcommand == "search":
        cmd_search(rehber, args)
    elif args.subcommand == "city":
        cmd_city(rehber, args)
    elif args.subcommand == "compare":
        cmd_compare(rehber, args)
    elif args.subcommand == "ask":
        cmd_ask(rehber, args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
