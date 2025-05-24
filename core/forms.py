from django import forms


class DoacaoForm(forms.Form):
    valor = forms.IntegerField(min_value=1, label="Valor (R$)")
    cpf = forms.CharField(max_length=14, required=False, label="CPF (opcional)")

