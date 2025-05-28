import qrcode
import io
from django.http import HttpResponse
from .models import Doacao, Documento, Parceiro, Projeto
from django.core import serializers
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from .forms import DoacaoForm
from django.core.files.base import ContentFile
from django.utils import timezone
import base64
from pypix.pix import Pix

def gerar_pix_com_pypix(valor):
    pix = Pix()
    pix.set_merchant_name("Dagner Costa Leal")
    pix.set_merchant_city("Rio de Janeiro")
    pix.set_pixkey("05782543795")  # sua chave Pix
    pix.set_amount(float(valor))   # valor precisa ser float
    pix.set_description("Doação via Site CADON")
    pix.set_txid("DOACAO123")  # um identificador qualquer

    # Gera o código EMV do Pix
    brcode = str(pix)

    # Gera o QR Code e salva em buffer de memória
    qr = qrcode.make(brcode)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    return brcode, qr_base64

def doacao(request):
    context = {}

    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        valor = request.POST.get('valor')

        # Gera código Pix e QR code com pypix
        pix_code, qr_base64 = gerar_pix_com_pypix(valor)

        # Salva no banco
        Doacao.objects.create(
            nome=nome,
            email=email,
            cpf=cpf,
            valor=valor,
            data_hora=timezone.now()
        )

        context = {
            'qr_code': qr_base64,
            'nome': nome,
            'valor_doado': valor,
            'pix_code': pix_code
        }

    return render(request, 'doacao.html', context)
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


def projetos_view(request):
    projetos = Projeto.objects.prefetch_related('imagens').all()
    return render(request, 'projetos.html', {'projetos': projetos})
