from django.db import models
import uuid
class Produto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    quantidade = models.PositiveIntegerField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    marca = models.CharField(max_length=255)
    litragem = models.DecimalField(max_digits=5, decimal_places=2)
    url_imagem = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.nome} (Marca: {self.marca}, Litragem: {self.litragem}L, Quantidade: {self.quantidade}, Valor:R$ {self.valor:.2f})"
