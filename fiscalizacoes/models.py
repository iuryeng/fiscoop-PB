from django.db import models
from django.forms import ValidationError
from obras.choices import STATUS_CHOICES
from obras.models import Cisterna, PassagemMolhada
from recursos_humanos.models import Pessoa
from servicos.models import ItemCisterna, ItemPassagemMolhada, ServicoCisterna, ServicoPassagemMolhada
from django.db.models.signals import post_save
from django.dispatch import receiver


class FiscalizacaoItemCisterna(models.Model):
    fiscalizacao = models.ForeignKey('FiscalizacaoCisterna', on_delete=models.CASCADE)
    item = models.ForeignKey(ItemCisterna, on_delete=models.CASCADE)
    qnt = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def clean(self):
        # Obtenha o item do serviço correspondente diretamente
        item = self.item
        
        # Validações
        if self.qnt < 0 or self.qnt > item.qnt:
            raise ValidationError(f"A quantidade fornecida ({self.qnt}) é inválida. "
                                f"Por favor, insira um valor entre 0 e {item.qnt}.")
   
# Dentro de FiscalizacaoItemPassagemMolhada
    

class FiscalizacaoItemPassagemMolhada(models.Model):
    fiscalizacao = models.ForeignKey('FiscalizacaoPassagemMolhada', on_delete=models.CASCADE)
    item = models.ForeignKey(ItemPassagemMolhada, on_delete=models.CASCADE )
    qnt = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    # Dentro de FiscalizacaoItemPassagemMolhada
    def clean(self):
        # Obtenha o item do serviço correspondente diretamente
        item = self.item
        
        # Validações
        if self.qnt < 0 or self.qnt > item.qnt:
            raise ValidationError(f"A quantidade fornecida ({self.qnt}) é inválida. "
                                f"Por favor, insira um valor entre 0 e {item.qnt}.")

  
class FiscalizacaoCisterna(models.Model):
    viagem = models.ForeignKey('viagens.ViagemCister', on_delete=models.SET_NULL, null=True, blank=True, editable=True)
    data_fiscalizacao = models.DateField(verbose_name="Data da Fiscalização", blank=True, null=True)
    responsavel_fiscalizacao = models.ForeignKey(Pessoa, on_delete=models.SET_NULL, verbose_name="Responsável pela Fiscalização", blank=True, null=True)
    obra_cisterna = models.ForeignKey(Cisterna, on_delete=models.CASCADE, related_name='fiscalizacoes_cisterna', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True)
    itens = models.ManyToManyField(ItemCisterna, through='FiscalizacaoItemCisterna')

    def save(self, *args, **kwargs):
        # Quando criamos uma nova fiscalização, inicializamos seu status
        # com o status atual da obra associada
        if not self.status:
            self.status = self.obra_cisterna.status
        
        # Atualizamos o status da obra associada com o status da fiscalização
        self.obra_cisterna.status = self.status
        self.obra_cisterna.save()
        
        super(FiscalizacaoCisterna, self).save(*args, **kwargs)


class FiscalizacaoPassagemMolhada(models.Model):
    viagem = models.ForeignKey('viagens.ViagemPassagemMolhada', on_delete=models.SET_NULL, null=True, blank=True, editable=True)
    data_fiscalizacao = models.DateField(verbose_name="Data da Fiscalização", blank=True, null=True)
    responsavel_fiscalizacao = models.ForeignKey(Pessoa, on_delete=models.SET_NULL, verbose_name="Responsável pela Fiscalização", blank=True, null=True)
    obra_passagem_molhada = models.ForeignKey(PassagemMolhada, on_delete=models.CASCADE, related_name='fiscalizacoes_passagem_molhada', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True)
    itens = models.ManyToManyField(ItemPassagemMolhada, through='FiscalizacaoItemPassagemMolhada')

    def save(self, *args, **kwargs):
        # Quando criamos uma nova fiscalização, inicializamos seu status
        # com o status atual da obra associada
        if not self.status:
            self.status = self.obra_passagem_molhada.status
        
        # Atualizamos o status da obra associada com o status da fiscalização
        self.obra_passagem_molhada.status = self.status
        self.obra_passagem_molhada.save()
        
        super(FiscalizacaoPassagemMolhada, self).save(*args, **kwargs)



@receiver(post_save, sender=FiscalizacaoItemCisterna)
def update_servico_cisterna(sender, instance, **kwargs):
    # Obtenha o item do serviço correspondente
    item = ItemCisterna.objects.get(id=instance.item.id)

    # Atualize a quantidade executada no item com o valor da fiscalização
    item.qnt_exc = instance.qnt
    item.save()


@receiver(post_save, sender=FiscalizacaoItemPassagemMolhada)
def update_servico_passagem_molhada(sender, instance, **kwargs):
    # Obtenha o item do serviço correspondente
    item = ItemPassagemMolhada.objects.get(id=instance.item.id)

    # Atualize a quantidade executada no item com o valor da fiscalização
    item.qnt_exc = instance.qnt
    item.save()



