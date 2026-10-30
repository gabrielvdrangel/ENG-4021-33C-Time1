from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import Oportunidade, Usuario


def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        senha = request.POST.get("password", "")
        usuario = Usuario.objects.filter(email__iexact=email).first() if email else None
        user = authenticate(request, username=usuario.username, password=senha) if usuario else None

        if user is not None:
            login(request, user)
            return redirect("homepage_org" if user.matricula is None else "homepage")
        return render(request, "tela_login.html", {"erro": "E-mail ou senha inválidos."})
    return render(request, "tela_login.html")


def logout_user(request):
    logout(request)
    return redirect("login")


@login_required
def prazos(request):
    return render(request, "tela_prazos.html")


@login_required
def notificacoes(request):
    return render(request, "tela_notificacoes.html")


@login_required
def salvos(request):
    return render(request, "tela_salvos.html")


@login_required
def realizados(request):
    return render(request, "tela_realizados.html")


@login_required
def perfil(request):
    return render(request, "perfil.html", context={"usuario": request.user})


@login_required
def homepage(request):
    oportunidades = Oportunidade.objects.select_related("usuario")
    return render(request, "tela_homepage.html", context={"oportunidades": oportunidades})


@login_required
def homepage_org(request):
    oportunidades = Oportunidade.objects.all()
    return render(request, "tela_homepage-org.html", context={"oportunidades": oportunidades})


@login_required
def candidaturas(request):
    return render(request, "tela_candidaturas.html")


@login_required
def chat(request):
    return render(request, "tela_chat.html")


@login_required
def conversas(request):
    return render(request, "tela_conversas.html")


def entrar_cadastrar(request):
    return render(request, "entrar-cadastrar.html")


def escolhe_cadastro(request):
    return render(request, "escolhe-cadastro.html")


def cadastro_organizacao(request):
    erro = None
    if request.method == "POST":
        nome = request.POST.get("nome", "")
        email = request.POST.get("email", "")
        senha = request.POST.get("senha", "")

        if not nome or not email or not senha:
            erro = "Todos os campos são obrigatórios."
        elif Usuario.objects.filter(email=email).exists():
            erro = "Este email já está em uso."
        else:
            Usuario.objects.create_user(
                username=email,
                email=email,
                password=senha,
                first_name=nome,
            )
            return redirect("login")

    return render(request, "cadastro-organizacao.html", {"erro": erro})


@login_required
def tela_perfil_org(request):
    oportunidades=Oportunidade.objects.all()
    return render(request, 'tela_perfil_org.html',context={"oportunidades": oportunidades})
    
def esqueci_senha(request):
    mensagem = None
    if request.method == "POST":
        if Usuario.objects.filter(email=request.POST["email"]).exists():
            mensagem = "Foi enviado um email para a conta."
        else:
            mensagem = "Conta inexistente."
    return render(request, "esqueci-senha.html", {"mensagem": mensagem})


@login_required
def editar_perfil(request):
    user = request.user
    if request.method == "POST":
        user.first_name = request.POST["nome"]
        user.curso = request.POST["curso"] or None
        user.periodo = request.POST["periodo"] or None
        user.imagem_url = request.POST["imagem_url"] or None
        user.save()
        return redirect("perfil")
    return render(request, "editar-perfil.html", {"usuario": user})


def cadastro_aluno(request):
    if request.method == "POST":
        nome = request.POST["nome"]
        matricula = request.POST["login"]
        senha = request.POST["senha"]
        email = request.POST["email"]
        curso = request.POST["curso"]
        periodo = request.POST["periodo"]

        if not matricula.isdigit():
            return render(request, "cadastro-aluno.html", {"erro": "Matrícula deve conter apenas números."})

        if Usuario.objects.filter(matricula=int(matricula)).exists():
            return render(request, "cadastro-aluno.html", {"erro": "Matrícula já cadastrada."})

        if Usuario.objects.filter(email=email).exists():
            return render(request, "cadastro-aluno.html", {"erro": "Email já cadastrado."})

        Usuario.objects.create_user(
            username=matricula,
            password=senha,
            email=email,
            first_name=nome,
            matricula=int(matricula),
            curso=curso,
            periodo=periodo,
        )
        return redirect("login")

    return render(request, "cadastro-aluno.html")


@login_required
def add_publicacao(request):
    if request.method == "POST":
        Oportunidade.objects.create(
            usuario=request.user,
            nome=request.POST["Nome"],
            tipo=request.POST["Tipo"],
            descricao=request.POST["descricao"],
            limite_inscricao=request.POST["limite_inscricao"],
            imagem_url=request.POST.get("imagem_url") or None,
        )
        return redirect("homepage_org")
    return render(request, "tela_add-publicacao.html")