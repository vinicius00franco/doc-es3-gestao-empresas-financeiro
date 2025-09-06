from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Transacao, Categoria, Fornecedor
from .serializers import (
    TransacaoSerializer, 
    CategoriaSerializer, 
    FornecedorSerializer
)


class TransacaoListCreateView(generics.ListCreateAPIView):
    serializer_class = TransacaoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo_transacao', 'status', 'categoria', 'data_transacao']
    search_fields = ['descricao', 'observacoes', 'numero_documento']
    ordering_fields = ['data_transacao', 'valor', 'criado_em']
    ordering = ['-data_transacao']

    def get_queryset(self):
        user = self.request.user
        empresa_padrao = user.empresas.filter(empresa_padrao=True).first()
        
        if not empresa_padrao:
            return Transacao.objects.none()
        
        queryset = Transacao.objects.filter(empresa=empresa_padrao).select_related(
            'categoria', 'fornecedor'
        )
        
        # Filtros customizados
        data_inicio = self.request.query_params.get('data_inicio')
        data_fim = self.request.query_params.get('data_fim')
        
        if data_inicio:
            queryset = queryset.filter(data_transacao__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data_transacao__lte=data_fim)
        
        return queryset


class TransacaoDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TransacaoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        empresa_padrao = user.empresas.filter(empresa_padrao=True).first()
        
        if not empresa_padrao:
            return Transacao.objects.none()
        
        return Transacao.objects.filter(empresa=empresa_padrao)


class CategoriaListCreateView(generics.ListCreateAPIView):
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome', 'descricao']

    def get_queryset(self):
        user = self.request.user
        empresa_padrao = user.empresas.filter(empresa_padrao=True).first()
        
        if not empresa_padrao:
            return Categoria.objects.none()
        
        queryset = Categoria.objects.filter(empresa=empresa_padrao, ativa=True)
        
        # Filtro por tipo de transação
        tipo = self.request.query_params.get('tipo_transacao')
        if tipo:
            queryset = queryset.filter(tipo_transacao=tipo)
        
        return queryset


class CategoriaDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        empresa_padrao = user.empresas.filter(empresa_padrao=True).first()
        
        if not empresa_padrao:
            return Categoria.objects.none()
        
        return Categoria.objects.filter(empresa=empresa_padrao)


class FornecedorListCreateView(generics.ListCreateAPIView):
    serializer_class = FornecedorSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['razao_social', 'nome_fantasia', 'cnpj']

    def get_queryset(self):
        user = self.request.user
        empresa_padrao = user.empresas.filter(empresa_padrao=True).first()
        
        if not empresa_padrao:
            return Fornecedor.objects.none()
        
        return Fornecedor.objects.filter(empresa=empresa_padrao, ativo=True)


class FornecedorDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FornecedorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        empresa_padrao = user.empresas.filter(empresa_padrao=True).first()
        
        if not empresa_padrao:
            return Fornecedor.objects.none()
        
        return Fornecedor.objects.filter(empresa=empresa_padrao)