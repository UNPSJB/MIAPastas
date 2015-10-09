from django import forms
from . import models
from django.core.exceptions import ValidationError

class InsumoForm(forms.ModelForm):
    class Meta:
        model = models.Insumo
        fields = ["nombre", "descripcion", "stock", "unidad_medida"]

class RecetaForm(forms.ModelForm):
    class Meta:
        model = models.Receta
        fields = ["nombre", "descripcion", "producto_terminado","cant_prod_terminado","unidad_medida"]

    def __init__(self, *args, **kwargs):
        super(RecetaForm, self).__init__(*args, **kwargs)
        #self.fields['fecha_creacion'].widget.attrs.update({'class' : 'datepicker'})

    def clean_producto_terminado(self):
        producto_terminado=self.cleaned_data['producto_terminado']
        receta=models.Receta.objets.get (producto_terminado=producto_terminado)
        if (receta is not None):
            raise ValidationError("ya hay una receta para esta producto")
        return producto_terminado


class RecetaDetalleForm(forms.ModelForm):
    class Meta:
        model = models.RecetaDetalle
        exclude = ['receta'] #setea todos campos menos receta

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = models.Proveedor
        fields = ["cuit", "razon_social", "localidad","nombre_dueno","direccion","email","numero_cuenta","provincia","telefono","insumos" ]

class ProductoTerminadoForm(forms.ModelForm):
    class Meta:
        model = models.ProductoTerminado
        fields = ["nombre","stock","unidad_medida","precio"]

class CiudadForm(forms.ModelForm):
    class Meta:
        model = models.Ciudad
        fields = ["nombre","codigo_postal","zona"]


class ZonaForm(forms.ModelForm):
    class Meta:
        model = models.Zona
        fields = ["nombre"]


class ClienteForm(forms.ModelForm):
    class Meta:
        model = models.Cliente
        fields = ["cuit_cuil","razon_social","nombre_dueno","tipo_cliente","ciudad","direccion","telefono","email","es_moroso"]







