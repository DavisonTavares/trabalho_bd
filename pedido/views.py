from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from .models import Pedido
from .forms import PedidoForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

class lista_pedidos(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        pedidos = Pedido.objects.all()
        return render(request, 'pedido_lista.html', {'pedidos': pedidos})

class cadastrar_pedido(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        form = PedidoForm()
        vendedores = User.objects.all()  # Carrega todos os usuários como vendedores
        return render(request, 'pedido_form.html', {'form': form, 'vendedores': vendedores, 'pagina': 'cadastrar'})

    def post(self, request):
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.save()
            form.save_m2m()  # Salva as relações ManyToMany
            return redirect('lista_pedidos')
        vendedores = User.objects.all()
        return render(request, 'pedido_form.html', {'form': form, 'vendedores': vendedores, 'pagina': 'cadastrar'})

class editar_pedido(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, id):
        pedido = get_object_or_404(Pedido, id_venda=id)
        form = PedidoForm(instance=pedido)
        vendedores = User.objects.all()
        return render(request, 'pedido_form.html', {'form': form, 'vendedores': vendedores, 'pagina': 'editar', 'pedido': pedido})

    def post(self, request, id):
        pedido = get_object_or_404(Pedido, id_venda=id)
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.save()
            form.save_m2m()  # Salva as relações ManyToMany
            return redirect('lista_pedidos')
        vendedores = User.objects.all()
        return render(request, 'pedido_form.html', {'form': form, 'vendedores': vendedores, 'pagina': 'editar', 'pedido': pedido})

class deletar_pedido(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, id):
        pedido = get_object_or_404(Pedido, id_venda=id)
        return render(request, 'pedido_confirmar_delete.html', {'pedido': pedido})

    def post(self, request, id):
        pedido = get_object_or_404(Pedido, id_venda=id)
        pedido.delete()
        return redirect('lista_pedidos')
