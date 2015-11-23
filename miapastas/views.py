from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import models as auth_models
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from recetas import models
from recetas import views
from recetas import forms
import datetime
from datetime import date
import re #esto sirve para usar expresiones regulares
import xlsxwriter
import io
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

from django.http import HttpResponse
from django.http import HttpResponseNotFound

from xlsxwriter.workbook import Workbook








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



@login_required()
def index(request):
    return render_to_response('index.html', {'user': request.user}, context_instance=RequestContext(request))

#def index(request):
#   messages.success(request, 'Hola usuario.')
#   return render(request, "index.html", {})

@login_required()
def cacho(request):
    return render(request, "cacho.html", {})

@login_required()
def ayuda(request):
    return render(request, "ayuda.html", {})

@login_required()
def probando(request):
    return render(request, "probando.html", {})

@login_required()
def prueba(request):
    return render(request, "prueba.html", {})

@login_required()
def prueba2(request):
    return render(request, "prueba2.html", {})

@login_required()
def prueba3(request):
    return render(request, "prueba3.html", {})


def login(request):
    return render(request, "login.html", {},context_instance=RequestContext(request))

@login_required()
def usuario(request):
    return render(request, "usuario.html", {})

@login_required()
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]

            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name

            user.save()

            return HttpResponseRedirect(reverse('login'))
    else:
        form = SignUpForm()

    data = {
        'form': form,
    }
    return render_to_response('signup.html', data, context_instance=RequestContext(request))



@login_required()
def usuariosAdmin(request):
    usuarios = auth_models.User.objects.all()
    return render(request, "usuariosAdmin.html", {"usuarios":usuarios})



@login_required()
def usuariosAdminModificar(request,usuario_id):
    usuario = auth_models.User.objects.get(pk=usuario_id)
    return render(request, "usuariosAdminModificar.html", {})



@login_required()
def usuariosAdminBaja(request,usuario_id):
    usuario = auth_models.User.objects.get(pk=usuario_id)
    messages.success(request, 'El usuario: ' + usuario.username + ', ha sido eliminado correctamente.')
    usuario.delete()
    return redirect('usuariosAdmin')




@login_required()
def recetasConsulta(request):
    return render(request, "recetasConsulta.html", {})



@login_required()
def recetasModificar(request):
    return render(request, "recetasModificar.html", {})


@login_required()
def recetasAlta(request):
    return render(request, "recetasAlta.html", {})


@login_required()
def clientes(request):
    return render(request, "clientes.html", {})


@login_required()
def clientesConsulta(request):
    return render(request, "clientesConsulta.html", {})


@login_required()
def clientesAlta(request):
    return render(request, "clientesAlta.html", {})


@login_required()
def clientesModificar(request):
    return render(request, "clientesModificar.html", {})



@login_required()
def proveedoresConsulta(request):
    return render(request, "proveedoresConsulta.html", {})


@login_required()
def proveedoresAlta(request):
    return render(request, "proveedoresAlta.html", {})


@login_required()
def proveedoresModificar(request):
    return render(request, "proveedoresModificar.html", {})


@login_required()
def producciones(request):
    return render(request, "producciones.html", {})



@login_required()
def produccionesAlta(request):
    return render(request, "produccionesAlta.html", {})


@login_required()
def produccionesConsulta(request):
    return render(request, "produccionesConsulta.html", {})


@login_required()
def produccionesModificar(request):
    return render(request, "produccionesModificar.html", {})


@login_required()
def hojaDeRuta(request):
    return render(request, "hojaDeRuta.html", {})



@login_required()
def ciudades(request):
    return render(request, "ciudades.html", {})


@login_required()
def ciudadesAlta(request):
    return render(request, "ciudadesAlta.html", {})



@login_required()
def ciudadesModificar(request):
    return render(request, "ciudadesModificar.html", {})


@login_required()
def insumosAlta(request):
    return render(request, "insumosAlta.html", {})


@login_required()
def insumosConsulta(request):
    return render(request, "insumosConsulta.html", {})


@login_required()
def insumosModificar(request):
    return render(request, "insumosModificar.html", {})


@login_required()
def zonas(request):
    return render(request, "zonas.html", {})


@login_required()
def zonasAlta(request):
    return render(request, "zonasAlta.html", {})


@login_required()
def zonasConsulta(request):
    return render(request, "zonasConsulta.html", {})


@login_required()
def zonasModificar(request):
    return render(request, "zonasModificar.html", {})


@login_required()
def rendicionReparto(request):
    return render(request, "rendicionReparto.html", {})




@login_required()
def pedidosCliente(request):
    return render(request, "pedidosCliente.html", {})


@login_required()
def choferes(request):
    return render(request, "choferes.html", {})


@login_required()
def choferesModificar(request):
    return render(request, "choferesModificar.html", {})


@login_required()
def choferesAlta(request):
    return render(request, "choferesAlta.html", {})


@login_required()
def productosTerminados(request):
    return render(request, "productosTerminados.html", {})


@login_required()
def productosTerminadosAlta(request):
    return render(request, "productosTerminadosAlta.html", {})


@login_required()
def productosTerminadosModificar(request):
    return render(request, "productosTerminadosModificar.html", {})


@login_required()
def productosTerminadosActualizarStock(request):
    return render(request, "productosTerminadosActualizarStock.html", {})


@login_required()
def productosTerminadosActualizarPrecio(request):
    return render(request, "productosTerminadosActualizarPrecio.html", {})


@login_required()
def pedidosClienteAlta(request):
    return render(request, "pedidosClienteAlta.html", {})

@login_required()
def pedidosProveedor(request):
    return render(request, "pedidosProveedor.html", {})


@login_required()
def pedidosProveedorAlta(request):
    return render(request, "pedidosProveedorAlta.html", {})


def documentacion(request):
    #return redirect("lotes")
    return render(request,"/recetas/documentacion/_build/html/index.html", {})
    #return render(request, , {})

@login_required()
def listadoClientesMorosos(request):
    clientes = models.Cliente.objects.filter(saldo__gt=0)
    print("pase por acaaaaaa")
    print(clientes)
    print("pase por acaaaaaa")
    ciudades= models.Ciudad.objects.all()
    return render(request, "listadoClientesMorosos.html", {"clientes": clientes,"ciudades":ciudades})

@login_required()
def listadoClientesMorososFiltros(request):
    if request.method == "GET":
        print("Entreee al GETTT")
        filters, mfilters = get_filtros(request.GET, models.Cliente)
        print(mfilters)
        if "saldo__gt" not in mfilters or mfilters['saldo__gt'] == "" or float(mfilters['saldo__gt'])<0:
            mfilters["saldo__gt"] = 0
        clientes = models.Cliente.objects.filter(**mfilters)
        ciudades= models.Ciudad.objects.all()
        return render(request, "listadoClientesMorosos.html",
                  {"clientes": clientes,
                   "filtros": filters,
                   "ciudades":ciudades})

    clientes = models.Cliente.objects.filter(saldo__gt=0)
    print("pase por acaaaaaa")
    print(clientes)
    print("pase por acaaaaaa")
    ciudades= models.Ciudad.objects.all()
    return render(request, "listadoClientesMorosos.html", {"clientes": clientes,"ciudades":ciudades})


@login_required()
def listadoClientesMorososExcel(request):
    #para poner el total adeudado, recorrer los clientes
    #hacer la validacion con un message.error cuando clientes=None

    #OBTENIENDO LOS CLIENTES A TRAVES DEL ATRIBUTO FILTERS
    filters, mfilters = get_filtros(request.GET, models.Cliente)
    print(mfilters)
    clientes = models.Cliente.objects.filter(**mfilters)

    #VERIFICANDO QUE HAYA CLIENTES
    if not clientes.exists():
        return HttpResponseNotFound('No hay clientes morosos para exportar a Excel')

    #ARMANDO EL ARCHIVO EXCEL
    output = io.BytesIO()
    workbook = Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, "Listado de Clientes Morosos")

    worksheet.write(1, 0, "Cuit")
    worksheet.write(1, 1, "Razon Social")
    worksheet.write(1, 2, "Ciudad")
    worksheet.write(1, 3, "Direccion")
    worksheet.write(1, 4, "Telefono")
    worksheet.write(1, 5, "Monto Adeudado")

    cantidad_total_adeudado = 0
    numero_fila = 2

    for index, cliente in enumerate(clientes, 1):
        if cliente.saldo!=0:

            worksheet.write(numero_fila, 0, cliente.cuit)
            worksheet.write(numero_fila, 1, cliente.razon_social)
            worksheet.write(numero_fila, 2, cliente.ciudad.nombre)
            worksheet.write(numero_fila, 3, cliente.direccion)
            worksheet.write(numero_fila, 4, cliente.telefono)
            worksheet.write(numero_fila, 5, cliente.saldo)
            cantidad_total_adeudado += cliente.saldo
            numero_fila+=1

    worksheet.write(numero_fila, 0, 'TOTAL ADEUDADO')
    worksheet.write(numero_fila, 1, cantidad_total_adeudado)

    workbook.close()

    output.seek(0)

    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=ListadoClientesMorosos.xlsx"

    return response




@login_required()
def listadoProductosTerminadosDisponibles(request):
    productos = models.ProductoTerminado.objects.filter(stock__gt=0)

    print("pase por acaaaaaa")
    print(productos)

    print("pase por acaaaaaa")

    return render(request, "listadoProductosTerminadosDisponibles.html", {"productos": productos,"productos_filtrados":productos})


@login_required()
def listadoProductosTerminadosDisponiblesFiltros(request):
    if request.method == "GET":
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print("Entreee al GETTT")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        filters, mfilters = get_filtros(request.GET, models.ProductoTerminado)
        print(mfilters)
        #if "saldo__gt" not in mfilters or mfilters['saldo__gt'] == "" or float(mfilters['saldo__gt'])<0:
         #   mfilters["saldo__gt"] = 0
        productos = models.ProductoTerminado.objects.filter(stock__gt=0)
        productos_filtrados = models.ProductoTerminado.objects.filter(**mfilters)

        return render(request, "listadoProductosTerminadosDisponibles.html",
                  {"productos": productos,"productos_filtrados":productos_filtrados,
                   "filtros": filters,
                   })

    productos = models.ProductoTerminado.objects.filter(stock__gt=0)
    print("pase por acaaaaaa")
    print(productos)
    print("pase por acaaaaaa")

    return render(request, "listadoProductosTerminadosDisponibles.html", {"productos": productos})


@login_required()
def listadoProductosTerminadosDisponiblesExcel(request):
    #para poner el total adeudado, recorrer los clientes
    #hacer la validacion con un message.error cuando clientes=None

    #OBTENIENDO LOS CLIENTES A TRAVES DEL ATRIBUTO FILTERS
    filters, mfilters = get_filtros(request.GET, models.ProductoTerminado)
    print(mfilters)
    productos = models.ProductoTerminado.objects.filter(**mfilters)

    print("comienzo..............")
    print(productos)
    print("fin...................")


    #VERIFICANDO QUE HAYA PRODUCTOS
    if not productos.exists():
        return HttpResponseNotFound('No hay productos terminados disponibles para exportar a Excel')

    #ARMANDO EL ARCHIVO EXCEL
    output = io.BytesIO()
    workbook = Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, "Listado de Productos Terminados Disponibles")
    fila = 1
    total_stock = 0
    for producto in productos:
        worksheet.write(fila, 0, "Tipo de Fideo")
        worksheet.write(fila, 1, producto.nombre)
        fila = fila + 1
        worksheet.write(fila, 1, "N de Lote")
        worksheet.write(fila, 2, "Cantidad")
        fila = fila + 1
        for lote in producto.lote_set.all():
            worksheet.write(fila, 1, lote.nro_lote)
            worksheet.write(fila, 2, lote.cantidad_producida)
            fila = fila + 1

        total_stock = total_stock + producto.stock
        worksheet.write(fila, 1, "Total")
        worksheet.write(fila, 2, producto.stock)
        fila = fila + 1

    fila = fila + 1
    worksheet.write(fila, 1, "Total BOLSINES")
    worksheet.write(fila, 2, total_stock)


    workbook.close()

    output.seek(0)

    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=ListadoProductosTerminados.xlsx"

    return response


@login_required()
def listadoProductosMasVendidos(request):
    entregas = models.Entrega.objects.all()
    prod = {}
    for entrega in entregas:
        for d in entrega.entregadetalle_set.all():
            try:
                prod[d.get_producto_terminado().nombre] += d.cantidad_entregada
            except:
                prod[d.get_producto_terminado().nombre]=0
                prod[d.get_producto_terminado().nombre] += d.cantidad_entregada

    print("pase por acaaaaaa")
    print(entregas)
    print(prod)
    print("pase por acaaaaaa")
    #for a,b in prod.items
     #   print
    return render(request, "listadoProductosMasVendidos.html", {"prod": prod})


@login_required()
def listadoProductosMasVendidosFiltros(request):
    if request.method == "GET":
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print("Entreee al GETTT")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")



        filters, mfilters = get_filtros(request.GET, models.Entrega)
        entregas = models.Entrega.objects.filter(**mfilters)



        print(mfilters)


        prod = {}
        for entrega in entregas:
            for d in entrega.entregadetalle_set.all():
                try:
                    prod[d.get_producto_terminado().nombre] += d.cantidad_entregada
                except:
                    prod[d.get_producto_terminado().nombre]=0
                    prod[d.get_producto_terminado().nombre] += d.cantidad_entregada


        return render(request, "listadoProductosMasVendidos.html",
                  {"prod": prod,
                   "filtros": filters,
                   })


    print("<<<<<<<<< HUBO UN ERROR...NO PUDO ENTRAR AL GET >>>>>>>>>>>")
    return render(request, "listadoProductosTerminadosDisponibles.html", {})





@login_required()
def listadoProductosMasVendidosExcel(request):
    #OBTENIENDO LAS FECHAS
    try:
        fecha_desde = request.GET['fecha_desde']
        fecha_hasta = request.GET['fecha_hasta']
    except:
        print('ENTREEEEE EN LA EXCEPCION!!!')
        fecha_desde = datetime.datetime.today()
        fecha_hasta = datetime.datetime.today()

    if not fecha_desde:
        fecha_desde = datetime.datetime.today()
        fecha_desde = fecha_desde.strftime("%d/%m/%Y")


    if not fecha_hasta:
        fecha_hasta = datetime.datetime.today()
        fecha_hasta = fecha_hasta.strftime("%d/%m/%Y")

    print(fecha_desde)
    print(fecha_hasta)
    #OBTENIENDO LOS CLIENTES A TRAVES DEL ATRIBUTO FILTERS
    filters, mfilters = get_filtros(request.GET, models.Entrega)
    print(mfilters)
    entregas = models.Entrega.objects.filter(**mfilters)

    print("comienzo..............")
    print(entregas)
    print("fin...................")


    #VERIFICANDO QUE HAYA PRODUCTOS
    if not entregas.exists():
        return HttpResponseNotFound('No hay productos terminados vendidos.')

    #ARMANDO EL ARCHIVO EXCEL
    output = io.BytesIO()
    workbook = Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, "Listado de Productos Terminados Mas Vendidos")

    worksheet.write(1, 0, "Fecha Desde: ")
    worksheet.write(1, 1, fecha_desde)

    worksheet.write(2, 0, "Fecha Hasta: ")
    worksheet.write(2, 1, fecha_hasta)

    worksheet.write(3, 0, "Producto Terminado")
    worksheet.write(3, 1, "Cantidad Vendida")

    numero_fila = 4

    prod = {}
    for entrega in entregas:
        for d in entrega.entregadetalle_set.all():
                try:
                    prod[d.get_producto_terminado().nombre] += d.cantidad_entregada
                except:
                    prod[d.get_producto_terminado().nombre]=0
                    prod[d.get_producto_terminado().nombre] += d.cantidad_entregada


    for nombre,cantidad in prod.items():
        worksheet.write(numero_fila, 0, nombre)
        worksheet.write(numero_fila, 1, cantidad)
        numero_fila = numero_fila + 1

    workbook.close()

    output.seek(0)

    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=ListadoPDVendidos.xlsx"

    return response
