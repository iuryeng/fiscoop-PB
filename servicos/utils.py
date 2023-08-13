# utils.py


import locale


def calculate_partial_value(item):
    qnt_exc = item.qnt_exc 
    val_uni_c_bdi = item.val_uni_c_bdi 
    return qnt_exc * val_uni_c_bdi


def calculate_partial_total(servico):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    total_parcial = sum(item.valor_parcial for item in servico.itens.all())
    return locale.currency(total_parcial, grouping=True)



def calculate_completion(item):
    if item.qnt_exc is None or item.qnt is None or item.qnt == 0:
        return 0.0

    return (item.qnt_exc / item.qnt) * 100



def calculate_service_completion(servico):
    total_value_of_all_items = sum(item.total for item in servico.itens.all() if item.total is not None)
    weighted_completion = 0
    for item in servico.itens.all():
        if item.total is not None and item.conclusao_item is not None and total_value_of_all_items > 0:
            peso_percent = (item.total / total_value_of_all_items) * 100
            weighted_completion += peso_percent * item.conclusao_item

    if total_value_of_all_items == 0:
        return 0.0

    return weighted_completion / 100


def obter_itens_servico(obra):
    # Definindo o local para o Brasil
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    informacoes_servicos_table = []
    servicos = obra.servicos.all()

    for servico in servicos:
        for item in servico.itens.all():
            # Formatando o total como moeda
            total_formatado = locale.currency(item.total, grouping=True)

            # Formatando o valor executado como  moeda
            valor_parcial_formatado = locale.currency(item.valor_parcial, grouping=True)

            # Formatando a conclusão como porcentagem
            conclusao_formatada = f"{item.conclusao_item}%"

            # Obtendo a representação legível do status
            status_display = item.get_status_display()  # Ajuste o nome do método se necessário

            tipo_display = item.get_tipo_display()

             
            item_data = {
                'Status': status_display,
                'Tipo': item.tipo,
                'Descrição': item.descricao,
                'Total': total_formatado,
                'Valor Parcial': valor_parcial_formatado,
                'Conclusão': conclusao_formatada
            }
            informacoes_servicos_table.append(item_data)

    return informacoes_servicos_table



