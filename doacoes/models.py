from django.db import models

# Create your models here.
from django.db import models

class Doacao(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    cpf = models.CharField(max_length=14)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nome} - R${self.valor}'
