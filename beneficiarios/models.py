from django.db import models

from associacoes.models import Associacao

from django.core.validators import RegexValidator
from django.db import models

from associacoes.models import Associacao

cpf_regex = r'^\d{3}\.\d{3}\.\d{3}-\d{2}$'
cpf_validator = RegexValidator(cpf_regex, 'CPF deve ter o formato: XXX.XXX.XXX-XX')

class Beneficiario(models.Model):
    nome = models.CharField(max_length=200)
    cpf = models.CharField(max_length=14, validators=[cpf_validator], unique=True, null=True)
    comunidade = models.CharField(max_length=200, unique=False, null=True) 
    associacao = models.ForeignKey(Associacao, on_delete=models.CASCADE, related_name='beneficiarios', blank=True, null=True)

    def __str__(self):
        return self.nome
