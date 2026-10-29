from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    image_url = models.URLField(max_length=500)
    matricula = models.IntegerField(unique=True)
    curso = models.CharField(max_length=100, null=True, blank=True)
    periodo = models.IntegerField(  null=True, blank=True)

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
    image_url = models.URLField(max_length=500)
