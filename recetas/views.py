from django.shortcuts import render, redirect,render_to_response
from . import models
from . import forms
from django.forms.formsets import formset_factory
from django.shortcuts import get_object_or_404
from django.forms.models import BaseModelFormSet
from django.forms.models import modelformset_factory
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.contrib.messages import get_messages
import json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import inlineformset_factory
import re #esto sirve para usar expresiones regulares
import datetime
from datetime import date
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from itertools import chain
import xhtml2pdf.pisa as pisa
from wkhtmltopdf import *
from django.template.loader import get_template
from django.template.context import RequestContext
from django.core.context_processors import csrf
import StringIO
from django.template import Context
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required






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
    return filtros, filtros_modelo

#********************************************************#
               #     C H O F E R E S    #
#********************************************************#
@login_required()
@permission_required('recetas.add_chofer')
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
        choferes = choferes.filter(activo=True)
        #choferes = [c for c in choferes if c.activo == True]
        return render(request, "recetas/choferes.html",
                  {"choferes": choferes,
                   "filtros": filters})


@login_required()
@permission_required('recetas.add_chofer')
def choferesAlta(request):
    """
    Recibe una peticion de dar de alta un chofer. Verifica que el nuevo chofer sea valido y de serlo lo da de alta
        precondicion: El chofer a dar de alta no debe existir
        postcondicion: El chofer ha sido dado de alta
        """

    if request.method == "POST":
        chofer_form = forms.ChoferForm(request.POST)
        print chofer_form['nombre'].value, "nombre choferrrr"
        if chofer_form.is_valid():
            chofer_form.save()
            return redirect('choferes')
    else:
        chofer_form = forms.ChoferForm()

    return render(request, "choferesAlta.html", {"chofer_form":chofer_form})



@login_required()
@permission_required('recetas.change_chofer')
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



@login_required()
@csrf_exempt
@permission_required('recetas.delete_chofer')
def choferesBaja(request,chofer_id=None):
    """
        Recibe una peticion de dar de baja un chofer. Da de baja el chofer espedificado.
        precondicion: El chofer a dar de baja debe existir
        postcondicion: El chofer ha sido dado de baja
    """
    chofer = models.Chofer.objects.get(pk=chofer_id)
    # HAY Q HACER VALIDACIONES.
    hojas_de_ruta=models.HojaDeRuta.objects.filter(chofer=chofer)
    hojas_de_ruta = hojas_de_ruta.filter(rendida=False)
    if len(hojas_de_ruta) == 0:
        #chofer.delete()
        chofer.activo=False
        chofer.save()
    else:
        messages.error(request, 'El chofer: ' + chofer.nombre + ' no se puede eliminar porque tiene hojas de rutas pendientes')
    return redirect('choferes')


#********************************************************#
               #     I N S U M O S    #
#********************************************************#

@login_required()
@permission_required('recetas.add_insumo')
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
        insumos = [i for i in insumos if i.activo == True]
        return render(request, "recetas/insumos.html",
                  {"insumos": insumos,
                   "filtros": filters})



@login_required()
@permission_required('recetas.add_insumo')
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



@login_required()
@permission_required('recetas.change_insumo')
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



@login_required()
@permission_required('recetas.delete_insumo')
def insumosBaja(request,insumo_id):
    """
        Recibe una peticion de dar de baja un insumo. Da de baja el insumo espedificado. Si posee recetas asociadas, tambien las elimina
        precondicion: El insumo a dar de baja debe existir
        postcondicion: El insumo ha sido dado de baja junto a culquier receta asociada al mismo
    """

    insumo = models.Insumo.objects.get(pk=insumo_id)


    if len(insumo.pedidoproveedor_set.all())>0:
        messages.error(request, 'El Insumo: ' + insumo.nombre + ', no se puede eliminar porque tiene asociados pedidos a proveedores. \n Si desea eliminarlo, elimine primero los pedidos.')
        return redirect('insumos')

    if insumo.receta_set.exists():
        messages.error(request, 'El Insumo: ' + insumo.nombre + ', no se ha podido eliminar porque tiene las siguiente recetas asociadas: %s .' % ", ".join(
           [ "%s" % r for r in insumo.receta_set.all()]
        ))
        return redirect('insumos')
        #insumo.delete()
    else:
        messages.success(request, 'El Insumo: ' + insumo.nombre + ', ha sido eliminado correctamente.')
        #insumo.delete()
    insumo.activo=False
    insumo.save()
    return redirect('insumos')




@login_required()
def datosInsumo(request,insumo_id= None):
    insumo= models.Insumo.objects.get( pk= insumo_id)
    insumo_data = serializers.serialize('json', [insumo,])

    t = request.GET['b']
    b = request.GET['t']
    pedidos_list = re.findall("\d+",request.GET['pedidos'])
    for i in range(0,len(pedidos_list)):
        #los paso a INT para buscarlos despues
        pedidos_list[i]= int(pedidos_list[i])
        print "pedido entero: ",pedidos_list[i]

    return HttpResponse(insumo_data, content_type='json')




@login_required()
@permission_required('recetas.change_insumo')
def insumosModificarStock(request):
    if request.method == 'POST':
        insumo_form = forms.ModificarStockInsumoForm(request.POST)
        if insumo_form.is_valid():
            print "formulario valido"
            insumo_form.save()
            return redirect('insumos')
    else:
        insumo_form = forms.ModificarStockInsumoForm()
    tuplas_json = json.dumps(models.Insumo.TUPLAS)  # es para diccionarios
    return render(request,"modificarStockInsumo.html",{"insumo_form":insumo_form,"tuplas_json":tuplas_json})







#********************************************************#
               #     R E C E T A S    #
#********************************************************#
@login_required()
@permission_required('recetas.add_receta')
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
    productos_terminados= models.ProductoTerminado.objects.filter(activo=True)
    return render(request, "recetas/recetas.html",
                      {"recetas": recetas,
                       "filtros": filters,
                       "productos_terminados":models.ProductoTerminado.objects.all()})




@login_required()
@permission_required('recetas.change_receta')
def recetasModificar(request,receta_id):
    """
        Recibe una peticion de modificar datos de una receta. Modifica los datos correspondientes de la receta
        precondicion: La receta a modificar debe existir
        postcondicion: La receta ha sido modificada
    """
    detalles_formset = None
    receta_instancia = get_object_or_404(models.Receta, pk=receta_id)
    detalles_instancias = models.RecetaDetalle.objects.filter(receta = receta_instancia)
    insumos = models.Insumo.objects.filter(activo=True) #para detalles
    detalles_inlinefactory = inlineformset_factory(models.Receta,models.RecetaDetalle,fields=('cantidad_insumo','insumo','receta'))
    error = False
    if request.method == "POST":
        receta_form = forms.RecetaForm(request.POST,instance= receta_instancia)
        detalles_formset = detalles_inlinefactory(request.POST,request.FILES,prefix='recetadetalle_set',instance=receta_instancia)
        if receta_form.is_valid():
            receta_instancia = receta_form.save(commit=False)
            #Detalles
            if detalles_formset.is_valid():
                detalles_formset.save()
                messages.success(request, 'La Receta: ' + receta_instancia.nombre + ', ha sido modificada correctamente.')
                receta_instancia.save()
            return redirect('recetas')
        else:
            error = True
    else:
        receta_form = forms.RecetaForm(instance= receta_instancia)        
    pref = "recetadetalle_set"
    return render(request,"recetasModificar.html",{"receta_form":receta_form,"id":receta_id,
                                                   "detalles_receta":detalles_instancias,
                                                   "insumos":insumos,
                                                   "detalles_form_factory":detalles_formset or detalles_inlinefactory(initial=list(detalles_instancias.values()), prefix='recetadetalle_set'),
                                                   "error": error,
                                                   "receta_id":receta_id,
                                                   "pref":pref
                                                   })



@login_required()
@permission_required('recetas.add_receta')
def recetasAlta(request):
    """
       Recibe una peticion de dar de alta una receta. Verifica que la nueva receta sea valida y de serlo la da de alta
       precondicion: La receta a dar de alta no debe existir
       postcondicion: La receta ha sido dada de alta
    """
    detalles_form_class = formset_factory(forms.RecetaDetalleForm)
    detalles_form = None
    receta_form = None
    insumos = models.Insumo.objects.filter(activo=True)
    if request.method == "POST":
        receta_form = forms.RecetaForm(request.POST) #crea formulario de receta cno los datos del post
        detalles_form = detalles_form_class(request.POST, request.FILES)
        if receta_form.is_valid():
            receta_instancia = receta_form.save(commit = False) #commit false            
            if detalles_form.is_valid():
                #detalles = detalles_form.save(commit=False)
                receta_instancia.save()
                for detalle in detalles_form:
                    detalle_instancia = detalle.save(commit=False)
                    detalle_instancia.receta = receta_instancia
                    detalle_instancia.save()
                messages.success(request, 'La Receta: ' + receta_instancia.nombre + ', ha sido registrada correctamente.')
                return redirect('recetas')
    return render(request, "recetasAlta.html", {
            "insumos":insumos,
            "receta_form": receta_form or forms.RecetaForm(),
            "detalles_form_factory": detalles_form or detalles_form_class(),
            "prefix":"form"})




@login_required()
@permission_required('recetas.delete_receta')
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

@login_required()
@permission_required('recetas.add_proveedor')
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

@login_required()
@permission_required('recetas.add_proveedor')
def proveedoresAlta(request):
    proveedores_form = forms.ProveedorForm()
    insumos = models.Insumo.objects.filter(activo=True)
    error = False
    if request.method == "POST":
        proveedores_form = forms.ProveedorForm(request.POST)
        if proveedores_form.is_valid():
            proveedor_instancia=proveedores_form.save()
            return redirect('proveedores')
        else:
            error = True    
    return render(request, "proveedoresAlta.html",{"proveedores_form": proveedores_form,
                                                    "insumos":insumos,"error":error})





@login_required()
@permission_required('recetas.delete_proveedor')
@csrf_exempt
def proveedoresBaja(request,proveedor_id =None):
    p = models.Proveedor.objects.get(pk=proveedor_id)
    p.delete()
    #p.activo=False
    #p.save()
    return redirect('proveedores')
    



@login_required()
@permission_required('recetas.change_proveedor')
def proveedoresModificar(request,proveedor_id =None):
    proveedor_instancia = get_object_or_404(models.Proveedor, pk=proveedor_id)
    insumos_instancias = models.Insumo.objects.filter(activo=True)
    error = False
    proveedor_form = None
    if request.method=="POST":
        proveedor_form = forms.ProveedorModificarForm(request.POST,instance= proveedor_instancia)
        if proveedor_form.is_valid():
            proveedor_form.save()
            return redirect('proveedores')
        else:
            error = True
    return render(request,"proveedoresModificar.html",{"insumos_instancias":insumos_instancias,
                        "proveedor_form":proveedor_form or forms.ProveedorModificarForm(instance= proveedor_instancia),
                                                            "id":proveedor_id,"error":error})

#********************************************************#
               #     P R O D U C T O S   #
#********************************************************#

@login_required()
@permission_required('recetas.add_productoterminado')
def productosTerminados(request,producto_id=None):
    if producto_id is not None:
        # consulta
        producto = models.ProductoTerminado.objects.get(pk=producto_id)

        return render(request, "productosTerminadosConsulta.html",{"producto": producto})
    elif request.method == 'GET':
        # filtros
        filters, mfilters = get_filtros(request.GET, models.ProductoTerminado)
        productos = models.ProductoTerminado.objects.filter(**mfilters)
        productos = [i for i in productos if i.activo == True]

        return render(request, "recetas/productosTerminados.html",
                  {"productos": productos,
                   "filtros": filters})



@login_required()
@permission_required('recetas.add_productoterminado')
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



@login_required()
@permission_required('recetas.change_productoterminado')
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



@login_required()
@permission_required('recetas.delete_productoterminado')
@csrf_exempt
def productosTerminadosBaja(request, producto_id=None):
    print "estoy en bajaaa"
    p = models.ProductoTerminado.objects.get(pk=producto_id)
    '''
    try:
        lotes_disponibles = len(p.lote_set.filter(stock_disponible>0)
    except:
        lotes_disponibles = 1      
        #para que lo pueda aliminar
    finally:
        pass
    '''
    if len(p.pedidocliente_set.filter(activo=True))> 0:
        messages.error(request, 'El Producto: ' + p.nombre + ', no se puede eliminar porque tiene pedidos asociados.')
    elif len(p.lote_set.filter(stock_disponible__gt = 0))>0:
        messages.error(request, 'El Producto: ' + p.nombre + ', no se puede eliminar porque tiene lotes con stock disponible.')
    elif p.receta_set.exists():
        messages.error(request, 'El producto: ' + p.nombre + ', se elimino correctamente junto a las recetas: %s .' % ", ".join(
            [ "%s" % r for r in p.receta_set.all()]
        ))
        p.activo=False
        p.save()
    else:
        messages.success(request, 'El Producto: ' + p.nombre + ', ha sido eliminado correctamente.')
        p.activo=False
        p.save()
    return redirect('productosTerminados')









#********************************************************#
              #     Z O N A S    #
#********************************************************#
@login_required()
@permission_required('recetas.add_zona')
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




@login_required()
@permission_required('recetas.add_zona')
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



@login_required()
@permission_required('recetas.change_zona')
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



@login_required()
@permission_required('recetas.delete_zona')
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
@login_required()
@permission_required('recetas.add_cliente')
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
        clientes_form = forms.ClienteModificarForm()
        ciudades= models.Ciudad.objects.all()
        return render(request, "recetas/clientes.html",
                  {"clientes": clientes,
                   "filtros": filters,
                   "ciudades":ciudades})





@login_required()
@permission_required('recetas.change_cliente')
def clientesModificar(request,cliente_id = None):
    cliente_instancia = get_object_or_404(models.Cliente, pk=cliente_id)
    if request.method=="POST":
        cliente_form = forms.ClienteModificarForm(request.POST,instance= cliente_instancia)
        if cliente_form.is_valid():
            print "ENCLIENTEEEEE",cliente_instancia.saldo

            if cliente_instancia.es_moroso and cliente_instancia.saldo==0:
                print(cliente_instancia.es_moroso)
                messages.error(request,'El cliente no puede ser moroso ya que no posee saldo deudor')
                cliente_form = forms.ClienteModificarForm(initial={'cuit':cliente_instancia.cuit,'razon_social':cliente_instancia.razon_social,'nombre_dueno':cliente_instancia.nombre_dueno,'ciudad':cliente_instancia.ciudad,'direccion':cliente_instancia.direccion,'telefono':cliente_instancia.telefono,'email':cliente_instancia.email,'es_moroso':cliente_instancia.es_moroso})
                return render(request,"clientesModificar.html",{"cliente_form":cliente_form,"id":cliente_id})
            cliente_form.save()
            return redirect('clientes')
        else:
            return render(request,"clientesModificar.html",{"cliente_form":cliente_form,"id":cliente_id})


    else:
        cliente_form = forms.ClienteModificarForm(instance= cliente_instancia)
        return render(request,"clientesModificar.html",{"cliente_form":cliente_form,"id":cliente_id})



@login_required()
@permission_required('recetas.add_cliente')
def clientesAlta(request):
    if request.method == "POST":
        cliente_form = forms.ClienteAltaForm(request.POST)
        if cliente_form.is_valid():
            cliente_form.save()
            return redirect('clientes')
    else:
        cliente_form = forms.ClienteAltaForm()
    return render(request, "clientesAlta.html", {"cliente_form":cliente_form})




@login_required()
@permission_required('recetas.delete_cliente')
@csrf_exempt
def clientesBaja(request,cliente_id =None):
    p = models.Cliente.objects.get(pk=cliente_id)
    if p.saldo >0:
        messages.error(request, 'El cliente: ' + p.razon_social + ', no se puede eliminar porque tiene deudas')
    else:
        p.activo=False
        p.save()
        #p.delete()
    return redirect('clientes')


#********************************************************#
               #     C I U D A D E S   #
#********************************************************#
@login_required()
@permission_required('recetas.add_ciudad')
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




@login_required()
@permission_required('recetas.add_ciudad')
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



@login_required()
@permission_required('recetas.change_ciudad')
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




@login_required()
@permission_required('recetas.delete_ciudad')
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

#@login_required()
#@permission_required('recetas.change_pedidocliente')
'''
>>>>>>> origin/master
def eliminarVencidos():
    pedidos_fijos = models.PedidoFijo.objects.all()
    for pedido in pedidos_fijos:
        if pedido.fecha_cancelacion != None and pedido.fecha_cancelacion<date.today():
            pedido.activo=False
            pedido.save()
            print "en vencidos: ",pedido.id
    #los de cambio y ocacionales se deben eliminar cuando se hace la rendicion
'''



@login_required()
@permission_required('recetas.add_pedidocliente')
def pedidosClientes(request,pedido_id=None):
    ''' Muestra los pedidos de clientes que esten vigentes, pudiendolos filtrarlos segun atributos.
        Tambien procesa un pedido seleccionado para mostrar su informacion completa
    '''
    #eliminarVencidos()
    if pedido_id is not None:
        # consulta
        pedido = models.PedidoCliente.objects.get(pk=pedido_id)
        productos = pedido.productos.all()
        return render(request, "pedidosClienteConsulta.html",{"pedido": pedido,"productos":productos})
    elif request.method == 'GET':
        # filtros
        print "GET ",request.GET
        #filtros para filtrar por rango de fechas de entrega, varia para cada tipo
        filters, mfilters = get_filtros(request.GET, models.PedidoCliente)
        pobj = Q(**mfilters)
        filters, mfilters = get_filtros(request.GET, models.PedidoFijo)
        qobj = Q(**mfilters)
        filters, mfilters = get_filtros(request.GET, models.PedidoOcacional)
        qobj |= Q(**mfilters)
        filters, mfilters = get_filtros(request.GET, models.PedidoCambio)
        qobj |= Q(**mfilters)
        pedidos = models.PedidoCliente.objects.filter(pobj & qobj)
        pedidos = pedidos.filter(activo=True)
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
        print filters, "FILTERSSSSSSSSSSSSSS"
        return render(request, "pedidosCliente.html",
                      {"pedidos": pedidos,
                       "filtros": filters,
                       "clientes":clientes,
                       "totales":totales})




@login_required()
@permission_required('recetas.add_pedidocliente')
def pedidosClientesAlta(request, tipo_pedido_id):
    '''Procesa el alta de un pedido segun su tipo (fijo,de cambio u ocacional).
       Llama a funciones que verifican mediante formularios que los datos cargados para el alta sean correctos
    '''
    detalles_form_class = formset_factory(forms.PedidoClienteDetalleForm)
    detalles_form = None
    pedidosClientes_form = None
    productosTerminados = models.ProductoTerminado.objects.filter(activo=True)
    if tipo_pedido_id == "1":
        pedidosClientes_form = forms.PedidoClienteFijoForm
    elif tipo_pedido_id == "2":
        pedidosClientes_form = forms.PedidoClienteOcacionalForm

    elif tipo_pedido_id == "3":
        pedidosClientes_form = forms.PedidoClienteCambioForm

    if request.method == "POST":
        pedidosClientes_form = pedidosClientes_form(request.POST) #crea formulario de receta cono los datos del post
        detalles_form = detalles_form_class(request.POST, request.FILES)
        if  pedidosClientes_form.is_valid():
            if tipo_pedido_id == "1":
                dias = pedidosClientes_form.cleaned_data.get('dias')    #agregado por lo que decia un foro wtf
            pedido_instancia =  pedidosClientes_form.save(commit = False) #commit false
            if detalles_form.is_valid():
                pedido_instancia.tipo_pedido=tipo_pedido_id
                print pedido_instancia
                pedido_instancia.save()
                for detalle in detalles_form:
                    detalle_instancia = detalle.save(commit=False)
                    detalle_instancia.pedido_cliente = pedido_instancia
                    detalle_instancia.save()
                messages.success(request, 'El pedido: ' + pedido_instancia.get_tipo_pedido_display() + ', ha sido registrada correctamente.')

                return redirect('pedidosCliente')
        # se lo paso todo a la pagina para que muestre cuales fueron los errores.
    return render(request, "pedidosClienteAlta.html", {
                "productosTerminados":productosTerminados,
                "pedido_form":  pedidosClientes_form,
                "detalles_form_factory": detalles_form or detalles_form_class(),
                "tipo_pedido": tipo_pedido_id})




@login_required()
@permission_required('recetas.delete_pedidocliente')
def pedidosClienteBaja(request,pedido_id):
    ''' Realiza una "baja logica" de un pedido previamente seleccionado, el cual no se tendra en cuanta
        para realizar las hojas de ruta porque no estara mas vigente
    '''
    print "en bajaaaaaaaaaaa"
    pedido = models.PedidoCliente.objects.get(pk=pedido_id)
    messages.success(request, 'El pedido: de '+pedido.cliente.razon_social + ', ha sido eliminada correctamente.')
    pedido.activo=False
    pedido.save()
    return redirect('pedidosCliente')




@login_required()
@permission_required('recetas.change_pedidocliente')
def pedidosClienteModificar(request, pedido_id):
    ''' Procesa la modificacion de un pedido previamente seleccionado, mostrando el pedido y permitiendo
        modificar los atributos permitidos. Mediante formularios realiza las validaciones de los nuevos datos
        del pedido.
    '''
    detalles_formset=None
    error = False
    pedido_instancia = get_object_or_404(models.PedidoCliente, pk=pedido_id)
    detalles_inlinefactory = inlineformset_factory(models.PedidoCliente,models.PedidoClienteDetalle,fields=('cantidad_producto','producto_terminado','pedido_cliente'))
    if pedido_instancia.tipo_pedido == 1:
        pedido_instancia = get_object_or_404(models.PedidoFijo, pk=pedido_id)
        pedidosClientes_form = forms.PedidoClienteFijoForm
    elif pedido_instancia.tipo_pedido == 2:
        pedido_instancia = get_object_or_404(models.PedidoOcacional, pk=pedido_id)
        pedidosClientes_form = forms.PedidoClienteOcacionalForm
    else:
        pedido_instancia = get_object_or_404(models.PedidoCambio, pk=pedido_id)
        pedidosClientes_form = forms.PedidoClienteCambioForm
    detalles_instancias = models.PedidoClienteDetalle.objects.filter(pedido_cliente = pedido_instancia)
    pedidosClientes_form = pedidosClientes_form(instance= pedido_instancia)
    productos = models.ProductoTerminado.objects.filter(activo=True) #para detalles

    if request.method=="POST":
        detalles_formset = detalles_inlinefactory(request.POST,request.FILES,prefix='pedidoclientedetalle_set',instance=pedido_instancia)
        if pedido_instancia.tipo_pedido == 1:
            pedidosClientes_form = forms.PedidoClienteFijoForm(request.POST,instance= pedido_instancia,my_arg = pedido_id)
            fecha_posta = pedido_instancia.fecha_inicio
        elif pedido_instancia.tipo_pedido == 2:
            pedidosClientes_form = forms.PedidoClienteOcacionalForm(request.POST,instance= pedido_instancia,my_arg = pedido_id)
        else:
            pedidosClientes_form = forms.PedidoClienteCambioForm(request.POST,instance= pedido_instancia,my_arg = pedido_id)
        if pedidosClientes_form.is_valid():
            pedido_instancia = pedidosClientes_form.save(commit=False)
            if pedido_instancia.tipo_pedido == 1:
                if pedido_instancia.fecha_inicio != fecha_posta: #solo si modifico la fecha inicio debo verificar que sea maor al dia actual
                    if pedido_instancia.fecha_inicio < datetime.date.today():
                        pedido_instancia.fecha_inicio = fecha_posta
                        pedido_instancia.save()
                        messages.error(request, 'La fecha inicio nueva no puede ser anterior al dia actual')
                        return redirect('/pedidosCliente/Modificar/'+pedido_id)
            #DETALLES
            print detalles_formset.is_valid()
            if detalles_formset.is_valid():
                detalles_formset.save()
                messages.success(request, 'El pedido: ' + pedido_instancia.get_tipo_pedido_display()+" de "+pedido_instancia.cliente.razon_social + ', ha sido modificada correctamente.')
                pedido_instancia.save()
                return redirect('pedidosCliente')
        else:
            error=True
    #si el form no es valido, le mando todo al html para que muestre los errores#
    pref = "pedidoclientedetalle_set" #pedidoclientedetalle_set
    return render(request,"pedidosClienteModificar.html",{"pedido_form":pedidosClientes_form,"id":pedido_id,
                                                   "detalles_pedido":detalles_instancias,
                                                   "productos":productos,
                                                   "detalles_form_factory":detalles_formset or detalles_inlinefactory(initial=list(detalles_instancias.values()), prefix='pedidoclientedetalle_set'),
                                                   "pedido_id":pedido_id,
                                                   "pref":pref,
                                                   "tipo_pedido":pedido_instancia.tipo_pedido,
                                                    "id_cliente":pedido_instancia.cliente.id,
                                                    "error":error

                                                   })



#********************************************************#
         #    P E D I D O S   A   P R O V E E D O R   #
#********************************************************#
@login_required()
@permission_required('recetas.add_pedidoproveedor')
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



#if pedido_proveedor_instancia.fecha_realizacion > datetime.date.today():
             #   messages.error(request, 'la fecha de realizacion no debe ser superior a la fecha actual.')
                #return redirect('pedidosProveedorAlta')

@login_required()
@permission_required('recetas.add_pedidoproveedor')
def pedidosProveedorAlta(request):
    detalles_form_class = formset_factory(forms.DetallePedidoProveedorForm)
    detalles_form = None
    pedido_proveedor_form = None
    insumos = models.Insumo.objects.filter(activo=True)
    if request.method == "POST":
        pedido_proveedor_form = forms.PedidoProveedorAltaForm(request.POST) #crea formulario de pedido con los datos del post
        if pedido_proveedor_form.is_valid():
            pedido_proveedor_instancia = pedido_proveedor_form.save(commit = False) #commit false
            detalles_form = detalles_form_class(request.POST, request.FILES)
            if pedido_proveedor_instancia.fecha_realizacion > datetime.date.today():
                messages.error(request, 'la fecha de realizacion no debe ser superior a la fecha actual.')
                return redirect('pedidosProveedorAlta')
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
            insumos = proveedor.insumos.filter()
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




@login_required()
@permission_required('recetas.change_pedidoproveedor')
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






@login_required()
@permission_required('recetas.change_pedidoproveedor')
def pedidosProveedorRecepcionar(request,pedido_id):
    pedido_proveedor_instancia = get_object_or_404(models.PedidoProveedor, pk=pedido_id)
    proveedor = models.Proveedor.objects.get(pk=pedido_proveedor_instancia.proveedor.id)
    if request.method == "POST":
        pedido_proveedor_form = forms.PedidoProveedorRecepcionarForm(request.POST, instance=pedido_proveedor_instancia)
        if pedido_proveedor_form.is_valid():
            #pedido_proveedor_instancia.fecha_de_entrega = date.today()
            #if pedido_proveedor_instancia.fecha_de_entrega < pedido_proveedor_instancia.fecha_realizacion:
            fecha_de_hoy = datetime.date.today()
            if pedido_proveedor_instancia.fecha_de_entrega < pedido_proveedor_instancia.fecha_realizacion or pedido_proveedor_instancia.fecha_de_entrega>fecha_de_hoy:
                messages.error(request, 'Problema de Fechas: La fecha de entrega debe estar entre la fecha de realizacion y la fecha de hoy')
                return render(request,"pedidosProveedorRecepcionar.html",{
                "pedido_proveedor_form":pedido_proveedor_form,
                "proveedor":proveedor,
                "pedido_id":pedido_id,
                "pedido":pedido_proveedor_instancia })
            pedido_proveedor_instancia.estado_pedido = 2
            pedido_proveedor_instancia.save()
            for detalle in pedido_proveedor_instancia.detallepedidoproveedor_set.all():
                print detalle.insumo.stock, "ANTES"
                detalle.insumo.stock +=detalle.cantidad_insumo
                detalle.insumo.save()
                print detalle.insumo.stock
            messages.success(request, 'El Pedido ha sido recepcionado correctamente.')
            return redirect('pedidosProveedor')
    else:
        pedido_proveedor_form = forms.PedidoProveedorRecepcionarForm(instance=pedido_proveedor_instancia)

    return render(request,"pedidosProveedorRecepcionar.html",{
        "pedido_proveedor_form":pedido_proveedor_form,
        "proveedor":proveedor,
        "pedido_id":pedido_id,
        "pedido":pedido_proveedor_instancia })

#la idea es que en proveedorRepecionar se recpcione y actualice el stock
#poner un boton de cancelar, para cancelar el pedio






@login_required()
@permission_required('recetas.add_pedidoproveedor')
@csrf_exempt
def pedidosProveedorBaja(request,pedido_id =None):
    print "estoy en bajaaa"
    p = models.PedidoProveedor.objects.get(pk=pedido_id)
    messages.success(request, 'El pedido realizado en la fecha: ' + p.fecha_realizacion.strftime('%d/%m/%Y') + ', realizado al proveedor: ' + p.proveedor.razon_social +', ha sido eliminado correctamente.')
    p.delete()
    return redirect('pedidosProveedor')






@login_required()
@permission_required('recetas.change_pedidoproveedor')
def pedidosProveedorCancelar(request,pedido_id =None):
    print "estoy en cancelar pedido..."
    p = models.PedidoProveedor.objects.get(pk=pedido_id)
    p.estado_pedido = 3
    p.fecha_cancelacion = date.today()
    p.save()
    print(p.estado_pedido)
    print(p.fecha_cancelacion)
    messages.success(request, 'El pedido realizado en la fecha: ' + p.fecha_realizacion.strftime('%d/%m/%Y') + ', realizado al proveedor: ' + p.proveedor.razon_social +', ha sido cancelado correctamente.')
    return redirect('pedidosProveedor')

#********************************************************#
         #    L O T E S   #
#********************************************************#
@login_required()
@permission_required('recetas.add_lote')
def lotes(request,lote_id=None):
    if lote_id is not None:
        #consulta
        lote = models.Lote.objects.get(pk=lote_id)
        return render(request,"lotesConsulta.html",{"lote":lote})
    else:
        # filtros
        filters, mfilters = get_filtros(request.GET, models.Lote)
        print "por aplicar filtros",filters,mfilters

        lotes= models.Lote.objects.filter(**mfilters)
    productos = models.ProductoTerminado.objects.filter(activo=True)
    return render(request,"recetas/lotes.html",{"lotes":lotes,"productos":productos})





@login_required()
@permission_required('recetas.change_lote')
def lotesModificar(request,lote_id=None):
    lote_instancia = models.Lote.objects.get(pk=lote_id)
    return render(request,"lotesModificar.html",{"lote_form_modificar":forms.LoteForm() ,"lote_instancia":lote_instancia,"id":lote_id})







@login_required()
@permission_required('recetas.add_lote')
def lotesAlta(request):
    if request.method == "POST":
        lote_form = forms.LoteForm(request.POST)
        if lote_form.is_valid():
            lote = lote_form.save(commit = False)
            print "MIRAR ESTO"
            print lote.producto_terminado, lote.pk
            lote.stock_disponible = lote.cantidad_producida #stock inicial
            #lote.save()
            # actualizo stock del producto
            lote.producto_terminado.stock +=  lote.stock_disponible
            #lote.producto_terminado.save()
            # disminuye stock de insumos
            try:
                receta = lote.producto_terminado.receta_set.get()
                print receta ,"receeeeee"
                cant__producida= lote.cantidad_producida
                detalles_receta = receta.recetadetalle_set.all()
                for detalle_receta in  detalles_receta:
                    cant_decrementar =(detalle_receta.cantidad_insumo * cant__producida) / receta.cant_prod_terminado
                    detalle_receta.insumo.decrementar(cant_decrementar)
                    if detalle_receta.insumo.stock < 0:
                        messages.error(request, 'No se puede dar de alta el Lote. El insumo %s no tiene stock, faltan:  %d %s'%(detalle_receta.insumo,(detalle_receta.insumo.stock * -1),detalle_receta.insumo.get_unidad_medida_display()))
                        return render(request,"lotesAlta.html",{"lote_form":lote_form}) 
                    else:
                        messages.success(request, 'Se decrementaron %d %s de %s '%(cant_decrementar,detalle_receta.insumo.get_unidad_medida_display(),detalle_receta.insumo.nombre))
                        print "LOTEEE", lote.pk, "___",lote.fecha_produccion

                        lote.save()
                        lote.producto_terminado.save()
                        detalle_receta.insumo.save()
            except:
                messages.error(request, 'No se creo el Lote ya que no hay receta asociada al Producto')
                print "asasdsadas--------"
                print lote.pk
                return render(request,"lotesAlta.html",{"lote_form":lote_form}) #

            return redirect("lotes")
    else:
        lote_form=forms.LoteForm()
    return render(request,"lotesAlta.html",{"lote_form":lote_form})






@login_required()
def loteStock(request,lote_id):
    ''' Recibe un lote y procesa la carga de un formulario para setear un decremento en su stock debido
        a una perdida (por vencimiento, rotura u otros)
    '''
    lote_instancia = models.Lote.objects.get(pk = lote_id)
    if request.method == "POST":
        lote_form = forms.LoteStockForm(request.POST,instance=lote_instancia)
        if lote_form.is_valid():
            lote_form.save(lote_instancia)
            return redirect("lotes")
    else:
        lote_form = forms.LoteStockForm(instance = lote_instancia)

    return render(request,"ModificarStockProducto.html",{"lote_form":lote_form,
                                                         "lote": lote_instancia,
                                                         "id":lote_id})




#********************************************************#
         #    H O J A   D E  R U T A    #
#********************************************************#
@login_required()
def hojaDeRuta(request):
        #eliminarVencidos()
        pedidos_clientes = []
        pedidos_fijos = models.PedidoFijo.objects.all()
        pedidos_ocacionales = models.PedidoOcacional.objects.all()
        pedidos_cambio = models.PedidoCambio.objects.all()
        hojaDeRuta_form = forms.HojaDeRutaForm()
        pedidos_clientes= chain(models.PedidoFijo.objects.filter(activo=True), models.PedidoOcacional.objects.filter(activo=True),models.PedidoCambio.objects.filter(activo=True))
        pedidos_clientes_enviar = []
        pedidos_ya_cargados = []
        hojas_de_ruta=models.HojaDeRuta.objects.filter(fecha_creacion=date.today())
        for hoja in hojas_de_ruta:
            entregas=hoja.entrega_set.all()
            for entrega in entregas:
                pedidos_ya_cargados.append(entrega.pedido.id)
        for pedido in pedidos_clientes:
            if pedido.esParaHoy() and (pedido.id not in pedidos_ya_cargados):
                if(pedido.cliente.es_moroso == True):
                    messages.error(request, 'El pedido para el cliente '+pedido.cliente.razon_social+' no se puede enviar porque es moroso.')
                    continue    
                pedidos_clientes_enviar.append(pedido)
        choferes = models.Chofer.objects.filter(activo=True)
        #choferes = models.Chofer.objects.filter(disponible=True)
        productos = models.ProductoTerminado.objects.filter(activo=True)
        extras_factory_class = formset_factory(forms.ProductosLlevadosForm)
        entregas_factory_class = formset_factory(forms.EntregaForm)
        print productos,choferes, "EEEEEEEEEEEEEEEEEEEEEEEEE"
        return render(request, "hojaDeRuta.html/",{"hojaDeRuta_form": hojaDeRuta_form,
                                                  "pedidos":pedidos_clientes_enviar,
                                                  "choferes":choferes,
                                                  "productos":productos,
                                                  "fecha":datetime.date.today(),
                                                  "extras_form_factory":extras_factory_class(prefix="productos_totales"),
                                                  "prefix_extras": "productos_totales",
                                                  "entregas_form_factory":entregas_factory_class(prefix = "entregas"),
                                                  "prefix_entregas":"entregas"})





@login_required()
@permission_required('recetas.add_hojaderuta')
def hojaDeRutaAlta(request):
     
    hoja_form = forms.HojaDeRutaForm(request.POST)
    if hoja_form.is_valid():
        hoja_ruta_instancia = hoja_form.save()
        entregas_factory =  forms.EntregaFormsetClass(request.POST,request.FILES,prefix="entregas")
        prod_llevados_factory = forms.ProductoLlevadoFormsetClass(request.POST,request.FILES,prefix="productos_totales")
        for p_llevado in prod_llevados_factory:
            if p_llevado.is_valid():
                 p_llevado.save(hoja_ruta_instancia)
            #print "ERRORES ",p_llevado.errors.as_data()
        if hoja_ruta_instancia.tiene_algun_producto():
            if  entregas_factory.is_valid():
                for e in entregas_factory:
                    entrega_instancia= e.save(hoja_ruta_instancia)
                    if entrega_instancia.pedido.tipo_pedido == 2 or entrega_instancia.pedido.tipo_pedido == 3:
                        entrega_instancia.pedido.activo=False #marco como entregado
                        entrega_instancia.pedido.save()
            else:
                for form in entregas_factory:
                    for k,error in form.errors.items():
                        print "error ",error
                        messages.error(request,error)                
                return redirect("hojaDeRuta/")
        else:
            hoja_ruta_instancia.delete()
            messages.error(request, 'No se pudo registrar la Hoja de Ruta ya que No hay productos para llevar')
            return redirect("hojaDeRuta/")

    return redirect("HojaDeRutaMostrar/",hoja_ruta_instancia.pk)







@login_required()
def HojaDeRutaMostrar(request,hoja_id):
    hoja = models.HojaDeRuta.objects.get(pk=hoja_id)
    return render(request,"HojaDeRutaMostrar.html/",{"hoja_ruta":hoja})





@login_required()
def generarTotales(request):
    pedidos_list = re.findall("\d+",request.GET['pedidos'])
    totales={}
    nombres={}
    pedidos = []
    for id in pedidos_list:
        pedidos.append(models.PedidoCliente.objects.get(pk=id))
    for pedido in pedidos:
        for producto in pedido.productos.all():
            if producto.pk in totales:
                totales[producto.pk]=totales[producto.pk]+producto.pedidoclientedetalle_set.all().get(pedido_cliente=pedido).cantidad_producto
                nombres[producto.pk] = "%s" % producto
            else:
                totales[producto.pk]=0
                totales[producto.pk]=totales[producto.pk]+producto.pedidoclientedetalle_set.all().get(pedido_cliente=pedido).cantidad_producto
                nombres[producto.pk] = "%s" % producto
    print "EN GENERAR TOTALES: totales: ",totales, "datos: ",nombres
    return HttpResponse(json.dumps({ "totales": totales, "datos": nombres   }),content_type='json')






@login_required()
def rendicionReparto(request,hoja_id=None):
    print "EN RENDICION", hoja_id
    hoja = models.HojaDeRuta.objects.get(pk=hoja_id)    
    prefix_detalles_entregas = "entregas"
    prefix_prod_llevados = "prod_llevados"
    detalles_formset = forms.EntregaDetalleFormset(prefix=prefix_detalles_entregas)
    prod_llevados_formset = forms.ProdLlevadoFormset_class(prefix=prefix_prod_llevados)        
    if request.method == "POST":
        print "vino post"
        # E n t r e g a s
        detalles_formset = forms.EntregaDetalleFormset(request.POST,request.FILES,prefix=prefix_detalles_entregas)
        if detalles_formset.is_valid():
            for det_form in  detalles_formset:
                det_form.save()
            #  P r o d u c t o s   L l e v a d o s
            prod_llevados_forms = forms.ProdLlevadoFormset_class(request.POST,request.FILES,prefix=prefix_prod_llevados)
            if prod_llevados_forms.is_valid():
                for prod_llevado_form in prod_llevados_forms:
                    prod_llevado_form.save()
                hoja.rendida = True
                chofer = models.Chofer.objects.filter(pk=hoja.chofer.id)
                chofer=chofer[0]
                #chofer.disponible=True
                chofer.save()
                hoja.save()
                print "guarde la hgoja"
            return redirect("rendicionDeRepartoMostrar/",hoja.id)
    return render(request,"rendicionDeReparto.html/",{"hoja":hoja,
                                                     "detalles_factory":detalles_formset,
                                                     "prefix":prefix_detalles_entregas,
                                                     "prod_llevados_factory":prod_llevados_formset,
                                                     "prefix_prod_llevados":prefix_prod_llevados
                                                     })



@login_required()
def rendicionHojasDeRutasSinCobrar(request):
    ''' Devuelve todas las hojas de ruta ya rendidas pero que no fueron cobradas en el momento de la recepcion.
    '''
    print "EN REND SIN COBRARRRR"

    hojas = models.HojaDeRuta.objects.filter(rendida=True,pagado=False) 
    print hojas
    return render(request,"rendicionHojasDeRutasSinCobrar.html/",{"hojas":hojas})



@login_required()
def RendicionDeRepartoMostrar(request,hoja_id):
    print "EN RENDICION REPARTO MOSTRAR VIEWW"
    hoja = models.HojaDeRuta.objects.get(pk = hoja_id)
    cobros_form = forms.CobroEntregaRendirFormsetClass(prefix="cobros")
    if request.method == "POST":
        cobros_form = forms.CobroEntregaRendirFormsetClass(request.POST,request.FILES,prefix="cobros")
        if cobros_form.is_valid():
            print "COBROS FORM SON VALIDOS"
            for form in cobros_form:
                if form.is_valid():
                    form.save()
                else:
                    print "el formulario solo no es valido"
            messages.success(request,"Se registraron correctamente los pagos de las entregas")
            hoja.pagado = True   #registro como hoja de ruta ya cobrada en la recepcion
            hoja.save()
            return redirect('index')
        else:
            print "el factory no es valido"
            print "context"

            print request.session
            return render_to_response('rendicionDeRepartoMostrar.html/',
                                    {"hoja":hoja,
                                    "cobros_factory":cobros_form,
                                    "prefix_cobros":"cobros"}, 
                                    context_instance=RequestContext(request))

          
    return render(request,"rendicionDeRepartoMostrar.html/",{"hoja":hoja,
                                                            "cobros_factory":cobros_form,
                                                            "prefix_cobros":"cobros"})



@login_required()
def rendicionHojasDeRutas(request):
    hojas = models.HojaDeRuta.objects.filter(rendida=False) #a futuro filtrar por hojas de rutas no rendidas
    print hojas
    return render(request,"rendicionHojasDeRutas.html/",{"hojas":hojas})


#********************************************************#
         #    P D F    #
#********************************************************#
def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return HttpResponse('We had some errors<pre>%s</pre>' % html)



@login_required()
def HojaDeRutaPdf(request,hoja_id=None):
    hoja = models.HojaDeRuta.objects.get(pk=hoja_id) #tengo q buscar la hoja q resiba por parametro
    print "hoja de ruta a mostrar ",hoja.id
    fecha = hoja.fecha_creacion
    return render_to_pdf('PDFs/HojaDeRutaPdf.html',{'pagesize':'A4',
                                                   'hoja': hoja,
                                                   'date': fecha,
            }
        )



@login_required()
def LotesHojaRutaPdf(request,hoja_id=None):
    hoja = models.HojaDeRuta.objects.get(pk=hoja_id)
    return render_to_pdf('PDFs/LoteHojaRutaPdf.html',{'pagesize':'A4',
                                                   'hoja': hoja,
            }
        )



#********************************************************#
         #    COBRAR CLIENTE  #
#********************************************************#



@login_required()
def cobrarClienteFiltrado(request,cliente_id=None):
# Busca todas las entregas de un cliente que no hayan sido abonadas completamente
# Devuelve esas entregas y el monto total que adeuda
    entregas_no_facturadas = []
    cliente=models.Cliente.objects.get(pk=(cliente_id))
    entregas = models.Entrega.objects.filter(pedido__cliente=cliente)
    saldo = 0
    for entrega in entregas:
        if entrega.pedido.tipo_pedido == 3:    #si el pedido es de cambio no se cobra
            continue
        if entrega.factura == None and entrega.monto_total() > 0:
            entregas_no_facturadas.append(entrega)
            saldo += entrega.monto_restante()
    clientes = models.Cliente.objects.all()
    #las deudas se saldan comenzando por las mas antiguas.
    entregas_no_facturadas = sorted(entregas_no_facturadas, key=lambda entrega: entrega.fecha)
    print entregas_no_facturadas,"saldoo", saldo
    return render(request, "cobrarCliente.html", {"entregas":entregas_no_facturadas,"cliente":cliente,"clientes":clientes,"saldo":saldo})




@login_required()
def cobrarCliente(request):
    clientes = models.Cliente.objects.all()
    return render(request, "cobrarCliente.html", {"entregas":[],"clientes":clientes,"saldo":-1})



@login_required()
def cobrarClienteClasificar(request):
    ''' Recibe las entregas no facturadas del cliente seleccionado, y las separa para cobrar con factura o con recibos
        Devuelve dos listados de entregas, una para facturacion y otra para recibo.
    ''' 
    entregas = re.findall("\d+",request.GET['entregas'])
    mont = re.findall("\S+",request.GET['monto'])
    monto = re.sub('["]', '', mont[0])
    monto=monto.replace(',', '.')
    monto=Decimal(monto)
    entregas_para_factura = {}
    entregas_para_recibo={}
    monto_recibo = 0
    monto_ingresado = monto
    for entrega_id in entregas:
        entrega = models.Entrega.objects.get(pk=entrega_id)
        if monto == 0:
            break
        if entrega.monto_restante() > monto:
            entregas_para_recibo[entrega_id]="%s" % entrega.fecha
            monto_recibo = "%s" % monto
            break
        else:
            entregas_para_factura[entrega_id]="%s" % entrega.fecha
        monto -= entrega.monto_restante()
    monto_factura = monto_ingresado - Decimal(monto_recibo)
    for entrega_id in entregas_para_factura: #verifico si las entregas a facturar tenian pagos en recibos para sumarlo al monto de la factura
        entrega = models.Entrega.objects.get(pk=entrega_id)
        recibos_de_entrega = entrega.recibo_set.all()
        for recibo in recibos_de_entrega:
            monto_factura += recibo.monto_pagado
    return HttpResponse(json.dumps({"para_facturas": entregas_para_factura,"para_recibo": entregas_para_recibo,"monto_recibo":monto_recibo, "monto_factura":str(monto_factura)}),content_type='json')



@login_required()
def cobrarClienteFacturar(request):
    ''' Realiza el seteo de los cobros con factura o con recibos, segun corresponde.
        Si se realiza un cobro con factura, el monto de esa factura incluye los recibos realizados
        con anterioridad, si es que lo tuvieran.
    '''
    para_factura = re.findall("\d+",request.GET['para_facturas'])
    para_recibo = re.findall("\d+",request.GET['para_recibo'])
    monto_recibo = re.findall("\S+",request.GET['monto_recibo'])
    monto_factura = re.findall("\S+",request.GET['monto_factura'])
    num_factura = re.findall("\d+",request.GET['num_factura'])
    num_recibo = re.findall("\d+",request.GET['num_recibo'])
    cliente=None
    if len(para_factura) != 0:
        monto_factura = re.sub('["]', '', monto_factura[0])
        monto_factura=Decimal(monto_factura)
        entrega = models.Entrega.objects.get(pk=para_factura[0]) #para obtener el saldo del cliente
        cliente=entrega.pedido.cliente
        cliente.saldo -=float(monto_factura)
    if len(para_recibo) != 0:
        monto_recibo = re.sub('["]', '', monto_recibo[0])
        monto_recibo=Decimal(monto_recibo)
        if cliente==None:
            entrega = models.Entrega.objects.get(pk=para_recibo[0])
            cliente=entrega.pedido.cliente
        cliente.saldo -=float(monto_recibo)
    cliente.save()
    if len(num_factura) !=0:
        num_factura = int(num_factura[0])
    if len(num_recibo) !=0:
        num_recibo = int(num_recibo[0])
    print para_factura," ",para_recibo," ",monto_recibo," ",monto_factura," ",num_factura," ",num_recibo
    for id_entrega in para_factura:
        entrega = models.Entrega.objects.get(pk=id_entrega)
        entrega.cobrar_con_factura(monto_factura,(num_factura))
    for id_entrega in para_recibo:
        entrega = models.Entrega.objects.get(pk=id_entrega)
        entrega.cobrar_con_recibo(monto_recibo,(num_recibo))
        

    messages.success(request, 'Pago realizado correctamente.')
    return HttpResponse(json.dumps("ok"),content_type='json')



def getFacturas(request): 

    num_factura = int(request.GET['factura'])
    try:
        factura = models.Factura.objects.get(numero=num_factura)
        factura=1
    except:
        factura=0 #si no existe el factura
    print factura
    return HttpResponse(json.dumps(factura), content_type='json')


def getRecibos(request): 
    num_recibo = int(request.GET['recibo'])
    try:
        recibo = models.Recibo.objects.get(numero=num_recibo)
        recibo=1
    except:
        recibo=0 #si no existe el recibo
    print recibo
    #json.dumps(recibo)
    print recibo
    return HttpResponse(json.dumps(recibo), content_type='json')




@login_required()
def cobrarClienteMostrarRecibos(request):
        ''' Devuelve una lista con los recibos de una entrega
        '''
        entrega_id = re.findall("\d+",request.GET['entrega_id'])
        entrega = models.Entrega.objects.get(pk=entrega_id[0])
        recibos = models.Recibo.objects.filter(entrega=entrega)
        print recibos," estos son los recibos"
        recibos=serializers.serialize('json', recibos) #en javascript se lo puede manejar como objetos
        return HttpResponse(recibos,content_type='json')


@login_required()
def perdidasStockLotes(request):
    ''' Devuelve las instancias de perdida de Stock segun criterios de filtracion para listarlos
    '''
    filters, mfilters = get_filtros(request.GET, models.PerdidaStock)
    perdidas = models.PerdidaStock.objects.filter(**mfilters)
    return render(request, "perdidasStockLotes.html", {"perdidas":perdidas})



@login_required()
def productosMasVendidos(request):
    import os
    from pylab import *    
    #  I M A G E N
    figure(1, figsize=(8,8))# tamanio de figura
    ax = axes([0, 0, 0.9, 0.9])# donde esta la figura ancho alto etc..
    labels = 'Fideo Verde ', 'Fideo Negro'
    fracs = [12,33]#datos a graficar
    explode=(0, 0.1)#exposicion de uno de los datos segun donde se encuentra 
    pie(fracs, explode=explode,labels=labels, autopct='%10.0f%%', shadow=True)
    legend()
    title('Productos Mas Vendidos', bbox={'facecolor':'0.8', 'pad':5})
    savefig("a.png")
    response = HttpResponse(content_type='image/png')
    savefig(response,format='PNG')
    return response

def pdfGuia(request):
    with open(' static "/documentacion" ', 'r') as pdf:
        response = HttpResponse(pdf.read(), mimetype='application/pdf')
        response['Content-Disposition'] = 'inline;filename=Guia-v2.pdf'
        return response
    pdf.closed
