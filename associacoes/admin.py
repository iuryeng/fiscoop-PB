from django.contrib import admin
from associacoes.analises import analise_associacoes_por_municipio, analise_beneficiarios_por_associacao, analise_comunidade_por_associacao
from associacoes.models import Associacao, AssociacaoGraficos



from beneficiarios.models import Beneficiario

# Register your models here.
class BeneficiarioInline(admin.TabularInline):
    model = Beneficiario
    extra = 1  # Exibe 1 campo extra vazio para adicionar novos Beneficiários

class AssociacaoAdmin(admin.ModelAdmin):
    inlines = [BeneficiarioInline]
    search_fields = ['nome', 'municipio']
    

class AssociacaoGraficosAdmin(admin.ModelAdmin):
   
    change_list_template = 'admin/associacao_change_list.html'  # Adicione esta linha
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['associacoes_por_municipio_plot'] = analise_associacoes_por_municipio()
        extra_context['comunidade_por_associacao_plot'] = analise_comunidade_por_associacao()
        extra_context['beneficiarios_por_associacao_plot'] = analise_beneficiarios_por_associacao()
        return super().changelist_view(request, extra_context=extra_context)

    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
 
    

admin.site.register(Associacao, AssociacaoAdmin)
admin.site.register(AssociacaoGraficos, AssociacaoGraficosAdmin)

