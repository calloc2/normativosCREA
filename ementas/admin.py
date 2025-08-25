from django.contrib import admin
from .models import Ementa

@admin.register(Ementa)
class EmentaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "numero", "tipo_ato_normativo", "situacao", "data_publicacao", "publicado")
    list_filter = ("publicado", "tipo_ato_normativo", "situacao", "data_publicacao")
    search_fields = ("titulo", "resumo", "ementa", "numero")
    ordering = ("-data_publicacao", "-criado_em")
    
    fieldsets = (
        ("Informações Básicas", {
            "fields": ("titulo", "numero", "tipo_ato_normativo", "situacao")
        }),
        ("Conteúdo", {
            "fields": ("ementa", "resumo")
        }),
        ("Arquivos e Publicação", {
            "fields": ("arquivo", "data_publicacao", "publicado")
        }),
        ("Metadados", {
            "fields": ("criado_em", "atualizado_em"),
            "classes": ("collapse",)
        }),
    )
    
    readonly_fields = ("criado_em", "atualizado_em")