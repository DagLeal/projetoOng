from django.contrib import admin
from django.utils.html import format_html
from .models import Documento, Parceiro, Projeto, MediaProjeto, Doacoes


@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'preview', 'arquivo')
    readonly_fields = ('preview',)
    search_fields = ('titulo',)

    def preview(self, obj):
        if obj.arquivo:
            if obj.tipo == 'imagem':
                return format_html('<img src="{}" style="max-height: 200px;"/>', obj.arquivo.url)
            elif obj.tipo == 'pdf':
                return format_html('<a href="{}" target="_blank">📄 Visualizar PDF</a>', obj.arquivo.url)
            elif obj.tipo == 'planilha':
                return format_html('<a href="{}" target="_blank">📊 Baixar Planilha</a>', obj.arquivo.url)
            elif obj.tipo == 'word':
                return format_html('<a href="{}" target="_blank">📝 Baixar Documento Word</a>', obj.arquivo.url)
            else:
                return format_html('<a href="{}" target="_blank">📁 Baixar Arquivo</a>', obj.arquivo.url)
        return "Nenhum arquivo enviado"


@admin.register(Parceiro)
class ParceiroAdmin(admin.ModelAdmin):
    list_display = ('nome', 'link')

class MediaProjetoInline(admin.TabularInline):
    model = MediaProjeto
    extra = 1
    fields = ('media_type', 'arquivo', 'thumbnail', 'titulo')

class ProjetoAdmin(admin.ModelAdmin):
    inlines = [MediaProjetoInline]

admin.site.register(Projeto, ProjetoAdmin)


@admin.register(Doacoes)
class DoacoesAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'cpf', 'valor', 'data_hora')
    readonly_fields = ('nome', 'email', 'cpf', 'valor', 'data_hora')
    can_add = False
    can_delete = False

    def has_add_permission(self, request):
        return False  # impede adicionar no admin

    def has_change_permission(self, request, obj=None):
        return False  # impede editar

    def has_delete_permission(self, request, obj=None):
        return False  # impede deletar
