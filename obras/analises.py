import pandas as pd
import plotly.express as px
import plotly.io as pio
from django.utils.safestring import mark_safe
from collections import defaultdict

from obras.utils import calcular_investimentos_por_municipio


def analise_status_obras(informacoes_obras):
    
    # Criar um DataFrame com os dados
    df = pd.DataFrame({
        'Status': ['Em Execução', 'Concluídas', 'Planejadas', 'Paralisadas'],
        'Quantidade': [
            informacoes_obras['total_execucao'],
            informacoes_obras['total_concluidas'],
            informacoes_obras['total_planejadas'],
            informacoes_obras['total_paralisadas']
        ]
    })

    # Verificar se há dados suficientes
    if df['Quantidade'].sum() > 0:
        # Criar um gráfico de barras com Plotly
        fig = px.bar(df, x='Status', y='Quantidade', text='Quantidade',
                     hover_data={'Quantidade': True},
                     barmode='group')

        # Definir o formato da dica de ferramenta
        fig.update_traces(hovertemplate="Status: %{x}<br>Quantidade: %{y}")

        # Definir o gráfico como responsivo
        fig.update_layout(autosize=True)

        # Converter o gráfico em HTML e marcar como seguro
        div = pio.to_html(fig, full_html=False, config={'responsive': True})
        return mark_safe(div)
    
    return "Não há dados suficientes para gerar o gráfico."

def analise_obras_por_municipio(informacoes_obras):
    # Criar uma lista com os dados
    data = []
    for obra in informacoes_obras['informacoes']:
        data.append({
            'Municipio': obra['municipio'],
            'Status': obra['status'],
        })

    # Criar um DataFrame com os dados
    df = pd.DataFrame(data)

    # Verificar se há dados suficientes
    if 'Municipio' in df.columns and df['Municipio'].notna().any():
        # Agrupar por município e contar o número de obras
        df_municipio = df.groupby('Municipio').size().reset_index(name='Quantidade')

        # Criar um gráfico de barras com Plotly
        fig = px.bar(df_municipio, x='Municipio', y='Quantidade', text='Quantidade',
                     hover_data={'Quantidade': True},
                     barmode='group')

        # Definir o formato da dica de ferramenta
        fig.update_traces(hovertemplate="Município: %{x}<br>Quantidade: %{y}")

        # Definir o gráfico como responsivo
        fig.update_layout(autosize=True)

        # Converter o gráfico em HTML e marcar como seguro
        div = pio.to_html(fig, full_html=False, config={'responsive': True})
        return mark_safe(div)

    return "Não há dados suficientes para gerar o gráfico."

def analise_impacto_municipio(informacoes_obras):
    # Criar um DataFrame com os dados
    df = pd.DataFrame({
        'Tipo de Obra': ['Cisternas', 'Passagens Molhadas', 'Total'],
        'Número de Municípios Impactados': [
            informacoes_obras['total_municipios_impactados_cisternas'],
            informacoes_obras['total_municipios_impactados_passagens'],
            informacoes_obras['total_municipios_impactados']
        ]
    })

    # Verificar se há dados suficientes
    if df['Número de Municípios Impactados'].sum() > 0:
        # Criar um gráfico de barras com Plotly
        fig = px.bar(df, x='Tipo de Obra', y='Número de Municípios Impactados', text='Número de Municípios Impactados',
                     hover_data={'Número de Municípios Impactados': True},
                     barmode='group')

        # Definir o formato da dica de ferramenta
        fig.update_traces(hovertemplate="Tipo de Obra: %{x}<br>Número de Municípios Impactados: %{y}")

        # Definir o gráfico como responsivo
        fig.update_layout(autosize=True)

        # Converter o gráfico em HTML e marcar como seguro
        div = pio.to_html(fig, full_html=False, config={'responsive': True})
        return mark_safe(div)

    return "Não há dados suficientes para gerar o gráfico."

    # Criar um DataFrame com os dados
    df = pd.DataFrame({
        'Tipo de Obra': ['Cisternas', 'Passagens Molhadas', 'Total'],
        'Número de Municípios Impactados': [
            informacoes_obras['total_municipios_impactados_cisternas'],
            informacoes_obras['total_municipios_impactados_passagens'],
            informacoes_obras['total_municipios_impactados']
        ]
    })

    # Criar um gráfico de barras com Plotly
    fig = px.bar(df, x='Tipo de Obra', y='Número de Municípios Impactados', text='Número de Municípios Impactados',
                 hover_data={'Número de Municípios Impactados': True},
                 barmode='group')

    # Definir o formato da dica de ferramenta
    fig.update_traces(hovertemplate="Tipo de Obra: %{x}<br>Número de Municípios Impactados: %{y}")

    # Definir o gráfico como responsivo
    fig.update_layout(autosize=True)

    # Converter o gráfico em HTML e marcar como seguro
    div = pio.to_html(fig, full_html=False, config={'responsive': True})
    return mark_safe(div)

def analise_investimentos_por_municipio():
    # Obter os dados dos investimentos por município
    investimentos = calcular_investimentos_por_municipio()

    # Preparar os dados para o DataFrame
    municipios = []
    tipos = []
    valores = []
    for municipio, investimento in investimentos.items():
        municipios.append(municipio)
        tipos.append('Cisterna')
        valores.append(investimento['Cisterna'])

        municipios.append(municipio)
        tipos.append('Passagem Molhada')
        valores.append(investimento['Passagem Molhada'])

    # Criar um DataFrame com os dados
    df = pd.DataFrame({
        'Municipio': municipios,
        'Tipo de Obra': tipos,
        'Investimento': valores
    })

    # Verificar se há dados suficientes
    if df['Investimento'].sum() > 0:
        # Criar um gráfico de barras com Plotly
        fig = px.bar(df, x='Municipio', y='Investimento', color='Tipo de Obra', text='Investimento',
                     hover_data={'Tipo de Obra': True, 'Investimento': True},
                     barmode='group')

        # Definir o formato da dica de ferramenta
        fig.update_traces(hovertemplate="Município: %{x}<br>Tipo de Obra: %{customdata[0]}<br>Investimento: %{y}")

        # Definir o gráfico como responsivo
        fig.update_layout(autosize=True)

        # Converter o gráfico em HTML e marcar como seguro
        div = pio.to_html(fig, full_html=False, config={'responsive': True})
        return mark_safe(div)

    return "Não há dados suficientes para gerar o gráfico."

