from django.shortcuts import render, redirect
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
    return render(request, 'cadastro-organizacao.html')

def esqueci_senha(request):
    return render(request, 'esqueci-senha.html')

def editar_perfil(request):
    return render(request, 'editar-perfil.html')

def cadastro_aluno(request):
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

