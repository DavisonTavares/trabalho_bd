from django.http import HttpResponse, JsonResponse,HttpResponseNotFound
from django.shortcuts import render,redirect
from .models import Cliente
from endereco.models import Endereco
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from .forms import ClienteForm
from django.db import IntegrityError, OperationalError
def limpar_cpf(cpf):
    """Remove caracteres não numéricos do CPF."""
    return ''.join(filter(str.isdigit, cpf))

def limpar_cep(cep):
    """Remove caracteres não numéricos do CEP."""
    return ''.join(filter(str.isdigit, cep))

def limpar_telefone(telefone):
    """Remove caracteres não numéricos do telefone."""
    return ''.join(filter(str.isdigit, telefone))
def formatar_cpf(cpf):
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
def formatar_cep(cep):
        return f"{cep[:5]}-{cep[5:]}"
def formatar_telefone(telefone):
        return f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"

class cadastrar_cliente(CreateView):
    def get(self, request, *args, **kwargs):
        return render(request,'cliente\cadastrar_cliente.html')
    def post(self, request, *args, **kwargs):   
        campos_cliente = ['nome', 'cpf', 'telefone','endereco']
        campos_endereco =['rua', 'numero', 'complemento', 'bairro', 'cidade', 'estado', 'cep']
        # Lista para armazenar os dados
        dados_cliente = []
        dados_endereco = []
        # Coleta os dados usando request.POST.get para cada campo
        for campo in campos_cliente:
            if campo == 'endereco':
                continue  # Pula o campo 'endereco'

            valor = request.POST.get(campo)
            if campo == 'cpf':
                valor = limpar_cpf(valor)
            if campo == 'telefone':
                valor = limpar_telefone(valor)

            dados_cliente.append(valor)
        for campo in campos_endereco:
            valor = request.POST.get(campo)
            if campo == 'cep':
                valor = limpar_cep(valor)
            dados_endereco.append(valor)
        try:
            dados_endereco = dict(zip(campos_endereco, dados_endereco))
            endereco = Endereco.objects.create(**dados_endereco)
            dados_cliente.append(endereco)
            dados_cliente = dict(zip(campos_cliente, dados_cliente))
            Cliente.objects.create(**dados_cliente)
        except IntegrityError:
            # Lida com erros relacionados à integridade dos dados
            return HttpResponse("Erro de integridade: Dados inválidos ou violação de chave única.", status=400)
        except OperationalError:
            # Lida com erros operacionais
            return HttpResponse("Erro operacional: Problema com o banco de dados.", status=500)
        except Exception as e:
            # Lida com qualquer outro erro inesperado
            return HttpResponse(f"Erro inesperado: {e}", status=500)
        return redirect(reverse_lazy("lista_clientes"))

class listar_cliente(ListView):
    model = Cliente

class editar_cliente(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente\cliente_edit.html'
    def campos_alterados(self,cliente,endereco,dados):
        campos_cliente = {}
        campos_endereco = {}
        # Atualiza campos do cliente
        if dados['cpf'] != cliente.cpf:
            campos_cliente['cpf'] = dados['cpf']
        if dados['nome'] != cliente.nome:
            campos_cliente['nome'] = dados['nome']
        if dados['telefone'] != cliente.telefone:
            campos_cliente['telefone'] = dados['telefone']
        # Atualiza campos do endereço
        if dados['rua'] != endereco.rua:
            campos_endereco['rua'] = dados['rua']
        if dados['numero'] != endereco.numero:
            campos_endereco['numero'] = dados['numero']
        if dados['complemento'] != endereco.complemento:
            campos_endereco['complemento'] = dados['complemento']
        if dados['bairro'] != endereco.bairro:
            campos_endereco['bairro'] = dados['bairro']
        if dados['cidade'] != endereco.cidade:
            campos_endereco['cidade'] = dados['cidade']
        if dados['estado'] != endereco.estado:
            campos_endereco['estado'] = dados['estado']
        if dados['cep'] != endereco.cep:
            campos_endereco['cep'] = dados['cep']
        return campos_cliente, campos_endereco
    def get(self, request, *args, **kwargs):
        # Recupera o cliente usando um identificador (exemplo: 'pk' ou 'cpf')
        id = kwargs.get('pk', None)
        cliente = Cliente.objects.get(id=id)
        endereco = cliente.endereco
        # Inicializa o formulário com dados existentes
        cpf = formatar_cpf(cliente.cpf)
        cep = formatar_cep(endereco.cep)
        telefone = formatar_telefone(cliente.telefone)
        cliente = {
            'id': id,
            'nome': cliente.nome,
            'cpf': cpf,
            'telefone': telefone,
            'rua': endereco.rua,
            'numero': endereco.numero,
            'complemento': endereco.complemento,
            'bairro': endereco.bairro,
            'cidade': endereco.cidade,
            'estado': endereco.estado,
            'cep': cep
        }
        return render(request, self.template_name, {'cliente': cliente})
    def post(self, request, *args, **kwargs):
        try:        
            id = kwargs.get('pk', None)
            nome = request.POST.get('nome')
            cpf = limpar_cpf(request.POST.get('cpf'))
            telefone = limpar_telefone(request.POST.get('telefone'))
            rua = request.POST.get('rua')
            numero = request.POST.get('numero')
            complemento = request.POST.get('complemento')
            bairro = request.POST.get('bairro')
            cidade = request.POST.get('cidade')
            estado = request.POST.get('estado')
            cep = limpar_cep(request.POST.get('cep'))
            dados = {
            'nome': nome,
            'cpf': cpf,
            'telefone': telefone,
            'rua': rua,
            'numero': numero,
            'complemento': complemento,
            'bairro': bairro,
            'cidade': cidade,
            'estado': estado,
            'cep': cep
            }
            cliente = Cliente.objects.get(id=id)
            endereco = cliente.endereco
            campos_cliente, campos_endereco = self.campos_alterados(cliente,endereco,dados)
            Cliente.objects.filter(id=id).update(**campos_cliente)
            Endereco.objects.filter(id=endereco.id).update(**campos_endereco)
        except IntegrityError:
            # Lida com erros relacionados à integridade dos dados
            return HttpResponse("Erro de integridade: Dados inválidos ou violação de chave única.", status=400)
        except OperationalError:
            # Lida com erros operacionais
            return HttpResponse("Erro operacional: Problema com o banco de dados.", status=500)
        except Exception as e:
            # Lida com qualquer outro erro inesperado
            return HttpResponse(f"Erro inesperado: {e}", status=500)
        # redireciona caso operação bem sucedida
        return redirect(reverse_lazy("lista_clientes"))
    
class deletar_cliente(DeleteView):
    def get(self, request, *args, **kwargs):
        try:
            id = kwargs.get('pk', None)
            cliente = Cliente.objects.get(id=id)
        except Cliente.DoesNotExist:
            return HttpResponseNotFound('Cliente não encontrado.')
        except OperationalError:
            # Lida com erros operacionais
            return HttpResponse("Erro operacional: Problema com o banco de dados.", status=500)
        except Exception as e:
            # Lida com qualquer outro erro inesperado
            return HttpResponse(f"Erro inesperado: {e}", status=500) 
        # redireciona caso operação bem sucedida 
        return render(request,'cliente\confirmar_apagar_cliente.html',{"cliente": cliente})   
    model = Cliente
    success_url = reverse_lazy("listar_cliente")
    def delete(self, request, *args, **kwargs):
        id = kwargs.get('pk', None)
        if id is None:
            return HttpResponseNotFound('Cliente não encontrado.')
        try:
            cliente = Cliente.objects.get(id=id)
            endereco = cliente.endereco
            cliente.delete()  # Deleta o cliente
            endereco.delete()  # Deleta o endereço
            return JsonResponse({'message': 'Cliente excluído com sucesso.'}, status=200)
        except Cliente.DoesNotExist:
            return HttpResponseNotFound('Cliente não encontrado.')
        except Exception as e:
            return JsonResponse({'message': 'Erro ao excluir cliente.', 'error': str(e)}, status=500)