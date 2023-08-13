
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone

from obras.models import Cisterna, PassagemMolhada
from recursos_humanos.models import Pessoa
from .choices import SEVERIDADES, STATUS, CATEGORIAS

class ProblemaBase(models.Model):
    pessoa_identificou = models.ForeignKey(Pessoa, on_delete=models.SET_NULL, blank=True, null=True)
    descricao = models.TextField()
    data_identificacao =  models.DateField(default=timezone.now)
    categoria = models.CharField(max_length=4, choices=CATEGORIAS, default='MAT')
    severidade = models.CharField(max_length=4, choices=SEVERIDADES, default='BAIX')
    status = models.CharField(max_length=9, choices=STATUS, default='ABERTO')
    imagem_problema = models.ImageField(upload_to='problemas_imagens/', blank=True, null=True)
    acao_corretiva = models.TextField(blank=True, null=True)
    data_prevista_resolucao = models.DateField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'Problema: {self.descricao[:50]}... Status: {self.get_status_display()}'

class ProblemaCisterna(ProblemaBase):
    cisterna = models.ForeignKey(Cisterna, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def obra(self):
        return self.cisterna

class ProblemaPassagemMolhada(ProblemaBase):
    passagem_molhada = models.ForeignKey(PassagemMolhada, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def obra(self):
        return self.passagem_molhada

class ResolucaoBase(models.Model):
    data_resolucao = models.DateField(default=timezone.now)
    responsavel_resolucao = models.CharField(max_length=200, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'Resolução para o problema {self.problema.id}'

class ResolucaoCisterna(ResolucaoBase):
    problema = models.OneToOneField(ProblemaCisterna, on_delete=models.CASCADE)

class ResolucaoPassagemMolhada(ResolucaoBase):
    problema = models.OneToOneField(ProblemaPassagemMolhada, on_delete=models.CASCADE)

@receiver(post_save, sender=ResolucaoCisterna)
@receiver(post_save, sender=ResolucaoPassagemMolhada)
def update_problema_status(sender, instance, **kwargs):
    problema = instance.problema
    problema.status = 'RESOLVIDO'
    problema.save()