from django import forms
from .models import Protocolo
import re

class ProtocoloForm(forms.ModelForm):
    class Meta:
        model = Protocolo
        fields = [
            'numero', 'cpf_cnpj', 'local_armazenamento', 'observacoes'
        ]
        widgets = {
            'numero': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Número do protocolo'
            }),
            'cpf_cnpj': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'CPF (11 dígitos) ou CNPJ (14 dígitos)',
                'data-mask': 'cpf-cnpj'
            }),
            'local_armazenamento': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ex: CAIXA X, FILEIRA X, FACE X'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Observações adicionais'
            }),

        }
        labels = {
            'numero': 'Número de Protocolo',
            'cpf_cnpj': 'CPF/CNPJ',
            'local_armazenamento': 'Local de Armazenamento',
            'observacoes': 'Observações',
        }
        help_texts = {
            'numero': 'Número único do protocolo',
            'cpf_cnpj': 'CPF (11 dígitos) ou CNPJ (14 dígitos)',
            'local_armazenamento': 'Local onde o processo está armazenado',
            'observacoes': 'Observações adicionais sobre o protocolo',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona classes Bootstrap aos labels
        for field_name, field in self.fields.items():
            if hasattr(field, 'label'):
                field.label = field.label

    def clean_cpf_cnpj(self):
        """Validação e formatação do CPF/CNPJ"""
        cpf_cnpj = self.cleaned_data.get('cpf_cnpj')
        if cpf_cnpj:
            # Remove caracteres não numéricos
            cpf_cnpj_limpo = re.sub(r'[^\d]', '', cpf_cnpj)
            
            if len(cpf_cnpj_limpo) == 11:
                # É um CPF
                return cpf_cnpj_limpo
            elif len(cpf_cnpj_limpo) == 14:
                # É um CNPJ
                return cpf_cnpj_limpo
            else:
                raise forms.ValidationError(
                    'CPF deve ter 11 dígitos ou CNPJ deve ter 14 dígitos'
                )
        return cpf_cnpj

    def clean(self):
        """Validação geral do formulário"""
        cleaned_data = super().clean()
        cpf_cnpj = cleaned_data.get('cpf_cnpj')
        
        if cpf_cnpj:
            cpf_cnpj_limpo = re.sub(r'[^\d]', '', cpf_cnpj)
            
            # Define automaticamente o tipo baseado no número de dígitos
            if len(cpf_cnpj_limpo) == 11:
                cleaned_data['tipo'] = 'profissional'
            elif len(cpf_cnpj_limpo) == 14:
                cleaned_data['tipo'] = 'empresa'
        
        return cleaned_data
