from django import forms
from django.forms import inlineformset_factory
from .models import Pedido, PedidoItem

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['id_vendedor', 'id_cliente']

class PedidoItemForm(forms.ModelForm):
    class Meta:
        model = PedidoItem
        fields = ['produto', 'quantidade', 'valor_prod']
    
PedidoItemFormSet = inlineformset_factory(
    Pedido, PedidoItem,
    form=PedidoItemForm,
    fields=['produto', 'quantidade', 'valor_prod'],
    extra=1,
    can_delete=True
)
