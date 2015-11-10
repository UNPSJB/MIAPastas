from django import forms
from . import models
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.utils.text import capfirst
from django.core import exceptions
from django.forms import CheckboxSelectMultiple, MultipleChoiceField
import re
import datetime
from datetime import timedelta

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


class ModificarStockInsumoForm(forms.Form):
    insumo = forms.ModelChoiceField(queryset=models.Insumo.objects.all(), empty_label="(----)")
    cantidad = forms.IntegerField()
    unidad_medida = forms.ChoiceField(choices=models.Insumo.UNIDADES)
    def save(self):
        insumo = self.cleaned_data["insumo"]
        cantidad = self.cleaned_data["cantidad"]
        unidad_medida = self.cleaned_data["unidad_medida"]
        print "cantidad: ",cantidad
        print "unidad_medida: ",unidad_medida
        insumo.modificar_stock(cantidad,int(unidad_medida))
        insumo.save()


class InsumoForm(forms.ModelForm):
    class Meta:
        model = models.Insumo
        fields = ["nombre", "descripcion","unidad_medida"]
    unidad_medida = forms.ChoiceField(choices=models.Insumo.UNIDADES_BASICAS)

    def __init__(self, *args, **kwargs):
        super(InsumoForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].label = "Nombre ( * )"
        self.fields['descripcion'].label = "Dscripcion ( * )"
        self.fields['unidad_medida'].label = "Unidad de Medida ( * )"

class RecetaForm(forms.ModelForm):
    class Meta:
        model = models.Receta
        fields = ["nombre", "producto_terminado","cant_prod_terminado", "descripcion"]

    def __init__(self, *args, **kwargs):
        super(RecetaForm, self).__init__(*args, **kwargs)
        self.fields['cant_prod_terminado'].label = "Cantidad Bolsines ( * )"


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
        fields = ["nombre","precio","dias_vigencia"]



    def __init__(self, *args, **kwargs):
        super(ProductoTerminadoForm, self).__init__(*args, **kwargs)
        self.fields['precio'].label = "Precio Bolsin ( * )"

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        nombre = texto_lindo(nombre, True)
        if models.Zona.objects.filter(nombre=nombre).exists():
            raise ValidationError('Ya existe un Producto Terminado con ese nombre.')
        return nombre


class LoteStockForm(forms.ModelForm):

    class Meta:
        model = models.Lote
        fields = ["stock_disponible", "cantidad_producida"]
    cantidad = forms.IntegerField(label = "Cantidad (*)")

    def __init__(self, *args, **kwargs):
        super(LoteStockForm, self).__init__(*args, **kwargs)
        self.fields['stock_disponible'].label = "Stock (*)"
        self.fields['cantidad_producida'].label = "producida(*)"
        self.fields['cantidad'].label = "Cantidad ( * )"



    def save(self, *args, **kwargs):
        lote= super(LoteStockForm, self).save(*args, **kwargs)
        print "cantuidad a modificar: ",self.cleaned_data['cantidad']
        lote.stock_disponible += self.cleaned_data['cantidad']
        print "stock final es: ",lote.stock_disponible
        lote.save()
        lote.producto_terminado.stock += self.cleaned_data['cantidad']
        lote.producto_terminado.save()
        return lote


    def clean(self):
        print "CLEAN POSTA"
        cleaned_data = super(LoteStockForm, self).clean()
        return cleaned_data


    def clean_cantidad_producida(self):
        print "clean_cantidad_producida "
        return self.cleaned_data["cantidad_producida"]

    def clean_stock_disponible(self):
        print "clean_stock_disponible "
        return self.cleaned_data["stock_disponible"]

    def clean_cantidad(self):
        print "clean_cantidad "
        c =self.cleaned_data['cantidad']
        cantidad_producida = self.cleaned_data['cantidad_producida']
        nueva_cantidad = self.cleaned_data['stock_disponible'] + c
        if nueva_cantidad > cantidad_producida:
            print "lanzo error"
            raise ValidationError("El stock disponible no debe superar la cantidad producida")
        elif nueva_cantidad < 0:
            raise ValidationError("El stock disponible no puede ser Negativo")


        return self.cleaned_data['cantidad']

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
        exclude = ['fecha_de_entrega', 'estado_pedido','insumos','descripcion','fecha_cancelacion']



class PedidoProveedorModificarForm(forms.ModelForm):
    class Meta:
        model = models.PedidoProveedor
        widgets = {
            'fecha_realizacion': forms.DateInput(attrs={'class': 'datepicker'})}
        exclude = ['fecha_de_entrega', 'estado_pedido','insumos','descripcion','proveedor','fecha_cancelacion']


class PedidoProveedorRecepcionarForm(forms.ModelForm):
    class Meta:
        model = models.PedidoProveedor
        widgets = {
            'fecha_de_entrega': forms.DateInput(attrs={'class': 'datepicker'})}
        exclude = ['fecha_realizacion','insumos','proveedor','fecha_cancelacion','estado_pedido']



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
        fields = ['cliente','fecha_inicio','fecha_cancelacion','dias']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'class': 'datepicker'}),
            'fecha_cancelacion': forms.DateInput(attrs={'class': 'datepicker'})}

    def clean(self):
        cleaned_data = super(PedidoClienteFijoForm, self).clean()
        if not self.errors:
            cliente = cleaned_data["cliente"]
            pedidos = cliente.pedidocliente_set.all()
            try:
                dias = cleaned_data["dias"]
            except:
                raise ValidationError("Debe marcar al menos un dia para la entrega.")
            for pedido in pedidos:
                if pedido.tipo_pedido == 1:
                    lista =pedido.pedidofijo.dias
                    for dia in dias:
                        if dia in lista:
                            raise ValidationError("Ya existen pedido/s de este cliente para el/los dias marcados.")

            if (cleaned_data["fecha_cancelacion"] !=None) and (cleaned_data["fecha_cancelacion"] < cleaned_data["fecha_inicio"]):
                raise ValidationError("Fecha de cancelacion debe ser mayor a la de inicio")
        return cleaned_data

    def clean_fecha_inicio(self):  #Django agota todas las instancas de validacion, por eso si fecha_inicio tenia error, posteriormente no se lo puede usar para validar porque tiene error
        fecha = self.cleaned_data['fecha_inicio']
        if fecha < datetime.date.today():
            raise ValidationError("Fecha de inicio debe ser mayor o igual a la fecha actual")
        return fecha


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

    def clean(self):
        cleaned_data = super(PedidoClienteOcacionalForm, self).clean()
        if not self.errors:
            cliente = cleaned_data["cliente"]
            pedidos = cliente.pedidocliente_set.all()
            dia = cleaned_data['fecha_entrega']
            for pedido in pedidos:
                if pedido.tipo_pedido == 2:
                    fecha =pedido.pedidoocacional.fecha_entrega
                    if dia == fecha:
                        raise ValidationError("Ya existe un pedido de este cliente para ese mismo dia. Modifique ese pedido") #como generar link??


    def clean_fecha_entrega(self):
        fecha = self.cleaned_data['fecha_entrega']
        if fecha < datetime.date.today():
            raise ValidationError("No se puede registrar un pedido para una fecha anterior a la actual")
        elif fecha.weekday() == 5 or fecha.weekday() == 6:
            raise ValidationError("No se puede registrar un pedido para un sabado o domingo, se entrega de lunes a viernes")
        return fecha

    def __init__(self, *args, **kwargs):
        super(PedidoClienteOcacionalForm, self).__init__(*args, **kwargs)


class PedidoClienteCambioForm(forms.ModelForm):
    class Meta:
        model = models.PedidoCambio
        widgets = {
           'fecha_entrega': forms.DateInput(attrs={'class': 'datepicker'})}
        exclude = ['productos','tipo_pedido']


    def clean(self):
            cleaned_data = super(PedidoClienteCambioForm, self).clean()
            if not self.errors:
                cliente = cleaned_data["cliente"]
                pedidos = cliente.pedidocliente_set.all()
                dia = cleaned_data['fecha_entrega']
                for pedido in pedidos:
                    if pedido.tipo_pedido == 3:
                        fecha =pedido.pedidocambio.fecha_entrega
                        if dia == fecha:
                            raise ValidationError("Ya existe un pedido de este cliente para ese mismo dia. Modifique ese pedido") #como generar link??



    def clean_fecha_entrega(self):
        fecha = self.cleaned_data['fecha_entrega']
        if fecha < datetime.date.today():
            raise ValidationError("No se puede registrar un pedido para una fecha anterior a la actual")
        elif fecha.weekday() == 5 or fecha.weekday() == 6:
            raise ValidationError("No se puede registrar un pedido para un sabado o domingo, se entrega de lunes a viernes")
        return fecha

    def __init__(self, *args, **kwargs):
        super(PedidoClienteCambioForm, self).__init__(*args, **kwargs)






#############################################################################
############################################################################



class LoteForm(forms.ModelForm):
    class Meta:
        model = models.Lote
        fields = ["producto_terminado","fecha_produccion","cantidad_producida"]
        widgets = {
           'fecha_produccion': forms.DateInput(attrs={'class': 'datepicker'}),
        }

    def save(self, *args, **kwargs):
        print "en metodo save del form de Lote"
        # Sobrecargar save devuelve el objeto apunto de ser guardado
        lote = super(LoteForm, self).save(*args, **kwargs)
        lote.stock_disponible = lote.cantidad_producida
        prod = lote.producto_terminado
        dias = prod.dias_vigencia
        print "DIAS DE VIGENCIA DEL PRODUCTO: ",dias
        delta = timedelta(days=dias)
        print  "DELTA A SUMAR ES: ",delta
        lote.fecha_vencimiento = lote.fecha_produccion + delta
        print "fecha de vencimiento del lote: " ,lote.fecha_vencimiento
        lote.save()
        return lote





    def clean_fecha_vencimiento(self):
        print "cleanb fecha vencimiento"
        fecha = self.cleaned_data['fecha_vencimiento']
        if fecha <= datetime.date.today():
            raise ValidationError("Fecha de vencimiento debe ser mayor a la actual")
        return fecha


    def clean_fecha_produccion(self):
        print "clean en fecha de produccion"
        fecha = self.cleaned_data['fecha_produccion']
        if fecha > datetime.date.today():
            raise ValidationError("No se puede registrar una produccion para una fecha adelantada")
        return fecha


#############################################################################
############################################################################

class ProductoExtraForm(forms.ModelForm):
    class Meta:
        model = models.ProductoExtra
        fields = ["cantidad","producto_terminado"]
    #productos_terminados = forms.ModelMultipleChoiceField(queryset=models.ProductoTerminado.objects.all())

    def clean_producto_terminado(self):
        print "en clean de producto terminado"
        prod = self.cleaned_data["producto_terminado"]
        print "producto:" ,prod
        return prod
        # aca tengo q agarrar el producto y salir a buscar a los lotes.




class HojaDeRutaForm(forms.Form):
    pedidos = forms.ModelMultipleChoiceField(queryset=models.PedidoCliente.objects.all())
    chofer = forms.ModelChoiceField(queryset=models.Chofer.objects.all())

    def save(self):
        pedidos = self.cleaned_data["pedidos"]
        chofer = self.cleaned_data["chofer"]
        print "EN SAVE DE HOJA DE RUTA"
        hoja = models.HojaDeRuta.objects.create(chofer = chofer)
        for pedido in pedidos:
            # por cada pedido tengo q crear una ENTREGA asociada a el
            for detalle in pedido.pedidoclientedetalle_set.all():
                #por cada detalle tengo q crear un detalle de entrega q apunte a uno o mas lotes para q cubran la cantidad buscada
                producto_buscado = detalle.producto_terminado
                cantidad_buscada = detalle.cantidad_producto
                #esta cantidad hay que salir a buscarla a los lotes
                lotes = models.Lote.objects.filter(producto_terminado = producto_buscado) #falta filtrar por no vencidos
                lotes = lotes.order_by("fecha_produccion") # ordenamos de los mas viejos a mas nuevos.
                for lote in lotes:
                    cantidad_reservada = lote.reservar_stock(cantidad_buscada)
                    cantidad_buscada -=  cantidad_reservada
                    if  cantidad_buscada == 0:
                        break; #busco otro detalle
		        if cantidad_buscada > 0:
			    print "no alcance a cubrir la cantidad: ", cantidad_buscada, "para el producto: ",producto_buscado
        print "fin de procesar los pedidos"
        hoja.save()
        return hoja
        ##










