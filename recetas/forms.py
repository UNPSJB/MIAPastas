from django import forms
from . import models

class InsumoForm(forms.ModelForm):
    class Meta:
        model = models.Insumo
        fields = ["nombre", "descripcion", "stock", "unidad_medida"]



class RecetaForm(forms.ModelForm):
    class Meta:
        model = models.Receta
        fields = ["nombre", "Descripcion", "fechaCreacion", "cantProdTerminado","unidad_medida","insumos"]
