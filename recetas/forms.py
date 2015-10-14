from django import forms
from . import models
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

class InsumoForm(forms.ModelForm):
    class Meta:
        model = models.Insumo
        fields = ["nombre", "descripcion", "stock", "unidad_medida"]

class RecetaForm(forms.ModelForm):
    class Meta:
        model = models.Receta
        fields = ["nombre", "producto_terminado","cant_prod_terminado","unidad_medida", "descripcion"]

    def __init__(self, *args, **kwargs):
        super(RecetaForm, self).__init__(*args, **kwargs)
        #self.fields['fecha_creacion'].widget.attrs.update({'class' : 'datepicker'})


    def clean_producto_terminado(self):
        print "CLEAN DE RECETA"
        producto_terminado = self.cleaned_data['producto_terminado']
        try:
            receta = get_object_or_404(models.Receta, producto_terminado=producto_terminado)
        except:
            return producto_terminado
        #if receta is not None:
        if receta.id != self.instance.id:
            raise ValidationError("ya hay una receta para este producto.")
        return producto_terminado



class RecetaDetalleForm(forms.ModelForm):
    class Meta:
        model = models.RecetaDetalle
        exclude = ['receta'] #setea todos campos menos receta

    def clean_cantidad_insumo(self):
        print "entre al clean de cantidad de insumo de detalles"
        cantidad = self.clean_cantidad_insumo<0
        if cantidad<0:
            print "LANZO"
            raise ValidationError("ya hay una receta para este producto.")
        return cantidad

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = models.Proveedor
        fields = ["cuit", "razon_social", "localidad","nombre_dueno","direccion","email","numero_cuenta","provincia","telefono","insumos" ]

    def __init__(self, *args, **kwargs):
        super(ProveedorForm, self).__init__(*args, **kwargs)
        #self.fields['fecha_creacion'].widget.attrs.update({'class' : 'datepicker'})









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







