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
    def save(self, commit=True):
        # Salva o cliente sem confirmar ainda
        cliente = super().save(commit=False)

        # Atualiza o endereço existente ou cria um novo endereço
        if self.instance.endereco:
            # Atualiza o endereço existente associado ao cliente
            endereco = self.instance.endereco
            endereco.rua = self.cleaned_data['rua']
            endereco.numero = self.cleaned_data['numero']
            endereco.bairro = self.cleaned_data['bairro']
            endereco.cidade = self.cleaned_data['cidade']
            endereco.estado = self.cleaned_data['estado']
            endereco.cep = self.cleaned_data['cep']
            endereco.complemento = self.cleaned_data['complemento']
            if commit:
                endereco.save()
        else:
            # Cria um novo endereço ou obtém um existente com os mesmos dados
            endereco, created = Endereco.objects.get_or_create(
                rua=self.cleaned_data['rua'],
                numero=self.cleaned_data['numero'],
                bairro=self.cleaned_data['bairro'],
                cidade=self.cleaned_data['cidade'],
                estado=self.cleaned_data['estado'],
                cep=self.cleaned_data['cep'],
                complemento=self.cleaned_data['complemento']
            )
            cliente.endereco = endereco

        if commit:
            # Salva o cliente com o endereço atualizado ou novo
            cliente.save()

        return cliente