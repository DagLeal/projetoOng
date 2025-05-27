from django.contrib import admin
from django.utils.html import format_html
from .models import Documento, Doacao, Noticia, Parceiro, Projeto, ImagemProjeto


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
            else:
                return format_html('<a href="{}" target="_blank">📁 Baixar Arquivo</a>', obj.arquivo.url)
        return "Nenhum arquivo enviado"

    preview.short_description = "Pré-visualização"

@admin.register(Doacao)
class DoacaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'cpf', 'valor', 'data_hora')



@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_publicacao')
    search_fields = ('titulo',)

@admin.register(Parceiro)
class ParceiroAdmin(admin.ModelAdmin):
    list_display = ('nome', 'link')

class ImagemProjetoInline(admin.TabularInline):
    model = ImagemProjeto
    extra = 1

class ProjetoAdmin(admin.ModelAdmin):
    inlines = [ImagemProjetoInline]

admin.site.register(Projeto, ProjetoAdmin)
