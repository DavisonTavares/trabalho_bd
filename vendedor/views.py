from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from .models import Vendedor
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import VendedorForm
from django.db import IntegrityError, OperationalError
from fpdf import FPDF
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import  UserPassesTestMixin


class cadastrar_vendedor(UserPassesTestMixin, CreateView):
    login_url = '/lista_produtos/'
    def test_func(self):
        # Verifica se o usuário é um superusuário
        return self.request.user.is_superuser
    model = User
    form_class = VendedorForm
    template_name = 'vendedor/vendedor_form.html'
    success_url = reverse_lazy('listar_vendedor')

    def form_valid(self, form):
        try:
            # Aqui criamos o usuário usando o método 'create_user' que já trata a senha corretamente
            User.objects.create_user(
                username=form.cleaned_data['nome'], 
                email=form.cleaned_data['email'], 
                password=form.cleaned_data['senha']
            )
            return redirect(self.success_url)
        except IntegrityError:
            # Captura um erro de integridade (como duplicação de email ou nome de usuário)
            form.add_error(None, "Erro de integridade: Dados inválidos.")
            return self.form_invalid(form)
        except OperationalError:
            # Captura erros relacionados ao banco de dados
            form.add_error(None, "Erro operacional: Problema com o banco de dados.")
            return self.form_invalid(form)
        except Exception as e:
            # Captura qualquer outro tipo de erro inesperado
            form.add_error(None, f"Erro inesperado: {e}")
            return self.form_invalid(form)

class listar_vendedor(UserPassesTestMixin, ListView):
    login_url = '/lista_produtos/'
    def test_func(self):
        # Verifica se o usuário é um superusuário
        return self.request.user.is_superuser
    model = User  # Modelo que será listado
    template_name = 'vendedor/vendedor_list.html'  # Template a ser renderizado
    context_object_name = 'vendedores'  # Nome do contexto para o template

    def get_queryset(self):
        # Defina o queryset que será listado
        return User.objects.all()

class editar_vendedor(UserPassesTestMixin, UpdateView):
    login_url = '/lista_produtos/'
    def test_func(self):
        # Verifica se o usuário é um superusuário
        return self.request.user.is_superuser
    model = User
    form_class = VendedorForm
    template_name = 'vendedor/vendedor_form.html'
    success_url = reverse_lazy('listar_vendedor')
    
class deletar_vendedor(UserPassesTestMixin, DeleteView):
    login_url = '/lista_produtos/'
    def test_func(self):
        # Verifica se o usuário é um superusuário
        return self.request.user.is_superuser
    model = User
    template_name = 'vendedor/vendedor_delete.html'
    success_url = reverse_lazy('listar_vendedor')
def superuser_required(u):
    return u.is_superuser

@user_passes_test(superuser_required)
def gerar_relatorio_vendedor(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_vendedor.pdf"'
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, 'Relatório de Vendedores')
    
    vendedores = User.objects.all()
    for vendedor in vendedores:
        pdf.set_font('Arial', '', 12)
        pdf.ln(10)
        pdf.cell(0, 10, f'Nome: {vendedor.first_name}')
        pdf.ln(10)
        pdf.cell(0, 10, f'Email: {vendedor.email}')
        pdf.ln(10)
    
    response.write(pdf.output(dest='S').encode('latin1'))
    return response