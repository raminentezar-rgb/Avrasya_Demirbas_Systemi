# AVRASYA ÜNİVERSİTESİ DEMİRBAŞ SİSTEMİ
## GÖRSEL YÜKLEME ÖZELLİĞİ KILAVUZU

### 🎯 YENİ ÖZELLİKLER

Bu güncelleme ile demirbaş sistemine **görsel yükleme ve görüntüleme** özellikleri eklenmiştir.

---

## 📌 YENİ EKLENMİŞ ÖZELLİKLER

### 1. **Görsel Yükleme (Resim Yüklü)**
- Her demirbaş için fotoğraf yükleyebilirsiniz
- Desteklenen formatlar: PNG, JPG, JPEG, GIF, BMP
- Görseller otomatik olarak `images` klasöründe saklanır
- Her demirbaş için benzersiz dosya adı oluşturulur

### 2. **Görsel Görüntüleme (Görseli Göster)**  
- Yüklenen görselleri büyük pencerede görüntüleyebilirsiniz
- Görsel otomatik olarak boyutlandırılır
- Demirbaş bilgileri ile birlikte gösterilir

### 3. **Görsel Silme**
- İstenmeyen görseller silinebilir
- Güvenlik için onay penceresi çıkar

---

## 🎨 KULLANIM KILAVUZU

### 📤 GÖRSEL YÜKLEME ADIMLARI

1. **Demirbaş Seçimi**
   - Ana tabloda görseli yüklemek istediğiniz demirbaşı seçin
   - Satıra tıklayarak seçim yapın

2. **Görsel Yükle Butonuna Tıklayın**
   - Orta panelde "Görsel İşlemleri" bölümünü bulun
   - Turuncu renkli **"Görsel Yükle"** butonuna tıklayın

3. **Dosya Seçimi**
   - Açılan pencereden yüklemek istediğiniz resmi seçin
   - Sadece resim dosyaları gösterilir (.png, .jpg, .jpeg, .gif, .bmp)

4. **Yükleme Onayı**
   - Dosya otomatik olarak kopyalanır ve kaydedilir
   - Başarı mesajı görüntülenir
   - Görsel otomatik olarak açılır

### 👁️ GÖRSEL GÖRÜNTÜLEME ADIMLARI

1. **Demirbaş Seçimi**
   - Görseli görüntülemek istediğiniz demirbaşı seçin

2. **Görseli Göster Butonuna Tıklayın**
   - Turuncu renkli **"Görseli Göster"** butonuna tıklayın

3. **Görsel Penceresi**
   - Yeni bir pencere açılır
   - Görsel ve demirbaş bilgileri görüntülenir
   - İsterseniz "Görseli Sil" butonuyla görseli kaldırabilirsiniz

### 🗑️ GÖRSEL SİLME

1. Görseli görüntüleyin
2. Pencerenin altındaki kırmızı **"Görseli Sil"** butonuna tıklayın
3. Onay mesajında **"Evet"** seçin
4. Görsel hem dosya sisteminden hem de veritabanından silinir

---

## 🖥️ ARAYÜZ YERLEŞİMİ

### Orta Panel - İşlemler Bölümü

```
┌─────────────────────────────────┐
│   QR Kod İşlemleri              │
├─────────────────────────────────┤
│  [QR Kod Göster]                │
│  [Tüm QR Kodlar]                │
├─────────────────────────────────┤
│   Görsel İşlemleri  ⭐ YENİ     │
├─────────────────────────────────┤
│  [Görsel Yükle] [Görseli Göster]│
└─────────────────────────────────┘
```

### Ana Tablo

Tabloya yeni **"Görsel"** sütunu eklenmiştir:

| ID | Kod | Dahili Kod | ... | Renk | Kullanan Personel | **Görsel** ⭐ |
|----|-----|------------|-----|------|-------------------|---------------|
| ... | ... | ... | ... | ... | ... | ✓/✗ |

- ✓ işareti: Görsel mevcut
- Boş: Görsel yok

---

## 📂 DOSYA YAPISI

### Yeni Oluşturulan Klasör

```
DDD/
├── Avrasya_Demirbas_Sistemi.py
├── inventory.xlsx
├── barcodes/
├── qrcodes/
└── images/          ⭐ YENİ KLASÖR
    ├── item_KOD123.png
    ├── item_KOD456.jpg
    └── ...
```

### Görsel Dosya Adlandırma

- Format: `item_[DEMIRBAŞ_KODU].[uzantı]`
- Örnek: `item_PEL_MASA_1.jpg`
- Her demirbaş için benzersiz dosya adı garantilidir

---

## 🔧 TEKNİK DETAYLAR

### Veritabanı Değişiklikleri

Excel dosyasına yeni sütun eklenmiştir:

**HEADERS:**
```python
[
  "ID", "Code", "Internal_Code", "Inventory_Item", 
  "Campus", "Floor", "Room", "Category", "Status", 
  "Date", "Color", "Turkish_Name", "Image_Path" ⭐
]
```

### Yeni Fonksiyonlar

1. **`upload_item_image()`**
   - Görsel yükleme işlemini yönetir
   - Dosya kopyalama ve veritabanı güncelleme

2. **`show_item_image()`**
   - Görseli yeni pencerede gösterir
   - Silme özelliği içerir

3. **`update_item_image_path(item_id, image_path)`**
   - Veritabanında görsel yolu günceller

### Görsel İşleme

- **Otomatik Boyutlandırma:** Görseller 550x450 piksel içinde orantılı olarak küçültülür
- **Format Desteği:** PNG, JPG, JPEG, GIF, BMP
- **Kalite Koruma:** LANCZOS algoritması ile yeniden boyutlandırma

---

## ⚠️ ÖNEMLİ NOTLAR

### ✅ Yapılması Gerekenler

1. **İlk Kullanımda**
   - Program ilk çalıştırıldığında `images` klasörü otomatik oluşturulur
   - Mevcut kayıtların "Görsel" alanı boş olacaktır

2. **Görsel Boyutu**
   - Çok büyük görseller (10MB+) yavaşlığa sebep olabilir
   - Önerilen maksimum boyut: 5MB

3. **Dosya Adları**
   - Türkçe karakterler ve özel karakterler desteklenir
   - Sistem otomatik olarak güvenli dosya adları oluşturur

### ❌ Dikkat Edilmesi Gerekenler

1. **Manuel Dosya Silme**
   - `images` klasöründeki dosyaları manuel olarak silmeyin
   - Mutlaka program içinden silin

2. **Dosya Taşıma**
   - Görselleri başka bir klasöre taşımayın
   - Aksi halde görsel bulunamaz hatası alırsınız

3. **Veritabanı Bağlantısı**
   - Her görsel demirbaş ID'si ile ilişkilendirilmiştir
   - Demirbaş silinirse görsel de silinmelidir

---

## 🐛 SORUN GİDERME

### Görsel Yüklenemiyor

**Sorun:** "Görsel yükleme hatası" mesajı alıyorum

**Çözüm:**
1. Dosya formatını kontrol edin (PNG, JPG, etc.)
2. Dosya boyutunun çok büyük olmadığından emin olun
3. Dosya yolunda Türkçe karakter olmamasına dikkat edin
4. `images` klasörü yazma izinleri kontrol edin

### Görsel Görüntülenemiyor

**Sorun:** "Bu öğe için görsel bulunamadı" mesajı alıyorum

**Çözüm:**
1. Önce görsel yüklenmiş olduğundan emin olun
2. `images` klasöründe dosyanın var olduğunu kontrol edin
3. Excel dosyasını açıp "Image_Path" sütununu kontrol edin

### Excel Dosyası Hatalı

**Sorun:** Program açılırken hata veriyor

**Çözüm:**
1. Eski `inventory.xlsx` dosyasını yedekleyin
2. Dosyayı silin
3. Programı yeniden başlatın (otomatik yeni dosya oluşturulur)
4. Excel import özelliğini kullanarak verileri geri yükleyin

---

## 📊 ÖRNEK KULLANIM SENARYOSU

### Senaryo: Ofis Masası için Görsel Ekleme

1. **Kayıt Oluşturma**
   ```
   - Kod: PEL_MASA_001
   - Demirbaş Öğesi: Office Desk
   - Kullanan Personel: Ahmet Yılmaz
   - Kampüs: Pelitli
   - Oda: YAZI İŞLERİ
   ```

2. **Masanın Fotoğrafını Çekin**
   - Cep telefonu veya kamera ile fotoğraf çekin
   - Fotoğrafı bilgisayara aktarın

3. **Görseli Sisteme Yükleyin**
   - Tablodan "PEL_MASA_001" kaydını seçin
   - "Görsel Yükle" butonuna tıklayın
   - Fotoğrafı seçin
   - Yükleme tamamlandı!

4. **Kontrol**
   - "Görseli Göster" ile fotoğrafı görüntüleyin
   - QR kod oluşturarak masaya yapıştırın
   - QR kod ile tüm bilgilere ulaşılabilir

---

## 🚀 GELİŞMİŞ ÖZELLİKLER

### Toplu Görsel Yükleme (Gelecek Güncelleme)

Planlanmış özellikler:
- Birden fazla görseli aynı anda yükleme
- Excel'den görsel yollarını import etme
- Görsel galerisi modunda görüntüleme

### Görsel Düzenleme

Planlanmış özellikler:
- Görsel düzenleme (kırpma, döndürme)
- Thumbnail oluşturma
- Filigran ekleme

---

## 📞 DESTEK ve İLETİŞİM

**Programcı:** Ramin Entezar  
**Kurum:** Avrasya Üniversitesi  
**Sürüm:** 2.1 - Görsel Destekli  
**Güncelleme Tarihi:** 2025

### Yardım Almak İçin

1. Programdaki **"Hakkında"** bölümünü inceleyin
2. Bu kılavuzu dikkatlice okuyun
3. Hata mesajlarını kaydedin
4. Teknik destek ile iletişime geçin

---

## ✨ ÖZELLİK LİSTESİ

### Görsel İşlemleri

- ✅ Görsel yükleme
- ✅ Görsel görüntüleme
- ✅ Görsel silme
- ✅ Otomatik dosya adlandırma
- ✅ Otomatik boyutlandırma
- ✅ Format desteği (PNG, JPG, GIF, BMP)
- ✅ Veritabanı entegrasyonu
- ✅ Kullanıcı dostu arayüz
- ✅ Türkçe dil desteği
- ✅ Hata yönetimi

### Mevcut Özellikler (Değişmedi)

- ✅ Demirbaş kayıt sistemi
- ✅ QR kod oluşturma
- ✅ Excel import/export
- ✅ Filtreleme ve arama
- ✅ Raporlama
- ✅ Grafikler
- ✅ Yedekleme

---

## 🎓 KULLANIM İPUÇLARI

### En İyi Uygulamalar

1. **Kaliteli Fotoğraflar**
   - İyi ışıklandırma altında çekin
   - Nesneyi merkeze alın
   - Net ve odaklanmış fotoğraf kullanın

2. **Düzenli Güncelleme**
   - Demirbaşların durumu değiştiğinde görsel güncelleyin
   - Hasar durumunda yeni fotoğraf ekleyin

3. **Sistematik İsimlendirme**
   - Demirbaş kodlarını anlamlı tutun
   - Görsel dosyaları otomatik sistemle yönetin

4. **Yedekleme**
   - `images` klasörünü düzenli yedekleyin
   - Excel dosyası ile birlikte tutun

### Hızlı Erişim

**Klavye Kısayolları (Gelecek güncelleme):**
- `Ctrl+U`: Görsel Yükle
- `Ctrl+V`: Görseli Göster
- `Delete`: Görseli Sil

---

## 📝 SÜRÜM NOTLARI

### Versiyon 2.1 (Şubat 2025)

**Yeni Özellikler:**
- ✨ Görsel yükleme sistemi
- ✨ Görsel görüntüleme penceresi
- ✨ Görsel silme özelliği
- ✨ Image_Path veritabanı alanı
- ✨ İki yeni buton (Görsel Yükle, Görseli Göster)
- ✨ Otomatik images klasörü oluşturma

**Değişiklikler:**
- 📊 Tabloya "Görsel" sütunu eklendi
- 🔧 HEADERS yapısı güncellendi (13 alan)
- 🔧 save_record() fonksiyonu güncellendi
- 🔧 save_edited() fonksiyonu güncellendi
- 🔧 Excel import fonksiyonları güncellendi

**Düzeltmeler:**
- 🐛 Görsel yolu koruması (edit sırasında)
- 🐛 Veritabanı uyumluluğu
- 🐛 Türkçe karakter desteği

---

## 🎯 BAŞARI KONTROL LİSTESİ

İlk kullanımda şunları test edin:

- [ ] Program normal açılıyor mu?
- [ ] `images` klasörü oluştu mu?
- [ ] Tabloda "Görsel" sütunu görünüyor mu?
- [ ] Yeni kayıt ekleyebiliyor musunuz?
- [ ] Bir kayıt seçip görsel yükleyebiliyor musunuz?
- [ ] Yüklenen görsel görüntüleniyor mu?
- [ ] Görseli silme özelliği çalışıyor mu?
- [ ] QR kod özellikleri hala çalışıyor mu?
- [ ] Excel import çalışıyor mu?

Tüm maddeler ✅ ise sistem hazır!

---

**🎉 Başarılar Dileriz!**

> Bu özellik, Avrasya Üniversitesi Demirbaş Takip Sistemini daha kullanışlı ve modern hale getirmek için eklenmiştir.

