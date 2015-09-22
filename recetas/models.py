# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

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
    stock = models.PositiveIntegerField()
    unidad_medida = models.PositiveSmallIntegerField(choices=UNIDADES)

    def __str__(self):
        return "%s (%d %s)" % (self.nombre, self.stock, self.get_unidad_medida_display())


#********************************************************#
            #     P R O D U C T O S     #
#********************************************************#

class ProductoTerminado(models.Model):
    UNIDADES = {
        (1, "Kg"),
        (3, "Unidad"),
        (5, "Bolson"),
        (5, "Bolsines"),
    }
    FILTROS = ['nombre__icontains','stock__lte']
    nombre = models.CharField(max_length=100,unique=True,help_text="El nombre del insumo")
    stock = models.IntegerField()
    unidad_medida = models.PositiveSmallIntegerField(choices=UNIDADES)
    precio= models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return "%s"% self.nombre



#********************************************************#
               #     R E C E T A S    #
#********************************************************#


class Receta(models.Model):
    UNIDADES = (
        (1, "Kg"),
        (3, "Unidad"),
        (5, "Bolson"),
        (5, "Bolsines"),
    )
    FILTROS = ['nombre__icontains']



    fechaCreacion= models.DateField()
    nombre = models.CharField(max_length=100, unique=True,help_text="El nombre de la receta")
    unidad_medida =  models.PositiveSmallIntegerField(choices=UNIDADES)
    descripcion = models.TextField()
    cantProdTerminado= models.PositiveIntegerField()
    insumos = models.ManyToManyField(Insumo,blank = True)
    productoTerminado = models.ForeignKey(ProductoTerminado)

    def __str__(self):
        return "%s (%d %s)" % (self.nombre, self.cantProdTerminado, self.get_unidad_medida_display())


#********************************************************#
               #     P R O V E E D O R E S    #
#********************************************************#

class Proveedor(models.Model):

    FILTROS = ['cuit__icontains','razonSocial__icontains','ciudad__icontains']
    razonSocial = models.CharField(max_length=100, unique=True)
    nombreDueno = models.CharField(max_length=100, unique=True)
    direccion = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=30, unique=True, blank=True,null=True) #blank=True indica que puede estar el campo vacio
    localidad = models.CharField(max_length=50, unique=True)
    numeroCuenta= models.PositiveIntegerField()
    provincia = models.CharField(max_length=50, unique=True)
    telefono= models.PositiveIntegerField()
    cuit= models.PositiveIntegerField()
    insumos= models.ManyToManyField(Insumo,related_name='proveedores')#con related_name='proveedores' los objetos insumos puede llamar a sus proveedores por "proveedores"
#RELACION UNO A MUCHOS CON pedidosProveedor

    def __str__(self):
        return "%s (%d %s)" % (self.razonSocial, self.telefono, self.cuit)










#********************************************************#
               #     Z O N A S    #
#********************************************************#

class Zona(models.Model):

    FILTROS = ['nombre__icontains']
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return (self.nombre)



#********************************************************#
               #     C I U D A D E S    #
#********************************************************#
class Ciudad(models.Model):

    FILTROS = ['nombre__icontains','codigoPostal__icontains','zona_icontains']
    nombre = models.CharField(max_length=100, unique=True)
    codigoPostal = models.PositiveIntegerField()
    zona = models.ForeignKey(Zona)

    def __str__(self):
        return "%s (%d %s)" % (self.nombre, self.codigoPostal, self.zona)





#********************************************************#
               #     C L I E N T E S    #
#********************************************************#
class Cliente(models.Model):

    FILTROS = ['cuit_cuil__icontains','razonSocial__icontains','ciudad_icontains','esMoroso_icontains']#'zona_icontains'
    TIPOCLIENTE = (
        (1, "Cliente Fijo"),
        (2, "Cliente Ocasional"),
    )
    cuit_cuil = models.PositiveIntegerField()
    razonSocial = models.CharField(max_length=100, unique=True)
    nombreDueno = models.CharField(max_length=100, unique=True)
    tipo_cliente = models.PositiveSmallIntegerField(choices=TIPOCLIENTE)
    ciudad = models.ForeignKey(Ciudad)#----> problema para filtrar
    #zona = ....   ---> la saco de la ciudad
    direccion = models.CharField(max_length=100, unique=True)
    telefono= models.PositiveIntegerField()
    email = models.CharField(max_length=30, unique=True, blank=True,null=True) #blank=True indica que puede estar el campo vacio
    esMoroso = models.BooleanField(default=False)


    def __str__(self):
        return "%s (%d %s)" % (self.cuit_cuil, self.razonSocial, self.get_tipo_cliente_display())