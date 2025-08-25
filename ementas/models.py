from django.db import models

class Ementa(models.Model):
    numero = models.CharField("Número", max_length=30,blank=True)
    titulo = models.CharField("Título",max_length=200)
    resumo = models.TextField("Resumo",blank=True)
    data_publicacao = models.DateField("Data de Publicação",blank=True,null=True)
    arquivo = models.FileField("PDF",upload_to="ementas/",null=True,blank=True)
    publicado = models.BooleanField("Publicado",default=True)
    criado_em = models.DateTimeField("Criado em",auto_now_add=True)
    atualizado_em = models.DateTimeField("Atualizado em",auto_now=True)

    class Meta:
        ordering = ["-data_publicacao", "-criado_em"]
        verbose_name = "Ementa"
        verbose_name_plural = "Ementas"

    def __str__(self):
        return f"{self.titulo}"
