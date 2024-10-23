from django.contrib import admin
from django.urls import path
from cliente.views import cadastrar_cliente,listar_cliente,editar_cliente,deletar_cliente,gerar_relatorio_cliente
from produto.views import cadastrar_produto, editar_produto, listar_produto, deletar_produto, gerar_relatorio, cadastrar_marca
from vendedor.views import cadastrar_vendedor, listar_vendedor, editar_vendedor, deletar_vendedor,gerar_relatorio_vendedor
from vendedor.views import cadastrar_vendedor, listar_vendedor, editar_vendedor, deletar_vendedor, gerar_relatorio_vendedor
from pedido.views import cadastrar_pedido, editar_pedido, deletar_pedido, lista_pedidos
from login.views import login

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
    path('vendedor/editar/<uuid:pk>/', editar_vendedor.as_view(), name='editar_vendedor'),
    path('vendedor/deletar/<uuid:pk>/', deletar_vendedor.as_view(), name='deletar_vendedor'),
    path('gerar_relatorio_vendedor/', gerar_relatorio_vendedor, name='gerar_relatorio_vendedor'),
    path('cadastrar/', cadastrar_pedido.as_view(), name='cadastrar_pedido'),
    path('editar/<uuid:id>/', editar_pedido.as_view(), name='editar_pedido'),
    path('deletar/<uuid:id>/', deletar_pedido.as_view(), name='deletar_pedido'),
    path('lista_pedidos/', lista_pedidos.as_view(), name='lista_pedidos'),
    path('login/', login, name='login'),
]
