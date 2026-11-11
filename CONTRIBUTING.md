# 🤝 Katkıda Bulunma Rehberi (Contributing Guide)

`turkiye-kampus-rehberi` projesine hoş geldin! Bu proje, Türkiye'deki 81 ilde bulunan tüm devlet ve vakıf üniversitelerinin merkez kampüslerini, fakültelerini ve ilçe meslek yüksekokullarını (MYO) öğrencilerin gerçek deneyimleriyle belgeleyen açık kaynaklı bir bilgi tabanıdır.

---

## 🎯 Katkı Türleri

1. **Yeni Kampüs / Fakülte / MYO Ekleme:** Henüz rehberde yer almayan bir yerleşkeyi `TEMPLATE.md` formatına uygun olarak ilgili il ve ilçe klasörüne ekleyebilirsin.
2. **Mevcut Verileri Güncelleme:** Yemekhane ücretleri, ulaşım hatları, kira ortalamaları, yeni açılan KYK yurtları veya kütüphane saatleri gibi bilgileri güncelleyebilirsin.
3. **Şehir Rehberi Geliştirme:** Her ilin ana klasöründe bulunan `README.md` dosyasındaki şehir içi ulaşım, öğrenci mahalleleri ve yaşam maliyeti bilgilerini zenginleştirebilirsin.
4. **Yazım ve Format Düzeltmeleri:** Kırık linkleri, tablo kaymalarını veya imla hatalarını düzeltebilirsin.

---

## 📂 Klasör ve Dosya İsimlendirme Kuralları

Reponun hem insanlar hem de ileride kurulacak Web/API ve RAG sistemleri tarafından kolayca okunabilmesi için standart bir dizin yapısı kullanıyoruz. Tüm iller `iller/` dizini altında toplanmıştır:

* **İl Klasörleri (`iller/` altında):** `iller/<PlakaKodu>-<IlAdi>` formatındadır ve Türkçe karakter **içermez**.
  * ✅ Doğru: `iller/06-Ankara`, `iller/34-Istanbul`, `iller/48-Mugla`, `iller/61-Trabzon`
  * ❌ Yanlış: `06-Ankara` (kök dizinde), `iller/6-Ankara`, `iller/34-İstanbul`
* **İlçe Klasörleri:** İlgili il klasörünün altında Türkçe karaktersiz PascalCase / Tireli formatta yer alır.
  * ✅ Doğru: `iller/48-Mugla/Mentese`, `iller/61-Trabzon/Ortahisar`, `iller/06-Ankara/Cankaya`
* **Kampüs Dosyaları:** `<UniversiteKisaAdiVeyaAdi>-<KampusVeyaFakulteAdi>.md` formatındadır.
  * ✅ Doğru: `ODTU-Merkez-Kampusu.md`, `KTU-Of-Teknoloji-Fakultesi.md`, `MSKU-Kotekli-Kampusu.md`

---

## 🛠️ Adım Adım Pull Request (PR) Süreci

### 1. Repoyu Forkla ve Klonla
```bash
git clone https://github.com/<kullanici-adin>/turkiye-kampus-rehberi.git
cd turkiye-kampus-rehberi
```

### 2. Yeni Bir Dal (Branch) Oluştur
Yapacağın değişikliği özetleyen anlamlı bir branch adı seç:
```bash
git checkout -b feat/35-izmir-ege-merkez
# veya güncelleme için:
git checkout -b update/06-ankara-odtu-yemekhane
```

### 3. Şablonu Kopyala ve Doldur
Ana dizindeki `TEMPLATE.md` dosyasını ilgili il ve ilçe klasörüne kopyala:
```bash
cp TEMPLATE.md iller/35-Izmir/Bornova/Ege-Universitesi-Merkez.md
```
Ardından tüm başlıkları **objektif, ölçülebilir ve güncel** verilerle doldur.

### 4. Commit Kuralları (Conventional Commits)
Commit mesajlarında şu önekleri kullanmaya özen göster:
* `feat:` Yeni bir kampüs, ilçe veya özellik eklendiğinde
* `update:` Mevcut bir kampüsün verileri (fiyat, ulaşım, yurt vb.) güncellendiğinde
* `docs:` Dokümantasyon veya README düzenlemelerinde
* `fix:` Yazım hatası veya kırık link düzeltmelerinde

```bash
git add .
git commit -m "feat(35-Izmir): Ege Üniversitesi Bornova Merkez Kampüsü eklendi"
git push origin feat/35-izmir-ege-merkez
```

### 5. Pull Request Aç
GitHub üzerinden kendi fork'una giderek **Compare & pull request** butonuna tıkla ve yaptığın katkıyı kısaca açıkla.

---

## ⚠️ Altın Kurallar

* **Objektif Ol:** "Bu okul berbat, sakın gelmeyin" gibi öznel ve karalayıcı ifadeler yerine; "Kampüs şehir merkezine 25 km uzaklıkta ve akşam 20.00'den sonra otobüs seferi bulunmuyor" gibi somut veriler sun.
* **Kişisel Veri Paylaşma:** Öğretim üyelerinin, personelin veya öğrencilerin özel bilgilerini, isimlerini hedef gösteren ifadeleri kesinlikle ekleme.
* **Şablon Bütünlüğünü Koru:** `TEMPLATE.md` içerisindeki ana başlıkları silme; böylece tüm kampüsler birbiriyle karşılaştırılabilir kalır.
