from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

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
    
    # Campo sigiloso deve vir antes dos campos de conteúdo
    sigiloso = models.BooleanField("Sigiloso", default=False, help_text="Marque se esta ementa contém informações sigilosas")
    
    # Campos de conteúdo (só preenchidos se não for sigiloso)
    ementa = models.TextField("Ementa (Resumo)", blank=True, help_text="Resumo do ato normativo para facilitar a pesquisa")
    resumo = models.TextField("Resumo", blank=True)
    arquivo = models.FileField("PDF", upload_to="ementas/pdf/", null=True, blank=True)
    
    data_publicacao = models.DateField("Data de Publicação", blank=True, null=True)
    
    # Campos de controle de acesso
    publicado = models.BooleanField("Publicado", default=True)
    
    # Campos de usuário
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ementas_criadas',
        verbose_name="Criado por"
    )
    
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    atualizado_em = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        ordering = ["-data_publicacao", "-criado_em"]
        verbose_name = "Ementa"
        verbose_name_plural = "Ementas"

    def __str__(self):
        if self.sigiloso:
            return f"{self.tipo_ato_normativo.title()} {self.numero} - SIGILOSO"
        return f"{self.titulo}"
    
    def clean(self):
        """Validação personalizada para ementas sigilosas"""
        if self.sigiloso:
            # Se for sigiloso, limpa os campos de conteúdo
            self.ementa = ""
            self.resumo = ""
            self.arquivo = None
            # Mantém apenas título básico
            if not self.titulo:
                self.titulo = f"{self.get_tipo_ato_normativo_display()} {self.numero}"
    
    def save(self, *args, **kwargs):
        """Sobrescreve save para aplicar validações"""
        self.clean()
        super().save(*args, **kwargs)
    
    @property
    def pode_ser_visualizada_por(self, user):
        """Verifica se um usuário pode visualizar esta ementa"""
        if not self.sigiloso:
            return True
        if user.is_authenticated and hasattr(user, 'perfil') and user.perfil.can_view_confidential:
            return True
        return False
    
    @property
    def conteudo_disponivel(self):
        """Retorna se a ementa tem conteúdo disponível para visualização"""
        return not self.sigiloso and (self.ementa or self.resumo or self.arquivo)
