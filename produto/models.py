from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    id = models.AutoField(primary_key=True)
    quantidade = models.PositiveIntegerField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    marca = models.CharField(max_length=255)
    litragem = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.nome} (Marca: {self.marca}, Litragem: {self.litragem}L, Quantidade: {self.quantidade}, Valor:R$ {self.valor:.2f})"
