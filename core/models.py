from django.db import models

# Create your models here.


class Doacao(models.Model):
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    cpf = models.CharField(max_length=14)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cpf} - R$ {self.valor} em {self.data.strftime('%d/%m/%Y')}"

