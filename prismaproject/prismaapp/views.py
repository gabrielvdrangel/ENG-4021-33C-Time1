from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.shortcuts import render
from django.core.mail import send_mail
from django.utils import timezone


from .models import Oportunidade, Usuario, Feedback


def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        senha = request.POST.get("password", "")
        usuario = Usuario.objects.filter(email__iexact=email).first() if email else None
        user = authenticate(request, username=usuario.username, password=senha) if usuario else None

        if user is not None:
            login(request, user)
            return redirect("homepage")
        return render(request, "tela_login.html", {"erro": "E-mail ou senha inválidos."})
    return render(request, "tela_login.html")


def logout_user(request):
    logout(request)
    return redirect("login")


@login_required
def prazos(request):
    oportunidades = (
        request.user.candidaturas
        .filter(limite_inscricao__gte=timezone.now())
        .select_related("usuario")
        .order_by("limite_inscricao")
    )

    tipo = request.GET.get("tipo")
    if tipo in dict(Oportunidade.TIPO_CHOICES):
        oportunidades = oportunidades.filter(tipo=tipo)

    return render(request, "tela_prazos.html", context={
        "oportunidades": oportunidades,
        "tipos": Oportunidade.TIPO_CHOICES,
        "tipo_atual": tipo,
    })



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
    usuarios = Usuario.objects.filter(curso__isnull=True, is_superuser=False, is_staff=False)

    if request.GET.get("seguindo"):
        oportunidades = oportunidades.filter(usuario__in=request.user.seguindo.all())

    return render(request, "tela_homepage.html", context={"oportunidades": oportunidades, "usuarios": usuarios})


@login_required
def candidaturas(request, username):
    usuario = Usuario.objects.filter(username=username).first()
    oportunidade = Oportunidade.objects.filter(candidatos=usuario)
    return render(request, "tela_candidaturas.html", context={"oportunidades": oportunidade})


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
        elif Usuario.objects.filter(email=email).exists() or Usuario.objects.filter(username=nome).exists():
            erro = "Este email ou nome de usuário já está em uso."
        else:
            Usuario.objects.create_user(
                username=nome,
                email=email,
                password=senha,
                first_name=nome,
            )
            return redirect("login")

    return render(request, "cadastro-organizacao.html", {"erro": erro})


@login_required
def tela_perfil_org(request, username):
    org = Usuario.objects.filter(username=username).first()
    oportunidades=Oportunidade.objects.filter(usuario=org).all()
    return render(request, 'tela_perfil_org.html',context={"org": org, "oportunidades": oportunidades})
    
def esqueci_senha(request):
    mensagem = None
    
    if request.method == "POST":
        email = request.POST["email"]

        if Usuario.objects.filter(email=email).exists():
            send_mail(
                subject="Prisma - Redefinição de senha",
                message="Olá!, Recebemos um pedido para redefinir a senha da sua conta no Prisma.",
                from_email=None,
                recipient_list=[email],
            )
            mensagem = "Foi enviado um email para a conta."
        else:
            mensagem = "Conta inexistente."
    return render(request, "esqueci-senha.html", {"mensagem": mensagem})

def redefinir_email(request):
    mensagem = None

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        novo_email = request.POST.get("novo_email", "").strip()
        senha = request.POST.get("senha", "")

        user = authenticate(request, username=username, password=senha)

        if user is None:
            mensagem = "Usuário ou senha inválidos."
        elif Usuario.objects.filter(email__iexact=novo_email).exists():
            mensagem = "Este email já está em uso."
        else:
            user.email = novo_email
            user.save()
            mensagem = "Email atualizado com sucesso."

    return render(request, "tela_redefinir_email.html", {"mensagem": mensagem})

@login_required
def editar_perfil(request):
    user = request.user
    if request.method == "POST":
        user.first_name = request.POST.get("nome", user.first_name)
        user.curso = request.POST.get("curso") or None
        user.periodo = request.POST.get("periodo") or None
        imagem = request.FILES.get("imagem")
        if imagem:
            user.imagem = imagem
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
            username=nome,
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
            tipo=request.POST["tipo"],
            descricao=request.POST["descricao"],
            limite_inscricao=request.POST["limite_inscricao"],
            imagem=request.FILES.get("imagem") or None,
        )
        return redirect("homepage")
    return render(request, "tela_add-publicacao.html")


@login_required
def feedbacks_perfil(request):
    feedbacks = request.user.feedbacks_enviados.select_related("destinatario", "oportunidade").order_by("-data")
    return render(request, 'feedbacks_perfil.html', {'feedbacks': feedbacks})


@login_required
def deixar_feedback(request, username):
    org = get_object_or_404(Usuario, username=username)

    if org == request.user:
        return redirect("tela_feedbacks", username=username)

    if request.method == "POST":
        comentario = request.POST.get("comentario", "").strip()
        if comentario:
            Feedback.objects.create(
                autor=request.user,
                destinatario=org,
                comentario=comentario,
            )
            return redirect("tela_feedbacks", username=username)
        return render(request, "tela_deixar_feedback.html", {
            "org": org,
            "erro": "Escreva um comentário antes de enviar.",
        })

    return render(request, "tela_deixar_feedback.html", {"org": org})


@login_required
def tela_feedbacks(request,username):
    org = get_object_or_404(Usuario, username=username)
    feedbacks = org.feedbacks_recebidos.select_related("autor").order_by("-data")
    return render(request, "tela_feedback.html", {"feedbacks": feedbacks,"username": username, "org": org})


@login_required
def perfil_aluno(request, username):
    aluno = Usuario.objects.filter(username=username).first()
    return render(request, "perfil_aluno.html", {"aluno": aluno})


@login_required
def alternar_seguir(request, username):
    alvo = Usuario.objects.filter(username=username).first()

    if request.method == "POST" and alvo and alvo != request.user:
        if alvo in request.user.seguindo.all():
            request.user.seguindo.remove(alvo)
        else:
            request.user.seguindo.add(alvo)

    return redirect("tela_perfil_org", username=username)


@login_required
def alternar_salvo(request, code):
    alvo = Oportunidade.objects.filter(code=code).first()

    if request.method == "POST" and alvo and alvo.usuario != request.user:
        if alvo in request.user.salvos.all():
            request.user.salvos.remove(alvo)
        else:
            request.user.salvos.add(alvo)

    return redirect("homepage")


@login_required
def alternar_candidatura(request, code):
    post = Oportunidade.objects.filter(code=code).first()
    if request.method == "POST":
        if request.user in post.candidatos.all():
            post.candidatos.remove(request.user)
        else:
            post.candidatos.add(request.user)
    return redirect('homepage') 


def remover_publicacao(request, code):
    post = Oportunidade.objects.filter(code=code).first()
    if request.method == "POST":
        post.delete()
    return redirect('homepage')
