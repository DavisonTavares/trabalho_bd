from django.db import models
import uuid

class Produto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    nomeFormatado = models.CharField(max_length=255, editable=False)
    quantidade = models.PositiveIntegerField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    marca = models.ForeignKey('Marca', on_delete=models.PROTECT)
    litragem = models.DecimalField(max_digits=5, decimal_places=2)
    local_de_fabricacao = models.CharField(max_length=255, blank=True, null=True, default='Brasil')
    url_imagem = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    
    def __str__(self):
        return f"{self.nome} (Marca: {self.marca}, Litragem: {self.litragem}L, Quantidade: {self.quantidade}, Valor:R$ {self.valor:.2f})"

class Marca(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nome
    
