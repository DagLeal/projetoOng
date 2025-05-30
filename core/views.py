from .models import Documento, Parceiro, Projeto
from django.core import serializers
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator

def doacao(request):
    return render(request, 'doacao.html')

def home(request):
    return render(request, 'home.html')


def sobre(request):
    return render(request, 'sobre.html')


def historia(request):
    return render(request, 'historia.html')


def presidencia(request):
    return render(request, 'presidencia.html')


def projetos(request):
    # Order by newest first (add - before the field name for descending)
    projetos_list = Projeto.objects.prefetch_related('media').order_by('-id')

    # Add pagination (5 items per page)
    paginator = Paginator(projetos_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'projetos.html', {'page_obj': page_obj})


def parceiros(request):
    parceiros = Parceiro.objects.all()
    return render(request, 'parceiros.html', {'parceiros': parceiros})


def documentacao(request):
    documentos = Documento.objects.all().order_by('-id')
    ultimo_documento = documentos.first() if documentos.exists() else None

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
