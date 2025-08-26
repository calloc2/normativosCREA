from django import forms
from .models import Ementa

class EmentaForm(forms.ModelForm):
    class Meta:
        model = Ementa
        fields = [
            'numero', 'titulo', 'tipo_ato_normativo', 'situacao',
            'ementa', 'resumo', 'arquivo', 'data_publicacao',
            'publicado', 'sigiloso'
        ]
        widgets = {
            'numero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número da ementa'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título da ementa'}),
            'tipo_ato_normativo': forms.Select(attrs={'class': 'form-select'}),
            'situacao': forms.Select(attrs={'class': 'form-select'}),
            'ementa': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Resumo da ementa'}),
            'resumo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Resumo adicional'}),
            'arquivo': forms.FileInput(attrs={'class': 'form-control'}),
            'data_publicacao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'publicado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sigiloso': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'numero': 'Número',
            'titulo': 'Título',
            'tipo_ato_normativo': 'Tipo de Ato Normativo',
            'situacao': 'Situação',
            'ementa': 'Ementa (Resumo)',
            'resumo': 'Resumo Adicional',
            'arquivo': 'PDF',
            'data_publicacao': 'Data de Publicação',
            'publicado': 'Publicado',
            'sigiloso': 'Sigiloso',
        }
        help_texts = {
            'ementa': 'Resumo do ato normativo para facilitar a pesquisa',
            'resumo': 'Resumo adicional opcional',
            'arquivo': 'Arquivo PDF da ementa',
            'sigiloso': 'Marque se esta ementa contém informações sigilosas',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona classes Bootstrap aos labels
        for field_name, field in self.fields.items():
            if hasattr(field, 'label'):
                field.label = field.label

    def clean(self):
        cleaned_data = super().clean()
        sigiloso = cleaned_data.get('sigiloso')
        
        # Se for sigiloso, limpa campos de conteúdo
        if sigiloso:
            cleaned_data['ementa'] = ""
            cleaned_data['resumo'] = ""
            cleaned_data['arquivo'] = None
            
            # Define título básico se não fornecido
            if not cleaned_data.get('titulo'):
                tipo_ato = cleaned_data.get('tipo_ato_normativo', 'Ato')
                numero = cleaned_data.get('numero', '')
                cleaned_data['titulo'] = f"{tipo_ato} {numero}".strip()
        
        return cleaned_data
