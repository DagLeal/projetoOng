from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('sobre/', sobre, name='sobre'),
    path('historia/', historia, name='historia'),
    path('presidencia/', presidencia, name='presidencia'),
    path('projetos/', projetos, name='projetos'),
    path('servicos/', servicos, name='servicos'),
    path('documentacao/', documentacao, name='documentacao'),
    path('contato/', contato, name='contato'),
    path('doacao/', doacao, name='doacao'),
]

