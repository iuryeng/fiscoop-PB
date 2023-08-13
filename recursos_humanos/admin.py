from django.contrib import admin


from .models import Cargo, Pessoa, Funcao

class PessoaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'funcao', 'email', 'telefone', 'data_contratacao')
    search_fields = ('nome', 'email', 'funcao__titulo',)
    list_filter = ('funcao',)
    ordering = ('nome',)

class FuncaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descricao')
    search_fields = ('titulo',)
    ordering = ('titulo',)

class CargoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descricao')
    search_fields = ('titulo',)
    ordering = ('titulo',)

admin.site.register(Pessoa, PessoaAdmin)
admin.site.register(Funcao, FuncaoAdmin)
admin.site.register(Cargo, CargoAdmin)