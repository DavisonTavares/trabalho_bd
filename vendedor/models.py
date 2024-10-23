from django.db import models
import uuid
class Vendedor(models.Model):
    nome = models.CharField(max_length=255)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return f"{self.nome} (ID: {self.id})"
