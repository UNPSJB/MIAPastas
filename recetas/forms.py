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
        raise ValidationError("Cuit no valido")
        return cuit


class ModificarStockInsumoForm(forms.Form):
    insumo = forms.ModelChoiceField(queryset=models.Insumo.objects.all(), empty_label="(----)")
    cantidad = forms.IntegerField()
    unidad_medida = forms.ChoiceField(choices=models.Insumo.UNIDADES)
    unidad_medida.empty_label="(----)"
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
        if models.Proveedor.objects.filter(razon_social=razon_social).exists():
            raise ValidationError('Ya existe un Proveedor con esa Razon Social.')
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



class ProveedorModificarForm(forms.ModelForm):
    class Meta:
        model = models.Proveedor
        fields = ["cuit", "razon_social", "localidad","nombre_dueno","direccion","email","numero_cuenta","provincia","telefono","insumos" ]

    def __init__(self, *args, **kwargs):
        super(ProveedorModificarForm, self).__init__(*args, **kwargs)
        #self.fields['fecha_creacion'].widget.attrs.update({'class' : 'datepicker'})

    def clean_razon_social(self):
        razon_social = self.cleaned_data['razon_social']
        razon_social = texto_lindo(razon_social, True)
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
    ''' 
    Formulario que se usa para decrementar el stock de un lote debido a una perdida (rotura, vencimiento, otro)
    '''
    class Meta:
        model = models.Lote
        fields = ["stock_disponible", "cantidad_producida","stock_reservado"]
    cantidad = forms.IntegerField(min_value=0, max_value=99999999)
    descripcion = forms.CharField(max_length=200,required=False,widget=forms.Textarea)
    select_causas = forms.ChoiceField(widget=forms.RadioSelect, choices=models.CAUSAS_DECREMENTO_STOCK)


    def __init__(self, *args, **kwargs):
        super(LoteStockForm, self).__init__(*args, **kwargs)
        self.fields['stock_disponible'].label = "Stock (*)"
        self.fields['cantidad_producida'].label = "producida(*)"
        self.fields['cantidad'].label = "Cantidad ( * )"
        self.mensaje_error = ""

    def save(self, *args, **kwargs):
        ''' Metodo que decrementa el stock en la cantidad ingresada de la perdida y crea una instancia 
            de perdida para poder tenes un historial de esos decrementos.
        '''
        print "en save"
        lote= super(LoteStockForm, self).save(*args, **kwargs)
        lote.decrementar_stock_disponible(self.cleaned_data['cantidad'])
        perdida_instancia = models.PerdidaStock.objects.create(cantidad_perdida= self.cleaned_data['cantidad'],descripcion = self.cleaned_data['descripcion'],lote=lote,causas=self.cleaned_data['select_causas'])
        perdida_instancia.save()
        return lote

    def clean(self):
        ''' Metodo que lanza mensajes de errores si lo hubieron en las validaciones del formulario
        '''
        if len(self.mensaje_error) > 0:
           raise ValidationError(self.mensaje_error)
        cleaned_data = super(LoteStockForm, self).clean()
        return cleaned_data

    #def clean_cantidad_producida(self):
     #   return self.cleaned_data["cantidad_producida"]

    def clean_cantidad(self):
        ''' Metodo que verifica que:
                El stock resultante de la decrementacion no sea negativo.
                La cantidad a decrementar ingresada sea mayor a 0.
                El stock resultante de la decrementacion no sea mayor al stock que se dispone en el deposito.
                (lo ultimo se debe a que no se puede dar como perdidos productos que se encuentren reservados porque
                  fueron cargados en una hoja de ruta y se encuantran en etapa de envio)
        '''
        c =self.cleaned_data['cantidad']
        nueva_cantidad = self.cleaned_data['stock_disponible'] - c
        if nueva_cantidad < 0:
            self.mensaje_error = "ERROR: El stock disponible no puede ser Negativo."
        elif c == 0:
            self.mensaje_error = "ERROR: La cantidad debe ser mayor a 0."
        elif self.cleaned_data['cantidad'] > (self.cleaned_data['stock_disponible'] - self.cleaned_data['stock_reservado']):
            self.mensaje_error = "ERROR: No puede decrementar esa cantidad. Primero debe rendir las hojas de ruta creadas"
        return self.cleaned_data['cantidad']


class CiudadForm(forms.ModelForm):
    class Meta:
        model = models.Ciudad
        fields = ["nombre","codigo_postal","zona"]  

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        nombre = texto_lindo(nombre, True)
        if models.Ciudad.objects.filter(nombre=nombre).exists():
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



class ClienteModificarForm(forms.ModelForm):
    class Meta:
        model = models.Cliente
        fields = ["cuit","razon_social","nombre_dueno","ciudad","direccion","telefono","email","es_moroso"]



    def clean_razon_social(self):
        razon_social = self.cleaned_data['razon_social']
        cuit = self.cleaned_data['cuit']
        razon_social = texto_lindo(razon_social, True)
        return razon_social

    def clean_nombre_dueno(self):
        nombre_dueno = self.cleaned_data['nombre_dueno']
        nombre_dueno = texto_lindo(nombre_dueno, True)
        return nombre_dueno

    def clean_direccion(self):
        direccion = self.cleaned_data['direccion']
        direccion = texto_lindo(direccion, True)
        return direccion



class ClienteAltaForm(forms.ModelForm):
    class Meta:
        model = models.Cliente
        fields = ["cuit","razon_social","nombre_dueno","ciudad","direccion","telefono","email"]
        exclude = ['es_moroso']

    def clean_razon_social(self):
        razon_social = self.cleaned_data['razon_social']
        cuit = self.cleaned_data['cuit']
        razon_social = texto_lindo(razon_social, True)
        if models.Cliente.objects.filter(razon_social=razon_social).exists():
            if models.Cliente.objects.filter(cuit=cuit).exists():
                raise ValidationError('Ya existe un Cliente con esa Razon Social.')
        return razon_social

    def clean_nombre_dueno(self):
        nombre_dueno = self.cleaned_data['nombre_dueno']
        nombre_dueno = texto_lindo(nombre_dueno, True)
        return nombre_dueno

    def clean_direccion(self):
        direccion = self.cleaned_data['direccion']
        direccion = texto_lindo(direccion, True)
        return direccion

    def clean_es_moroso(self):
        moroso = self.cleaned_data["es_moroso"]
        print "EN CLEAN DE MOROSO: ",moroso
        return moroso



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
    ''' Formulario "padre" de los tres tipos de pedidos (Fijo, Ocacional y de Cambio)
        Se lo usa cuando se quiere manejar a los pedidos de manera general sin importar su tipo.
    '''
    class Meta:
        model = models.PedidoCliente
        fields = ["tipo_pedido","cliente"]


class PedidoClienteFijoForm(forms.ModelForm):
    ''' 
    Formulario que se utiliza para el alta y modificacion de un pedido Fijo
    '''
    class Meta:
        model = models.PedidoFijo
        dias = MultipleChoiceField(required=True, widget=CheckboxSelectMultiple, choices=models.TIPODIAS)
        fields = ['cliente','fecha_inicio','fecha_cancelacion','dias']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'class': 'datepicker'}),
            'fecha_cancelacion': forms.DateInput(attrs={'class': 'datepicker'})}

                
    def clean(self):
        ''' 
        Metodo que realiza validaciones sobre los campos del Formulario.
            Validaciones:
                Que la fecha de cancelacion (si existe) sea mayor a la de inicio y a la fecha actual
                Que se defina almenos un dia de la semana (lunes a viernes)
                Que no exista otro pedido fijo de ese mismo cliente para los dias seleccionados.
        '''
        cleaned_data = super(PedidoClienteFijoForm, self).clean()
        if not self.errors:
            cliente = cleaned_data["cliente"]
            pedidos = cliente.pedidocliente_set.filter(activo=True)
            try:
                dias = cleaned_data["dias"]
            except:
                raise ValidationError("Debe marcar al menos un dia para la entrega.")
            for pedido in pedidos:
                if pedido.tipo_pedido == 1:
                    lista =pedido.pedidofijo.dias
                    try:
                        id_pedido_instancia_existente = int(self.my_arg)
                    except:
                        id_pedido_instancia_existente = 0 #porque el id 0 no existe nunca asi no tiene problemas en el if para el alta
                    for dia in dias:
                        if dia in lista and pedido.id != id_pedido_instancia_existente:
                            id = str(pedido.id)
                            raise forms.ValidationError(((mark_safe('Ya existen pedido/s de este cliente para el/los dias marcados. <a href="/pedidosCliente/Modificar/'+id+'">Modificar el pedido existente</a>'))))

            if (cleaned_data["fecha_cancelacion"] !=None) and (cleaned_data["fecha_cancelacion"] <= cleaned_data["fecha_inicio"]):
                raise ValidationError("Fecha de cancelacion debe ser mayor a la de inicio")
            if (cleaned_data["fecha_cancelacion"] !=None) and (cleaned_data["fecha_cancelacion"] < datetime.date.today()):
                raise ValidationError("Fecha de cancelacion debe ser mayor a la fecha actual")
        return cleaned_data

    def clean_fecha_inicio(self):  #Django agota todas las instancas de validacion, por eso si fecha_inicio tenia error, posteriormente no se lo puede usar para validar porque tiene error
        ''' Metodo que valida en el alta de un pedido fijo que la fecha de inicio no sea menor a la fecha actual.
        '''
        fecha = self.cleaned_data['fecha_inicio']
        if fecha < datetime.date.today() and self.my_arg == None:
            raise ValidationError("Fecha de inicio debe ser mayor o igual a la fecha actual")
        return fecha

    def __init__(self, *args, **kwargs):
        self.my_arg = kwargs.pop('my_arg') if 'my_arg' in kwargs else None
        super(PedidoClienteFijoForm, self).__init__(*args, **kwargs)




class PedidoClienteDetalleForm(forms.ModelForm):
    ''' 
    Formulario que se usa para los detalles de los pedidos de cualquier tipo de pedido
    '''
    class Meta:
        model = models.PedidoClienteDetalle
        exclude = ['pedido_cliente'] #setea todos campos menos pedido


class PedidoClienteOcacionalForm(forms.ModelForm):
    ''' Formulario que se utiliza para el alta y modificacion de un pedido Ocacinoal
    '''
    class Meta:
        model = models.PedidoOcacional
        exclude = ['productos','tipo_pedido','activo']
        widgets = {
           'fecha_entrega': forms.DateInput(attrs={'class': 'datepicker'})}
    
    def clean(self):
        ''' Metodo que realiza validaciones sobre los campos del Formulario.
            Se valida que el cliente no tenga pedidos ocacionales para ese mismo dia      
        '''
        
        cleaned_data = super(PedidoClienteOcacionalForm, self).clean()
        if not self.errors:
            cliente = cleaned_data["cliente"]
            pedidos = cliente.pedidocliente_set.filter(activo=True)
            dia = cleaned_data['fecha_entrega']
            for pedido in pedidos:
                if pedido.tipo_pedido == 2:
                    fecha =pedido.pedidoocacional.fecha_entrega
                    try:
                        id_pedido_instancia_existente = int(self.my_arg)
                    except:
                        id_pedido_instancia_existente = 0 #porque el id 0 no existe nunca asi no tiene problemas en el if para el alta
                    if (dia == fecha) and pedido.id != id_pedido_instancia_existente:
                        id = str(pedido.id)
                        raise forms.ValidationError(((mark_safe('Ya existe un pedido de este cliente para ese mismo dia. Modifique ese pedido. <a href="/pedidosCliente/Modificar/'+id+'">Modificar el pedido existente</a>'))))
            

    def clean_fecha_entrega(self):
        ''' Metodo que verifica que:
                La fecha de entrega no sea menor a la actual.
                El dia seleccionado para la entrega sea de lunes a viernes
        '''
        fecha = self.cleaned_data['fecha_entrega']
        if fecha < datetime.date.today():
            raise ValidationError("No se puede registrar un pedido para una fecha anterior a la actual")
        elif fecha.weekday() == 5 or fecha.weekday() == 6:
            raise ValidationError("No se puede registrar un pedido para un sabado o domingo, se entrega de lunes a viernes")
        return fecha

    def __init__(self, *args, **kwargs):
        self.my_arg = kwargs.pop('my_arg') if 'my_arg' in kwargs else None
        super(PedidoClienteOcacionalForm, self).__init__(*args, **kwargs)


class PedidoClienteCambioForm(forms.ModelForm):
    ''' Formulario que se utiliza para el alta y modificacion de un pedido de Cambio
    '''
    class Meta:
        model = models.PedidoCambio
        widgets = {
           'fecha_entrega': forms.DateInput(attrs={'class': 'datepicker'})}
        exclude = ['productos','tipo_pedido','activo']


    def clean(self):
            ''' 
                Metodo que realiza validaciones sobre los campos del Formulario.
                Se valida que el cliente no tenga pedidos de cambio para ese mismo dia      
            '''
            cleaned_data = super(PedidoClienteCambioForm, self).clean()
            if not self.errors:
                cliente = cleaned_data["cliente"]
                pedidos = cliente.pedidocliente_set.filter(activo=True)
                dia = cleaned_data['fecha_entrega']
                for pedido in pedidos:
                    if pedido.tipo_pedido == 3:
                        fecha =pedido.pedidocambio.fecha_entrega
                        try:
                            id_pedido_instancia_existente = int(self.my_arg)
                        except:
                            id_pedido_instancia_existente = 0 #porque el id 0 no existe nunca asi no tiene problemas en el if para el alta
                        if (dia == fecha) and pedido.id != id_pedido_instancia_existente:
                            id = str(pedido.id)
                            raise forms.ValidationError(((mark_safe('Ya existe un pedido de este cliente para ese mismo dia. Modifique ese pedido. <a href="/pedidosCliente/Modificar/'+id+'">Modificar el pedido existente</a>'))))


    def clean_fecha_entrega(self):
        ''' Metodo que verifica que:
                La fecha de entrega no sea menor a la actual.
                El dia seleccionado para la entrega sea de lunes a viernes
        '''
        fecha = self.cleaned_data['fecha_entrega']
        if fecha < datetime.date.today():
            raise ValidationError("No se puede registrar un pedido para una fecha anterior a la actual")
        elif fecha.weekday() == 5 or fecha.weekday() == 6:
            raise ValidationError("No se puede registrar un pedido para un sabado o domingo, se entrega de lunes a viernes")
        return fecha

    def __init__(self, *args, **kwargs):
        self.my_arg = kwargs.pop('my_arg') if 'my_arg' in kwargs else None
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

class HojaDeRutaForm(forms.ModelForm):
    
    class Meta:
        model = models.HojaDeRuta
        fields = ["chofer"]
    
class EntregaForm(forms.ModelForm):
    class Meta:
        model = models.Entrega
        fields = ["pedido"]
    
    def save(self, hoja_de_ruta):
        entrega = super(EntregaForm, self).save(commit=False)
        entrega.hoja_de_ruta = hoja_de_ruta
        entrega.save()
        return entrega

class BaseEntregaFormset(BaseFormSet):
    def clean(self):
        print "en clean de base de entregaFormset"

EntregaFormsetClass = formset_factory(EntregaForm,formset=BaseEntregaFormset,extra=0)

class EntregaDetalleForm(forms.ModelForm):
    class Meta:
        model = models.EntregaDetalle
        fields = ["cantidad_entregada","entrega","pedido_cliente_detalle","producto_terminado"]

    def save(self):        
        det = super(EntregaDetalleForm, self).save(commit=False)
        if det.pedido_cliente_detalle is None and det.cantidad_entregada == 0:
            return # no sirve para nada
        #for p in self.cleaned_data["entrega"].hoja_de_ruta.productosllevados_set.all():
         #   if p.producto_terminado == det.get_producto_terminado():                
          #      det.precio = p.precio * det.cantidad_entregada 
           #     break
        det.set_precio()
        det.save()
        det.entrega.pedido.cliente.aumentar_saldo(det.precio)
            

class BaseEntregaDetalleFormset(BaseFormSet):
    def clean(self):        
        print "en clean principal base"
       

EntregaDetalleFormset = formset_factory(EntregaDetalleForm, formset=BaseEntregaDetalleFormset,extra=0)


  ############### TOTALES PARA BUSCAR EN LOTES ####################

class ProductosLlevadosForm(forms.ModelForm):
    class Meta:
        model = models.ProductosLlevados
        fields = ["cantidad_pedida","producto_terminado"]

    def save(self, hoja_de_ruta):
        producto_llevado= super(ProductosLlevadosForm, self).save(commit=False)
        producto_llevado.hoja_de_ruta = hoja_de_ruta
        producto_llevado.precio = producto_llevado.producto_terminado.precio
        producto_llevado.save()
        producto_llevado.generar_detalles()
         # si no tengo stock para el producto pedido, no lo LLEVO 
        #if producto_llevado.cantidad_enviada == 0:
        #    producto_llevado.delete()
        #    return None
        return producto_llevado


class BaseProductoLlevadoFormset(BaseFormSet):
    def clean(self):
        print "en clean de base de prod llevado formset"
    # EN ESTE FORMULARIO TENGO Q RECORRER LOTES Y CREAR LAS INSTANCIAS DE LOTES LLEVADOS (PRODEXTRAS)
    

ProductoLlevadoFormsetClass = formset_factory(ProductosLlevadosForm,formset=BaseEntregaDetalleFormset,extra=0)

class ProdLlevadoDetalleRendirForm(forms.Form):
    detalle_id = forms.ModelChoiceField(models.ProductosLlevadosDetalle.objects.all())
    cantidad_sobrante = forms.IntegerField()

    def save(self):
        """ recupera el detalle de prod llevado, y en base a la cantidad sobrane actualiza el stock 
            reservado y disponible del LOTE """
        det = self.cleaned_data["detalle_id"]
        cant_sobrante = self.cleaned_data["cantidad_sobrante"]
        det.cantidad_sobrante = cant_sobrante
        det.lote.decrementar_stock_reservado(det.cantidad)
        cant_vendida = det.cantidad - cant_sobrante
        det.lote.decrementar_stock_disponible(cant_vendida)
        det.save()

ProdLlevadoFormset_class = formset_factory(ProdLlevadoDetalleRendirForm)

############### REGISTRAR PAGOS PARA ENTREGAS EN RENDICION ####################

class CobroEntregaRendir(forms.Form):
    entrega = forms.ModelChoiceField(models.Entrega.objects.all())
    cantidad_abonada = forms.FloatField()
    nro_doc = forms.IntegerField()

    def clean(self):
        """ Verifica que el nro de doc ingresado no exista.
            si el monto abonado = precio total de lo entregado, se busca en Factura
            si el monto abonado < precio total de lo entregado, se busca en Recibo
        """        
        cleaned_data = super(CobroEntregaRendir, self).clean()
        cantidad_abonada = self.cleaned_data["cantidad_abonada"]
        entrega = self.cleaned_data["entrega"]
        nro_doc = self.cleaned_data["nro_doc"]        
        if cantidad_abonada == entrega.precio_total():
            obj = models.Factura 
        elif cantidad_abonada < entrega.precio_total():
            print "por crear recibo"
            obj = models.Recibo
        else:
            raise Validaciones("Se pago de Mas")
        o = obj.objects.filter(numero=nro_doc)       
        if len(o) > 0:   
            print "Error doc ya existe"         
            raise ValidationError("Ya existe una factura con el numero %d "%(nro_doc))
        return cleaned_data




    def save(self):
        """ Si la cantidad abonada es igual al precio total de la Entrega se crea una Factura
            con nro_doc y se asocia a la Entrega, si cantidad abonada es menor al precio total
            se crea un resibo"""
        cantidad_abonada = self.cleaned_data["cantidad_abonada"]
        entrega = self.cleaned_data["entrega"]
        nro_doc = self.cleaned_data["nro_doc"]
        if cantidad_abonada == entrega.precio_total():            
            entrega.cobrar_con_factura(cantidad_abonada, nro_doc)
        else:            
            entrega.cobrar_con_recibo(cantidad_abonada, nro_doc)
        
        self.cleaned_data["entrega"].pedido.cliente.decrementar_saldo(self.cleaned_data["cantidad_abonada"])



  ############### fin ####################
