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

class PedidoClienteDetalleInline(admin.TabularInline):
    model = models.PedidoClienteDetalle

class PedidoFijoAdmin(admin.ModelAdmin):
    inlines = [ PedidoClienteDetalleInline ]

class ClienteAdmin(admin.ModelAdmin):
    model = models.Cliente

admin.site.register(models.Insumo, InsumoAdmin)
admin.site.register(models.Receta, RecetaAdmin)
admin.site.register(models.PedidoFijo, PedidoFijoAdmin)
admin.site.register(models.Cliente, ClienteAdmin)