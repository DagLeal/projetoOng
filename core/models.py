from django.db import models

# Create your models here.

class Doacao(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nome} - R$ {self.valor}'

