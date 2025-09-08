from django.urls import path
from . import views

urlpatterns = [
    path('automacoes/regras/', views.RegraListCreateView.as_view(), name='automacao-regra-list-create'),
    path('automacoes/regras/<int:pk>/', views.RegraDetailView.as_view(), name='automacao-regra-detail'),
    path('automacoes/concilia/', views.conciliar, name='automacao-concilia'),
]
