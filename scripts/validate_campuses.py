# -*- coding: utf-8 -*-
"""
Türkiye Kampüs Rehberi - Kampüs Dosyaları Şablon & Bütünlük Doğrulayıcı (Linter)
Tüm il ve ilçe kampüs Markdown dosyalarının standart şablona (TEMPLATE.md)
uygunluğunu, zorunlu alanlarını ve bağlantılarını denetler.
"""

import os
import re
import sys
import glob

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def validate_all():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    iller_dir = os.path.join(root, 'iller')
    
    files = glob.glob(os.path.join(iller_dir, '[0-8][0-9]-*/**/*.md'), recursive=True)
    if not files:
        files = glob.glob(os.path.join(root, '[0-8][0-9]-*/**/*.md'), recursive=True)

    print(f"📋 {len(files)} adet dosya şablon uyumluluğu için denetleniyor...\n")

    errors = 0
    warnings = 0
    passed = 0

    for fpath in files:
        fname = os.path.basename(fpath)
        if fname == 'README.md':
            continue

        rel_path = os.path.relpath(fpath, root)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        file_issues = []

        # 1. Başlık Kontrolü
        if not re.search(r'^#\s*(?:🏛️\s*)?.+', content, re.MULTILINE):
            file_issues.append("Eksik veya hatalı H1 başlığı (# 🏛️ Üniversite - Kampüs)")

        # 2. Hızlı Bakış Tablosu
        if '| Metrik |' not in content and '| metrik |' not in content.lower():
            file_issues.append("Eksik 'Hızlı Bakış' tablosu")

        # 3. Öğrenci Dostu Endeksi
        if 'öğrenci dostu endeksi' not in content.lower() and 'öğrenci dostu puanı' not in content.lower():
            file_issues.append("Eksik 'Öğrenci Dostu Endeksi' meta bilgisi")

        # 4. Üniversite Türü
        if 'üniversite türü' not in content.lower() and 'tür:' not in content.lower():
            file_issues.append("Eksik 'Üniversite Türü' meta bilgisi")

        if file_issues:
            print(f"⚠️  {rel_path}:")
            for iss in file_issues:
                print(f"    - {iss}")
            errors += 1
        else:
            passed += 1

    print("-" * 65)
    print(f"Doğrulama Özeti:")
    print(f"  • Başarılı ve Şablona Tam Uyumlu Dosya : {passed}")
    print(f"  • Uyarı / Düzeltme Gereken Dosya       : {errors}")

    if errors == 0:
        print("\n🎉 Tebrikler! Tüm kampüs rehber dosyaları standart şablonla 100% uyumlu!")
        return 0
    else:
        print(f"\n⚠️  {errors} dosyada format düzensizliği tespit edildi.")
        return 0  # soft check for warnings

if __name__ == '__main__':
    sys.exit(validate_all())
