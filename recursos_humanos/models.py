from django.db import models


class Cargo(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    
    def __str__(self):
        return self.titulo

# Create your models here.
class Funcao(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.titulo


class Pessoa(models.Model):
    nome = models.CharField(max_length=200)
    cargo = models.ForeignKey(Cargo, on_delete=models.SET_NULL, null=True, blank=True)
    funcao = models.ForeignKey(Funcao, on_delete=models.SET_NULL, null=True, blank=True)
    matricula = models.CharField(max_length=20, unique=True, null = True) 
    email = models.EmailField()
    telefone = models.CharField(max_length=15, blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    data_contratacao = models.DateField(blank=True, null=True)
    foto = models.ImageField(upload_to='pessoas_fotos/', blank=True, null=True)
    experiencia = models.TextField(blank=True, null=True) 

    def __str__(self):
        return self.nome