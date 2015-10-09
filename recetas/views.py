from django.shortcuts import render, redirect
from . import models
from . import forms
from django.forms.formsets import formset_factory
from django.shortcuts import get_object_or_404
from django.forms.models import BaseModelFormSet
from django.forms.models import modelformset_factory
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def get_order(get):
    if "o" in get:
        return get["o"]

def get_filtros(get, modelo):
    mfilter = {}
    for filtro in modelo.FILTROS:
        attr = filtro.split("__")[0]
        if attr in get and get[attr]:
            mfilter[filtro] = get[attr]
            mfilter[attr] = get[attr]
    return mfilter

#********************************************************#
               #     I N S U M O S    #
#********************************************************#

def insumos(request,insumo_id=None):
    print "INSUMOS PRINCIPAL"
    if insumo_id is not None:
        # consulta
        insumo_instancia = models.Insumo.objects.get(pk=insumo_id)
        insumo_form = forms.InsumoForm(instance= insumo_instancia)
        return render(request, "insumosConsulta.html",{"insumo_form": insumo_form})
    elif request.method == 'GET':
        # filtros
        filters = get_filtros(request.GET, models.Insumo)
        mfilters = dict(filter(lambda v: v[0] in models.Insumo.FILTROS, filters.items()))
        insumos = models.Insumo.objects.filter(**mfilters)
        return render(request, "recetas/insumos.html",
                  {"insumos": insumos,
                   "filtros": filters})


def insumosAlta(request):
    print "INSUMOS ALTA"

    if request.method == "POST":
        insumo_form = forms.InsumoForm(request.POST)
        if insumo_form.is_valid():
            insumo_form.save()
            return redirect('insumos')
    else:
        insumo_form = forms.InsumoForm()
    return render(request, "insumosAlta.html", {"insumo_form":insumo_form})


def insumosModificar(request,insumo_id =None): #zona id nunca va a ser none D:
    print "INSUMOS MODIFICAR"

    insumo_instancia = get_object_or_404(models.Insumo, pk=insumo_id)
    if request.method=="POST":
        insumo_form = forms.InsumoForm(request.POST,instance= insumo_instancia)
        if insumo_form.is_valid():
            insumo_form.save()
        return redirect('insumos')
    else:
        insumo_form = forms.InsumoForm(instance= insumo_instancia)
        return render(request,"insumosModificar.html",{"insumo_form":insumo_form,"id":insumo_id})








#********************************************************#
               #     R E C E T A S    #
#********************************************************#
"""
def recetas(request,receta_id=None):

    if receta_id is not None:
        r = models.Receta.objects.get(pk=receta_id)
        i = r.insumos.all()
        return render(request, "recetasConsulta.html",{"receta": r,"insumos":i})
    filters = get_filtros(request.GET, models.Receta)
    mfilters = dict(filter(lambda v: v[0] in models.Receta.FILTROS, filters.items()))
    recetas = models.Receta.objects.filter(**mfilters)
    detalles_form_class = formset_factory(forms.RecetaDetalleForm)
    detalles_form = None
    receta_form = None
    if request.method == "POST":
        receta_form = forms.RecetaForm(request.POST) #crea formulario de receta cno los datos del post
        if receta_form.is_valid():
            receta_instancia = receta_form.save() #commit false
            detalles_form = detalles_form_class(request.POST, request.FILES)
            if detalles_form.is_valid():
                #detalles = detalles_form.save(commit=False)
                #receta.save()
                for detalle in detalles_form:
                    detalle_instancia = detalle.save(commit=False)
                    detalle_instancia.receta = receta_instancia
                    detalle_instancia.save()
                return redirect('recetas')

    insumos = models.Insumo.objects.all()
    return render(request, "recetas/recetas.html", {
        "recetas": recetas,
        "receta_form": receta_form or forms.RecetaForm(),
        "detalles_form_factory": detalles_form or detalles_form_class(),
        "modal": request.method == "POST",
        "insumos":insumos})

"""
def recetas(request,receta_id=None):
    print "PRINCIPAL"
    if receta_id is not None:
        # consulta
        receta = models.Receta.objects.get(pk=receta_id)
        insumos = receta.insumos.all()
        return render(request, "recetasConsulta.html",{"receta": receta,"insumos":insumos})
    elif request.method == 'GET':
        # filtros
        filters = get_filtros(request.GET, models.Receta)
        mfilters = dict(filter(lambda v: v[0] in models.Receta.FILTROS, filters.items()))
        recetas = models.Receta.objects.filter(**mfilters)
        productos_terminados= models.ProductoTerminado.objects.all()
        return render(request, "recetas/recetas.html",
                      {"recetas": recetas,
                       "filtros": filters,
                       "productos_terminados":productos_terminados})



def recetasModificar(request,receta_id):

    receta_instancia = get_object_or_404(models.Receta, pk=receta_id)
    detalles_form_factory = formset_factory(forms.RecetaDetalleForm)

    if request.method=="POST":
        receta_form = forms.RecetaForm(request.POST,instance= receta_instancia)
        if receta_form.is_valid():
            receta_form.save()
        return redirect('recetas')
    else:
        receta_form = forms.RecetaForm(instance= receta_instancia)
        detaless = models.RecetaDetalle.objects.filter(receta = receta_instancia)
        detalles_formset = detalles_form_factory()
        return render(request,"recetasModificar.html",{"receta_form":receta_form,"id":receta_id,"detalles_formset":detalles_formset})

    # FIN BORRADOR




def recetasAlta(request):
    detalles_form_class = formset_factory(forms.RecetaDetalleForm)
    detalles_form = None
    receta_form = None
    if request.method == "POST":
        receta_form = forms.RecetaForm(request.POST) #crea formulario de receta cno los datos del post
        if receta_form.is_valid():
            receta_instancia = receta_form.save() #commit false
            detalles_form = detalles_form_class(request.POST, request.FILES)
            if detalles_form.is_valid():
                #detalles = detalles_form.save(commit=False)
                #receta.save()
                for detalle in detalles_form:
                    detalle_instancia = detalle.save(commit=False)
                    detalle_instancia.receta = receta_instancia
                    detalle_instancia.save()
                return redirect('recetas')
    else:
        insumos = models.Insumo.objects.all()
        return render(request, "recetasAlta.html", {
            "insumos":insumos,
            "receta_form": receta_form or forms.RecetaForm(),
            "detalles_form_factory": detalles_form or detalles_form_class()})
    return redirect('recetas')




#********************************************************#
               #     P R O V E E D O R E S   #
#********************************************************#


def proveedores(request,proveedor_id=None):
    print "soy prinsipa",proveedor_id

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
    if request.method == "POST":
        proveedores_form = forms.ProveedorForm(request.POST)
        if proveedores_form.is_valid():
            proveedores_form.save()
            return redirect('proveedores')
    else:
        proveedores_form = forms.ProveedorForm()
        #recetas = models.Receta.objects.all()
        return render(request, "proveedoresAlta.html",{"proveedores_form": proveedores_form})



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
    #return render(request, "recetas/proveedores.html",{"proveedores": proveedores,"proveedores_form": proveedores_form,"filtros":filters})

    return redirect('proveedores')


def proveedoresModificar(request,proveedor_id =None):
    proveedor_instancia = get_object_or_404(models.Proveedor, pk=proveedor_id)
    if request.method=="POST":
        proveedor_form = forms.ProveedorForm(request.POST,instance= proveedor_instancia)
        if proveedor_form.is_valid():
            proveedor_form.save()
        return redirect('proveedores')
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
def productosTerminadosBaja(request,producto_id =None):
    print "estoy en bajaaa"
    p = models.ProductoTerminado.objects.get(pk=producto_id)
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
        return render(request, "recetas/ciudades.html",{"ciudades":ciudades,"zonas":zonas})



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

