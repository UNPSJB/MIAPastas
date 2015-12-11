from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()

@register.simple_tag
def producto_id(detalle):
    if detalle.producto_terminado is not None:
        return detalle.producto_terminado.pk
    else:
        return detalle.pedido_cliente_detalle.producto_terminado.pk

@register.simple_tag
def producto_nombre(detalle):
    if detalle.producto_terminado is not None:
        return detalle.producto_terminado.nombre
    else:
        return detalle.pedido_cliente_detalle.producto_terminado.nombre

@register.simple_tag
def producto_cantidad(detalle):
    if detalle.producto_terminado is not None:
        return 0
    else:
        return detalle.pedido_cliente_detalle.cantidad_producto

@register.simple_tag
def devolver_cantidad_pedida_entrega(entrega,prod):
    """ metodo que resiba una Entrega y un producto
        se recorre los detalles del pedido que apunta la entrega buscando el Producto resibido
        Si lo encuentra devuelve la cantidad pedida que indica el detalle de pedido
        Si no lo encuentra devuelve 0 
    """
    for d in entrega.pedido.pedidoclientedetalle_set.all():
    	if d.producto_terminado == prod:
    		return d.cantidad_producto
    return 0

@register.simple_tag
def devolver_cantidad_pedida(detalle):
    """ metodo resibe un detalle de entrega.
        si este detalle tiene asociado un detalle de pedido, devuelve cantidad pedida que indica el detalle de pedido
        si este detalle no tiene asociado un detalle de pedido, devuelve 0
    """
    if detalle.producto_terminado is not None:
        return 0
    else:
        return detalle.pedido_cliente_detalle.cantidad_producto


@register.simple_tag
def devolver_detalle(entrega,prod):
    """ Recibe una Entrega y un ProductoTerminado p
        retorna una cadena vacia si no encuentra ningun detalle de pedido que apunte a p
        retorna un detalle de pedido que coincida con p
    """
    for d in entrega.pedido.pedidoclientedetalle_set.all():
		if d.producto_terminado == prod:
		    return d.id
    return ""

@register.simple_tag
def devolver_producto(entrega,prod):
    """Recibe una Entrega y un ProductoTerminado p
        retorna una cadena vacia si encuentra un detalle de pedido que apunte a p
        retorna el id del producto en caso que no se encuentre ningun detalle relacionado con p 
    """
    for d in entrega.pedido.pedidoclientedetalle_set.all():
		if d.producto_terminado == prod:
			return ""
    return prod.id

@register.simple_tag
def saldos_totales(clientes):
	cant=0.0
	for c in clientes:
         cant+=c.saldo
	return cant

@register.simple_tag
def devolver_len(algo):
    return len(algo)
    

@register.simple_tag
def stock_totales(productos):
	cant=0.0
	for p in productos:
         cant+=p.stock
	return cant

@register.simple_tag
def devolver_precio_total(entrega):
    """ Recibe un objeto Entrega
        Recorre sus detalles sumando el precio que tenga cada uno para obtener el precio total
        detalles deben tener en precio, el precio total (precio prod * cantidad entregada)
        retorna precio total
    """
    count = 0
    for d in entrega.entregadetalle_set.all():
        count += d.precio
    return count


@register.filter
def producto_fue_llevado(h,p):
    """ Recibe un producto y lo busca en la hoja.
        devuelve True si lo encuentra y cantidad enviada > 0
        Falso si no lo encuentra o no se envio nada
    """
    esta = False
    print "producto fue  llevado",p
    for c in h.productosllevados_set.all():        
        if c.producto_terminado == p and c.cantidad_enviada>0:        
            esta =  True
            break    
    if  esta:
        return True    
    return False

