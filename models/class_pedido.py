from django.db import models
from class_produto import Produto
from class_vendedor import Vendedor
from class_cliente import Cliente
class Pedido(models.Model):
    id_venda = models.AutoField(primary_key=True)
    quantidade = models.PositiveIntegerField()
    valor_prod = models.DecimalField(max_digits=10, decimal_places=2)
    id_produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    id_vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return (f"Pedido ID: {self.id_venda}, Produto: {self.id_produto.nome}, "
                f"Quantidade: {self.quantidade}, Valor: R${self.valor_prod:.2f}, "
                f"Vendedor: {self.id_vendedor.nome}, Cliente: {self.id_cliente.nome}")
