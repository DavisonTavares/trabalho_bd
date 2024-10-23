from django.db import models
from endereco.models import Endereco
import uuid
class Cliente(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=20)
    endereco = models.ForeignKey(Endereco, on_delete=models.PROTECT)
    time = models.CharField(max_length=15, default="")
    audiovisual = models.CharField(max_length=20, default="")
    naturalidade_cidade = models.CharField(max_length=30, default="")
    naturalidade_estado = models.CharField(max_length=30, default="")
    nome_formatado = models.CharField(max_length=255,editable=False)
    naturalidade_cidade_formatado = models.CharField(max_length=30,editable=False, default="")
    naturalidade_estado_formatado = models.CharField(max_length=30,editable=False, default="")
    def __str__(self):
        return f"{self.nome} (CPF: {self.cpf})"
class ViewClientes(models.Model):
    nome = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20)
    endereco = models.CharField(max_length=500)  # Ajuste o max_length conforme necessário

    class Meta:
        managed = False  # Isso indica que o Django não deve tentar criar ou migrar essa tabela
        db_table = 'view_clientes'
class ViewClientesPedido(models.Model):
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14)
    telefone = models.CharField(max_length=20)
    endereco = models.CharField(max_length=500)  # Ajuste o max_length conforme necessário
    time = models.CharField(max_length=15, default="")
    audiovisual = models.CharField(max_length=20, default="")
    class Meta:
        managed = False  # Isso indica que o Django não deve tentar criar ou migrar essa tabela
        db_table = 'view_clientes_pedido'