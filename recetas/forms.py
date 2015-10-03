from django import forms
from . import models

class InsumoForm(forms.ModelForm):
    class Meta:
        model = models.Insumo
        fields = ["nombre", "descripcion", "stock", "unidad_medida"]

class RecetaForm(forms.ModelForm):
    class Meta:
        model = models.Receta
        fields = ["nombre", "descripcion", "fechaCreacion", "productoTerminado","cantProdTerminado","unidad_medida"]

    def __init__(self, *args, **kwargs):
        super(RecetaForm, self).__init__(*args, **kwargs)
        self.fields['fechaCreacion'].widget.attrs.update({'class' : 'datepicker'})

class RecetaDetalleForm(forms.ModelForm):
    class Meta:
        model = models.RecetaDetalle
        exclude = ['receta']

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = models.Proveedor
        fields = ["cuit", "razonSocial", "localidad","nombreDueno","direccion","email","numeroCuenta","provincia","telefono","insumos" ]

class ProductoTerminadoForm(forms.ModelForm):
    class Meta:
        model = models.ProductoTerminado
        fields = ["nombre","stock","unidad_medida","precio"]

class CiudadForm(forms.ModelForm):
    class Meta:
        model = models.Ciudad
        fields = ["nombre","codigoPostal","zona"]



class ZonaForm(forms.ModelForm):
    class Meta:
        model = models.Zona
        fields = ["nombre"]


class ClienteForm(forms.ModelForm):
    class Meta:
        model = models.Cliente
        fields = ["cuit_cuil","razonSocial","nombreDueno","tipo_cliente","ciudad","direccion","telefono","email","esMoroso"]







