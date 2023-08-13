from django.db import models
from smart_selects.db_fields import ChainedForeignKey
from associacoes.models import Associacao
from beneficiarios.models import Beneficiario
from empresas.models import Empresa
from .choices import GERENCIAS, MUNICIPIOS, LOTES, STATUS_CHOICES, TIPOS_ARQUIVO_CHOICES


class Obra(models.Model):
    nome = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='NAO_INI')
    edital = models.CharField(max_length=50, null=True)
    empresa_encarregada = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True, blank=True)
    lote = models.CharField(max_length=200, choices=LOTES, blank=True, null=True)
    regional = models.CharField(max_length=200, choices=GERENCIAS, blank=True, null=True)
    municipio = models.CharField(max_length=200, choices=MUNICIPIOS, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.nome


class Cisterna(Obra):
    TIPOS_OBRA = (
        ('CIST', 'Cisterna'),
    )
    associacao = models.ForeignKey(Associacao, on_delete=models.CASCADE, related_name='cisternas', blank=True, null=True)
    beneficiario = ChainedForeignKey(
        Beneficiario, 
        chained_field="associacao",
        chained_model_field="associacao", 
        show_all=False, 
        auto_choose=True,
        sort=True,
        on_delete=models.CASCADE, 
        related_name='cisterna', 
        blank=True, 
        null=True
    )
    


class PassagemMolhada(Obra):
    TIPOS_OBRA = (
        ('PASS', 'Passagem Molhada'),
    )
    associacao = models.ForeignKey(Associacao, on_delete=models.CASCADE, related_name='passagens_molhadas', blank=True, null=True)
   


class ObraArquivo(models.Model):
  
    arquivo = models.FileField(upload_to='obras_arquivos/')
    tipo = models.CharField(max_length=20, choices=TIPOS_ARQUIVO_CHOICES)

    class Meta:
        abstract = True

class ObraArquivoCisterna(ObraArquivo):
    cisterna = models.ForeignKey(Cisterna, on_delete=models.CASCADE)

    def __str__(self):
        return f"Arquivo da obra {self.cisterna.nome}: {self.tipo}"

class ObraArquivoPassagemMolhada(ObraArquivo):
    passagem_molhada = models.ForeignKey(PassagemMolhada, on_delete=models.CASCADE)

    def __str__(self):
        return f"Arquivo da obra {self.passagem_molhada.nome}: {self.tipo}"   # ou qualquer outro campo que faça sentido para sua aplicação