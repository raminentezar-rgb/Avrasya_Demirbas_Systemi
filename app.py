import streamlit as st
import pandas as pd
import logic
import os
import matplotlib.pyplot as plt
from time import sleep

# --- Page Config ---
st.set_page_config(
    page_title="Avrasya Demirbaş Sistemi",
    page_icon="🏢",
    layout="wide"
)

# --- CSS Injection ---
def load_css():
    if os.path.exists("styles.css"):
        with open("styles.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()
logic.init_db()

# --- Application State ---
if 'search_results' not in st.session_state:
    st.session_state.search_results = None

# --- Sidebar Navigation ---
st.sidebar.markdown("<div class='sidebar-title'>AVRASYA</div>", unsafe_allow_html=True)
if os.path.exists(logic.LOGO_FILE):
    st.sidebar.image(logic.LOGO_FILE, use_container_width=True)
st.sidebar.caption("Demirbaş Yönetim Sistemi v2.0")

nav = st.sidebar.radio("Ana Menü", ["🏠 Gösterge Paneli", "📊 Analiz ve Grafikler", "🔍 Gelişmiş Arama", "📋 Envanter Listesi", "📱 QR Kod İşlemleri", "📍 Oda Görünümü", "➕ Yeni Kayıt", "📥 İçe Aktar"])

# --- Data Loading ---
df = logic.load_data()

# --- Helper: QR Dialog ---
if hasattr(st, "dialog"):
    @st.dialog("🖼️ QR Kod Görüntüleyici", width="normal")
    def show_qr_dialog(item_dict):
        path = logic.generate_qrcode(item_dict)
        c1, c2 = st.columns([1, 1.2])
        with c1:
            st.image(path, use_container_width=True)
        with c2:
            st.markdown("### Demirbaş Detayları")
            st.markdown(f"**Kayıt No:** `{item_dict.get('Code', '')}`")
            st.markdown(f"**Eşya Adı:** {item_dict.get('Turkish_Name', '')}")
            st.markdown(f"**Konum:** {item_dict.get('Campus', '')} / {item_dict.get('Room', '')}")
            st.markdown(f"**Durum:** {item_dict.get('Status', '')}")
            st.info("📱 *Bu QR kodu telefonunuzla taratarak yukarıdaki tüm özellikleri mobil cihazınızda görebilirsiniz.*")

# --- Helper: Display Item Card ---
def item_card(item):
    with st.container(border=True):
        col1, col2, col3, col4 = st.columns([1.5, 2, 1.5, 1])
        with col1:
             st.markdown(f"**Kod:** `{item['Code']}`")
             st.markdown(f"**Dahili:** `{item.get('Internal_Code', '-')}`")
        with col2:
             st.markdown(f"**📍 Yer:** {item['Campus']} / {item['Room']}")
             st.markdown(f"**🏷️ Kategori:** {item['Category']}")
        with col3:
             st.markdown(f"**👤 Personel:** {item['Turkish_Name']}")
             st.markdown(f"**🕒 Tarih:** {item['Date']}")
        with col4:
            if st.button("🖼️ QR Göster", key=f"qr_btn_{item['ID']}", use_container_width=True):
                if hasattr(st, "dialog"):
                    show_qr_dialog(item.to_dict())
                else:
                    path = logic.generate_qrcode(item.to_dict())
                    st.image(path, caption="QR Kod", width=150)

if nav == "🏠 Gösterge Paneli":
    st.markdown("<h1 class='main-title'>Yönetim Paneli</h1>", unsafe_allow_html=True)
    
    # Hero Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Toplam Varlık", len(df), delta=None)
    m2.metric("Aktif Kategori", df["Category"].nunique(), delta=None)
    m3.metric("Toplam Yerleşke", df["Campus"].nunique(), delta=None)
    m4.metric("Kayıtlı Oda", df["Room"].nunique(), delta=None)
    
    st.divider()
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🏷️ Kategori Dağılımı")
        cat_data = df["Category"].value_counts()
        st.bar_chart(cat_data, color="#1e3a8a")
        
    with c2:
        st.markdown("### 📍 Yerleşke Dağılımı")
        campus_data = df["Campus"].value_counts()
        fig, ax = plt.subplots(figsize=(6, 6))
        campus_data.plot(kind='pie', autopct='%1.1f%%', ax=ax, colors=['#1e3a8a', '#3b82f6', '#93c5fd', '#d1d5db'])
        ax.set_ylabel('')
        st.pyplot(fig)
        
    st.markdown("### 🕒 Son Eklenen 10 Demirbaş")
    st.dataframe(df.tail(10).iloc[::-1], use_container_width=True)

elif nav == "📊 Analiz ve Grafikler":
    st.markdown("<h1 class='main-title'>Karşılaştırmalı Analiz</h1>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🏛️ Oda Bazlı Analiz", "🏢 Yerleşke Karşılaştırması"])
    
    with tab1:
        st.markdown("### Oda Başına Demirbaş Sayısı")
        room_counts = df["Room"].value_counts().head(15)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        room_counts.plot(kind='bar', ax=ax, color='#3b82f6')
        ax.set_title("En Yoğun 15 Oda", fontsize=14, fontweight='bold')
        ax.set_ylabel("Adet")
        plt.xticks(rotation=45)
        st.pyplot(fig)
        
    with tab2:
        st.markdown("### Yerleşke ve Kategori Kırılımı")
        pivot_df = df.pivot_table(index='Campus', columns='Category', values='ID', aggfunc='count').fillna(0)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        pivot_df.plot(kind='bar', stacked=True, ax=ax)
        ax.set_title("Yerleşkelere Göre Kategori Dağılımı", fontsize=14, fontweight='bold')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig)

elif nav == "🔍 Gelişmiş Arama":
    st.markdown("<h1 class='main-title'>Akıllı Filtreleme</h1>", unsafe_allow_html=True)
    
    with st.container(border=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            f_name = st.text_input("Malzeme Adı / Personel")
            f_code = st.text_input("Demirbaş Kodu")
        with c2:
            f_campus = st.multiselect("Yerleşke", options=df["Campus"].unique().tolist())
            f_category = st.multiselect("Kategori", options=df["Category"].unique().tolist())
        with c3:
            f_room = st.text_input("Oda / Sınıf")
            f_status = st.multiselect("Durum", options=df["Status"].unique().tolist())
            
        if st.button("🔍 Filtrele", use_container_width=True):
            res = df.copy()
            if f_name: res = res[res['Turkish_Name'].str.contains(f_name, case=False, na=False) | res['Inventory_Item'].str.contains(f_name, case=False, na=False)]
            if f_code: res = res[res['Code'].str.contains(f_code, case=False, na=False)]
            if f_campus: res = res[res['Campus'].isin(f_campus)]
            if f_category: res = res[res['Category'].isin(f_category)]
            if f_room: res = res[res['Room'].str.contains(f_room, case=False, na=False)]
            if f_status: res = res[res['Status'].isin(f_status)]
            st.session_state.search_results = res
            
    with st.container(border=True):
        st.markdown("### 📷 Barkod/QR ile Hızlı Arama")
        st.caption("Fiziksel barkod okuyucunuzu bağlayın, aşağıdaki kutuya tıklayın ve demirbaşı okutun.")
        f_barcode = st.text_input("Barkod Okutunuz", key="barcode_scan")
        if f_barcode:
            res = df[df['Code'].astype(str) == f_barcode.strip()]
            st.session_state.search_results = res
            st.success(f"✅ Barkod okundu: {f_barcode}")
            
    if st.session_state.search_results is not None:
        st.markdown(f"#### Bulunan Sonuçlar ({len(st.session_state.search_results)})")
        
        if len(st.session_state.search_results) > 0:
            res = st.session_state.search_results
            total_items = len(res)
            items_per_page = 50
            total_pages = max(1, (total_items + items_per_page - 1) // items_per_page)
            
            if total_pages > 1:
                page = st.number_input(f"Sonuç Sayfası (1 - {total_pages})", min_value=1, max_value=total_pages, value=1, key="search_page")
            else:
                page = 1
                
            start_idx = (page - 1) * items_per_page
            end_idx = start_idx + items_per_page
            
            st.caption(f"Gösterilen: {start_idx + 1} - {min(end_idx, total_items)}")
            
            for _, item in res.iloc[start_idx:end_idx].iterrows():
                item_card(item)
                
            csv = st.session_state.search_results.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Sonuçları Excel/CSV Olarak İndir", csv, "arama_sonuclari.csv", "text/csv")

elif nav == "📋 Envanter Listesi":
    st.markdown("<h1 class='main-title'>Envanter Yönetimi</h1>", unsafe_allow_html=True)
    
    with st.expander("💼 Toplu İşlemler (Tüm Envanter)"):
        st.markdown("Veritabanınızdaki tüm demirbaşlar için tek seferde QR kod üretebilirsiniz. Kodlar projenin `qrcodes/` klasörüne kaydedilecektir.")
        if st.button("🚀 Tüm Eşyalar İçin QR Kod Üret"):
            with st.spinner("QR Kodlar üretiliyor, lütfen bekleyin..."):
                count = logic.generate_all_qrcodes()
                st.success(f"✅ Başarılı! Toplam {count} adet QR kod oluşturuldu ve klasöre kaydedildi.")
                
    st.dataframe(df, use_container_width=True)
    
    st.divider()
    
    st.markdown("### 🛠️ Kayıt Düzenleme / İşlemler")
    selected_id = st.selectbox("İşlem Yapmak İçin Kayıt Seçin", options=df["ID"].tolist(), 
                               format_func=lambda x: f"{df[df['ID']==x]['Code'].iloc[0]} - {df[df['ID']==x]['Turkish_Name'].iloc[0]}")
    
    if selected_id:
        item = df[df["ID"] == selected_id].iloc[0]
        
        col1, col2 = st.columns([2, 1])
        with col1:
            if "Image_Path" in item and pd.notna(item["Image_Path"]) and os.path.exists(str(item["Image_Path"])):
                st.image(item["Image_Path"], caption="Mevcut Görsel", width=200)
                
            with st.form("edit_master_form"):
                st.markdown(f"**Kayıt ID:** `{selected_id}`")
                e_name = st.text_input("Malzeme / Personel", item["Turkish_Name"])
                e_code = st.text_input("Demirbaş Kodu", item["Code"])
                e_campus = st.selectbox("Yerleşke", ["Pelitli", "Yomra", "Merkez", "Diğer"], 
                                      index=["Pelitli", "Yomra", "Merkez", "Diğer"].index(item["Campus"]) if item["Campus"] in ["Pelitli", "Yomra", "Merkez", "Diğer"] else 3)
                e_room = st.text_input("Oda", item["Room"])
                e_cat = st.text_input("Kategori", item["Category"])
                e_status = st.selectbox("Durum", ["Yeni", "Kullanılmış", "Arızalı", "Hurda"], 
                                      index=["Yeni", "Kullanılmış", "Arızalı", "Hurda"].index(item["Status"]) if item["Status"] in ["Yeni", "Kullanılmış", "Arızalı", "Hurda"] else 1)
                
                e_image = st.file_uploader("🖼️ Yeni Görsel Yükle (Eskisinin Yerine Geçer)", type=["png", "jpg", "jpeg"])
                
                c_sub1, c_sub2 = st.columns(2)
                with c_sub1:
                    if st.form_submit_button("✅ Bilgileri Güncelle"):
                        updated_data = item.to_dict()
                        updated_data.update({"Turkish_Name": e_name, "Code": e_code, "Campus": e_campus, "Room": e_room, "Category": e_cat, "Status": e_status})
                        
                        if e_image:
                            img_path = logic.save_image(e_image, e_code)
                            updated_data["Image_Path"] = img_path
                            
                        logic.save_item(updated_data)
                        logic.clear_cache()
                        st.success("Kayıt başarıyla güncellendi!")
                        sleep(1)
                        st.rerun()
                with c_sub2:
                    st.markdown(" ") # Spacer
        
        with col2:
            st.markdown("#### ⚡ Hızlı İşlemler")
            if st.button("🖼️ QR Kod Göster", use_container_width=True):
                if hasattr(st, "dialog"):
                    show_qr_dialog(item.to_dict())
                else:
                    path = logic.generate_qrcode(item.to_dict())
                    st.image(path, caption="QR Kod Açıldı", width=200)
                
            if st.button("🏷️ Barkod Göster", use_container_width=True):
                path = logic.generate_barcode(item['Code'])
                if path: st.image(path, caption="Barkod", width=300)
                
            if st.button("📄 Demirbaş Belgesi (PDF)", use_container_width=True):
                qr_path = logic.generate_qrcode(item.to_dict())
                pdf_path = logic.create_item_pdf(item.to_dict(), qr_path)
                with open(pdf_path, "rb") as f:
                    st.download_button("📥 Belgeyi İndir", f, file_name=pdf_path)
            
            st.divider()
            if st.button("🗑️ Kaydı Sil", type="primary", use_container_width=True):
                logic.delete_item(selected_id)
                logic.clear_cache()
                st.warning("Kayıt silindi.")
                sleep(1)
                st.rerun()

elif nav == "📱 QR Kod İşlemleri":
    st.markdown("<h1 class='main-title'>QR Kod Modülü</h1>", unsafe_allow_html=True)
    st.info("Bu sayfada tüm demirbaşlarınızın özelliklerini içeren QR kodlarını hemen açabilir ve telefonunuzla tarayabilirsiniz.")
    
    with st.container(border=True):
        st.markdown("### 🔍 Demirbaş Ara")
        search_query = st.text_input("Malzeme Adı veya Kodu giriniz...")
        
    res = df.copy()
    if search_query:
        res = res[res['Turkish_Name'].str.contains(search_query, case=False, na=False) | res['Code'].astype(str).str.contains(search_query, case=False, na=False)]
        
    if len(res) == 0:
        st.warning("Sonuç bulunamadı.")
    else:
        total_items = len(res)
        items_per_page = 50
        total_pages = max(1, (total_items + items_per_page - 1) // items_per_page)
        
        st.markdown(f"#### 📦 Demirbaş Listesi (Toplam: {total_items} Kayıt)")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            if total_pages > 1:
                page = st.number_input(f"Sayfa (1 - {total_pages})", min_value=1, max_value=total_pages, value=1, key="qr_page")
            else:
                page = 1
        
        start_idx = (page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        
        st.caption(f"Hızlıca QR kodunu pop-up olarak açmak için 'QR Göster' butonuna tıklayınız. (Gösterilen: {start_idx + 1} - {min(end_idx, total_items)})")
        
        for _, item in res.iloc[start_idx:end_idx].iterrows():
            item_card(item)

elif nav == "📍 Oda Görünümü":
    st.markdown("<h1 class='main-title'>Oda Odaklı Takip</h1>", unsafe_allow_html=True)
    sel_room = st.selectbox("Görüntülemek İstediğiniz Oda", sorted(df["Room"].unique().astype(str)))
    if sel_room:
        items = df[df["Room"] == sel_room]
        st.info(f"Oda: **{sel_room}** | Toplam Eşya: **{len(items)}**")
        st.dataframe(items, use_container_width=True)
        
        if st.button("🖨️ Oda Envanter Listesi (PDF)", use_container_width=True):
            pdf_path = logic.create_room_pdf(sel_room, items.to_dict('records'))
            with open(pdf_path, "rb") as f:
                st.download_button("📥 PDF İndir", f, file_name=pdf_path)

elif nav == "➕ Yeni Kayıt":
    st.markdown("<h1 class='main-title'>Yeni Demirbaş Kaydı</h1>", unsafe_allow_html=True)
    with st.form("new_entry_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            n_name = st.text_input("Malzeme Adı / Personel *")
            n_code = st.text_input("Demirbaş No / Barkod *")
            n_int = st.text_input("Dahili Kod")
            n_campus = st.selectbox("Yerleşke", ["Pelitli", "Yomra", "Merkez", "Diğer"])
        with c2:
            n_cat = st.text_input("Kategori")
            n_room = st.text_input("Oda / Bölüm *")
            n_status = st.selectbox("Durum", ["Yeni", "Kullanılmış", "Arızalı"])
            n_color = st.text_input("Renk")
            n_image = st.file_uploader("🖼️ Demirbaş Görseli", type=["png", "jpg", "jpeg"])
            
        if st.form_submit_button("💾 Kaydı Tamamla", use_container_width=True):
            if n_name and n_code and n_room:
                 new_item = {
                     "Turkish_Name": n_name, "Inventory_Item": n_name, "Code": n_code, 
                     "Internal_Code": n_int, "Campus": n_campus, "Room": n_room, 
                     "Category": n_cat, "Status": n_status, "Color": n_color, 
                     "Date": pd.Timestamp.now().strftime('%Y-%m-%d')
                 }
                 item_id = logic.save_item(new_item)
                 
                 if n_image:
                     img_path = logic.save_image(n_image, n_code)
                     new_item["ID"] = item_id
                     new_item["Image_Path"] = img_path
                     logic.save_item(new_item)
                     
                 logic.clear_cache()
                 st.success("✅ Yeni demirbaş sisteme eklendi.")
                 sleep(1)
                 st.rerun()
            else:
                 st.error("Lütfen yıldızlı (*) alanları doldurun.")

elif nav == "📥 İçe Aktar":
    st.markdown("<h1 class='main-title'>Veri Aktarımı</h1>", unsafe_allow_html=True)
    st.info("Var olan bir envanteri Excel (.xlsx) formatında toplu olarak yükleyebilirsiniz.")
    up_file = st.file_uploader("Dosya Seçin", type=["xlsx"])
    if up_file:
        if st.button("🚀 Verileri İçe Aktar", use_container_width=True):
            cnt = logic.import_from_excel(up_file)
            if cnt > 0:
                logic.clear_cache()
                st.success(f"Başarılı! {cnt} yeni kayıt eklendi.")
                sleep(2)
                st.rerun()
            else:
                st.error("İçe aktarma hatası.")
