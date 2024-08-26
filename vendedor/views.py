from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from .models import Vendedor
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import VendedorForm
from django.db import IntegrityError, OperationalError
from fpdf import FPDF


class cadastrar_vendedor(CreateView):
    model = Vendedor
    form_class = VendedorForm
    template_name = 'vendedor/vendedor_form.html'
    success_url = reverse_lazy('listar_vendedor')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'vendedor': False})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect(self.success_url)
            except IntegrityError:
                return render(request, self.template_name, {'form': form, 'erro': "Erro de integridade: Dados inválidos."})
            except OperationalError:
                return render(request, self.template_name, {'form': form, 'erro': "Erro operacional: Problema com o banco de dados."})
            except Exception as e:
                return render(request, self.template_name, {'form': form, 'erro': f"Erro inesperado: {e}"})
        else:
            return render(request, self.template_name, {'form': form})

class listar_vendedor(ListView):
    model = Vendedor
    template_name = 'vendedor/vendedor_list.html'

class editar_vendedor(UpdateView):
    model = Vendedor
    form_class = VendedorForm
    template_name = 'vendedor/vendedor_form.html'
    success_url = reverse_lazy('listar_vendedor')

    def campos_alterados(self, vendedor, dados):
        campos_vendedor = {}
        if dados['nome'] != vendedor.nome:
            campos_vendedor['nome'] = dados['nome']
        return campos_vendedor

    def vendedor_return(self, id, vendedor):
        return {
            'id': id,
            'nome': vendedor.nome,
        }

    def get(self, request, *args, **kwargs):
        id = kwargs.get('pk', None)
        try:
            vendedor = Vendedor.objects.get(id=id)
            vendedor = self.vendedor_return(id, vendedor)
        except Vendedor.DoesNotExist:
            return HttpResponseNotFound('Vendedor não encontrado.')
        except OperationalError:
            return HttpResponse("Erro operacional: Problema com o banco de dados.", status=500)
        except Exception as e:
            return HttpResponse(f"Erro inesperado: {e}", status=500)
        return render(request, self.template_name, {'vendedor': vendedor})

    def post(self, request, *args, **kwargs):
        id = kwargs.get('pk', None)
        nome = request.POST.get('nome')
        dados = {'nome': nome}

        try:
            vendedor = Vendedor.objects.get(id=id)
            campos_vendedor = self.campos_alterados(vendedor, dados)
            Vendedor.objects.filter(id=id).update(**campos_vendedor)
        except IntegrityError:
            vendedor = self.vendedor_return(id, vendedor)
            return render(request, self.template_name, {'vendedor': vendedor, 'erro': "Dados inválidos."})
        except OperationalError:
            vendedor = self.vendedor_return(id, vendedor)
            return render(request, self.template_name, {'vendedor': vendedor, 'erro': "Problema com o banco de dados."})
        except Exception as e:
            vendedor = self.vendedor_return(id, vendedor)
            return render(request, self.template_name, {'vendedor': vendedor, 'erro': f"Erro inesperado: {e}"})

        return redirect(self.success_url)
    
class deletar_vendedor(DeleteView):
    model = Vendedor
    template_name = 'vendedor/confirmar_apagar_vendedor.html'
    success_url = reverse_lazy('listar_vendedor')

    def get(self, request, *args, **kwargs):
        try:
            id = kwargs.get('pk', None)
            vendedor = Vendedor.objects.get(id=id)
        except Vendedor.DoesNotExist:
            return HttpResponseNotFound('Vendedor não encontrado.')
        except OperationalError:
            return HttpResponse("Erro operacional: Problema com o banco de dados.", status=500)
        except Exception as e:
            return HttpResponse(f"Erro inesperado: {e}", status=500)
        return render(request, self.template_name, {"vendedor": vendedor})

    def delete(self, request, *args, **kwargs):
        id = kwargs.get('pk', None)
        if id is None:
            return HttpResponseNotFound('Vendedor não encontrado.')
        try:
            vendedor = Vendedor.objects.get(id=id)
            vendedor.delete()
            return JsonResponse({'message': 'Vendedor excluído com sucesso.'}, status=200)
        except Vendedor.DoesNotExist:
            return HttpResponseNotFound('Vendedor não encontrado.')
        except Exception as e:
            return JsonResponse({'message': 'Erro ao excluir vendedor.', 'error': str(e)}, status=500)

def gerar_relatorio_vendedor(request):
    vendedores = Vendedor.objects.all()
    
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("Arial", size=10, style='B')

    # Definindo a cor de fundo do cabeçalho da tabela
    pdf.set_fill_color(95, 158, 160)
    pdf.set_text_color(255, 255, 255)  # Cor do texto (branco)
    pdf.set_draw_color(95, 158, 160)  # Cor das linhas

    # Definindo a largura da célula (em mm) e a altura da célula
    largura_cabecalho = 280  # Largura da célula em milímetros
    altura_cabecalho = 10     # Altura da célula em milímetros

    pdf.multi_cell(largura_cabecalho, altura_cabecalho, "Relatório de vendedores", 0, 'C', 1)
    pdf.ln(10)

    # Definindo a largura das colunas
    largura_coluna_id = 30
    largura_coluna_nome = 150
    altura_linha = 10

    # Cabeçalhos da tabela
    pdf.cell(largura_coluna_id, altura_linha, 'ID', 1, 0, 'C', 1)
    pdf.cell(largura_coluna_nome, altura_linha, 'Nome', 1, 1, 'C', 1)

    pdf.set_text_color(0, 0, 0)  # Resetar cor do texto para preto
    pdf.set_font("Arial", size=10, style='')

    # Linhas da tabela
    for vendedor in vendedores:
        pdf.cell(largura_coluna_id, altura_linha, str(vendedor.id), 1, 0, 'C')
        pdf.cell(largura_coluna_nome, altura_linha, vendedor.nome, 1, 1, 'C')

    pdf.ln(10)
    total_de_vendedores = vendedores.count()                
    pdf.cell(largura_cabecalho, altura_linha, f"Total de vendedores: {total_de_vendedores}", 0, 1, 'R')
    pdf.set_text_color(0, 0, 0)   

    # Criando a resposta HTTP com o PDF gerado
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_vendedores.pdf"'

    # Salvando o PDF na resposta HTTP
    pdf_output = pdf.output(dest='S').encode('latin1')
    response.write(pdf_output)
    
    return response