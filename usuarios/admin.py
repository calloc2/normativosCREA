from django.contrib import admin
from .models import PerfilUsuario

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'cpf', 'tipo_usuario', 'permissao', 
        'conta_aprovada', 'email_verificado', 'criado_em'
    ]
    list_filter = [
        'tipo_usuario', 'permissao', 'conta_aprovada', 
        'email_verificado', 'pode_publicar', 'pode_visualizar_sigiloso',
        'criado_em', 'data_aprovacao'
    ]
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'cpf']
    ordering = ['-criado_em']
    
    fieldsets = (
        ('Usuário', {
            'fields': ('user',)
        }),
        ('Informações Pessoais', {
            'fields': ('cpf', 'telefone')
        }),
        ('Informações Profissionais', {
            'fields': ('tipo_usuario', 'registro_profissional', 'empresa', 'cargo')
        }),
        ('Permissões', {
            'fields': ('permissao', 'pode_publicar', 'pode_visualizar_sigiloso')
        }),
        ('Documentos', {
            'fields': ('documento_identidade', 'comprovante_residencia', 'diploma_ou_certificado'),
            'classes': ('collapse',)
        }),
        ('Status da Conta', {
            'fields': ('email_verificado', 'conta_aprovada', 'data_aprovacao', 'aprovado_por'),
            'classes': ('collapse',)
        }),
        ('Datas Importantes', {
            'fields': ('criado_em', 'atualizado_em', 'ultimo_acesso'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['criado_em', 'atualizado_em']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'aprovado_por')
    
    actions = ['aprovar_usuarios', 'rejeitar_usuarios', 'verificar_emails']
    
    def aprovar_usuarios(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(
            conta_aprovada=True, 
            data_aprovacao=timezone.now(),
            aprovado_por=request.user
        )
        self.message_user(request, f'{updated} usuário(s) aprovado(s) com sucesso.')
    aprovar_usuarios.short_description = "Aprovar usuários selecionados"
    
    def rejeitar_usuarios(self, request, queryset):
        updated = queryset.update(conta_aprovada=False, data_aprovacao=None, aprovado_por=None)
        self.message_user(request, f'{updated} usuário(s) rejeitado(s).')
    rejeitar_usuarios.short_description = "Rejeitar usuários selecionados"
    
    def verificar_emails(self, request, queryset):
        updated = queryset.update(email_verificado=True)
        self.message_user(request, f'{updated} usuário(s) com e-mail verificado.')
    verificar_emails.short_description = "Marcar e-mails como verificados"
