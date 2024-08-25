
from django.contrib import admin
from django.urls import path
from cliente.views import cadastrar_cliente,listar_cliente,editar_cliente,deletar_cliente
from produto.views import cadastrar_produto, editar_produto, listar_produto
urlpatterns = [
    path('admin/', admin.site.urls),
    path('lista_clientes', listar_cliente.as_view(),name="lista_clientes"),
    path('', listar_cliente.as_view(),name="home"),
    path('cadastrar_cliente', cadastrar_cliente.as_view(), name='cadastrar_cliente'),
    path('cadastrar_poduto/',cadastrar_produto,name="cadastrar_produto"),
    path('editar_produto/<uuid:produto_id>/', editar_produto, name='editar_produto'),
    path('lista_produtos/',listar_produto,name="lista_produtos"),
    path('editar_cliente/<int:pk>',editar_cliente.as_view(),name="editar_cliente"),
    path('deletar_cliente/<int:pk>',deletar_cliente.as_view(),name="deletar_cliente"),
]
