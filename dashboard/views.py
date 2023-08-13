# dashboard/views.py
from django.shortcuts import render
from associacoes.analises import get_total_beneficiarios, get_total_comunidades

from dashboard.utils import get_municipios_com_obras, get_total_cisternas, get_total_passagens_molhadas, get_total_municipios_impactados

def dashboard(request):
    context = {
        'municipios_com_obras': get_municipios_com_obras(),
        'total_cisternas': get_total_cisternas(),
        'total_passagens_molhadas': get_total_passagens_molhadas(),
        'total_municipios_impactados': get_total_municipios_impactados(),
        'total_comunidades' : get_total_comunidades(),
        'total_beneficiarios': get_total_beneficiarios(),
    }
    return render(request, 'dashboard/index.html', context)
