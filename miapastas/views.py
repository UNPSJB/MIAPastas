from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from forms import SignUpForm
from django.contrib.auth.decorators import login_required



@login_required()
def index(request):
    return render_to_response('index.html', {'user': request.user}, context_instance=RequestContext(request))

#def index(request):
#   messages.success(request, 'Hola usuario.')
#   return render(request, "index.html", {})


def cacho(request):
    return render(request, "cacho.html", {})


def ayuda(request):
    return render(request, "ayuda.html", {})


def probando(request):
    return render(request, "probando.html", {})


def prueba(request):
    return render(request, "prueba.html", {})


def prueba2(request):
    return render(request, "prueba2.html", {})


def prueba3(request):
    return render(request, "prueba3.html", {})


def login(request):
    return render(request, "login.html", {},context_instance=RequestContext(request))


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


def recetasConsulta(request):
    return render(request, "recetasConsulta.html", {})


def recetasModificar(request):
    return render(request, "recetasModificar.html", {})


def recetasAlta(request):
    return render(request, "recetasAlta.html", {})


def clientes(request):
    return render(request, "clientes.html", {})


def clientesConsulta(request):
    return render(request, "clientesConsulta.html", {})


def clientesAlta(request):
    return render(request, "clientesAlta.html", {})


def clientesModificar(request):
    return render(request, "clientesModificar.html", {})



def proveedoresConsulta(request):
    return render(request, "proveedoresConsulta.html", {})


def proveedoresAlta(request):
    return render(request, "proveedoresAlta.html", {})


def proveedoresModificar(request):
    return render(request, "proveedoresModificar.html", {})


def producciones(request):
    return render(request, "producciones.html", {})



def produccionesAlta(request):
    return render(request, "produccionesAlta.html", {})


def produccionesConsulta(request):
    return render(request, "produccionesConsulta.html", {})


def produccionesModificar(request):
    return render(request, "produccionesModificar.html", {})


def hojaDeRuta(request):
    return render(request, "hojaDeRuta.html", {})



def ciudades(request):
    return render(request, "ciudades.html", {})


def ciudadesAlta(request):
    return render(request, "ciudadesAlta.html", {})



def ciudadesModificar(request):
    return render(request, "ciudadesModificar.html", {})


def insumosAlta(request):
    return render(request, "insumosAlta.html", {})


def insumosConsulta(request):
    return render(request, "insumosConsulta.html", {})


def insumosModificar(request):
    return render(request, "insumosModificar.html", {})


def zonas(request):
    return render(request, "zonas.html", {})


def zonasAlta(request):
    return render(request, "zonasAlta.html", {})


def zonasConsulta(request):
    return render(request, "zonasConsulta.html", {})


def zonasModificar(request):
    return render(request, "zonasModificar.html", {})


def rendicionReparto(request):
    return render(request, "rendicionReparto.html", {})



def cobrarCliente(request):
    return render(request, "cobrarCliente.html", {})


def pedidosCliente(request):
    return render(request, "pedidosCliente.html", {})


def choferes(request):
    return render(request, "choferes.html", {})


def choferesModificar(request):
    return render(request, "choferesModificar.html", {})


def choferesAlta(request):
    return render(request, "choferesAlta.html", {})


def productosTerminados(request):
    return render(request, "productosTerminados.html", {})


def productosTerminadosAlta(request):
    return render(request, "productosTerminadosAlta.html", {})


def productosTerminadosModificar(request):
    return render(request, "productosTerminadosModificar.html", {})


def productosTerminadosActualizarStock(request):
    return render(request, "productosTerminadosActualizarStock.html", {})


def productosTerminadosActualizarPrecio(request):
    return render(request, "productosTerminadosActualizarPrecio.html", {})


def pedidosClienteAlta(request):
    return render(request, "pedidosClienteAlta.html", {})


def rendicionRepartoPedidos(request):
    return render(request, "rendicionRepartoPedidos.html", {})

def pedidosProveedor(request):
    return render(request, "pedidosProveedor.html", {})

def proveedoresRecepcion(request):
    return render(request, "proveedoresRecepcion.html", {})