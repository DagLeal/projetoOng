from django.shortcuts import render

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
    return render(request, 'doacao.html')
