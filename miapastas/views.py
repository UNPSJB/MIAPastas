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