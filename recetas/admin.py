from django.contrib import admin

# Register your models here.

from . import models

class InsumoAdmin(admin.ModelAdmin):
    search_fields = ['nombre', 'descripcion']
    list_display = ['nombre', 'descripcion']

class RecetaDetalleInline(admin.TabularInline):
    model = models.RecetaDetalle

class RecetaAdmin(admin.ModelAdmin):
    inlines = [ RecetaDetalleInline ]

admin.site.register(models.Insumo, InsumoAdmin)
admin.site.register(models.Receta, RecetaAdmin)