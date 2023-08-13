# associacoes/urls.py
from django.urls import path
from .views import admin_associacoes_graficos

from . import views

app_name = "associacoes"

urlpatterns = [
     path('graficos/', views.associacoes_graficos, name='graficos'),
     path('relatorio/', views.relatorio_associacoes_view, name='relatorio'), 
     path('geral/', views.associacoes_geral, name='geral'),  # nova URL
     path('download/', views.download_associacoes, name='associacoes_download'),
     path('admin/associacoes/associacao/', admin_associacoes_graficos, name='admin_associacoes_graficos'),
    # Adicione mais rotas aqui para outras views em seu aplicativo 'associacoes'
]
