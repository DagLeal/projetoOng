from django.contrib import admin
from .models import Doacao
from django.http import HttpResponse
import csv

# Register your models here.

@admin.register(Doacao)
class DoacaoAdmin(admin.ModelAdmin):
    list_display = ['cpf', 'valor', 'data']
    actions = ['exportar_csv']

    def exportar_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="doacoes.csv"'

        writer = csv.writer(response)
        writer.writerow(['CPF', 'Valor', 'Data'])

        for d in queryset:
            writer.writerow([d.cpf, d.valor, d.data.strftime('%d/%m/%Y')])

        return response

    exportar_csv.short_description = "Exportar CSV das doações selecionadas"
