from django.contrib import admin
from .models import Ementa

@admin.register(Ementa)
class EmentaAdmin(admin.ModelAdmin):
    list_display = [
        'titulo', 'numero', 'tipo_ato_normativo', 'situacao',
        'data_publicacao', 'publicado', 'sigiloso', 'criado_por', 'criado_em'
    ]
    list_filter = [
        'tipo_ato_normativo', 'situacao', 'publicado', 'sigiloso',
        'data_publicacao', 'criado_em'
    ]
    search_fields = ['titulo', 'numero', 'ementa', 'resumo']
    ordering = ['-data_publicacao', '-criado_em']
    readonly_fields = ['criado_em', 'atualizado_em']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('numero', 'titulo', 'tipo_ato_normativo', 'situacao', 'data_publicacao')
        }),
        ('Controle de Acesso', {
            'fields': ('sigiloso', 'publicado', 'criado_por'),
            'description': 'Marque como sigiloso se esta ementa não deve ter conteúdo visível'
        }),
        ('Conteúdo (não disponível para ementas sigilosas)', {
            'fields': ('ementa', 'resumo', 'arquivo'),
            'classes': ('collapse',),
            'description': 'Estes campos são automaticamente limpos para ementas sigilosas'
        }),
        ('Datas', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Torna campos de conteúdo readonly se for sigiloso"""
        if obj and obj.sigiloso:
            return self.readonly_fields + ('ementa', 'resumo', 'arquivo')
        return self.readonly_fields
    
    def get_fieldsets(self, request, obj=None):
        """Ajusta fieldsets baseado no status sigiloso"""
        fieldsets = list(super().get_fieldsets(request, obj))
        
        if obj and obj.sigiloso:
            # Se for sigiloso, remove o fieldset de conteúdo
            fieldsets = [fs for fs in fieldsets if 'Conteúdo' not in fs[0]]
        
        return fieldsets
    
    def save_model(self, request, obj, form, change):
        if not change:  # Se é uma nova ementa
            obj.criado_por = request.user
        
        # Aplica validações antes de salvar
        obj.clean()
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('criado_por')
    
    actions = ['marcar_sigiloso', 'desmarcar_sigiloso']
    
    def marcar_sigiloso(self, request, queryset):
        """Marca ementas selecionadas como sigilosas"""
        updated = queryset.update(sigiloso=True)
        self.message_user(request, f'{updated} ementa(s) marcada(s) como sigilosa(s).')
    marcar_sigiloso.short_description = "Marcar ementas como sigilosas"
    
    def desmarcar_sigiloso(self, request, queryset):
        """Desmarca ementas selecionadas como sigilosas"""
        updated = queryset.update(sigiloso=False)
        self.message_user(request, f'{updated} ementa(s) desmarcada(s) como sigilosa(s).')
    desmarcar_sigiloso.short_description = "Desmarcar ementas como sigilosas"