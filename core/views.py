from .models import Documento, Parceiro, Projeto, InstagramAccount
from django.core import serializers
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from .utils import InstagramService, InstagramServiceError
from django.views.decorators.http import require_GET
from django.core.cache import cache
import logging
from django.utils import timezone


def doacao(request):
    return render(request, 'doacao.html')


logger = logging.getLogger(__name__)


def home(request):
    context = {}
    try:
        # Get the user's Instagram account if connected
        account = InstagramAccount.objects.filter(user=request.user, is_active=True).first()

        if account:
            # Initialize service with automatic token refresh
            instagram = InstagramService(
                access_token=account.access_token,
                token_timestamp=account.token_timestamp
            )

            # Store potentially refreshed token
            if instagram.access_token != account.access_token:
                account.access_token = instagram.access_token
                account.token_timestamp = instagram.token_timestamp
                account.save()

            context['instagram_posts'] = instagram.get_recent_posts(count=8)
            context['instagram_connected'] = True
        else:
            context['instagram_posts'] = []
            context['instagram_connected'] = False

    except InstagramServiceError as e:
        messages.error(request, f"Instagram service error: {e}")
        context['instagram_posts'] = []

    parceiros = Parceiro.objects.all()

    # Order by newest first (add - before the field name for descending)
    projetos_list = Projeto.objects.prefetch_related('media').order_by('-id')

    # Add pagination (5 items per page)
    paginator = Paginator(projetos_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {'parceiros': parceiros, 'page_obj': page_obj})

@require_GET
def instagram_auth_start(request):
    try:
        instagram = InstagramService()
        auth_url = instagram.get_oauth_authorize_url()
        return redirect(auth_url)
    except InstagramServiceError as e:
        messages.error(request, f"Could not start Instagram authentication: {e}")
        return redirect('home')

@require_GET
def instagram_auth_callback(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to connect Instagram")
        return redirect('home')

    if 'error' in request.GET:
        error_description = request.GET.get('error_description', 'No description provided')
        messages.error(request, f"Instagram authorization failed: {error_description}")
        return redirect('home')

    if 'code' not in request.GET:
        messages.error(request, "Instagram authorization callback missing required code")
        return redirect('home')

    try:
        instagram = InstagramService()
        short_lived_token = instagram.get_access_token(request.GET['code'])
        long_lived_token = instagram.get_long_lived_token(short_lived_token)

        # Get or create Instagram account
        account, created = InstagramAccount.objects.get_or_create(
            user=request.user,
            defaults={
                'access_token': long_lived_token,
                'token_timestamp': timezone.now()
            }
        )

        if not created:
            account.access_token = long_lived_token
            account.token_timestamp = timezone.now()
            account.is_active = True
            account.save()

        messages.success(request, "Successfully connected Instagram account!")
        return redirect('home')

    except InstagramServiceError as e:
        messages.error(request, f"Instagram authentication failed: {e}")
        return redirect('home')


def instagram_disconnect(request):
    if 'instagram_access_token' in request.session:
        del request.session['instagram_access_token']
        cache.clear()
        messages.success(request, "Disconnected from Instagram")
    return redirect('home')


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
