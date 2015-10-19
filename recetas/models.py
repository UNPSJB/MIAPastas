# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import MinValueValidator

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

#********************************************************#
               #     I N S U M O     #
#********************************************************#

class Insumo(models.Model):

    FILTROS = ['nombre__icontains', 'stock__lte']
    UNIDADES = (
        (1, "Kg"),
        (2, "Litro"),
        (3, "Unidad"),
        (4, "Docena"),
        (5, "Caja"),
    )
    nombre = models.CharField(max_length=100, unique=True, help_text="El nombre del insumo")
    descripcion = models.TextField("Descripcón")
    stock = models.PositiveIntegerField(blank= True, null=True, default=0)
    unidad_medida = models.PositiveSmallIntegerField(choices=UNIDADES)

    def __str__(self):
        return "%s (%s)" % (self.nombre, self.get_unidad_medida_display())


#********************************************************#
            #     P R O D U C T O S     #
#********************************************************#

class ProductoTerminado(models.Model):
    UNIDADES = {
        (1, "Kg"),
        (2, "Unidad"),
        (3, "Bolson"),
        (4, "Bolsines"),
    }
    FILTROS = ['nombre__icontains','stock__lte']
    nombre = models.CharField(max_length=100,unique=True,help_text="El nombre del producto")
    stock = models.PositiveIntegerField()
    unidad_medida = models.PositiveSmallIntegerField(choices=UNIDADES)
    precio= models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0,00)])
    #http://blog.p3infotech.in/2013/enforcing-minimum-and-maximum-values-in-django-model-fields/


    def __str__(self):
        return "%s"% self.nombre



#********************************************************#
               #     R E C E T A S    #
#********************************************************#


class Receta(models.Model):
    UNIDADES = (
        (1, "Kg"),
        (2, "Unidad"),
        (3, "Bolson"),
        (4, "Bolsines"),
    )
    FILTROS = ['nombre__icontains','producto_terminado']
    fecha_creacion = models.DateField(auto_now_add = True)
    nombre = models.CharField(max_length=100, unique=True,help_text="El nombre de la receta")
    unidad_medida =  models.PositiveSmallIntegerField(choices=UNIDADES)
    descripcion = models.TextField()
    cant_prod_terminado= models.PositiveIntegerField()
    producto_terminado = models.ForeignKey(ProductoTerminado)
    insumos = models.ManyToManyField(Insumo, through="RecetaDetalle")


    def __str__(self):
        return "%s (%d %s)" % (self.nombre, self.cant_prod_terminado, self.get_unidad_medida_display())


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

    FILTROS = ['cuit_cuil__icontains','razon_social__icontains','ciudad','es_moroso_icontains']#'zona_icontains'
    cuit_cuil = models.PositiveIntegerField(unique=True)
    razon_social = models.CharField(max_length=100, unique=True)
    nombre_dueno = models.CharField(max_length=100)
    ciudad = models.ForeignKey(Ciudad)#----> problema para filtrar
    direccion = models.CharField(max_length=100, unique=True)
    telefono= models.PositiveIntegerField()
    email = models.CharField(max_length=30, unique=True, blank=True,null=True) #blank=True indica que puede estar el campo vacio
    es_moroso = models.BooleanField(default=False)


    def __str__(self):
        return "%s (%s)" % (self.cuit_cuil, self.razon_social)




#************************************************************************#
               #     P E D I D O S  D E  C L I E N T E S    #
#************************************************************************#


class PedidoCliente(models.Model):
    FILTROS = ['fecha_creacion__icontains','fecha_desde__icontains','fecha_hasta__icontains' ] #,'tipo_pedido__' como hacer para filtrar
    TIPOPEDIDO = (
        (1, "Pedido Fijo"),
        (2, "Pedido Ocasional"),
        (3,"Pedido de Cambio")
    )
    fecha_creacion = models.DateField(auto_now_add = True)
    tipo_pedido = models.PositiveSmallIntegerField(choices=TIPOPEDIDO)
    productos = models.ManyToManyField(ProductoTerminado, through="PedidoClienteDetalle")
    cliente = models.ForeignKey(Cliente)

    def __str__(self):
        return "%s ( %s)" % (self.cliente, self.get_tipo_pedido_display())

class PedidoClienteDetalle(models.Model):
    cantidad_producto = models.PositiveIntegerField()
    producto_terminado = models.ForeignKey(ProductoTerminado)   #como hacer para q a un mismo cliente solo pueda haber un producto el mismo tipo
    pedido_cliente = models.ForeignKey(PedidoCliente)


class DiasSemana(models.Model):
    dia = models.CharField(unique=True,max_length=100)


class PedidoFijo(PedidoCliente):
    fecha_inicio = models.DateField()
    fecha_cancelacion = models.DateField(blank=True)
    dias = models.ForeignKey(DiasSemana,blank=True)  #quitar blank

class PedidoCambio(PedidoCliente):
    fecha_entrega = models.DateField()

class PedidoOcacional(PedidoCliente):
    fecha_entrega = models.DateField()



#********************************************************#
         #   P E D I D O S   A  P R O V E E D O R   #
#********************************************************#
class PedidoProveedor(models.Model):

    FILTROS = ['fecha_realizacion__icontains','fecha_probable_entrega__icontains','proveedor']
    fecha_realizacion = models.DateField()
    fecha_probable_entrega = models.DateField()
    proveedor = models.ForeignKey(Proveedor)
    #relacion con proveedor
    #relacion con
    #https://jqueryui.com/datepicker/

