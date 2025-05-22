from django.shortcuts import render
from .forms import DoacaoForm
from .models import Doacao
from pypix import Pix
import qrcode
import io
import base64


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


def servicos(request):
    return render(request, 'servicos.html')


def documentacao(request):
    return render(request, 'documentacao.html')


def contato(request):
    return render(request, 'contato.html')


def doacao(request):
    qr_code_base64 = None
    codigo_pix = None

    if request.method == 'POST':
        form = DoacaoForm(request.POST)
        if form.is_valid():
            valor = form.cleaned_data['valor']
            cpf = form.cleaned_data['cpf']

            Doacao.objects.create(valor=valor, cpf=cpf)

            pix = Pix()
            pix.set_receiver_name("Seu Nome ou Empresa")
            pix.set_receiver_city("SuaCidade")
            pix.set_pix_key("sua-chave-pix@exemplo.com")
            pix.set_amount(float(valor))

            codigo_pix = pix.build_pix_code()

            # Gerar QR code
            qr = qrcode.make(codigo_pix)
            buffer = io.BytesIO()
            qr.save(buffer, format='PNG')
            qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()

    else:
        form = DoacaoForm()

    return render(request, 'doacao.html', {
        'form': form,
        'qr_code': qr_code_base64,
        'codigo_pix': codigo_pix
    })


