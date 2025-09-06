from django.urls import path
from . import views

urlpatterns = [
    # Transações
    path('transacoes/', views.TransacaoListCreateView.as_view(), name='transacao-list-create'),
    path('transacoes/<int:pk>/', views.TransacaoDetailView.as_view(), name='transacao-detail'),
    
    # Categorias
    path('categorias/', views.CategoriaListCreateView.as_view(), name='categoria-list-create'),
    path('categorias/<int:pk>/', views.CategoriaDetailView.as_view(), name='categoria-detail'),
    
    # Fornecedores
    path('fornecedores/', views.FornecedorListCreateView.as_view(), name='fornecedor-list-create'),
    path('fornecedores/<int:pk>/', views.FornecedorDetailView.as_view(), name='fornecedor-detail'),
]