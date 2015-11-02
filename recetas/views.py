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
import json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import inlineformset_factory
import re #esto sirve para usar expresiones regulares
import datetime

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from itertools import chain


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
    filtros = {}
    filtros_modelo = {}
    for filtro in modelo.FILTROS:
        attr = filtro.split("__")[0]
        field = None
        try:
            field = modelo._meta.get_field(attr)
        except:
            pass
        if attr in get and get[attr]:
            texto = get[attr]
            match=fechareg.match(texto) #aca estoy preguntando si el texto que me viene del GET tiene forma de fecha, si es asi, convierte texto en un tipo "date"
            if match is not None:
                ano = int(match.groups()[2])
                mes = int(match.groups()[1])
                dia = int(match.groups()[0])
                fecha = datetime.date(ano,mes,dia)
                value = datetime.date(ano,mes,dia)
            else:
                value = texto
            if hasattr(modelo, "FILTROS_MAPPER") and filtro in modelo.FILTROS_MAPPER:
                filtro = modelo.FILTROS_MAPPER[filtro]
            filtros[attr] = texto
            filtros_modelo[filtro] = value
        elif attr in get and field is not None and field.get_internal_type() == "BooleanField":
            # Es un valor booleano
            filtros[attr] = ""
            filtros_modelo[filtro] = True
    print(filtros, filtros_modelo)
    return filtros, filtros_modelo

#********************************************************#
               #     C H O F E R E S    #
#********************************************************#
def choferes(request,chofer_id=None):
    """
        Permite buscar choferes con caracteristicas espesificas dentro de un grupo de choferes y obtener la informacion detallada de un chofer
    """
    if chofer_id is not None:
        # consulta
        chofer = models.Chofer.objects.get(pk=chofer_id)
        return render(request, "choferesConsulta.html",{"chofer": chofer})
    elif request.method == 'GET':
        # filtros
        filters, mfilters = get_filtros(request.GET, models.Chofer)
        choferes = models.Chofer.objects.filter(**mfilters)
        return render(request, "recetas/choferes.html",
                  {"choferes": choferes,
                   "filtros": filters})


def choferesAlta(request):
    """
        Recibe una peticion de dar de alta un chofer. Verifica que el nuevo chofer sea valido y de serlo lo da de alta
        precondicion: El chofer a dar de alta no debe existir
        postcondicion: El chofer ha sido dado de alta
    """
    if request.method == "POST":
        chofer_form = forms.ChoferForm(request.POST)
        if chofer_form.is_valid():
            chofer_form.save()
            return redirect('choferes')
    else:
        chofer_form = forms.ChoferForm()

    return render(request, "choferesAlta.html", {"chofer_form":chofer_form})



def choferesModificar(request,chofer_id =None):
    """
        Recibe una peticion de modificar datos de un chofer. Modifica los datos correspondientes del chofer
        precondicion: El chofer a modificar debe existir
        postcondicion: El chofer ha sido modificado
    """
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
    """
        Recibe una peticion de dar de baja un chofer. Da de baja el chofer espedificado.
        precondicion: El chofer a dar de baja debe existir
        postcondicion: El chofer ha sido dado de baja
    """
    chofer = models.Chofer.objects.get(pk=chofer_id)
    # HAY Q HACER VALIDACIONES.
    chofer.delete()
    return redirect('choferes')


#********************************************************#
               #     I N S U M O S    #
#********************************************************#

def insumos(request,insumo_id=None):
    """
        Permite buscar insumos con caracteristicas espesificas dentro de un grupo de insumos y obtener la informacion detallada de un insumo particular
    """

    if insumo_id is not None:
        # consulta
        insumo_instancia = models.Insumo.objects.get(pk=insumo_id)
        insumo_form = forms.InsumoForm(instance= insumo_instancia)
        return render(request, "insumosConsulta.html",{"insumo":insumo_instancia})
    elif request.method == 'GET':
        # filtros
        filters, mfilters = get_filtros(request.GET, models.Insumo)
        insumos = models.Insumo.objects.filter(**mfilters)
        return render(request, "recetas/insumos.html",
                  {"insumos": insumos,
                   "filtros": filters})


def insumosAlta(request):
    """
        Recibe una peticion de dar de alta un insumo. Da de alta el insumo
        precondicion: El insumo a dar de alta no debe existir
        postcondicion: El insumo ha sido dado de alta
    """

    if request.method == "POST":
        insumo_form = forms.InsumoForm(request.POST)
        if insumo_form.is_valid():
            insumo_form.save()
            return redirect('insumos')
    else:
        insumo_form = forms.InsumoForm()
    return render(request, "insumosAlta.html", {"insumo_form":insumo_form})


def insumosModificar(request,insumo_id =None): #zona id nunca va a ser none D:
    """
        Recibe una peticion de modificar datos de un insumo. Modifica los datos correspondientes del insumo
        precondicion: El insumo a modificar debe existir
        postcondicion: El insumo ha sido modificado
    """

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
    """
        Recibe una peticion de dar de baja un insumo. Da de baja el insumo espedificado. Si posee recetas asociadas, tambien las elimina
        precondicion: El insumo a dar de baja debe existir
        postcondicion: El insumo ha sido dado de baja junto a culquier receta asociada al mismo
    """

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

def datosInsumo(request,insumo_id= None):

    insumo= models.Insumo.objects.get( pk= insumo_id)

    data = serializers.serialize('json', [insumo,])
    print "en datois del insumooooooo", data
    return HttpResponse(data, content_type='json')




def insumosModificarStock(request):
    if request.method == 'POST':
        insumo_form = forms.ModificarStockInsumoForm(request.POST)
        if insumo_form.is_valid():
            print "formulario valido"
            insumo_form.save()
            return redirect('insumos')
    else:
        insumo_form = forms.ModificarStockInsumoForm()
    tuplas_json = json.dumps(models.Insumo.TUPLAS)
    return render(request,"modificarStockInsumo.html",{"insumo_form":insumo_form,"tuplas_json":tuplas_json})







#********************************************************#
               #     R E C E T A S    #
#********************************************************#

def recetas(request,receta_id=None):
    """
        Permite buscar recetas con caracteristicas espesificas dentro de un grupo de recetas y obtener la informacion detallada de una receta particular
    """
    if receta_id is not None:
        # consulta
        receta = models.Receta.objects.get(pk=receta_id)
        return render(request, "recetasConsulta.html",{"receta": receta})
    # filtros
    filters, mfilters = get_filtros(request.GET, models.Receta)
    recetas = models.Receta.objects.filter(**mfilters)

        # filtrar recetas por productos
    productos_terminados= models.ProductoTerminado.objects.all()
    return render(request, "recetas/recetas.html",
                      {"recetas": recetas,
                       "filtros": filters,
                       "productos_terminados":productos_terminados})



def recetasModificar(request,receta_id):
    """
        Recibe una peticion de modificar datos de una receta. Modifica los datos correspondientes de la receta
        precondicion: La receta a modificar debe existir
        postcondicion: La receta ha sido modificada
    """
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
    """
       Recibe una peticion de dar de alta una receta. Verifica que la nueva receta sea valida y de serlo la da de alta
       precondicion: La receta a dar de alta no debe existir
       postcondicion: La receta ha sido dada de alta
    """
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
            "detalles_form_factory": detalles_form or detalles_form_class(),
            "prefix":"form"})


def recetasBaja(request,receta_id):
    """
        Recibe una peticion de dar de baja una receta. Da de baja la receta espedificada.
        precondicion: La receta a dar de baja debe existir
        postcondicion: La receta ha sido dada de baja
    """
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
    filters, mfilters = get_filtros(request.GET, models.Proveedor)
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
    filters, mfilters = get_filtros(request.GET, models.Proveedor)
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
        filters, mfilters = get_filtros(request.GET, models.ProductoTerminado)
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
    """
        Permite buscar zonas con caracteristicas espesificas dentro de un grupo de zonas y obtener informacion detallada de una zona particular
    """
    if zona_id is not None:
        # consulta
        zona = models.Zona.objects.get(pk=zona_id)
        ciudades = zona.ciudades.all()
        return render(request, "zonasConsulta.html",{"zona": zona,"ciudades":ciudades})
    elif request.method == 'GET':
        # filtros
        filters, mfilters = get_filtros(request.GET, models.Zona)
        zonas = models.Zona.objects.filter(**mfilters)
        return render(request, "recetas/zonas.html",
                  {"zonas": zonas,
                   "filtros": filters})


def zonasAlta(request):
    """
        Recibe una peticion de dar de alta una zona. Verifica que la nueva zona sea valida y de serlo la da de alta
        precondicion: La zona a dar de alta no debe existir
        postcondicion: La zona ha sido dada de alta
    """
    if request.method == "POST":
        zona_form = forms.ZonaForm(request.POST)
        if zona_form.is_valid():
            zona_form.save()
            return redirect('zonas')
    else:
        zona_form = forms.ZonaForm()
    return render(request, "zonasAlta.html", {"zona_form":zona_form})


def zonasModificar(request,zona_id =None): #zona id nunca va a ser none D:
    """
        Recibe una peticion de modificar datos de una zona. Modifica los datos correspondientes de la zona
        precondicion: La zona a modificar debe existir
        postcondicion: La zona ha sido modificada
    """
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
    """
        Recibe una peticion de dar de baja una zona. Si la zona posee ciudades asociadas muestra un mensaje de error. Si no las posee da de baja la zona espedificada.
        precondicion: La zona a dar de baja debe existir y no debe poseer ciudades asociadas
        postcondicion: La zona ha sido dada de baja
    """
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
        filters, mfilters = get_filtros(request.GET, models.Cliente)
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
    """
        Permite buscar ciudades con caracteristicas espesificas dentro de un grupo de ciudades y obtener informacion detallada de una ciudad particular
    """
    if ciudad_id is not None:
        # consulta
        ciudad = models.Ciudad.objects.get(pk=ciudad_id)
        return render(request, "ciudadesConsulta.html",{"ciudad": ciudad})
    elif request.method == 'GET':
        # filtros
        filters, mfilters = get_filtros(request.GET, models.Ciudad)
        ciudades = models.Ciudad.objects.filter(**mfilters)
        zonas = models.Zona.objects.all()
        return render(request, "recetas/ciudades.html",{"filtros": filters,"ciudades":ciudades,"zonas":zonas})



def ciudadesAlta(request):
    """
        Recibe una peticion de dar de alta una ciudad. Verifica que la nueva ciudad sea valida y de serlo la da de alta
        precondicion: La ciudad a dar de alta no debe existir
        postcondicion: La ciudad ha sido dada de alta
    """
    if request.method == "POST":
        ciudad_form = forms.CiudadForm(request.POST)
        if ciudad_form.is_valid():
            ciudad_form.save()
            return redirect('ciudades')
    else:
        ciudad_form = forms.CiudadForm()
    return render(request, "ciudadesAlta.html", {"ciudad_form":ciudad_form})


def ciudadesModificar(request,ciudad_id =None): #zona id nunca va a ser none D:
    """
        Recibe una peticion de modificar datos de una ciudad. Modifica los datos correspondientes de la ciudad
        precondicion: La ciudad a modificar debe existir
        postcondicion: La ciudad ha sido modificada
    """
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
    """
        Recibe una peticion de dar de baja una ciudad.Da de baja la ciudad espedificada.
        precondicion: La ciudad a dar de baja debe existir
        postcondicion: La ciudad ha sido dada de baja
    """
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
        filters, mfilters = get_filtros(request.GET, models.PedidoCliente)
        pedidos = models.PedidoCliente.objects.filter(**mfilters)
        clientes = models.Cliente.objects.all()
        totales=dict()
        for pedido in pedidos:
            for producto in pedido.productos.all():
                if producto in totales:
                    totales[producto]=totales[producto]+producto.pedidoclientedetalle_set.all().get(pedido_cliente=pedido).cantidad_producto
                else:
                    totales[producto]=0
                    totales[producto]=totales[producto]+producto.pedidoclientedetalle_set.all().get(pedido_cliente=pedido).cantidad_producto
        print "diccionario",totales
        return render(request, "pedidosCliente.html",
                      {"pedidos": pedidos,
                       "filtros": filters,
                       "clientes":clientes,
                       "totales":totales})



def pedidosClientesAlta(request, tipo_pedido_id):
    detalles_form_class = formset_factory(forms.PedidoClienteDetalleForm)
    detalles_form = None
    pedidosClientes_form = None
    productosTerminados = models.ProductoTerminado.objects.all()
    if tipo_pedido_id == "1":
        pedidosClientes_form = forms.PedidoClienteFijoForm
    elif tipo_pedido_id == "2":
        pedidosClientes_form = forms.PedidoClienteOcacionalForm

    elif tipo_pedido_id == "3":
        pedidosClientes_form = forms.PedidoClienteCambioForm

    if request.method == "POST":
        pedidosClientes_form = pedidosClientes_form(request.POST) #crea formulario de receta cono los datos del post
        if  pedidosClientes_form.is_valid():
            if tipo_pedido_id == "1":
                dias = pedidosClientes_form.cleaned_data.get('dias')    #agregado por lo que decia un foro wtf
            pedido_instancia =  pedidosClientes_form.save(commit = False) #commit false
            detalles_form = detalles_form_class(request.POST, request.FILES)
            if detalles_form.is_valid():
                pedido_instancia.tipo_pedido=tipo_pedido_id
                print pedido_instancia
                pedido_instancia.save()
                for detalle in detalles_form:
                    detalle_instancia = detalle.save(commit=False)
                    detalle_instancia.pedido_cliente = pedido_instancia
                    detalle_instancia.save()
               # messages.success(request, 'El pedido: ' + pedido_instancia.get_tipo_pedido_display() + ', ha sido registrada correctamente.')

                return redirect('pedidosCliente')
        # se lo paso todo a la pagina para que muestre cuales fueron los errores.
    return render(request, "pedidosClienteAlta.html", {
                "productosTerminados":productosTerminados,
                "pedido_form":  pedidosClientes_form,
                "detalles_form_factory": detalles_form or detalles_form_class(),
                "tipo_pedido": tipo_pedido_id})



def pedidosClienteBaja(request,pedido_id):
    pedido = models.PedidoCliente.objects.get(pk=pedido_id)
    #messages.success(request, 'El pedido: de "+pedido.cliente.razon_social + ', ha sido eliminada correctamente.')
    pedido.delete()     #hacer baja logica
    return redirect('pedidosCliente')


def pedidosClienteModificar(request, pedido_id):
    '''
    pedido_instancia = get_object_or_404(models.PedidoCliente, pk=pedido_id)
    pedido_class = models.PedidoCliente.TIPOS[pedido_instancia.TIPO]
    pedido_instancia = get_object_or_404(pedido_class, pk=pedido_id)
    detalles_inlinefactory = inlineformset_factory(pedido_class, models.PedidoClienteDetalle, fields=('cantidad_producto','producto_terminado','pedido_cliente'))
    # aca hay que hacer o mismo que hicmos para modelos peropara form.
    pedidosClientes_form = forms.PedidoClienteFijoForm

    detalles_instancias = models.PedidoClienteDetalle.objects.filter(pedido_cliente = pedido_instancia)
    pedidosClientes_form = pedidosClientes_form(instance= pedido_instancia)
    productos = models.ProductoTerminado.objects.all() #para detalles
    '''

    pedido_instancia = get_object_or_404(models.PedidoCliente, pk=pedido_id)
    if pedido_instancia.tipo_pedido == 1:
        pedido_instancia = get_object_or_404(models.PedidoFijo, pk=pedido_id)
        detalles_inlinefactory = inlineformset_factory(models.PedidoCliente,models.PedidoClienteDetalle,fields=('cantidad_producto','producto_terminado','pedido_cliente'))
        pedidosClientes_form = forms.PedidoClienteFijoForm

    elif pedido_instancia.tipo_pedido == 2:
        pedido_instancia = get_object_or_404(models.PedidoOcacional, pk=pedido_id)
        detalles_inlinefactory = inlineformset_factory(models.PedidoCliente,models.PedidoClienteDetalle,fields=('cantidad_producto','producto_terminado','pedido_cliente'))
        pedidosClientes_form = forms.PedidoClienteOcacionalForm
    else:
        pedido_instancia = get_object_or_404(models.PedidoCambio, pk=pedido_id)
        detalles_inlinefactory = inlineformset_factory(models.PedidoCliente,models.PedidoClienteDetalle,fields=('cantidad_producto','producto_terminado','pedido_cliente'))
        pedidosClientes_form = forms.PedidoClienteCambioForm

    detalles_instancias = models.PedidoClienteDetalle.objects.filter(pedido_cliente = pedido_instancia)
    pedidosClientes_form = pedidosClientes_form(instance= pedido_instancia)
    productos = models.ProductoTerminado.objects.all() #para detalles

    if request.method=="POST":
        if pedido_instancia.tipo_pedido == 1:
            pedidosClientes_form = forms.PedidoClienteFijoForm(request.POST,instance= pedido_instancia)
        elif pedido_instancia.tipo_pedido == 2:
            pedidosClientes_form = forms.PedidoClienteOcacionalForm(request.POST,instance= pedido_instancia)
        else:
            pedidosClientes_form = forms.PedidoClienteCambioForm(request.POST,instance= pedido_instancia)
        if pedidosClientes_form.is_valid():
            pedido_instancia = pedidosClientes_form.save(commit=False)
            #DETALLES
            detalles_formset = detalles_inlinefactory(request.POST,request.FILES,prefix='pedidoclientedetalle_set',instance=pedido_instancia)
            print detalles_formset.is_valid()
            if detalles_formset.is_valid():
                detalles_formset.save()
                messages.success(request, 'El pedido: ' + pedido_instancia.get_tipo_pedido_display()+" de "+pedido_instancia.cliente.razon_social + ', ha sido modificada correctamente.')
                pedido_instancia.save()
            return redirect('pedidosCliente')

    #si el form no es valido, le mando todo al html para que muestre los errores#
    pref = "pedidoclientedetalle_set" #pedidoclientedetalle_set
    return render(request,"pedidosClienteModificar.html",{"pedido_form":pedidosClientes_form,"id":pedido_id,
                                                   "detalles_pedido":detalles_instancias,
                                                   "productos":productos,
                                                   "detalles_form_factory":detalles_inlinefactory(initial=list(detalles_instancias.values()), prefix='pedidoclientedetalle_set'),
                                                   "pedido_id":pedido_id,
                                                   "pref":pref,
                                                   "tipo_pedido":pedido_instancia.tipo_pedido,
                                                    "id_cliente":pedido_instancia.cliente.id

                                                   })



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
        filters, mfilters = get_filtros(request.GET, models.PedidoProveedor)
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
        pedido_proveedor_form = forms.PedidoProveedorAltaForm(request.POST) #crea formulario de pedido con los datos del post
        if pedido_proveedor_form.is_valid():
            pedido_proveedor_instancia = pedido_proveedor_form.save(commit = False) #commit false
            detalles_form = detalles_form_class(request.POST, request.FILES)
            if detalles_form.is_valid():
                #detalles = detalles_form.save(commit=False)
                pedido_proveedor_instancia.save()

                for detalle in detalles_form:
                    detalle_instancia = detalle.save(commit=False)
                    detalle_instancia.pedido_proveedor = pedido_proveedor_instancia
                    detalle_instancia.save()


                messages.success(request, 'El Pedido ha sido registrada correctamente.')

                return redirect('pedidosProveedor')
        # se lo paso todo a la pagina para que muestre cuales fueron los errores.
            #por el get paso el id del proveedor
    else:

        pedido_proveedor_form = forms.PedidoProveedorAltaForm() #crea formulario de pedido con los datos del post
        insumos = None
        try:
            id_proveedor = request.GET['proveedor']
            id_fecha = request.GET['fecha']
            proveedor = models.Proveedor.objects.get(pk=id_proveedor)
            insumos = proveedor.insumos.all()
            form = forms.PedidoProveedorAltaForm(initial={'proveedor':id_proveedor,'fecha_realizacion':id_fecha})#esto esta copado, te iniciaiza los datos del form automatico de django con los valores que vos queres......

            return render(request, "pedidosProveedorAlta.html", {
                "insumos":insumos,
                "idProveedor":id_proveedor,
                "pedido_proveedor_form": form,
                "detalles_form_factory": detalles_form or detalles_form_class()})
        except:
            return render(request, "pedidosProveedorAlta.html", {
                "insumos":insumos,
                "pedido_proveedor_form": pedido_proveedor_form or forms.PedidoProveedorAltaForm(),
                "detalles_form_factory": detalles_form or detalles_form_class()})



def pedidosProveedorModificar(request,pedido_id):
    pedido_proveedor_instancia = get_object_or_404(models.PedidoProveedor, pk=pedido_id)
    detalles_instancias = models.DetallePedidoProveedor.objects.filter(pedido_proveedor = pedido_proveedor_instancia)

    proveedor = models.Proveedor.objects.get(pk=pedido_proveedor_instancia.proveedor.id)
    insumos = proveedor.insumos.all()

    detalles_inlinefactory = inlineformset_factory(models.PedidoProveedor,models.DetallePedidoProveedor,fields=('cantidad_insumo','insumo','pedido_proveedor'))

    if request.method=="POST":
        pedido_proveedor_form = forms.PedidoProveedorModificarForm(request.POST,instance= pedido_proveedor_instancia)
        if pedido_proveedor_form.is_valid():
            pedido_proveedor_instancia = pedido_proveedor_form.save(commit=False)
            #DETALLES
            detalles_formset = detalles_inlinefactory(request.POST,request.FILES,prefix='pedidodetalle_set',instance=pedido_proveedor_instancia)
            if detalles_formset.is_valid():
                print(detalles_formset)
                detalles_formset.save()
                messages.success(request, 'El Pedido ha sido modificado correctamente.')
                pedido_proveedor_instancia.save()
            return redirect('pedidosProveedor')
    else:
         pedido_proveedor_form = forms.PedidoProveedorModificarForm(instance= pedido_proveedor_instancia)
         proveedor = models.Proveedor.objects.get(pk=pedido_proveedor_instancia.proveedor.id)
        #si el form no es valido, le mando todo al html para que muestre los errores#
    pref = "pedidodetalle_set"
    return render(request,"pedidosProveedorModificar.html",{"pedido_proveedor_form":pedido_proveedor_form,"id":pedido_id,
                                                   "detalles_pedido":detalles_instancias,
                                                   "insumos":insumos,
                                                   "detalles_form_factory":detalles_inlinefactory(initial=list(detalles_instancias.values()), prefix='pedidodetalle_set'),
                                                   "pedido_id":pedido_id,"proveedor":proveedor,
                                                   "pref":pref
                                                   })


def pedidosProveedorRecepcionar(request,pedido_id):
    pedido_proveedor_instancia = get_object_or_404(models.PedidoProveedor, pk=pedido_id)
    proveedor = models.Proveedor.objects.get(pk=pedido_proveedor_instancia.proveedor.id)
    if request.method == "POST":
        pedido_proveedor_form = forms.PedidoProveedorRecepcionarForm(request.POST, instance=pedido_proveedor_instancia)
        if pedido_proveedor_form.is_valid():
            pedido_proveedor_instancia.save()
            messages.success(request, 'El Pedido ha sido recepcionado correctamente.')
            return redirect('pedidosProveedor')
    else:
        pedido_proveedor_form = forms.PedidoProveedorRecepcionarForm(instance=pedido_proveedor_instancia)

    return render(request,"pedidosProveedorRecepcionar.html",{
        "pedido_proveedor_form":pedido_proveedor_form,
        "proveedor":proveedor,
        "pedido_id":pedido_id})

#la idea es que en proveedorRepecionar se recpcione y actualice el stock
#poner un boton de cancelar, para cancelar el pedio




@csrf_exempt
def pedidosProveedorBaja(request,pedido_id =None):
    print "estoy en bajaaa"
    p = models.PedidoProveedor.objects.get(pk=pedido_id)
    messages.success(request, 'El pedido realizado en la fecha: ' + p.fecha_realizacion.strftime('%d/%m/%Y') + ', realizado al proveedor: ' + p.proveedor.razon_social +', ha sido eliminado correctamente.')
    p.delete()
    return redirect('pedidosProveedor')



def pedidosProveedorCancelar(request,pedido_id =None):
    print "estoy en cancelar pedido..."
    p = models.PedidoProveedor.objects.get(pk=pedido_id)
    p.estado_pedido = 3
    p.save()
    print(p.estado_pedido)
    messages.success(request, 'El pedido realizado en la fecha: ' + p.fecha_realizacion.strftime('%d/%m/%Y') + ', realizado al proveedor: ' + p.proveedor.razon_social +', ha sido cancelado correctamente.')
    return redirect('pedidosProveedor')

#********************************************************#
         #    L O T E S   #
#********************************************************#
def lotes(request,lote_id=None):
    if lote_id is not None:
        #consulta
        lote = models.Lote.objects.get(pk=lote_id)
        return render(request,"lotesConsulta.html",{"lote":lote})
    else:
        # filtros
        filters, mfilters = get_filtros(request.GET, models.Lote)
        lotes= models.Lote.objects.filter(**mfilters)

    productos = models.ProductoTerminado.objects.all()
    return render(request,"recetas/lotes.html",{"lotes":lotes,"productos":productos})


def lotesModificar(request,lote_id=None):
    lote_instancia = models.Lote.objects.get(pk=lote_id)
    lote_form = forms.LoteForm(instance=lote_instancia)
    return render(request,"lotesModificar.html",{"lote_form":lote_form,"id":lote_id})


def lotesAlta(request):
    if request.method == "POST":
        lote_form = forms.LoteForm(request.POST)
        if lote_form.is_valid():
            lote = lote_form.save(commit = False)
            lote.stock_disponible = lote.cantidad_producida #stock inicial
            lote.save()
            # actualizo stock del producto
            lote.producto_terminado.stock +=  lote.stock_disponible
            lote.producto_terminado.save()
            # disminuye stock de insumos
            try:
                receta = lote.producto_terminado.receta_set.get()
                cant__producida= lote.cantidad_producida
                detalles_receta = receta.recetadetalle_set.all()
                for detalle_receta in  detalles_receta:
                    cant_decrementar =(detalle_receta.cantidad_insumo * cant__producida) / receta.cant_prod_terminado
                    detalle_receta.insumo.decrementar(cant_decrementar)
                    if detalle_receta.insumo.stock < 0:
                        messages.error(request, 'El insumo %s quedo con stock %d '%(detalle_receta.insumo,detalle_receta.insumo.stock))
                    detalle_receta.insumo.save()
            except:
                messages.success(request, 'No se actualizo stock de insumos ya que no hay receta asociada al Producto')
            return redirect("lotes")
    else:
        lote_form=forms.LoteForm()
    return render(request,"lotesAlta.html",{"lote_form":lote_form})

def lotesBaja(request,lote_id):
    l = models.Lote.objects.get(pk=lote_id)
    l.producto_terminado.stock = l.producto_terminado.stock - l.stock_disponible
    l.producto_terminado.save()
    l.delete()
    messages.success(request, 'Lote fue eliminado correctamente.')
    return redirect ('lotes')


#********************************************************#
         #    H O J A   D E  R U T A    #
#********************************************************#
def hojaDeRuta(request):

        pedidos_clientes = []
        pedidos_fijos = models.PedidoFijo.objects.all()
        pedidos_ocacionales = models.PedidoOcacional.objects.all()
        pedidos_cambio = models.PedidoCambio.objects.all()
        detalles_form = formset_factory(forms.LotesExtraDetalleForm())
        hojaDeRuta_form = forms.HojaDeRutaForm()
        pedidos_clientes= chain(models.PedidoFijo.objects.all(), models.PedidoOcacional.objects.all(),models.PedidoCambio.objects.all())
        pedidos_clientes_enviar = []
        for pedido in pedidos_clientes:
            #print pedido.__class__
            if pedido.esParaHoy():
               pedidos_clientes_enviar.append(pedido)
        choferes = models.Chofer.objects.all()
        productos = models.ProductoTerminado.objects.all()
        return render(request, "hojaDeRuta.html",{"hojaDeRuta_form": hojaDeRuta_form,"detalles_form":detalles_form,"pedidos":pedidos_clientes_enviar,"choferes":choferes,"productos":productos})



def generarTotales(request):
    print "soy viewwwwwww"
    pedidos=request.POST.getlist('tasks[]')
    #pedidos = json.loads(request.raw_post_data)
    print pedidos, "soy listtaaaaaaaaaaaaa"



    return HttpResponse('Success')
    '''
    data = serializers.serialize('json', [insumo,])
    print "en datois del insumooooooo", data
    return HttpResponse(data, content_type='json')
'''