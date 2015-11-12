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
from django.utils.safestring import mark_safe
from django.forms.formsets import formset_factory
from django.forms import BaseFormSet, formset_factory
from django.forms.models import inlineformset_factory

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
                            id = str(pedido.id)
                            raise forms.ValidationError(((mark_safe('Ya existen pedido/s de este cliente para el/los dias marcados. <a href="/pedidosCliente/Modificar/'+id+'">Modificar el pedido existente</a>'))))

            if (cleaned_data["fecha_cancelacion"] !=None) and (cleaned_data["fecha_cancelacion"] < cleaned_data["fecha_inicio"]):
                raise ValidationError("Fecha de cancelacion debe ser mayor a la de inicio")
        return cleaned_data

    def clean_fecha_inicio(self):  #Django agota todas las instancas de validacion, por eso si fecha_inicio tenia error, posteriormente no se lo puede usar para validar porque tiene error
        fecha = self.cleaned_data['fecha_inicio']
        if fecha < datetime.date.today():
            raise ValidationError("Fecha de inicio debe ser mayor o igual a la fecha actual")
        return fecha


#probando probando ivan ivan
class PedidoClienteFijoModificarForm(forms.ModelForm):
#mi idea: poner en models.PedidoCliente un atributo generico que sea fechaCancelacion...
    class Meta:
        model = models.PedidoFijo
        dias = MultipleChoiceField(required=True, widget=CheckboxSelectMultiple, choices=models.TIPODIAS)
        fields = ['cliente','dias']
        #widgets = {
        #    'fecha_inicio': forms.DateInput(attrs={'class': 'datepicker'})}

       # widgets = {
        #    'fecha_inicio': forms.DateInput(attrs={'class': 'datepicker'}),
         #   'fecha_cancelacion': forms.DateInput(attrs={'class': 'datepicker'})}#ponerlo como un boton "cancelarPedido"
    #def clean_fecha_inicio(self):  #Django agota todas las instancas de validacion, por eso si fecha_inicio tenia error, posteriormente no se lo puede usar para validar porque tiene error
     #   cleaned_data = super(PedidoClienteFijoForm, self).clean()
      #  cliente = cleaned_data["cliente"]
       # pedidos = cliente.pedidocliente_set.all()
       # fecha = self.cleaned_data['fecha_inicio']

        #if fecha < datetime.date.today():
         #   raise ValidationError("Fecha de inicio debe ser mayor o igual a la fecha actual")
        #return fecha


class PedidoClienteDetalleForm(forms.ModelForm):
    class Meta:
        model = models.PedidoClienteDetalle
        exclude = ['pedido_cliente'] #setea todos campos menos pedido





class PedidoClienteOcacionalForm(forms.ModelForm):

    class Meta:
        model = models.PedidoOcacional
        exclude = ['productos','tipo_pedido','activo']
        widgets = {
           'fecha_entrega': forms.DateInput(attrs={'class': 'datepicker'})}
    my_field = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super(PedidoClienteOcacionalForm, self).clean()
        print "pruebaaaaaaaaaa", self.instance.my_field, " s "
        if not self.errors:
            cliente = cleaned_data["cliente"]
            pedidos = cliente.pedidocliente_set.all()
            dia = cleaned_data['fecha_entrega']
            for pedido in pedidos:
                if pedido.tipo_pedido == 2:
                    fecha =pedido.pedidoocacional.fecha_entrega
                    print "iddddddddd",cleaned_data, " "
                    if (dia == fecha):
                        id = str(pedido.id)
                        raise forms.ValidationError(((mark_safe('Ya existe un pedido de este cliente para ese mismo dia. Modifique ese pedido. <a href="/pedidosCliente/Modificar/'+id+'">Modificar el pedido existente</a>'))))


    def clean_fecha_entrega(self):
        fecha = self.cleaned_data['fecha_entrega']
        if fecha < datetime.date.today():
            raise ValidationError("No se puede registrar un pedido para una fecha anterior a la actual")
        elif fecha.weekday() == 5 or fecha.weekday() == 6:
            raise ValidationError("No se puede registrar un pedido para un sabado o domingo, se entrega de lunes a viernes")
        return fecha

    def __init__(self, *args, **kwargs):
        try:
            my_arg = kwargs.pop('my_arg')
            self.url = kwargs.pop('my_arg')
            super(PedidoClienteOcacionalForm, self).__init__(*args, **kwargs)
            self.instance.my_field=my_arg
        except:
            super(PedidoClienteOcacionalForm, self).__init__(*args, **kwargs)

        
        


class PedidoClienteCambioForm(forms.ModelForm):
    class Meta:
        model = models.PedidoCambio
        widgets = {
           'fecha_entrega': forms.DateInput(attrs={'class': 'datepicker'})}
        exclude = ['productos','tipo_pedido','activo']


    def clean(self):
            cleaned_data = super(PedidoClienteCambioForm, self).clean()
            if not self.errors:
                cliente = cleaned_data["cliente"]
                pedidos = cliente.pedidocliente_set.all()
                dia = cleaned_data['fecha_entrega']
                for pedido in pedidos:
                    if pedido.tipo_pedido == 3:
                        fecha =pedido.pedidocambio.fecha_entrega
                        if dia == fecha :
                            id = str(pedido.id)
                            raise forms.ValidationError(((mark_safe('Ya existe un pedido de este cliente para ese mismo dia. Modifique ese pedido. <a href="/pedidosCliente/Modificar/'+id+'">Modificar el pedido existente</a>'))))


    def clean_fecha_entrega(self):
        fecha = self.cleaned_data['fecha_entrega']
        if fecha < datetime.date.today():
            raise ValidationError("No se puede registrar un pedido para una fecha anterior a la actual")
        elif fecha.weekday() == 5 or fecha.weekday() == 6:
            raise ValidationError("No se puede registrar un pedido para un sabado o domingo, se entrega de lunes a viernes")
        return fecha

    def __init__(self, *args, **kwargs):
        my_arg = kwargs.pop('my_arg')

        super(PedidoClienteCambioForm, self).__init__(*args, **kwargs)
        
        self.fields['my_field'] = forms.CharField(initial=my_arg)





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

class HojaDeRutaForm(forms.ModelForm):
    #pedidos = forms.ModelMultipleChoiceField(queryset=models.PedidoCliente.objects.all())
    #chofer = forms.ModelChoiceField(queryset=models.Chofer.objects.all())
    class Meta:
        model = models.HojaDeRuta
        fields = ["chofer"]
    def clean_chofer(self):
        chofer = self.cleaned_data["chofer"]
        print "en clean de chofer de hoja de ruta:", chofer
        return chofer



class EntregaForm(forms.ModelForm):
    class Meta:
        model = models.Entrega
        fields = ["pedido"]

    def clean_pedido(self):
        pedido = self.cleaned_data["pedido"]
        print "en clean pedido de ENTREGA", pedido
        return pedido

    def save(self, hoja_de_ruta):
        entrega = super(EntregaForm, self).save(commit=False)
        entrega.hoja_de_ruta = hoja_de_ruta
        entrega.save()
        #entrega.generar_detalles() # esto gnera edtalles pero no recorre LOTES!
        return entrega


class EntregaDetalleForm(forms.ModelForm):
    class Meta:
        model = models.EntregaDetalle
        fields = ["cantidad_entregada"]
    detalle= forms.ModelChoiceField(models.EntregaDetalle.objects.all())

    def save(self):
        print "EN SAVE PAPA: ",self.instance.pk

    def rendir_detalle(self):
        """ Este metodo, con id_detalle, busca al EntregaDetalle
            le setea su cantidad entregada. Si la cant entregada es menor igual a 0 BORRA ese detalle.
        """
        detalle_entrega = self.cleaned_data["detalle"]
        cantidad_nueva = self.cleaned_data["cantidad_entregada"]
        detalle_entrega.cantidad_entregada = cantidad_nueva
        print "cantidad entregada final: ",detalle_entrega.cantidad_entregada
        detalle_entrega.save()

class BaseEntregaDetalleFormset(BaseFormSet):
    def clean(self):
        productos_totales={}
        if any(self.errors):
            return
        for f in self.forms:
            detalle = f.cleaned_data["detalle"]
            try:
                productos_totales[detalle.get_producto_terminado()] += f.cleaned_data["cantidad_entregada"]
            except:
                productos_totales[detalle.get_producto_terminado()] = 0
                productos_totales[detalle.get_producto_terminado()] += f.cleaned_data["cantidad_entregada"]
        productos_llevados = self.forms[0].cleaned_data["detalle"].entrega.hoja_de_ruta.productosllevados_set.all()
        for llevado in productos_llevados:
            cant_entregada = productos_totales[llevado.producto_terminado]
            cant_llevada = llevado.cantidad_enviada
            if cant_entregada > cant_llevada:
                raise ValidationError("Se entregaste mas productos de los que llevaste")


EntregaDetalleFormset = formset_factory(EntregaDetalleForm, formset=BaseEntregaDetalleFormset,extra=0)
EntregaDetalleInlineFormset = inlineformset_factory(models.Entrega, models.EntregaDetalle,fields=("cantidad_entregada",))


  ############### TOTALES PARA BUSCAR EN LOTES ####################
class ProductosLlevadosForm(forms.ModelForm):
    class Meta:
        model = models.ProductosLlevados
        fields = ["cantidad_pedida","producto_terminado"]


    # EN ESTE FORMULARIO TENGO Q RECORRER LOTES Y CREAR LAS INSTANCIAS DE LOTES LLEVADOS (PRODEXTRAS)
    def save(self, hoja_de_ruta):
        productos_llevados= super(ProductosLlevadosForm, self).save(commit=False)
        print "PROCUTO LLEVADO TIENE LA CANTIDAD: ",productos_llevados.cantidad_pedida,productos_llevados.cantidad_enviada
        print "Y TIENE EL PRODUCTO, ",productos_llevados.producto_terminado
        productos_llevados.hoja_de_ruta = hoja_de_ruta
        productos_llevados.save()
        productos_llevados.generar_detalles()

class ProdLlevadoDetalleRendirForm(forms.Form):
    detalle_id = forms.ModelChoiceField(models.ProductosLlevadosDetalle.objects.all())
    cantidad_sobrante = forms.IntegerField()

    def save(self):
        """ recupera el detalle de prod llevado, y en base a la cantidad sobrane actualiza el stock reservado y disponible del LOTE """
        det = self.cleaned_data["detalle_id"]
        cant_sobrante = self.cleaned_data["cantidad_sobrante"]
        #det.lote.decrementar_stock_reservado(det.cantidad_enviada)
        det.cantidad_sobrante = cant_sobrante
        print "EN RENDIR DETALLE: ",det.lote.nro_lote
        det.lote.decrementar_stock_reservado(det.cantidad)
        cant_vendida = det.cantidad - cant_sobrante
        det.lote.decrementar_stock_disponible(cant_vendida)
        det.save()



  ############### COBRAR A CLIENTE ####################

