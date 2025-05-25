from django.db import models

# Create your models here.


class Documento(models.Model):
    titulo = models.CharField(max_length=255)
    imagem = models.ImageField(upload_to='documentos/')

    def __str__(self):
        return self.titulo


class Doacao(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    cpf = models.CharField(max_length=14)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_transacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - R$ {self.valor}"


class Noticia(models.Model):
    titulo = models.CharField(max_length=255)
    materia = models.TextField()
    data_publicacao = models.DateField()
    imagem = models.ImageField(upload_to='noticias/')

    def __str__(self):
        return self.titulo

