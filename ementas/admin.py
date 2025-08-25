from django.contrib import admin
from .models import Ementa

@admin.register(Ementa)
class EmentaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "numero", "data_publicacao", "publicado")
    list_filter = ("publicado", "data_publicacao")
    search_fields = ("titulo", "resumo", "numero")
    ordering = ("-data_publicacao", "-criado_em")