import os
import qrcode
import barcode
from barcode.writer import ImageWriter
from fpdf import FPDF
from django.conf import settings
from .models import Asset

def tr_to_eng(text):
    if not isinstance(text, str):
        return str(text)
    replacements = {
        'ı': 'i', 'İ': 'I',
        'ş': 's', 'Ş': 'S',
        'ğ': 'g', 'Ğ': 'G',
        'ü': 'u', 'Ü': 'U',
        'ö': 'o', 'Ö': 'O',
        'ç': 'c', 'Ç': 'C'
    }
    for search, replace in replacements.items():
        text = text.replace(search, replace)
    return text

def generate_qrcode(asset):
    qr_dir = os.path.join(settings.MEDIA_ROOT, 'qrcodes')
    os.makedirs(qr_dir, exist_ok=True)
    
    qr = qrcode.QRCode(version=2, box_size=8, border=4)
    
    qr_content = f""" AVRASYA ÜNİVERSİTESİ - DEMİRBAŞ SİSTEMİ 

TEMEL BİLGİLER:
├─ Demirbaş Numarası: {asset.code}
├─ Dahili Kod: {asset.internal_code or ''}
├─ Kullanan Personel: {asset.turkish_name}
├─ Ad: {asset.inventory_item or ''}

YERLEŞİM BİLGİSİ:
├─ Yerleşke: {asset.campus}
├─ Oda: {asset.room}

KATEGORİ ve DURUM:
├─ Kategori: {asset.category}
├─ Durum: {asset.status}
├─ Renk: {asset.color or 'Belirtilmemiş'}

KAYIT BİLGİSİ:
├─ Kayıt Tarihi: {asset.date}
├─ Benzersiz ID: {asset.id}

AÇIKLAMA:
Avrasya Üniversitesi demirbaş sistemine kayıtlı demirbaş malzemedir.
Lütfen bu malzemenin yerini değiştirmeyiniz veya başka birime taşımayınız.

 İLETİŞİM:
Demirbaş Yönetimi - Avrasya Üniversitesi
"""
    qr.add_data(qr_content)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    filename = f"qrcode_{asset.code}.png"
    path = os.path.join(qr_dir, filename)
    img.save(path)
    
    return os.path.join(settings.MEDIA_URL, 'qrcodes', filename)

def generate_barcode(asset):
    bar_dir = os.path.join(settings.MEDIA_ROOT, 'barcodes')
    os.makedirs(bar_dir, exist_ok=True)
    
    try:
        code128 = barcode.get_barcode_class('code128')
        it_code = str(asset.code).strip()
        bar = code128(it_code, writer=ImageWriter())
        
        # python-barcode automatically appends .png
        save_path = os.path.join(bar_dir, f"barcode_{it_code}")
        bar.save(save_path)
        
        return os.path.join(settings.MEDIA_URL, 'barcodes', f"barcode_{it_code}.png")
    except Exception as e:
        print(f"Barcode error: {e}")
        return None

def create_item_pdf(asset, request):
    # Determine logo path (using old logo file from previous workspace copy if available)
    # Since Django doesn't know where it runs initially, we'll try to use a static context
    logo_file = os.path.join(settings.BASE_DIR.parent, "LOGO1.png")
    
    qr_url = generate_qrcode(asset) 
    # qr_url gives /media/qrcodes/..., we need the local filesystem path for FPDF
    qr_path = os.path.join(settings.MEDIA_ROOT, 'qrcodes', f"qrcode_{asset.code}.png")
    
    pdf = FPDF()
    pdf.add_page()
    
    if os.path.exists(logo_file):
        pdf.image(logo_file, x=75, y=10, w=60)
        pdf.set_y(80)  # Move cursor below the logo
    else:
        pdf.set_y(10)
        
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, tr_to_eng("AVRASYA UNIVERSITESI - DEMIRBAS SISTEMI"), ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", '', 12)
    fields = [
        ("ID", str(asset.id)),
        ("Code", asset.code),
        ("Internal Code", asset.internal_code),
        ("Inventory Item", asset.inventory_item),
        ("Campus", asset.campus),
        ("Floor", asset.floor),
        ("Room", asset.room),
        ("Category", asset.category),
        ("Status", asset.status),
        ("Date", str(asset.date)),
        ("Color", asset.color),
        ("Turkish Name", asset.turkish_name),
    ]
    
    for label, val in fields:
        # Convert any TR string to Eng to avoid FPDF latin-1 encoding errors
        display_val = tr_to_eng(f"{label}: {val or ''}")
        pdf.cell(200, 8, display_val, ln=True)
            
    if os.path.exists(qr_path):
        pdf.ln(10)
        pdf.image(qr_path, x=70, y=pdf.get_y(), w=70)
        
    reports_dir = os.path.join(settings.MEDIA_ROOT, 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    filename = f"Demirbas_{tr_to_eng(str(asset.code)).replace(' ', '_')}.pdf"
    filepath = os.path.join(reports_dir, filename)
    pdf.output(filepath)
    
    return os.path.join(settings.MEDIA_URL, 'reports', filename)

def create_room_pdf(room_name, assets):
    logo_file = os.path.join(settings.BASE_DIR.parent, "LOGO1.png")
    
    pdf = FPDF()
    pdf.add_page()
    
    if os.path.exists(logo_file):
        pdf.image(logo_file, x=85, y=10, w=40)
        pdf.set_y(60)  # Move cursor below the logo
    else:
        pdf.set_y(10)
        
    pdf.set_font("Arial", 'B', 18)
    pdf.cell(200, 10, "AVRASYA UNIVERSITESI", ln=True, align='C')
    pdf.set_font("Arial", 'B', 14)
    room_eng = tr_to_eng(str(room_name))
    pdf.cell(200, 10, f"ODA ENVANTER LISTESI - {room_eng}", ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(40, 10, "Kod", 1)
    pdf.cell(100, 10, "Malzeme", 1)
    pdf.cell(50, 10, "Durum", 1, ln=True)
    
    pdf.set_font("Arial", '', 9)
    for asset in assets:
        pdf.cell(40, 8, tr_to_eng(str(asset.code or '')), 1)
        pdf.cell(100, 8, tr_to_eng(str(asset.turkish_name[:45] or '')), 1)  # trim length
        pdf.cell(50, 8, tr_to_eng(str(asset.status or '')), 1, ln=True)
        
    reports_dir = os.path.join(settings.MEDIA_ROOT, 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    filename = f"Room_{room_eng.replace(' ', '_')}.pdf"
    filepath = os.path.join(reports_dir, filename)
    pdf.output(filepath)
    
    return os.path.join(settings.MEDIA_URL, 'reports', filename)
