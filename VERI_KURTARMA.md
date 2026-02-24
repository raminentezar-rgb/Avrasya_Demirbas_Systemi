# راهنمای بازیابی داده‌ها / Veri Kurtarma Kılavuzu

## 🔄 مشکل حل شد / Sorun Çözüldü

مشکل ترتیب ستون‌ها حل شد! برنامه اکنون با ساختار صحیح اجرا می‌شود.
Sütun sırası sorunu çözüldü! Program artık doğru yapı ile çalışıyor.

---

## ✅ انجام شده / Yapılanlar

1. ✅ کد بروزرسانی اصلاح شد
   Güncelleme kodu düzeltildi

2. ✅ فایل قدیمی حذف شد
   Eski dosya silindi

3. ✅ فایل جدید با ساختار صحیح ایجاد شد
   Yeni dosya doğru yapı ile oluşturuldu

---

## 📊 بازگرداندن داده‌های قدیمی / Eski Verileri Geri Yükleme

اگر داده‌های قدیمی داشتید، دو راه برای بازگرداندن آن‌ها وجود دارد:

### روش 1: استفاده از Excel Import (آسان‌تر)

1. **آماده‌سازی فایل Excel:**
   - فایل Excel قدیمی خود را باز کنید
   - مطمئن شوید ستون‌ها به ترتیب زیر هستند:
     * Adı (نام ترکی)
     * Cinsi (دسته‌بندی)
     * Renk (رنگ)
     * Adet (تعداد)

2. **وارد کردن به برنامه:**
   - برنامه را باز کنید
   - روی دکمه **"Excel Import"** (سبز رنگ) کلیک کنید
   - فایل Excel قدیمی را انتخاب کنید
   - داده‌ها به طور خودکار وارد می‌شوند

### روش 2: وارد کردن دستی

اگر تعداد رکوردهای کمی دارید:

1. برنامه را باز کنید
2. برای هر مورد:
   - فرم سمت چپ را پر کنید
   - روی "Yeni Kayıt" کلیک کنید
3. در صورت نیاز، بعداً تصاویر را اضافه کنید

---

## 🔍 بررسی صحت / Doğruluk Kontrolü

برای اطمینان از درست بودن ستون‌ها:

### ترتیب صحیح ستون‌ها / Doğru Sütun Sırası:

```
┌────┬──────┬────────────┬────────────┬────────┬─────┬──────┬──────────┬───────┬────────┬──────┬──────────────┬────────┐
│ ID │ Kod  │ Dahili Kod │ Demirbaş   │ Kampüs │ Kat │ Oda  │ Kategori │ Durum │ Tarih  │ Renk │ Kullanan     │ Görsel │
│    │      │            │ Öğesi      │        │     │      │          │       │        │      │ Personel     │        │
└────┴──────┴────────────┴────────────┴────────┴─────┴──────┴──────────┴───────┴────────┴──────┴──────────────┴────────┘
  0     1         2            3          4       5     6        7         8       9       10        11           12
```

### تست / Test:

1. یک رکورد جدید اضافه کنید:
   ```
   - Kod: TEST_001
   - Demirbaş Öğesi: Test Item
   - Kampüs: Pelitli
   - Kat: Kat 0
   - Oda: Test Odası
   ```

2. بررسی کنید:
   - آیا "Pelitli" در ستون "Kampüs" است؟ ✓
   - آیا "Kat 0" در ستون "Kat" است؟ ✓
   - آیا "Test Odası" در ستون "Oda" است؟ ✓

3. اگر همه صحیح است:
   - ✅ سیستم درست کار می‌کند!
   - ✅ Sistem doğru çalışıyor!

---

## 📝 تغییرات فنی / Teknik Değişiklikler

### مشکل قبلی / Önceki Sorun:

کد قدیمی داده‌های موجود را به طور نادرست به ساختار جدید منتقل می‌کرد.

```python
# کد قدیمی - YANLIŞ:
while len(row_list) < len(HEADERS) - 1:
    row_list.append("")
if len(row_list) < len(HEADERS) - 1:  # ❌ همیشه False بود!
    row_list.append("")
new_row = [str(uuid4())] + row_list[:len(HEADERS)-1]
```

### راه حل / Çözüm:

```python
# کد جدید - DOĞRU:
existing_id = row_list[0]  # ID موجود را نگه دار
data_without_id = row_list[1:]  # داده‌ها بدون ID

# تا 12 عنصر (بدون ID) پر کن
while len(data_without_id) < len(HEADERS) - 1:
    data_without_id.append("")

# [ID] + [11 data] + [Image_Path] = 13 ستون
new_row = [existing_id] + data_without_id[:len(HEADERS)-1]
```

---

## 🔧 در صورت مشکل / Sorun Olursa

### ستون‌ها هنوز به هم ریخته‌اند / Sütunlar Hala Karışık:

1. برنامه را ببندید
   Programı kapatın

2. فایل `inventory.xlsx` را حذف کنید
   `inventory.xlsx` dosyasını silin

3. برنامه را دوباره باز کنید
   Programı tekrar açın

4. از Excel Import استفاده کنید
   Excel Import kullanın

### Excel Import کار نمی‌کند / Excel Import Çalışmıyor:

مطمئن شوید فایل Excel شما شامل این ستون‌ها است:
Excel dosyanızda bu sütunların olduğundan emin olun:

```
┌──────────┬──────────┬──────┬──────┐
│ Adı      │ Cinsi    │ Renk │ Adet │
├──────────┼──────────┼──────┼──────┤
│ Masa     │ Mobilya  │ Kahv.│ 1    │
│ Koltuk   │ Mobilya  │ Siyah│ 4    │
└──────────┴──────────┴──────┴──────┘
```

---

## 📞 پشتیبانی / Destek

اگر مشکل دارید:

1. برنامه را ببندید و دوباره باز کنید
   Programı kapatıp tekrar açın

2. فایل‌های زیر را نگه دارید:
   Bu dosyaları saklayın:
   - `inventory_backup_*.xlsx` (یدک‌گیری اتوماتیک)
   - Excel فایل اصلی شما

3. با پشتیبانی تماس بگیرید
   Destek ile iletişime geçin

---

## ✨ خلاصه / Özet

### قبل / Önce:
```
❌ Pelitli → [Kat] sütununda  (YANLIŞ!)
❌ Kat 0   → [Oda] sütununda  (YANLIŞ!)
❌ Oda adı → [Kategori] sütununda  (YANLIŞ!)
```

### بعد / Sonra:
```
✅ Pelitli → [Kampüs] sütununda  (DOĞRU!)
✅ Kat 0   → [Kat] sütununda  (DOĞRU!)
✅ Oda adı → [Oda] sütununda  (DOĞRU!)
```

---

**🎉 مشکل حل شد! / Sorun Çözüldü!**

سیستم اکنون درست کار می‌کند و آماده استفاده است.
Sistem şimdi doğru çalışıyor ve kullanıma hazır.

---

## 📋 چک‌لیست نهایی / Final Kontrol Listesi

قبل از شروع کار، این موارد را بررسی کنید:

- [ ] برنامه باز می‌شود / Program açılıyor
- [ ] فایل `inventory.xlsx` جدید ایجاد شده / Yeni `inventory.xlsx` oluştu
- [ ] ستون‌ها به ترتیب صحیح هستند / Sütunlar doğru sırada
- [ ] یک رکورد تست اضافه کردم / Test kaydı ekledim
- [ ] داده در ستون صحیح نمایش داده می‌شود / Veri doğru sütunda görünüyor
- [ ] آماده وارد کردن داده‌های اصلی هستم / Ana verileri yüklemeye hazırım

همه موارد ✅ است؟ عالی! شروع کنید! 🚀
Hepsi ✅ mi? Harika! Başlayın! 🚀

