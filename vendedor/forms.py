from django import forms
from .models import Vendedor

class VendedorForm(forms.ModelForm):
    nome = forms.CharField(max_length=255)

    class Meta:
        model = Vendedor
        fields = ['nome']
