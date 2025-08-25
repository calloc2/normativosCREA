from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Ementa

def ementa_list(request):
    q = request.GET.get("q", "").strip()
    tipo_ato = request.GET.get("tipo_ato", "")
    situacao = request.GET.get("situacao", "")
    itens_por_pagina = request.GET.get("itens_por_pagina", "10")
    
    try:
        itens_por_pagina = int(itens_por_pagina)
        if itens_por_pagina not in [10, 50, 100]:
            itens_por_pagina = 10
    except ValueError:
        itens_por_pagina = 10
    
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
    
    paginator = Paginator(qs, itens_por_pagina)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context = {
        "page_obj": page_obj,
        "q": q,
        "tipo_ato": tipo_ato,
        "situacao": situacao,
        "itens_por_pagina": itens_por_pagina,
        "tipos_ato": Ementa.TIPO_ATO_CHOICES,
        "situacoes": Ementa.SITUACAO_CHOICES,
        "opcoes_paginacao": [10, 50, 100],
    }
    return render(request, "ementas/lista.html", context)

def ementa_detail(request, pk):
    ementa = get_object_or_404(Ementa, pk=pk)
    if not ementa.publicado and not (request.user.is_authenticated and request.user.is_staff):
        return render(request, "404.html", status=404)
    return render(request, "ementas/detalhe.html", {"ementa": ementa})