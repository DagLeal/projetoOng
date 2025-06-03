from django.urls import path
from .views import gerar_pix_view

urlpatterns = [
    path("gerar-pix/", gerar_pix_view, name="gerar_pix")
]
