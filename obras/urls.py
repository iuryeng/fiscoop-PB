from django.urls import path
from . import views

app_name = 'obras' # linha adicionada

urlpatterns = [
    path('obras/cisterna/<int:obra_id>/', views.cisterna_detalhe, name='cisterna_detalhe'),
    path('obras/passagem-molhada/<int:obra_id>/', views.passagem_molhada_detalhe, name='passagem_molhada_detalhe'),    
    path('graficos/', views.obras_graficos, name='graficos'),
    path('geral/', views.obras_geral, name='geral'),
]

