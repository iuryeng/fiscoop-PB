import pandas as pd
import plotly.express as px
import plotly.io as pio

from associacoes.models import Associacao
from django.utils.safestring import mark_safe

from beneficiarios.models import Beneficiario


def analise_associacoes_por_municipio():
    associacoes = Associacao.objects.values('municipio')
    df = pd.DataFrame(list(associacoes))

    # Verifique se a coluna 'municipio' existe no DataFrame
    if 'municipio' in df.columns:
        # Além disso, verifique se 'municipio' tem algum dado não-nulo
        if df['municipio'].notna().any():
            df = df.groupby('municipio').size().reset_index(name='qtd_associacoes')
            fig = px.bar(df, x="municipio", y="qtd_associacoes",
                         text="qtd_associacoes",
                         hover_data={"qtd_associacoes": True},
                         barmode="group")

            # Define o formato da dica de ferramenta com o número de associações
            fig.update_traces(hovertemplate="Município: %{x}<br>Número de Associações: %{y}")

            # Adicione esta linha para definir o gráfico como responsivo
            fig.update_layout(autosize=True)

            div = pio.to_html(fig, full_html=False, config={'responsive': True})
            return mark_safe(div)
   
    return "Não há dados suficientes para gerar o gráfico."
    


def analise_comunidade_por_associacao():
    associacoes = Associacao.objects.values('sigla', 'nome', 'municipio', 'comunidades_beneficiadas')
    df = pd.DataFrame(list(associacoes))

    if 'comunidades_beneficiadas' in df.columns:
        # Adiciona uma nova coluna com o número de comunidades beneficiadas por cada associação
        df['num_comunidades'] = df['comunidades_beneficiadas'].apply(lambda x: len(x.split(',')))

        # Cria uma nova coluna concatenando 'nome' e 'municipio', separados por uma quebra de linha
        df['nome_municipio'] = df['nome'] + '<br>(' + df['municipio'] + ')'

        fig = px.pie(df, values='num_comunidades', names='sigla')

        # Atualiza as dicas de ferramenta para mostrar a sigla, o percentual, o nome_municipio e a quantidade de comunidades
        fig.update_traces(textinfo='percent+label',
                          hovertemplate="%{customdata[0]}<br>%{value} comunidades",
                          customdata=df['nome_municipio'])

        div = pio.to_html(fig, full_html=False, config={'responsive': True})
        return mark_safe(div)
    
    return "Não há dados suficientes para gerar o gráfico."



def analise_beneficiarios_por_associacao():
    beneficiarios = Beneficiario.objects.values('associacao__sigla', 'associacao__nome', 'associacao__municipio')
    df = pd.DataFrame(list(beneficiarios))

    if 'associacao__sigla' in df.columns and df['associacao__sigla'].notna().any():
        df = df.groupby(['associacao__sigla', 'associacao__nome', 'associacao__municipio']).size().reset_index(name='qtd_beneficiarios')
        fig = px.bar(df, x="associacao__sigla", y="qtd_beneficiarios", text="qtd_beneficiarios",
                     hover_data=["associacao__nome", "associacao__municipio"],
                     barmode="group")

        # Define o formato da dica de ferramenta com os dados personalizados
        fig.update_traces(hovertemplate="Associação: %{customdata[0]}<br>Município: %{customdata[1]}<br>Número de Beneficiários: %{y}")

        fig.update_layout(autosize=True)
        div = pio.to_html(fig, full_html=False, config={'responsive': True})
        return mark_safe(div)
    
    return "Não há dados suficientes para gerar o gráfico."


def get_total_associacoes():
    return Associacao.objects.count()

def get_total_municipios():
    return Associacao.objects.values('municipio').distinct().count()

def get_total_comunidades():
    all_comunidades = []
    for assoc in Associacao.objects.all():
        comunidades = assoc.comunidades_beneficiadas.split(', ')
        all_comunidades.extend(comunidades)
    return len(set(all_comunidades))



def get_total_beneficiarios():
    # Conte o número total de beneficiários
    total_beneficiarios = Beneficiario.objects.count()

    return total_beneficiarios

