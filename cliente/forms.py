from django import forms
from .models import Cliente, Endereco

class ClienteForm(forms.ModelForm):
    rua = forms.CharField(max_length=100, required=True)
    numero = forms.CharField(max_length=10, required=True)
    bairro = forms.CharField(max_length=100, required=True)
    cidade = forms.CharField(max_length=100, required=True)
    estado = forms.CharField(max_length=100, required=True)
    cep = forms.CharField(max_length=100, required=True)
    complemento = forms.CharField(max_length=100, required=False)
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'telefone', 'rua', 'numero', 'bairro', 'cidade', 'estado','cep','complemento']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.endereco:
            endereco = self.instance.endereco
            self.fields['rua'].initial = endereco.rua
            self.fields['numero'].initial = endereco.numero
            self.fields['bairro'].initial = endereco.bairro
            self.fields['cidade'].initial = endereco.cidade
            self.fields['estado'].initial = endereco.estado
            self.fields['cep'].initial = endereco.cep
            self.fields['complemento'].initial = endereco.complemento
    