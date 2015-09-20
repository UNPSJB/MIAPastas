# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

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





class Receta(models.Model):
    UNIDADES = (
        (1, "Kg"),
        (3, "Unidad"),
        (5, "Bolson"),
        (5, "Bolsines"),
    )
    FILTROS = ['nombre__icontains']



    fechaCreacion= models.DateField()
   # fechaModificacion= models.DateField() HAY Q SACARLO
    nombre = models.CharField(max_length=100, unique=True,help_text="El nombre de la receta")
    unidad_medida =  models.PositiveSmallIntegerField(choices=UNIDADES)
    Descripcion = models.TextField()
    cantProdTerminado= models.PositiveIntegerField()
    insumos = models.ManyToManyField(Insumo)

    def __str__(self):
        return "%s (%d %s)" % (self.nombre, self.cantProdTerminado, self.get_unidad_medida_display())



class Proveedor(models.Model):

    FILTROS = ['cuit__icontains','razonSocial__icontains','ciudad__icontains']
    razonSocial = models.CharField(max_length=100, unique=True)
    nombreDueno = models.CharField(max_length=100, unique=True)
    direccion = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=30, unique=True, blank=True) #blank=True indica que puede estar el campo vacio
    localidad = models.CharField(max_length=50, unique=True)
    numeroCuenta= models.PositiveIntegerField()
    provincia = models.CharField(max_length=50, unique=True)
    telefono= models.PositiveIntegerField()
    cuit= models.PositiveIntegerField()
    insumos= models.ManyToManyField(Insumo,related_name='proveedores')#con related_name='proveedores' los objetos insumos puede llamar a sus proveedores por "proveedores"
#RELACION UNO A MUCHOS CON pedidosProveedor

    def __str__(self):
        return "%s (%d %s)" % (self.razonSocial, self.telefono, self.cuit)


