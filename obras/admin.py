# admin.py

from django.contrib import admin
from .models import Cisterna, PassagemMolhada, ObraArquivoCisterna, ObraArquivoPassagemMolhada

class ObraArquivoCisternaInline(admin.TabularInline):  
    model = ObraArquivoCisterna
    extra = 1  # Define quantos campos vazios serão mostrados por padrão

class ObraArquivoPassagemMolhadaInline(admin.TabularInline):
    model = ObraArquivoPassagemMolhada
    extra = 1

class CisternaAdmin(admin.ModelAdmin):
    search_fields = ['nome', 'empresa_encarregada__nome', 'lote', 'regional', 'municipio']
    list_filter = ['edital', 'lote', 'regional', 'municipio', 'associacao', 'beneficiario']
    inlines = [ObraArquivoCisternaInline]

class PassagemMolhadaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'edital', 'empresa_encarregada', 'lote', 'regional', 'municipio', 'associacao']
    list_filter = ['edital', 'empresa_encarregada', 'lote', 'regional', 'municipio', 'associacao']
    search_fields = ['nome']
    inlines = [ObraArquivoPassagemMolhadaInline]

admin.site.register(Cisterna, CisternaAdmin)
admin.site.register(PassagemMolhada, PassagemMolhadaAdmin)
admin.site.register(ObraArquivoPassagemMolhada)

