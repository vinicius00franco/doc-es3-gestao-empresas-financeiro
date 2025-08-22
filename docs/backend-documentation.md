# Backend Documentation - Django REST Framework (MVP)

Documentação técnica do backend Django REST Framework para o sistema de gestão financeira - versão MVP.

## 🐍 Visão Geral

O backend é desenvolvido em Django REST Framework seguindo a arquitetura Feature Folder com padrão MVC, focado nas funcionalidades essenciais para o MVP.

## 🏗️ Arquitetura

### Feature Folder Structure
Cada funcionalidade possui sua própria pasta com responsabilidades bem definidas:

- **models.py**: Definição dos modelos de dados (ORM)
- **views.py**: Lógica de controle e endpoints
- **serializers.py**: Serialização/deserialização de dados
- **urls.py**: Roteamento de URLs
- **admin.py**: Interface administrativa

## 📁 Estrutura do Projeto

```
gestao_financeira/
├── gestao_financeira/          # Configurações principais
│   ├── __init__.py
│   ├── settings.py             # Configurações
│   ├── urls.py                # URLs principais
│   └── wsgi.py                # WSGI para deploy
├── core/                      # Funcionalidades centrais
│   ├── __init__.py
│   └── validators.py         # Validadores reutilizáveis
├── usuarios/                  # Feature: Gestão de usuários
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── admin.py
├── empresas/                  # Feature: Gestão de empresas
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── admin.py
├── transacoes/               # Feature: Gestão de transações
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── admin.py
├── assinaturas/             # Feature: Assinaturas
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── dashboard/               # Feature: Dashboard
│   ├── __init__.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── requirements.txt         # Dependências
├── manage.py
├── Dockerfile
└── docker-compose.yml
```

## ⚙️ Configurações

### Settings
```python
# gestao_financeira/settings.py
import os
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-mvp-key')
DEBUG = True
ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'core',
    'usuarios',
    'empresas',
    'transacoes',
    'assinaturas',
    'dashboard',
]

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# JWT Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=24),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
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

# CORS
CORS_ALLOW_ALL_ORIGINS = True
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
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
    
    def __str__(self):
        return self.nome
```

### Serializers
```python
# usuarios/serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Usuario

class UsuarioRegistroSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = Usuario
        fields = ('nome', 'email', 'senha')
    
    def create(self, validated_data):
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
from .models import Usuario
from .serializers import UsuarioRegistroSerializer, UsuarioSerializer, LoginSerializer

class RegistroView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioRegistroSerializer
    permission_classes = [AllowAny]

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
from usuarios.models import Usuario

class Empresa(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='empresas')
    razao_social = models.CharField(max_length=255)
    nome_fantasia = models.CharField(max_length=255, blank=True)
    ativa = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
    
    def __str__(self):
        return self.nome_fantasia or self.razao_social
```

### ViewSets
```python
# empresas/views.py
from rest_framework import viewsets
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
```

## 💰 Feature: Transacoes

### Models
```python
# transacoes/models.py
from django.db import models
from django.core.exceptions import ValidationError
from usuarios.models import Usuario

class Categoria(models.Model):
    TIPOS_TRANSACAO = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    ]
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='categorias')
    nome = models.CharField(max_length=100)
    tipo_transacao = models.CharField(max_length=10, choices=TIPOS_TRANSACAO)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        unique_together = ['usuario', 'nome']

class Transacao(models.Model):
    TIPOS_TRANSACAO = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    ]
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='transacoes')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data_transacao = models.DateField()
    tipo_transacao = models.CharField(max_length=10, choices=TIPOS_TRANSACAO)
    criado_em = models.DateTimeField(auto_now_add=True)
    
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

### ViewSets
```python
# transacoes/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Transacao, Categoria
from .serializers import TransacaoSerializer, CategoriaSerializer

class TransacaoViewSet(viewsets.ModelViewSet):
    serializer_class = TransacaoSerializer
    permission_classes = [IsAuthenticated, HasActiveSubscription, CheckTransactionLimits]
    
    def get_queryset(self):
        return Transacao.objects.filter(usuario=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

class CategoriaViewSet(viewsets.ModelViewSet):
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Categoria.objects.filter(usuario=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
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
    
    def __str__(self):
        return f"{self.usuario.nome} - {self.plano.nome}"
```

### Views
```python
# assinaturas/views.py
from rest_framework import viewsets, views
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Plano, Assinatura
from .serializers import PlanoSerializer, AssinaturaSerializer

class PlanoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Plano.objects.filter(ativo=True)
    serializer_class = PlanoSerializer
    permission_classes = [AllowAny]

class AssinaturaAtualView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            assinatura = request.user.assinatura
            serializer = AssinaturaSerializer(assinatura)
            return Response(serializer.data)
        except Assinatura.DoesNotExist:
            return Response({'detail': 'Nenhuma assinatura encontrada.'}, status=404)

class UpgradeView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        plano_id = request.data.get('plano_id')
        plano = Plano.objects.get(id=plano_id)
        
        # Integração com gateway de pagamento
        payment_url = f"https://payment-gateway.com/checkout/{plano_id}"
        session_id = f"cs_{plano_id}_{request.user.id}"
        
        return Response({
            'payment_url': payment_url,
            'session_id': session_id
        })
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

class CheckTransactionLimits(permissions.BasePermission):
    message = "Limite de transações atingido. Faça upgrade do seu plano."
    
    def has_permission(self, request, view):
        if request.method != 'POST':
            return True
            
        try:
            subscription = request.user.assinatura
            if subscription.plano.limite_transacoes:
                from django.utils import timezone
                from datetime import datetime
                current_month = timezone.now().month
                current_year = timezone.now().year
                
                transacoes_mes = request.user.transacoes.filter(
                    criado_em__month=current_month,
                    criado_em__year=current_year
                ).count()
                
                return transacoes_mes < subscription.plano.limite_transacoes
            return True
        except:
            return False
```

## 📈 Feature: Dashboard

### Views
```python
# dashboard/views.py
from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from transacoes.models import Transacao

class DashboardView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        transacoes = Transacao.objects.filter(usuario=request.user)
        
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
            'resumo': {
                'total_entradas': str(entradas),
                'total_saidas': str(saidas),
                'saldo': str(entradas - saidas),
                'transacoes_count': transacoes.count()
            },
            'entradas_por_categoria': entradas_por_categoria,
            'saidas_por_categoria': saidas_por_categoria
        })
```

## 🚀 Deploy Simples

### Dockerfile
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    libpq-dev

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy project
COPY . /app/

# Run server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=True
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: gestao_financeira
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres123
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
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

# Executar servidor de desenvolvimento
python manage.py runserver
```

### Docker
```bash
# Executar com Docker Compose
docker-compose up --build

# Ver logs
docker-compose logs -f backend

# Executar migrações
docker-compose exec backend python manage.py migrate
```