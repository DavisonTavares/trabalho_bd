from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from cliente.models import Cliente
from .models import Pedido
from cliente.models import ViewClientesPedido
from vendedor.models import Vendedor
from .forms import PedidoForm, PedidoItemFormSet
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
class lista_pedidos(LoginRequiredMixin, View):
    login_url = '/login/'
    
    def get(self, request):
        return render(request, 'pedido_lista.html')

    def post(self, request):
        search_query = request.POST.get('search', '')  
        cliente = None
        pedidos = None

        if search_query:
            cliente = Cliente.objects.filter(nome__icontains=search_query).first()
            if cliente:
                pedidos = Pedido.objects.filter(id_cliente=cliente)
                

        return render(request, 'pedido_lista.html', {
            'cliente': cliente,
            'pedidos': pedidos,
            'search_query': search_query
        })

class cadastrar_pedido(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        pedido_form = PedidoForm()
        item_formset = PedidoItemFormSet()
        clientes = ViewClientesPedido.objects.all()
        return render(request, 'pedido_form.html', {
            'pedido_form': pedido_form,
            'item_formset': item_formset,
            'clientes': serializers.serialize('json', clientes),
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
