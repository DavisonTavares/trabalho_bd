from django.db import models
from produto.models import Produto
from vendedor.models import Vendedor
from cliente.models import Cliente
import uuid

class Pedido(models.Model):
    id_venda = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    quantidade = models.PositiveIntegerField()
    valor_prod = models.DecimalField(max_digits=10, decimal_places=2)
    id_produto = models.ManyToManyField(Produto, related_name='pedidos') 
    id_vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return (f"Pedido ID: {self.id_venda}, Quantidade: {self.quantidade}, "
                f"Valor: R${self.valor_prod:.2f}, "
                f"Vendedor: {self.id_vendedor.nome}, Cliente: {self.id_cliente.nome}")
