# 🎓 Türkiye Kampüs Rehberi (`turkiye-kampus-rehberi`)

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](./CONTRIBUTING.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](./LICENSE)
[![81 İl Kapsamı](https://img.shields.io/badge/Kapsam-81%20%C4%B0l%20%2F%20208%2B%20%C3%9Cniversite-8a2be2?style=flat-square)](#-81-il-hızlı-erişim-ve-üniversite-rehberi-indeksi)
[![Hacktoberfest](https://img.shields.io/badge/Hacktoberfest-Participating-orange.svg?style=flat-square)](#)
[![Katkıda Bulunanlar](https://img.shields.io/github/contributors/bahattinyunus/turkiye-kampus-rehberi.svg?style=flat-square)](https://github.com/bahattinyunus/turkiye-kampus-rehberi/graphs/contributors)

Türkiye'deki üniversitelerin, fakültelerin, merkez yerleşkelerin ve ilçe meslek yüksekokullarının (MYO) **gerçek yüzünü** yansıtan; öğrenciden öğrenciye, kitle kaynaklı (crowdsourced) ve filtresiz tercih rehberi.

---

## 📖 Manifesto: Neden Buradayız?

YKS tercih dönemi, adaylar için bir bilinmezlikler okyanusudur. Üniversitelerin resmi web siteleri; her zaman güneşli kampüs fotoğrafları, en yeni laboratuvarlar ve gülümseyen öğrenci stok görselleriyle doludur. Ancak gerçek hayat her zaman o fotoğraflardaki gibi değildir:

* Kampüs şehre 30 kilometre uzaklıkta bir dağın başında mı?
* KYK yurtları kampüse yürüme mesafesinde mi yoksa sabahları 45 dakika otobüs/ring sırası mı bekleniyor?
* Of, Elmadağ, Menteşe, Biga, İsabeyli, Seyitler gibi yerleşkelerdeki öğrencilik hayatı merkez kampüslerle aynı imkanları sunuyor mu?
* Şehirde yerel halkın ve ev sahiplerinin öğrenciye yaklaşımı nasıl? Popüler öğrenci mahallelerinde (Görükle, Kötekli, Bosna Hersek, 100. Yıl, Bahçelievler, Serdivan, Talas, Atakum vb.) kiralar ne durumda?

Bu repo; farklı illerdeki KYK yurtlarında kalmış, Türkiye'nin dört bir yanındaki kampüslerin havasını solumuş öğrencilerin kolektif hafızasıdır. Amacımız, tercih yapacak adaylara **veriye dayalı, objektif ve şeffaf** bir rehber sunmaktır.

---

## 🗂️ Mimari ve Klasör Yapısı

Repo, Türkiye'nin **81 ilini** plaka kodlarıyla (`01-Adana` ... `81-Duzce`) ayırır. Her ilin içinde o şehrin genel öğrenci profilini özetleyen bir `README.md`, altında ilgili ilçeler ve ilçelerin altında ise o bölgedeki kampüs ve fakültelerin detaylı Markdown (`.md`) dosyaları bulunur.

```text
📦 turkiye-kampus-rehberi
 ┣ 📂 01-Adana
 ┃ ┣ 📜 README.md
 ┃ ┗ 📂 Saricam
 ┃   ┣ 📜 Cukurova-Uni-Balcali-Kampusu.md
 ┃   ┗ 📜 ATU-Merkez-Kampusu.md
 ┣ 📂 06-Ankara
 ┃ ┣ 📜 README.md
 ┃ ┣ 📂 Cankaya
 ┃ ┃ ┣ 📜 ODTU-Merkez-Kampusu.md
 ┃ ┃ ┣ 📜 Hacettepe-Beytepe-Kampusu.md
 ┃ ┃ ┗ 📜 Bilkent-Merkez-Kampusu.md
 ┃ ┣ 📂 Yenimahalle
 ┃ ┃ ┗ 📜 Gazi-Merkez-Kampusu.md
 ┃ ┗ 📂 Elmadag
 ┃   ┗ 📜 Ankara-Uni-Elmadag-MYO.md
 ┣ 📂 34-Istanbul
 ┃ ┣ 📜 README.md
 ┃ ┣ 📂 Sariyer
 ┃ ┃ ┗ 📜 ITU-Ayazaga-Kampusu.md
 ┃ ┣ 📂 Besiktas
 ┃ ┃ ┗ 📜 Bogazici-Guney-Kuzey-Kampusu.md
 ┃ ┗ 📂 Esenler
 ┃   ┗ 📜 YTU-Davutpasa-Kampusu.md
 ┣ 📂 48-Mugla
 ┃ ┣ 📜 README.md
 ┃ ┣ 📂 Mentese
 ┃ ┃ ┗ 📜 MSKU-Kotekli-Kampusu.md
 ┃ ┗ 📂 Bodrum
 ┃   ┗ 📜 MSKU-Denizcilik-Fakultesi.md
 ┣ 📂 61-Trabzon
 ┃ ┣ 📜 README.md
 ┃ ┣ 📂 Ortahisar
 ┃ ┃ ┗ 📜 KTU-Merkez.md
 ┃ ┗ 📂 Of
 ┃   ┗ 📜 KTU-Of-Teknoloji-Fakultesi.md
 ┣ 📜 README.md
 ┣ 📜 TEMPLATE.md
 ┣ 📜 CONTRIBUTING.md
 ┣ 📜 CODE_OF_CONDUCT.md
 ┗ 📜 LICENSE
```

---

## 🗺️ 81 İl Hızlı Erişim ve Üniversite Rehberi İndeksi

Aşağıdaki tablodan incelemek istediğiniz ilin klasörüne doğrudan gidebilir, şehir içi ulaşım/barınma özetini ve ilçe bazlı kampüs analizlerini okuyabilirsiniz:

| Plaka | İl Klasörü | Şehirdeki Başlıca Üniversiteler | Öne Çıkan Öğrenci Bölgeleri / Kampüsler |
| :---: | :--- | :--- | :--- |
| **01** | [📂 01-Adana](./01-Adana/README.md) | Çukurova Üniversitesi, Adana Alparslan Türkeş BTÜ | Balcalı (Sarıçam), Barajyolu, Çukurova |
| **02** | [📂 02-Adiyaman](./02-Adiyaman/README.md) | Adıyaman Üniversitesi | Altınşehir Mahallesi, Merkez, Kahta |
| **03** | [📂 03-Afyonkarahisar](./03-Afyonkarahisar/README.md) | Afyon Kocatepe Üni. (AKÜ), Afyonkarahisar Sağlık Bilimleri Üni. (AFSÜ) | ANS Kampüsü, Erenler Mahallesi, Sandıklı |
| **04** | [📂 04-Agri](./04-Agri/README.md) | Ağrı İbrahim Çeçen Üniversitesi (AİÇÜ) | Erzurum Yolu Merkez Kampüsü, Fırat Mah. |
| **05** | [📂 05-Amasya](./05-Amasya/README.md) | Amasya Üniversitesi | İpekköy, Yeşilırmak, Şeyhcui, Merzifon |
| **06** | [📂 06-Ankara](./06-Ankara/README.md) | ODTÜ, Hacettepe, Ankara Üni., Gazi, AYBÜ, Bilkent, TOBB ETÜ, Başkent, TEDÜ, Atılım, Çankaya | Beytepe, 100. Yıl, Bahçelievler, Cebeci, Beşevler, Gölbaşı, Elmadağ |
| **07** | [📂 07-Antalya](./07-Antalya/README.md) | Akdeniz Üniversitesi, Alanya Alaaddin Keykubat Üni. (ALKÜ), Antalya Bilim Üni. | Kültür Mahallesi, Gülveren, Konyaaltı, Alanya Kestel |
| **08** | [📂 08-Artvin](./08-Artvin/README.md) | Artvin Çoruh Üniversitesi (AÇÜ) | Seyitler Yerleşkesi, Çayağzı, Hopa, Arhavi |
| **09** | [📂 09-Aydin](./09-Aydin/README.md) | Aydın Adnan Menderes Üniversitesi (ADÜ) | Aytepe (Efeler), Zafer Mah., Nazilli İsabeyli, Kuşadası |
| **10** | [📂 10-Balikesir](./10-Balikesir/README.md) | Balıkesir Üniversitesi (BAÜN), Bandırma Onyedi Eylül Üniversitesi (BANÜ) | Çağış Kampüsü, Bahçelievler, Bandırma Merkez |
| **11** | [📂 11-Bilecik](./11-Bilecik/README.md) | Bilecik Şeyh Edebali Üniversitesi (BŞEÜ) | Gülümbe Kampüsü, Pelitözü, Bozüyük |
| **12** | [📂 12-Bingol](./12-Bingol/README.md) | Bingöl Üniversitesi | Selahaddin-i Eyyubi Mah., Merkez Kampüs |
| **13** | [📂 13-Bitlis](./13-Bitlis/README.md) | Bitlis Eren Üniversitesi (BEÜ) | Rahva Merkez Kampüsü, Tatvan, Ahlat |
| **14** | [📂 14-Bolu](./14-Bolu/README.md) | Bolu Abant İzzet Baysal Üniversitesi (BAİBÜ) | Gölköy Kampüsü, Karaköy, İzzet Baysal Cad., Gerede |
| **15** | [📂 15-Burdur](./15-Burdur/README.md) | Burdur Mehmet Akif Ersoy Üniversitesi (MAKÜ) | İstiklal Yerleşkesi, Bahçelievler, Bucak |
| **16** | [📂 16-Bursa](./16-Bursa/README.md) | Bursa Uludağ Üniversitesi (BUÜ), Bursa Teknik Üniversitesi (BTÜ), Mudanya Üni. | Görükle (Nilüfer), Mimar Sinan (Yıldırım), İnegöl |
| **17** | [📂 17-Canakkale](./17-Canakkale/README.md) | Çanakkale Onsekiz Mart Üniversitesi (ÇOMÜ) | Terzioğlu Kampüsü, Barbaros Mah., Kepez, Biga Ağaköy |
| **18** | [📂 18-Cankiri](./18-Cankiri/README.md) | Çankırı Karatekin Üniversitesi (ÇAKÜ) | Uluyazı Kampüsü, Kırkevler, Cumhuriyet Mah. |
| **19** | [📂 19-Corum](./19-Corum/README.md) | Hitit Üniversitesi | Kuzey Kampüsü, Güney Kampüsü, Bahçelievler, Sungurlu |
| **20** | [📂 20-Denizli](./20-Denizli/README.md) | Pamukkale Üniversitesi (PAÜ) | Kınıklı Kampüsü, Asmalıevler, Bağbaşı, Çivril |
| **21** | [📂 21-Diyarbakir](./21-Diyarbakir/README.md) | Dicle Üniversitesi | Sur Kampüsü, Kayapınar, Bağlar, Ergani |
| **22** | [📂 22-Edirne](./22-Edirne/README.md) | Trakya Üniversitesi | Balkan Yerleşkesi, Ayşekadın, Karaağaç, Keşan |
| **23** | [📂 23-Elazig](./23-Elazig/README.md) | Fırat Üniversitesi | Üniversite Mahallesi, Sürsürü, Mühendislik Kampüsü |
| **24** | [📂 24-Erzincan](./24-Erzincan/README.md) | Erzincan Binali Yıldırım Üniversitesi (EBYÜ) | Yalnızbağ Yerleşkesi, Fatih Mah., Kemaliye |
| **25** | [📂 25-Erzurum](./25-Erzurum/README.md) | Atatürk Üniversitesi (ATAÜNİ), Erzurum Teknik Üniversitesi (ETÜ) | Yakutiye Merkez Kampüs, Yıldızkent, Dadaşkent, Oltu |
| **26** | [📂 26-Eskisehir](./26-Eskisehir/README.md) | Anadolu Üniversitesi, Eskişehir Osmangazi Üni. (ESOGÜ), Eskişehir Teknik Üni. (ESTÜ) | Yunus Emre (Bağlar), Meşelik, İki Eylül |
| **27** | [📂 27-Gaziantep](./27-Gaziantep/README.md) | Gaziantep Üniversitesi (GAÜN), GİBTÜ, Hasan Kalyoncu Üni., Sanko Üni. | Üniversite Bulvarı (Şahinbey), Yeditepe, Karataş, Nizip |
| **28** | [📂 28-Giresun](./28-Giresun/README.md) | Giresun Üniversitesi (GRÜ) | Güre Yerleşkesi, Teyyaredüzü, Tirebolu, Bulancak |
| **29** | [📂 29-Gumushane](./29-Gumushane/README.md) | Gümüşhane Üniversitesi | Bağlarbaşı Kampüsü, Kelkit, Şiran |
| **30** | [📂 30-Hakkari](./30-Hakkari/README.md) | Hakkari Üniversitesi | Zeynel Bey (Çölemerik) Kampüsü, Yüksekova |
| **31** | [📂 31-Hatay](./31-Hatay/README.md) | Hatay Mustafa Kemal Üniversitesi (HMKÜ), İskenderun Teknik Üniversitesi (İSTE) | Tayfur Sökmen (Serinyol/Antakya), İskenderun Merkez |
| **32** | [📂 32-Isparta](./32-Isparta/README.md) | Süleyman Demirel Üniversitesi (SDÜ), Isparta Uygulamalı Bilimler Üni. (ISUBÜ) | Çünür Doğu/Batı Kampüsü, Fatih Mah., Kafeler Cad., Eğirdir |
| **33** | [📂 33-Mersin](./33-Mersin/README.md) | Mersin Üniversitesi (MEÜ), Tarsus Üniversitesi, Çağ Üni., Toros Üni. | Çiftlikköy (Yenişehir), Üniversite Cad., Tarsus |
| **34** | [📂 34-Istanbul](./34-Istanbul/README.md) | İTÜ, Boğaziçi, YTÜ, İÜ, İÜC, Marmara, GSÜ, MSGSÜ, Koç, Sabancı, Özyeğin, BAU, Yeditepe, TAÜ vb. | Ayazağa, Güney/Kuzey, Davutpaşa, Beyazıt, Avcılar, Göztepe/Maltepe |
| **35** | [📂 35-Izmir](./35-Izmir/README.md) | Ege Üni., Dokuz Eylül (DEÜ), İYTE, İKÇÜ, İzmir Bakırçay, İDÜ, İzmir Ekonomi, Yaşar | Bornova (Küçükpark), Buca (Tınaztepe), Urla (Gülbahçe), Çiğli, Seyrek |
| **36** | [📂 36-Kars](./36-Kars/README.md) | Kafkas Üniversitesi (KAÜ) | Paşaçayırı Kampüsü, Yenişehir, Sarıkamış |
| **37** | [📂 37-Kastamonu](./37-Kastamonu/README.md) | Kastamonu Üniversitesi | Kuzeykent Kampüsü, Tosya, Taşköprü |
| **38** | [📂 38-Kayseri](./38-Kayseri/README.md) | Erciyes Üniversitesi (ERÜ), Abdullah Gül Üni. (AGÜ), Kayseri Üni., Nuh Naci Yazgan | Talas (Mevlana Mah.), Melikgazi, Sümer Kampüsü |
| **39** | [📂 39-Kirklareli](./39-Kirklareli/README.md) | Kırklareli Üniversitesi (KLÜ) | Kayalı Kampüsü, Karakaş Mah., Lüleburgaz |
| **40** | [📂 40-Kirsehir](./40-Kirsehir/README.md) | Kırşehir Ahi Evran Üniversitesi (KAEÜ) | Bağbaşı Kampüsü, Cacabey, Kaman |
| **41** | [📂 41-Kocaeli](./41-Kocaeli/README.md) | Kocaeli Üniversitesi (KOÜ), Gebze Teknik Üniversitesi (GTÜ) | Umuttepe (Kabaoğlu), İzmit Merkez, Gebze Çayırova |
| **42** | [📂 42-Konya](./42-Konya/README.md) | Selçuk Üni., Necmettin Erbakan Üni. (NEÜ), Konya Teknik (KTÜN), KTO Karatay, KGTÜ | Bosna Hersek (Selçuklu), Köyceğiz (Meram), Alaeddin |
| **43** | [📂 43-Kutahya](./43-Kutahya/README.md) | Kütahya Dumlupınar Üniversitesi (DPÜ), Kütahya Sağlık Bilimleri Üni. (KSBÜ) | Evliya Çelebi Kampüsü, Germiyan, Tavşanlı, Simav |
| **44** | [📂 44-Malatya](./44-Malatya/README.md) | İnönü Üniversitesi, Malatya Turgut Özal Üniversitesi (MTÜ) | Bulgurlu/Battalgazi Merkez Kampüs, Yeşilyurt |
| **45** | [📂 45-Manisa](./45-Manisa/README.md) | Manisa Celal Bayar Üniversitesi (MCBÜ) | Muradiye Kampüsü, Uncubozköy, Turgutlu, Akhisar |
| **46** | [📂 46-Kahramanmaras](./46-Kahramanmaras/README.md) | Kahramanmaraş Sütçü İmam Üni. (KSÜ), Kahramanmaraş İstiklal Üni. (KİÜ) | Avşar Kampüsü (Onikişubat), Karacasu, Elbistan |
| **47** | [📂 47-Mardin](./47-Mardin/README.md) | Mardin Artuklu Üniversitesi (MAÜ) | Artuklu Kampüs Yerleşkesi, Yenişehir, Midyat |
| **48** | [📂 48-Mugla](./48-Mugla/README.md) | Muğla Sıtkı Koçman Üniversitesi (MSKÜ) | Kötekli (Menteşe), Bodrum, Fethiye, Marmaris, Milas |
| **49** | [📂 49-Mus](./49-Mus/README.md) | Muş Alparslan Üniversitesi (MAUN) | Güzeltepe Kampüsü, Kültür Mah., Malazgirt |
| **50** | [📂 50-Nevsehir](./50-Nevsehir/README.md) | Nevşehir Hacı Bektaş Veli Üni. (NEVÜ), Kapadokya Üniversitesi (KÜN) | 2000 Evler Mah., Ürgüp Mustafapaşa, Uçhisar |
| **51** | [📂 51-Nigde](./51-Nigde/README.md) | Niğde Ömer Halisdemir Üniversitesi (NOHÜ) | Bor Yolu Merkez Kampüsü, Aşağı Kayabaşı, Bor |
| **52** | [📂 52-Ordu](./52-Ordu/README.md) | Ordu Üniversitesi (ODÜ) | Cumhuriyet Kampüsü (Altınordu), Fatsa, Ünye |
| **53** | [📂 53-Rize](./53-Rize/README.md) | Recep Tayyip Erdoğan Üniversitesi (RTEÜ) | Zihni Derin (Fener), Çayeli, Ardeşen, Pazar |
| **54** | [📂 54-Sakarya](./54-Sakarya/README.md) | Sakarya Üniversitesi (SAÜ), Sakarya Uygulamalı Bilimler Üni. (SUBÜ) | Esentepe Kampüsü, Serdivan (Kemalpaşa/Mavi Durak), Sapanca |
| **55** | [📂 55-Samsun](./55-Samsun/README.md) | Ondokuz Mayıs Üniversitesi (OMÜ), Samsun Üniversitesi (SAMÜ) | Kurupelit (Atakum), Türkiş, Ballıca (19 Mayıs), Canik |
| **56** | [📂 56-Siirt](./56-Siirt/README.md) | Siirt Üniversitesi (SİÜ) | Kezer Yerleşkesi, Bahçelievler, Kurtalan |
| **57** | [📂 57-Sinop](./57-Sinop/README.md) | Sinop Üniversitesi (SNÜ) | Osmaniye/Korucuk Kampüsü, Gelincik, Boyabat, Gerze |
| **58** | [📂 58-Sivas](./58-Sivas/README.md) | Sivas Cumhuriyet Üniversitesi (SCÜ), Sivas Bilim ve Teknoloji Üni. (SBTÜ) | Cumhuriyet Merkez Kampüsü, Yenişehir, Gültepe |
| **59** | [📂 59-Tekirdag](./59-Tekirdag/README.md) | Tekirdağ Namık Kemal Üniversitesi (TNKÜ) | Değirmenaltı (Süleymanpaşa), Çorlu Mühendislik, Çerkezköy |
| **60** | [📂 60-Tokat](./60-Tokat/README.md) | Tokat Gaziosmanpaşa Üniversitesi (TOGÜ) | Taşlıçiftlik Kampüsü, Karşıyaka, Erbaa, Turhal, Zile |
| **61** | [📂 61-Trabzon](./61-Trabzon/README.md) | Karadeniz Teknik Üni. (KTÜ), Trabzon Üniversitesi (TRÜ), Avrasya Üni. | Kanuni Kampüsü (Kalkınma), Akçaabat Söğütlü, Of, Sürmene |
| **62** | [📂 62-Tunceli](./62-Tunceli/README.md) | Munzur Üniversitesi | Aktuluk Yerleşkesi, Atatürk Mah., Pertek |
| **63** | [📂 63-Sanliurfa](./63-Sanliurfa/README.md) | Harran Üniversitesi | Osmanbey Kampüsü, Yenişehir, Eyyübiye, Siverek |
| **64** | [📂 64-Usak](./64-Usak/README.md) | Uşak Üniversitesi | Bir Eylül Kampüsü, Kemalöz, Durak Mah. |
| **65** | [📂 65-Van](./65-Van/README.md) | Van Yüzüncü Yıl Üniversitesi (Van YYÜ) | Zeve Kampüsü (Tuşba), Maraş Cad., Erciş, Gevaş |
| **66** | [📂 66-Yozgat](./66-Yozgat/README.md) | Yozgat Bozok Üniversitesi (YOBÜ) | Erdoğan Akdağ Kampüsü, Bahçeşehir, Sorgun, Akdağmadeni |
| **67** | [📂 67-Zonguldak](./67-Zonguldak/README.md) | Zonguldak Bülent Ecevit Üniversitesi (BEUN) | Farabi Kampüsü (İncivez), Kozlu, Kdz. Ereğli, Çaycuma |
| **68** | [📂 68-Aksaray](./68-Aksaray/README.md) | Aksaray Üniversitesi (ASÜ) | Adana Yolu Kampüsü, Küçük Bölcek, Kafeler Cad. |
| **69** | [📂 69-Bayburt](./69-Bayburt/README.md) | Bayburt Üniversitesi | Dede Korkut Kampüsü, Baberti Külliyesi, Tuzcuzade |
| **70** | [📂 70-Karaman](./70-Karaman/README.md) | Karamanoğlu Mehmetbey Üniversitesi (KMÜ) | Yunus Emre Kampüsü, Üniversite Mah., Ermenek |
| **71** | [📂 71-Kirikkale](./71-Kirikkale/README.md) | Kırıkkale Üniversitesi (KKÜ) | Yahşihan Merkez Kampüsü, Yenişehir Mah., Keskin |
| **72** | [📂 72-Batman](./72-Batman/README.md) | Batman Üniversitesi | Batı Raman Kampüsü, Merkez Kampüs, Kültür Mah. |
| **73** | [📂 73-Sirnak](./73-Sirnak/README.md) | Şırnak Üniversitesi | Mehmet Emin Acar Kampüsü, Cizre, Silopi |
| **74** | [📂 74-Bartin](./74-Bartin/README.md) | Bartın Üniversitesi (BARÜ) | Kutlubey Kampüsü, Ağdacı Kampüsü, Çatmaca, Amasra |
| **75** | [📂 75-Ardahan](./75-Ardahan/README.md) | Ardahan Üniversitesi (ARÜ) | Yenisey Kampüsü, Karagöl Mah., Göle |
| **76** | [📂 76-Igdir](./76-Igdir/README.md) | Iğdır Üniversitesi | Şehit Bülent Yurtseven (Suveren) Kampüsü, Karaağaç |
| **77** | [📂 77-Yalova](./77-Yalova/README.md) | Yalova Üniversitesi | Merkez Yerleşke (Çınarcık Yolu), Çınarcık, Termal |
| **78** | [📂 78-Karabuk](./78-Karabuk/README.md) | Karabük Üniversitesi (KBÜ) | Demir Çelik Kampüsü, 100. Yıl Mah., Safranbolu |
| **79** | [📂 79-Kilis](./79-Kilis/README.md) | Kilis 7 Aralık Üniversitesi (KİYÜ) | Merkez Kampüs, Karataş Yerleşkesi, Mercidabık |
| **80** | [📂 80-Osmaniye](./80-Osmaniye/README.md) | Osmaniye Korkut Ata Üniversitesi (OKÜ) | Karacaoğlan Kampüsü (Fakıuşağı), Kadirli |
| **81** | [📂 81-Duzce](./81-Duzce/README.md) | Düzce Üniversitesi (DÜ) | Konuralp Merkez Kampüsü, Beçi, Akçakoca |

---

---

## 💻 Komut Satırı Aracı (CLI), JSON API ve Web Arayüzü

Rehbere yalnızca Markdown dosyaları üzerinden değil; terminalden, web arayüzünden veya kod içerisinden de erişebilirsiniz:

### 1. Terminal CLI (`scripts/cli.py`)
```bash
# Genel depo istatistiklerini görüntüle
python scripts/cli.py stats

# Kampüs, üniversite veya anahtar kelime ara (örn: metro, tıp, kyk)
python scripts/cli.py search "ODTÜ"
python scripts/cli.py search "metro"

# Şehir bazlı yerleşkeleri listele (plaka veya şehir adı ile)
python scripts/cli.py city 06
python scripts/cli.py city Izmir

# Depodaki tüm bağlantıların ve Markdown dosyalarının bütünlüğünü test et
python scripts/cli.py validate
```

### 2. Yapılandırılmış JSON API (`data/kampusler.json`)
Ed-Tech girişimleri, tercih robotları ve mobil uygulamalar için tüm Markdown rehberleri ayrıştırılarak yapılandırılmış JSON veritabanına dönüştürülmüştür:
* **Kampüs Veritabanı:** [`data/kampusler.json`](./data/kampusler.json) (250+ kampüsün metrikleri, puanları ve artıları/eksileri)
* **İstatistikler:** [`data/istatistikler.json`](./data/istatistikler.json)
* **Otomatik Üretim:** `python scripts/export_json.py`

### 3. Web Arayüzü (Açık Kaynak Kampüs Arama Motoru)
Depoda yer alan [`web/index.html`](./web/index.html) sayfasını doğrudan tarayıcınızda açarak tüm iller ve kampüsler arasında anlık filtreleme ve arama yapabilirsiniz (GitHub Pages uyumludur).

---

## 🔍 İçerik Kapsamı: Bir Kampüs Dosyasında Neler Var?

Repoya eklenen her `.md` dosyası belirli bir standardı takip eder ([`TEMPLATE.md`](./TEMPLATE.md)). Bir üniversite/kampüs incelenirken şu metrikler baz alınır:

1. **🚇 Ulaşım Ağı:** Şehir merkezine uzaklık, ring seferleri, otobüs/metro/tramvay entegrasyonu, öğrenci abonman ücretleri ve kış koşullarında ulaşım.
2. **🏠 Barınma ve Yurtlar:** KYK yurtlarının kapasitesi ve konumu, özel yurt fiyat bantları, popüler öğrenci mahalleleri ve güncel kira ortalamaları.
3. **🎓 Akademik & Fiziki Altyapı:** Kütüphane kapasitesi (Vize/final haftası 7/24 açık mı?), laboratuvar/atölye imkanları, internet (`eduroam`) hızı ve öğrenci kulüpleri.
4. **🍽️ Beslenme ve Kampüs Hayatı:** Yemekhane ücretleri, porsiyon doyuruculuğu, alternatif kafeteryalar, çarşı ve spor tesisleri.
5. **🌆 Şehir ve İlçe Dinamikleri:** Yerel halkın öğrenciye tutumu, sosyal etkinlikler, doğa/kamp/kültür imkanları, part-time iş/staj olanakları ve ilçenin merkeze göre dezavantajları.

---

## 🛠️ Nasıl Katkıda Bulunabilirim?

Bu repo tamamen açık kaynaktır ve senin deneyimlerine ihtiyacı var! Kendi üniversiteni, eski okulunu veya çok iyi bildiğin bir kampüsü ekleyebilir ya da mevcut verileri güncelleyebilirsin. Detaylı kurallar için [`CONTRIBUTING.md`](./CONTRIBUTING.md) dosyasına göz atabilirsin.

### Terminal/Git CLI ile Katkı (Önerilen)

```bash
# 1. Repoyu kendi bilgisayarına klonla
git clone https://github.com/bahattinyunus/turkiye-kampus-rehberi.git
cd turkiye-kampus-rehberi

# 2. Yeni bir branch (dal) oluştur
git checkout -b kampus-ekle/ktu-of-teknoloji

# 3. Şablon dosyasını ilgili klasöre kopyala
cp TEMPLATE.md 61-Trabzon/Of/KTU-Of-Teknoloji-Fakultesi.md

# 4. Dosyayı düzenle (Markdown formatında içini doldur)
code 61-Trabzon/Of/KTU-Of-Teknoloji-Fakultesi.md

# 5. Değişiklikleri kaydet ve Commit at
git add .
git commit -m "feat(61-Trabzon): KTÜ Of Teknoloji Fakültesi eklendi"

# 6. Branch'i pushla ve GitHub üzerinden PR oluştur
git push origin kampus-ekle/ktu-of-teknoloji
```

### GitHub Web Arayüzü Üzerinden Katkı (Hızlı Yöntem)

1. Sağ üstteki **Fork** butonuna bas.
2. İlgili il ve ilçe klasörüne git (Örn: `06-Ankara/Cankaya/`).
3. **Add File > Create New File** seçeneğine tıkla.
4. Dosya adını gir ve ana dizindeki [`TEMPLATE.md`](./TEMPLATE.md) içeriğini yapıştırıp doldur.
5. **Commit Changes** diyerek Pull Request (PR) yolla.

---

## ⚖️ İçerik Standartları (Code of Conduct)

Bu reponun kalbi **objektifliktir**. Detaylar için [`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md) dosyasını inceleyebilirsin.

* **❌ Yanlış:** "Bu okul çöp, hocalar berbat, yemekler yenmez."
* **✅ Doğru:** "Yemekhane 35 TL ancak öğlenleri 40 dakika sıra bekleniyor. Okulun kütüphanesi vize haftalarında yetersiz kalıyor, sabah 8'de yer tutmak gerekiyor."
* Küfür, hakaret, kurumsal karalama veya kişisel veri içeren hiçbir Pull Request kabul edilmeyecektir. Amacımız karalamak değil, şeffaf bir durum tespiti yapmaktır.

---

## 🚀 Proje Yol Haritası (Roadmap)

- [x] Temel depo mimarisinin ve klasör yapısının (81 İl) oluşturulması.
- [x] Standart Markdown şablonlarının ([`TEMPLATE.md`](./TEMPLATE.md), [`CONTRIBUTING.md`](./CONTRIBUTING.md), [`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md), `.github/ISSUE_TEMPLATE`) yazılması.
- [x] 81 ilin tamamı için şehir öğrenci rehberlerinin (`README.md`) ve merkez/ilçe kampüs analizlerinin oluşturulması.
- [x] **Web Entegrasyonu (Faz 2):** Markdown ve JSON verilerini okuyan, filtreleme ve arama destekli açık kaynak web arayüzü ([`web/index.html`](./web/index.html)).
- [x] **API Geliştirme (Faz 3):** Tercih botları ve Ed-Tech girişimleri için yapılandırılmış JSON veritabanı ([`data/kampusler.json`](./data/kampusler.json)) ve terminal CLI aracı ([`scripts/cli.py`](./scripts/cli.py)).
- [ ] **LLM Desteği (Faz 4):** Adayların doğal dilde *"Ankara'da KYK yurduna yürüme mesafesinde olan, kütüphanesi 7/24 açık bölümler"* şeklinde arama yapabileceği bir RAG (Retrieval-Augmented Generation) sisteminin kurulması.

---

## 📞 İletişim

Fikirlerin, hata bildirimlerin veya özel projelerin için repoda [Issue açabilir](https://github.com/bahattinyunus/turkiye-kampus-rehberi/issues) veya topluluk tartışmalarına ([Discussions](https://github.com/bahattinyunus/turkiye-kampus-rehberi/discussions)) katılabilirsin.

> *Resmi kataloglar binaları gösterir, açık kaynak kültürü ise o binaların içindeki gerçeği.*
