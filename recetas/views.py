from django.shortcuts import render, redirect
from . import models
from . import forms
from django.forms.formsets import formset_factory
from django.shortcuts import get_object_or_404
from django.forms.models import BaseModelFormSet
from django.forms.models import modelformset_factory
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.messages import get_messages
import json as simplejson
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import inlineformset_factory
import re
import datetime
#from datetime import date, datetime
#import time

    # Create your views here.

def get_order(get):
    if "o" in get:
        return get["o"]


fechareg = re.compile("^(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})$") #esta es una expresion regular par las fechas
##permite fechas del siguiente tipo: dd/mm/aa or d/m/aa or dd/mm/aaaa etc....
#permite fechas del siguiente tipo: dd-mm-aa or d-m-aa or dd-mm-aaaa etc....

def get_filtros(get, modelo):
    mfilter = {}
    for filtro in modelo.FILTROS:
        attr = filtro.split("__")[0]
        if attr in get and get[attr]:
            texto = get[attr]
            match=fechareg.match(texto) #aca estoy preguntando si el texto que me viene del GET tiene forma de fecha, si es asi, convierte texto en un tipo "date"
            if match is not None:
                print(match)
                print(texto)
                print(match.groups()[2])
                print(match.groups()[1])
                print(match.groups()[0])
                print(filtro)
                ano = int(match.groups()[2])
                mes = int(match.groups()[0])
                dia = int(match.groups()[1])
                print(ano,mes,dia)
                fecha = datetime.date(ano,mes,dia)
                mfilter[filtro] = datetime.date(ano,mes,dia)
            else:
                mfilter[filtro] = texto
            mfilter[attr] = texto
    return mfilter

#********************************************************#
               #     C H O F E R E S    #
#********************************************************#
def choferes(request,chofer_id=None):
    if chofer_id is not None:
        # consulta
        chofer = models.Chofer.objects.get(pk=chofer_id)
        return render(request, "choferesConsulta.html",{"chofer": chofer})
    elif request.method == 'GET':
        # filtros
        filters = get_filtros(request.GET, models.Chofer)
        mfilters = dict(filter(lambda v: v[0] in models.Chofer.FILTROS, filters.items()))
        choferes = models.Chofer.objects.filter(**mfilters)
        return render(request, "recetas/choferes.html",
                  {"choferes": choferes,
                   "filtros": filters})


def choferesAlta(request):
    if request.method == "POST":
        chofer_form = forms.ChoferForm(request.POST)
        if chofer_form.is_valid():
            chofer_form.save()
            return redirect('choferes')
    else:
        chofer_form = forms.ChoferForm()

    return render(request, "choferesAlta.html", {"chofer_form":chofer_form})



def choferesModificar(request,chofer_id =None):
    chofer_instancia = get_object_or_404(models.Chofer, pk=chofer_id)
    if request.method=="POST":
        chofer_form = forms.ChoferForm(request.POST,instance= chofer_instancia)
        if chofer_form.is_valid():
            chofer_form.save()
            return redirect('choferes')
    else:
        chofer_form = forms.ChoferForm(instance= chofer_instancia)
    return render(request,"choferesModificar.html",{"chofer_form":chofer_form,"id":chofer_id})


@csrf_exempt
def choferesBaja(request,chofer_id=None):
    chofer = models.Chofer.objects.get(pk=chofer_id)
    # HAY Q HACER VALIDACIONES.
    chofer.delete()
    return redirect('choferes')


#********************************************************#
               #     I N S U M O S    #
#********************************************************#

def insumos(request,insumo_id=None):
    if insumo_id is not None:
        # consulta
        insumo_instancia = models.Insumo.objects.get(pk=insumo_id)
        insumo_form = forms.InsumoForm(instance= insumo_instancia)
        return render(request, "insumosConsulta.html",{"insumo":insumo_instancia})
    elif request.method == 'GET':
        # filtros
        filters = get_filtros(request.GET, models.Insumo)
        mfilters = dict(filter(lambda v: v[0] in models.Insumo.FILTROS, filters.items()))
        insumos = models.Insumo.objects.filter(**mfilters)
        return render(request, "recetas/insumos.html",
                  {"insumos": insumos,
                   "filtros": filters})


def insumosAlta(request):
    if request.method == "POST":
        insumo_form = forms.InsumoForm(request.POST)
        if insumo_form.is_valid():
            insumo_form.save()
            return redirect('insumos')
    else:
        insumo_form = forms.InsumoForm()
    return render(request, "insumosAlta.html", {"insumo_form":insumo_form})


def insumosModificar(request,insumo_id =None): #zona id nunca va a ser none D:
    insumo_instancia = get_object_or_404(models.Insumo, pk=insumo_id)
    if request.method=="POST":
        insumo_form = forms.InsumoForm(request.POST,instance= insumo_instancia)
        if insumo_form.is_valid():
            insumo_form.save()
        return redirect('insumos')
    else:
        insumo_form = forms.InsumoForm(instance= insumo_instancia)
        return render(request,"insumosModificar.html",{"insumo_form":insumo_form,"id":insumo_id})


def insumosBaja(request,insumo_id):
    insumo = models.Insumo.objects.get(pk=insumo_id)
    # HAY Q HACER VALIDACIONES.
    if insumo.receta_set.exists():
        messages.success(request, 'El Insumo: ' + insumo.nombre + ', se elimino correctamente junto a las recetas: %s .' % ", ".join(
            [ "%s" % r for r in insumo.receta_set.all()]
        ))
        insumo.delete()
    else:
        messages.success(request, 'El Insumo: ' + insumo.nombre + ', ha sido eliminado correctamente.')
        insumo.delete()

    return redirect('insumos')






#********************************************************#
               #     R E C E T A S    #
#********************************************************#

def recetas(request,receta_id=None):
    if receta_id is not None:
        # consulta
        receta = models.Receta.objects.get(pk=receta_id)
        return render(request, "recetasConsulta.html",{"receta": receta})
    elif request.method == 'GET':
        # filtros
        filters = get_filtros(request.GET, models.Receta)
        mfilters = dict(filter(lambda v: v[0] in models.Receta.FILTROS, filters.items()))
        recetas = models.Receta.objects.filter(**mfilters)

        for receta in recetas:
            insumos = receta.insumos.all()
            print "soy recetaaaaaaaaaa ",insumos
        # filtrar recetas por productos
        productos_terminados= models.ProductoTerminado.objects.all()
        return render(request, "recetas/recetas.html",
                      {"recetas": recetas,
                       "filtros": filters,
                       "productos_terminados":productos_terminados})



def recetasModificar(request,receta_id):
    receta_instancia = get_object_or_404(models.Receta, pk=receta_id)
    detalles_instancias = models.RecetaDetalle.objects.filter(receta = receta_instancia)
    insumos = models.Insumo.objects.all() #para detalles

    detalles_inlinefactory = inlineformset_factory(models.Receta,models.RecetaDetalle,fields=('cantidad_insumo','insumo','receta'))

    if request.method=="POST":
        receta_form = forms.RecetaForm(request.POST,instance= receta_instancia)
        if receta_form.is_valid():
            receta_instancia = receta_form.save(commit=False)
            #DETALLES
            detalles_formset = detalles_inlinefactory(request.POST,request.FILES,prefix='recetadetalle_set',instance=receta_instancia)
            if detalles_formset.is_valid():
                detalles_formset.save()
                messages.success(request, 'La Receta: ' + receta_instancia.nombre + ', ha sido modificada correctamente.')
                receta_instancia.save()
            return redirect('recetas')
    else:
        receta_form = forms.RecetaForm(instance= receta_instancia)

        #si el form no es valido, le mando todo al html para que muestre los errores#
    pref = "recetadetalle_set"
    return render(request,"recetasModificar.html",{"receta_form":receta_form,"id":receta_id,
                                                   "detalles_receta":detalles_instancias,
                                                   "insumos":insumos,
                                                   "detalles_form_factory":detalles_inlinefactory(initial=list(detalles_instancias.values()), prefix='recetadetalle_set'),
                                                   "receta_id":receta_id,
                                                   "pref":pref
                                                   })


def recetasAlta(request):
    detalles_form_class = formset_factory(forms.RecetaDetalleForm)
    detalles_form = None
    receta_form = None
    insumos = models.Insumo.objects.all()
    if request.method == "POST":
        receta_form = forms.RecetaForm(request.POST) #crea formulario de receta cno los datos del post
        if receta_form.is_valid():
            receta_instancia = receta_form.save(commit = False) #commit false
            detalles_form = detalles_form_class(request.POST, request.FILES)
            if detalles_form.is_valid():
                #detalles = detalles_form.save(commit=False)
                receta_instancia.save()
                for detalle in detalles_form:
                    detalle_instancia = detalle.save(commit=False)
                    detalle_instancia.receta = receta_instancia
                    detalle_instancia.save()
                messages.success(request, 'La Receta: ' + receta_instancia.nombre + ', ha sido registrada correctamente.')

                return redirect('recetas')
        # se lo paso todo a la pagina para que muestre cuales fueron los errores.
    return render(request, "recetasAlta.html", {
            "insumos":insumos,
            "receta_form": receta_form or forms.RecetaForm(),
            "detalles_form_factory": detalles_form or detalles_form_class()})


def recetasBaja(request,receta_id):
    receta = models.Receta.objects.get(pk=receta_id)
    messages.success(request, 'La Receta: ' + receta.nombre + ', ha sido eliminada correctamente.')
    receta.delete()
    return redirect('recetas')

#********************************************************#
               #     P R O V E E D O R E S   #
#********************************************************#


def proveedores(request,proveedor_id=None):
    if proveedor_id is not None:
        p = models.Proveedor.objects.get(pk=proveedor_id)
        i = p.insumos.all()
        return render(request, "proveedoresConsulta.html",{"proveedor":p,"insumos":i})
    filters = get_filtros(request.GET, models.Proveedor)
    mfilters = dict(filter(lambda v: v[0] in models.Proveedor.FILTROS, filters.items()))
    proveedores = models.Proveedor.objects.filter(**mfilters)
    if request.method == "POST":
        proveedores_form = forms.ProveedorForm(request.POST)
        if proveedores_form.is_valid():
            proveedores_form.save()
            return redirect('proveedores')
    else:
        proveedores_form = forms.ProveedorForm()
    return render(request, "recetas/proveedores.html",{"proveedores": proveedores,"proveedores_form": proveedores_form,"filtros":filters})


def proveedoresAlta(request):
    proveedores_form = forms.ProveedorForm()
    insumos = models.Insumo.objects.all()
    if request.method == "POST":
        proveedores_form = forms.ProveedorForm(request.POST)
        if proveedores_form.is_valid():
            proveedor_instancia=proveedores_form.save()
            return redirect('proveedores')
        return render(request, "proveedoresAlta.html",{"proveedores_form": proveedores_form or forms.ProveedorForm(),"insumos":insumos})
    return render(request, "proveedoresAlta.html",{"proveedores_form": proveedores_form or forms.ProveedorForm(),"insumos":insumos})

@csrf_exempt
def proveedoresBaja(request,proveedor_id =None):
    print "estoy en bajaaa"
    p = models.Proveedor.objects.get(pk=proveedor_id)
    p.delete()
    return redirect('proveedores')
    proveedores = models.Proveedor.objects.all  ()
    proveedores_form = forms.ProveedorForm()
    filters = get_filtros(request.GET, models.Proveedor)
    mfilters = dict(filter(lambda v: v[0] in models.Proveedor.FILTROS, filters.items()))
    proveedores = models.Proveedor.objects.filter(**mfilters)
    return redirect('proveedores')


def proveedoresModificar(request,proveedor_id =None):
    proveedor_instancia = get_object_or_404(models.Proveedor, pk=proveedor_id)
    if request.method=="POST":
        proveedor_form = forms.ProveedorForm(request.POST,instance= proveedor_instancia)
        if proveedor_form.is_valid():
            proveedor_form.save()
            return redirect('proveedores')
        return render(request,"proveedoresModificar.html",{"proveedor_form":proveedor_form,"id":proveedor_id})
    else:
        proveedor_form = forms.ProveedorForm(instance= proveedor_instancia)
        return render(request,"proveedoresModificar.html",{"proveedor_form":proveedor_form,"id":proveedor_id})


#********************************************************#
               #     P R O D U C T O S   #
#********************************************************#



def productosTerminados(request,producto_id=None):
    if producto_id is not None:
        # consulta
        producto = models.ProductoTerminado.objects.get(pk=producto_id)

        return render(request, "productosTerminadosConsulta.html",{"producto": producto})
    elif request.method == 'GET':
        # filtros
        filters = get_filtros(request.GET, models.ProductoTerminado)
        mfilters = dict(filter(lambda v: v[0] in models.ProductoTerminado.FILTROS, filters.items()))
        productos = models.ProductoTerminado.objects.filter(**mfilters)
        return render(request, "recetas/productosTerminados.html",
                  {"productos": productos,
                   "filtros": filters})


def productosTerminadosAlta(request):
    if request.method == "POST":
        producto_form = forms.ProductoTerminadoForm(request.POST)
        if producto_form.is_valid():
            producto_form.save()
            return redirect('productosTerminados')
    else:
        producto_form = forms.ProductoTerminadoForm()
    return render(request, "productosTerminadosAlta.html", {"producto_form": producto_form})

"""
def productosTerminadosAlta(request):
    if request.method == "POST":
        producto_form = forms.ProductoTerminadoForm(request.POST)
        if producto_form.is_valid():
            nombre = producto_form.cleaned_data['nombre']
            datos = models.ProductoTerminado.objects.filter(nombre__icontains=nombre)
            if datos == None: #significa que no existe un producto con ese nombre. Ejemplo receta1 != Receta1 != ReCeTa1
                producto_form.save()
                messages.success(request, 'El Producto: ' + nombre + ', ha sido dado de alta correctamente.')
                return redirect('productosTerminados')
            else:
                messages.error(request, 'El Producto: ' + nombre + ', ya existe.')
                return HttpResponseRedirect('')
                #return render(request,'productosTerminadosAlta.html',{"producto_form": producto_form})

    else:
        producto_form = forms.ProductoTerminadoForm()
    return render(request, "productosTerminadosAlta.html", {"producto_form": producto_form})
"""


def productosTerminadosModificar(request,producto_id = None):
    producto_instancia = get_object_or_404(models.ProductoTerminado, pk = producto_id)
    print(producto_instancia.nombre)
    print(producto_instancia.nombre)
    #producto_instancia.unidad_medida=5
    if request.method=="POST":
        print("estoy en post")
        print(producto_instancia.stock)
        producto_form = forms.ProductoTerminadoForm(request.POST, instance = producto_instancia)
        #nombre = request.POST.get('stock')
        #print(nombre)
        if producto_form.is_valid():
            print("el formulario es valido")
            producto_form.save()
            print(producto_instancia.stock)
            return redirect('productosTerminados')
    else:
        producto_form = forms.ProductoTerminadoForm(instance= producto_instancia)
    return render(request,"productosTerminadosModificar.html",{"producto_form":producto_form,"id":producto_id,"producto":producto_instancia})



@csrf_exempt
def productosTerminadosBaja(request, producto_id=None):
    print "estoy en bajaaa"
    p = models.ProductoTerminado.objects.get(pk=producto_id)
    if p.receta_set.exists():
        messages.success(request, 'El producto: ' + p.nombre + ', se elimino correctamente junto a las recetas: %s .' % ", ".join(
            [ "%s" % r for r in p.receta_set.all()]
        ))
        p.delete()
    else:
        messages.success(request, 'El Producto: ' + p.nombre + ', ha sido eliminado correctamente.')
        p.delete()

    return redirect('productosTerminados')




#********************************************************#
              #     Z O N A S    #
#********************************************************#

def zonas(request,zona_id=None):
    if zona_id is not None:
        # consulta
        zona = models.Zona.objects.get(pk=zona_id)
        ciudades = zona.ciudades.all()
        return render(request, "zonasConsulta.html",{"zona": zona,"ciudades":ciudades})
    elif request.method == 'GET':
        # filtros
        filters = get_filtros(request.GET, models.Zona)
        mfilters = dict(filter(lambda v: v[0] in models.Zona.FILTROS, filters.items()))
        zonas = models.Zona.objects.filter(**mfilters)
        return render(request, "recetas/zonas.html",
                  {"zonas": zonas,
                   "filtros": filters})


def zonasAlta(request):
    if request.method == "POST":
        zona_form = forms.ZonaForm(request.POST)
        if zona_form.is_valid():
            zona_form.save()
            return redirect('zonas')
    else:
        zona_form = forms.ZonaForm()
    return render(request, "zonasAlta.html", {"zona_form":zona_form})


def zonasModificar(request,zona_id =None): #zona id nunca va a ser none D:
    zona_instancia = get_object_or_404(models.Zona, pk=zona_id)
    if request.method=="POST":
        zona_form = forms.ZonaForm(request.POST,instance= zona_instancia)
        if zona_form.is_valid():
            zona_form.save()
        return redirect('zonas')
    else:
        zona_form = forms.ZonaForm(instance= zona_instancia)
        return render(request,"zonasModificar.html",{"zona_form":zona_form,"id":zona_id})


@csrf_exempt
def zonasBaja(request,zona_id =None):
    print "estoy en bajaaa"
    p = models.Zona.objects.get(pk=zona_id)
    if p.ciudades.exists():
        messages.error(request, 'La zona: ' + p.nombre + ', no se puede eliminar porque tiene las siguientes ciudades asociadas: %s .' % ", ".join(
            [ "%s" % r for r in p.ciudades.all()]
        ))

    else:
        messages.success(request, 'La zona: ' + p.nombre + ', ha sido eliminado correctamente.')
        p.delete()

    return redirect('zonas')



#********************************************************#
              #     C L I E N T E S    #
#********************************************************#

def clientes(request,cliente_id=None):
    if cliente_id is not None:
        # consulta
        cliente_instancia = models.Cliente.objects.get(pk=cliente_id)
        #cliente_form = forms.ClienteForm(instance= cliente_instancia)

        return render(request, "clientesConsulta.html",{"cliente": cliente_instancia})
    elif request.method == "GET":
        #filtros
        filters = get_filtros(request.GET, models.Cliente)
        mfilters = dict(filter(lambda v: v[0] in models.Cliente.FILTROS, filters.items()))
        clientes = models.Cliente.objects.filter(**mfilters)
        clientes_form = forms.ClienteForm()
        ciudades= models.Ciudad.objects.all()
        return render(request, "recetas/clientes.html",
                  {"clientes": clientes,
                   "filtros": filters,
                   "ciudades":ciudades})




def clientesModificar(request,cliente_id = None):
    cliente_instancia = get_object_or_404(models.Cliente, pk=cliente_id)
    if request.method=="POST":
        cliente_form = forms.ClienteForm(request.POST,instance= cliente_instancia)
        if cliente_form.is_valid():
            cliente_form.save()
        return redirect('clientes')
    else:
        cliente_form = forms.ClienteForm(instance= cliente_instancia)
        return render(request,"clientesModificar.html",{"cliente_form":cliente_form,"id":cliente_id})

def clientesAlta(request):
    if request.method == "POST":
        cliente_form = forms.ClienteForm(request.POST)
        if cliente_form.is_valid():
            cliente_form.save()
            return redirect('clientes')
    else:
        cliente_form = forms.ClienteForm()
    return render(request, "clientesAlta.html", {"cliente_form":cliente_form})



@csrf_exempt
def clientesBaja(request,cliente_id =None):
    print "estoy en bajaaa"
    p = models.Cliente.objects.get(pk=cliente_id)
    p.delete()
    return redirect('clientes')


#********************************************************#
               #     C I U D A D E S   #
#********************************************************#
def ciudades(request,ciudad_id=None):
    if ciudad_id is not None:
        # consulta
        ciudad = models.Ciudad.objects.get(pk=ciudad_id)
        return render(request, "ciudadesConsulta.html",{"ciudad": ciudad})
    elif request.method == 'GET':
        # filtros
        filters = get_filtros(request.GET, models.Ciudad)
        mfilters = dict(filter(lambda v: v[0] in models.Ciudad.FILTROS, filters.items()))
        ciudades = models.Ciudad.objects.filter(**mfilters)
        zonas = models.Zona.objects.all()
        return render(request, "recetas/ciudades.html",{"filtros": filters,"ciudades":ciudades,"zonas":zonas})



def ciudadesAlta(request):
    if request.method == "POST":
        ciudad_form = forms.CiudadForm(request.POST)
        if ciudad_form.is_valid():
            ciudad_form.save()
            return redirect('ciudades')
    else:
        ciudad_form = forms.CiudadForm()
    return render(request, "ciudadesAlta.html", {"ciudad_form":ciudad_form})


def ciudadesModificar(request,ciudad_id =None): #zona id nunca va a ser none D:
    ciudad_instancia = get_object_or_404(models.Ciudad, pk=ciudad_id)
    if request.method=="POST":
        ciudad_form = forms.CiudadForm(request.POST,instance= ciudad_instancia)
        if ciudad_form.is_valid():
            ciudad_form.save()
        return redirect('ciudades')
    else:
        ciudad_form = forms.CiudadForm(instance= ciudad_instancia)
        return render(request,"ciudadesModificar.html",{"ciudad_form":ciudad_form,"id":ciudad_id})


@csrf_exempt
def ciudadesBaja(request,ciudad_id =None):
    print "estoy en bajaaa"
    p = models.Ciudad.objects.get(pk=ciudad_id)
    p.delete()
    return redirect('ciudades')



#********************************************************#
               #     PEDIDOS CLIENTES   #
#********************************************************#


def pedidosClientes(request,pedido_id=None):
    if pedido_id is not None:
        # consulta
        pedido = models.PedidoCliente.objects.get(pk=pedido_id)
        productos = pedido.productos.all()
        return render(request, "pedidosClienteConsulta.html",{"pedido": pedido,"productos":productos})
    elif request.method == 'GET':
        # filtros
        filters = get_filtros(request.GET, models.PedidoCliente)
        mfilters = dict(filter(lambda v: v[0] in models.PedidoCliente.FILTROS, filters.items()))
        pedidos = models.PedidoCliente.objects.filter(**mfilters)
        clientes = models.Cliente.objects.all()

        totales=dict()
        for pedido in pedidos:
            var=pedido.productos.all()
            var2=pedido.pedidoclientedetalle_set.all()

            print "esssssss",len(var),"el pedido es",pedido.pedidoclientedetalle_set.all()
            for producto in pedido.productos.all():
                print "dentrooooo", producto.nombre
                if producto in totales:
                    totales[producto]=totales[producto]+producto.pedidoclientedetalle_set.all().get(pedido_cliente=pedido).cantidad_producto
                else:
                    print "lpm ",producto.pedidoclientedetalle_set.all().get(pedido_cliente=pedido).cantidad_producto

                    totales[producto]=0
                    print producto.nombre,"  oolisssho ",totales[producto]


        return render(request, "pedidosCliente.html",
                      {"pedidos": pedidos,
                       "filtros": filters,
                       "clientes":clientes})



def pedidosClientesAlta(request, tipo_pedido_id=None):
    detalles_form_class = formset_factory(forms.PedidoClienteDetalleForm)
    detalles_form = None
    pedidosClientes_form = None
    productosTerminados = models.ProductoTerminado.objects.all()

    if request.method == "POST":
        pedidosClientes_form = forms.PedidoClienteFijoForm(request.POST) #crea formulario de receta cno los datos del post
        if  pedidosClientes_form.is_valid():
            print "Estoy en alta papa y soy valido"
            dias = pedidosClientes_form.cleaned_data.get('dias')    #agregado por lo que decia un foro wtf
            pedido_instancia =  pedidosClientes_form.save(commit = False) #commit false
            detalles_form = detalles_form_class(request.POST, request.FILES)
            if detalles_form.is_valid():
                print "soy detalle y soy valido"
                #detalles = detalles_form.save(commit=False)
                pedido_instancia.save()
                for detalle in detalles_form:
                    detalle_instancia = detalle.save(commit=False)
                    detalle_instancia.receta = pedido_instancia
                    detalle_instancia.save()
                messages.success(request, 'El pedido: ' + pedido_instancia.nombre + ', ha sido registrada correctamente.')

                return redirect('pedidosCliente')
        # se lo paso todo a la pagina para que muestre cuales fueron los errores.
        print "Estoy en alta papa y NO soy valido"
    print tipo_pedido_id
    if tipo_pedido_id == "1":
        pedidosClientes_form = forms.PedidoClienteFijoForm()
    elif tipo_pedido_id == "2":
        pedidosClientes_form = forms.PedidoClienteFijoForm()    #poner ocacional
    elif tipo_pedido_id == "3":
        pedidosClientes_form = forms.PedidoClienteFijoForm()

    return render(request, "pedidosClienteAlta.html", {
                "productosTerminados":productosTerminados,
                "pedido_form":  pedidosClientes_form,
                "detalles_form_factory": detalles_form or detalles_form_class()})















#********************************************************#
         #    P E D I D O S   A   P R O V E E D O R   #
#********************************************************#

def pedidosProveedor(request,pedido_id=None):
    if pedido_id is not None:
        # consulta
        pedido_instancia = models.PedidoProveedor.objects.get(pk=pedido_id)
        return render(request, "pedidosProveedorConsulta.html",{"pedido":pedido_instancia})
    elif request.method == 'GET':
        # filtros
        filters = get_filtros(request.GET, models.PedidoProveedor)
        mfilters = dict(filter(lambda v: v[0] in models.PedidoProveedor.FILTROS, filters.items()))
        pedidos = models.PedidoProveedor.objects.filter(**mfilters)
        proveedores = models.Proveedor.objects.all()
        return render(request, "pedidosProveedor.html",
                  {"pedidos": pedidos,"proveedores":proveedores,
                   "filtros": filters})




def pedidosProveedorAlta(request):
    detalles_form_class = formset_factory(forms.DetallePedidoProveedorForm)
    detalles_form = None
    pedido_proveedor_form = None
    insumos = models.Insumo.objects.all()
    if request.method == "POST":
        pedido_proveedor_form = forms.PedidoProveedorForm(request.POST) #crea formulario de pedido con los datos del post
        if pedido_proveedor_form.is_valid():
            pedido_proveedor_instancia = pedido_proveedor_form.save(commit = False) #commit false
            detalles_form = detalles_form_class(request.POST, request.FILES)
            if detalles_form.is_valid():
                #detalles = detalles_form.save(commit=False)
                pedido_proveedor_instancia.save()
                for detalle in detalles_form:
                    detalle_instancia = detalle.save(commit=False)
                    detalle_instancia.receta = pedido_proveedor_instancia
                    detalle_instancia.save()
                messages.success(request, 'El Pedido ha sido registrada correctamente.')

                return redirect('pedidosProveedor')
        # se lo paso todo a la pagina para que muestre cuales fueron los errores.
    return render(request, "pedidosProveedorAlta.html", {
            "insumos":insumos,
            "pedido_proveedor_form": pedido_proveedor_form or forms.PedidoProveedorForm(),
            "detalles_form_factory": detalles_form or detalles_form_class()})

#********************************************************#
         #    L O T E S   #
#********************************************************#
def lotes(request,lote_id=None):
    if lote_id is not None:
        lote = models.Lote.objects.get(pk=lote_id)
        # enviar a lotesConsulta
    else:
        # filtros
        filters = get_filtros(request.GET, models.Lote)
        mfilters = dict(filter(lambda v: v[0] in models.Lote.FILTROS, filters.items()))
        lotes= models.Lote.objects.filter(**mfilters)

    productos = models.ProductoTerminado.objects.all()
    return render(request,"recetas/lotes.html",{"lotes":lotes,"productos":productos})

def lotesModificar(request,lote_id=None):
    lotes = models.Lote.objects.all()
    return render(request,"recetas/lotes.html",{"lotes":lotes})

def lotesAlta(request):
    if request.method == "POST":
        lote_form = forms.LoteForm(request.POST)
        if lote_form.is_valid:
            lote = lote_form.save()
            lote.stock = lote.cantidad_producida

            return redirect("lotes")
    else:
        lote_form=forms.LoteForm()



    return render(request,"lotesAlta.html",{"lote_form":lote_form})
