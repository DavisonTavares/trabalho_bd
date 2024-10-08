# forms.py
from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'quantidade', 'valor', 'marca', 'litragem', 'local_de_fabricacao', 'url_imagem']
        widgets = {
            'litragem': forms.NumberInput(attrs={'step': '0.01'}),
            'valor': forms.NumberInput(attrs={'step': '0.01'}),
        }
        labels = {
            'litragem': 'litragem (L)',
            'url_imagem': 'URL da imagem'
        }
        def clean_url_imagem(self):
            url_imagem = self.cleaned_data.get('url_imagem')
            if not url_imagem:
                return 'https://i.pinimg.com/736x/a2/2e/55/a22e5584986d9c09b02a382805802469.jpg'
            return url_imagem

class FiltroPrecoForm(forms.Form):
    preco_minimo = forms.DecimalField(required=False, decimal_places=2, max_digits=10, label="Preço Mínimo")
    preco_maximo = forms.DecimalField(required=False, decimal_places=2, max_digits=10, label="Preço Máximo")