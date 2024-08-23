from django.shortcuts import render
from .models import Cliente

def home(request):
    client = Cliente.objects.all()
    return render(request, 'index.html', {'clients': client})

def add_client(request):
    nome = request.POST.get('nome')
    cpf = request.POST.get('cpf')
    telefone = request.POST.get('telefone')
    cidade = request.POST.get('cidade')
    profissao = request.POST.get('profissao')
    Cliente.objects.create(nome=nome, cpf=cpf, telefone=telefone, cidade=cidade, profissao=profissao)
    return render(request, 'index.html', {'clients': Cliente.objects.all()})