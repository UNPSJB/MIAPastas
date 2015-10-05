"""disney URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from . import views
from recetas import views as recetasviews

urlpatterns = [
    url(r'^index$', views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ayuda$', views.ayuda, name='ayuda'),
    url(r'^cacho$', views.cacho, name='cacho'),
    url(r'^probando$', views.probando, name='probando'),
    url(r'^prueba$', views.prueba, name='prueba'),
    url(r'^prueba2$', views.prueba2, name='prueba2'),
    url(r'^prueba3$', views.prueba3, name='prueba3'),
    url(r'^login$', views.login, name='login'),
    url(r'^recetasConsulta$',views.recetasConsulta,name='recetasConsulta'),

    url(r'^recetasModificar$',recetasviews.recetasModificar,name='recetasModificar'),

    url(r'^clientesConsulta$',views.clientesConsulta,name='clientesConsulta'),
    url(r'^clientesModificar$',views.clientesModificar,name='clientesModificar'),
    url(r'^proveedoresConsulta$',views.proveedoresConsulta,name='proveedoresConsulta'),
    url(r'^proveedoresModificar$',views.proveedoresModificar,name='proveedoresModificar'),
    url(r'^producciones$',views.producciones,name='producciones'),
    url(r'^produccionesAlta$',views.produccionesAlta,name='produccionesAlta'),
    url(r'^produccionesConsulta$',views.produccionesConsulta,name='produccionesConsulta'),
    url(r'^produccionesModificar$',views.produccionesModificar,name='produccionesModificar'),

    url(r'^ciudadesModificar$',views.ciudadesModificar,name='ciudadesModificar'),



    # Hechos en forms
    url(r'^insumos$',recetasviews.insumos,name='insumos'),
    url(r'^insumos/add$',recetasviews.insumos,name='insumosAlta'),
    url(r'^recetas$',recetasviews.recetas,name='recetas'),

    url(r'^recetas/(?P<receta_id>[0-9]+)/$',recetasviews.recetas,name='recetasID'),




    url(r'^zonas/$',recetasviews.zonas,name='zonas'),
    url(r'^zonas/alta/$',recetasviews.zonasAlta,name='zonasAlta'),
    url(r'^zonas/(?P<zona_id>[0-9]+)/$',recetasviews.zonas,name='zonaConsulta'),
    url(r'^zonas/modificar/(?P<zona_id>[0-9]+)/$',recetasviews.zonasModificar,name='zonaModificar'),

    url(r'^clientes/$',recetasviews.clientes,name='clientes'),
    url(r'^clientes/alta/$',recetasviews.clientesAlta,name='clientesAlta'),
    url(r'^clientes/(?P<cliente_id>[0-9]+)/$',recetasviews.clientes,name='clienteConsulta'),
    url(r'^clientes/modificar/(?P<cliente_id>[0-9]+)/$',recetasviews.clientesModificar,name='clienteModificar'),



    url(r'^recetas/add$',recetasviews.recetas,name='recetasAlta'),
    url(r'^proveedores$',recetasviews.proveedores,name='proveedores'),
    url(r'^proveedores/add$',recetasviews.proveedores,name='proveedoresAlta'),
    url(r'^productosTerminados$',recetasviews.productosTerminados,name='productosTerminados'),
    url(r'^productosTerminados/add$',recetasviews.productosTerminados,name='productosTerminadosAlta'),
    url(r'^ciudades$',recetasviews.ciudades,name='ciudades'),
    url(r'^ciudades/add$',recetasviews.ciudades,name='ciudadesAlta'),
    url(r'^ciudadesAlta/$',recetasviews.ciudadesAlta,name='ciudadesAlta'),
    #url(r'^clientes$',recetasviews.clientes,name='clientes'),
    #url(r'^clientes/add$',recetasviews.clientes,name='clientesAlta'),





    url(r'^recetasConsulta$',views.recetasConsulta,name='recetasConsulta'),
    url(r'^recetasModificar$',views.recetasModificar,name='recetasModificar'),
    url(r'^clientesConsulta$',views.clientesConsulta,name='clientesConsulta'),
    #url(r'^clientesAlta$',views.clientesAlta,name='clientesAlta'),
    url(r'^clientesModificar$',views.clientesModificar,name='clientesModificar'),
    url(r'^proveedoresConsulta$',views.proveedoresConsulta,name='proveedoresConsulta'),
    url(r'^proveedoresModificar$',views.proveedoresModificar,name='proveedoresModificar'),
    url(r'^producciones$',views.producciones,name='producciones'),
    url(r'^produccionesAlta$',views.produccionesAlta,name='produccionesAlta'),
    url(r'^produccionesConsulta$',views.produccionesConsulta,name='produccionesConsulta'),
    url(r'^produccionesModificar$',views.produccionesModificar,name='produccionesModificar'),

    url(r'^ciudadesModificar$',views.ciudadesModificar,name='ciudadesModificar'),
    url(r'^insumosConsulta$',views.insumosConsulta,name='insumosConsulta'),
    url(r'^insumosModificar$',views.insumosModificar,name='insumosModificar'),
    # url(r'^zonas$',views.zonas,name='zonas'),
    #url(r'^zonasAlta$',views.zonasAlta,name='zonasAlta'),
    url(r'^zonasConsulta$',views.zonasConsulta,name='zonasConsulta'),
    url(r'^zonasModificar$',views.zonasModificar,name='zonasMoficar'),
    url(r'^hojaDeRuta$',views.hojaDeRuta,name='hojaDeRuta'),
    url(r'^rendicionReparto$',views.rendicionReparto,name='rendicionReparto'),
    url(r'^cobrarCliente$',views.cobrarCliente,name='cobrarCliente'),
    url(r'^pedidosCliente$',views.pedidosCliente,name='pedidosCliente'),
    url(r'^choferes$',views.choferes,name='choferes'),
    url(r'^choferesModificar$',views.choferesModificar,name='choferesModificar'),
    url(r'^choferesAlta$',views.choferesAlta,name='choferesAlta'),
    #url(r'^productosTerminadosAlta$',views.productosTerminadosAlta,name='productosTerminadosAlta'),
    url(r'^productosTerminadosModificar$',views.productosTerminadosModificar,name='productosTerminadosModificar'),
    url(r'^productosTerminadosActualizarStock',views.productosTerminadosActualizarStock,name='productosTerminadosActualizarStock'),
    url(r'^productosTerminadosActualizarPrecio$',views.productosTerminadosActualizarPrecio,name='productosTerminadosActualizarPrecio'),
    url(r'^pedidosClienteAlta$',views.pedidosClienteAlta,name='pedidosClienteAlta'),
    url(r'^rendicionRepartoPedidos$',views.rendicionRepartoPedidos,name='rendicionRepartoPedidos'),
    url(r'^pedidosProveedores$',views.pedidosProveedores,name='pedidosProveedores'),
    url(r'^proveedoresRecepcion$',views.proveedoresRecepcion,name='proveedoresRecepcion'),
    url(r'^$',views.login,name='login')


]
