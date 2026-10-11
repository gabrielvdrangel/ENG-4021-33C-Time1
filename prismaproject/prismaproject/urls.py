"""
URL configuration for prismaproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from prismaapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('prazos/', prazos, name='prazos'),
    path('notificacoes/', notificacoes, name='notificacoes'),
    path('login/', login, name='login'),
    path('', salvos, name='salvos'),
    path('realizados/', realizados, name='realizados'),
    path('perfil/', perfil, name='perfil'),
    path('homepage/', homepage, name='homepage'),
    path('candidaturas/', candidaturas, name='candidaturas'),
    path('chat/', chat, name='chat'),
    path('conversas/', conversas, name='conversas'),
    path('', views.entrar_cadastrar, name='entrar_cadastrar'),
    path('cadastro/', views.escolhe_cadastro, name='escolhe_cadastro'),
    path('cadastro/organizacao/', views.cadastro_organizacao, name='cadastro_organizacao'),
    path('esqueci-senha/', views.esqueci_senha, name='esqueci_senha'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
]

urlpatterns=[
    path('cadastro/',cadastro), name='cadastro'),
    path('cadastro/aluno/',cadastro), cadastro_aluno='cadastro_aluno'),
    path('cadastro/organizacao/',cadastro_organizacao), name='cadastro_organizacao'),
]
