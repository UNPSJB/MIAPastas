from django.shortcuts import render, redirect
from . import models
from . import forms
from django.forms.formsets import formset_factory
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
def insumos(request):
    filters = get_filtros(request.GET, models.Insumo)
    mfilters = dict(filter(lambda v: v[0] in models.Insumo.FILTROS, filters.items()))
    insumos = models.Insumo.objects.filter(**mfilters)
    if request.method == 'POST':
        insumos_form = forms.InsumoForm(request.POST)
        if insumos_form.is_valid():
            insumos_form.save()
            return redirect('insumos')
    else:
        insumos_form = forms.InsumoForm()
    return render(request, "recetas/insumos.html",
                  {"insumos": insumos,
                   "filtros": filters,
                   "insumos_form": insumos_form})



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
def proveedores(request):
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
               #     Z O N A S   #
#********************************************************#
def zonas(request):
    filters = get_filtros(request.GET, models.Zona)
    mfilters = dict(filter(lambda v: v[0] in models.Zona.FILTROS, filters.items()))
    zonas = models.Zona.objects.filter(**mfilters)
    if request.method == 'POST':
        zonas_form = forms.ZonaForm(request.POST)
        if zonas_form.is_valid():
            zonas_form.save()
            return redirect('zonas')
    else:
        zonas_form = forms.ZonaForm()
    return render(request, "recetas/zonas.html",
                  {"zonas": zonas,
                   "filtros": filters,
                   "zonas_form": zonas_form})


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
#********************************************************#
               #     C L I E N T E S   #
#********************************************************#
def clientes(request):
    clientes = None
    filters = None
    if request.method == 'POST':
        clientes_form = forms.ClienteForm(request.POST)
        if clientes_form.is_valid():
            clientes_form.save()
            return redirect('clientes')
    else:
        filters = get_filtros(request.GET, models.Cliente)
        clientes_form = forms.ClienteForm()
        mfilters = dict(filter(lambda v: v[0] in models.Cliente.FILTROS, filters.items()))
        clientes = models.Cliente.objects.filter(**mfilters)
    return render(request, "recetas/clientes.html",
                  {"clientes": clientes,
                   "filtros": filters,
                   "clientes_form": clientes_form})
