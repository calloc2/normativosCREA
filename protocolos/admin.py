from django.contrib import admin
from .models import Protocolo

@admin.register(Protocolo)
class ProtocoloAdmin(admin.ModelAdmin):
    list_display = [
        'numero', 'tipo', 'cpf_cnpj_formatado', 'data_emissao', 
        'local_armazenamento', 'protocolo_sitac', 'criado_por'
    ]
    list_filter = ['tipo', 'data_emissao', 'criado_em']
    search_fields = ['numero', 'cpf_cnpj', 'local_armazenamento', 'observacoes']
    readonly_fields = ['data_emissao', 'criado_em', 'atualizado_em', 'criado_por']
    date_hierarchy = 'data_emissao'
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('numero', 'tipo', 'cpf_cnpj')
        }),
        ('Localização', {
            'fields': ('local_armazenamento', 'observacoes')
        }),
        ('SITAC', {
            'fields': ('protocolo_sitac',),
            'classes': ('collapse',)
        }),
        ('Controle', {
            'fields': ('criado_por', 'data_emissao', 'criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Se for uma nova criação
            obj.criado_por = request.user
        super().save_model(request, obj, form, change)
