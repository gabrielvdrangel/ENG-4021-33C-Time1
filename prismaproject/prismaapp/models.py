from django.db import models

class usuario(models.Model):
    nome = models.CharField(max_length=100)
    login = models.IntegerField(unique=True)
    senha = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    curso = models.CharField(max_length=100)
    periodo = models.IntegerField()

class publicacoes(models.Model):
    Nome = models.CharField(max_length=100)
    descricao = models.TextField()
    data_publicacao = models.DateTimeField(auto_now_add=True)
