from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    email = models.EmailField(unique=True, null=True, blank=True)
    matricula = models.IntegerField(unique=True, null=True, blank=True)
    curso = models.CharField(max_length=100, null=True, blank=True)
    periodo = models.IntegerField(null=True, blank=True)
    seguindo = models.ManyToManyField("self", symmetrical=False, related_name="seguidores", blank=True)
    salvos = models.ManyToManyField( "Oportunidade", related_name="salvo_por",blank=True)
    imagem_url = models.URLField(max_length=500, null=True, blank=True)

class Oportunidade(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="oportunidades",
    )
    curtidas = models.IntegerField(default=0)
    nome = models.CharField(max_length=100)
    TIPO_CHOICES = [
        ("evento", "Evento"),
        ("monitoria", "Monitoria"),
        ("iniciacao_cientifica", "Iniciação científica"),
        ("estagio", "Estágio"),
        ("outro", "Outro"),
    ]
    tipo = models.CharField(max_length=100, choices=TIPO_CHOICES)
    descricao = models.TextField()
    limite_inscricao = models.DateTimeField()
    data_publicacao = models.DateTimeField(auto_now_add=True)
    imagem_url = models.URLField(max_length=500, null=True, blank=True)

