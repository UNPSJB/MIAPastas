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
    url(r'^recetas$',views.recetas,name='recetas'),
    url(r'^recetasConsulta$',views.recetasConsulta,name='recetasConsulta'),
    url(r'^recetasModificar$',views.recetasModificar,name='recetasModificar'),
    url(r'^recetasAlta$',views.recetasAlta,name='recetasAlta'),
    url(r'^clientes$',views.clientes,name='clientes'),
    url(r'^clientesConsulta$',views.clientesConsulta,name='clientesConsulta'),
    url(r'^clientesAlta$',views.clientesAlta,name='clientesAlta'),
    url(r'^clientesModificar$',views.clientesModificar,name='clientesModificar'),
    url(r'^proveedores$',views.proveedores,name='proveedores'),
    url(r'^proveedoresConsulta$',views.proveedoresConsulta,name='proveedoresConsulta'),
    url(r'^proveedoresAlta$',views.proveedoresAlta,name='proveedoresAlta'),
    url(r'^proveedoresModificar$',views.proveedoresModificar,name='proveedoresModificar'),
    url(r'^producciones$',views.producciones,name='producciones'),
    url(r'^produccionesAlta$',views.produccionesAlta,name='produccionesAlta'),
    url(r'^produccionesConsulta$',views.produccionesConsulta,name='produccionesConsulta'),
    url(r'^produccionesModificar$',views.produccionesModificar,name='produccionesModificar'),
    url(r'^ciudades$',views.ciudades,name='ciudades'),
    url(r'^ciudadesAlta$',views.ciudadesAlta,name='ciudadesAlta'),
    url(r'^ciudadesModificar$',views.ciudadesModificar,name='ciudadesModificar'),

    url(r'^insumos$',recetasviews.insumos,name='insumos'),
    url(r'^insumos/add$',recetasviews.insumos,name='insumosAlta'),
    url(r'^insumosConsulta$',views.insumosConsulta,name='insumosConsulta'),
    url(r'^insumosModificar$',views.insumosModificar,name='insumosModificar'),
    url(r'^zonas$',views.zonas,name='zonas'),
    url(r'^zonasAlta$',views.zonasAlta,name='zonasAlta'),
    url(r'^zonasConsulta$',views.zonasConsulta,name='zonasConsulta'),
    url(r'^zonasModificar$',views.zonasModificar,name='zonasMoficar'),
    url(r'^hojaDeRuta$',views.hojaDeRuta,name='hojaDeRuta'),
    url(r'^rendicionReparto$',views.rendicionReparto,name='rendicionReparto'),
    url(r'^cobrarCliente$',views.cobrarCliente,name='cobrarCliente'),
    url(r'^pedidosCliente$',views.pedidosCliente,name='pedidosCliente'),
    url(r'^choferes$',views.choferes,name='choferes'),
    url(r'^choferesModificar$',views.choferesModificar,name='choferesModificar'),
    url(r'^choferesAlta$',views.choferesAlta,name='choferesAlta'),
    url(r'^productosTerminados$',views.productosTerminados,name='productosTerminados'),
    url(r'^productosTerminadosAlta$',views.productosTerminadosAlta,name='productosTerminadosAlta'),
    url(r'^productosTerminadosModificar$',views.productosTerminadosModificar,name='productosTerminadosModificar'),
    url(r'^productosTerminadosActualizarStock',views.productosTerminadosActualizarStock,name='productosTerminadosActualizarStock'),
    url(r'^productosTerminadosActualizarPrecio$',views.productosTerminadosActualizarPrecio,name='productosTerminadosActualizarPrecio'),
    url(r'^pedidosClienteAlta$',views.pedidosClienteAlta,name='pedidosClienteAlta'),
    url(r'^rendicionRepartoPedidos$',views.rendicionRepartoPedidos,name='rendicionRepartoPedidos'),
    url(r'^$',views.login,name='login')


]
