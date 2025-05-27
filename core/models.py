from django.db import models

class Documento(models.Model):
    titulo = models.CharField(max_length=255)
    arquivo = models.FileField(upload_to='documentos/', default='documentos/default.png')

    def __str__(self):
        return self.titulo

    @property
    def tipo(self):
        if self.arquivo.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
            return 'imagem'
        elif self.arquivo.name.lower().endswith('.pdf'):
            return 'pdf'
        elif self.arquivo.name.lower().endswith(('.xls', '.xlsx', '.csv')):
            return 'planilha'
        return 'outro'

from django.db import models

class Doacao(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    cpf = models.CharField(max_length=14)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_hora = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)

    def __str__(self):
        return f"{self.nome} - R$ {self.valor}"




class Noticia(models.Model):
    titulo = models.CharField(max_length=255)
    materia = models.TextField()
    data_publicacao = models.DateField()
    imagem = models.ImageField(upload_to='noticias/')

    def __str__(self):
        return self.titulo


class Parceiro(models.Model):
    nome = models.CharField(max_length=255)
    imagem = models.ImageField(upload_to='parceiros/')
    link = models.URLField()
    texto = models.TextField()

    def __str__(self):
        return self.nome


class Projeto(models.Model):
    nome = models.CharField(max_length=200)
    link = models.URLField(blank=True)
    texto = models.TextField()

    def __str__(self):
        return self.nome

class ImagemProjeto(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='imagens')
    imagem = models.ImageField(upload_to='projetos/')
    titulo = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.titulo or f"Imagem de {self.projeto.nome}"
