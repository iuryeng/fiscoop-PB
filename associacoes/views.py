from django.http import FileResponse
from django.shortcuts import render
from associacoes.models import Associacao

from associacoes.relatorios import gerar_assistente_gestor, gerar_pdf_associacoes, gerar_relatorio_pdf

from associacoes.utils import gerar_informacoes_associacoes

from .analises import analise_comunidade_por_associacao, analise_associacoes_por_municipio, analise_beneficiarios_por_associacao, get_total_associacoes, get_total_beneficiarios, get_total_municipios, get_total_comunidades

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_associacoes_graficos(request):
    associacoes_por_municipio_plot = analise_associacoes_por_municipio()
    comunidade_por_associacao_plot = analise_comunidade_por_associacao()
    beneficiarios_por_associacao_plot = analise_beneficiarios_por_associacao()
    return render(request, 'admin/associacoes/associacao_change_list.html', {
        'associacoes_por_municipio_plot': associacoes_por_municipio_plot,
        'comunidade_por_associacao_plot': comunidade_por_associacao_plot,
        'beneficiarios_por_associacao_plot': beneficiarios_por_associacao_plot
    })

def associacoes_graficos(request):
    associacoes_por_municipio_plot = analise_associacoes_por_municipio()
    comunidade_por_associacao_plot = analise_comunidade_por_associacao()
    beneficiarios_por_associacao_plot = analise_beneficiarios_por_associacao()
    return render(request, 'associacoes/associacoes_graficos.html', {'associacoes_por_municipio_plot': associacoes_por_municipio_plot,
                                                            'comunidade_por_associacao_plot': comunidade_por_associacao_plot,
                                                            'beneficiarios_por_associacao_plot': beneficiarios_por_associacao_plot})

def relatorio_associacoes_view(request):
    informacoes_associacoes = gerar_informacoes_associacoes()
    assistente_texto = gerar_assistente_gestor(informacoes_associacoes)
    return gerar_relatorio_pdf(assistente_texto)


def associacoes_geral(request):
    informacoes_associacoes = gerar_informacoes_associacoes()

    context = {
        'total_associacoes': get_total_associacoes(),
        'total_municipios': get_total_municipios(),
        'total_comunidades': get_total_comunidades(),
        'total_beneficiarios': get_total_beneficiarios(),
        'associacoes_table': {
            'title': 'Lista de Associações',
            'columns': ['Sigla', 'Nome', 'Comunidades Beneficiadas', 'Gerência Responsável', 'Município', 'Número de Beneficiários'],
            'data': informacoes_associacoes,
        },
    }

    return render(request, 'associacoes/associacoes_geral.html', context)


def download_associacoes(request):
    """
    Esta função de view gera um PDF com as informações das associações e o retorna como uma resposta de download.
    """
    informacoes_associacoes = gerar_informacoes_associacoes()
    # Gera o PDF
    response = gerar_pdf_associacoes(informacoes_associacoes)
    
    return response







