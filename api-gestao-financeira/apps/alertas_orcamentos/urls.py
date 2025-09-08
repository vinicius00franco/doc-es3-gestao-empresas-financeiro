from django.urls import path
from . import views

urlpatterns = [
    path('alertas/', views.AlertaListCreateView.as_view(), name='alerta-list-create'),
    path('alertas/<int:pk>/', views.AlertaDetailView.as_view(), name='alerta-detail'),
    path('orcamentos/', views.OrcamentoMensalListCreateView.as_view(), name='orcamento-list-create'),
    path('orcamentos/<int:pk>/', views.OrcamentoMensalDetailView.as_view(), name='orcamento-detail'),
]
