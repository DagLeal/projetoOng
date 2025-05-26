import qrcode
from io import BytesIO
from django.http import HttpResponse
from .models import Doacao, Documento, Parceiro, Projeto
from django.core import serializers
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages

def gerar_qr_code_pix(request, doacao_id):
    doacao = Doacao.objects.get(id=doacao_id)

    # Substitua por sua chave PIX e dados reais
    chave_pix = '981107467'
    nome_recebedor = 'Dagner'
    cidade = 'Niterói'
    valor = f'{doacao.valor:.2f}'

    payload = f"""
000201
26580014BR.GOV.BCB.PIX0114{chave_pix}
52040000
5303986
540{len(valor):02}{valor}
5802BR
5914{nome_recebedor[:14]}
6010{cidade[:10]}
62100506abcde
6304
""".strip().replace('\n', '')

    # Gerar imagem do QR Code
    qr = qrcode.make(payload)
    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type='image/png')


# Create your views here.


def home(request):
    return render(request, 'home.html')


def sobre(request):
    return render(request, 'sobre.html')


def historia(request):
    return render(request, 'historia.html')


def presidencia(request):
    return render(request, 'presidencia.html')


def projetos(request):
    return render(request, 'projetos.html')


def parceiros(request):
    parceiros = Parceiro.objects.all()
    return render(request, 'parceiros.html', {'parceiros': parceiros})


def documentacao(request):
    documentos = Documento.objects.all()
    ultimo_documento = documentos.last() if documentos.exists() else None

    documentos_json = serializers.serialize('json', documentos)

    return render(request, 'documentacao.html', {
        'documentos': documentos,
        'ultimo_documento': ultimo_documento,
        'documentos_json': documentos_json
    })


def contato(request):
    return render(request, 'contato.html')


def enviar_contato(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        mensagem = request.POST.get('mensagem')

        corpo_email = f"""
        Nova mensagem do site:

        Nome: {nome}
        E-mail: {email}

        Mensagem:
        {mensagem}
        """

        send_mail(
            subject="Nova mensagem do formulário de contato",
            message=corpo_email,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],  # ou escreva diretamente o e-mail, ex: ['voce@gmail.com']
            fail_silently=False,
        )

        messages.success(request, 'Mensagem enviada com sucesso!')
        return redirect('contato')  # redirecione para a mesma página ou outra

    return redirect('contato')


def doacao(request):
    return render(request, 'doacao.html')


def projetos_view(request):
    projetos = Projeto.objects.prefetch_related('imagens').all()
    return render(request, 'projetos.html', {'projetos': projetos})
