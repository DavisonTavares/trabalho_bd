from django import forms
from django.contrib.auth.models import User

class VendedorForm(forms.ModelForm):
    nome = forms.CharField(max_length=255, label="Nome")
    senha = forms.CharField(widget=forms.PasswordInput(), label="Senha")

    class Meta:
        model = User
        fields = ['nome', 'email', 'senha']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['nome']  # Mapeando 'nome' para 'first_name'
        user.set_password(self.cleaned_data['senha'])  # Salvando a senha corretamente
        if commit:
            user.save()
        return user
