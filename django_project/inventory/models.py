import uuid
from django.db import models

class Asset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=100, unique=True, verbose_name="Demirbaş Kodu")
    internal_code = models.CharField(max_length=100, blank=True, null=True, verbose_name="Dahili Kod")
    inventory_item = models.CharField(max_length=255, blank=True, null=True, verbose_name="İngilizce Ad (Inventory Item)")
    turkish_name = models.CharField(max_length=255, verbose_name="Malzeme Adı (Turkish Name)")
    campus = models.CharField(max_length=100, verbose_name="Yerleşke")
    floor = models.CharField(max_length=50, blank=True, null=True, verbose_name="Kat")
    room = models.CharField(max_length=100, verbose_name="Oda / Bölüm")
    category = models.CharField(max_length=100, verbose_name="Kategori")
    status = models.CharField(max_length=100, verbose_name="Durum")
    color = models.CharField(max_length=50, blank=True, null=True, verbose_name="Renk")
    date = models.DateField(auto_now_add=True, verbose_name="Kayıt Tarihi")
    image = models.ImageField(upload_to='assets/', blank=True, null=True, verbose_name="Görsel")

    def __str__(self):
        return f"{self.code} - {self.turkish_name}"

    class Meta:
        verbose_name = "Demirbaş"
        verbose_name_plural = "Demirbaşlar"
        ordering = ['-date']
