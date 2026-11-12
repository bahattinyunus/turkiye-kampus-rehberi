# -*- coding: utf-8 -*-
"""
Türkiye Kampüs Rehberi - Gelişmiş CLI Arayüzü & Akıllı Tercih Asistanı
"""

import sys
import os
import argparse
import webbrowser

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from .core import KampusRehberi
from .advisor import TercihDanismani
from .budget import CostCalculator
from .yks import TercihListesi
from .api import run_api_server

def print_banner():
    print("=" * 70)
    print("🎓 TÜRKİYE KAMPÜS REHBERİ - ÖĞRENCİDEN ÖĞRENCİYE TERCİH ASİSTANI")
    print("=" * 70)

def cmd_stats(rehber, args):
    st = rehber.stats()
    print_banner()
    print(f"📊 Toplam İncelenen Kampüs / Yerleşke : {st['toplam_kampus']}")
    print(f"📍 Kapsanan İl Sayısı                  : {st['kapsanan_il']} / 81 İl (100% Kapsam)")
    print(f"⭐ Ortalama Öğrenci Puanı              : {st['ortalama_puan']} / 5.0")
    print("\n🏛️ Üniversite Türleri Dağılımı:")
    for t, cnt in st['turler'].items():
        print(f"   • {t:<15}: {cnt} yerleşke")
    print("=" * 70)

def cmd_search(rehber, args):
    results = rehber.search(
        query=args.query or "",
        city=args.city,
        type_=args.type,
        min_rating=args.min_rating,
        sort_by=args.sort or "default"
    )
    print(f"\n🔍 Arama Sonuçları: {len(results)} yerleşke bulundu.\n")
    if not results:
        print("  ❌ Eşleşen kampüs bulunamadı. Lütfen arama terimini değiştirin.")
        return

    limit = args.limit or 15
    for i, c in enumerate(results[:limit], 1):
        print(f"{i:2d}. 🏛️  {c.title}")
        print(f"    📍 İl/İlçe : {c.plate} - {c.city} / {c.district}")
        print(f"    ⭐ Puan    : {c.rating} ({c.rating_num}/5) | Tür: {c.type}")
        if c.pros:
            print(f"    ✅ Artı    : {', '.join(c.pros[:2])}")
        if c.student_note:
            note_short = (c.student_note[:110] + '...') if len(c.student_note) > 110 else c.student_note
            print(f"    💬 Not     : \"{note_short}\"")
        print(f"    📄 Dosya   : {c.file_path}")
        print("-" * 65)

    if len(results) > limit:
        print(f"\n... ve {len(results) - limit} sonuç daha. Tümünü görmek için --limit parametresini kullanın.")

def cmd_city(rehber, args):
    results = rehber.search(city=args.city)
    if not results:
        print(f"❌ Hata: '{args.city}' ili için kampüs bulunamadı.")
        return

    city_name = results[0].city
    plate = results[0].plate
    print(f"\n📍 {plate} - {city_name} Kampüsleri ({len(results)} Yerleşke):\n")
    for i, c in enumerate(results, 1):
        print(f" {i:2d}. 🏛️  {c.title}")
        print(f"     İlçe: {c.district} | Tür: {c.type} | Endeks: {c.rating}")
        if c.student_note:
            note_short = (c.student_note[:90] + '...') if len(c.student_note) > 90 else c.student_note
            print(f"     💬 \"{note_short}\"")
        print(f"     Rehber Dosyası: {c.file_path}\n")

def cmd_top(rehber, args):
    top_campuses = rehber.get_top_rated(n=args.n or 10, city=args.city)
    header = f"🏆 TÜRKİYE'NİN EN YÜKSEK PUANLI {len(top_campuses)} KAMPÜSÜ"
    if args.city:
        header += f" ({args.city})"
    print("\n" + "=" * 70)
    print(header)
    print("=" * 70)
    for i, c in enumerate(top_campuses, 1):
        print(f" {i:2d}. ⭐ {c.rating_num}/5.0 | {c.title}")
        print(f"     📍 {c.city} / {c.district} ({c.type})")
        if c.pros:
            print(f"     ✅ {', '.join(c.pros[:2])}")
        print("-" * 70)

def cmd_random(rehber, args):
    campus = rehber.get_random()
    print("\n🎲 RASTGELE KAMPÜS KEŞFİ:")
    print("=" * 70)
    print(campus.to_markdown())
    print("=" * 70)

def cmd_compare(rehber, args):
    try:
        res = rehber.compare(args.campus1, args.campus2)
        c1 = res["kampus_1"]
        c2 = res["kampus_2"]
        print("=" * 70)
        print(f"⚖️  KARŞILAŞTIRMA: {c1['baslik'][:30]}  VS  {c2['baslik'][:30]}")
        print("=" * 70)
        print(f"{'Özellik':<22} | {'1. Kampüs':<22} | {'2. Kampüs'}")
        print("-" * 70)
        print(f"{'Şehir / İlçe':<22} | {c1['il'] + '/' + c1['ilce']:<22} | {c2['il'] + '/' + c2['ilce']}")
        print(f"{'Üniversite Türü':<22} | {c1['universite_turu']:<22} | {c2['universite_turu']}")
        print(f"{'Öğrenci Puanı':<22} | {str(c1.get('puan_sayisal', '4.0')) + '/5.0':<22} | {str(c2.get('puan_sayisal', '4.0')) + '/5.0'}")
        print("=" * 70)
        print(f"\n✅ {c1['baslik'][:35]} Öne Çıkan Artıları:")
        for pro in c1.get("artilar", [])[:3]:
            print(f"   • {pro}")
        print(f"\n✅ {c2['baslik'][:35]} Öne Çıkan Artıları:")
        for pro in c2.get("artilar", [])[:3]:
            print(f"   • {pro}")
        print("=" * 70)
    except Exception as e:
        print(f"❌ Hata: {e}")

def cmd_ask(rehber, args):
    advisor = TercihDanismani(rehber)
    results = advisor.danis(args.question, top_k=args.top_k)
    print("=" * 70)
    print(f"🤖 AKILLI TERCİH DANIŞMANI: \"{args.question}\"")
    print("=" * 70)
    if not results:
        print("Uygun eşleşme bulunamadı. Lütfen sorunuzu farklı anahtar kelimelerle deneyin.")
        return

    for i, r in enumerate(results, 1):
        print(f"\n{i}. 🏛️  {r['kampus']}  [Uyum: {r['uyum_yuzdesi']}]")
        print(f"   📍 Konum   : {r['sehir']} | {r['tur']}")
        print(f"   ⭐ Puan    : {r['puan']} ({r['puan_sayisal']}/5)")
        if r['eslesen_kriterler']:
            print(f"   🎯 Nedenler: {', '.join(r['eslesen_kriterler'])}")
        if r['one_cikan_artilar']:
            print(f"   ✅ Artılar : {'; '.join(r['one_cikan_artilar'])}")
        if r['ogrenci_notu']:
            print(f"   💬 Tavsiye : \"{r['ogrenci_notu']}\"")
    print("\n" + "=" * 70)

def cmd_budget(rehber, args):
    calc = CostCalculator(rehber)
    res = calc.calculate_monthly(
        args.city,
        housing_type=args.housing or "kyk",
        meals_on_campus=args.meals if args.meals is not None else 1,
        lifestyle=args.lifestyle or "moderate"
    )
    print("\n" + "=" * 70)
    print(f"💰 {res['sehir'].upper()} ÖĞRENCİ AYLIK YAŞAM MALİYETİ RAPORU")
    print("=" * 70)
    print(f"Barınma Modeli : {res['barinma_turu'].upper()}")
    print(f"Yaşam Tarzı    : {res['yasam_tarzi'].capitalize()}")
    print("-" * 70)
    print("Gider Kalemleri (Aylık):")
    k = res['kalemler']
    print(f"  • Kira / Yurt Bedeli        : {k['barinma_kira']:>6,d} TL".replace(',', '.'))
    print(f"  • Faturalar & Aidat         : {k['faturalar_aidat']:>6,d} TL".replace(',', '.'))
    print(f"  • Yemekhane & Gıda          : {k['yemekhane_ve_gida']:>6,d} TL".replace(',', '.'))
    print(f"  • Ulaşım (Öğrenci Abonman)  : {k['ulasim_abonman']:>6,d} TL".replace(',', '.'))
    print(f"  • Sosyal & Kişisel Giderler : {k['sosyal_ve_kisisel']:>6,d} TL".replace(',', '.'))
    print("-" * 70)
    print(f"💵 TAHMİNİ TOPLAM AYLIK : {res['tahmini_aylik_toplam_tl']:,d} TL / Ay".replace(',', '.'))
    print(f"\n💡 Not: {res['ogrenci_butce_yorumu']}")
    print("=" * 70)

def cmd_wizard(rehber, args):
    """Terminalde interaktif tercih danışmanlığı sihirbazı."""
    print_banner()
    print("🎯 İNTERAKTİF TERCİH SİHİRBAZINA HOŞ GELDİNİZ!\n")
    print("Birkaç soruya cevap vererek sana en uygun kampüsleri bulalım:\n")

    try:
        sehir = input("1. Tercih etmek istediğin belirli bir il/bölge var mı? (Boş bırakılabilir): ").strip()
        tur = input("2. Üniversite türü tercihi? [1: Devlet, 2: Vakıf, 3: Fark Etmez] (Varsayılan: 3): ").strip()
        oncelikler = input("3. Senin için en kritik öncelikler neler? (Örn: metro, deniz, ucuz kira, 7/24 kütüphane, mühendislik): ").strip()
        
        tur_secim = ""
        if tur == "1":
            tur_secim = "devlet"
        elif tur == "2":
            tur_secim = "vakıf"

        soru_parcalari = []
        if sehir:
            soru_parcalari.append(sehir)
        if tur_secim:
            soru_parcalari.append(tur_secim)
        if oncelikler:
            soru_parcalari.append(oncelikler)

        birlestirilmis_soru = " ".join(soru_parcalari) if soru_parcalari else "yüksek puanlı en iyi kampüsler"
        
        print("\n🔍 Analiz yapılıyor...")
        advisor = TercihDanismani(rehber)
        results = advisor.danis(birlestirilmis_soru, top_k=5)
        
        print(f"\n🎉 Senin Kriterlerine En Uygun {len(results)} Kampüs:\n")
        for i, r in enumerate(results, 1):
            print(f"{i}. 🏛️  {r['kampus']} (Uyum: {r['uyum_yuzdesi']})")
            print(f"   📍 {r['sehir']} - {r['tur']} (⭐ {r['puan_sayisal']}/5)")
            if r['eslesen_kriterler']:
                print(f"   🎯 {', '.join(r['eslesen_kriterler'])}")
            if r['ogrenci_notu']:
                print(f"   💬 \"{r['ogrenci_notu'][:120]}...\"")
            print("-" * 60)
    except (KeyboardInterrupt, EOFError):
        print("\nSihirbaz iptal edildi.")

def cmd_export(rehber, args):
    fmt = args.format or "json"
    out = args.output
    if not out:
        out = f"kampusler_export.{fmt}"
    res = rehber.export(format=fmt, output_path=out)
    print(res)

def cmd_validate():
    print("🔍 Depo bütünlüğü, dosya yapısı ve bağlantıları doğrulanıyor...")
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
    print(f"  • Toplam taranan Markdown dosya : {checked_files}")
    print(f"  • Kırık bağlantı sayısı         : {broken}")
    if broken == 0:
        print("  ✓ TÜM BAĞLANTILAR GEÇERLİ! Depo 100% sağlıklı.")
    else:
        sys.exit(1)

def cmd_serve(args):
    port = args.port
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(root)
    rehber = KampusRehberi()
    if not args.no_browser:
        webbrowser.open(f"http://localhost:{port}/web/index.html")
    run_api_server(port=port, rehber=rehber)

def main():
    parser = argparse.ArgumentParser(
        prog="kampus-rehberi",
        description="Türkiye Kampüs Rehberi CLI ve Akıllı Tercih Motoru"
    )
    subparsers = parser.add_subparsers(dest="subcommand", help="Komutlar")

    subparsers.add_parser("stats", help="Genel depo ve kampüs istatistikleri")

    search_p = subparsers.add_parser("search", help="Kampüs ara ve filtrele")
    search_p.add_argument("query", nargs="?", default="", help="Arama metni")
    search_p.add_argument("--city", help="Şehir / İl filtresi")
    search_p.add_argument("--type", help="Tür filtresi (Devlet / Vakıf)")
    search_p.add_argument("--min-rating", type=float, help="Minimum puan (örn: 4.5)")
    search_p.add_argument("--sort", choices=["default", "rating_desc", "rating_asc", "title_asc", "city_asc"], help="Sıralama")
    search_p.add_argument("--limit", type=int, default=15, help="Maksimum listelenecek sonuç")

    city_p = subparsers.add_parser("city", help="Şehre göre yerleşkeleri listele")
    city_p.add_argument("city", help="Plaka kodu (örn: 06) veya şehir adı")

    top_p = subparsers.add_parser("top", help="En yüksek puanlı yerleşkeleri listele")
    top_p.add_argument("-n", type=int, default=10, help="Kaç kampüs listelensin")
    top_p.add_argument("--city", help="Belirli bir ildeki en iyiler")

    subparsers.add_parser("random", help="Rastgele bir kampüs kartı keşfet")

    compare_p = subparsers.add_parser("compare", help="İki kampüsü kıyasla")
    compare_p.add_argument("campus1", help="1. Kampüs ID'si")
    compare_p.add_argument("campus2", help="2. Kampüs ID'si")

    ask_p = subparsers.add_parser("ask", help="Akıllı tercih danışmanına sor")
    ask_p.add_argument("question", help="Sorunuz (örn: 'Deniz kıyısında olan mühendislikler')")
    ask_p.add_argument("--top-k", type=int, default=5, help="Döndürülecek sonuç sayısı")

    budget_p = subparsers.add_parser("budget", help="Bir ildeki tahmini öğrenci yaşam maliyetini hesapla")
    budget_p.add_argument("city", help="Şehir adı veya plaka (örn: 'Eskisehir' veya '06')")
    budget_p.add_argument("--housing", choices=["kyk", "shared_flat", "studio", "private_dorm"], default="kyk", help="Barınma tipi")
    budget_p.add_argument("--meals", type=int, default=1, help="Günde kampüste yenilen öğün sayısı")
    budget_p.add_argument("--lifestyle", choices=["budget", "moderate", "comfortable"], default="moderate", help="Yaşam tarzı")

    subparsers.add_parser("wizard", help="İnteraktif adım adım tercih sihirbazı")

    export_p = subparsers.add_parser("export", help="Kampüs verilerini dışa aktar")
    export_p.add_argument("--format", choices=["json", "csv", "md"], default="json", help="Çıktı formatı")
    export_p.add_argument("--output", "-o", help="Kaydedilecek dosya yolu")

    serve_p = subparsers.add_parser("serve", help="Web portalı ve REST API yerel sunucusunu başlat")
    serve_p.add_argument("--port", type=int, default=8000, help="Port numarası")
    serve_p.add_argument("--no-browser", action="store_true", help="Tarayıcıyı otomatik açma")

    subparsers.add_parser("validate", help="Depodaki bağlantıları ve dosya bütünlüğünü doğrula")

    args = parser.parse_args()

    if not args.subcommand:
        parser.print_help()
        return

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
    elif args.subcommand == "top":
        cmd_top(rehber, args)
    elif args.subcommand == "random":
        cmd_random(rehber, args)
    elif args.subcommand == "compare":
        cmd_compare(rehber, args)
    elif args.subcommand == "ask":
        cmd_ask(rehber, args)
    elif args.subcommand == "budget":
        cmd_budget(rehber, args)
    elif args.subcommand == "wizard":
        cmd_wizard(rehber, args)
    elif args.subcommand == "export":
        cmd_export(rehber, args)

if __name__ == '__main__':
    main()
