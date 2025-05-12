from django import forms


class DoacaoForm(forms.Form):
    valor = forms.IntegerField(label='Valor da doação (R$)', min_value=1)
    cpf = forms.CharField(label='CPF', max_length=14)

