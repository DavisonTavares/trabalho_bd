from django.shortcuts import render,redirect
from .models import Cliente
from endereco.models import Endereco
from django.views.generic import ListView,CreateView
from django.urls import reverse_lazy

def cliente_form(request):
    return render(request,'cliente\cliente_form.html')

def cadastrar_cliente(request):

    nome = request.POST.get('nome')
    cpf = request.POST.get('cpf')
    telefone = request.POST.get('telefone')
    rua = request.POST.get('rua')
    numero = request.POST.get('numero')
    complemento = request.POST.get('complemento')
    bairro = request.POST.get('bairro')
    cidade = request.POST.get('cidade')
    estado = request.POST.get('estado')
    cep = request.POST.get('cep')
    endereco = Endereco.objects.create(rua=rua,numero=numero,complemento=complemento,bairro=bairro,cidade=cidade,estado=estado,cep=cep)
    Cliente.objects.create(nome=nome, cpf=cpf, telefone=telefone,endereco=endereco)
    return redirect(reverse_lazy("listar_cliente"))

class listarCliente(ListView):
    model = Cliente
