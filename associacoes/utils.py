from associacoes.models import Associacao

def gerar_informacoes_associacoes():
    """
    Esta função busca todas as associações e retorna uma lista de dicionários com informações relevantes.
    """
    associacoes = Associacao.objects.all()
    informacoes = []

    for associacao in associacoes:
        info = {
            'sigla': associacao.sigla,
            'nome': associacao.nome,
            'comunidades_beneficiadas': associacao.comunidades_beneficiadas,
            'gerencia_responsavel': associacao.gerencia_responsavel,
            'municipio': associacao.municipio,
            'numero_beneficiarios': associacao.beneficiarios.count()
        }
        informacoes.append(info)

    return informacoes
