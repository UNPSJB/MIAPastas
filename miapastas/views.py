from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import models as auth_models
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template.context import RequestContext
from django.core import serializers

from forms import SignUpForm, UsuarioEditarForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
import json

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
#from pylab import *


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
    print "INDEXXXXXXXXXXXXX"
    return render_to_response('index.html', {'user': request.user}, context_instance=RequestContext(request))


@login_required()
def ayuda(request):
    return render(request, "ayuda.html", {})


def login(request):
    return render(request, "login.html", {},context_instance=RequestContext(request))

@login_required()
def usuario(request):
    return render(request, "usuario.html", {})

@login_required()
@permission_required('auth.add_user')
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

            return HttpResponseRedirect(reverse('usuariosAdmin'))
    else:
        form = SignUpForm()

    data = {
        'form': form,
    }
    return render_to_response('signup.html', data, context_instance=RequestContext(request))



@login_required()
@permission_required('auth.change_user')
def usuarioEditar(request ,usuario_id):
    usuario_instancia = get_object_or_404(auth_models.User, pk = usuario_id)
    if request.method == 'POST':
        form = UsuarioEditarForm(request.POST,instance= usuario_instancia)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('usuario'))

    return render(request, "usuarioEditar.html", {})


@login_required()
def usuarioCambiarClave(request,usuario_id):    
    password = request.GET['passw']
    usuario = auth_models.User.objects.get(pk=usuario_id)
    usuario.set_password(password)
    usuario.save()
    messages.success(request,"Se realizo el cambio de clave")
    return HttpResponse(json.dumps("ok"),content_type='json')



@login_required()
def usuarioCambiarClaveMostrar(request,usuario_id):
    print "ENNN usuarioCambiarClaveMostrar"
    usuario = auth_models.User.objects.get(pk=usuario_id)
    return render(request, "usuarioCambiarClave.html", {"user":usuario})



@login_required()
@permission_required('auth.change_user')
def usuariosAdmin(request):
    usuarios = auth_models.User.objects.all()
    return render(request, "usuariosAdmin.html", {"usuarios":usuarios})



@login_required()
@permission_required('auth.change_user')
def usuariosAdminModificar(request,usuario_id):
    usuario = auth_models.User.objects.get(pk=usuario_id)
    grupos_usuario = usuario.groups.all()
    grupos = []
    for u in auth_models.Group.objects.all():
        if not (u in grupos_usuario):
            grupos.append(u)
    return render(request, "usuariosAdminModificar.html", {"usuario":usuario,"id":usuario_id,
                                                           "grupos":grupos, "grupos_usuario":grupos_usuario
                                                          })


@login_required()
@permission_required('auth.change_user')
def usuariosAdminModificarAgregarGrupo(request,usuario_id,grupo_id):
    usuario = auth_models.User.objects.get(pk=usuario_id)
    grupo = auth_models.Group.objects.get(pk=grupo_id)
    usuario.groups.add(grupo)
    usuario.save()
    return HttpResponse('Ok')




@login_required()
@permission_required('auth.change_user')
def usuariosAdminModificarQuitarGrupo(request, usuario_id, grupo_usuario_id):
    usuario = auth_models.User.objects.get(pk=usuario_id)
    grupo = auth_models.Group.objects.get(pk=grupo_usuario_id)
    usuario.groups.remove(grupo)
    usuario.save()
    return HttpResponse('Ok')




@login_required()
@permission_required('auth.delete_user')
def usuariosAdminBaja(request,usuario_id):
    usuario = auth_models.User.objects.get(pk=usuario_id)
    if not usuario.is_staff:
        messages.success(request, 'El usuario: ' + usuario.username + ', ha sido eliminado correctamente.')
        usuario.delete()
    else:
        messages.error(request, 'El usuario: ' + usuario.username + ', no puede ser eliminado ya que posee privilegios de superusuaro.')
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


#retorna todos los clientes morosos.
@login_required()
def listadoClientesMorosos(request):
    clientes = models.Cliente.objects.filter(saldo__gt=0)
    print("pase por acaaaaaa")
    print(clientes)
    print("pase por acaaaaaa")
    ciudades= models.Ciudad.objects.all()
    return render(request, "listadoClientesMorosos.html", {"clientes": clientes,"ciudades":ciudades})

#retorna los clientes morosos filtrados por el usuario.
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
def listadoHojasDeRutaFinalizadas(request):
    hojas = models.HojaDeRuta.objects.filter(rendida=True,pagado=True)

    filters, mfilters = get_filtros(request.GET, models.HojaDeRuta)
    hojas = hojas.filter(**mfilters)
    hojas = sorted(hojas, key=lambda hoja: hoja.fecha_creacion)
    print(mfilters)
    return render(request, "listadoHojasDeRutaFinalizadas.html/", {"hojas": hojas,"filtros": filters})



#retorna un archivo excel que contiene todos los cliente morosos.
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


    bold = workbook.add_format({'bold': True})
    italic = workbook.add_format({'italic': True})
    red = workbook.add_format({'color': 'red'})

    cell_format_titulo = workbook.add_format({'align': 'center',
                                   'valign': 'vcenter',
                                   'border': 1,
                                       'bold':bold,
                                              'italic':italic,'font_size':16,})

    cell_format_header = workbook.add_format({'align': 'center',
                                   'valign': 'vcenter',
                                   'border': 1,
                                       'bold':bold,
                                              })

    cell_format_body = workbook.add_format({'align': 'center',
                                   'valign': 'vcenter',
                                   'border': 1,
                                            })

    cell_format_footer = workbook.add_format({'align': 'center',
                                   'valign': 'vcenter',
                                   'border': 1,
                                    'bold':bold,'font_size':13,
                                    'font_color': 'red',
                                            })

    #http://xlsxwriter.readthedocs.org/format.html
    fecha = datetime.date.today()
    fecha = fecha.strftime("%d/%m/%Y")
    worksheet.merge_range('A1:F1', "Listado de Clientes Morosos: "+fecha, cell_format_titulo)
    #worksheet.set_column('A:F', 12)

    #worksheet.set_column('A:F')
    #worksheet.autofilter('A2:F2')
    #worksheet.write(0, 0, "Listado de Clientes Morosos")

    worksheet.write(1, 0,"Cuit",cell_format_header)
    worksheet.set_column('A:A', 25)
    worksheet.write(1, 1, "Razon Social",cell_format_header)
    worksheet.set_column('B:B', 30)
    worksheet.write(1, 2, "Ciudad",cell_format_header)
    worksheet.set_column('C:C', 20)
    worksheet.write(1, 3, "Direccion",cell_format_header)
    #worksheet.set_column(1,3,15)
    worksheet.set_column('D:D', 20)
    worksheet.write(1, 4, "Telefono",cell_format_header)
    #worksheet.set_column(1,4,15)
    worksheet.set_column('E:E', 15)
    worksheet.write(1, 5, "Monto Adeudado",cell_format_header)
    #worksheet.set_column(1,5,5)
    worksheet.set_column('F:F', 20)

    cantidad_total_adeudado = 0
    numero_fila = 2

    for index, cliente in enumerate(clientes, 1):
        if cliente.saldo!=0:

            worksheet.write(numero_fila, 0, cliente.cuit,cell_format_body)
            #worksheet.set_column(1,0,len(str(cliente.cuit)))
            worksheet.write(numero_fila, 1, cliente.razon_social,cell_format_body)
            worksheet.write(numero_fila, 2, cliente.ciudad.nombre,cell_format_body)
            worksheet.write(numero_fila, 3, cliente.direccion,cell_format_body)
            worksheet.write(numero_fila, 4, cliente.telefono,cell_format_body)
            worksheet.write(numero_fila, 5, '$'+str(cliente.saldo),cell_format_body)
            cantidad_total_adeudado += cliente.saldo
            numero_fila+=1


    worksheet.write(numero_fila, 0, 'TOTAL ADEUDADO',cell_format_footer)
    worksheet.write(numero_fila, 1, '$'+str(cantidad_total_adeudado),cell_format_footer)
    #worksheet.add_table('B3:F7')
    workbook.close()

    output.seek(0)

    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=ListadoClientesMorosos.xlsx"

    return response



#muestra todos los productos termiandos disponibles.
@login_required()
def listadoProductosTerminadosDisponibles(request):
    productos = models.ProductoTerminado.objects.filter(stock__gt=0)

    print("pase por acaaaaaa")
    print(productos)

    print("pase por acaaaaaa")

    return render(request, "listadoProductosTerminadosDisponibles.html", {"productos": productos,"productos_filtrados":productos})

#muestra los productos terminados dispobibles filtrados por el usuario.
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

#arma el archivo excel que muestra los productos terminados disponibles.
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

    bold = workbook.add_format({'bold': True})
    italic = workbook.add_format({'italic': True})
    red = workbook.add_format({'color': 'red'})

    cell_format_titulo = workbook.add_format({'align': 'center',
                                   'valign': 'vcenter',
                                   'border': 1,
                                       'bold':bold,
                                              'italic':italic,'font_size':16,})

    cell_format_header = workbook.add_format({'align': 'center',
                                   'valign': 'vcenter',
                                   'border': 1,
                                       'bold':bold,
                                              })

    cell_format_sub_header = workbook.add_format({'align': 'center',
                                   'valign': 'vcenter',

                                       'bold':bold,
                                              })


    cell_format_body = workbook.add_format({'align': 'center',
                                   'valign': 'vcenter',

                                            })

    cell_format_sub_footer = workbook.add_format({'align': 'center',
                                   'valign': 'vcenter',

                                    'bold':bold,'font_size':12,
                                    'font_color': 'red',
                                            })

    cell_format_footer = workbook.add_format({'align': 'center',
                                   'valign': 'vcenter',
                                    'border': 1,
                                    'bold':bold,'font_size':14,
                                    'font_color': 'red',
                                            })

    fecha = datetime.date.today()
    fecha = fecha.strftime("%d/%m/%Y")
    worksheet.merge_range('A1:F1', "Listado de Productos Terminados Disponibles: "+fecha, cell_format_titulo)
    worksheet.set_column('A1:F1', 25)



    fila = 1
    total_stock = 0
    for producto in productos:
        worksheet.write(fila, 0, "Tipo de Fideo",cell_format_header)
        worksheet.set_column('A:A', 25)
        worksheet.write(fila, 1, producto.nombre,cell_format_header)
        worksheet.set_column('B:B', 25)

        fila = fila + 1

        worksheet.write(fila, 1, "N de Lote",cell_format_sub_header)
        #worksheet.set_column('C:C', 15)
        worksheet.write(fila, 2, "Cantidad",cell_format_sub_header)
        worksheet.set_column('C:C', 15)

        fila = fila + 1
        for lote in producto.lote_set.all():
            worksheet.write(fila, 1, lote.nro_lote,cell_format_body)
            worksheet.write(fila, 2, lote.stock_disponible,cell_format_body)
            fila = fila + 1

        total_stock = total_stock + producto.stock
        worksheet.write(fila, 1, "Total",cell_format_sub_footer)
        worksheet.write(fila, 2, producto.stock,cell_format_sub_footer)
        fila = fila + 1

    fila = fila + 1
    worksheet.write(fila, 1, "TOTAL BOLSINES",cell_format_footer)
    worksheet.write(fila, 2, total_stock,cell_format_footer)


    workbook.close()

    output.seek(0)

    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=ListadoProductosTerminados.xlsx"

    return response

#retorna todos los productos y sus cantidades vendidas
@login_required()
def listadoProductosMasVendidos(request):
    entregas = models.Entrega.objects.all()
    prod = {}
    for entrega in entregas:
        #aca iria una validacion de que no sean pedidos de cambio------------><----------------
        if not entrega.pedido.tipo_pedido == 3:#si no es un pedido de cambio, entonces proceso....

            for d in entrega.entregadetalle_set.all():
                try:
                    prod[d.get_producto_terminado().nombre] += d.cantidad_entregada
                except:
                    prod[d.get_producto_terminado().nombre]=0
                    prod[d.get_producto_terminado().nombre] += d.cantidad_entregada
    return render(request, "listadoProductosMasVendidos.html", {"prod": prod})

#retorna los productos mas vendidos filtrados por el usuario.
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
            if not entrega.pedido.tipo_pedido == 3:#si no es un pedido de cambio, entonces proceso....
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


#arma el grafico de torta utilizando la libreria pylab
def GraficoTorta(request,productos,fecha_desde,fecha_hasta):
    from pylab import *
    #  I M A G E N
    #print productos,"hahhahahahha"
    figure(1, figsize=(9,9))# tamanio de figura
    #ax = axes([0, 0, 0.9, 0.9])# donde esta la figura ancho alto etc..
    ax = axes([0.1, 0.1, 0.8, 0.8])

    title('Productos Mas Vendidos ', bbox={'facecolor':'0.8', 'pad':5})
    figtext(.5,.85,'Fecha Desde: ' + fecha_desde + "\n" + 'Fecha Hasta: ' + fecha_hasta,fontsize=10,horizontalalignment='center',bbox={'facecolor':'0.8', 'pad':5})

    labels = []
    fracs = []
    print "+"*20
    print "productos: ",productos
    for p in productos:
        labels.append(p)
        fracs.append(productos[p])

    pie(fracs,labels=labels, autopct='%10.0f%%',startangle=90 ,shadow=True)
    legend(labels,loc="lower left",bbox_to_anchor=[0.8, 0.5])#,loc='bottom rigth')
    #axis('equal')
    #savefig("a.png")
    response = HttpResponse(content_type='image/png')
    savefig(response,format='PNG')

    return response



#retorna verdadero si todos los pedidos de las entregas son de cambio, falso sino.
def verificarNoTodosPedidosCambio(entregas):
    bandera = False
    for entrega in entregas:
        if entrega.pedido.tipo_pedido == 3:
            bandera = True
        else:
            bandera = False
            break
    return bandera



#obtiene todos los datos necesarios para pasarlos a la funcion GraficoTorta() y que esta arme el grafico de torta
@login_required()
def ListadoProductosMasVendidosGrafico(request):
    #OBTENIENDO LAS FECHAS
    try:
        fecha_desde = request.GET['fecha_desde']
        fecha_hasta = request.GET['fecha_hasta']
    except:
        print('ENTREEEEE EN LA EXCEPCION!!!')
        fecha_desde = datetime.datetime.today()
        fecha_hasta = datetime.datetime.today()

    if not fecha_desde:
        #fecha_desde = datetime.datetime.today()
        #fecha_desde = fecha_desde.strftime("%d/%m/%Y")
        fecha_desde = "Los inicios"

    if not fecha_hasta:
        fecha_hasta = datetime.datetime.today()
        fecha_hasta = fecha_hasta.strftime("%d/%m/%Y")

    #if fecha_hasta > datetime.datetime.today().strftime("%d/%m/%Y"):
    #    fecha_hasta = datetime.datetime.today().strftime("%d/%m/%Y") DUDA---> Preguntar: Hace falta esta validacion??? igual no tiraria error


    #OBTENIENDO LAS ENTREGAS A TRAVES DEL ATRIBUTO FILTERS
    filters, mfilters = get_filtros(request.GET, models.Entrega)
    entregas = models.Entrega.objects.filter(**mfilters)
    if not entregas.exists():
        return HttpResponseNotFound('No hay productos terminados vendidos.')

    if verificarNoTodosPedidosCambio(entregas):
        return HttpResponseNotFound('No hay productos terminados vendidos. (Todos son Pedidos de Cambio)')


    prod = {}




    for entrega in entregas:
        if not entrega.pedido.tipo_pedido == 3:#si no es un pedido de cambio, entonces proceso....
            for d in entrega.entregadetalle_set.all():
                    try:
                        prod[d.get_producto_terminado().nombre] += d.cantidad_entregada
                    except:
                        prod[d.get_producto_terminado().nombre]=0
                        prod[d.get_producto_terminado().nombre] += d.cantidad_entregada
    return GraficoTorta(request,prod,fecha_desde,fecha_hasta)


#permite armar un archivo excel con los productos mas vendidos.
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
        #fecha_desde = datetime.datetime.today()
        #fecha_desde = fecha_desde.strftime("%d/%m/%Y")
        fecha_desde = "Los inicios"

    if not fecha_hasta:
        fecha_hasta = datetime.datetime.today()
        fecha_hasta = fecha_hasta.strftime("%d/%m/%Y")



    print(fecha_desde)
    print(fecha_hasta)


    #OBTENIENDO LAS ENTREGAS A TRAVES DEL ATRIBUTO FILTERS
    filters, mfilters = get_filtros(request.GET, models.Entrega)
    print(mfilters)
    entregas = models.Entrega.objects.filter(**mfilters)

    print("comienzo..............")
    print(entregas)
    print("fin...................")


    #VERIFICANDO QUE HAYA PRODUCTOS
    if not entregas.exists():
        return HttpResponseNotFound('No hay productos terminados vendidos.')

    if verificarNoTodosPedidosCambio(entregas):
        return HttpResponseNotFound('No hay productos terminados vendidos. (Todos son Pedidos de Cambio)')


    #ARMANDO EL ARCHIVO EXCEL
    output = io.BytesIO()
    workbook = Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    #<<<<creando formatos>>>>
    bold = workbook.add_format({'bold': True})
    italic = workbook.add_format({'italic': True})
    red = workbook.add_format({'color': 'red'})

    cell_format_titulo = workbook.add_format({'align': 'center',
                                   'valign': 'vcenter',
                                   'border': 1,
                                       'bold':bold,
                                              'italic':italic,'font_size':16,})

    cell_format_header = workbook.add_format({'align': 'center',
                                   'valign': 'vcenter',
                                   'border': 1,
                                       'bold':bold,
                                              })

    cell_format_header_fechas = workbook.add_format({'align': 'center',
                                   'valign': 'vcenter',
                                   'border': 1,

                                              })

    cell_format_body = workbook.add_format({'align': 'center',
                                   'valign': 'vcenter',
                                   'border': 1,
                                            })

    cell_format_footer = workbook.add_format({'align': 'center',
                                   'valign': 'vcenter',
                                   'border': 1,
                                    'bold':bold,'font_size':13,
                                    'font_color': 'red',
                                            })

    #<<<<armando el archivo>>>>
    fecha = datetime.date.today()
    fecha = fecha.strftime("%d/%m/%Y")
    worksheet.merge_range('A1:F1', "Listado de Productos Terminados Mas Vendidos: "+fecha, cell_format_titulo)
    worksheet.set_column('A1:F1', 15)

    worksheet.write(1, 0, "Fecha Desde: ",cell_format_header)
    worksheet.write(1, 1, fecha_desde,cell_format_header_fechas)

    worksheet.write(2, 0, "Fecha Hasta: ",cell_format_header)
    worksheet.write(2, 1, fecha_hasta,cell_format_header_fechas)

    worksheet.write(3, 0, "Producto Terminado",cell_format_header)
    worksheet.set_column('A:A', 25)
    worksheet.write(3, 1, "Cantidad Vendida",cell_format_header)
    worksheet.set_column('B:B', 25)

    numero_fila = 4

    prod = {}
    totales = 0
    for entrega in entregas:
        if not entrega.pedido.tipo_pedido == 3:#si no es un pedido de cambio, entonces proceso....
            for d in entrega.entregadetalle_set.all():
                    try:
                        prod[d.get_producto_terminado().nombre] += d.cantidad_entregada
                        totales = totales + d.cantidad_entregada
                    except:
                        prod[d.get_producto_terminado().nombre]=0
                        prod[d.get_producto_terminado().nombre] += d.cantidad_entregada
                        totales = totales + d.cantidad_entregada


    for nombre,cantidad in prod.items():
        worksheet.write(numero_fila, 0, nombre,cell_format_header)
        worksheet.write(numero_fila, 1, str(cantidad) + ' Bolsines ',cell_format_header_fechas)
        numero_fila = numero_fila + 1


    worksheet.write(numero_fila, 0, "TOTALES: ",cell_format_footer)
    worksheet.write(numero_fila, 1,str(totales)+' Bolsines' , cell_format_footer)

    workbook.close()

    output.seek(0)

    response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=ListadoPDVendidos.xlsx"

    return response
