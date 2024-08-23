
from django.contrib import admin
from django.urls import path
from cliente.views import cadastrar_cliente,listarCliente
from produto.views import criarProduto
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', listarCliente.as_view(),name="listar_cliente"),
    path('cadastrar_cliente', cadastrar_cliente, name='cadastrar_cliente'),
    path('cadastrar_poduto',criarProduto.as_view(),name="cadastrar_poduto"),
]
