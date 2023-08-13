from django.contrib import admin
from .models import ViagemCister, ViagemPassagemMolhada, Municipio, Comunidade

class ViagemCisterAdmin(admin.ModelAdmin):
    filter_horizontal = ('equipe', 'cisternas',)

class ViagemPassagemMolhadaAdmin(admin.ModelAdmin):
    filter_horizontal = ('equipe', 'passagens_molhadas',)

admin.site.register(ViagemCister, ViagemCisterAdmin)
admin.site.register(ViagemPassagemMolhada, ViagemPassagemMolhadaAdmin)
admin.site.register(Municipio)
admin.site.register(Comunidade)
