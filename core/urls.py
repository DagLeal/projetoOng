from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('sobre/', views.sobre, name='sobre'),
    path('historia/', views.historia, name='historia'),
    path('presidencia/', views.presidencia, name='presidencia'),
    path('projetos/', views.projetos, name='projetos'),
    path('servicos/', views.servicos, name='servicos'),
    path('documentacao/', views.documentacao, name='documentacao'),
    path('contato/', views.contato, name='contato'),
    path('doacao/', views.doacao, name='doacao'),
    path('qr/<int:doacao_id>/', views.gerar_qr_code_pix, name='qr_pix'),
]

