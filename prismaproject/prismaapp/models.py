from django.contrib.auth.models import AbstractUser
from django.db import models


class usuario(AbstractUser):
    image_url = models.URLField(max_length=500,null=True, blank=True)
    matricula = models.IntegerField(unique=True,null=True, blank=True)
    curso = models.CharField(max_length=100, null=True, blank=True)
    periodo = models.IntegerField(  null=True, blank=True)

class oportunidade(models.Model):
    usuario = models.ForeignKey(
        usuario,
        on_delete=models.CASCADE,
        related_name="oportunidades",
    )
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    descricao = models.TextField()
    limite_inscricao = models.DateTimeField()
    data_publicacao = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(max_length=500)
