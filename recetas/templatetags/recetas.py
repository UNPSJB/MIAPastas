from django import template

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
	for d in entrega.pedido.pedidoclientedetalle_set.all():
		if d.producto_terminado == prod:
			return d.id
	return ""

@register.simple_tag
def devolver_producto(entrega,prod):
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


