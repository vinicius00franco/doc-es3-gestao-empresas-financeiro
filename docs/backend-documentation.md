# Backend Documentation - Django REST Framework (MVP)

Documentação visual e técnica do backend Django REST Framework para o sistema de gestão financeira.

## 🐍 Visão Geral

Backend desenvolvido em Django REST Framework seguindo arquitetura Feature Folder com padrão MVC, focado nas funcionalidades essenciais para o MVP.

## 🏗️ Arquitetura Visual

### Estrutura Feature Folder
```mermaid
%%{init: {'flowchart': {'curve': 'linear'}}}%%
graph TB
    subgraph "GESTÃO FINANCEIRA BACKEND"
        subgraph "CORE"
            A[settings.py] --> B[urls.py]
            B --> C[wsgi.py]
        end
        
        subgraph "FEATURES"
            D[👤 usuarios/] --> E[🏢 empresas/]
            E --> F[💰 transacoes/]
            F --> G[💳 assinaturas/]
            G --> H[📊 dashboard/]
        end
        
        subgraph "SHARED"
            I[🔧 core/validators]
            J[📦 requirements.txt]
        end
    end
    
    style D fill:#E3F2FD
    style E fill:#E8F5E8
    style F fill:#FFF3E0
    style G fill:#F3E5F5
    style H fill:#FFEBEE
```

### Padrão MVC por Feature
```mermaid
%%{init: {'flowchart': {'curve': 'linear'}}}%%
graph LR
    subgraph "FEATURE STRUCTURE"
        A[📄 models.py] --> B[🎯 views.py]
        B --> C[🔄 serializers.py]
        C --> D[🛣️ urls.py]
        D --> E[⚙️ admin.py]
    end
    
    subgraph "RESPONSIBILITIES"
        F[Data Models] --> G[Business Logic]
        G --> H[Data Serialization]
        H --> I[URL Routing]
        I --> J[Admin Interface]
    end
    
    A -.-> F
    B -.-> G
    C -.-> H
    D -.-> I
    E -.-> J
```

## 📊 Modelo de Dados Visual

### Relacionamentos Principais
```mermaid
erDiagram
    USUARIO ||--o{ EMPRESA : possui
    USUARIO ||--|| ASSINATURA : tem
    USUARIO ||--o{ CATEGORIA : cria
    USUARIO ||--o{ TRANSACAO : registra
    
    EMPRESA ||--o{ TRANSACAO : contem
    CATEGORIA ||--o{ TRANSACAO : classifica
    PLANO ||--o{ ASSINATURA : define
    
    USUARIO {
        int id PK
        string nome
        string email UK
        datetime criado_em
    }
    
    EMPRESA {
        int id PK
        int usuario_id FK
        string razao_social
        string nome_fantasia
        boolean ativa
    }
    
    TRANSACAO {
        int id PK
        int usuario_id FK
        int categoria_id FK
        string descricao
        decimal valor
        date data_transacao
        string tipo_transacao
    }
    
    ASSINATURA {
        int id PK
        int usuario_id FK
        int plano_id FK
        string status
        date data_inicio
        date data_fim
    }
```

### Fluxo de Dados
```mermaid
%%{init: {'flowchart': {'curve': 'linear'}}}%%
flowchart TD
    A[📱 Mobile App] --> B[🌐 Django API]
    B --> C{🔐 JWT Auth}
    C -->|✅ Valid| D[🎯 Feature Views]
    C -->|❌ Invalid| E[🚫 401 Error]
    
    D --> F[📊 Dashboard]
    D --> G[👤 Usuarios]
    D --> H[🏢 Empresas]
    D --> I[💰 Transacoes]
    D --> J[💳 Assinaturas]
    
    F --> K[(🗄️ PostgreSQL)]
    G --> K
    H --> K
    I --> K
    J --> K
    
    style A fill:#61DAFB
    style B fill:#092E20,color:#FFF
    style K fill:#336791,color:#FFF
```

## 🔐 Sistema de Autenticação

### Fluxo JWT
```mermaid
sequenceDiagram
    participant U as 📱 User
    participant A as 🔐 Auth API
    participant D as 🗄️ Database
    
    U->>A: POST /auth/login/
    A->>D: Validate credentials
    D-->>A: User data
    A-->>U: JWT tokens
    
    Note over U,A: Subsequent requests
    U->>A: API call + JWT header
    A->>A: Validate token
    A-->>U: Protected resource
```

### Níveis de Permissão
```mermaid
%%{init: {'flowchart': {'curve': 'linear'}}}%%
graph TD
    A[🔓 Public Endpoints] --> B[📝 Register]
    A --> C[🔑 Login]
    
    D[🔒 Authenticated] --> E[👤 Profile]
    D --> F[🏢 Companies]
    D --> G[💰 Transactions]
    
    H[💎 Premium Features] --> I[📊 Advanced Reports]
    H --> J[📤 Data Export]
    
    style A fill:#E8F5E8
    style D fill:#FFF3E0
    style H fill:#F3E5F5
```

## 💳 Sistema de Assinaturas

### Planos e Limites
```mermaid
%%{init: {'flowchart': {'curve': 'linear'}}}%%
graph TB
    subgraph "PLANO GRÁTIS"
        A[50 transações/mês]
        B[1 empresa]
        C[Relatórios básicos]
    end
    
    subgraph "PLANO PRO"
        D[Transações ilimitadas]
        E[5 empresas]
        F[Relatórios avançados]
        G[Exportação dados]
    end
    
    H[👤 Usuário] --> I{Plano Atual?}
    I -->|Grátis| A
    I -->|Pro| D
    
    style A fill:#FFEBEE
    style D fill:#E8F5E8
```

### Fluxo de Upgrade
```mermaid
%%{init: {'flowchart': {'curve': 'linear'}}}%%
flowchart LR
    A[📋 Selecionar Plano] --> B[💳 Gateway Pagamento]
    B --> C[✅ Confirmação]
    C --> D[🔄 Webhook]
    D --> E[📝 Atualizar BD]
    E --> F[🎉 Plano Ativo]
    
    style A fill:#E3F2FD
    style B fill:#FFF3E0
    style F fill:#E8F5E8
```

## 📊 API Endpoints Visuais

### Estrutura de URLs
```
📍 API BASE: /api/v1/

🔐 AUTENTICAÇÃO
├── POST /auth/login/          # Login usuário
├── POST /auth/register/       # Registro
└── POST /auth/refresh/        # Refresh token

👤 USUÁRIOS
├── GET  /users/profile/       # Perfil atual
└── PUT  /users/profile/       # Atualizar perfil

🏢 EMPRESAS
├── GET  /empresas/            # Listar empresas
└── POST /empresas/            # Criar empresa

💰 TRANSAÇÕES
├── GET  /transacoes/          # Listar transações
├── POST /transacoes/          # Criar transação
├── PUT  /transacoes/{id}/     # Atualizar
└── DEL  /transacoes/{id}/     # Excluir

🏷️ CATEGORIAS
├── GET  /categorias/          # Listar categorias
└── POST /categorias/          # Criar categoria

💳 ASSINATURAS
├── GET  /planos/              # Listar planos
├── GET  /assinaturas/atual/   # Assinatura atual
└── POST /assinaturas/upgrade/ # Fazer upgrade

📊 DASHBOARD
└── GET  /dashboard/           # Dados resumo
```

### Códigos de Resposta
```mermaid
%%{init: {'flowchart': {'curve': 'linear'}}}%%
graph LR
    A[📤 Request] --> B{Processing}
    B -->|Success| C[✅ 200 OK]
    B -->|Created| D[🆕 201 Created]
    B -->|No Content| E[📭 204 No Content]
    B -->|Bad Request| F[❌ 400 Bad Request]
    B -->|Unauthorized| G[🔒 401 Unauthorized]
    B -->|Forbidden| H[🚫 403 Forbidden]
    B -->|Not Found| I[❓ 404 Not Found]
    B -->|Server Error| J[💥 500 Internal Error]
    
    style C fill:#E8F5E8
    style D fill:#E8F5E8
    style E fill:#E8F5E8
    style F fill:#FFEBEE
    style G fill:#FFEBEE
    style H fill:#FFEBEE
    style I fill:#FFEBEE
    style J fill:#FFEBEE
```

## ⚡ Performance e Otimizações

### Estratégias de Cache
```mermaid
%%{init: {'flowchart': {'curve': 'linear'}}}%%
graph TD
    A[📱 Request] --> B{Cache Hit?}
    B -->|Yes| C[⚡ Return Cached]
    B -->|No| D[🗄️ Query Database]
    D --> E[💾 Store in Cache]
    E --> F[📤 Return Response]
    
    style C fill:#E8F5E8
    style D fill:#FFF3E0
```

### Otimizações de Query
```mermaid
%%{init: {'flowchart': {'curve': 'linear'}}}%%
graph LR
    A[🔍 Query Optimization] --> B[📊 Select Related]
    A --> C[📋 Prefetch Related]
    A --> D[🎯 Only/Defer Fields]
    A --> E[📄 Pagination]
    
    style A fill:#E3F2FD
    style B fill:#E8F5E8
    style C fill:#E8F5E8
    style D fill:#E8F5E8
    style E fill:#E8F5E8
```

## 🐳 Deploy e Infraestrutura

### Arquitetura de Deploy
```mermaid
%%{init: {'flowchart': {'curve': 'linear'}}}%%
graph TB
    subgraph "DOCKER ENVIRONMENT"
        A[🐳 Django Container] --> B[🗄️ PostgreSQL Container]
        A --> C[📧 Email Service]
        A --> D[💳 Payment Gateway]
    end
    
    E[🌐 Internet] --> F[🔒 HTTPS/SSL]
    F --> A
    
    style A fill:#092E20,color:#FFF
    style B fill:#336791,color:#FFF
```

### Configuração Simples
```mermaid
%%{init: {'flowchart': {'curve': 'linear'}}}%%
flowchart LR
    A[📦 Docker Compose] --> B[🔧 Build Images]
    B --> C[🗄️ Setup Database]
    C --> D[🔄 Run Migrations]
    D --> E[🚀 Start Services]
    
    style A fill:#2496ED,color:#FFF
    style E fill:#E8F5E8
```

## 📈 Monitoramento

### Métricas Principais
```mermaid
%%{init: {'flowchart': {'curve': 'linear'}}}%%
graph TD
    A[📊 System Metrics] --> B[⏱️ Response Time]
    A --> C[💾 Memory Usage]
    A --> D[🔄 Request Rate]
    A --> E[❌ Error Rate]
    
    F[📈 Business Metrics] --> G[👥 Active Users]
    F --> H[💰 Transactions/Day]
    F --> I[💳 Subscription Rate]
    
    style A fill:#E3F2FD
    style F fill:#F3E5F5
```

### Health Check
```mermaid
stateDiagram-v2
    [*] --> Healthy
    Healthy --> Warning: High Load
    Healthy --> Critical: Service Down
    Warning --> Healthy: Load Normal
    Warning --> Critical: Overload
    Critical --> Warning: Partial Recovery
    Critical --> Healthy: Full Recovery
```

## 🔧 Comandos Úteis

### Desenvolvimento
```
🛠️ COMANDOS ESSENCIAIS

📦 Setup
├── docker-compose up --build    # Iniciar ambiente
├── python manage.py migrate     # Aplicar migrações
└── python manage.py runserver   # Servidor dev

🗄️ Database
├── python manage.py makemigrations  # Criar migrações
├── python manage.py createsuperuser # Admin user
└── python manage.py shell           # Shell interativo

🐳 Docker
├── docker-compose logs -f backend   # Ver logs
├── docker-compose exec backend bash # Acessar container
└── docker-compose down              # Parar serviços
```

## 📋 Checklist de Qualidade

### Padrões Implementados
```mermaid
%%{init: {'flowchart': {'curve': 'linear'}}}%%
graph LR
    A[✅ Code Quality] --> B[🧪 Tests]
    A --> C[📝 Documentation]
    A --> D[🔒 Security]
    A --> E[⚡ Performance]
    
    F[✅ API Standards] --> G[🌐 RESTful]
    F --> H[📊 Status Codes]
    F --> I[🔄 Pagination]
    F --> J[🔍 Filtering]
    
    style A fill:#E8F5E8
    style F fill:#E8F5E8
```

### Segurança
```mermaid
%%{init: {'flowchart': {'curve': 'linear'}}}%%
graph TD
    A[🛡️ Security Layers] --> B[🔐 JWT Authentication]
    A --> C[🔒 HTTPS/TLS]
    A --> D[🚫 CORS Policy]
    A --> E[✅ Input Validation]
    A --> F[🛡️ SQL Injection Protection]
    
    style A fill:#FFEBEE
    style B fill:#E8F5E8
    style C fill:#E8F5E8
    style D fill:#E8F5E8
    style E fill:#E8F5E8
    style F fill:#E8F5E8
```

---

💡 **Foco**: Arquitetura robusta, performance otimizada e segurança em todas as camadas do backend.