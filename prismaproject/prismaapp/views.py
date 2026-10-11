from django.shortcuts import render

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
    return render(request, 'perfil.html')

def homepage(request):
    return render(request, 'tela_homepage.html')

def candidaturas(request):
    return render(request, 'tela_candidaturas.html')

def chat(request):
    return render(request, 'tela_chat.html')

def conversas(request):
    return render(request, 'tela_conversas.html')

