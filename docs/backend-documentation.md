# Backend Documentation - Django REST Framework

Documentação técnica do backend Django REST Framework para o sistema de gestão financeira.

## 🐍 Visão Geral

O backend é desenvolvido em Django REST Framework seguindo a arquitetura Feature Folder com padrão MVC, proporcionando alta coesão e baixo acoplamento.

## 🏗️ Arquitetura

### Feature Folder Structure
Cada funcionalidade possui sua própria pasta com responsabilidades bem definidas:

- **models.py**: Definição dos modelos de dados (ORM)
- **views.py**: Lógica de controle e endpoints
- **serializers.py**: Serialização/deserialização de dados
- **urls.py**: Roteamento de URLs
- **tests.py**: Testes unitários e de integração
- **permissions.py**: Permissões customizadas
- **admin.py**: Interface administrativa

## 📁 Estrutura do Projeto

```
gestao_financeira/
├── gestao_financeira/          # Configurações principais
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py            # Configurações base
│   │   ├── development.py     # Ambiente de desenvolvimento
│   │   ├── production.py      # Ambiente de produção
│   │   └── testing.py         # Ambiente de testes
│   ├── urls.py                # URLs principais
│   ├── wsgi.py                # WSGI para deploy
│   └── asgi.py                # ASGI para WebSockets
├── core/                      # Funcionalidades centrais
│   ├── __init__.py
│   ├── authentication.py     # Autenticação JWT customizada
│   ├── permissions.py        # Permissões globais
│   ├── exceptions.py         # Tratamento de exceções
│   ├── middleware.py         # Middlewares customizados
│   ├── pagination.py         # Paginação customizada
│   └── validators.py         # Validadores reutilizáveis
├── usuarios/                  # Feature: Gestão de usuários
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── tests.py
│   ├── permissions.py
│   └── admin.py
├── empresas/                  # Feature: Gestão de empresas
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── tests.py
│   └── admin.py
├── transacoes/               # Feature: Gestão de transações
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── tests.py
│   ├── filters.py           # Filtros customizados
│   └── admin.py
├── assinaturas/             # Feature: Planos e assinaturas
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── tests.py
│   ├── permissions.py       # Controle de acesso por plano
│   └── admin.py
├── relatorios/              # Feature: Relatórios
│   ├── __init__.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── tests.py
│   └── generators.py        # Geradores de relatório
├── utils/                   # Utilitários
│   ├── __init__.py
│   ├── formatters.py        # Formatadores de dados
│   ├── validators.py        # Validações específicas
│   ├── constants.py         # Constantes do sistema
│   └── helpers.py           # Funções auxiliares
├── static/                  # Arquivos estáticos
├── media/                   # Uploads de usuários
├── requirements/            # Dependências
│   ├── base.txt            # Dependências base
│   ├── development.txt     # Dependências de desenvolvimento
│   └── production.txt      # Dependências de produção
├── manage.py
├── Dockerfile
└── docker-compose.yml
```

## ⚙️ Configurações

### Settings Base
```python
# gestao_financeira/settings/base.py
import os
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Security
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-in-production')
DEBUG = False
ALLOWED_HOSTS = []

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'drf_spectacular',
]

LOCAL_APPS = [
    'core',
    'usuarios',
    'empresas',
    'transacoes',
    'assinaturas',
    'relatorios',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'core.pagination.CustomPageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# JWT Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'gestao_financeira'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'postgres123'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True
```

## 👤 Feature: Usuarios

### Models
```python
# usuarios/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
    
    def __str__(self):
        return self.nome

class TokenRecuperacao(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    usado = models.BooleanField(default=False)
    expira_em = models.DateTimeField()
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Token de Recuperação'
        verbose_name_plural = 'Tokens de Recuperação'
```

### Serializers
```python
# usuarios/serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Usuario

class UsuarioRegistroSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True, min_length=8)
    confirmar_senha = serializers.CharField(write_only=True)
    
    class Meta:
        model = Usuario
        fields = ('nome', 'email', 'senha', 'confirmar_senha')
    
    def validate(self, attrs):
        if attrs['senha'] != attrs['confirmar_senha']:
            raise serializers.ValidationError("As senhas não coincidem.")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirmar_senha')
        senha = validated_data.pop('senha')
        usuario = Usuario(**validated_data)
        usuario.set_password(senha)
        usuario.save()
        return usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'nome', 'email', 'criado_em', 'atualizado_em')
        read_only_fields = ('id', 'criado_em', 'atualizado_em')

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    senha = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        senha = attrs.get('senha')
        
        if email and senha:
            usuario = authenticate(username=email, password=senha)
            if not usuario:
                raise serializers.ValidationError('Credenciais inválidas.')
            if not usuario.is_active:
                raise serializers.ValidationError('Conta inativa.')
            attrs['usuario'] = usuario
        return attrs
```

### Views
```python
# usuarios/views.py
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Usuario
from .serializers import UsuarioRegistroSerializer, UsuarioSerializer, LoginSerializer

class RegistroView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioRegistroSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        usuario = serializer.save()
        
        return Response({
            'usuario': UsuarioSerializer(usuario).data,
            'message': 'Usuário criado com sucesso.'
        }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    usuario = serializer.validated_data['usuario']
    refresh = RefreshToken.for_user(usuario)
    
    return Response({
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh),
        'user': UsuarioSerializer(usuario).data
    })

class PerfilView(generics.RetrieveUpdateAPIView):
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
```

## 🏢 Feature: Empresas

### Models
```python
# empresas/models.py
from django.db import models
from django.core.validators import RegexValidator
from usuarios.models import Usuario

class Empresa(models.Model):
    TIPOS_EMPRESA = [
        ('MEI', 'Microempreendedor Individual'),
        ('ME', 'Microempresa'),
        ('EPP', 'Empresa de Pequeno Porte'),
        ('LTDA', 'Sociedade Limitada'),
        ('SA', 'Sociedade Anônima'),
    ]
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='empresas')
    cnpj = models.CharField(
        max_length=18,
        unique=True,
        validators=[RegexValidator(regex=r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$')]
    )
    razao_social = models.CharField(max_length=255)
    nome_fantasia = models.CharField(max_length=255, blank=True)
    tipo_empresa = models.CharField(max_length=5, choices=TIPOS_EMPRESA)
    ativa = models.BooleanField(default=True)
    empresa_padrao = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        constraints = [
            models.UniqueConstraint(
                fields=['usuario'],
                condition=models.Q(empresa_padrao=True),
                name='unique_empresa_padrao_por_usuario'
            )
        ]
    
    def save(self, *args, **kwargs):
        if self.empresa_padrao:
            # Remove empresa padrão anterior
            Empresa.objects.filter(
                usuario=self.usuario,
                empresa_padrao=True
            ).update(empresa_padrao=False)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nome_fantasia or self.razao_social
```

### ViewSets
```python
# empresas/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Empresa
from .serializers import EmpresaSerializer

class EmpresaViewSet(viewsets.ModelViewSet):
    serializer_class = EmpresaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Empresa.objects.filter(usuario=self.request.user, ativa=True)
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
    
    @action(detail=True, methods=['post'])
    def set_padrao(self, request, pk=None):
        empresa = self.get_object()
        empresa.empresa_padrao = True
        empresa.save()
        return Response({'message': 'Empresa definida como padrão.'})
    
    @action(detail=False, methods=['get'])
    def padrao(self, request):
        empresa = self.get_queryset().filter(empresa_padrao=True).first()
        if empresa:
            serializer = self.get_serializer(empresa)
            return Response(serializer.data)
        return Response({'detail': 'Nenhuma empresa padrão encontrada.'}, 
                       status=status.HTTP_404_NOT_FOUND)
```

## 💰 Feature: Transacoes

### Models
```python
# transacoes/models.py
from django.db import models
from decimal import Decimal
from empresas.models import Empresa

class Categoria(models.Model):
    TIPOS_TRANSACAO = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
        ('ambos', 'Ambos'),
    ]
    
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='categorias')
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    cor = models.CharField(max_length=7, default='#2196F3')
    icone = models.CharField(max_length=50, default='category')
    tipo_transacao = models.CharField(max_length=10, choices=TIPOS_TRANSACAO, default='ambos')
    ativa = models.BooleanField(default=True)
    categoria_padrao = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        unique_together = ['empresa', 'nome']

class Transacao(models.Model):
    TIPOS_TRANSACAO = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    ]
    
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]
    
    FORMAS_PAGAMENTO = [
        ('dinheiro', 'Dinheiro'),
        ('pix', 'PIX'),
        ('cartao_credito', 'Cartão de Crédito'),
        ('cartao_debito', 'Cartão de Débito'),
        ('boleto', 'Boleto'),
        ('transferencia', 'Transferência'),
    ]
    
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='transacoes')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data_transacao = models.DateField()
    tipo_transacao = models.CharField(max_length=10, choices=TIPOS_TRANSACAO)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='confirmada')
    observacoes = models.TextField(blank=True)
    numero_documento = models.CharField(max_length=100, blank=True)
    forma_pagamento = models.CharField(max_length=20, choices=FORMAS_PAGAMENTO, blank=True)
    recorrente = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'
        ordering = ['-data_transacao', '-criado_em']
    
    def clean(self):
        if self.valor <= 0:
            raise ValidationError('O valor deve ser maior que zero.')
    
    def __str__(self):
        return f"{self.descricao} - {self.valor}"
```

### Filters
```python
# transacoes/filters.py
import django_filters
from .models import Transacao

class TransacaoFilter(django_filters.FilterSet):
    data_inicio = django_filters.DateFilter(field_name='data_transacao', lookup_expr='gte')
    data_fim = django_filters.DateFilter(field_name='data_transacao', lookup_expr='lte')
    valor_min = django_filters.NumberFilter(field_name='valor', lookup_expr='gte')
    valor_max = django_filters.NumberFilter(field_name='valor', lookup_expr='lte')
    
    class Meta:
        model = Transacao
        fields = ['tipo_transacao', 'categoria', 'status', 'forma_pagamento']
```

### ViewSets
```python
# transacoes/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from assinaturas.permissions import HasActiveSubscription
from .models import Transacao, Categoria
from .serializers import TransacaoSerializer, CategoriaSerializer
from .filters import TransacaoFilter

class TransacaoViewSet(viewsets.ModelViewSet):
    serializer_class = TransacaoSerializer
    permission_classes = [IsAuthenticated, HasActiveSubscription]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransacaoFilter
    search_fields = ['descricao', 'numero_documento']
    ordering_fields = ['data_transacao', 'valor', 'criado_em']
    
    def get_queryset(self):
        return Transacao.objects.filter(
            empresa__usuario=self.request.user,
            empresa__ativa=True
        )
    
    def perform_create(self, serializer):
        # Verificar limites do plano
        self.check_transaction_limits()
        serializer.save()
    
    def check_transaction_limits(self):
        user = self.request.user
        subscription = user.assinatura
        if subscription.plano.limite_transacoes:
            current_month_count = self.get_current_month_transactions_count()
            if current_month_count >= subscription.plano.limite_transacoes:
                raise PermissionDenied(
                    "Limite de transações mensais atingido. Faça upgrade do seu plano."
                )
```

## 📊 Feature: Assinaturas

### Models
```python
# assinaturas/models.py
from django.db import models
from usuarios.models import Usuario

class Plano(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    limite_transacoes = models.IntegerField(null=True, blank=True)
    limite_empresas = models.IntegerField(null=True, blank=True)
    permite_relatorios = models.BooleanField(default=False)
    permite_exportacao = models.BooleanField(default=False)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Plano'
        verbose_name_plural = 'Planos'
    
    def __str__(self):
        return self.nome

class Assinatura(models.Model):
    STATUS_CHOICES = [
        ('ativa', 'Ativa'),
        ('cancelada', 'Cancelada'),
        ('inadimplente', 'Inadimplente'),
        ('expirada', 'Expirada'),
    ]
    
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='assinatura')
    plano = models.ForeignKey(Plano, on_delete=models.PROTECT)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='ativa')
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    gateway_pagamento = models.CharField(max_length=50, blank=True)
    id_transacao_gateway = models.CharField(max_length=255, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Assinatura'
        verbose_name_plural = 'Assinaturas'
    
    def __str__(self):
        return f"{self.usuario.nome} - {self.plano.nome}"
```

### Permissions
```python
# assinaturas/permissions.py
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

class HasActiveSubscription(permissions.BasePermission):
    message = "Assinatura inativa ou expirada."
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        try:
            subscription = request.user.assinatura
            return subscription.status == 'ativa'
        except:
            return False

class CanAccessReports(permissions.BasePermission):
    message = "Seu plano não permite acesso a relatórios."
    
    def has_permission(self, request, view):
        try:
            subscription = request.user.assinatura
            return subscription.plano.permite_relatorios
        except:
            return False
```

## 📈 Feature: Relatorios

### Views
```python
# relatorios/views.py
from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from assinaturas.permissions import CanAccessReports
from transacoes.models import Transacao

class DashboardView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        empresa_id = request.query_params.get('empresa_id')
        periodo = request.query_params.get('periodo', '30d')
        
        # Calcular data de início baseada no período
        if periodo == '7d':
            data_inicio = timezone.now().date() - timedelta(days=7)
        elif periodo == '30d':
            data_inicio = timezone.now().date() - timedelta(days=30)
        elif periodo == '90d':
            data_inicio = timezone.now().date() - timedelta(days=90)
        else:
            data_inicio = timezone.now().date() - timedelta(days=365)
        
        # Filtrar transações
        transacoes = Transacao.objects.filter(
            empresa__usuario=request.user,
            data_transacao__gte=data_inicio,
            status='confirmada'
        )
        
        if empresa_id:
            transacoes = transacoes.filter(empresa_id=empresa_id)
        
        # Calcular resumo
        entradas = transacoes.filter(tipo_transacao='entrada').aggregate(
            total=Sum('valor'))['total'] or 0
        saidas = transacoes.filter(tipo_transacao='saida').aggregate(
            total=Sum('valor'))['total'] or 0
        
        # Entradas por categoria
        entradas_por_categoria = transacoes.filter(
            tipo_transacao='entrada'
        ).values('categoria__nome').annotate(
            valor=Sum('valor')
        ).order_by('-valor')[:5]
        
        # Saídas por categoria
        saidas_por_categoria = transacoes.filter(
            tipo_transacao='saida'
        ).values('categoria__nome').annotate(
            valor=Sum('valor')
        ).order_by('-valor')[:5]
        
        return Response({
            'periodo': periodo,
            'resumo': {
                'total_entradas': str(entradas),
                'total_saidas': str(saidas),
                'saldo': str(entradas - saidas),
                'transacoes_count': transacoes.count()
            },
            'entradas_por_categoria': entradas_por_categoria,
            'saidas_por_categoria': saidas_por_categoria
        })

class FluxoCaixaView(views.APIView):
    permission_classes = [IsAuthenticated, CanAccessReports]
    
    def get(self, request):
        empresa_id = request.query_params.get('empresa_id')
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')
        
        # Implementar lógica do relatório de fluxo de caixa
        # ...
        
        return Response({
            'empresa': {},
            'periodo': {},
            'resumo': {},
            'transacoes': []
        })
```

## 🧪 Testes

### Test Base
```python
# core/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class BaseAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            nome='Test User',
            password='testpass123'
        )
        self.token = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}'
        )
```

### Testes de Transações
```python
# transacoes/tests.py
from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from core.tests import BaseAPITestCase
from empresas.models import Empresa
from .models import Transacao, Categoria

class TransacaoAPITestCase(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.empresa = Empresa.objects.create(
            usuario=self.user,
            cnpj='12.345.678/0001-90',
            razao_social='Test Company',
            tipo_empresa='LTDA'
        )
        self.categoria = Categoria.objects.create(
            empresa=self.empresa,
            nome='Test Category',
            tipo_transacao='entrada'
        )
    
    def test_create_transacao(self):
        url = reverse('transacao-list')
        data = {
            'empresa': self.empresa.id,
            'categoria': self.categoria.id,
            'descricao': 'Test Transaction',
            'valor': '100.00',
            'data_transacao': '2025-08-21',
            'tipo_transacao': 'entrada'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transacao.objects.count(), 1)
    
    def test_list_transacoes(self):
        Transacao.objects.create(
            empresa=self.empresa,
            categoria=self.categoria,
            descricao='Test Transaction',
            valor=Decimal('100.00'),
            data_transacao='2025-08-21',
            tipo_transacao='entrada'
        )
        
        url = reverse('transacao-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
```

## 🚀 Deploy

### Dockerfile
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements/production.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Run migrations and start server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "gestao_financeira.wsgi:application"]
```

### Docker Compose Production
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./static:/app/static
    depends_on:
      - backend

  backend:
    build: .
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/gestao_financeira
      - DEBUG=False
      - ALLOWED_HOSTS=yourdomain.com
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: gestao_financeira
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

## 📚 Comandos Úteis

### Desenvolvimento
```bash
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Executar testes
python manage.py test

# Coletar arquivos estáticos
python manage.py collectstatic

# Shell interativo
python manage.py shell

# Executar servidor de desenvolvimento
python manage.py runserver
```

### Produção
```bash
# Build da imagem Docker
docker build -t gestao-financeira-backend .

# Executar com Docker Compose
docker-compose -f docker-compose.prod.yml up -d

# Ver logs
docker-compose logs -f backend

# Executar migrações em produção
docker-compose exec backend python manage.py migrate

# Backup do banco
docker-compose exec db pg_dump -U postgres gestao_financeira > backup.sql
```
