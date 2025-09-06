from django.urls import path
from . import views

urlpatterns = [
    # Planos
    path('planos/', views.PlanoListView.as_view(), name='plano-list'),
    
    # Assinaturas
    path('assinaturas/atual/', views.AssinaturaAtualView.as_view(), name='assinatura-atual'),
    path('assinaturas/upgrade/', views.upgrade_assinatura, name='upgrade-assinatura'),
    path('assinaturas/confirmar-pagamento/', views.confirmar_pagamento, name='confirmar-pagamento'),
]