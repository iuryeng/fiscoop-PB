from django.contrib import admin
from .models import FiscalizacaoCisterna, FiscalizacaoItemCisterna, FiscalizacaoItemPassagemMolhada, FiscalizacaoPassagemMolhada

class FiscalizacaoItemCisternaInline(admin.TabularInline):
    model = FiscalizacaoItemCisterna
    extra = 1


class FiscalizacaoItemPassagemMolhadaInline(admin.TabularInline):
    model = FiscalizacaoItemPassagemMolhada
    extra = 1
    

class FiscalizacaoCisternaAdmin(admin.ModelAdmin):
    list_display = ['data_fiscalizacao', 'obra_cisterna', 'status']
    search_fields = ['obra_cisterna__nome', 'status']
    list_filter = ['status']
    list_editable = ['status']
    inlines = [FiscalizacaoItemCisternaInline]

class FiscalizacaoPassagemMolhadaAdmin(admin.ModelAdmin):
    list_display = ['data_fiscalizacao', 'obra_passagem_molhada', 'status']
    search_fields = ['obra_passagem_molhada__nome', 'status']
    list_filter = ['status']
    list_editable = ['status']
    inlines = [FiscalizacaoItemPassagemMolhadaInline]

admin.site.register(FiscalizacaoCisterna, FiscalizacaoCisternaAdmin)
admin.site.register(FiscalizacaoPassagemMolhada, FiscalizacaoPassagemMolhadaAdmin)
