from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('sobre/', views.sobre, name='sobre'),
    path('historia/', views.historia, name='historia'),
    path('presidencia/', views.presidencia, name='presidencia'),
    path('projetos/', views.projetos, name='projetos'),
    path('parceiros/', views.parceiros, name='parceiros'),
    path('documentacao/', views.documentacao, name='documentacao'),
    path('contato/', views.contato, name='contato'),
    path('doacao/', views.doacao, name='doacao'),
    path('enviar-contato/', views.enviar_contato, name='enviar_contato'),
    path('instagram/auth/', views.instagram_auth_start, name='instagram_auth_start'),
    path('instagram/callback/', views.instagram_auth_callback, name='instagram_auth_callback'),
    path('instagram/disconnect/', views.instagram_disconnect, name='instagram_disconnect'),
]

