from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from .models import Produto
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Produto
from .forms import ProdutoForm

def deletar_produto(request, produto_id):
    if request.method == 'POST':    
        Produto.objects.filter(id=produto_id).delete()
        return redirect(reverse_lazy('lista_produtos'))
    return HttpResponse(status=404)

def editar_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        url_imagem = form.cleaned_data.get('url_imagem') or 'https://i.pinimg.com/736x/a2/2e/55/a22e5584986d9c09b02a382805802469.jpg'
        if form.is_valid():
            Produto.objects.filter(id=produto_id).update(
                nome=form.cleaned_data['nome'],
                quantidade=form.cleaned_data['quantidade'],
                valor=form.cleaned_data['valor'],
                marca=form.cleaned_data['marca'],
                litragem=form.cleaned_data['litragem'],
                url_imagem=url_imagem
            )
            return redirect(reverse_lazy('lista_produtos'))
    else:
        form = ProdutoForm(instance=produto)
    
    return render(request, 'produto/produto_form.html', {'form': form, 'titlebutton': 'Editar', 'produto_id': produto_id})

    
def cadastrar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if not form.is_valid():
            return render(request, 'produto/produto_form.html', {'form': form})
    
      # Criando o objeto Produto e salvando no banco de dados
        Produto.objects.create(
            nome=form.cleaned_data['nome'],
            quantidade=form.cleaned_data['quantidade'],
            valor=form.cleaned_data['valor'],
            marca=form.cleaned_data['marca'],
            litragem=form.cleaned_data['litragem'],
            url_imagem=form.cleaned_data['url_imagem']
        )
        
        # Redirecionando após o cadastro
        return redirect(reverse_lazy('lista_produtos'))
    
    # Se o método for GET, renderize o formulário
    return render(request, 'produto/produto_form.html', {'form': ProdutoForm(), 'titlebutton': 'Cadastrar'})

def listar_produto(request):
    produtos = Produto.objects.all()
    return render(request, 'produto/produto_list.html', {'produtos': produtos})

