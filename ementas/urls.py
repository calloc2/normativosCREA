from django.urls import path
from . import views

app_name = "ementas"

urlpatterns = [
    path("", views.ementa_list,name="lista"),
    path("ementa/<int:pk>/", views.ementa_detail,name="ementa_detail"),
]