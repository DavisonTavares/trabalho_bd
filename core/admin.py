from django.contrib import admin
from .models import Endereco, Cliente, Pedido, Produto, Vendedor

admin.site.register(Endereco)
admin.site.register(Cliente)
admin.site.register(Pedido)
admin.site.register(Produto)
admin.site.register(Vendedor)

