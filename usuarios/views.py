from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils import timezone
from .models import PerfilUsuario
from .forms import UsuarioRegistrationForm, PerfilUsuarioUpdateForm
from ementas.models import Ementa

def cadastro(request):
    """View para cadastro de novos usuários"""
    if request.method == 'POST':
        form = UsuarioRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            
            # Criar perfil do usuário
            perfil = PerfilUsuario.objects.create(
                user=user,
                cpf=form.cleaned_data['cpf'],
                telefone=form.cleaned_data['telefone'],
                tipo_usuario=form.cleaned_data['tipo_usuario'],
                registro_profissional=form.cleaned_data['registro_profissional'],
                empresa=form.cleaned_data['empresa'],
                cargo=form.cleaned_data['cargo'],
                documento_identidade=form.cleaned_data.get('documento_identidade'),
                comprovante_residencia=form.cleaned_data.get('comprovante_residencia'),
                diploma_ou_certificado=form.cleaned_data.get('diploma_ou_certificado'),
            )
            
            messages.success(
                request, 
                'Cadastro realizado com sucesso! Sua conta será analisada por um administrador.'
            )
            return redirect('usuarios:login')
    else:
        form = UsuarioRegistrationForm()
    
    return render(request, 'usuarios/cadastro.html', {'form': form})

def login_view(request):
    """View para login de usuários"""
    if request.user.is_authenticated:
        return redirect('usuarios:perfil')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # Atualiza último acesso no perfil
                    try:
                        perfil = user.perfil
                        perfil.ultimo_acesso = timezone.now()
                        perfil.save(update_fields=['ultimo_acesso'])
                    except PerfilUsuario.DoesNotExist:
                        pass
                    
                    messages.success(request, f'Bem-vindo, {user.get_full_name()}!')
                    return redirect('usuarios:perfil')
                else:
                    messages.error(request, 'Sua conta foi desativada.')
            else:
                messages.error(request, 'Usuário ou senha incorretos.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'usuarios/login.html', {'form': form})

def logout_view(request):
    """View para logout de usuários"""
    logout(request)
    messages.info(request, 'Você foi desconectado com sucesso.')
    return redirect('ementas:lista')

@login_required
def perfil(request):
    """View para perfil do usuário logado"""
    try:
        perfil = request.user.perfil
    except PerfilUsuario.DoesNotExist:
        perfil = None
    
    # Busca ementas do usuário se ele pode publicar
    ementas_usuario = []
    if perfil and perfil.can_publish:
        ementas_usuario = Ementa.objects.filter(
            criado_por=request.user
        ).order_by('-criado_em')[:5]
    
    # Busca ementas sigilosas se ele pode visualizar
    ementas_sigilosas = []
    if perfil and perfil.can_view_confidential:
        ementas_sigilosas = Ementa.objects.filter(
            sigiloso=True
        ).order_by('-criado_em')[:5]
    
    context = {
        'usuario': request.user,
        'perfil': perfil,
        'ementas_usuario': ementas_usuario,
        'ementas_sigilosas': ementas_sigilosas,
    }
    return render(request, 'usuarios/perfil.html', context)

@login_required
def editar_perfil(request):
    """View para edição do perfil do usuário"""
    try:
        perfil = request.user.perfil
    except PerfilUsuario.DoesNotExist:
        perfil = None
    
    if request.method == 'POST':
        form = PerfilUsuarioUpdateForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            if perfil is None:
                # Criar perfil se não existir
                perfil = form.save(commit=False)
                perfil.user = request.user
                perfil.save()
            else:
                form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('usuarios:perfil')
    else:
        form = PerfilUsuarioUpdateForm(instance=perfil)
    
    return render(request, 'usuarios/editar_perfil.html', {'form': form})

@login_required
def dashboard(request):
    """Dashboard principal para usuários autenticados"""
    try:
        perfil = request.user.perfil
    except PerfilUsuario.DoesNotExist:
        perfil = None
    
    # Estatísticas básicas
    total_ementas = Ementa.objects.filter(publicado=True).count()
    ementas_recentes = Ementa.objects.filter(publicado=True).order_by('-criado_em')[:10]
    
    # Ementas do usuário se ele pode publicar
    minhas_ementas = []
    if perfil and perfil.can_publish:
        minhas_ementas = Ementa.objects.filter(criado_por=request.user).order_by('-criado_em')[:5]
    
    context = {
        'usuario': request.user,
        'perfil': perfil,
        'total_ementas': total_ementas,
        'ementas_recentes': ementas_recentes,
        'minhas_ementas': minhas_ementas,
    }
    return render(request, 'usuarios/dashboard.html', context)
