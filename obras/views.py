from django.shortcuts import get_object_or_404, render
from django.db.models import Sum
from obras.analises import analise_impacto_municipio, analise_investimentos_por_municipio, analise_obras_por_municipio, analise_status_obras
from obras.utils import calcular_preco_obra, calcular_total_investimentos, contar_fiscalizacoes_cisterna, contar_fiscalizacoes_passagem_molhada, gerar_informacoes_obras
from servicos.models import ItemCisterna, ItemPassagemMolhada
from servicos.utils import calculate_partial_total, obter_itens_servico
from .models import Cisterna, Obra, PassagemMolhada


def obras_graficos(request):
    informacoes_obras = gerar_informacoes_obras()
    obras_por_status_plot = analise_status_obras(informacoes_obras)
    obras_por_municipio_plot = analise_obras_por_municipio(informacoes_obras)
    impacto_municipio_plot = analise_impacto_municipio(informacoes_obras)
    investimentos_por_municipio_plot = analise_investimentos_por_municipio()

    return render(request, 'obras/obras_graficos.html', {
        'obras_por_status_plot': obras_por_status_plot,
        'obras_por_municipio_plot': obras_por_municipio_plot,
        'impacto_municipio_plot': impacto_municipio_plot,
        'investimentos_por_municipio_plot': investimentos_por_municipio_plot, # Adicionando o novo gráfico
    })

def obras_geral(request):
    dados_obras = gerar_informacoes_obras()
    total_investimentos = calcular_total_investimentos()

    informacoes_obras_table = []
    for obra_info in dados_obras['informacoes']:
        obra_obj = None
        if obra_info['tipo'] == 'Cisterna':
            obra_obj = Cisterna.objects.get(id=obra_info['id'])
        elif obra_info['tipo'] == 'Passagem Molhada':
            obra_obj = PassagemMolhada.objects.get(id=obra_info['id'])

        status_display = obra_obj.get_status_display() if obra_obj else obra_info['status']
        
        
        informacoes_obras_table.append({
            'id': obra_info['id'],
            'Tipo': obra_info['tipo'],
            'Nome': obra_info['nome'],
            'Edital': obra_info['edital'],
            'Empresa Encarregada': obra_info['empresa_encarregada'],
            'Lote': obra_info['lote'],
            'Regional': obra_info['regional'],
            'Município': obra_info['municipio'],
            'Status': status_display,
            'Ações': '<a href="{}" class="btn btn-primary">Detalhes</a>'.format(obra_info['detalhes_url']),
        })

    context = {
        'total_obras': dados_obras['total_cisternas'] + dados_obras['total_passagens_molhadas'],
        'obras_execucao': dados_obras['total_execucao'],
        'obras_concluidas': dados_obras['total_concluidas'],
        'obras_planejadas': dados_obras['total_planejadas'],
        'obras_paralisadas': dados_obras['total_paralisadas'],
        'total_municipios': dados_obras['total_municipios_impactados'],
        'total_investimentos': total_investimentos, 
        'obras_table': {
            'title': 'Lista de Obras',
            'columns': ['ID', 'Tipo', 'Nome', 'Edital', 'Empresa Encarregada', 'Lote', 'Regional', 'Município', 'Status', 'Ações'],
            'data': informacoes_obras_table,
        },
    }

    return render(request, 'obras/obras_geral.html', context)


def cisterna_detalhe(request, obra_id):
    obra = get_object_or_404(Cisterna, pk=obra_id)
    conclusao_value = obra.servicos.first().conclusao if obra.servicos.exists() else 0.0
    conclusao = "{:.2f}%".format(conclusao_value)
    total_investido = calcular_preco_obra(obra)
    servico = obra.servicos.first() if obra.servicos.exists() else None
    valor_parcial_total = calculate_partial_total(servico) if servico else "R$ 0,00"
    numero_fiscalizacoes = contar_fiscalizacoes_cisterna(obra)
    informacoes_servicos_table = obter_itens_servico(obra) # Certifique-se de ajustar essa função
    print(valor_parcial_total)

    columns = ['Status', 'Tipo', 'Descrição', 'Valor Investido','Valor Executado', 'Conclusão']
    servicos_table = {
        'title': 'Lista de Serviços',
        'columns': columns,
        'data': informacoes_servicos_table,
    }

    return render(request, 'obras/obra_detalhe.html', {'obra': obra, 'conclusao': conclusao, 'conclusao_value': conclusao_value, 'total_investido': total_investido, 'fiscalizacoes': numero_fiscalizacoes, 'servicos_table': servicos_table, 'valor_parcial_total': valor_parcial_total})


from obras.models import PassagemMolhada, ObraArquivoPassagemMolhada
from django.shortcuts import render, get_object_or_404

def passagem_molhada_detalhe(request, obra_id):
    obra = get_object_or_404(PassagemMolhada, pk=obra_id)
    
    # Pega os arquivos relacionados à obra
    arquivos = ObraArquivoPassagemMolhada.objects.filter(passagem_molhada=obra)
    
    # Organize os arquivos em um dicionário para acesso fácil por tipo no template
    arquivos_map = {}
    for arquivo in arquivos:
        arquivos_map[arquivo.tipo] = arquivo.arquivo.url

    conclusao_value = obra.servicos.first().conclusao if obra.servicos.exists() else 0.0
    conclusao = "{:.2f}%".format(conclusao_value)    
    total_investido = calcular_preco_obra(obra)
    servico = obra.servicos.first() if obra.servicos.exists() else None
    valor_parcial_total = calculate_partial_total(servico) if servico else "R$ 0,00"
    numero_fiscalizacoes = contar_fiscalizacoes_passagem_molhada(obra)
    informacoes_servicos_table = obter_itens_servico(obra) # Certifique-se de ajustar essa função
    columns = ['Status', 'Tipo', 'Descrição', 'Valor Investido', 'Valor Executado', 'Conclusão']
    servicos_table = {
        'title': 'Lista de Serviços',
        'columns': columns,
        'data': informacoes_servicos_table,
    }

    return render(request, 'obras/obra_detalhe.html', {
        'obra': obra,
        'conclusao': conclusao,
        'conclusao_value': conclusao_value,
        'total_investido': total_investido,
        'fiscalizacoes': numero_fiscalizacoes,
        'servicos_table': servicos_table,
        'valor_parcial_total': valor_parcial_total,
        'arquivos_map': arquivos_map  # Adicione este dicionário ao contexto
    })
