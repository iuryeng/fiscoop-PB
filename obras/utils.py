from django.urls import reverse
from django.db.models import Sum
import locale
from fiscalizacoes.models import FiscalizacaoCisterna, FiscalizacaoPassagemMolhada
from obras.choices import MUNICIPIOS
from obras.models import Cisterna, ObraArquivoCisterna, PassagemMolhada, ObraArquivoPassagemMolhada
from servicos.models import ItemCisterna, ItemPassagemMolhada
from servicos.utils import calculate_service_completion


def contar_status_e_municipios(obras):
    total_execucao = total_concluidas = total_planejadas = total_paralisadas = 0 # Inicialize total_paralisadas aqui
    municipios = set()
    for obra in obras:
        if obra.status == 'EXEC':
            total_execucao += 1
        elif obra.status == 'CONCL':
            total_concluidas += 1
        elif obra.status == 'NAO_INI':
            total_planejadas += 1
        elif obra.status == 'PARA':  
            total_paralisadas += 1
        municipios.add(obra.municipio)
    return total_execucao, total_concluidas, total_planejadas, total_paralisadas, municipios



def gerar_informacoes_obras():
    informacoes = []
    
    cisternas = Cisterna.objects.all()
    passagens_molhadas = PassagemMolhada.objects.all()

    total_cisternas = cisternas.count()
    total_passagens_molhadas = passagens_molhadas.count()

    total_execucao_cisternas, total_concluidas_cisternas, total_planejadas_cisternas, total_paralisadas_cisternas, municipios_impactados_cisternas = contar_status_e_municipios(cisternas)
    total_execucao_passagens, total_concluidas_passagens, total_planejadas_passagens, total_paralisadas_passagens, municipios_impactados_passagens = contar_status_e_municipios(passagens_molhadas)

    total_municipios_impactados = municipios_impactados_cisternas.union(municipios_impactados_passagens)

    for cisterna in cisternas:
        conclusao_cisterna = calculate_service_completion(cisterna.servicos.first()) if cisterna.servicos.first() else 0
        detalhes_url = reverse('obras:cisterna_detalhe', args=[cisterna.id])
        arquivos = ObraArquivoCisterna.objects.filter(cisterna=cisterna)
        arquivos_info = [
          {
            'tipo': arquivo.tipo,
            'url': reverse('admin:obras_obraarquivocisterna_change', args=[arquivo.id])
          }
          for arquivo in arquivos
        ]
        informacoes.append({
            'id': cisterna.id,
            'tipo': 'Cisterna',
            'nome': cisterna.nome,
            'edital': cisterna.edital,
            'empresa_encarregada': cisterna.empresa_encarregada.nome,
            'lote': cisterna.lote,
            'regional': cisterna.regional,
            'municipio': cisterna.municipio,
            'numero_servicos': cisterna.servicos.count(),
            'status': cisterna.status,
            'conclusao': conclusao_cisterna,
            'detalhes_url': detalhes_url,
            'arquivos': arquivos_info,
        })

    for passagem in passagens_molhadas:
        conclusao_passagem = calculate_service_completion(passagem.servicos.first()) if passagem.servicos.first() else 0
        detalhes_url = reverse('obras:passagem_molhada_detalhe', args=[passagem.id])
        arquivos = ObraArquivoPassagemMolhada.objects.filter(passagem_molhada=passagem)
        arquivos_info = [
          {
            'tipo': arquivo.tipo,
            'url': reverse('admin:obras_obraarquivopassagemmolhada_change', args=[arquivo.id])
          }
          for arquivo in arquivos
        ]
        informacoes.append({
            'id': passagem.id,
            'tipo': 'Passagem Molhada',
            'nome': passagem.nome,
            'edital': passagem.edital,
            'empresa_encarregada': passagem.empresa_encarregada.nome,
            'lote': passagem.lote,
            'regional': passagem.regional,
            'municipio': passagem.municipio,
            'numero_servicos': passagem.servicos.count(),
            'status': passagem.status,
            'conclusao': conclusao_passagem,
            'detalhes_url': detalhes_url,
            'arquivos': arquivos_info,
        })

    return {
        'informacoes': informacoes,
        'total_municipios_impactados_cisternas': len(municipios_impactados_cisternas),
        'total_municipios_impactados_passagens': len(municipios_impactados_passagens),
        'total_municipios_impactados': len(total_municipios_impactados),
        'total_execucao': total_execucao_cisternas + total_execucao_passagens,
        'total_concluidas': total_concluidas_cisternas + total_concluidas_passagens,
        'total_planejadas': total_planejadas_cisternas + total_planejadas_passagens,
        'total_paralisadas': total_paralisadas_cisternas + total_paralisadas_passagens,
        'total_cisternas': total_cisternas,
        'total_passagens_molhadas': total_passagens_molhadas,
        'total_execucao_cisternas': total_execucao_cisternas,
        'total_concluidas_cisternas': total_concluidas_cisternas,
        'total_planejadas_cisternas': total_planejadas_cisternas,
        'total_execucao_passagens': total_execucao_passagens,
        'total_concluidas_passagens': total_concluidas_passagens,
        'total_planejadas_passagens': total_planejadas_passagens,
    }


def calcular_total_investimentos():
    # Configurar o locale para o padrão brasileiro
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    
    total_cisternas = ItemCisterna.objects.all().aggregate(Sum('total'))['total__sum'] or 0
    total_passagens_molhadas = ItemPassagemMolhada.objects.all().aggregate(Sum('total'))['total__sum'] or 0
    total = total_cisternas + total_passagens_molhadas

    # Formatar o total no padrão de moeda brasileiro
    return locale.currency(total, grouping=True)


def calcular_preco_obra(obra):
    # Configurar o locale para o padrão brasileiro
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    
    # Determinar o tipo de obra e calcular o total
    if isinstance(obra, Cisterna):
        servicos = ItemCisterna.objects.filter(servico__obra=obra)
    elif isinstance(obra, PassagemMolhada):
        servicos = ItemPassagemMolhada.objects.filter(servico__obra=obra)
    else:
        return "Tipo de obra inválido"

    total = servicos.aggregate(Sum('total'))['total__sum'] or 0

    # Formatar o total no padrão de moeda brasileiro
    return locale.currency(total, grouping=True)



def calcular_investimentos_por_municipio():
    # Coletando todos os municípios das obras
    municipios_cisternas = Cisterna.objects.values_list('municipio', flat=True).distinct()
    municipios_passagens = PassagemMolhada.objects.values_list('municipio', flat=True).distinct()
    municipios = set(municipios_cisternas).union(set(municipios_passagens))
    
    # Dicionário para armazenar o total investido por município
    investimentos_por_municipio = {}
    
    # Iterando pelos municípios para calcular o total investido
    for municipio in municipios:
        # Cisternas no município
        cisternas_no_municipio = Cisterna.objects.filter(municipio=municipio)
        servicos_cisternas = ItemCisterna.objects.filter(servico__obra__in=cisternas_no_municipio)
        total_cisternas = servicos_cisternas.aggregate(Sum('total'))['total__sum'] or 0
        
        # Passagens Molhadas no município
        passagens_no_municipio = PassagemMolhada.objects.filter(municipio=municipio)
        servicos_passagens = ItemPassagemMolhada.objects.filter(servico__obra__in=passagens_no_municipio)
        total_passagens = servicos_passagens.aggregate(Sum('total'))['total__sum'] or 0
        
        # Adicionando os valores ao dicionário
        investimentos_por_municipio[municipio] = {
            'Cisterna': total_cisternas,
            'Passagem Molhada': total_passagens
        }
        
    return investimentos_por_municipio



def contar_fiscalizacoes_cisterna(obra_cisterna):
    return FiscalizacaoCisterna.objects.filter(obra_cisterna=obra_cisterna).count()


def contar_fiscalizacoes_passagem_molhada(obra_passagem_molhada):
    return FiscalizacaoPassagemMolhada.objects.filter(obra_passagem_molhada=obra_passagem_molhada).count()







