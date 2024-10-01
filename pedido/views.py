# pedido/views.py
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from .models import Pedido
from .forms import PedidoForm

class lista_pedidos(View):
    def get(self, request):
        pedidos = Pedido.objects.all()
        return render(request, 'pedido_lista.html', {'pedidos': pedidos})

class cadastrar_pedido(View):
    def get(self, request):
        form = PedidoForm()
        return render(request, 'pedido_form.html', {'form': form, 'pagina': 'cadastrar'})

    def post(self, request):
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_pedidos')
        return render(request, 'pedido_form.html', {'form': form, 'pagina': 'cadastrar'})

class editar_pedido(View):
    def get(self, request, id):
        pedido = get_object_or_404(Pedido, id_venda=id)
        form = PedidoForm(instance=pedido)
        return render(request, 'pedido_form.html', {'form': form, 'pagina': 'editar', 'pedido': pedido})

    def post(self, request, id):
        pedido = get_object_or_404(Pedido, id_venda=id)
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            return redirect('lista_pedidos')
        return render(request, 'pedido_form.html', {'form': form, 'pagina': 'editar', 'pedido': pedido})

class deletar_pedido(View):
    def get(self, request, id):
        pedido = get_object_or_404(Pedido, id_venda=id)
        return render(request, 'pedido_confirmar_delete.html', {'pedido': pedido})

    def post(self, request, id):
        pedido = get_object_or_404(Pedido, id_venda=id)
        pedido.delete()
        return redirect('lista_pedidos')
