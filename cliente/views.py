from django.http import HttpRequest, HttpResponse
from django.shortcuts import render,redirect
from .models import Cliente
from endereco.models import Endereco
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from .forms import ClienteForm

class cadastrar_cliente(CreateView):
    def get(self, request, *args, **kwargs):
        return render(request,'cliente\cadastrar_cliente.html')
    def post(self, request, *args, **kwargs):   
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

class listar_cliente(ListView):
    model = Cliente

class editar_cliente(UpdateView):
    template_name = 'cliente\cliente_edit.html'
    model = Cliente
    form_class = ClienteForm
    success_url = reverse_lazy("listar_cliente")
class deletar_cliente(DeleteView):
    template_name = 'cliente\confirmar_apagar_cliente.html'
    model = Cliente
    success_url = reverse_lazy("listar_cliente")