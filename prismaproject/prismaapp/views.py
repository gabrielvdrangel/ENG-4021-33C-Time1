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

