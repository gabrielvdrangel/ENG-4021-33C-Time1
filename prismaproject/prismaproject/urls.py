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
from prismaapp import views
from prismaapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('prazos/', prazos, name='prazos'),
    path('notificacoes/', notificacoes, name='notificacoes'),
    path('salvos/', salvos, name='salvos'),
    path('realizados/', realizados, name='realizados'),
    path('perfil/', perfil, name='perfil'),
    path("homepage/", views.homepage, name="homepage"),
    path('candidaturas/', candidaturas, name='candidaturas'),
    path('chat/', chat, name='chat'),
    path('conversas/', conversas, name='conversas'),
    path('', entrar_cadastrar, name='entrar_cadastrar'),
    path('escolhe-cadastro/', escolhe_cadastro, name='escolhe_cadastro'),
    path('cadastro-organizacao/', cadastro_organizacao, name='cadastro_organizacao'),
    path('tela_perfil_org/<str:username>/', tela_perfil_org, name='tela_perfil_org'),
    path('esqueci-senha/', esqueci_senha, name='esqueci_senha'),
    path('perfil/editar/', editar_perfil, name='editar_perfil'),
    path('cadastro-aluno/', cadastro_aluno, name='cadastro_aluno'),
    path('add-publicacao/', add_publicacao, name='add_publicacao'),
    path('feedbacks-perfil/', views.feedbacks_perfil, name='feedbacks_perfil'),
    path("login/", views.login_user, name="login"),
    path('logout/', logout_user, name='logout'),
    path("redefinir-email/", views.redefinir_email, name="redefinir_email"),
    path("feedbacks/<str:username>/", views.tela_feedbacks, name="tela_feedbacks"),
    path("perfil-aluno/", views.perfil_aluno, name="perfil_aluno"),
    path('seguir/<str:username>/', alternar_seguir, name='alternar_seguir'),
    path('oportunidade/<uuid:code>/salvar/', views.alternar_salvo, name='alternar_salvo'),
]

