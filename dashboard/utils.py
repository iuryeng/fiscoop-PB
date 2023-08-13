from obras.choices import MUNICIPIOS
from obras.models import Cisterna, PassagemMolhada

# Convert MUNICIPIOS to a dictionary
MUNICIPIOS_DICT = dict(MUNICIPIOS)

def get_municipios_com_obras():
    municipios_abrev = list(set(
        list(Cisterna.objects.values_list('municipio', flat=True)) +
        list(PassagemMolhada.objects.values_list('municipio', flat=True))
    ))
    municipios = [MUNICIPIOS_DICT[abrev] for abrev in municipios_abrev if abrev in MUNICIPIOS_DICT]
    return municipios

def get_total_municipios_impactados():
    municipios_cisternas = list(Cisterna.objects.values_list('municipio', flat=True))
    municipios_passagens_molhadas = list(PassagemMolhada.objects.values_list('municipio', flat=True))

    # Combine the two lists and remove duplicates by converting to a set
    total_municipios = len(set(municipios_cisternas + municipios_passagens_molhadas))

    return total_municipios

def get_total_cisternas():
    return Cisterna.objects.count()

def get_total_passagens_molhadas():
    return PassagemMolhada.objects.count()


