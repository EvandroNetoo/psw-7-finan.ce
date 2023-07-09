from django.urls import path
from .views import *

urlpatterns = [
    path('novo_valor/', novo_valor, name="novo_valor"),
    path('extrato/', extrato, name="extrato"),
    path('exportar_extrato/', exportar_extrato, name="exportar_extrato"),
]
