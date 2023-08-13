from django.db import models
from django.forms import ValidationError

from servicos.utils import calculate_completion, calculate_partial_value, calculate_service_completion
from .choices import STATUS_CHOICES, TIPO_SERVICO_CISTERNA, TIPO_SERVICO_PASSAGEM_MOLHADA, UNIDADES
from django.db.models.signals import post_save
from django.dispatch import receiver

class Servico(models.Model):
    class Meta:
        abstract = True

    def __str__(self):
        return f'Serviço {self.id} para a obra {self.obra.nome}'

class ServicoCisterna(Servico):
    conclusao = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    obra = models.ForeignKey('obras.Cisterna', on_delete=models.CASCADE, related_name='servicos')

class ServicoPassagemMolhada(Servico):
    conclusao = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    obra = models.ForeignKey('obras.PassagemMolhada', on_delete=models.CASCADE, related_name='servicos')
    

class ItemCisterna(models.Model):
    

    def save(self, *args, **kwargs):
        self.conclusao_item = calculate_completion(self)
        self.valor_parcial = calculate_partial_value(self)
        super(ItemCisterna, self).save(*args, **kwargs)
        self.servico.conclusao = calculate_service_completion(self.servico)
        self.servico.save()
    
    conclusao_item = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, editable=False)    
    servico = models.ForeignKey(ServicoCisterna, on_delete=models.CASCADE, related_name='itens')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='NAO_INI')
    tipo = models.CharField(max_length=25, choices=TIPO_SERVICO_CISTERNA, null=True)
    descricao = models.TextField(blank=True, null=True)
    uni = models.CharField(max_length=50, choices=UNIDADES, blank=True, null=True)
    qnt_exc = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0.0)
    qnt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    val_uni_s_bdi = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    val_uni_c_bdi = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    valor_parcial = models.DecimalField(max_digits=10, decimal_places=2, blank=True,  default=0.0, editable=False)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    

    def clean(self):
        qnt_exc = self.qnt_exc
        qnt = self.qnt
        if qnt_exc is not None and (qnt_exc < 0 or (qnt is not None and qnt_exc > qnt)):
            raise ValidationError('A quantidade executada deve estar entre 0 e a quantidade total ou ser nula.')

    def __str__(self):
        return f'{self.descricao} ({self.tipo})'

    

class ItemPassagemMolhada(models.Model):
    

    def save(self, *args, **kwargs):
        self.conclusao_item = calculate_completion(self)
        self.valor_parcial = calculate_partial_value(self)
        super(ItemPassagemMolhada, self).save(*args, **kwargs)
        self.servico.conclusao = calculate_service_completion(self.servico)
        self.servico.save()

    conclusao_item = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, editable=False)
    servico = models.ForeignKey(ServicoPassagemMolhada, on_delete=models.CASCADE, related_name='itens')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='NAO_INI') 
    tipo = models.CharField(max_length=50, choices=TIPO_SERVICO_PASSAGEM_MOLHADA)    
    descricao = models.TextField(blank=True, null=True)
    uni = models.CharField(max_length=50, choices=UNIDADES, blank=True, null=True)
    qnt_exc = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0.0)
    qnt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    val_uni_s_bdi = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    val_uni_c_bdi = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    valor_parcial = models.DecimalField(max_digits=10, decimal_places=2, blank=True,  default=0.0, editable=False)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
   
    def clean(self):
        qnt_exc = self.qnt_exc
        qnt = self.qnt
        if qnt_exc is not None and (qnt_exc < 0 or (qnt is not None and qnt_exc > qnt)):
            raise ValidationError('A quantidade executada deve estar entre 0 e a quantidade total ou ser nula.')


    def __str__(self):
        return f'{self.descricao} ({self.tipo})'
    

@receiver(post_save, sender=ServicoCisterna)
def update_obra_status_cisterna(sender, instance, **kwargs):
    if instance.conclusao == 100:
        obra = instance.obra
        obra.status = 'CONCL'  # Substitua por seu valor correspondente
        obra.save()

@receiver(post_save, sender=ServicoPassagemMolhada)
def update_obra_status_passagem_molhada(sender, instance, **kwargs):
    if instance.conclusao == 100:
        obra = instance.obra
        obra.status = 'CONCL'  # Substitua por seu valor correspondente
        obra.save()

@receiver(post_save, sender=ItemCisterna)
def atualizar_status_cisterna(sender, instance, **kwargs):
    novo_status = instance.status
    if instance.qnt == 0:
        novo_status = 'NAO_INI'
    elif instance.qnt_exc == instance.qnt:
        novo_status = 'CONCL'
    elif 0 < instance.qnt_exc < instance.qnt:
        novo_status = 'EXEC'
    
    if novo_status != instance.status:
        instance.status = novo_status
        instance.save(update_fields=['status'])

@receiver(post_save, sender=ItemPassagemMolhada)
def atualizar_status_passagem_molhada(sender, instance, **kwargs):
    novo_status = instance.status
    if instance.qnt == 0:
        novo_status = 'NAO_INI'
    elif instance.qnt_exc == instance.qnt:
        novo_status = 'CONCL'
    elif 0 < instance.qnt_exc < instance.qnt:
        novo_status = 'EXEC'
    
    if novo_status != instance.status:
        instance.status = novo_status
        instance.save(update_fields=['status'])


