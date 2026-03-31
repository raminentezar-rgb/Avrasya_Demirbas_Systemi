from django import forms
from .models import Asset
import pandas as pd

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['code', 'internal_code', 'turkish_name', 'inventory_item', 'campus', 'floor', 'room', 'category', 'status', 'color', 'image']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Örn: ASSET123'}),
            'internal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'turkish_name': forms.TextInput(attrs={'class': 'form-control'}),
            'inventory_item': forms.TextInput(attrs={'class': 'form-control'}),
            'campus': forms.TextInput(attrs={'class': 'form-control'}),
            'floor': forms.TextInput(attrs={'class': 'form-control'}),
            'room': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(choices=[('Yeni', 'Yeni'), ('Kullanılmış', 'Kullanılmış'), ('Arızalı', 'Arızalı'), ('Hurda', 'Hurda')], attrs={'class': 'form-select'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class ExcelImportForm(forms.Form):
    excel_file = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))
