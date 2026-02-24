# 📸 GÖRSEL YÜKLEME - HIZLI BAŞVURU KARTI
## Quick Reference Card for Image Upload Feature

---

## 🚀 HIZLI BAŞLANGIÇ / Quick Start

### 1️⃣ Görsel Yükleme / Upload Image
```
1. Tabloda demirbaşı seçin    → Select item in table
2. "Görsel Yükle" tıklayın    → Click "Görsel Yükle"
3. Resim dosyasını seçin      → Choose image file
4. Otomatik gösterilir         → Shows automatically
```

### 2️⃣ Görsel Gösterme / Show Image
```
1. Demirbaşı seçin            → Select item
2. "Görseli Göster" tıklayın  → Click "Görseli Göster"
3. Yeni pencere açılır        → New window opens
```

### 3️⃣ Görsel Silme / Delete Image
```
1. Görseli göster             → Show image
2. "Görseli Sil" tıklayın     → Click "Görseli Sil"
3. Onaylayın                  → Confirm
```

---

## 🎨 BUTON KONUMLARI / Button Locations

```
┌─────────────────────────────────────┐
│         ORTA PANEL - CENTER         │
├─────────────────────────────────────┤
│  QR Kod İşlemleri                   │
│  ├─ QR Kod Göster                   │
│  └─ Tüm QR Kodlar                   │
├─────────────────────────────────────┤
│  Görsel İşlemleri  ⭐ YENİ          │
│  ├─ [Görsel Yükle]     (Turuncu)   │
│  └─ [Görseli Göster]   (Turuncu)   │
└─────────────────────────────────────┘
```

**Konum:** Orta panel, QR butonlarının altında
**Location:** Center panel, below QR buttons

---

## 📁 DOSYA BİLGİLERİ / File Information

### Desteklenen Formatlar / Supported Formats
✅ PNG  
✅ JPG / JPEG  
✅ GIF  
✅ BMP  

### Kaydedilir / Saved to
```
📂 DDD/
   └── 📂 images/
       ├── 📷 item_CODE1.png
       ├── 📷 item_CODE2.jpg
       └── ...
```

### Dosya Adı / Filename
```
item_[DEMİRBAŞ_KODU].[uzantı]
Örnek: item_PEL_MASA_001.jpg
```

---

## ⚙️ TEKNİK ÖZELLİKLER / Technical Features

| Özellik | Detay |
|---------|-------|
| **Maksimum Boyut** | Önerilir: 5MB |
| **Görüntüleme Boyutu** | 550x450 piksel (otomatik) |
| **Kalite** | LANCZOS algoritması |
| **Veritabanı** | Image_Path sütunu |
| **Türkçe Destek** | ✅ Tam destek |

---

## ⚠️ ÖNEMLİ KURALLAR / Important Rules

### ✅ YAPILMALI / DO
- ✅ Program üzerinden yükle
- ✅ Program üzerinden sil
- ✅ images klasörünü yedekle
- ✅ Kaliteli fotoğraf kullan

### ❌ YAPILMAMALI / DON'T
- ❌ Manuel dosya silme
- ❌ Dosya taşıma
- ❌ İsim değiştirme
- ❌ Çok büyük dosyalar (10MB+)

---

## 🔧 SORUN GİDERME / Troubleshooting

| Sorun | Çözüm |
|-------|-------|
| **Yüklenemiyor** | Format kontrol et (PNG/JPG) |
| **Görüntülenmiyor** | Önce yükle, sonra göster |
| **Bulunamadı hatası** | images klasörünü kontrol et |
| **Program hata veriyor** | inventory.xlsx'i sil, tekrar aç |

---

## 📊 TABLO SÜTUNLARI / Table Columns

```
┌────┬──────┬─────────┬───────┬──────────┐
│ ID │ Kod  │ ... ... │ Renk  │ Görsel ⭐│
├────┼──────┼─────────┼───────┼──────────┤
│... │ ... │ ... ... │ ...   │    ✓    │  ← Görsel var
│... │ ... │ ... ... │ ...   │         │  ← Görsel yok
└────┴──────┴─────────┴───────┴──────────┘
```

**✓** = Görsel mevcut  
**Boş** = Görsel yok

---

## 🎯 HIZLI KLAVYE İPUÇLARI / Quick Tips

1. **İyi Fotoğraf için:**
   - ✨ Gün ışığı kullan
   - ✨ Net çek
   - ✨ Merkeze odaklan

2. **Hızlı İş Akışı:**
   - 📸 Önce fotoğraf çek
   - 💾 Sonra kaydı oluştur
   - ⬆️ Görseli yükle
   - 🔍 QR kod oluştur

3. **Yedekleme:**
   - 💾 Excel + images klasörü
   - 🗓️ Düzenli olarak
   - ☁️ Bulut yedekleme önerilir

---

## 📞 YARDIM / Help

**Program İçinde:**
- 📖 "Hakkında" butonuna tıklayın
- 📄 GÖRSEL_YÜKLEME_KILAVUZU.md dosyasını okuyun

**Sorun mu var?**
1. Hata mesajını kaydet
2. Ekran görüntüsü al
3. Teknik destek ile iletişime geç

---

## ✨ ÖZELLİK ÖZETİ / Feature Summary

### Görsel İşlemleri
- ✅ Yükleme
- ✅ Görüntüleme
- ✅ Silme
- ✅ Otomatik kaydetme
- ✅ Otomatik boyutlandırma

### Avantajlar
- 🎯 Kolay kullanım
- 🔒 Güvenli
- 💾 Otomatik yönetim
- 🔍 QR entegrasyonu
- 🇹🇷 Türkçe destek

---

## 🎓 ÖRNEK SENARYO / Example Scenario

```
ADIM 1: Kayıt Oluştur
└─ Kod: PEL_KOLTUK_001
   Malzeme: Çalışma Koltuğu

ADIM 2: Fotoğraf
└─ 📸 Koltuğun fotoğrafını çek

ADIM 3: Yükle
└─ Kaydı seç → Görsel Yükle → Dosya seç

ADIM 4: Kontrol
└─ Görseli Göster ile kontrol et

ADIM 5: QR Kod
└─ QR kod oluştur ve yapıştır

✅ TAMAMLANDI!
```

---

## 📈 BAŞARI KRİTERLERİ / Success Criteria

Test listesi:
- [ ] Program açılıyor ✓
- [ ] images klasörü var ✓
- [ ] Görsel sütunu görünüyor ✓
- [ ] Görsel yükleyebilirim ✓
- [ ] Görsel gösterebilirim ✓
- [ ] Görsel silebilirim ✓
- [ ] QR kodlar çalışıyor ✓

---

**🎉 Tebrikler! Sistem Hazır!**

```
┌──────────────────────────────────┐
│  Avrasya Üniversitesi            │
│  Demirbaş Sistemi v2.1           │
│  Görsel Destekli                 │
│                                  │
│  Programcı: Ramin Entezar        │
│  © 2025                          │
└──────────────────────────────────┘
```

---

## 🆘 ACİL YARDIM / Emergency Help

### Program Açılmıyor?
```powershell
cd C:\Users\Avrasya\Desktop\DDD
del inventory.xlsx
python Avrasya_Demirbas_Sistemi.py
```

### Görsel Kayboldu?
```
1. images klasörünü kontrol et
2. Excel dosyasındaki Image_Path sütununu kontrol et
3. Gerekirse yeniden yükle
```

### Hepsi Bozuldu?
```
1. inventory.xlsx'i yedekle
2. images klasörünü yedekle
3. inventory.xlsx'i sil
4. Programı aç (yeni dosya oluşur)
5. Excel Import ile verileri geri yükle
```

---

**💡 İpucu:** Bu kartı yazdırıp masanıza koyun!  
**💡 Tip:** Print this card and keep it on your desk!

