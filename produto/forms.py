# forms.py
from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'quantidade', 'valor', 'marca', 'litragem', 'url_imagem']
        widgets = {
            'litragem': forms.NumberInput(attrs={'step': '0.01'}),
            'valor': forms.NumberInput(attrs={'step': '0.01'}),
        }
