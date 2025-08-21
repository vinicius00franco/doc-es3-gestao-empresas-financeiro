# Gestão Financeira Simplificada (v2)

Sistema de gestão financeira com backend robusto em Django, frontend mobile em React Native e ambiente de desenvolvimento containerizado com Docker.

## 📋 Índice

- [Stack Tecnológica](#stack-tecnológica)
- [Arquitetura](#arquitetura)
- [Requisitos Funcionais](#requisitos-funcionais)
- [Requisitos Não Funcionais](#requisitos-não-funcionais)
- [Modelagem de Dados](#modelagem-de-dados)
- [Estrutura de Pastas](#estrutura-de-pastas)
- [Setup do Ambiente](#setup-do-ambiente)
- [Roadmap](#roadmap)

## 🚀 Stack Tecnológica

### Backend
- **Framework**: Django REST Framework (Python)
- **Arquitetura**: Feature Folder com padrão MVC
- **Banco de Dados**: PostgreSQL
- **Autenticação**: Token JWT (JSON Web Token)

### Frontend
- **Framework**: React Native (iOS e Android)
- **Arquitetura**: MVC adaptado para mobile

### DevOps
- **Containerização**: Docker e Docker Compose
- **Ambiente**: Desenvolvimento padronizado

## 🏗️ Arquitetura

### Feature Folder Structure
Cada funcionalidade possui sua própria pasta contendo:
- `models.py` - Modelos de dados
- `views.py` - Lógica de controle
- `serializers.py` - Serialização de dados
- `urls.py` - Roteamento
- `tests.py` - Testes unitários

### Features Principais
- **Usuarios**: Autenticação e gestão de perfil
- **Empresas**: Gestão de empresas do usuário
- **Transacoes**: Controle financeiro
- **Assinaturas**: Planos e pagamentos
- **Relatorios**: Dashboards e análises

## 📋 Requisitos Funcionais

### 2.1. Gestão de Usuários e Autenticação (Feature: Usuarios)
- **RF001**: Cadastro de usuário (nome, e-mail, senha)
- **RF002**: Login com JWT
- **RF003**: Recuperação de senha via e-mail
- **RF004**: Visualização e edição de perfil
- **RF005**: Proteção de endpoints com JWT

### 2.2. Gestão de Empresas (Feature: Empresas)
- **RF006**: Registro de empresas (MEI, ME, etc.)
- **RF007**: Seleção de empresa ativa

### 2.3. Gestão de Transações (Feature: Transacoes)
- **RF008**: CRUD de transações financeiras
- **RF009**: Campos: descrição, valor, data, tipo, categoria, status
- **RF010**: Gestão de categorias personalizadas

### 2.4. Assinaturas e Planos (Feature: Assinaturas)
- **RF011**: Diferentes níveis de planos (Grátis, Pro)
- **RF012**: Limitações do plano gratuito
- **RF013**: Funcionalidades avançadas do plano Pro
- **RF014**: Visualização e assinatura de planos
- **RF015**: Controle de acesso baseado na assinatura

### 2.5. Relatórios (Feature: Relatorios)
- **RF016**: Relatórios de fluxo de caixa e dashboard

## 🔧 Requisitos Não Funcionais

- **RNF001 (Segurança)**: 
  - Senhas com hashing (Django padrão)
  - Comunicação HTTPS
  - Validação contra SQL Injection e XSS

- **RNF002 (Desempenho)**: 
  - API < 1 segundo para operações comuns
  - App mobile rápido e fluido

- **RNF003 (Reprodutibilidade)**: 
  - Ambiente configurável com `docker-compose up`

## 🗄️ Modelagem de Dados

### Tabelas Principais

#### usuarios
```
id: integer [PK]
nome: varchar(255)
email: varchar(255) [UNIQUE]
senha_hash: varchar(255)
criado_em: timestamp
```

#### planos
```
id: integer [PK]
nome: varchar(50) [UNIQUE] // 'Grátis', 'Pro'
preco: decimal(10, 2)
limite_transacoes: integer
limite_empresas: integer
```

#### assinaturas
```
id: integer [PK]
usuario_id: integer [FK -> usuarios.id, UNIQUE]
plano_id: integer [FK -> planos.id]
status: ENUM ('ativa', 'cancelada', 'inadimplente')
data_inicio: date
data_fim: date
```

#### empresas
```
id: integer [PK]
usuario_id: integer [FK -> usuarios.id]
cnpj: varchar(18) [UNIQUE]
razao_social: varchar(255)
```

#### categorias
```
id: integer [PK]
empresa_id: integer [FK -> empresas.id]
nome: varchar(100)
tipo_transacao: ENUM ('entrada', 'saida')
```

#### transacoes
```
id: integer [PK]
empresa_id: integer [FK -> empresas.id]
categoria_id: integer [FK -> categorias.id]
descricao: varchar(255)
valor: decimal(10, 2)
data_transacao: date
tipo_transacao: ENUM ('entrada', 'saida')
```

## 📁 Estrutura de Pastas

### Backend (Django - Feature Folder)
```
gestao_financeira/
├── transacoes/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── tests.py
├── usuarios/
│   ├── models.py
│   └── ...
├── assinaturas/
│   ├── models.py
│   └── ...
├── empresas/
│   ├── models.py
│   └── ...
├── relatorios/
│   ├── models.py
│   └── ...
├── gestao_financeira/
│   ├── settings.py
│   └── urls.py
└── manage.py
```

### Frontend (React Native)
```
mobile_app/
├── src/
│   ├── assets/
│   ├── components/      # Componentes reutilizáveis
│   ├── screens/         # Telas da aplicação (MVC - View)
│   │   ├── Login/
│   │   │   ├── index.js
│   │   │   └── styles.js
│   │   ├── Cadastro/
│   │   └── ...
│   ├── services/        # Lógica de API (MVC - Controller)
│   ├── contexts/        # Gerenciamento de estado (MVC - Model)
│   └── navigation/      # Roteamento de telas
└── App.js
```

## 🐳 Setup do Ambiente

### Pré-requisitos
- Docker
- Docker Compose

### Inicialização
```bash
# Clone o repositório
git clone <repo-url>
cd gestao_financeira

# Suba o ambiente
docker-compose up --build

# O backend estará disponível em: http://localhost:8000
# O banco PostgreSQL estará na porta: 5432
```

## 🗺️ Roadmap

### Fase 1: Setup do Ambiente
- [x] Configuração Docker/Docker Compose
- [ ] Dockerfile para Django
- [ ] Configuração PostgreSQL

### Fase 2: Backend (Django)
- [ ] Feature: Usuarios (Autenticação JWT)
- [ ] Feature: Empresas (CRUD)
- [ ] Feature: Transacoes (CRUD + Categorias)
- [ ] Feature: Assinaturas (Planos + Controle de Acesso)
- [ ] Feature: Relatorios (Dashboards)

### Fase 3: Frontend (React Native)
- [ ] Setup React Native
- [ ] Telas de Autenticação
- [ ] Navegação e Componentes
- [ ] Integração com API
- [ ] Telas de Gestão Financeira

### Fase 4: Integração e Deploy
- [ ] Testes End-to-End
- [ ] CI/CD Pipeline
- [ ] Deploy Production

## 📊 Diagramas

### Fluxo de Autenticação JWT
```
Usuário → App Mobile → API Django → PostgreSQL
                ↓
            Gera JWT Token
                ↓
        Armazena Token Seguro
                ↓
        Acesso Autenticado
```

### Arquitetura de Alto Nível
```
[App Mobile React Native] 
        ↓ HTTP/JSON
[API Django REST Framework]
        ↓ SQL
[PostgreSQL Database]
```

## 🔐 Segurança

- Senhas hasheadas com bcrypt
- Tokens JWT com expiração
- Validação de entrada rigorosa
- HTTPS obrigatório em produção
- Rate limiting nos endpoints

## 📈 Métricas de Sucesso

- Tempo de resposta API < 1s
- Uptime > 99.5%
- Carregamento do app < 3s
- Zero vulnerabilidades críticas

---

**Versão**: 2.0  
**Data**: Agosto 2025  
**Autor**: Equipe de Desenvolvimento
