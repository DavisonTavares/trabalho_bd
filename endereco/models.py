from django.db import models
import uuid
class Endereco(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rua = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=255, blank=True, null=True)
    bairro = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=10,null=False,blank=False)

    def __str__(self):
        return f"{self.rua}, {self.numero}, {self.complemento}, {self.bairro}, {self.cidade}-{self.estado}, CEP: {self.cep}"
