from django.urls import reverse
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from cliente.models import Cliente
from .models import Pedido,PedidoItem
from cliente.models import ViewClientesPedido
from vendedor.models import Vendedor
from .forms import PedidoForm, PedidoItemFormSet
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
class lista_pedidos(LoginRequiredMixin, View):
    login_url = '/login/'
    
    def get(self, request,cliente_id):
        if cliente_id:
            cliente = Cliente.objects.filter(id=cliente_id).first()
            if cliente:
            # Busca os pedidos associados ao cliente
                pedidos = Pedido.objects.filter(id_cliente=cliente)
                i = 0
                context = []
                
                # Itera sobre os pedidos e associa os itens do pedido
                for pedido in pedidos:
                    p = PedidoItem.objects.filter(pedido=pedido)
                    soma = sum(item.quantidade * item.valor_prod for item in p)
                    context.append((pedido,soma,p))
                    i+=1

        return render(request, 'pedido_lista.html', {
            'cliente': cliente,
            'context':context,
        })

    def post(self, request,cliente_id):
        search_query = id if id else request.POST.get('search', '')     
        cliente = None
        pedidos = None
        produtos = {}
        if search_query:
            cliente = Cliente.objects.filter(nome__icontains=search_query).first()
            if cliente:
            # Busca os pedidos associados ao cliente
                pedidos = Pedido.objects.filter(id_cliente=cliente)
                i = 0
                context = []
                
                # Itera sobre os pedidos e associa os itens do pedido
                for pedido in pedidos:
                    p = PedidoItem.objects.filter(pedido=pedido)
                    soma = sum(item.quantidade * item.valor_prod for item in p)
                    context.append((pedido,soma,p))
                    i+=1

        
        return render(request, 'pedido_lista.html', {
            'cliente': cliente,
            'context':context,
            
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
            return redirect(reverse('lista_pedidos', args=[pedido.id_cliente.id]))
        return render(request, 'pedido_form.html', {
            'pedido_form': pedido_form,
            'item_formset': item_formset,
            'pagina': 'cadastrar'
        })
    
class deletar_pedido(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, id):
        # Deleta o pedido após a confirmação no POST
        pedido = get_object_or_404(Pedido, id_venda=id)
        id_cliente = pedido.id_cliente
        pedido.delete()  # Remove o pedido
        search_query = request.POST.get('search', '')  # Captura a busca do POST
        return redirect(reverse('lista_pedidos', args=[id_cliente.id])) # Redireciona de volta para a lista de pedidos com pesquisa


