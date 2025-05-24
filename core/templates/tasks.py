"""import datetime
from django.core.mail import send_mail
from django.conf import settings
from .models import Doacao


def enviar_relatorio_mensal():
    hoje = datetime.date.today()
    primeiro_dia = hoje.replace(day=1)
    doacoes = Doacao.objects.filter(data__date__gte=primeiro_dia, data__date__lte=hoje)
    total = sum(d.valor for d in doacoes)

    texto = f'Relatório de {primeiro_dia} a {hoje}:\n\n'
    for d in doacoes:
        texto += f"Data: {d.data}, Valor: R${d.valor}, CPF: {d.cpf}\n"
    texto += f"\nTotal arrecadado: R$ {total}"

    send_mail(
        'Relatório de Doações - Mensal',
        texto,
        settings.DEFAULT_FROM_EMAIL,
        ['seu@email.com'],
        fail_silently=False,
    )
"""