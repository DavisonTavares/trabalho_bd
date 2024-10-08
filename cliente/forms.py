from django import forms
from .models import Cliente, Endereco

class ClienteForm(forms.ModelForm):
    nome = forms.CharField(max_length=100)
    cpf = forms.CharField(max_length=14)
    time = forms.CharField(max_length=15)
    audiovisual = forms.CharField(max_length=15)
    naturalidade_cidade = forms.CharField(max_length=30)
    naturalidade_estado = forms.CharField(max_length=30)
    telefone = forms.CharField(max_length=15)
    rua = forms.CharField(max_length=100)
    numero = forms.CharField(max_length=10)
    complemento = forms.CharField(max_length=100, required=False)
    bairro = forms.CharField(max_length=100)
    cidade = forms.CharField(max_length=100)
    estado = forms.CharField(max_length=2)
    cep = forms.CharField(max_length=10)
    class Meta:
        model = Cliente
        fields = ['nome','time','audiovisual','naturalidade_cidade','naturalidade_estado', 'cpf', 'telefone', 'estado','cep','complemento']

    
    