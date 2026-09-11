from django.db import models
from django.contrib.auth.models import User


class Usuario(models.Model):
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="perfil"
    )

    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    local_de_moradia = models.CharField(max_length=150)
    faculdade = models.CharField(max_length=150)
    curso = models.CharField(max_length=150)
    periodo = models.CharField(max_length=50)
    preferencias = models.TextField(blank=True)

    def __str__(self):
        return self.nome


class AreaPessoal(models.Model):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name="area_pessoal"
    )

    apelido = models.CharField(max_length=50)

    def __str__(self):
        return f"Área pessoal de {self.apelido}"


class Oportunidade(models.Model):
    tipo = models.CharField(max_length=100)
    processo_seletivo = models.TextField()
    beneficios = models.TextField(blank=True)
    descricao_vaga = models.TextField()
    remuneracao = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    prazo_inscricao = models.DateTimeField()
    forma_inscricao = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.tipo} - {self.processo_seletivo}"


class AreaBusca(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="areas_busca"
    )

    local = models.CharField(max_length=150)
    disponibilidade = models.CharField(max_length=150)

    periodo = models.CharField(
        max_length=150,
        help_text="Períodos para os quais o usuário está disponível"
    )

    segmento = models.CharField(max_length=100)

    oportunidades = models.ManyToManyField(
        Oportunidade,
        related_name="areas_busca",
        blank=True
    )

    def __str__(self):
        return f"Busca de {self.usuario.nome}"
