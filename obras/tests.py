from django.contrib import admin
from .models import ServicoCisterna, ServicoPassagemMolhada

class ServicoAdmin(admin.ModelAdmin):
    list_display = ['item', 'descricao', 'total', 'obra']
    search_fields = ['descricao']

admin.site.register(ServicoCisterna, ServicoAdmin)
admin.site.register(ServicoPassagemMolhada, ServicoAdmin)
