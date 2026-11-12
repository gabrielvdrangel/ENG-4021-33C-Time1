from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Curso, Experiencia, Oportunidade, Usuario

admin.site.register(Usuario, UserAdmin)
admin.site.register(Oportunidade)


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    search_fields = ["nome"]


@admin.register(Experiencia)
class ExperienciaAdmin(admin.ModelAdmin):
    list_display = ["usuario", "titulo", "organizacao", "data_inicio", "data_fim"]
    search_fields = ["usuario__username", "titulo", "organizacao"]
