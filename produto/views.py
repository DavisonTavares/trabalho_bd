from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from .models import Produto, Marca
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required


from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Produto
from .forms import ProdutoForm, FiltroPrecoForm
from django.db.models import Count, Q
from fpdf import FPDF
import unicodedata
from fpdf import FPDF

@login_required
def deletar_produto(request, produto_id):
    if request.method == 'POST':    
        Produto.objects.filter(id=produto_id).delete()
        return redirect(reverse_lazy('lista_produtos'))
    return HttpResponse(status=404)

@login_required
def editar_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            marca = Marca.objects.get_or_create(nome=form.cleaned_data['marca'])
     
            url_imagem = form.cleaned_data['url_imagem'] or 'https://i.pinimg.com/736x/a2/2e/55/a22e5584986d9c09b02a382805802469.jpg'
            nomeFormatado = unicodedata.normalize('NFKD', form.cleaned_data['nome']).encode('ASCII', 'ignore').decode('ASCII')
            nomeFormatado = nomeFormatado.lower()
            Produto.objects.filter(id=produto_id).update(
                nome=form.cleaned_data['nome'],
                nomeFormatado=nomeFormatado,
                quantidade=form.cleaned_data['quantidade'],
                valor=form.cleaned_data['valor'],
                marca=form.cleaned_data['marca'],
                litragem=form.cleaned_data['litragem'],
                url_imagem=url_imagem
            )
            return redirect(reverse_lazy('lista_produtos'))
    
    form = ProdutoForm(instance=produto)
    marcas = Marca.objects.all()
    produtos = Produto.objects.all()
    return render(request, 'produto/produto_list.html', {'produtos': produtos, 'produto_id': produto_id, 'marcas': marcas, 'form': form, 'titlebutton': 'Editar'})
    

@login_required    
def cadastrar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if not form.is_valid():
            return render(request, 'produto/produto_form.html', {'form': form})
        marca = Marca.objects.get_or_create(nome=form.cleaned_data['marca'])
        print(marca)        

        url_imagem = form.cleaned_data['url_imagem'] or 'https://i.pinimg.com/736x/a2/2e/55/a22e5584986d9c09b02a382805802469.jpg'        
        nomeFormatado = unicodedata.normalize('NFKD', form.cleaned_data['nome']).encode('ASCII', 'ignore').decode('ASCII')
        nomeFormatado = nomeFormatado.lower()
      # Criando o objeto Produto e salvando no banco de dados
        Produto.objects.create(
            nome=form.cleaned_data['nome'],
            nomeFormatado=nomeFormatado,
            quantidade=form.cleaned_data['quantidade'],
            valor=form.cleaned_data['valor'],
            marca=form.cleaned_data['marca'],
            litragem=form.cleaned_data['litragem'],
            url_imagem=url_imagem
        )
        
        # Redirecionando após o cadastro
        return redirect(reverse_lazy('lista_produtos'))
    
    # Se o método for GET, renderize o formulário
    marcas = Marca.objects.all()
    return render(request, 'produto/produto_form.html', {'form': ProdutoForm(), 'titlebutton': 'Cadastrar', 'marcas': marcas})

#@login_required
def listar_produto(request):
    if request.method == 'POST':
        print(request.POST)
        search_term = request.POST.get('search')
        priceMin = request.POST.get('priceMin') or 0
        priceMax = request.POST.get('priceMax')
       
        if search_term:
            # Retirar acentos e caracteres especiais da string
            search_term_normalized = unicodedata.normalize('NFKD', search_term)
            search_term_normalized = search_term_normalized.encode('ASCII', 'ignore').decode('ASCII')
            search_term_normalized = search_term_normalized.lower()
            # Filtrar produtos que contenham o termo de pesquisa, sem considerar acentos
           # Filtrando produtos com Q para combinar as condições
            produtos = Produto.objects.filter(
                Q(nomeFormatado__contains=search_term_normalized) | Q(marca__nome__contains=search_term_normalized)
            )
        else:
            produtos = Produto.objects.all()
            
        
        if priceMax and priceMin:
            produtos = produtos.filter(valor__gte=priceMin, valor__lte=priceMax)
    else:
        #verifica se o usuário está logado
        # Verifica se existe um usuário logado
        usuario_logado = request.user if request.user.is_authenticated else None
        produtos = Produto.objects.all()
    marcas = Marca.objects.all()
    return render(request, 'produto/produto_list.html', {'produtos': produtos, 'marcas': marcas, 'form': ProdutoForm(), 'titlebutton': 'Cadastrar', 'filtro': FiltroPrecoForm(), 'usuario_logado': usuario_logado})

@login_required
def cadastrar_marca(request):
    print(request.method)
    if request.method == 'POST':
        try:
            nome = request.POST.get('marca')
            nome = nome.upper()
            print(nome)
            Marca.objects.create(nome=nome)
            return redirect(reverse_lazy('cadastrar_produto'))
        except IntegrityError:
            return render(request, 'produto/produto_form.html', {'errors': 'Marca já cadastrada', 'form': ProdutoForm()})
        except:
            return render(request, 'produto/produto_form.html', {'errors': 'Erro ao cadastrar marca', 'form': ProdutoForm()})
    return HttpResponse(status=404)

@login_required
def gerar_relatorio(request):
    produtos = Produto.objects.all()
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12, style='B')

    # Definindo a cor de fundo do cabeçalho da tabela
    pdf.set_fill_color(95, 158, 160)
    pdf.set_text_color(255, 255, 255)  # Cor do texto (branco)
    pdf.set_draw_color(95, 158, 160)  # Cor das linhas (preto)
    
     # Definindo a largura da célula (em mm) e a altura da célula
    largura_cabecalho = 190  # Largura da célula em milímetros
    altura_cabecalho = 10     # Altura da célula em milímetros
    
    pdf.multi_cell(largura_cabecalho, altura_cabecalho, "Relatório de Produtos", 0, 'C', 1)
    pdf.ln(10)
    # Definindo a largura das colunas
    largura_coluna_nome = 60
    largura_coluna_marca = 40
    largura_coluna_litragem = 30
    largura_coluna_quantidade = 30
    largura_coluna_valor = 30
    altura_linha = 10

    # Cabeçalhos da tabela
    pdf.cell(largura_coluna_nome, altura_linha, 'Nome', 1, 0, 'C', 1)
    pdf.cell(largura_coluna_marca, altura_linha, 'Marca', 1, 0, 'C', 1)
    pdf.cell(largura_coluna_litragem, altura_linha, 'Litragem (L)', 1, 0, 'C', 1)
    pdf.cell(largura_coluna_quantidade, altura_linha, 'Quantidade', 1, 0, 'C', 1)
    pdf.cell(largura_coluna_valor, altura_linha, 'Valor (R$)', 1, 1, 'C', 1)

    pdf.set_text_color(0, 0, 0)  # Resetar cor do texto para preto
    pdf.set_font("Arial", size=12, style='')
    # Linhas da tabela
    for produto in produtos:
        pdf.cell(largura_coluna_nome, altura_linha, produto.nome, 1)
        pdf.cell(largura_coluna_marca, altura_linha, str(produto.marca), 1, 0, 'C')
        pdf.cell(largura_coluna_litragem, altura_linha, f"{produto.litragem:.2f}", 1, 0, 'C')
        pdf.cell(largura_coluna_quantidade, altura_linha, str(produto.quantidade), 1, 0, 'C')
        pdf.cell(largura_coluna_valor, altura_linha, f"R$ {produto.valor:.2f}", 1, 1, 'C')

    pdf.ln(10)
    totalDeProdutos = produtos.count()
    valorTOTAL = 0
    for produto in produtos:
        valorTOTAL += produto.valor * produto.quantidade                      

    totalDeProdutosPorMarca = Produto.objects.values('marca').annotate(total=Count('marca'))

    pdf.cell(largura_cabecalho, altura_linha, f"Total de produtos: {totalDeProdutos}",0, 1,'R')
    pdf.cell(largura_cabecalho, altura_linha, f"Valor total: R$ {valorTOTAL}", 0, 1, 'R')
    
    pdf.set_text_color(255, 255, 255)
    pdf.cell(largura_cabecalho, altura_linha, "Total de produtos por marca:", 1, 1, 'L', 1)

    pdf.set_text_color(0, 0, 0)
    marcas = Marca.objects.all()
    for marca in totalDeProdutosPorMarca:
        pdf.cell(largura_cabecalho, altura_linha, marcas.get(id=marca['marca']).nome + f": {marca['total']}", 1, 1, 'L')        


    # Criando a resposta HTTP com o PDF gerado
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_produtos.pdf"'
    
    # Salvando o PDF na resposta HTTP
    pdf.output(dest='S').encode('latin1')
    response.write(pdf.output(dest='S').encode('latin1'))
    
    return response