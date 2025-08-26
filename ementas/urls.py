from django.urls import path
from . import views

app_name = "ementas"

urlpatterns = [
    path("", views.ementa_list, name="lista"),
    path("ementa/<int:pk>/", views.ementa_detail, name="detalhe"),
    path("ementa/criar/", views.ementa_create, name="criar"),
    path("ementa/<int:pk>/editar/", views.ementa_edit, name="editar"),
]