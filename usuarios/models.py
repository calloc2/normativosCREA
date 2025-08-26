from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class PerfilUsuario(models.Model):
    TIPO_USUARIO_CHOICES = [
        ('engenheiro', 'Engenheiro'),
        ('arquiteto', 'Arquiteto'),
        ('tecnico', 'Técnico'),
        ('estudante', 'Estudante'),
        ('funcionario', 'Funcionário CREA-TO'),
        ('outro', 'Outro'),
    ]
    
    PERMISSAO_CHOICES = [
        ('visualizador', 'Visualizador'),
        ('editor', 'Editor'),
        ('publicador', 'Publicador'),
        ('admin', 'Administrador'),
    ]
    
    # Relação com o User padrão
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    
    # Campos básicos
    cpf = models.CharField("CPF", max_length=14, unique=True, help_text="000.000.000-00")
    telefone = models.CharField("Telefone", max_length=15, blank=True, help_text="(00) 00000-0000")
    
    # Campos profissionais
    tipo_usuario = models.CharField("Tipo de Usuário", max_length=20, choices=TIPO_USUARIO_CHOICES, default='engenheiro')
    registro_profissional = models.CharField("Registro Profissional", max_length=20, blank=True, help_text="Número do registro no CREA")
    empresa = models.CharField("Empresa/Instituição", max_length=200, blank=True)
    cargo = models.CharField("Cargo/Função", max_length=100, blank=True)
    
    # Permissões
    permissao = models.CharField("Nível de Permissão", max_length=20, choices=PERMISSAO_CHOICES, default='visualizador')
    pode_publicar = models.BooleanField("Pode Publicar Atas", default=False)
    pode_visualizar_sigiloso = models.BooleanField("Pode Visualizar Sigiloso", default=False)
    
    # Documentos
    documento_identidade = models.FileField(
        "Documento de Identidade", 
        upload_to="usuarios/documentos/", 
        null=True, 
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])]
    )
    comprovante_residencia = models.FileField(
        "Comprovante de Residência", 
        upload_to="usuarios/documentos/", 
        null=True, 
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])]
    )
    diploma_ou_certificado = models.FileField(
        "Diploma ou Certificado", 
        upload_to="usuarios/documentos/", 
        null=True, 
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])]
    )
    
    # Status e validação
    email_verificado = models.BooleanField("E-mail Verificado", default=False)
    conta_aprovada = models.BooleanField("Conta Aprovada", default=False)
    data_aprovacao = models.DateTimeField("Data de Aprovação", null=True, blank=True)
    aprovado_por = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='usuarios_aprovados'
    )
    
    # Campos de auditoria
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    atualizado_em = models.DateTimeField("Atualizado em", auto_now=True)
    ultimo_acesso = models.DateTimeField("Último Acesso", null=True, blank=True)
    
    class Meta:
        verbose_name = "Perfil de Usuário"
        verbose_name_plural = "Perfis de Usuários"
        ordering = ['-criado_em']
    
    def __str__(self):
        return f"Perfil de {self.user.get_full_name()}"
    
    @property
    def is_approved(self):
        return self.conta_aprovada and self.email_verificado
    
    @property
    def can_publish(self):
        return self.is_approved and self.pode_publicar
    
    @property
    def can_view_confidential(self):
        return self.is_approved and self.pode_visualizar_sigiloso
