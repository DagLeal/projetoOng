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

class MediaProjeto(models.Model):
    MEDIA_TYPES = (
        ('image', 'Image'),
        ('video', 'Video'),
    )
    projeto = models.ForeignKey('Projeto', on_delete=models.CASCADE, related_name='media')
    media_type = models.CharField(max_length=5, choices=MEDIA_TYPES)
    arquivo = models.FileField(upload_to='projetos/')
    titulo = models.CharField(max_length=200, blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)

    def __str__(self):
        return f"{self.media_type} - {self.titulo}"
