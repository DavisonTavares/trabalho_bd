from django.http import HttpResponse, JsonResponse,HttpResponseNotFound
from django.shortcuts import render,redirect
from .models import Cliente
from endereco.models import Endereco
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from .forms import ClienteForm
from django.db import IntegrityError, OperationalError
from fpdf import FPDF
def limpar_cpf(cpf):
    return ''.join(filter(str.isdigit, cpf))

def limpar_cep(cep):
    return ''.join(filter(str.isdigit, cep))

def limpar_telefone(telefone):
    return ''.join(filter(str.isdigit, telefone))
def formatar_cpf(cpf):
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
def formatar_cep(cep):
        return f"{cep[:5]}-{cep[5:]}"
def formatar_telefone(telefone):
        return f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"

class cadastrar_cliente(CreateView):
    template_name = 'cliente\cliente_form.html'
    def cliente_return(self,id, cliente, endereco):
        cpf = formatar_cpf(cliente["cpf"])
        cep = formatar_cep(endereco["cep"])
        telefone = formatar_telefone(cliente["telefone"])
        cliente = {
            'id': id,
            'nome': cliente["nome"], 
            'cpf': cpf,
            'telefone': telefone,
            'rua': endereco["rua"],
            'numero': endereco["numero"],
            'complemento': endereco["complemento"],
            'bairro': endereco["bairro"],
            'cidade': endereco["cidade"],
            'estado': endereco["estado"],
            'cep': cep
        }
        return cliente
    def get(self, request, *args, **kwargs):
        return render(request,self.template_name,{'cliente':False} )
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
            cliente = self.cliente_return(0,dados_cliente,dados_endereco)
            return render(request, self.template_name, {'cliente':cliente, 'erro': f"Dados inválidos ou CPF já cadastrado."})
        except OperationalError:
            cliente = self.cliente_return(0,dados_cliente,dados_endereco)
            return render(request, self.template_name, {'cliente':cliente, 'erro': f"Problema com o banco de dados."})
        except Exception as e:
            cliente = self.cliente_return(0,dados_cliente,dados_endereco)
            return render(request, self.template_name, {'cliente':cliente, 'erro': f"Erro inesperado: {e}"})
        return redirect(reverse_lazy("lista_clientes"))
class listar_cliente(ListView):
    model = Cliente


class editar_cliente(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente\cliente_form.html'
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
    def cliente_return(self,id,cliente,endereco):
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
        return cliente
    def get(self, request, *args, **kwargs):
        id = kwargs.get('cliente_id', None)
        try:
            cliente = Cliente.objects.get(id=id)
            endereco = cliente.endereco
            cliente = self.cliente_return(id,cliente,endereco)
        except Cliente.DoesNotExist:
            return HttpResponseNotFound('Cliente não encontrado.')
        except OperationalError:
            
            return HttpResponse("Erro operacional: Problema com o banco de dados.", status=500)
        except Exception as e:
            return HttpResponse(f"Erro inesperado: {e}", status=500) 
        return render(request, self.template_name, {'cliente': cliente})
    def post(self, request, *args, **kwargs):
        try:        
            id = kwargs.get('cliente_id', None)
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
            # Renderiza o template com uma mensagem de erro
            cliente = self.cliente_return(id,cliente,endereco)
            return render(request, self.template_name, {'cliente':cliente, 'erro': f"Dados inválidos ou CPF já cadastrado."})
        except OperationalError:
            cliente = self.cliente_return(id,cliente,endereco)
            return render(request, self.template_name, {'cliente': cliente, 'erro': "Problema com o banco de dados."})
        except Exception as e:
            cliente = self.cliente_return(id,cliente,endereco)
            return render(request, self.template_name, {'cliente': cliente, 'erro': f"Erro inesperado: {e}"})

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
def gerar_relatorio_cliente(request):
    clientes = Cliente.objects.all()
    
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("Arial", size=10, style='B')

    # Definindo a cor de fundo do cabeçalho da tabela
    pdf.set_fill_color(95, 158, 160)
    pdf.set_text_color(255, 255, 255)  # Cor do texto (branco)
    pdf.set_draw_color(95, 158, 160)  # Cor das linhas (preto)
    
     # Definindo a largura da célula (em mm) e a altura da célula
    largura_cabecalho = 280  # Largura da célula em milímetros
    altura_cabecalho = 10     # Altura da célula em milímetros
    
    pdf.multi_cell(largura_cabecalho, altura_cabecalho, "Relatório de clientes", 0, 'C', 1)
    pdf.ln(10)
    # Definindo a largura das colunas
    largura_coluna_nome = 60
    largura_coluna_cpf = 30
    largura_coluna_telefone = 30
    largura_coluna_endereço = 160
    altura_linha = 10

    # Cabeçalhos da tabela
    pdf.cell(largura_coluna_nome, altura_linha, 'Nome', 1, 0, 'C', 1)
    pdf.cell(largura_coluna_cpf, altura_linha, 'cpf', 1, 0, 'C', 1)
    pdf.cell(largura_coluna_telefone, altura_linha, 'telefone', 1, 0, 'C', 1)
    pdf.cell(largura_coluna_endereço, altura_linha, 'endereço', 1, 1, 'C', 1)

    pdf.set_text_color(0, 0, 0)  # Resetar cor do texto para preto
    pdf.set_font("Arial", size=10, style='')
    # Linhas da tabela
    for cliente in clientes:
        pdf.cell(largura_coluna_nome, altura_linha, cliente.nome, 1)
        pdf.cell(largura_coluna_cpf, altura_linha, formatar_cpf(cliente.cpf), 1, 0, 'C')
        pdf.cell(largura_coluna_telefone, altura_linha, formatar_telefone(cliente.telefone), 1, 0, 'C')
        pdf.cell(largura_coluna_endereço, altura_linha, str(cliente.endereco), 1, 1, 'C')

    pdf.ln(10)
    totalDeclientes = clientes.count()                
    pdf.cell(largura_cabecalho, altura_linha, f"Total de clientes: {totalDeclientes}",0, 1,'R')
    pdf.set_text_color(0, 0, 0)   
    # Criando a resposta HTTP com o PDF gerado
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_clientes.pdf"'
    
    # Salvando o PDF na resposta HTTP
    pdf.output(dest='S').encode('latin1')
    response.write(pdf.output(dest='S').encode('latin1'))
    
    return response