from django.shortcuts import render, redirect
from . import models
from . import forms
from django.forms.formsets import formset_factory
from django.shortcuts import get_object_or_404

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
#chupala facurfvbggrf

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








#********************************************************#
               #     R E C E T A S    #
#********************************************************#
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
        receta_form = forms.RecetaForm(request.POST)
        if receta_form.is_valid():
            receta = receta_form.save()
            detalles_form = detalles_form_class(request.POST, request.FILES)
            if detalles_form.is_valid():
                #detalles = detalles_form.save(commit=False)
                #receta.save()
                for detalle in detalles_form:
                    d = detalle.save(commit=False)
                    d.receta = receta
                    d.save()

                return redirect('recetas')

    insumos = models.Insumo.objects.all()
    return render(request, "recetas/recetas.html", {
        "recetas": recetas,
        "receta_form": receta_form or forms.RecetaForm(),
        "detalles_form_factory": detalles_form or detalles_form_class(),
        "modal": request.method == "POST",
        "insumos":insumos})



    # borrador no va


def recetasModificar(request):
    form = forms.RecetaForm()
    form2 = models.Receta.objects.all()
    return render(request, "recetasModificar.html", {"form":form,"form2":form2})


    # FIN BORRADOR


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

    #recetas = models.Receta.objects.all()


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


def proveedoresBaja(request):
    print "holaaaa "
    id_proveedor = request.POST["proveedor_id"]
    p = models.Receta.objects.get(pk=id_proveedor)




#********************************************************#
               #     P R O D U C T O S   #
#********************************************************#
def productosTerminados(request):
    filters = get_filtros(request.GET, models.ProductoTerminado)
    mfilters = dict(filter(lambda v: v[0] in models.ProductoTerminado.FILTROS, filters.items()))
    productosTerminados = models.ProductoTerminado.objects.filter(**mfilters)
    if request.method == "POST":
        productos_form = forms.ProductoTerminadoForm(request.POST)
        if productos_form.is_valid():
            productos_form.save()
            return redirect('productosTerminados')
    else:
        productos_form = forms.ProductoTerminadoForm()
    return render(request, "recetas/productosTerminados.html",{"productosTerminados": productosTerminados,"productos_form": productos_form})

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


#********************************************************#
              #     C L I E N T E S    #
#********************************************************#

def clientes(request,cliente_id=None):
    if cliente_id is not None:
        # consulta
        cliente_instancia = models.Cliente.objects.get(pk=cliente_id)
        cliente_form = forms.ClienteForm(instance= cliente_instancia)

        return render(request, "clientesConsulta.html",{"cliente_form": cliente_form})
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



#********************************************************#
               #     C I U D A D E S   #
#********************************************************#
def ciudades(request):
    filters = get_filtros(request.GET, models.Ciudad)
    mfilters = dict(filter(lambda v: v[0] in models.Ciudad.FILTROS, filters.items()))
    ciudades = models.Ciudad.objects.filter(**mfilters)
    zonas = models.Zona.objects.all() #zonas para poder filtrar
    if request.method == 'POST':
        ciudades_form = forms.CiudadForm(request.POST)
        if ciudades_form.is_valid():
            ciudades_form.save()
            return redirect('ciudades')
    else:
        ciudades_form = forms.CiudadForm()
    return render(request, "recetas/ciudades.html",
                  {"ciudades": ciudades,
                   "filtros": filters,
                   "ciudades_form": ciudades_form,
                   "zonas":zonas})


def ciudadesAlta(request):
    ciudades_form = forms.CiudadForm()
    print("puyo")
    return render(request,"ciudadesAlta.html",{"ciudades_form": ciudades_form})
