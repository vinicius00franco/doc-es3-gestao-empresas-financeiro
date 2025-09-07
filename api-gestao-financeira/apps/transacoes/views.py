from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from core.mixins import TenantViewMixin
from .models import Transacao, Categoria, Fornecedor
from .serializers import (
    TransacaoSerializer, 
    CategoriaSerializer, 
    FornecedorSerializer
)


class TransacaoListCreateView(TenantViewMixin, generics.ListCreateAPIView):
    serializer_class = TransacaoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo_transacao', 'status', 'categoria', 'data_transacao']
    search_fields = ['descricao', 'observacoes', 'numero_documento']
    ordering_fields = ['data_transacao', 'valor', 'criado_em']
    ordering = ['-data_transacao']

    def get_queryset(self):
        queryset = super().get_queryset()
        if not queryset.exists():
            return Transacao.objects.none()
        
        queryset = queryset.select_related('categoria', 'fornecedor')
        
        # Filtros customizados
        data_inicio = self.request.query_params.get('data_inicio')
        data_fim = self.request.query_params.get('data_fim')
        
        if data_inicio:
            queryset = queryset.filter(data_transacao__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data_transacao__lte=data_fim)
        
        return queryset


class TransacaoDetailView(TenantViewMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransacaoSerializer

    def get_queryset(self):
        return super().get_queryset()


class CategoriaListCreateView(TenantViewMixin, generics.ListCreateAPIView):
    serializer_class = CategoriaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome', 'descricao']

    def get_queryset(self):
        queryset = super().get_queryset().filter(ativa=True)
        
        # Filtro por tipo de transação
        tipo = self.request.query_params.get('tipo_transacao')
        if tipo:
            queryset = queryset.filter(tipo_transacao=tipo)
        
        return queryset


class CategoriaDetailView(TenantViewMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategoriaSerializer

    def get_queryset(self):
        return super().get_queryset()


class FornecedorListCreateView(TenantViewMixin, generics.ListCreateAPIView):
    serializer_class = FornecedorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['razao_social', 'nome_fantasia', 'cnpj']

    def get_queryset(self):
        return super().get_queryset().filter(ativo=True)


class FornecedorDetailView(TenantViewMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FornecedorSerializer

    def get_queryset(self):
        return super().get_queryset()