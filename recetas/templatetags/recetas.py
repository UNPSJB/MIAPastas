from django import template

register = template.Library()

@register.simple_tag
def producto_id(detalle):
    if detalle.producto_terminado is not None:
        return detalle.producto_terminado.pk
    else:
        return detalle.pedido_cliente_detalle.producto_terminado.pk