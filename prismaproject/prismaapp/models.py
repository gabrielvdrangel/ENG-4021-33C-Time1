from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    matricula = models.IntegerField(unique=True, null=True, blank=True)
    curso = models.CharField(max_length=100, null=True, blank=True)
    periodo = models.IntegerField(null=True, blank=True)
    imagem_url = models.URLField(max_length=500, null=True, blank=True)

class Oportunidade(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="oportunidades",
    )
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    descricao = models.TextField()
    limite_inscricao = models.DateTimeField()
    data_publicacao = models.DateTimeField(auto_now_add=True)
    imagem_url = models.URLField(max_length=500, null=True, blank=True)

