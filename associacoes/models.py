from django.db import models

class Associacao(models.Model):
    nome = models.CharField(max_length=200, unique=True)
    sigla = models.CharField(max_length=7, unique=True, null=True)
    comunidades_beneficiadas = models.CharField(max_length=200, unique=True, null=True)
    gerencia_responsavel = models.CharField(max_length=200, unique=False, null= True)
    municipio = models.CharField(max_length=200,  unique= False, null=True)

    class Meta:
        ordering = ['nome'] # ordenar por ordem alfabetica

    def __str__(self):
        return f"{self.nome} - {self.municipio}"
    
class AssociacaoGraficos(models.Model):
    # Você pode adicionar campos aqui se precisar, ou deixar vazio
    pass

