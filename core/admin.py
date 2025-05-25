from django.contrib import admin
from .models import Documento, Doacao, Noticia


@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('titulo',)


@admin.register(Doacao)
class DoacaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'cpf', 'valor', 'data_transacao')
    search_fields = ('nome', 'cpf')


@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_publicacao')
    search_fields = ('titulo',)
