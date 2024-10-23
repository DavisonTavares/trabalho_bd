from django.db import models
from produto.models import Produto
from django.contrib.auth.models import User
from cliente.models import Cliente
import uuid

class Pedido(models.Model):
    id_venda = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_vendedor = models.ForeignKey(User, on_delete=models.CASCADE)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return f"Pedido ID: {self.id_venda}, Vendedor: {self.id_vendedor.nome}, Cliente: {self.id_cliente.nome}"

class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    valor_prod = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Item ID: {self.id}, Produto: {self.produto.nome}, Quantidade: {self.quantidade}, Valor: R${self.valor_prod:.2f}"
