from pydoc import doc
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from django.http import HttpResponse
from datetime import date
from reportlab.platypus import Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import A4


import matplotlib.pyplot as plt


from associacoes.models import Associacao
from associacoes.utils import gerar_informacoes_associacoes



def gerar_tabela_associacoes_por_beneficiarios(informacoes_associacoes):
    """
    Esta função cria uma tabela com as associações que possuem mais beneficiários.
    """
    municipios_ordenados = sorted(informacoes_associacoes, key=lambda x: x['numero_beneficiarios'], reverse=True)
    top_assoc_beneficiarios = municipios_ordenados[:5]
    data_associacoes = [["#", "Associação", "Município", "Beneficiários"]]
    for idx, assoc in enumerate(top_assoc_beneficiarios, start=1):
        data_associacoes.append([str(idx), assoc['nome'], assoc['municipio'], str(assoc['numero_beneficiarios'])])
    
    tabela = Table(data_associacoes, [30, 460, 160, 90], len(data_associacoes)*[20], 
                   style=[('ALIGN', (1,1), (-2,-2), 'LEFT'),
                          ('ALIGN', (3,1), (3,-1), 'CENTER'),
                          ('FONT', (0,0), (-1,0), 'Helvetica-Bold'),
                          ('FONTSIZE', (0,0), (-1,-1), 10),
                          ('GRID', (0,0), (-1,-1), 1, colors.black)])
    
    return tabela



def gerar_tabela_comunidades_por_associacao(informacoes_associacoes):
    """
    Esta função cria uma tabela com as associações que beneficiam mais comunidades.
    """
    associacoes_ordenadas = sorted(informacoes_associacoes, key=lambda x: len(x['comunidades_beneficiadas'].split(',')), reverse=True)
    top_assoc_comunidades = associacoes_ordenadas[:5]
    data_associacoes = [["#", "Associação", "Nº de Com. Beneficiadas"]]
    for idx, assoc in enumerate(top_assoc_comunidades, start=1):
        data_associacoes.append([str(idx), assoc['nome'], str(len(assoc['comunidades_beneficiadas'].split(',')))])

    tabela = Table(data_associacoes, [30, 500, 160], len(data_associacoes)*[20], 
                   style=[('ALIGN', (1,1), (-2,-2), 'LEFT'),
                          ('ALIGN', (2,1), (2,-1), 'CENTER'),  # Ajuste a regra de alinhamento para a terceira coluna
                          ('FONT', (0,0), (-1,0), 'Helvetica-Bold'),
                          ('FONTSIZE', (0,0), (-1,-1), 10),
                          ('GRID', (0,0), (-1,-1), 1, colors.black)])
    
    return tabela

def gerar_tabela_associacoes_por_municipio(informacoes_associacoes):
    """
    Esta função cria uma tabela com os municípios que possuem mais associações.
    """
    associacoes_por_municipio = {}
    for assoc in informacoes_associacoes:
        municipio = assoc['municipio']
        if municipio not in associacoes_por_municipio:
            associacoes_por_municipio[municipio] = 0
        associacoes_por_municipio[municipio] += 1

    municipios_ordenados = sorted(associacoes_por_municipio.items(), key=lambda x: x[1], reverse=True)[:4]  # Limita a 4 municípios
    data_municipios = [["#", "Município", "Associações"]]
    for idx, (municipio, num_assoc) in enumerate(municipios_ordenados, start=1):
        data_municipios.append([str(idx), municipio, str(num_assoc)])
    
    tabela = Table(data_municipios, [30, 180, 90], len(data_municipios)*[20], 
                   style=[('ALIGN', (1,1), (-2,-2), 'LEFT'),
                          ('FONT', (0,0), (-1,0), 'Helvetica-Bold'),
                          ('GRID', (0,0), (-1,-1), 1, colors.black)])
    
    return tabela

def gerar_tabela_associacoes(informacoes_associacoes):
    """
    Esta função gera uma tabela com as informações das associações.
    """
    # Ordena as associações pelo número de beneficiários em ordem decrescente
    informacoes_associacoes.sort(key=lambda x: int(x['numero_beneficiarios']), reverse=True)
    
    # Cria a tabela
    data_associacoes = [["#", "Sigla", "Nome", "Município", "Nº Beneficiários"]]
    
    for idx, assoc in enumerate(informacoes_associacoes, start=1):
        data_associacoes.append([str(idx), assoc['sigla'], assoc['nome'], assoc['municipio'], str(assoc['numero_beneficiarios'])])

    tabela = Table(data_associacoes, [25, 50, 400, 130], len(data_associacoes)*[20], 
                   style=[('ALIGN', (1,1), (-2,-2), 'LEFT'),
                          ('ALIGN', (-1,0), (-1,-1), 'CENTER'),  # Alinhamento centralizado para a última coluna
                          ('FONT', (0,0), (-1,0), 'Helvetica-Bold'),
                          ('FONTSIZE', (0,0), (-1,-1), 8),
                          ('GRID', (0,0), (-1,-1), 1, colors.black)])

    return tabela

def gerar_tabela_siglas_associacoes(informacoes_associacoes):
    """
    Esta função cria uma tabela com as siglas, os nomes das associações e o número de beneficiários.
    As associações são ordenadas pelo número de beneficiários em ordem decrescente.
    """
    # Ordena as associações pelo número de beneficiários em ordem decrescente
    associacoes_ordenadas = sorted(informacoes_associacoes, key=lambda x: x['numero_beneficiarios'], reverse=True)

    # Cria a tabela
    data_associacoes = [["#", "Sigla", "Nome da Associação", "Nº Beneficiários"]]
    for idx, assoc in enumerate(associacoes_ordenadas, start=1):
        data_associacoes.append([str(idx), assoc['sigla'], assoc['nome'], str(assoc['numero_beneficiarios'])])

    tabela = Table(data_associacoes, [30, 90, 400, 90], len(data_associacoes)*[20], 
                   style=[('ALIGN', (1,1), (-2,-2), 'LEFT'),
                          ('ALIGN', (3,0), (3,-1), 'CENTER'),  # Alinhamento centralizado para a quarta coluna (Nº Beneficiários)
                          ('FONT', (0,0), (-1,0), 'Helvetica-Bold'),
                          ('FONTSIZE', (0,0), (-1,-1), 8),
                          ('GRID', (0,0), (-1,-1), 1, colors.black)])

    return tabela

def gerar_grafico_associacoes_por_municipio(informacoes_associacoes):
    associacoes_por_municipio = {}
    for assoc in informacoes_associacoes:
        municipio = assoc['municipio']
        if municipio not in associacoes_por_municipio:
            associacoes_por_municipio[municipio] = 0
        associacoes_por_municipio[municipio] += 1

    # Ordenar municípios pela quantidade de associações
    municipios_ordenados = sorted(associacoes_por_municipio.items(), key=lambda x: x[1], reverse=True)

    # Criar gráfico
    plt.figure(figsize=(20, 11))  # Aumenta a largura do gráfico
    plt.bar([municipio[0] for municipio in municipios_ordenados], [municipio[1] for municipio in municipios_ordenados])
    plt.xlabel("Município", fontsize=20)
    plt.ylabel("Número de Associações", fontsize=20)
    plt.xticks(rotation=45, fontsize=20, ha='right')  # Rotaciona os rótulos do eixo x em 45 graus, aumenta o tamanho da fonte e alinha à direita
    plt.yticks(fontsize=20)
    plt.tight_layout()  # Ajusta o layout

    # Salvar gráfico como imagem
    img_file = "associacoes/relatorios/img.png"  # substitua por um caminho válido em seu sistema
    plt.savefig(img_file)

    return img_file

def gerar_grafico_beneficiarios_por_associacao(informacoes_associacoes):
    beneficiarios_por_associacao = {}
    for assoc in informacoes_associacoes:
        sigla = assoc['sigla']
        if sigla not in beneficiarios_por_associacao:
            beneficiarios_por_associacao[sigla] = 0
        beneficiarios_por_associacao[sigla] += assoc['numero_beneficiarios']

    # Ordenar associações pelo número de beneficiários
    associacoes_ordenadas = sorted(beneficiarios_por_associacao.items(), key=lambda x: x[1], reverse=True)

    # Criar gráfico
    plt.figure(figsize=(20, 11))  # Aumenta a largura do gráfico
    plt.bar([associacao[0] for associacao in associacoes_ordenadas], [associacao[1] for associacao in associacoes_ordenadas])
    plt.xlabel("Associações", fontsize=20)
    plt.ylabel("Número de Beneficiários", fontsize=20)
    plt.xticks(rotation=45, fontsize=20, ha='right')  # Rotaciona os rótulos do eixo x em 45 graus, aumenta o tamanho da fonte e alinha à direita
    plt.yticks(fontsize=20)
    plt.tight_layout()  # Ajusta o layout

    # Salvar gráfico como imagem
    img_file = "associacoes/relatorios/img_benef.png"  # substitua por um caminho válido em seu sistema
    plt.savefig(img_file)

    return img_file

def gerar_assistente_gestor(informacoes_associacoes):
    """
    Esta função gera as informações a serem exibidas no relatório.
    """
    insights_texto = []

    num_assoc = len(informacoes_associacoes)
    total_beneficiarios = sum(assoc['numero_beneficiarios'] for assoc in informacoes_associacoes)
    insights_texto.append(["Atualmente, temos um total de {} associações cadastradas e um total de {} beneficiários atendidos pelas associações.".format(num_assoc, total_beneficiarios)])

    insights_texto.append(["As associações com o maior número de beneficiários são:"])
    insights_texto.append([gerar_tabela_associacoes_por_beneficiarios(informacoes_associacoes)])

    insights_texto.append(["As associações que beneficiam o maior número de comunidades são:"])
    insights_texto.append([gerar_tabela_comunidades_por_associacao(informacoes_associacoes)])

    insights_texto.append(["Os municípios com mais associações cadastradas são:"])
    insights_texto.append([gerar_tabela_associacoes_por_municipio(informacoes_associacoes)])

    # Adiciona o título do gráfico
    titulo_grafico = "Quantidade de Associações Beneficiadas por Município"
    insights_texto.append([titulo_grafico])

    # Adiciona o gráfico
    img_file = gerar_grafico_associacoes_por_municipio(informacoes_associacoes)
    insights_texto.append(Image(img_file, width=500, height=260))

    # Adiciona o título do gráfico
    titulo_grafico = "Número de Beneficiários por Associação"
    insights_texto.append([titulo_grafico])

    # Adiciona o gráfico
    img_file = gerar_grafico_beneficiarios_por_associacao(informacoes_associacoes)
    insights_texto.append(Image(img_file, width=500, height=250))

    return insights_texto

def footer(canvas, doc):
    """
    Esta função adiciona um rodapé em cada página do relatório.
    """
    data_atual = date.today().strftime("%d-%m-%Y")
    footer_text = "Gerado em: {} por Iury Coelho. Página: {}".format(data_atual, doc.page)
    canvas.saveState()
    canvas.setFont('Helvetica', 9)
    canvas.drawString(doc.leftMargin, doc.bottomMargin - 30, footer_text)
    canvas.restoreState()

def gerar_boas_praticas():
    """
    Esta função cria um parágrafo contendo as boas práticas a serem seguidas pelo gestor.
    """
    texto_boas_praticas = """
    <b>Boas Práticas - Gerência de Sousa</b>
    <br/><br/>
    <b>Panorama Completo:</b> Oferece uma visão geral do número de associações e beneficiários, permitindo um entendimento do alcance das associações.
    <br/><br/>
    <b>Reconhecimento de Desempenho Superior:</b> Identifica associações de alto desempenho, possibilitando reconhecimento e replicação de suas práticas.
    <br/><br/>
    <b>Insights Geográficos:</b> Revela a distribuição das associações por município, auxiliando no direcionamento estratégico de recursos e esforços.
    <br/><br/>
    <b>Decisões Baseadas em Dados:</b> A análise fornecida possibilita tomadas de decisão informadas, contribuindo para uma gestão mais eficaz.
    <br/><br/>
    <b>Economia de Tempo:</b> Automatiza a coleta e análise de dados, liberando tempo para outras tarefas importantes.
    <br/><br/>
    <b>Facilitador de Comunicação:</b> Serve como ferramenta de comunicação clara e eficaz com superiores e outras partes interessadas.
    <br/><br/>
    <b>Monitoramento Contínuo:</b> Permite acompanhar o progresso ao longo do tempo, identificando tendências e mudanças.
    <br/><br/>
    <b>Priorização de Recursos:</b> O gráfico ajuda a identificar as associações com mais beneficiários, auxiliando na decisão de onde alocar mais recursos.
    <br/><br/>
    <b>Identificação de Necessidades:</b> Associações com menos beneficiários no gráfico podem precisar de mais apoio ou intervenção.
    """
    # Define a largura da tabela
    tabela_width = 700  # Defina este valor de acordo com a largura desejada para a tabela

    # Criamos uma tabela com apenas uma célula, contendo o texto das boas práticas
    tabela_boas_praticas = Table([[Paragraph(texto_boas_praticas, getSampleStyleSheet()['BodyText'])]], 
                                 [tabela_width], [245],  # Largura e altura da tabela
                                 style=[('ALIGN', (0,0), (0,0), 'LEFT'),
                                        ('VALIGN', (0,0), (0,0), 'TOP'),
                                        ('BOX', (0,0), (0,0), 1, colors.black),  # Desenha uma borda ao redor da tabela
                                        ('FONT', (0,0), (0,0), 'Helvetica'),
                                        ('FONTSIZE', (0,0), (0,0), 10)])
    return tabela_boas_praticas


def gerar_pdf_associacoes(informacoes_associacoes):
    """
    Esta função gera um PDF com a tabela das informações das associações.
    """
    # Prepara a resposta
    response = HttpResponse(content_type='application/pdf')
    data_atual = date.today().strftime("%d-%m-%Y")
    response['Content-Disposition'] = 'attachment; filename="Associacoes - GER SOUSA - {}.pdf"'.format(data_atual)

    # Prepara o documento
    doc = BaseDocTemplate(response, pagesize=landscape(letter))
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
    template = PageTemplate(id='test', frames=frame, onPage=footer)
    doc.addPageTemplates([template])

    # Adiciona o logo e o título
    logo = Image('static/img/logo.png', width=150, height=50)
    elements = [logo, Spacer(1, 20)]
    titulo = Paragraph("Relatório de Associações", getSampleStyleSheet()['Title'])
    elements.append(titulo)

    # Cria um novo estilo de parágrafo com alinhamento central e adiciona o subtítulo
    centered_style = ParagraphStyle(name='Centered', parent=getSampleStyleSheet()['Heading2'], alignment=1)
    subtitulo = Paragraph("Gerência Regional de Sousa", centered_style)
    elements.append(subtitulo)
    elements.append(Spacer(1, 10))

    # Gera a tabela de associações e a adiciona ao relatório
    tabela_associacoes = gerar_tabela_associacoes(informacoes_associacoes)
    elements.append(tabela_associacoes)

    # Constrói o documento
    doc.build(elements)

    return response



def gerar_relatorio_pdf(assistente_texto):
    """
    Esta função gera o relatório em PDF com as informações fornecidas.
    """

    informacoes_associacoes = gerar_informacoes_associacoes()
    response = HttpResponse(content_type='application/pdf')
    data_atual = date.today().strftime("%d-%m-%Y")
    response['Content-Disposition'] = 'attachment; filename="Relatório de Insights das Associações - GER SOUSA - {}.pdf"'.format(data_atual)

    doc = BaseDocTemplate(response, pagesize=landscape(letter))
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
    template = PageTemplate(id='test', frames=frame, onPage=footer)
    doc.addPageTemplates([template])

    # Adiciona o logo
    logo = Image('static/img/logo.png', width=150, height=50)  
    elements = [logo, Spacer(1, 20)]

    titulo = Paragraph("Relatório de Insights das Associações", getSampleStyleSheet()['Title'])
    elements.append(titulo)

    # Cria um novo estilo de parágrafo com alinhamento central
    centered_style = ParagraphStyle(name='Centered', parent=getSampleStyleSheet()['Heading2'], alignment=1)
    subtitulo = Paragraph("Gerência Regional de Sousa", centered_style)
    elements.append(subtitulo)
    elements.append(Spacer(1, 10))

    for item in assistente_texto:
        if isinstance(item, Image):  # Se o item é uma imagem
            elements.append(item)
            elements.append(Spacer(1, 12))
        elif isinstance(item[0], str):
            elements.append(Paragraph(item[0], getSampleStyleSheet()['BodyText']))
            if "são:" not in item[0]:  
                elements.append(Spacer(1, 12))
        else:
            elements.append(item[0])
            elements.append(Spacer(1, 12))


    # Gera a tabela de siglas e nomes das associações e a adiciona ao relatório
    tabela_siglas_nomes = gerar_tabela_siglas_associacoes(informacoes_associacoes)
    elements.append(tabela_siglas_nomes)


    # Adiciona a seção de "Boas Práticas" no final do relatório
    tabela_boas_praticas = gerar_boas_praticas()
    elements.append(Spacer(1, 20))  # Adiciona um espaço antes da tabela
    elements.append(tabela_boas_praticas)

    doc.build(elements)

    return response


    """
    Esta função gera um PDF com a tabela das informações das associações.
    """
    response = HttpResponse(content_type='application/pdf')
    data_atual = date.today().strftime("%d-%m-%Y")
    response['Content-Disposition'] = 'attachment; filename="Associacoes - GER SOUSA - {}.pdf"'.format(data_atual)

    doc = BaseDocTemplate(response, pagesize=landscape(letter))
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
    template = PageTemplate(id='test', frames=frame, onPage=footer)
    doc.addPageTemplates([template])

    # Adiciona o logo
    logo = Image('static/img/logo.png', width=150, height=50)  
    elements = [logo, Spacer(1, 20)]

    titulo = Paragraph("Relatório de Associações", getSampleStyleSheet()['Title'])
    elements.append(titulo)

    # Cria um novo estilo de parágrafo com alinhamento central
    centered_style = ParagraphStyle(name='Centered', parent=getSampleStyleSheet()['Heading2'], alignment=1)
    subtitulo = Paragraph("Gerência Regional de Sousa", centered_style)
    elements.append(subtitulo)
    elements.append(Spacer(1, 10))

    # Gera a tabela de associações e a adiciona ao relatório
    tabela_associacoes = gerar_tabela_associacoes(informacoes_associacoes)
    elements.append(tabela_associacoes)

    doc.build(elements)

    return response