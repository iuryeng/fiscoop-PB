from django.contrib import admin
from .models import ProblemaCisterna, ProblemaPassagemMolhada, ResolucaoCisterna, ResolucaoPassagemMolhada

class ResolucaoCisternaInline(admin.StackedInline):
    model = ResolucaoCisterna
    extra = 0

class ResolucaoPassagemMolhadaInline(admin.StackedInline):
    model = ResolucaoPassagemMolhada
    extra = 0

class ProblemaBaseAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'data_identificacao', 'categoria', 'severidade', 'status']
    search_fields = ['descricao', 'categoria', 'status']
    list_filter = ['categoria', 'severidade', 'status']

class ProblemaCisternaAdmin(ProblemaBaseAdmin):
    inlines = [ResolucaoCisternaInline]

class ProblemaPassagemMolhadaAdmin(ProblemaBaseAdmin):
    inlines = [ResolucaoPassagemMolhadaInline]

admin.site.register(ProblemaCisterna, ProblemaCisternaAdmin)  
admin.site.register(ProblemaPassagemMolhada, ProblemaPassagemMolhadaAdmin)
