from django.db import migrations

CURSOS_PUC_RIO = [
    "Administração",
    "Arquitetura e Urbanismo",
    "Artes Cênicas",
    "Ciência da Computação",
    "Ciências Biológicas",
    "Ciências Econômicas",
    "Ciências Sociais",
    "Comunicação Social - Cinema",
    "Comunicação Social - Estudos de Mídia",
    "Comunicação Social - Jornalismo",
    "Comunicação Social - Publicidade e Propaganda",
    "Design - Comunicação Visual",
    "Design - Mídia Digital",
    "Design - Moda",
    "Design - Projeto de Produto",
    "Direito",
    "Engenharia Ambiental",
    "Engenharia Civil",
    "Engenharia de Computação",
    "Engenharia de Controle e Automação",
    "Engenharia de Materiais e Nanotecnologia",
    "Engenharia de Petróleo",
    "Engenharia de Produção",
    "Engenharia Elétrica",
    "Engenharia Mecânica",
    "Engenharia Química",
    "Filosofia",
    "Física",
    "Geografia",
    "História",
    "Letras - Português e Inglês",
    "Letras - Português e Literaturas",
    "Letras - Produção Textual",
    "Letras - Tradução",
    "Matemática",
    "Pedagogia",
    "Psicologia",
    "Química",
    "Relações Internacionais",
    "Serviço Social",
    "Sistemas de Informação",
    "Teologia",
]


def popular(apps, schema_editor):
    Curso = apps.get_model("prismaapp", "Curso")
    for nome in CURSOS_PUC_RIO:
        Curso.objects.get_or_create(nome=nome)


def despopular(apps, schema_editor):
    Curso = apps.get_model("prismaapp", "Curso")
    Curso.objects.filter(nome__in=CURSOS_PUC_RIO).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("prismaapp", "0017_curso"),
    ]

    operations = [
        migrations.RunPython(popular, despopular),
    ]
