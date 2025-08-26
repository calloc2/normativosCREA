from django.db import models

class Ementa(models.Model):
    TIPO_ATO_CHOICES = [
        ('portaria', 'Portaria'),
        ('decisao_plenaria', 'Decisão Plenária'),
        ('ato_administrativo', 'Ato Administrativo'),
    ]
    
    SITUACAO_CHOICES = [
        ('em_vigor', 'Em Vigor'),
        ('revogada', 'Revogada'),
        ('cancelada', 'Cancelada'),
    ]
    
    numero = models.CharField("Número", max_length=30, blank=True)
    titulo = models.CharField("Título", max_length=200)
    tipo_ato_normativo = models.CharField(
        "Tipo de Ato Normativo", 
        max_length=20, 
        choices=TIPO_ATO_CHOICES,
        default='portaria'
    )
    situacao = models.CharField(
        "Situação", 
        max_length=20, 
        choices=SITUACAO_CHOICES,
        default='em_vigor'
    )
    ementa = models.TextField("Ementa (Resumo)", blank=True, help_text="Resumo do ato normativo para facilitar a pesquisa")
    resumo = models.TextField("Resumo", blank=True)
    data_publicacao = models.DateField("Data de Publicação", blank=True, null=True)
    arquivo = models.FileField("PDF", upload_to="ementas/pdf/", null=True, blank=True)
    publicado = models.BooleanField("Publicado", default=True)
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    atualizado_em = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        ordering = ["-data_publicacao", "-criado_em"]
        verbose_name = "Ementa"
        verbose_name_plural = "Ementas"

    def __str__(self):
        return f"{self.titulo}"
