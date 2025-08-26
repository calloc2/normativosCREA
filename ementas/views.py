from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Ementa
from .forms import EmentaForm

def ementa_list(request):
    q = request.GET.get("q", "").strip()
    tipo_ato = request.GET.get("tipo_ato", "")
    situacao = request.GET.get("situacao", "")
    data_inicio = request.GET.get("data_inicio", "")
    data_fim = request.GET.get("data_fim", "")
    itens_por_pagina = request.GET.get("itens_por_pagina", "10")
    
    try:
        itens_por_pagina = int(itens_por_pagina)
        if itens_por_pagina not in [10, 50, 100]:
            itens_por_pagina = 10
    except ValueError:
        itens_por_pagina = 10
    
    # Base queryset - apenas ementas publicadas
    qs = Ementa.objects.filter(publicado=True)
    
    if q:
        qs = qs.filter(
            Q(titulo__icontains=q) |
            Q(numero__icontains=q) |
            Q(resumo__icontains=q) |
            Q(ementa__icontains=q)
        )
    
    if tipo_ato:
        qs = qs.filter(tipo_ato_normativo=tipo_ato)
    
    if situacao:
        qs = qs.filter(situacao=situacao)
    
    # Filtros de data
    if data_inicio:
        try:
            data_inicio_parsed = parse_date(data_inicio)
            if data_inicio_parsed:
                qs = qs.filter(data_publicacao__gte=data_inicio_parsed)
        except (ValueError, TypeError):
            pass
    
    if data_fim:
        try:
            data_fim_parsed = parse_date(data_fim)
            if data_fim_parsed:
                qs = qs.filter(data_publicacao__lte=data_fim_parsed)
        except (ValueError, TypeError):
            pass
    
    paginator = Paginator(qs, itens_por_pagina)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context = {
        "page_obj": page_obj,
        "q": q,
        "tipo_ato": tipo_ato,
        "situacao": situacao,
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "itens_por_pagina": itens_por_pagina,
        "tipos_ato": Ementa.TIPO_ATO_CHOICES,
        "situacoes": Ementa.SITUACAO_CHOICES,
        "opcoes_paginacao": [10, 50, 100],
        "user_can_edit": request.user.is_authenticated and hasattr(request.user, 'perfil') and request.user.perfil.can_edit,
        "user_can_publish": request.user.is_authenticated and hasattr(request.user, 'perfil') and request.user.perfil.can_publish,
    }
    return render(request, "ementas/lista.html", context)

def ementa_detail(request, pk):
    ementa = get_object_or_404(Ementa, pk=pk)
    
    # Verifica se a ementa está publicada
    if not ementa.publicado and not (request.user.is_authenticated and request.user.is_staff):
        return render(request, "404.html", status=404)
    
    context = {
        "ementa": ementa,
        "user_can_edit": request.user.is_authenticated and hasattr(request.user, 'perfil') and request.user.perfil.can_edit,
        "user_can_publish": request.user.is_authenticated and hasattr(request.user, 'perfil') and request.user.perfil.can_publish,
    }
    return render(request, "ementas/detalhe.html", context)

@login_required
def ementa_create(request):
    """View para criar nova ementa"""
    if not hasattr(request.user, 'perfil') or not request.user.perfil.can_publish:
        messages.error(request, 'Você não tem permissão para criar ementas.')
        return redirect('ementas:lista')
    
    if request.method == 'POST':
        form = EmentaForm(request.POST, request.FILES)
        if form.is_valid():
            ementa = form.save(commit=False)
            ementa.criado_por = request.user
            ementa.save()
            messages.success(request, 'Ementa criada com sucesso!')
            return redirect('ementas:detalhe', pk=ementa.pk)
    else:
        form = EmentaForm()
    
    context = {
        'form': form,
        'action': 'criar',
        'title': 'Criar Nova Ementa'
    }
    return render(request, 'ementas/form.html', context)

@login_required
def ementa_edit(request, pk):
    """View para editar ementa existente"""
    ementa = get_object_or_404(Ementa, pk=pk)
    
    # Verifica permissões
    if not hasattr(request.user, 'perfil'):
        messages.error(request, 'Perfil não encontrado.')
        return redirect('ementas:lista')
    
    perfil = request.user.perfil
    
    # Apenas criador ou usuários com permissão de edição podem editar
    if not (perfil.can_edit or ementa.criado_por == request.user):
        messages.error(request, 'Você não tem permissão para editar esta ementa.')
        return redirect('ementas:detalhe', pk=ementa.pk)
    
    if request.method == 'POST':
        form = EmentaForm(request.POST, request.FILES, instance=ementa)
        if form.is_valid():
            ementa = form.save()
            messages.success(request, 'Ementa atualizada com sucesso!')
            return redirect('ementas:detalhe', pk=ementa.pk)
    else:
        form = EmentaForm(instance=ementa)
    
    context = {
        'form': form,
        'ementa': ementa,
        'action': 'editar',
        'title': 'Editar Ementa'
    }
    return render(request, 'ementas/form.html', context)