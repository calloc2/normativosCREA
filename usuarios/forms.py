from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import PerfilUsuario

class UsuarioRegistrationForm(UserCreationForm):
    cpf = forms.CharField(
        max_length=14,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
                message='CPF deve estar no formato 000.000.000-00'
            )
        ],
        help_text='Formato: 000.000.000-00',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000-00'})
    )
    
    telefone = forms.CharField(
        max_length=15,
        required=False,
        validators=[
            RegexValidator(
                regex=r'^\(\d{2}\) \d{5}-\d{4}$',
                message='Telefone deve estar no formato (00) 00000-0000'
            )
        ],
        help_text='Formato: (00) 00000-0000',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'})
    )
    
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
    
    registro_profissional = forms.CharField(
        max_length=20,
        required=False,
        label='Registro Profissional',
        help_text='Número do registro no CREA',
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
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Requerido. 150 caracteres ou menos. Apenas letras, números e @/./+/-/_'
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
    telefone = forms.CharField(
        max_length=15,
        required=False,
        validators=[
            RegexValidator(
                regex=r'^\(\d{2}\) \d{5}-\d{4}$',
                message='Telefone deve estar no formato (00) 00000-0000'
            )
        ],
        help_text='Formato: (00) 00000-0000',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'})
    )

    class Meta:
        model = PerfilUsuario
        fields = [
            'cpf', 'telefone', 'registro_profissional',
            'empresa', 'cargo'
        ]
        widgets = {
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'registro_profissional': forms.TextInput(attrs={'class': 'form-control'}),
            'empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona formatação automática para CPF
        if self.instance and self.instance.cpf:
            self.fields['cpf'].widget.attrs['placeholder'] = '000.000.000-00'

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if PerfilUsuario.objects.exclude(pk=self.instance.pk).filter(cpf=cpf).exists():
            raise forms.ValidationError('Este CPF já está cadastrado.')
        return cpf
