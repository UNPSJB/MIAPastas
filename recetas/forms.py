from django import forms
from . import models
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.utils.text import capfirst
from django.core import exceptions
from django.forms import CheckboxSelectMultiple, MultipleChoiceField
import re
import datetime

def cuit_valido(cuit):
    cuit = str(cuit)
    cuit = cuit.replace("-", "")
    #cuit = cuit.replace(" ", "")
   # cuit = cuit.replace(".", "")
    print "cuit inicial " ,cuit
    if len(cuit) != 11:
        if len(cuit) == 10:
            cuit = cuit[:2] + '0' + cuit[2:]
            print "es 10 ",cuit
        else:
            return False
    if not cuit.isdigit():
        return False
    base = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
    aux = 0
    for i in xrange(10):
        aux += int(cuit[i]) * base[i]
    aux = 11 - (aux % 11)
    if aux == 11:
        aux = 0
    elif aux == 10:
        aux = 9
    if int(cuit[10]) == aux:
        return True
    else:
        return False



class ChoferForm(forms.ModelForm):
    class Meta:
        model = models.Chofer
        fields = ["cuit", "nombre", "direccion", "telefono", "e_mail"]

    def clean_cuit(self):
        cuit = self.cleaned_data['cuit']
        pattern="\d\d-\d\d\d\d\d\d\d\d?-\d"
        result = re.match(pattern, cuit)
        print "esult ",result
        if result is not None:
            #if cuit_valido(cuit):
            return cuit
        raise ValidationError("Cuit no valido papa")
        return cuit




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

    def save(self, *args, **kwargs):
        # Sobrecargar save devuelve el objeto apunto de ser guardado
        obj_receta = super(RecetaForm, self).save(*args, **kwargs)
        #detalles = models.RecetaDetalle.objects.filter(receta = obj_receta)
        #if detalles is  None:
        #    raise ValidationError("Debe existir al menos un detalle para la Receta.")
        #else:
        #    obj_receta.save()
        return obj_receta

    def clean(self):
        print "CLEAN POSTA"
        cleaned_data = super(RecetaForm, self).clean()
        #valido que existe al menos un detalle
        #detalles =models.RecetaDetalle.objects.filter(receta=self.instance)
        #if len(detalles) == 0:
        #    raise ValidationError("Debe existir al menos un detalle para la Receta.")
        return cleaned_data

    def clean_producto_terminado(self):
        print "CLEAN DE RECETA_producto_terminado"
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




class ProveedorForm(forms.ModelForm):
    class Meta:
        model = models.Proveedor
        fields = ["cuit", "razon_social", "localidad","nombre_dueno","direccion","email","numero_cuenta","provincia","telefono","insumos" ]

    def __init__(self, *args, **kwargs):
        super(ProveedorForm, self).__init__(*args, **kwargs)
        #self.fields['fecha_creacion'].widget.attrs.update({'class' : 'datepicker'})

    def clean_razon_social(self):
        razon_social = self.cleaned_data['razon_social']
        razon_social = texto_lindo(razon_social, True)
        if models.Cliente.objects.filter(razon_social=razon_social).exists():
            raise ValidationError('Ya existe una Ciudad con esa Razon Social.')
        return razon_social

    def clean_nombre_dueno(self):
        nombre_dueno = self.cleaned_data['nombre_dueno']
        nombre_dueno = texto_lindo(nombre_dueno, True)
        return nombre_dueno

    def clean_direccion(self):
        direccion = self.cleaned_data['direccion']
        direccion = texto_lindo(direccion, True)
        return direccion

    def clean_email(self):
        email = self.cleaned_data['email']
        email = texto_lindo(email, True)
        return email

    def clean_localidad(self):
        localidad = self.cleaned_data['localidad']
        localidad = texto_lindo(localidad, True)
        return localidad

    def clean_provincia(self):
        provincia = self.cleaned_data['provincia']
        provincia = texto_lindo(provincia, True)
        return provincia








class ProductoTerminadoForm(forms.ModelForm):
    class Meta:
        model = models.ProductoTerminado
        fields = ["nombre","unidad_medida","precio"]

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        nombre = texto_lindo(nombre, True)
        if models.Zona.objects.filter(nombre=nombre).exists():
            raise ValidationError('Ya existe un Producto Terminado con ese nombre.')
        return nombre




class CiudadForm(forms.ModelForm):
    class Meta:
        model = models.Ciudad
        fields = ["nombre","codigo_postal","zona"]

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        nombre = texto_lindo(nombre, True)
        if models.Zona.objects.filter(nombre=nombre).exists():
            raise ValidationError('Ya existe una Ciudad con ese nombre.')
        return nombre



def texto_lindo(texto, titulo=False):
    #esta funcion es generica, la pueda llamar en cualquier lugar
    #Sirve para que ante una entrada de texto fea, por ej: " dsadasd     hola  dasda", me la junte toda
    #titulo=True significa que si ingresamos un texto "hola mundo" se transformara en "Hola Mundo".
    #si titulo=False significa que si ingresamos un texto "HOLA MUNDO" se tranformara en "Hola mundo"
    # Quitamos espacios extra en todo el texto
    texto = " ".join(texto.split())
    texto = ". ".join(map(lambda t: t.strip().capitalize(), texto.split(".")))
    return titulo and texto.title() or texto



class ZonaForm(forms.ModelForm):
    class Meta:
        model = models.Zona
        fields = ["nombre"]

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        nombre = texto_lindo(nombre, True)
        if models.Zona.objects.filter(nombre=nombre).exists():
            raise ValidationError('Ya existe una Zona con ese nombre.')
        return nombre



class ClienteForm(forms.ModelForm):
    class Meta:
        model = models.Cliente
        fields = ["cuit_cuil","razon_social","nombre_dueno","ciudad","direccion","telefono","email","es_moroso"]

    def clean_razon_social(self):
        razon_social = self.cleaned_data['razon_social']
        razon_social = texto_lindo(razon_social, True)
        if models.Cliente.objects.filter(razon_social=razon_social).exists():
            raise ValidationError('Ya existe una Ciudad con esa Razon Social.')
        return razon_social

    def clean_nombre_dueno(self):
        nombre_dueno = self.cleaned_data['nombre_dueno']
        nombre_dueno = texto_lindo(nombre_dueno, True)
        return nombre_dueno

    def clean_direccion(self):
        direccion = self.cleaned_data['direccion']
        direccion = texto_lindo(direccion, True)
        return direccion




class PedidoProveedorAltaForm(forms.ModelForm):
    class Meta:
        model = models.PedidoProveedor
        widgets = {
            'fecha_realizacion': forms.DateInput(attrs={'class': 'datepicker'})}
        exclude = ['fecha_de_entrega', 'estado_pedido','insumos','descripcion']



class PedidoProveedorModificarForm(forms.ModelForm):
    class Meta:
        model = models.PedidoProveedor
        widgets = {
            'fecha_realizacion': forms.DateInput(attrs={'class': 'datepicker'})}
        exclude = ['fecha_de_entrega', 'estado_pedido','insumos','descripcion','proveedor']


class PedidoProveedorRecepcionarForm(forms.ModelForm):
    class Meta:
        model = models.PedidoProveedor
        widgets = {
            'fecha_de_entrega': forms.DateInput(attrs={'class': 'datepicker'})}
        exclude = ['fecha_realizacion','insumos','proveedor']


class DetallePedidoProveedorForm(forms.ModelForm):
    class Meta:
        model = models.DetallePedidoProveedor
        exclude = ['pedido_proveedor'] #setea todos campos menos pedido_proveedor



###########################################################
##########################################################

class PedidoCliente(forms.ModelForm):
    class Meta:
        model = models.PedidoCliente
        fields = ["tipo_pedido","cliente"]


class PedidoClienteFijoForm(forms.ModelForm):
    class Meta:
        model = models.PedidoFijo
        dias = MultipleChoiceField(required=True, widget=CheckboxSelectMultiple, choices=models.TIPODIAS)
        widgets = {
            'fecha_cancelacion': forms.DateInput(attrs={'class': 'datepicker'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'datepicker'})}
        exclude = ['productos', 'tipo_pedido']

    def __init__(self, *args, **kwargs):
        super(PedidoClienteFijoForm, self).__init__(*args, **kwargs)


class PedidoClienteDetalleForm(forms.ModelForm):
    class Meta:
        model = models.PedidoClienteDetalle
        exclude = ['pedido_cliente'] #setea todos campos menos pedido




class PedidoClienteOcacionalForm(forms.ModelForm):
    class Meta:
        model = models.PedidoOcacional
        exclude = ['productos','tipo_pedido']
        widgets = {
           'fecha_entrega': forms.DateInput(attrs={'class': 'datepicker'})}

    def __init__(self, *args, **kwargs):
        super(PedidoClienteOcacionalForm, self).__init__(*args, **kwargs)


class PedidoClienteCambioForm(forms.ModelForm):
    class Meta:
        model = models.PedidoCambio
        widgets = {
           'fecha_entrega': forms.DateInput(attrs={'class': 'datepicker'})}
        exclude = ['productos','tipo_pedido']


    def __init__(self, *args, **kwargs):
        super(PedidoClienteCambioForm, self).__init__(*args, **kwargs)






#############################################################################
############################################################################


class LoteForm(forms.ModelForm):
    class Meta:
        model = models.Lote
        fields = ["producto_terminado","fecha_produccion","fecha_vencimiento","cantidad_producida"]
        widgets = {
           'fecha_produccion': forms.DateInput(attrs={'class': 'datepicker'}),
           'fecha_vencimiento': forms.DateInput(attrs={'class': 'datepicker'}),
        }

    def clean_fecha_vencimiento(self):
        print "cleanb fecha vencimiento"
        fecha = self.cleaned_data['fecha_vencimiento']
        if fecha <= datetime.date.today():
            raise ValidationError("Fecha de vencimiento debe ser mayor a la actual")
        return fecha

    def clean_fecha_produccion(self):
        print "clean en fecha de produccion"
        fecha = self.cleaned_data['fecha_produccion']
        if fecha >= datetime.date.today():
            raise ValidationError("No se puede registrar una produccion para una fecha adelantada")
        return fecha

