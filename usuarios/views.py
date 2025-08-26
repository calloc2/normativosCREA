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
    if request.method == 'POST':
        form = UsuarioRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            # Criar perfil do usuário
            perfil = PerfilUsuario.objects.create(
                user=user,
                cpf=form.cleaned_data['cpf'],
                telefone=form.cleaned_data['telefone'],
                registro_profissional=form.cleaned_data['registro_profissional'],
                empresa=form.cleaned_data['empresa'],
                cargo=form.cleaned_data['cargo'],
            )
            messages.success(request, 'Cadastro realizado com sucesso! Sua conta será analisada por um administrador.')
            return redirect('usuarios:login')
    else:
        form = UsuarioRegistrationForm()
    return render(request, 'usuarios/cadastro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Atualiza último acesso
                if hasattr(user, 'perfil'):
                    user.perfil.ultimo_acesso = timezone.now()
                    user.perfil.save()
                messages.success(request, f'Bem-vindo, {user.get_full_name()}!')
                return redirect('usuarios:dashboard')
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = AuthenticationForm()
    return render(request, 'usuarios/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Você foi desconectado com sucesso.')
    return redirect('ementas:lista')

@login_required
def perfil(request):
    try:
        perfil = request.user.perfil
    except PerfilUsuario.DoesNotExist:
        perfil = None
    
    context = {
        'perfil': perfil,
        'user': request.user
    }
    return render(request, 'usuarios/perfil.html', context)

@login_required
def editar_perfil(request):
    try:
        perfil = request.user.perfil
    except PerfilUsuario.DoesNotExist:
        perfil = None
    
    if request.method == 'POST':
        form = PerfilUsuarioUpdateForm(request.POST, instance=perfil)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.user = request.user
            perfil.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('usuarios:perfil')
    else:
        form = PerfilUsuarioUpdateForm(instance=perfil)
    
    context = {
        'form': form,
        'perfil': perfil
    }
    return render(request, 'usuarios/editar_perfil.html', context)

@login_required
def dashboard(request):
    # Estatísticas básicas
    total_ementas = Ementa.objects.filter(publicado=True).count()
    ementas_publicas = Ementa.objects.filter(publicado=True, sigiloso=False).count()
    ementas_sigilosas = Ementa.objects.filter(publicado=True, sigiloso=True).count()
    
    # Ementas recentes (apenas públicas)
    ementas_recentes = Ementa.objects.filter(
        publicado=True, 
        sigiloso=False
    ).order_by('-criado_em')[:5]
    
    context = {
        'total_ementas': total_ementas,
        'ementas_publicas': ementas_publicas,
        'ementas_sigilosas': ementas_sigilosas,
        'ementas_recentes': ementas_recentes,
        'perfil': getattr(request.user, 'perfil', None)
    }
    return render(request, 'usuarios/dashboard.html', context)
