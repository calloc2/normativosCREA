from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import PerfilUsuario

class UsuarioRegistrationForm(UserCreationForm):
    """Formulário para cadastro de novos usuários"""
    
    # Validação de CPF
    cpf = forms.CharField(
        max_length=14,
        validators=[
            RegexValidator(
                regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
                message='CPF deve estar no formato 000.000.000-00'
            )
        ],
        help_text='Formato: 000.000.000-00'
    )
    
    # Validação de telefone
    telefone = forms.CharField(
        max_length=15,
        required=False,
        validators=[
            RegexValidator(
                regex=r'^\(\d{2}\) \d{5}-\d{4}$',
                message='Telefone deve estar no formato (00) 00000-0000'
            )
        ],
        help_text='Formato: (00) 00000-0000'
    )
    
    # Campos obrigatórios
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label='Nome',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label='Sobrenome',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    # Campos profissionais
    tipo_usuario = forms.ChoiceField(
        choices=PerfilUsuario.TIPO_USUARIO_CHOICES,
        required=True,
        label='Tipo de Usuário',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    registro_profissional = forms.CharField(
        max_length=20,
        required=False,
        label='Registro Profissional',
        help_text='Número do registro no CREA (opcional)',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    empresa = forms.CharField(
        max_length=200,
        required=False,
        label='Empresa/Instituição',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    cargo = forms.CharField(
        max_length=100,
        required=False,
        label='Cargo/Função',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    # Documentos
    documento_identidade = forms.FileField(
        required=False,
        label='Documento de Identidade',
        help_text='PDF, JPG ou PNG (opcional)',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    
    comprovante_residencia = forms.FileField(
        required=False,
        label='Comprovante de Residência',
        help_text='PDF, JPG ou PNG (opcional)',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    
    diploma_ou_certificado = forms.FileField(
        required=False,
        label='Diploma ou Certificado',
        help_text='PDF, JPG ou PNG (opcional)',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    
    # Termos de uso
    aceito_termos = forms.BooleanField(
        required=True,
        label='Li e aceito os termos de uso e política de privacidade',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'password1', 'password2'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Estilização dos campos de senha
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        
        # Help texts personalizados
        self.fields['username'].help_text = 'Requerido. 150 caracteres ou menos. Apenas letras, dígitos e @/./+/-/_'
        self.fields['password1'].help_text = 'Sua senha deve conter pelo menos 8 caracteres e não pode ser muito comum.'
        self.fields['password2'].help_text = 'Digite a mesma senha novamente para verificação.'
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este e-mail já está em uso.')
        return email
    
    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if PerfilUsuario.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError('Este CPF já está cadastrado.')
        return cpf

class PerfilUsuarioUpdateForm(forms.ModelForm):
    """Formulário para edição do perfil do usuário"""
    
    # Validação de telefone
    telefone = forms.CharField(
        max_length=15,
        required=False,
        validators=[
            RegexValidator(
                regex=r'^\(\d{2}\) \d{5}-\d{4}$',
                message='Telefone deve estar no formato (00) 00000-0000'
            )
        ],
        help_text='Formato: (00) 00000-0000'
    )
    
    class Meta:
        model = PerfilUsuario
        fields = [
            'cpf', 'telefone', 'tipo_usuario', 'registro_profissional', 
            'empresa', 'cargo', 'documento_identidade', 
            'comprovante_residencia', 'diploma_ou_certificado'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Estilização dos campos
        for field in self.fields.values():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({'class': 'form-control'})
    
    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        # Verifica se o CPF já existe para outro usuário
        if PerfilUsuario.objects.exclude(pk=self.instance.pk).filter(cpf=cpf).exists():
            raise forms.ValidationError('Este CPF já está cadastrado.')
        return cpf
