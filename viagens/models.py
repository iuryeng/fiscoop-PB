from django.db import models
from obras.models import Cisterna, PassagemMolhada
from recursos_humanos.models import Pessoa
from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import m2m_changed


from django.db import models
from smart_selects.db_fields import ChainedManyToManyField

class Municipio(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do Município")

    def __str__(self):
        return self.nome

class Comunidade(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome da Comunidade")
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, related_name='comunidades', verbose_name="Município")

    def __str__(self):
        return self.nome

class Viagem(models.Model):
    data_inicio = models.DateField(verbose_name="Data de Início", default=date.today)
    data_fim = models.DateField(verbose_name="Data de Fim", default=date.today)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, verbose_name="Município")
    comunidades = ChainedManyToManyField(
        Comunidade,
        chained_field="municipio",
        chained_model_field="municipio",
        horizontal=True,
        verbose_name="Comunidades",
        blank=True
    )
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")

    class Meta:
        abstract = True

class ViagemCister(Viagem):
    cisternas = models.ManyToManyField(Cisterna, verbose_name="Obras de Cisternas", blank=True)
    equipe = models.ManyToManyField(Pessoa, related_name='viagens_cister', verbose_name="Equipe")

    def __str__(self):
       return f'Viagem de Cisterna (ID: {self.id}) - Início: {self.data_inicio} - Fim: {self.data_fim}'

class ViagemPassagemMolhada(Viagem):
    passagens_molhadas = models.ManyToManyField(PassagemMolhada, verbose_name="Obras de Passagens Molhadas", blank=True)
    equipe = models.ManyToManyField(Pessoa, related_name='viagens_passagem_molhada', verbose_name="Equipe")

    def __str__(self):
        return f'Viagem de Passagens Molhadas (ID: {self.id}) - Início: {self.data_inicio} - Fim: {self.data_fim}'



@receiver(m2m_changed, sender=ViagemCister.cisternas.through)
def create_fiscalizacao_cisterna(sender, instance, action, **kwargs):
    from fiscalizacoes.models import FiscalizacaoCisterna
    if action == "post_add":
        print(f"Sinal para ViagemCister {instance.id} chamado")
        print(f"Cisternas relacionadas: {instance.cisternas.all()}")
        for cisterna in instance.cisternas.all():
            try:
                fiscalizacao = FiscalizacaoCisterna.objects.create(obra_cisterna=cisterna, viagem=instance)
                print(f"Fiscalização criada: {fiscalizacao}")
            except Exception as e:
                print(f"Erro ao criar fiscalização para cisterna {cisterna}: {e}")


@receiver(m2m_changed, sender=ViagemPassagemMolhada.passagens_molhadas.through)
def create_fiscalizacao_passagem_molhada(sender, instance, action, **kwargs):
    from fiscalizacoes.models import FiscalizacaoPassagemMolhada
    if action == "post_add":
        print(f"Sinal para ViagemPassagemMolhada {instance.id} chamado")
        print(f"Passagens Molhadas relacionadas: {instance.passagens_molhadas.all()}")
        for passagem_molhada in instance.passagens_molhadas.all():
            try:
                fiscalizacao = FiscalizacaoPassagemMolhada.objects.create(obra_passagem_molhada=passagem_molhada, viagem=instance)
                print(f"Fiscalização criada: {fiscalizacao}")
            except Exception as e:
                print(f"Erro ao criar fiscalização para passagem molhada {passagem_molhada}: {e}")