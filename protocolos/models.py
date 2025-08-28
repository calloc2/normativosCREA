from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re

class Protocolo(models.Model):
    TIPO_CHOICES = [
        ('profissional', 'Profissional'),
        ('empresa', 'Empresa'),
    ]
    
    numero = models.CharField(
        "Número de Protocolo", 
        max_length=50, 
        unique=True,
        help_text="Número único do protocolo"
    )
    
    data_emissao = models.DateField(
        "Data de Emissão", 
        auto_now_add=True,
        help_text="Data de criação do protocolo"
    )
    
    cpf_cnpj = models.CharField(
        "CPF/CNPJ", 
        max_length=18,
        validators=[
            RegexValidator(
                regex=r'^\d{11}|\d{14}$',
                message='CPF deve ter 11 dígitos ou CNPJ deve ter 14 dígitos'
            )
        ],
        help_text="CPF (11 dígitos) ou CNPJ (14 dígitos)"
    )
    
    tipo = models.CharField(
        "Tipo", 
        max_length=15, 
        choices=TIPO_CHOICES,
        help_text="Tipo de pessoa física ou jurídica"
    )
    
    local_armazenamento = models.CharField(
        "Local de Armazenamento", 
        max_length=100,
        help_text="Ex: CAIXA X, FILEIRA X, FACE X"
    )
    
    observacoes = models.TextField(
        "Observações", 
        blank=True,
        help_text="Observações adicionais sobre o protocolo"
    )
    
    # Campo para resposta da API SITAC
    protocolo_sitac = models.CharField(
        "Protocolo SITAC", 
        max_length=50, 
        blank=True,
        null=True,
        help_text="Número de protocolo retornado pela API do SITAC"
    )
    
    # Campos de usuário
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='protocolos_criados',
        verbose_name="Criado por"
    )
    
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    atualizado_em = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        ordering = ["-data_emissao", "-criado_em"]
        verbose_name = "Protocolo"
        verbose_name_plural = "Protocolos"

    def __str__(self):
        return f"Protocolo {self.numero} - {self.get_tipo_display()}"

    def clean(self):
        """Validação personalizada para CPF/CNPJ"""
        if self.cpf_cnpj:
            # Remove caracteres não numéricos
            cpf_cnpj_limpo = re.sub(r'[^\d]', '', self.cpf_cnpj)
            
            if len(cpf_cnpj_limpo) == 11:
                # É um CPF
                if self.tipo != 'profissional':
                    self.tipo = 'profissional'
            elif len(cpf_cnpj_limpo) == 14:
                # É um CNPJ
                if self.tipo != 'empresa':
                    self.tipo = 'empresa'
            else:
                raise ValidationError({
                    'cpf_cnpj': 'CPF deve ter 11 dígitos ou CNPJ deve ter 14 dígitos'
                })
    
    def save(self, *args, **kwargs):
        """Sobrescreve save para aplicar validações"""
        self.clean()
        super().save(*args, **kwargs)
    
    @property
    def cpf_cnpj_formatado(self):
        """Retorna o CPF/CNPJ formatado"""
        cpf_cnpj_limpo = re.sub(r'[^\d]', '', self.cpf_cnpj)
        if len(cpf_cnpj_limpo) == 11:
            # Formata CPF: 000.000.000-00
            return f"{cpf_cnpj_limpo[:3]}.{cpf_cnpj_limpo[3:6]}.{cpf_cnpj_limpo[6:9]}-{cpf_cnpj_limpo[9:]}"
        elif len(cpf_cnpj_limpo) == 14:
            # Formata CNPJ: 00.000.000/0000-00
            return f"{cpf_cnpj_limpo[:2]}.{cpf_cnpj_limpo[2:5]}.{cpf_cnpj_limpo[5:8]}/{cpf_cnpj_limpo[8:12]}-{cpf_cnpj_limpo[12:]}"
        return self.cpf_cnpj
