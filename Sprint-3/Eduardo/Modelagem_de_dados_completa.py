# models.py

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class Curso(models.Model):
    periodo = models.CharField(max_length=100)
    segmento = models.CharField(max_length=100)
    conexoes = models.TextField(blank=True)
    opcoes_carreira = models.TextField(blank=True)

    def __str__(self):
        return self.periodo


class Usuario(AbstractUser):
    """
    Usuário da plataforma.

    AbstractUser já fornece:
    - username
    - password (armazenada com hash)
    - first_name
    - last_name
    - email
    etc.
    """

    # Nome é tratado pelo first_name/last_name do AbstractUser,
    # mas pode ser substituído por um campo próprio se necessário.

    email = models.EmailField(unique=True)

    local_moradia = models.CharField(max_length=255, blank=True)

    curso = models.OneToOneField(
        Curso,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="usuario",
    )

    preferencias = models.JSONField(
        default=dict,
        blank=True,
    )

    area_pessoal = models.TextField(blank=True)

    def __str__(self):
        return self.get_full_name() or self.username


class Oportunidade(models.Model):

    class Tipo(models.TextChoices):
        MONITORIA = "MONITORIA", "Monitoria"
        LIGA_ACADEMICA = "LIGA_ACADEMICA", "Liga Acadêmica"
        ESTAGIO = "ESTAGIO", "Estágio"
        EMPREGO = "EMPREGO", "Emprego"
        PROJETO = "PROJETO", "Projeto"
        OUTRO = "OUTRO", "Outro"

    tipo = models.CharField(
        max_length=50,
        choices=Tipo.choices,
    )

    processo_seletivo = models.BooleanField(default=False)

    beneficios = models.TextField(blank=True)

    descricao_vaga = models.TextField()

    remuneracao = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )

    prazo_inscricao = models.DateTimeField(
        null=True,
        blank=True,
    )

    forma_inscricao = models.TextField(blank=True)

    feedbacks = models.TextField(blank=True)

    usuarios = models.ManyToManyField(
        Usuario,
        through="UsuarioOportunidade",
        related_name="oportunidades",
        blank=True,
    )

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.descricao_vaga[:50]}"


class ProcessoSeletivo(models.Model):
    oportunidade = models.OneToOneField(
        Oportunidade,
        on_delete=models.CASCADE,
        related_name="processo",
    )

    data = models.DateTimeField()

    dinamica = models.TextField(blank=True)

    pitch = models.TextField(blank=True)

    curriculo = models.FileField(
        upload_to="curriculos/",
        blank=True,
        null=True,
    )

    cr = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
        ],
    )

    def __str__(self):
        return f"Processo seletivo - {self.oportunidade}"


class UsuarioOportunidade(models.Model):
    """
    Tabela intermediária entre Usuario e Oportunidade.

    Representa a relação N:N indicada no diagrama:
        Usuário 1..N <-> 1..N Oportunidade
    """

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="usuario_oportunidades",
    )

    oportunidade = models.ForeignKey(
        Oportunidade,
        on_delete=models.CASCADE,
        related_name="usuario_oportunidades",
    )

    local = models.CharField(
        max_length=255,
        blank=True,
    )

    disponibilidade = models.TextField(
        blank=True,
    )

    aberto_para_quais_periodos = models.TextField(
        blank=True,
    )

    segmento = models.CharField(
        max_length=100,
        blank=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "oportunidade"],
                name="unique_usuario_oportunidade",
            )
        ]

    def __str__(self):
        return f"{self.usuario} - {self.oportunidade}"
