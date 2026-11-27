from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import request
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme, urlencode
from django.shortcuts import redirect, render, get_object_or_404
from django.core.mail import send_mail
from django.utils import timezone
from datetime import date, timedelta
from django.db.models import Q
from .models import Curso, Experiencia, Oportunidade, Usuario, Feedback, Mensagem,Comentario, Notificacao


def _url_segura(request, url):
    if url and url_has_allowed_host_and_scheme(url, allowed_hosts={request.get_host()}):
        return url
    return None


def _voltar_para_origem(request, padrao="homepage"):
    """Redireciona para a página de onde o usuário veio (ex.: perfil da organização)."""
    return redirect(_url_segura(request, request.META.get("HTTP_REFERER")) or padrao)


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
    agora = timezone.now()

    for op in request.user.candidaturas.filter(
        limite_inscricao__gte=agora,
        limite_inscricao__lte=agora + timedelta(hours=48),
    ).select_related("usuario"):
        Notificacao.objects.get_or_create(
            destinatario=request.user,
            tipo="prazo",
            oportunidade=op,
            defaults={
                "origem": op.usuario,
                "texto": f"O prazo de {op.get_tipo_display()} termina em "
                         f"{op.limite_inscricao.strftime('%d/%m às %H:%M')}",
            },
        )

    lista = request.user.notificacoes.select_related("origem", "oportunidade")
    novas = set(lista.filter(lida=False).values_list("id", flat=True))
    lista.filter(lida=False).update(lida=True)

    tipo = request.GET.get("tipo", "")
    q = request.GET.get("q", "").strip()
    if tipo in dict(Notificacao.TIPO_CHOICES):
            lista = lista.filter(tipo=tipo)
    if q:
        lista = lista.filter(
            Q(texto__icontains=q)
            | Q(origem__first_name__icontains=q)
            | Q(origem__username__icontains=q)
        )

    return render(request, "tela_notificacoes.html", {
        "notificacoes": lista,
        "novas": novas,
        "tipos": Notificacao.TIPO_CHOICES,
        "tipo_atual": tipo,
        "q": q,
    })


@login_required
def abrir_notificacao(request, id):
    """Ao clicar numa notificação de seguidor, ela é removida e o usuário vai ao perfil."""
    n = get_object_or_404(Notificacao, id=id, destinatario=request.user)
    destino = n.destino
    if n.tipo == "seguidor":
        n.delete()
    return redirect(destino if destino != "#" else "notificacoes")


@login_required
def salvos(request):
    return render(request, "tela_salvos.html")


@login_required
def realizados(request):
    oportunidades = (
        request.user.candidaturas
        .filter(limite_inscricao__lt=timezone.now())
        .select_related("usuario")
        .order_by("-limite_inscricao")
    )
    return render(request, "tela_realizados.html", context={"oportunidades": oportunidades})



@login_required
def perfil(request):
    return render(request, "perfil.html", context={"usuario": request.user})


@login_required
def homepage(request):
    oportunidades = Oportunidade.objects.select_related("usuario").prefetch_related("comentarios__autor")
    usuarios = Usuario.objects.filter(curso__isnull=True, is_superuser=False, is_staff=False)

    if request.GET.get("seguindo"):
        oportunidades = oportunidades.filter(usuario__in=request.user.seguindo.all())

    return render(request, "tela_homepage.html", context={
        "oportunidades": oportunidades,
        "usuarios": usuarios,
        "today": timezone.now(),
    })


@login_required
def candidaturas(request):
    oportunidades = request.user.candidaturas.select_related("usuario").order_by("limite_inscricao")
    return render(request, "tela_candidaturas.html", context={"oportunidades": oportunidades})


@login_required
def chat(request, username):
    outro = get_object_or_404(Usuario, username=username)
    if outro == request.user:
        return redirect("conversas")

    # Ao abrir a conversa, remove as notificações de mensagem desse remetente
    Notificacao.objects.filter(
        destinatario=request.user, origem=outro, tipo="mensagem"
    ).delete()
    Mensagem.objects.filter(
        remetente=outro, destinatario=request.user, lida=False
    ).update(lida=True)

    if request.method == "POST":
        texto = request.POST.get("texto", "").strip()
        if texto:
            Mensagem.objects.create(remetente=request.user, destinatario=outro, texto=texto)
            nome = request.user.get_full_name() or request.user.username
            # Um único card por remetente: atualiza o existente em vez de criar outro
            Notificacao.objects.update_or_create(
                destinatario=outro, origem=request.user, tipo="mensagem",
                defaults={
                    "texto": f"{nome} enviou uma mensagem: {texto[:60]}",
                    "data": timezone.now(),
                    "lida": False,
                },
            )

        return redirect("chat", username=outro.username)

    mensagens = (
        Mensagem.objects
        .filter(Q(remetente=request.user, destinatario=outro)
                | Q(remetente=outro, destinatario=request.user))
        .select_related("remetente")
        .order_by("id")
    )

    return render(request, "tela_chat.html", {"outro": outro, "mensagens": mensagens})


@login_required
def conversas(request):
    msgs = (
        Mensagem.objects
        .filter(Q(remetente=request.user) | Q(destinatario=request.user))
        .select_related("remetente", "destinatario")
        .order_by("-data")
    )

    vistos = {}
    for m in msgs:  # da mais recente para a mais antiga
        outro = m.destinatario if m.remetente == request.user else m.remetente
        if outro.pk not in vistos:
            vistos[outro.pk] = {"usuario": outro, "ultima": m}

    seguindo = request.user.seguindo.filter(is_active=True).order_by("first_name", "username")

    return render(request, "tela_conversas.html", {
        "conversas": vistos.values(),
        "seguindo": seguindo,
        "oportunidades": request.user.oportunidades.order_by("-data_publicacao"),
    })


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
        elif "/" in nome:
            erro = "O nome da organização não pode conter \"/\"."
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
    org = get_object_or_404(Usuario, username=username)
    oportunidades = Oportunidade.objects.filter(usuario=org)
    return render(request, 'tela_perfil_org.html',context={"org": org, "oportunidades": oportunidades})
    
def esqueci_senha(request):
    mensagem = None

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        senha = request.POST.get("senha", "")
        nova_senha = request.POST.get("nova_senha", "")

        usuario = Usuario.objects.filter(email__iexact=email).first()
        user = authenticate(request, username=usuario.username, password=senha) if usuario else None

        if user is None:
            mensagem = "Usuário ou senha inválidos."
        elif not nova_senha:
            mensagem = "A nova senha não pode ser vazia."
        else:
            user.set_password(nova_senha)
            user.save()
            mensagem = "Senha atualizada com sucesso."

    return render(request, "esqueci-senha.html", {"mensagem": mensagem})  

def redefinir_email(request):
    mensagem = None

    if request.method == "POST":
        email_atual = request.POST.get("email_atual", "").strip()
        novo_email = request.POST.get("novo_email", "").strip()
        senha = request.POST.get("senha", "")

        usuario = Usuario.objects.filter(email__iexact=email_atual).first() if email_atual else None
        user = authenticate(request, username=usuario.username, password=senha) if usuario else None

        if user is None:
            mensagem = "E-mail ou senha inválidos."
        elif not novo_email:
            mensagem = "Informe o novo e-mail."
        elif Usuario.objects.filter(email__iexact=novo_email).exclude(pk=user.pk).exists():
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
        curso = (request.POST.get("curso") or "").strip() or None
        # Aluno não pode ficar sem curso (senão passa a ser tratado como organização).
        if user.matricula is not None and not curso:
            return render(request, "editar-perfil.html", {
                "usuario": user,
                "cursos": Curso.objects.all(),
                "erro": "Selecione um curso da lista.",
            })
        # Aceita o curso atual (contas antigas com texto livre) ou um curso da lista.
        if curso and curso != user.curso and not Curso.objects.filter(nome=curso).exists():
            return render(request, "editar-perfil.html", {
                "usuario": user,
                "cursos": Curso.objects.all(),
                "erro": "Selecione um curso da lista.",
            })
        user.first_name = request.POST.get("nome", user.first_name)
        user.curso = curso
        user.periodo = request.POST.get("periodo") or None
        imagem = request.FILES.get("imagem")
        if imagem:
            user.imagem = imagem
        user.save()
        return redirect("perfil")
    return render(request, "editar-perfil.html", {"usuario": user, "cursos": Curso.objects.all()})


def cadastro_aluno(request):
    cursos = Curso.objects.all()
    if request.method == "POST":
        nome = request.POST["nome"]
        matricula = request.POST["login"]
        senha = request.POST["senha"]
        email = request.POST["email"]
        curso = request.POST["curso"].strip()
        periodo = request.POST["periodo"]

        def erro(msg):
            return render(request, "cadastro-aluno.html", {"erro": msg, "cursos": cursos})

        if not matricula.isdigit():
            return erro("Matrícula deve conter apenas números.")

        if Usuario.objects.filter(matricula=int(matricula)).exists():
            return erro("Matrícula já cadastrada.")

        if Usuario.objects.filter(email=email).exists():
            return erro("Email já cadastrado.")

        if not cursos.filter(nome=curso).exists():
            return erro("Selecione um curso da lista.")

        # A matrícula é única e segura para URLs; o nome fica em first_name.
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

    return render(request, "cadastro-aluno.html", {"cursos": cursos})


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
def feedbacks_perfil(request, username=None):
    if username:
        dono = get_object_or_404(Usuario, username=username)
    else:
        dono = request.user

    feedbacks = dono.feedbacks_enviados.select_related("destinatario", "oportunidade").order_by("-data")
    return render(request, 'feedbacks_perfil.html', {
        'feedbacks': feedbacks,
        'dono': dono,
        'eh_proprio': dono == request.user,
    })



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
    aluno = get_object_or_404(Usuario, username=username)

    voltar_url = request.META.get("HTTP_REFERER", "")
    if not url_has_allowed_host_and_scheme(voltar_url, allowed_hosts={request.get_host()}):
        voltar_url = reverse("perfil")

    if voltar_url.rstrip("/").endswith(request.path.rstrip("/")):
        voltar_url = reverse("perfil")


    return render(request, "perfil_aluno.html", {
        "aluno": aluno,
        "total_seguidores": aluno.seguidores.count(),
        "total_seguindo": aluno.seguindo.count(),
        "eh_proprio_perfil": aluno == request.user,
        "ja_segue": request.user.seguindo.filter(pk=aluno.pk).exists(),
        "voltar_url": voltar_url,
    })


@login_required
def criar_experiencia(request):
    if request.method != "POST":
        return redirect("perfil_aluno", username=request.user.username)

    titulo = request.POST.get("titulo", "").strip()
    organizacao = request.POST.get("organizacao", "").strip()
    descricao = request.POST.get("descricao", "").strip()
    try:
        data_inicio = date.fromisoformat(request.POST.get("data_inicio", ""))
        data_fim_texto = request.POST.get("data_fim", "")
        data_fim = date.fromisoformat(data_fim_texto) if data_fim_texto else None
    except ValueError:
        data_inicio = data_fim = None

    if not titulo or not organizacao or not data_inicio:
        messages.error(request, "Preencha cargo, organização e data de início.")
    elif data_fim and data_fim < data_inicio:
        messages.error(request, "A data de término não pode ser antes da data de início.")
    else:
        Experiencia.objects.create(
            usuario=request.user,
            titulo=titulo,
            organizacao=organizacao,
            data_inicio=data_inicio,
            data_fim=data_fim,
            descricao=descricao,
            imagem=request.FILES.get("imagem"),
        )
        messages.success(request, "Experiência adicionada.")

    return redirect("perfil_aluno", username=request.user.username)


@login_required
def remover_experiencia(request, id):
    if request.method == "POST":
        experiencia = get_object_or_404(Experiencia, id=id, usuario=request.user)
        experiencia.delete()
        messages.success(request, "Experiência removida.")
    return redirect("perfil_aluno", username=request.user.username)


@login_required
def alternar_seguir(request, username):
    alvo = Usuario.objects.filter(username=username).first()

    if request.method == "POST" and alvo and alvo != request.user:
        if alvo in request.user.seguindo.all():
            request.user.seguindo.remove(alvo)
        else:
            request.user.seguindo.add(alvo)
            nome = request.user.get_full_name() or request.user.username
            Notificacao.objects.get_or_create(
                destinatario=alvo, origem=request.user, tipo="seguidor", lida=False,
                defaults={"texto": f"{nome} começou a seguir você"},
            )

    if alvo and alvo.curso is not None:
        return redirect("perfil_aluno", username=username)
    return redirect("tela_perfil_org", username=username)


@login_required
def alternar_salvo(request, code):
    alvo = Oportunidade.objects.filter(code=code).first()

    if request.method == "POST" and alvo and alvo.usuario != request.user:
        if alvo in request.user.salvos.all():
            request.user.salvos.remove(alvo)
        else:
            request.user.salvos.add(alvo)

    return _voltar_para_origem(request)


@login_required
def alternar_candidatura(request, code):
    post = get_object_or_404(Oportunidade, code=code)
    eh_aluno = request.user.matricula is not None
    if request.method == "POST" and eh_aluno:
        if post.candidatos.filter(pk=request.user.pk).exists():
            post.candidatos.remove(request.user)
        elif post.limite_inscricao >= timezone.now():
            post.candidatos.add(request.user)
    return _voltar_para_origem(request)


@login_required
def remover_publicacao(request, code):
    post = get_object_or_404(Oportunidade, code=code, usuario=request.user)
    if request.method == "POST":
        post.delete()
    return _voltar_para_origem(request)


@login_required
def candidatos(request, code):
    # Só o dono da publicação vê quem se candidatou
    post = get_object_or_404(Oportunidade, code=code, usuario=request.user)
    lista = post.candidatos.order_by("first_name", "username")
    return render(request, "tela_candidatos.html", {"post": post, "candidatos": lista})

@login_required
def tela_editar_publicacao(request, code):
    publicacao = get_object_or_404(Oportunidade, code=code, usuario=request.user)

    if request.method == "POST":
        publicacao.tipo = request.POST["tipo"]
        publicacao.descricao = request.POST["descricao"]
        publicacao.limite_inscricao = request.POST["limite_inscricao"]
        if request.FILES.get("imagem"):
            publicacao.imagem = request.FILES["imagem"]
        publicacao.save()
        return redirect("tela_perfil_org", username=request.user.username)

    return render(request, "tela_editar_publicacao.html", {
        "publicacao": publicacao,
        "tipos": Oportunidade.TIPO_CHOICES,
    })

@login_required
def tela_comentarios(request, code):
    post = get_object_or_404(Oportunidade.objects.select_related("usuario"), code=code)
    comentarios = post.comentarios.select_related("autor").order_by("-data")

    voltar_url = _url_segura(request, request.GET.get("next"))
    if not voltar_url:
        referer = _url_segura(request, request.META.get("HTTP_REFERER"))
        if referer and request.path not in referer:
            voltar_url = referer
    voltar_url = voltar_url or reverse("homepage")

    return render(request, "tela_comentarios.html", {
        "post": post,
        "comentarios": comentarios,
        "voltar_url": voltar_url,
    })


def _redirect_comentarios(request, code):
    url = reverse("tela_comentarios", kwargs={"code": code})
    proximo = _url_segura(request, request.POST.get("next"))
    if proximo:
        url += "?" + urlencode({"next": proximo})
    return redirect(url)


@login_required
def comentar(request, code):
    post = get_object_or_404(Oportunidade, code=code)

    if request.method == "POST":
        texto = request.POST.get("texto", "").strip()
        if texto:
            Comentario.objects.create(oportunidade=post, autor=request.user, texto=texto)
    return _redirect_comentarios(request, code)


@login_required
def remover_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    code = comentario.oportunidade.code

    pode_apagar = request.user in (comentario.autor, comentario.oportunidade.usuario)
    if request.method == "POST" and pode_apagar:
        comentario.delete()
    return _redirect_comentarios(request, code)

@login_required
def enviar_aviso(request):
    if request.method == "POST" and request.user.curso is None:
        oportunidade_id = request.POST.get("oportunidade", "")
        texto = request.POST.get("texto", "").strip()

        post = None
        if oportunidade_id.isdigit():
            post = Oportunidade.objects.filter(id=int(oportunidade_id), usuario=request.user).first()

        if post is None:
            messages.error(request, "Selecione uma das suas oportunidades.")
        elif not texto:
            messages.error(request, "Escreva o aviso antes de enviar.")
        else:
            enviados = 0
            for aluno in post.candidatos.all():
                Mensagem.objects.create(
                    remetente=request.user,
                    destinatario=aluno,
                    texto=f"[Aviso - {post.get_tipo_display()}] {texto}",
                )
                enviados += 1
            messages.success(request, f"Aviso enviado para {enviados} candidato(s).")

    return redirect("conversas")






