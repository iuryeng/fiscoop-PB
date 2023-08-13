from django import forms
from django.contrib import admin
from .models import ServicoCisterna, ServicoPassagemMolhada, ItemCisterna, ItemPassagemMolhada

class ItemCisternaInline(admin.TabularInline):
    readonly_fields = ('conclusao_item', 'valor_parcial',) # Incluindo o valor_parcial aqui
    model = ItemCisterna
    extra = 1
    fields = ('status', 'tipo', 'descricao', 'uni', 'qnt_exc', 'qnt', 'val_uni_s_bdi', 'val_uni_c_bdi', 'total', 'valor_parcial') # Incluindo o valor_parcial aqui também

class ItemPassagemMolhadaInline(admin.TabularInline):
    readonly_fields = ('conclusao_item', 'valor_parcial',) # Incluindo o valor_parcial aqui
    model = ItemPassagemMolhada
    extra = 1
    # Se necessário, adicione o 'fields' aqui também, similar ao ItemCisternaInline

class ServicoCisternaAdmin(admin.ModelAdmin):
    readonly_fields = ('conclusao',)
    inlines = [ItemCisternaInline]

class ServicoPassagemMolhadaAdmin(admin.ModelAdmin):
    readonly_fields = ('conclusao',)
    inlines = [ItemPassagemMolhadaInline]

admin.site.register(ServicoCisterna, ServicoCisternaAdmin)
admin.site.register(ServicoPassagemMolhada, ServicoPassagemMolhadaAdmin)
