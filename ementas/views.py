from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render,get_object_or_404
from .models import Ementa

def ementa_list(request):
    q = request.GET.get("q","").strip()
    qs = Ementa.objects.filter(publicado=True)
    if q:
        qs = qs.filter(
            Q(titulo__icontains=q) |
            Q(numero__icontains=q) |
            Q(resumo__icontains=q)
        )
    paginator = Paginator(qs, 10) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj, "q": q}
    return render(request, "ementas/lista.html", context)

def ementa_detail(request, pk):
    ementa = get_object_or_404(Ementa, pk=pk)
    if not ementa.publicado and not (request.user.is_authenticated and request.user.is_staff):
        return render(request, "404.html", status=404)
    return render(request, "ementas/detalhe.html", {"ementa": ementa})