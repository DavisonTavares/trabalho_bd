from django import forms
from .models import Pedido
from produto.models import Produto
from vendedor.models import Vendedor
from cliente.models import Cliente

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['quantidade', 'valor_prod', 'id_produto', 'id_vendedor', 'id_cliente']
        
    quantidade = forms.IntegerField(min_value=1, label='Quantidade')
    valor_prod = forms.DecimalField(max_digits=10, decimal_places=2, label='Valor do Produto')
    id_produto = forms.ModelChoiceField(queryset=Produto.objects.all(), label='Produto')
    id_vendedor = forms.ModelChoiceField(queryset=Vendedor.objects.all(), label='Vendedor')
    id_cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), label='Cliente')
