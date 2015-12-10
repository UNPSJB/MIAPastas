# este script es para limpiar datos para debugg en Mia Pastas #
# borra todos los lotes.#
# stock de prod terminados = 0#
# saldo en clientes = 0#
# borra todas las hoja de ruta #
# borra todas las facturas #
# borra todos los resibos.#

from recetas import models

for c in models.Cliente.objects.all():
	c.saldo=0
	c.save()

for p in models.ProductoTerminado.objects.all():
	p.stock=0
	p.save()

for l in models.Lote.objects.all():
	l.delete()

for h in models.HojaDeRuta.objects.all():
	h.delete()

for f in models.Factura.objects.all():
	f.delete()

for f in models.Recibo.objects.all():
	f.delete()

