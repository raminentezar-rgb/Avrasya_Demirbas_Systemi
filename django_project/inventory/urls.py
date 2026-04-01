from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('assets/', views.AssetListView.as_view(), name='asset_list'),
    path('assets/add/', views.AssetCreateView.as_view(), name='asset_create'),
    path('assets/<uuid:pk>/edit/', views.AssetUpdateView.as_view(), name='asset_update'),
    path('assets/<uuid:pk>/delete/', views.AssetDeleteView.as_view(), name='asset_delete'),
    path('import/', views.import_excel_view, name='import_excel'),
    path('assets/<uuid:pk>/pdf/', views.generate_pdf_view, name='generate_pdf'),
    path('assets/<uuid:pk>/qr/', views.generate_qr_view, name='generate_qr'),
    path('assets/<uuid:pk>/barcode/', views.generate_barcode_view, name='generate_barcode'),
    path('rooms/', views.room_view, name='room_view'),
    path('rooms/qr/', views.print_room_qr_view, name='print_room_qr'),
    path('how-it-works/', views.how_it_works, name='how_it_works'),
]
