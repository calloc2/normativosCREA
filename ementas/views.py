from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from .models import Ementa

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
    
    # Filtro de sigiloso baseado no usuário
    if not request.user.is_authenticated or not hasattr(request.user, 'perfil') or not request.user.perfil.can_view_confidential:
        qs = qs.filter(sigiloso=False)
    
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
        "user_can_view_confidential": request.user.is_authenticated and hasattr(request.user, 'perfil') and request.user.perfil.can_view_confidential,
    }
    return render(request, "ementas/lista.html", context)

def ementa_detail(request, pk):
    ementa = get_object_or_404(Ementa, pk=pk)
    
    # Verifica se a ementa está publicada
    if not ementa.publicado and not (request.user.is_authenticated and request.user.is_staff):
        return render(request, "404.html", status=404)
    
    # Verifica se o usuário pode ver ementas sigilosas
    if ementa.sigiloso and not (request.user.is_authenticated and hasattr(request.user, 'perfil') and request.user.perfil.can_view_confidential):
        return render(request, "ementas/detalhe.html", {
            "ementa": ementa,
            "acesso_negado": True
        })
    
    return render(request, "ementas/detalhe.html", {"ementa": ementa})