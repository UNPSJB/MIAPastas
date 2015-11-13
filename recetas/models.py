# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import MinValueValidator
from datetime import date
import datetime
from multiselectfield import MultiSelectField
from django.utils import timezone

TIPODIAS = (
        (1, "lunes"),
        (2, "martes"),
        (3, "miercoles"),
        (4,"jueves"),
        (5,"viernes")
      )

# Create your models here.
#********************************************************#
               #     C H O F E R E S    #
#********************************************************#
class Chofer (models.Model):
    FILTROS = ['cuit_icontains', 'nombre_icontains']
    cuit= models.CharField(max_length=20, unique=True)
    nombre= models.CharField(max_length=100)
    direccion= models.CharField(max_length=100)
    telefono=models.PositiveIntegerField()
    e_mail=models.CharField(max_length=100)

    def __str__(self):
        return "%s" % (self.nombre)


#********************************************************#
               #     I N S U M O     #
#********************************************************#
def stock_litros_kg(cant):
    cant= cant * 1000
    return cant

def stock_unidad(cant):
    return cant

def stock_docena(cant):
    cant = cant * 12
    return cant



class Insumo(models.Model):
    FILTROS = ['nombre__icontains', 'stock__lte']



    NONE = 0
    GRAMO = 1
    CM3 = 2
    UNIDAD = 3
    KG = 4
    LITRO = 5
    DOCENA = 6
    MAPLE = 7
    TUPLAS = [(GRAMO,KG),
              (CM3,LITRO),
              (UNIDAD,DOCENA,MAPLE)]

    UNIDADES_BASICAS = (
        (GRAMO, "g"),
        (CM3, "cm3"),
        (UNIDAD, "unidad")
    )

    UNIDADES_DERIVADAS = (
        (KG, "kg"),
        (LITRO, "litro"),
        (DOCENA, "docena"),
        (MAPLE, "maple")
    )

    UNIDADES = UNIDADES_BASICAS + UNIDADES_DERIVADAS

    CONVERT = {
        NONE: lambda cantidad: cantidad,
        GRAMO: lambda cantidad: cantidad,
        CM3: lambda cantidad: cantidad,
        UNIDAD: lambda cantidad: cantidad,
        KG: lambda cantidad: cantidad * 1000,
        LITRO: lambda cantidad: cantidad * 1000,
        DOCENA: lambda cantidad: cantidad * 12,
        MAPLE: lambda cantidad: cantidad * 30
    }

    FORMAT = {
        GRAMO: lambda cantidad: "%s.%s kg" % (cantidad // 1000, cantidad % 1000),
        CM3: lambda cantidad: "%s.%s litros" % (cantidad // 1000, cantidad % 1000),
        UNIDAD: lambda cantidad: "%s docenas y %s unidades" % (cantidad // 12, cantidad % 12)
    }

    nombre = models.CharField(max_length=100, unique=True, help_text="El nombre del insumo")
    descripcion = models.TextField("Descripcón")
    stock = models.IntegerField(blank=True, null=True, default=0)
    unidad_medida = models.PositiveSmallIntegerField(choices=UNIDADES_BASICAS)

    # Control de stock
    def incrementar(self, cantidad, unidad=NONE):
        self.stock += self.CONVERT[unidad](cantidad)

    def decrementar(self, cantidad, unidad=NONE):
        print "voy a decrementar del insumo ",self.nombre, "la cantidad: ",cantidad, "unidad medida: ",unidad
        self.stock -= self.CONVERT[unidad](cantidad)

    modificar_stock = incrementar

    def get_stock_humano(self):
        return self.FORMAT[self.unidad_medida](self.stock)

    def __str__(self):
        return "%s (%s)" % (self.nombre, self.get_unidad_medida_display())


#********************************************************#
            #     P R O D U C T O S     #
#********************************************************#

class ProductoTerminado(models.Model):

    FILTROS = ['nombre__icontains','stock__lte']
    nombre = models.CharField(max_length=100,unique=True,help_text="El nombre del producto")
    stock = models.PositiveIntegerField(default = 0)
    precio= models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0,00)])
    dias_vigencia = models.PositiveIntegerField(default=01)
    #http://blog.p3infotech.in/2013/enforcing-minimum-and-maximum-values-in-django-model-fields/


    def __str__(self):
        return "%s"% self.nombre



#********************************************************#
               #     R E C E T A S    #
#********************************************************#


class Receta(models.Model):

    FILTROS = ['nombre__icontains','producto_terminado']
    fecha_creacion = models.DateField(auto_now_add = True)
    nombre = models.CharField(max_length=100, unique=True,help_text="El nombre de la receta")
    descripcion = models.TextField()
    cant_prod_terminado= models.PositiveIntegerField()
    producto_terminado = models.ForeignKey(ProductoTerminado)
    insumos = models.ManyToManyField(Insumo, through="RecetaDetalle")


    def __str__(self):
        return "%s (%d) Bolsines" % (self.nombre, self.cant_prod_terminado)


class RecetaDetalle(models.Model):
    cantidad_insumo = models.PositiveIntegerField()
    insumo = models.ForeignKey(Insumo)
    receta = models.ForeignKey(Receta)


#********************************************************#
            #     P R O V E E D O R E S    #
#********************************************************#

class Proveedor(models.Model):

    FILTROS = ['cuit__icontains','razon_social__icontains','localidad__icontains']
    razon_social = models.CharField(max_length=100, unique=True)
    nombre_dueno = models.CharField(max_length=100, unique=True)
    direccion = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=30, unique=True, blank=True,null=True) #blank=True indica que puede estar el campo vacio
    localidad = models.CharField(max_length=50, unique=True)
    numero_cuenta= models.PositiveIntegerField(unique=True)
    provincia = models.CharField(max_length=50, unique=True)
    telefono= models.PositiveIntegerField()
    cuit= models.PositiveIntegerField(unique=True)
    insumos= models.ManyToManyField(Insumo,related_name='proveedores')#con related_name='proveedores' los objetos insumos puede llamar a sus proveedores por "proveedores"
#RELACION UNO A MUCHOS CON pedidosProveedor

    def __str__(self):
        return "%s (%d %s)" % (self.razon_social, self.telefono, self.cuit)


#********************************************************#
               #     Z O N A S    #
#********************************************************#

class Zona(models.Model):

    FILTROS = ['nombre__icontains']
    nombre = models.CharField(max_length=100, unique=True)
    #el campo "activo" es para las bajas logicas
    #activo = models.BooleanField(default=True);

    def __str__(self):
        return (self.nombre)



#********************************************************#
               #     C I U D A D E S    #
#********************************************************#
class Ciudad(models.Model):

    FILTROS = ['nombre__icontains','codigo_postal__icontains','zona']
    nombre = models.CharField(max_length=100, unique=True)
    codigo_postal = models.PositiveIntegerField(unique=True)
    zona = models.ForeignKey(Zona,related_name="ciudades")

    def __str__(self):
        return "%s (%d %s)" % (self.nombre, self.codigo_postal, self.zona)





#********************************************************#
               #     C L I E N T E S    #
#********************************************************#
class Cliente(models.Model):

    FILTROS = ['cuit_cuil__icontains','razon_social__icontains','ciudad','es_moroso']#'zona_icontains'
    cuit_cuil = models.PositiveIntegerField(unique=True)
    razon_social = models.CharField(max_length=100, unique=True)
    nombre_dueno = models.CharField(max_length=100)
    ciudad = models.ForeignKey(Ciudad)#----> problema para filtrar
    direccion = models.CharField(max_length=100, unique=True)
    telefono= models.PositiveIntegerField()
    email = models.CharField(max_length=30, unique=True, blank=True,null=True) #blank=True indica que puede estar el campo vacio
    es_moroso = models.BooleanField(default=False)
    saldo = models.FloatField(default=0)

    def __str__(self):
        return "%s (%s)" % (self.cuit_cuil, self.razon_social)


#************************************************************************#
               #     P E D I D O S  D E  C L I E N T E S    #
#************************************************************************#


class PedidoCliente(models.Model):
    FILTROS = ['fecha_creacion__gte','tipo_pedido','cliente' ] #,'tipo_pedido__' como hacer para filtrar
    TIPOPEDIDO = (
        (1, "Pedido Fijo"),
        (2, "Pedido Ocasional"),
        (3,"Pedido de Cambio")
    )
    fecha_creacion = models.DateField(auto_now_add = True)
    tipo_pedido = models.PositiveSmallIntegerField(choices=TIPOPEDIDO)
    productos = models.ManyToManyField(ProductoTerminado, through="PedidoClienteDetalle")
    cliente = models.ForeignKey(Cliente)
    def esParaHoy(self):
        pass

    def esParaHoy(self):
        print "soy padreeeeee"

    
    def __str__(self):
        return "%s ( %s)" % (self.cliente, self.get_tipo_pedido_display())

class PedidoClienteDetalle(models.Model):
    cantidad_producto = models.PositiveIntegerField()
    producto_terminado = models.ForeignKey(ProductoTerminado)   #como hacer para q a un mismo cliente solo pueda haber un producto el mismo tipo

    pedido_cliente = models.ForeignKey(PedidoCliente)


class PedidoFijo(PedidoCliente):
    fecha_inicio = models.DateField(default=date.today())
    #fecha_inicio = models.DateField(default=timezone.now())
    fecha_cancelacion = models.DateField(blank=True,null=True)
    dias = MultiSelectField(choices=TIPODIAS)

    def esParaHoy(self):
        num_dia = date.today().weekday()
        if self.dias == None:
            return False
        if str(num_dia + 1) in self.dias:
            return True
        else:
            return False

class PedidoCambio(PedidoCliente):
    fecha_entrega = models.DateField()

    def esParaHoy(self):
        d = date.today()
        if d == self.fecha_entrega:
            return True
        else:
            return False


class PedidoOcacional(PedidoCliente):
    fecha_entrega = models.DateField()

    def esParaHoy(self):
        d = date.today()
        if d == self.fecha_entrega:
            return True
        else:
            return False

#********************************************************#
         #   P E D I D O S   A  P R O V E E D O R   #
#********************************************************#
class PedidoProveedor(models.Model):

    FILTROS = ['fecha_desde','fecha_hasta','proveedor','estado_pedido']
    FILTROS_MAPPER = {
        'fecha_desde': 'fecha_realizacion__gte',
        'fecha_hasta': 'fecha_realizacion__lte'
    }
    ESTADO = (
        (1, "Pendiente"),
        (2, "Recibido"),
        (3, "Cancelado"),
    )
    fecha_realizacion = models.DateField()
    fecha_de_entrega = models.DateField(blank=True,null=True)
    proveedor = models.ForeignKey(Proveedor)
    estado_pedido = models.PositiveSmallIntegerField(choices=ESTADO,default="1")
    insumos = models.ManyToManyField(Insumo, through="DetallePedidoProveedor")
    descripcion = models.TextField(null=True)
    fecha_cancelacion =  models.DateField(blank=True,null=True)

    #relacion con proveedor
    #relacion con
    #https://jqueryui.com/datepicker/
    #fecha_realizacion__gte

    #detalle de pedido


    #detalle de pedido
    #auto_now_add = True


class DetallePedidoProveedor(models.Model):
    cantidad_insumo = models.PositiveIntegerField()
    insumo = models.ForeignKey(Insumo)
    pedido_proveedor = models.ForeignKey(PedidoProveedor)


#********************************************************#
         #   L O T E S   P R O D U C C I O N #
#********************************************************#
class Lote(models.Model):
    FILTROS = ['producto_terminado']

    nro_lote = models.AutoField(primary_key=True) # Field name made lowercase.
    fecha_produccion = models.DateField()
    fecha_vencimiento=models.DateField()
    cantidad_producida = models.PositiveIntegerField()
    stock_disponible= models.PositiveIntegerField()
    stock_reservado= models.PositiveIntegerField(default=0)
    producto_terminado=models.ForeignKey(ProductoTerminado)



    def reservar_stock(self,cantidad):
        """ Resibe la cantidad de stock que se necesita reservar.
            Si stock disponible alcanza a cubrirla, se aumenta el stock reservado en esa cantidad
            Si stock disponible no alcanza a cubrirla, se aumenta el stock reservado con stock disponible
            Este metodo retorna la cantidad que LOGRO reservar
        """
        puede_reservar = self.stock_disponible - self.stock_reservado
        if cantidad <= puede_reservar:
            reservar = cantidad
        else:
            reservar = puede_reservar
        self.stock_reservado += reservar
        self.save()
        return reservar

        #    E N   C O N S T R U C C I O N  necesitamos rendicion.
    def reservar_stock_2(self,cantidad):
        print "en reservar stock 2, el stock disponible es:", self.stock_disponible
        #tengo q recorrer loteEntregaDetalle y DetalleProdExtra
        cantidad_total_reservada=0
        for d in self.loteentregadetalle_set.all():
            if d.cantidad_entregada == None:
                cantidad_total_reservada += d.cantidad
        # falta recorrer los detalles de productos EXTRAS!
        return cantidad_total_reservada

    def decrementar_stock_reservado(self,cant):
        self.stock_reservado -= cant
        self.save()

    def decrementar_stock_disponible(self,cant):
        self.stock_disponible -= cant
        self.save()




class Factura(models.Model):
    fecha = models.DateField(auto_now_add = True)
    numero = models.PositiveIntegerField()  #es el numero de la factura en papel
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0,00)])


#********************************************************#
         #    HOJA DE RUTA   #
#********************************************************#


class HojaDeRuta(models.Model):
    fecha_creacion = models.DateField(auto_now_add = True)
    chofer = models.ForeignKey(Chofer)
    rendida = models.BooleanField(default=False)
    #lote_extra = models.ManyToManyField(Lote, through="LotesExtraDetalle",null=True)

    def generar_rendicion(self):
        # aca tengo que generar TODOS los detalles de las entregas.
        # tengo q lanzar una exception si ya las entregas existen. NO se pude rendir una hoja mas de una vez.
        tiene_prod = False
        for entrega in self.entrega_set.all():
            if len(entrega.entregadetalle_set.all())>0:
                raise "ya tengo rendicion"
            for prod_llevado in self.productosllevados_set.all():
                for detalle_pedido in entrega.pedido.pedidoclientedetalle_set.all():
                    if detalle_pedido.producto_terminado == prod_llevado.producto_terminado:
                        tiene_prod=True
                        break
                if not tiene_prod:
                    entrega.generar_detalle(None, prod_llevado.producto_terminado)
                else:
                    entrega.generar_detalle(detalle_pedido, None)
                tiene_prod=False


    def balance(self):
        productos ={}
        sobrantes ={}
        for prod_llevado in self.productosllevados_set.all():
            productos[prod_llevado.producto_terminado.id] = prod_llevado.cantidad_enviada

            for det in prod_llevado.productosllevadosdetalle_set.all():
                try:
                    sobrantes[prod_llevado.producto_terminado.id] += det.cantidad_sobrante
                except:
                    sobrantes[prod_llevado.producto_terminado.id] =0
                    sobrantes[prod_llevado.producto_terminado.id] += det.cantidad_sobrante

        print "BALANCE productos llevados: ", productos
        productos_llevados = productos
        for entrega in self.entrega_set.all():
            for detalle_entrega in entrega.entregadetalle_set.all():
                if detalle_entrega.producto_terminado:
                    productos[detalle_entrega.producto_terminado.id] -= detalle_entrega.cantidad_entregada
                else:
                    productos[detalle_entrega.pedido_cliente_detalle.producto_terminado.id] -= detalle_entrega.cantidad_entregada
        print "Esto tenria que haber sobrado !!:",productos
        # y ahora como sé que fue lo que realmente sobro???? CANTIDAD_SOBRANTE en detalle producto_llevado
        print "LO QUE REALMENTE SOBRo: ",sobrantes
        totales = {"sobrantes_reales":productos,"productos_llevados":productos_llevados,"sobrantes_ingresados":sobrantes}
        return totales

class ProductosLlevados(models.Model):
    cantidad_pedida = models.PositiveIntegerField(default=0)
    cantidad_enviada = models.PositiveIntegerField(default=0)
    producto_terminado = models.ForeignKey(ProductoTerminado)
    hoja_de_ruta = models.ForeignKey(HojaDeRuta)


    def generar_detalles(self):
        """ En base al producto y a la cantidad pedida, sale a buscarlo en los lotes
            por cada lote que se necesite para satisfacer la cantidad pedida se crea un detalle asociado a el
            junto con la cantidad que pudo sacarle a ese lote.
        """
        cantidad_buscada = self.cantidad_pedida
        for lote in Lote.objects.filter(producto_terminado = self.producto_terminado,
                                        fecha_vencimiento__gte=datetime.date.today(),
                                        stock_disponible__gte = 0):
            cantidad_reservada = lote.reservar_stock(cantidad_buscada)
            if cantidad_reservada == 0:
                continue
            cantidad_buscada -=cantidad_reservada
            ProductosLlevadosDetalle.objects.create(cantidad = cantidad_reservada,
                                                    lote=lote,
                                                    producto_llevado = self)
            if cantidad_buscada == 0:
                break
        if cantidad_buscada > 0:
            print "Faltaron ",cantidad_buscada, "unidades para el producto: ",self.producto_terminado
        self.cantidad_enviada = self.cantidad_pedida - cantidad_buscada
        self.save()
        print "en generar detalles: cantida enviada: ",self.cantidad_enviada




class ProductosLlevadosDetalle(models.Model):
    cantidad = models.PositiveIntegerField()
    lote = models.ForeignKey(Lote)
    producto_llevado= models.ForeignKey(ProductosLlevados)
    cantidad_sobrante = models.PositiveIntegerField(null=True)

class Entrega(models.Model):
    hoja_de_ruta = models.ForeignKey(HojaDeRuta)
    pedido = models.ForeignKey(PedidoCliente)
    fecha = models.DateField(auto_now_add = True)
    factura = models.ForeignKey(Factura,null=True)
    #cliente = getCliente()

    def generar_detalles(self):
        if self.entregadetalle_set.all().exists():
            raise "Ya tengo detalles para el pedido %s" % self.pedido

        for detalle_pedido in self.pedido.pedidoclientedetalle_set.all():
            # creo detalle de entrega asociada al detalle del pedido
            entrega_detalle = EntregaDetalle.objects.create(entrega=self,
                                                                   precio=(detalle_pedido.producto_terminado.precio *detalle_pedido.cantidad_producto),
                                                                   cantidad_entregada = None,
                                                                   pedido_cliente_detalle=detalle_pedido)
    def getCliente(self):
        print ("soy clienteeeee",self.pedido.cliente)
        return self.pedido.cliente


    def monto_ya_abonado(self):
        recibos = self.recibo_set.all()
        total = 0
        for recibo in recibos:
            total += recibo.monto_pagado
        return total

    def monto_total(self):
        detalles = self.entregadetalle_set.all()
        total = 0
        for detalle in detalles:
            total += detalle.precio
        return total

    def monto_restante(self):   # sirve solo para entregas no facturadas, si esta facturada nunca se deberia llamar, no tendria sentido
        return self.monto_total()-self.monto_ya_abonado()

    def cobrar_con_factura(self,monto,numero_factura=None):
        factura=Factura.objects.filter(numero=numero_factura)   #devuelve una lista!!!!
        if (len(factura) == 0):
            factura=Factura.objects.create(numero=numero_factura,fecha=date.today(),monto_pagado=monto)
            self.factura=factura
        else:
            self.factura=factura[0]
        self.save()

    def cobrar_con_recibo(self,monto,numero_recibo=None):
        recibo = Recibo.objects.create(entrega=self,fecha=date.today(),numero=numero_recibo,monto_pagado=monto)

    def generar_detalle(self,detalle_pedido=None, prod_terminado=None):
        print "EN GENERAR DETALLE:"

        if detalle_pedido:
            precio = detalle_pedido.producto_terminado.precio
        else:
            precio = prod_terminado.precio

        detalle = EntregaDetalle.objects.create(entrega=self,
                                    pedido_cliente_detalle = detalle_pedido,
                                      producto_terminado = prod_terminado,
                                        cantidad_entregada=0,
                                    precio = precio)

        print "PRECIO PAPAAAA:", detalle.precio
        detalle.save()
        print "guarde detalle nuevo"

class EntregaDetalle(models.Model):
    entrega = models.ForeignKey(Entrega)
    cantidad_enviada = models.PositiveIntegerField(null=True) #no va
    cantidad_entregada = models.PositiveIntegerField(null=True)
    precio= models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0,00)])
    pedido_cliente_detalle = models.ForeignKey(PedidoClienteDetalle,null=True)
    producto_terminado = models.ForeignKey(ProductoTerminado,null=True)

class LoteEntregaDetalle(models.Model):
    entrega_detalle = models.ForeignKey(EntregaDetalle)
    lote = models.ForeignKey(Lote)
    cantidad = models.PositiveIntegerField()


entrega = models.ForeignKey(Entrega)





class Recibo(models.Model):
    entrega = models.ForeignKey(Entrega)
    fecha = models.DateField(auto_now_add = True)
    numero = models.PositiveIntegerField()  #es el numero del recibo en papel
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0,00)])






'''
#********************************************************#
         #    ENTREGA PEDIDO   #
#********************************************************#


class EntregaPedido(models.Model):
    fecha_entrega = models.DateField(auto_now_add = True)
    pedido = models.ForeignKey(PedidoCliente)
    lotes = models.ManyToManyField(Lote, through="EntregaPedidoDetalle")
    hoja_de_ruta = models.ForeignKey(HojaDeRuta)
    #falta recibo, factura
    def __str__(self):
        return "%s ( %s)" % (self.cliente, self.get_tipo_pedido_display())

class EntregaPedidoDetalle(models.Model):
    cantidad_entregada = models.FloatField()    #poner integer
    cantidad_enviada = models.FloatField()
    precio = models.FloatField()
    detalle_pedido = models.ForeignKey(PedidoClienteDetalle)    #porque
    lote = models.ManyToManyField(Lote)
    entrega_pedido = models.ForeignKey(EntregaPedido)










class PedidoCliente(models.Model):
    FILTROS = ['fecha_creacion__gte','tipo_pedido','cliente' ] #,'tipo_pedido__' como hacer para filtrar
    fecha_creacion = models.DateField(auto_now_add = True)
    productos = models.ManyToManyField(ProductoTerminado, through="PedidoClienteDetalle")
    cliente = models.ForeignKey(Cliente)
    TIPOS = {}


    def __str__(self):
        return "%s " % (self.cliente)

class PedidoClienteDetalle(models.Model):
    cantidad_producto = models.FloatField()
    producto_terminado = models.ForeignKey(ProductoTerminado)   #como hacer para q a un mismo cliente solo pueda haber un producto el mismo tipo
    pedido_cliente = models.ForeignKey(PedidoCliente)

class PedidoFijo(PedidoCliente):
    fecha_inicio = models.DateField(default=date.today())
    fecha_cancelacion = models.DateField(blank=True,null=True)
    dias = MultiSelectField(choices=TIPODIAS)
    NOMBRE = "Pedido Fijo"
    TIPO = 1

    def esParaHoy(self):
        d = date.today()
        if d.day in self.dias:
            return True
        else:
            return False
PedidoCliente.TIPOS[PedidoFijo.TIPO] = PedidoFijo

class PedidoCambio(PedidoCliente):
    fecha_entrega = models.DateField()
    TIPO = 3
    def esParaHoy(self):
        d = date.today()
        if d in self.fecha_entrega:
            return True
        else:
            return False
PedidoCliente.TIPOS[PedidoCambio.TIPO] = PedidoCambio

class PedidoOcacional(PedidoCliente):
    fecha_entrega = models.DateField()
    TIPO = 2
    def esParaHoy(self):
        d = date.today()
        if d in self.fecha_entrega:
            return True
        else:
            return False
PedidoCliente.TIPOS[PedidoOcacional.TIPO] = PedidoOcacional

'''

