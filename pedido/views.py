from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from .models import Pedido
from .forms import PedidoForm, PedidoItemFormSet
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
        pedido_form = PedidoForm()
        item_formset = PedidoItemFormSet()
        return render(request, 'pedido_form.html', {
            'pedido_form': pedido_form,
            'item_formset': item_formset,
            'pagina': 'cadastrar'
        })

    def post(self, request):
        pedido_form = PedidoForm(request.POST)
        item_formset = PedidoItemFormSet(request.POST)
        if pedido_form.is_valid() and item_formset.is_valid():
            pedido = pedido_form.save()
            itens = item_formset.save(commit=False)
            for item in itens:
                item.pedido = pedido
                item.save()
            return redirect('lista_pedidos')
        return render(request, 'pedido_form.html', {
            'pedido_form': pedido_form,
            'item_formset': item_formset,
            'pagina': 'cadastrar'
        })

class editar_pedido(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, id):
        pedido = get_object_or_404(Pedido, id_venda=id)
        pedido_form = PedidoForm(instance=pedido)
        item_formset = PedidoItemFormSet(instance=pedido)
        return render(request, 'pedido_form.html', {
            'pedido_form': pedido_form,
            'item_formset': item_formset,
            'pagina': 'editar',
            'pedido': pedido
        })

    def post(self, request, id):
        pedido = get_object_or_404(Pedido, id_venda=id)
        pedido_form = PedidoForm(request.POST, instance=pedido)
        item_formset = PedidoItemFormSet(request.POST, instance=pedido)
        if pedido_form.is_valid() and item_formset.is_valid():
            pedido = pedido_form.save()
            itens = item_formset.save(commit=False)
            for item in itens:
                item.pedido = pedido
                item.save()
            for item in item_formset.deleted_objects:
                item.delete()
            return redirect('lista_pedidos')
        return render(request, 'pedido_form.html', {
            'pedido_form': pedido_form,
            'item_formset': item_formset,
            'pagina': 'editar',
            'pedido': pedido
        })

class deletar_pedido(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, id):
        pedido = get_object_or_404(Pedido, id_venda=id)
        return render(request, 'pedido_confirmar_delete.html', {'pedido': pedido})

    def post(self, request, id):
        pedido = get_object_or_404(Pedido, id_venda=id)
        pedido.delete()
        return redirect('lista_pedidos')
