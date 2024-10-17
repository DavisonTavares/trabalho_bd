from django.http import HttpResponse, JsonResponse,HttpResponseNotFound
from django.shortcuts import render,redirect
from .models import Cliente,ViewClientes
from endereco.models import Endereco
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from .forms import ClienteForm
from django.db import IntegrityError, OperationalError
from fpdf import FPDF
import requests
import unicodedata
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection

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

class cadastrar_cliente(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    template_name = 'cliente\cliente_form.html'
    def cliente_return(self,id, cliente, endereco):# função para criar o objeto que será retornado caso ocorra um erro no cadastramento 
        cpf = formatar_cpf(cliente["cpf"]) # formata o cpf no padrão 111.111.111-11
        cep = formatar_cep(endereco["cep"]) # formata o cep no padrão 111111-11
        telefone = formatar_telefone(cliente["telefone"]) # formata o telefone no padrão (11) 11111-1111
        cliente = {
            'id': id,
            'nome': cliente["nome"], 
            'time': cliente["time"], 
            'audiovisual': cliente["audiovisual"], 
            'naturalidade_cidade': cliente["naturalidade_cidade"], 
            'naturalidade_estado': cliente["naturalidade_estado"], 
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
        # Obter estados brasileiros da API do IBGE
        url_estados = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
        response = requests.get(url_estados)
        
        if response.status_code == 200:
            estados = response.json()
            estados = sorted(estados, key=lambda estado: estado['nome'])
        else:
            estados = []

        times_serie_a = [
        "Botafogo", "Flamengo", "Palmeiras", "São Paulo", "Grêmio", "Internacional",
        "Fluminense", "Athletico-PR", "Atlético-MG", "Cruzeiro", "Santos", "Corinthians",
        "Fortaleza", "Bahia", "Vasco", "Cuiabá", "Goiás", "Coritiba", "América-MG"
        ]
        audiovisuais = ["One Piece","Code Geass","The Wire","CSI ",'Nenhum']
        context = {
        'estados': estados,
        'times': times_serie_a,
        'cliente': False,
        'audiovisuais':audiovisuais
        }
        return render(request,self.template_name,context )
    def post(self, request, *args, **kwargs):   
        campos_cliente = ['nome','time','audiovisual','naturalidade_cidade','naturalidade_estado', 'cpf', 'telefone','endereco','nome_formatado','naturalidade_cidade_formatado','naturalidade_estado_formatado']
        
        campos_endereco =['rua', 'numero', 'complemento', 'bairro', 'cidade', 'estado', 'cep']
        # Listas para armazenar os dados recebidos
        dados_cliente = {}
        dados_endereco = {}
        # Coleta os dados usando request.POST.get para cada campo
        for campo in campos_cliente:
            valor = request.POST.get(campo)
            if campo == 'nome':
                 # remove acentos e garante que as letras sejam minusculas
                nome_formatado = unicodedata.normalize('NFKD', valor).encode('ASCII', 'ignore').decode('ASCII').lower()
            if campo == 'endereco':
                continue  # Pula o campo 'endereco'
            if campo == 'cpf':
                valor = limpar_cpf(valor)
            if campo == 'telefone':
                valor = limpar_telefone(valor)
            if campo == 'naturalidade_cidade':
                naturalidade_cidade_formatado = unicodedata.normalize('NFKD', valor).encode('ASCII', 'ignore').decode('ASCII').lower()
            if campo == 'naturalidade_estado':
                naturalidade_estado_formatado = unicodedata.normalize('NFKD', valor).encode('ASCII', 'ignore').decode('ASCII').lower()
            dados_cliente[campo] = valor
        for campo in campos_endereco:
            valor = request.POST.get(campo)
            if campo == 'cep':
                valor = limpar_cep(valor)
            dados_endereco[campo] = valor
        try:
            endereco = Endereco.objects.create(**dados_endereco)
            dados_cliente['endereco'] = endereco
            dados_cliente['nome_formatado']= nome_formatado
            dados_cliente['naturalidade_cidade_formatado']= naturalidade_cidade_formatado
            dados_cliente['naturalidade_estado_formatado']= naturalidade_estado_formatado
            Cliente.objects.create(**dados_cliente)
        except IntegrityError:
            cliente = self.cliente_return(0,dados_cliente,dados_endereco)
            return render(request, self.template_name, {'cliente':cliente, 'erro': f"Dados inválidos ou CPF já cadastrado.",'pagina':'cadastrar'})
        except OperationalError:
            cliente = self.cliente_return(0,dados_cliente,dados_endereco)
            return render(request, self.template_name, {'cliente':cliente, 'erro': f"Problema com o banco de dados.",'pagina':'cadastrar'})
        except Exception as e:
            cliente = self.cliente_return(0,dados_cliente,dados_endereco)
            return render(request, self.template_name, {'cliente':cliente, 'erro': f"Erro inesperado: {e}",'pagina':'cadastrar'})
        return redirect(reverse_lazy("lista_clientes"))
class listar_cliente(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Cliente
    template_name = 'cliente\cliente_list.html'
    def get(self, request, *args, **kwargs): 
        clientes = ViewClientes.objects.all()
        return render(request, self.template_name, {'cliente_list': clientes})
    def post(self, request, *args, **kwargs):  
        nome = request.POST.get('search')
        nome = unicodedata.normalize('NFKD', nome).encode('ASCII', 'ignore').decode('ASCII').lower()
        clientes = Cliente.objects.filter(nome_formatado__contains=nome)  # filtra os clientes pelo nome formatado caso ele contenha parte do nome
        return render(request, self.template_name, {'cliente_list': clientes})
class editar_cliente(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Cliente
    form_class = ClienteForm
    template_name = 'cliente\cliente_form.html'
    def atualizar_cliente_endereco(self,cliente_id, campos_cliente, endereco_id, campos_endereco):
        with connection.cursor() as cursor:
            cursor.execute("""
            CALL update_cliente_endereco(
                %s::UUID, %s::VARCHAR, %s::VARCHAR, %s::VARCHAR, 
                %s::INT, %s::VARCHAR, %s::VARCHAR, %s::VARCHAR, 
                %s::VARCHAR, %s::VARCHAR, %s::VARCHAR
            );
        """, [
            cliente_id,
            campos_cliente.get('nome'),
            campos_cliente.get('cpf'),
            campos_cliente.get('telefone'),
            endereco_id,
            campos_endereco.get('rua'),
            campos_endereco.get('numero'),
            campos_endereco.get('bairro'),
            campos_endereco.get('cidade'),
            campos_endereco.get('estado'),
            campos_endereco.get('cep')
        ])
    def cliente_return(self,id,cliente,endereco):
        cpf = formatar_cpf(cliente.cpf)
        cep = formatar_cep(endereco.cep)
        telefone = formatar_telefone(cliente.telefone)
        cliente = {
            'id': id,
            'nome': cliente.nome,
            'time': cliente.time, 
            'audiovisual': cliente.audiovisual, 
            'naturalidade_cidade': cliente.naturalidade_cidade, 
            'naturalidade_estado': cliente.naturalidade_estado,   
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
        url_estados = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
        response = requests.get(url_estados)
        
        if response.status_code == 200:
            estados = response.json()
            estados = sorted(estados, key=lambda estado: estado['nome'])
        else:
            estados = []

        times_serie_a = [
        "Botafogo", "Flamengo", "Palmeiras", "São Paulo", "Grêmio", "Internacional",
        "Fluminense", "Athletico-PR", "Atlético-MG", "Cruzeiro", "Santos", "Corinthians",
        "Fortaleza", "Bahia", "Vasco", "Cuiabá", "Goiás", "Coritiba", "América-MG"
        ]
        audiovisuais = ["One Piece","Code Geass","The Wire","CSI ",'Nenhum']
        context = {
        'estados': estados,
        'times': times_serie_a,
        'cliente': cliente,
        'audiovisuais':audiovisuais,
        'pagina':'editar'
        }
        return render(request, self.template_name, context)
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
            campos_cliente = {
            'nome': nome,
            'cpf': cpf,
            'telefone': telefone,
            
            }
            campos_endereco = {'rua': rua,
            'numero': numero,
            'complemento': complemento,
            'bairro': bairro,
            'cidade': cidade,
            'estado': estado,
            'cep': cep}
            cliente = Cliente.objects.get(id=id)
            endereco = cliente.endereco
            self.atualizar_cliente_endereco(id,campos_cliente,endereco.id,campos_endereco) # utiliza a procedure update_cliente_endereco
        except IntegrityError:
            # Renderiza o template com uma mensagem de erro
            cliente = self.cliente_return(id,cliente,endereco)
            return render(request, self.template_name, {'cliente':cliente, 'erro': f"Dados inválidos ou CPF já cadastrado.",'pagina':'editar'})
        except OperationalError:
            cliente = self.cliente_return(id,cliente,endereco)
            return render(request, self.template_name, {'cliente': cliente, 'erro': "Problema com o banco de dados.",'pagina':'editar'})
        except Exception as e:
            cliente = self.cliente_return(id,cliente,endereco)
            return render(request, self.template_name, {'cliente': cliente, 'erro': f"Erro inesperado: {e}",'pagina':'editar'})

        return redirect(reverse_lazy("lista_clientes"))
    
class deletar_cliente(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    def get(self, request, *args, **kwargs):
        try:
            id = kwargs.get('cliente_id', None)
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
        id = kwargs.get('cliente_id', None)
        if id is None:
            return HttpResponseNotFound('Cliente não encontrado.')
        try:
            cliente = Cliente.objects.get(id=id)
            endereco = Endereco.objects.get(id=cliente.endereco.id)
            cliente.delete()  # Deleta o cliente
            endereco.delete()  # Deleta o endereço
            return JsonResponse({'message': 'Cliente excluído com sucesso.'}, status=200)
        except Cliente.DoesNotExist:
            return HttpResponseNotFound('Cliente não encontrado.')
        except Exception as e:
            return JsonResponse({'message': 'Erro ao excluir cliente.', 'error': str(e)}, status=500)

@login_required
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