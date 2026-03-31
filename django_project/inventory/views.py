from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Count, Q
from django.http import HttpResponseRedirect
import pandas as pd
import uuid
import json

from .models import Asset
from .forms import AssetForm, ExcelImportForm
from .utils import generate_qrcode, generate_barcode, create_item_pdf, create_room_pdf

def dashboard_view(request):
    total_assets = Asset.objects.count()
    total_categories = Asset.objects.values('category').distinct().count()
    total_campuses = Asset.objects.values('campus').distinct().count()
    total_rooms = Asset.objects.values('room').distinct().count()
    
    recent_assets = Asset.objects.order_by('-date')[:10]
    
    category_counts = list(Asset.objects.values('category').annotate(count=Count('category')).order_by('-count')[:10])
    campus_counts = list(Asset.objects.values('campus').annotate(count=Count('campus')).order_by('-count'))
    
    context = {
        'total_assets': total_assets,
        'total_categories': total_categories,
        'total_campuses': total_campuses,
        'total_rooms': total_rooms,
        'recent_assets': recent_assets,
        'category_counts': json.dumps(category_counts),
        'campus_counts': json.dumps(campus_counts),
    }
    return render(request, 'inventory/dashboard.html', context)

class AssetListView(ListView):
    model = Asset
    template_name = 'inventory/asset_list.html'
    context_object_name = 'assets'
    paginate_by = 50

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        campus = self.request.GET.get('campus')
        category = self.request.GET.get('category')
        room = self.request.GET.get('room')
        
        if query:
            queryset = queryset.filter(
                Q(turkish_name__icontains=query) | 
                Q(code__icontains=query) |
                Q(inventory_item__icontains=query)
            )
        if campus:
            queryset = queryset.filter(campus__icontains=campus)
        if category:
            queryset = queryset.filter(category__icontains=category)
        if room:
            queryset = queryset.filter(room__icontains=room)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campuses'] = Asset.objects.values_list('campus', flat=True).distinct().order_by('campus')
        context['categories'] = Asset.objects.values_list('category', flat=True).distinct().order_by('category')
        context['rooms'] = Asset.objects.values_list('room', flat=True).distinct().order_by('room')
        return context

class AssetCreateView(CreateView):
    model = Asset
    form_class = AssetForm
    template_name = 'inventory/asset_form.html'
    success_url = reverse_lazy('asset_list')

    def form_valid(self, form):
        messages.success(self.request, "Demirbaş başarıyla eklendi.")
        return super().form_valid(form)

class AssetUpdateView(UpdateView):
    model = Asset
    form_class = AssetForm
    template_name = 'inventory/asset_form.html'
    success_url = reverse_lazy('asset_list')

    def form_valid(self, form):
        messages.success(self.request, "Demirbaş başarıyla güncellendi.")
        return super().form_valid(form)

class AssetDeleteView(DeleteView):
    model = Asset
    success_url = reverse_lazy('asset_list')
    template_name = 'inventory/asset_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Demirbaş başarıyla silindi.")
        return super().delete(request, *args, **kwargs)

def import_excel_view(request):
    if request.method == 'POST':
        form = ExcelImportForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['excel_file']
            try:
                # Need to read all sheets
                excel_data = pd.read_excel(file, sheet_name=None, header=None)
                imported_count = 0
                existing_codes = set(Asset.objects.values_list('code', flat=True))
                assets_to_create = []

                for sheet_name, df_raw in excel_data.items():
                    header_row = 0
                    for i in range(min(5, len(df_raw))):
                        row_vals = [str(c).lower().strip() for c in df_raw.iloc[i] if pd.notna(c)]
                        if any(k in v for v in row_vals for k in ['adı', 'cinsi', 'turkish', 'category', 'code']):
                            header_row = i
                            break
                    
                    df = df_raw.iloc[header_row+1:].copy()
                    df.columns = [str(c).strip() for c in df_raw.iloc[header_row]]
                    
                    cm = {}
                    for idx_col, col in enumerate(df.columns):
                        cl = str(col).lower()
                        if any(k in cl for k in ['adı', 'adi', 'ad', 'isim', 'malzeme', 'turkish']): cm['tr_name'] = col
                        elif 'inventory' in cl or 'item' in cl: cm['eng_name'] = col
                        elif any(k in cl for k in ['cinsi', 'kategori', 'category']): cm['cat'] = col
                        elif 'renk' in cl or 'color' in cl: cm['color'] = col
                        elif 'adet' in cl or 'miktar' in cl or 'qty' in cl: cm['qty'] = col
                        elif 'code' in cl and 'internal' not in cl: cm['code'] = col
                        elif 'internal' in cl: cm['icode'] = col
                        elif 'campus' in cl or 'yerleşke' in cl: cm['campus'] = col
                        elif 'floor' in cl or 'kat' in cl: cm['floor'] = col
                        elif 'room' in cl or 'oda' in cl or 'sınıf' in cl: cm['room'] = col
                        elif 'status' in cl or 'durum' in cl: cm['status'] = col
                        
                    # If tr_name is STILL not found, use column 3 or 1 as fallback!
                    if 'tr_name' not in cm and 'eng_name' not in cm:
                        if len(df.columns) > 3: cm['tr_name'] = df.columns[3] # Usually Inventory_Item
                        elif len(df.columns) > 1: cm['tr_name'] = df.columns[1]
                        else: cm['tr_name'] = df.columns[0]
                        
                    if 'cat' not in cm and len(df.columns) > 7: cm['cat'] = df.columns[7]

                    for idx, row in df.iterrows():
                        name = ""
                        if 'tr_name' in cm and pd.notna(row[cm['tr_name']]):
                            name = str(row[cm['tr_name']]).strip()
                        
                        if (not name or name.lower() == 'nan') and 'eng_name' in cm and pd.notna(row[cm['eng_name']]):
                            name = str(row[cm['eng_name']]).strip()
                            
                        # If the name is absolutely empty, use a placeholder
                        if not name or name.lower() == 'nan':
                            name = "Bilinmeyen Demirbaş"
                        
                        cat = str(row[cm['cat']]).strip() if 'cat' in cm and pd.notna(row[cm['cat']]) else "Diğer"
                        if not cat or cat.lower() == 'nan': cat = "Diğer"
                        
                        color = str(row[cm['color']]).strip() if 'color' in cm and pd.notna(row[cm['color']]) else ""
                        if color.lower() == 'nan': color = ""
                        
                        try:
                            qty_val = str(row[cm['qty']]).strip() if 'qty' in cm else '1'
                            qty = int(float(qty_val)) if qty_val.lower() != 'nan' and qty_val else 1
                        except: qty = 1
                        
                        for _ in range(qty):
                            safe_name = "".join(c for c in name[:8] if c.isalnum()).upper() or "ITEM"
                            
                            row_code = str(row.get('Code', '')).strip()
                            if not row_code or row_code.lower() == 'nan':
                                row_code = f"{str(sheet_name)[:3].upper()}_{safe_name}_{imported_count+1}"
                                
                            # Absolute deduplication bypass for duplicate values in external spreadsheet!
                            base_code = row_code
                            counter = 1
                            while row_code in existing_codes:
                                row_code = f"{base_code}_{counter}"
                                counter += 1
                                
                            existing_codes.add(row_code)
                                
                            row_icode = str(row.get('Internal_Code', '')).strip()
                            if not row_icode or row_icode.lower() == 'nan':
                                row_icode = None
                                
                            row_campus = str(row.get('Campus', 'Pelitli')).strip()
                            row_floor = str(row.get('Floor', 'Kat 0')).strip()
                            row_room = str(row.get('Room', sheet_name)).strip()
                            if not row_room or row_room.lower() == 'nan': row_room = str(sheet_name)
                                
                            row_status = str(row.get('Status', 'Kullanılmış')).strip()
                            row_eng = str(row.get('Inventory_Item', name)).strip()
                            
                            assets_to_create.append(Asset(
                                id=uuid.uuid4(),
                                code=row_code,
                                internal_code=row_icode,
                                inventory_item=row_eng if row_eng and row_eng.lower() != 'nan' else "",
                                turkish_name=name,
                                campus=row_campus if row_campus and row_campus.lower() != 'nan' else "Pelitli",
                                floor=row_floor if row_floor and row_floor.lower() != 'nan' else "",
                                room=row_room,
                                category=cat,
                                status=row_status if row_status and row_status.lower() != 'nan' else "Kullanılmış",
                                color=color
                            ))
                            imported_count += 1
                            
                if assets_to_create:
                    Asset.objects.bulk_create(assets_to_create, batch_size=1000, ignore_conflicts=True)
                    
                messages.success(request, f"Başarıyla {imported_count} demirbaş yüklendi.")
                return redirect('asset_list')
            except Exception as e:
                messages.error(request, f"Hata: {e}")
    else:
        form = ExcelImportForm()
    return render(request, 'inventory/import_excel.html', {'form': form})

def generate_pdf_view(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    pdf_url = create_item_pdf(asset, request)
    return HttpResponseRedirect(pdf_url)

def generate_qr_view(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    qr_url = generate_qrcode(asset)
    return HttpResponseRedirect(qr_url)

def generate_barcode_view(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    bar_url = generate_barcode(asset)
    if bar_url:
        return HttpResponseRedirect(bar_url)
    messages.error(request, 'Barkod oluşturulamadı.')
    return redirect('asset_list')

def room_view(request):
    rooms = Asset.objects.values_list('room', flat=True).distinct().order_by('room')
    selected_room = request.GET.get('room')
    assets = []
    if selected_room:
        assets = Asset.objects.filter(room=selected_room)

    return render(request, 'inventory/room_view.html', {'rooms': rooms, 'selected_room': selected_room, 'assets': assets})

def print_room_qr_view(request):
    room = request.GET.get('room')
    if room:
        assets = Asset.objects.filter(room=room)
        pdf_url = create_room_pdf(room, list(assets))
        return HttpResponseRedirect(pdf_url)
    return redirect('room_view')
