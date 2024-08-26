from django.db import models
from endereco.models import Endereco
import uuid
class Cliente(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=20)
    endereco = models.ForeignKey(Endereco, on_delete=models.PROTECT)
    nome_formatado = models.CharField(max_length=255,editable=False)
    def __str__(self):
        return f"{self.nome} (CPF: {self.cpf})"
