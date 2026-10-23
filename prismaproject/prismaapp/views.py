from django.shortcuts import render, redirect
from django.shortcuts import redirect, render
from .models import usuario, oportunidade

def prazos(request):
    return render(request, 'tela_prazos.html')

def notificacoes(request):
    return render(request, 'tela_notificacoes.html')

def login(request):
    return render(request, 'tela_login.html')

def salvos(request):
    return render(request, 'tela_salvos.html')

def realizados(request):
    return render(request, 'tela_realizados.html')

def perfil(request):
    user = usuario.objects.first() 
    return render(request, 'perfil.html', context={'usuario': user})

def homepage(request):
    oportunidades = oportunidade.objects.all()
    return render(request, 'tela_homepage.html', context={'oportunidades': oportunidades})

def homepage_org(request):
    oportunidades = oportunidade.objects.all()
    return render(request, 'tela_homepage-org.html', context={'oportunidades': oportunidades})

def candidaturas(request):
    return render(request, 'tela_candidaturas.html')

def chat(request):
    return render(request, 'tela_chat.html')

def conversas(request):
    return render(request, 'tela_conversas.html')

def entrar_cadastrar(request):
    return render(request, 'entrar-cadastrar.html')

def escolhe_cadastro(request):
    return render(request, 'escolhe-cadastro.html')

def cadastro_organizacao(request):
    erro = None
    if request.method == 'POST':
        nome = request.POST.get('nome','')
        email = request.POST.get('email','')
        senha = request.POST.get('senha','')

        if not nome or not email or not senha:
            erro = "Todos os campos são obrigatórios."
        elif usuario.objects.filter(email=email).exists():
            erro = "Este email já está em uso."
        else:
            usuario.objects.create(
                nome=nome,
                email=email,
                senha=senha
                )
            return redirect('homepage_org')
        
    return render(request, 'cadastro-organizacao.html', {'erro': erro})

def perfil_organizacao(request):
    return render(request, 'perfil_organizacao.html')
    
def esqueci_senha(request):
    return render(request, 'esqueci-senha.html')

def editar_perfil(request):
    user = usuario.objects.first()
    if request.method == 'POST':
        user.nome = request.POST['nome']
        user.curso = request.POST['curso']
        user.periodo = request.POST['periodo']
        user.save()
        return redirect('perfil')
    return render(request, 'editar-perfil.html')

def cadastro_aluno(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        login = request.POST['login']
        senha = request.POST['senha']
        email = request.POST['email']
        curso = request.POST['curso']
        periodo = request.POST['periodo']

        if not login.isdigit():
            return render(request, 'cadastro-aluno.html', {'erro': 'Matrícula deve conter apenas números.'})

        if usuario.objects.filter(login=login).exists():
            return render(request, 'cadastro-aluno.html', {'erro': 'Matrícula já cadastrada.'})

        if usuario.objects.filter(email=email).exists():
            return render(request, 'cadastro-aluno.html', {'erro': 'Email já cadastrado.'})

        usuario.objects.create(
            nome=nome,
            login=int(login),
            senha=senha,
            email=email,
            curso=curso,
            periodo=periodo
        )
        return redirect('homepage')

    return render(request,'cadastro-aluno.html')

def add_publicacao(request):
    if request.method == 'POST':
        oportunidade.objects.create(
            Nome=request.POST['Nome'],
            Tipo=request.POST['Tipo'],
            descricao=request.POST['descricao'],
            limite_inscricao=request.POST['limite_inscricao'],
        )
        return redirect('homepage_org')
    return render(request, 'tela_add-publicacao.html')

