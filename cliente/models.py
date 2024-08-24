from django.db import models
from endereco.models import Endereco
class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=20)
    endereco = models.ForeignKey(Endereco, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.nome} (CPF: {self.cpf})"
