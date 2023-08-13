from django.db import models

class Empresa(models.Model):
    nome = models.CharField(max_length=200)
    cnpj = models.CharField(max_length=14, unique=True, blank=True, null=True)  # CNPJ da empresa
    numero_registro = models.CharField(max_length=100, blank=True, null=True)  # Número de Registro da empresa
    representante_legal = models.CharField(max_length=200, blank=True, null=True)  # Representante Legal
    endereco = models.CharField(max_length=200, blank=True, null=True)
    cidade = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    pais = models.CharField(max_length=50, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    gerente_tecnico = models.CharField(max_length=200, blank=True, null=True)  # Gerente Técnico
  



    # Adicione mais campos conforme necessário
    def __str__(self):
        return self.nome
