
from django.contrib import admin
from django.urls import path
from cliente.views import cadastrar_cliente,listar_cliente,editar_cliente,deletar_cliente,gerar_relatorio_cliente
from produto.views import cadastrar_produto, editar_produto, listar_produto, deletar_produto, gerar_relatorio, cadastrar_marca
from vendedor.views import cadastrar_vendedor, listar_vendedor, editar_vendedor, deletar_vendedor, gerar_relatorio_vendedor
urlpatterns = [
    path('admin/', admin.site.urls),
    path('lista_clientes/', listar_cliente.as_view(),name="lista_clientes"),
    path('', listar_cliente.as_view(),name="home"),
    path('cadastrar_cliente/', cadastrar_cliente.as_view(), name='cadastrar_cliente'),
    path('editar_cliente/<uuid:cliente_id>/',editar_cliente.as_view(),name="editar_cliente"),
    path('deletar_cliente/<uuid:cliente_id>/',deletar_cliente.as_view(),name="deletar_cliente"),
    path('gerar_relatorio_cliente/', gerar_relatorio_cliente, name='gerar_relatorio_cliente'),
    path('cadastrar_poduto/',cadastrar_produto,name="cadastrar_produto"),
    path('editar_produto/<uuid:produto_id>/', editar_produto, name='editar_produto'),
    path('deletar_produto/<uuid:produto_id>/', deletar_produto, name='deletar_produto'),
    path('gerar_relatorio/', gerar_relatorio, name='gerar_relatorio'),
    path('cadastrar_marca/', cadastrar_marca, name='cadastrar_marca'),
    path('lista_produtos/',listar_produto,name="lista_produtos"),
    path('vendedor/cadastrar/', cadastrar_vendedor.as_view(), name='cadastrar_vendedor'),
    path('vendedor/listar', listar_vendedor.as_view(), name='listar_vendedor'),
    path('vendedor/editar/<int:pk>/', editar_vendedor.as_view(), name='editar_vendedor'),
    path('vendedor/deletar/<int:pk>/', deletar_vendedor.as_view(), name='deletar_vendedor'),
    path('gerar_relatorio_vendedor/', gerar_relatorio_vendedor, name='gerar_relatorio_cliente'),
]
