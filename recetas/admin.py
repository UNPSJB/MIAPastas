from django.contrib import admin

# Register your models here.

from . import models

class InsumoAdmin(admin.ModelAdmin):
    search_fields = ['nombre', 'descripcion']
    list_display = ['nombre', 'descripcion']

admin.site.register(models.Insumo, InsumoAdmin)