from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class Usuario(AbstractUser):
    email = models.EmailField(unique=True, null=True, blank=True)
    matricula = models.IntegerField(unique=True, null=True, blank=True)
    curso = models.CharField(max_length=100, null=True, blank=True)
    periodo = models.IntegerField(null=True, blank=True)
    seguindo = models.ManyToManyField("self", symmetrical=False, related_name="seguidores", blank=True)
    salvos = models.ManyToManyField( "Oportunidade", related_name="salvo_por",blank=True)
    imagem = models.ImageField(upload_to='usuarios/', max_length=500, null=True, blank=True)

class Oportunidade(models.Model):
    code = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="oportunidades",
    )
    curtidas = models.IntegerField(default=0)
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
    imagem = models.ImageField(upload_to='oportunidades/', max_length=500, null=True, blank=True)
    candidatos = models.ManyToManyField('Usuario', related_name='candidaturas', blank=True)

class Feedback(models.Model):
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="feedbacks_enviados")
    destinatario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="feedbacks_recebidos")
    oportunidade = models.ForeignKey(Oportunidade, on_delete=models.SET_NULL, null=True, blank=True, related_name="feedbacks")
    comentario = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

class Curso(models.Model):
    nome = models.CharField(max_length=150, unique=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome

class Experiencia(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="experiencias")
    titulo = models.CharField(max_length=150)        # cargo/função, ex.: "Trainee de desenvolvimento"
    organizacao = models.CharField(max_length=150)   # ex.: "Empresa Júnior"
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)  # vazio = em andamento
    descricao = models.TextField(blank=True)

    class Meta:
        ordering = ["-data_inicio"]

    @property
    def atual(self):
        return self.data_fim is None

    def __str__(self):
        return f"{self.titulo} - {self.organizacao} ({self.usuario.username})"
