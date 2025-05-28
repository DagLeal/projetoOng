from django import forms
from .models import Doacao

class DoacaoForm(forms.ModelForm):
    class Meta:
        model = Doacao
        fields = ['nome', 'email', 'cpf', 'valor']
