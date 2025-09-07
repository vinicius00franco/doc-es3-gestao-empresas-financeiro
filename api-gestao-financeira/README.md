# API Gestão Financeira - Django REST Framework

API REST robusta para sistema de gestão financeira empresarial, desenvolvida seguindo as melhores práticas do Django REST Framework.

## 🚀 Funcionalidades

### 🔐 Autenticação JWT
- Registro e login de usuários
- Tokens JWT com refresh automático
- Perfil de usuário personalizável

### 🏢 Gestão de Empresas
- CRUD completo de empresas
- Múltiplas empresas por usuário
- Validação de CNPJ

### 💰 Transações Financeiras
- Entradas e saídas
- Categorização automática
- Filtros avançados por data, tipo, categoria
- Busca por descrição e documento

### 💳 Sistema de Assinaturas
- Planos Grátis e Pro
- Controle de limites por plano
- Simulação de gateway de pagamento

### 📄 Processamento de Notas Fiscais
- Upload de arquivos XML e PDF
- Extração automática de dados
- Criação automática de fornecedores
- Integração com transações

### 📊 Dashboard
- Resumo financeiro por período
- Gráficos por categoria
- Métricas de processamento fiscal

## 🏗️ Arquitetura

### Feature Folder Structure
```
apps/
├── usuarios/          # Autenticação e perfil
├── empresas/          # Gestão de empresas
├── transacoes/        # Transações e categorias
├── assinaturas/       # Planos e assinaturas
├── dashboard/         # Relatórios e métricas
└── notas_fiscais/     # Processamento de NF-e
```

### Tecnologias
- **Django 4.2** + **Django REST Framework 3.14**
- **PostgreSQL** - Banco de dados
- **JWT Authentication** - Segurança
- **Docker** - Containerização
- **Redis** - Cache (futuro)

## 🛠️ Setup do Projeto

### 1. Clonar e Configurar
```bash
# Copiar variáveis de ambiente
cp .env.example .env.local

# Editar .env.local com suas configurações
```

### 2. Desenvolvimento com Load Balancer
```bash
# Iniciar ambiente completo (Nginx + 2 Django + Celery)
docker-compose up --build

# Aplicar migrações
docker-compose exec web1 python manage.py migrate

# Criar superusuário
docker-compose exec web1 python manage.py createsuperuser

# Criar dados iniciais
docker-compose exec web1 python manage.py shell < setup.py
```

## 🔧 Como Funciona para o Desenvolvedor

### **Fluxo de Requisições**
```
Desenvolvedor → http://localhost (Nginx) → web1 ou web2 (Django) → Resposta
```

### **⚠️ Cuidados com Load Balancer**

#### **1. Sessões e Estado**
```python
# ❌ PROBLEMA: Dados em memória local
user_cache = {}  # Perdido se requisição vai para outra instância

# ✅ SOLUÇÃO: Use Redis ou banco
from django.core.cache import cache
cache.set('user_data', data, 300)
```

#### **2. Arquivos Temporários**
```python
# ❌ PROBLEMA: Arquivo salvo apenas em uma instância
with open('/tmp/temp_file.txt', 'w') as f:
    f.write(data)

# ✅ SOLUÇÃO: Use volume compartilhado ou Redis
import tempfile
with tempfile.NamedTemporaryFile(dir='/app/media/temp') as f:
    f.write(data)
```

#### **3. Variáveis Globais**
```python
# ❌ PROBLEMA: Contador local por instância
request_count = 0

# ✅ SOLUÇÃO: Use Redis para dados compartilhados
from django.core.cache import cache
cache.set('request_count', cache.get('request_count', 0) + 1)
```

### **🛠️ Comandos de Desenvolvimento**

```bash
# Iniciar ambiente completo
docker-compose up --build

# Acessar apenas uma instância (bypass load balancer)
curl http://localhost:8000/api/v1/auth/login/  # web1 direto

# Acessar via load balancer
curl http://localhost/api/v1/auth/login/  # Nginx distribui

# Escalar instâncias
docker-compose up --scale web1=1 --scale web2=3

# Parar uma instância para teste
docker-compose stop web2
```

### **📊 Monitoramento**

```bash
# Health checks
curl http://localhost/health/  # Via Nginx
curl http://localhost:8000/health/  # web1 direto

# Status dos containers
docker-compose ps

# Logs em tempo real
docker-compose logs -f nginx web1 web2 celery

# Debug específico
docker-compose logs -f web1  # Só uma instância
```

### **🔄 Hot Reload**

- **Mudanças no código** → Refletidas instantaneamente
- **Novas dependências** → Precisa rebuild: `docker-compose up --build`
- **Mudanças no settings** → Restart automático do Django
- **Arquivos estáticos** → Servidos pelo Nginx via volume

### 3. Instalação Local
```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar banco PostgreSQL
# Editar .env com credenciais do banco

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver
```

## 📋 Dados Iniciais

### Criar Planos de Assinatura
```python
# No shell do Django (python manage.py shell)
from apps.assinaturas.models import Plano

# Plano Grátis
Plano.objects.create(
    nome='Grátis',
    descricao='Plano básico gratuito',
    preco=0.00,
    limite_transacoes=50,
    limite_empresas=1,
    permite_relatorios=False,
    permite_exportacao=False,
    permite_notas_fiscais=False
)

# Plano Pro
Plano.objects.create(
    nome='Pro',
    descricao='Plano profissional completo',
    preco=29.90,
    limite_transacoes=None,  # Ilimitado
    limite_empresas=5,
    permite_relatorios=True,
    permite_exportacao=True,
    permite_notas_fiscais=True
)
```

## 🌐 Endpoints da API

### Base URL: `http://localhost:8000/api/v1/`

### Autenticação
- `POST /auth/register/` - Registro
- `POST /auth/login/` - Login
- `POST /auth/refresh/` - Refresh token

### Usuários
- `GET /users/profile/` - Perfil atual
- `PUT /users/profile/` - Atualizar perfil

### Empresas
- `GET /empresas/` - Listar empresas
- `POST /empresas/` - Criar empresa

### Transações
- `GET /transacoes/` - Listar transações
- `POST /transacoes/` - Criar transação
- `GET /categorias/` - Listar categorias

### Assinaturas
- `GET /planos/` - Listar planos
- `GET /assinaturas/atual/` - Assinatura atual
- `POST /assinaturas/upgrade/` - Upgrade de plano

### Dashboard
- `GET /dashboard/` - Resumo financeiro

### Notas Fiscais
- `POST /invoices/upload/` - Upload NF-e
- `GET /invoices/{id}/status/` - Status processamento
- `GET /invoices/` - Listar processadas

## 🔒 Autenticação

Todas as rotas protegidas requerem header:
```
Authorization: Bearer <access_token>
```

## 📊 Filtros e Busca

### Transações
```
GET /api/v1/transacoes/?tipo_transacao=entrada
GET /api/v1/transacoes/?data_inicio=2025-01-01&data_fim=2025-01-31
GET /api/v1/transacoes/?search=fornecedor
```

### Dashboard
```
GET /api/v1/dashboard/?data_inicio=2025-01-01&data_fim=2025-01-31
```

## 🧪 Testes

```bash
# Executar testes
python manage.py test

# Com coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## 📝 Comandos Úteis

```bash
# Migrations
python manage.py makemigrations
python manage.py migrate

# Shell interativo
python manage.py shell

# Coletar arquivos estáticos
python manage.py collectstatic

# Logs do Docker
docker-compose logs -f web
```

## 🔧 Configurações de Produção

### Variáveis de Ambiente Importantes
```env
DEBUG=False
SECRET_KEY=your-super-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_HOST=your-db-host
DB_PASSWORD=your-secure-password
```

### Segurança
- JWT tokens com expiração configurável
- CORS configurado para domínios específicos
- Validação de entrada em todos os endpoints
- Proteção contra SQL injection (Django ORM)

## 📈 Performance

- Queries otimizadas com `select_related` e `prefetch_related`
- Paginação automática (20 itens por página)
- Índices de banco configurados nos models
- Cache Redis preparado para implementação

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

---

💡 **Dica**: Consulte a documentação completa em `/docs/` para diagramas de arquitetura e especificações detalhadas da API.