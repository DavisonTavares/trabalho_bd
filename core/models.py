from django.db import models


class Endereco(models.Model):
    rua = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=255, blank=True, null=True)
    bairro = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.rua}, {self.numero}, {self.complemento}, {self.bairro}, {self.cidade}-{self.estado}, CEP: {self.cep}"

class Cliente(models.Model):
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=20)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome} (CPF: {self.cpf})"
    
class Produto(models.Model):
    nome = models.CharField(max_length=255)
    id = models.AutoField(primary_key=True)
    quantidade = models.PositiveIntegerField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    marca = models.CharField(max_length=255)
    litragem = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.nome} (Marca: {self.marca}, Litragem: {self.litragem}L, Quantidade: {self.quantidade}, Valor:R$ {self.valor:.2f})"
    
class Vendedor(models.Model):
    nome = models.CharField(max_length=255)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.nome} (ID: {self.id})"

class Pedido(models.Model):
    id_venda = models.AutoField(primary_key=True)
    quantidade = models.PositiveIntegerField()
    valor_prod = models.DecimalField(max_digits=10, decimal_places=2)
    id_produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    id_vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return (f"Pedido ID: {self.id_venda}, Produto: {self.id_produto.nome}, "
                f"Quantidade: {self.quantidade}, Valor: R${self.valor_prod:.2f}, "
                f"Vendedor: {self.id_vendedor.nome}, Cliente: {self.id_cliente.nome}")

