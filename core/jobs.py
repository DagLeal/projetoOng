# core/jobs.py
from .models import Doacao
from django.utils.timezone import now
from django.core.mail import send_mail
from datetime import timedelta
import csv
import io

def gerar_relatorio_mensal():
    hoje = now()
    inicio_mes = hoje.replace(day=1)
    mes_passado = inicio_mes - timedelta(days=1)

    doacoes = Doacao.objects.filter(data__month=mes_passado.month, data__year=mes_passado.year)
    total = sum(d.valor for d in doacoes)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['CPF', 'Valor', 'Data'])
    for d in doacoes:
        writer.writerow([d.cpf, f'{d.valor}', d.data.strftime('%d/%m/%Y')])
    writer.writerow(['TOTAL', f'{total}', ''])

    send_mail(
        subject=f'Relatório de Doações - {mes_passado.strftime("%m/%Y")}',
        message='Veja o relatório abaixo.',
        from_email='seu@email.com',
        recipient_list=['destino@email.com'],
        fail_silently=False,
        html_message=output.getvalue()
    )