# Diagrama de Arquitetura - Gestão Financeira

Este documento contém os diagramas de arquitetura do sistema.

## Arquitetura Geral do Sistema

```mermaid
graph TD
    subgraph "Ambiente Docker"
        subgraph "Backend (Django)"
            B1[Feature: Usuarios]
            B2[Feature: Transacoes]
            B3[Feature: Assinaturas]
            B4[Feature: Empresas]
            B5[Feature: Relatorios]
        end
        subgraph "Banco de Dados"
            C[(PostgreSQL)]
        end
    end

    A[App Mobile (React Native)] --> B1
    A --> B2
    A --> B3
    A --> B4
    A --> B5
    B1 --> C
    B2 --> C
    B3 --> C
    B4 --> C
    B5 --> C

    style A fill:#61DAFB,stroke:#333,stroke-width:2px
    style B1 fill:#092E20,stroke:#333,stroke-width:2px,color:#FFF
    style B2 fill:#092E20,stroke:#333,stroke-width:2px,color:#FFF
    style B3 fill:#092E20,stroke:#333,stroke-width:2px,color:#FFF
    style B4 fill:#092E20,stroke:#333,stroke-width:2px,color:#FFF
    style B5 fill:#092E20,stroke:#333,stroke-width:2px,color:#FFF
```

## Arquitetura Detalhada com Fluxo de Dados

```mermaid
graph TB
    subgraph "Cliente"
        RN[React Native App]
        RN_AUTH[Auth Context]
        RN_API[API Services]
        RN_STORE[Local Storage]
    end

    subgraph "Rede"
        HTTPS[HTTPS/SSL]
        JWT[JWT Tokens]
    end

    subgraph "Backend Django"
        NGINX[Nginx (Proxy)]
        DJANGO[Django REST API]
        
        subgraph "Features"
            F_USER[usuarios/]
            F_TRANS[transacoes/]
            F_SUB[assinaturas/]
            F_COMP[empresas/]
            F_REP[relatorios/]
        end
        
        subgraph "Core"
            MIDDLEWARE[Auth Middleware]
            PERMISSIONS[Permission Classes]
            SERIALIZERS[Serializers]
        end
    end

    subgraph "Dados"
        POSTGRES[(PostgreSQL)]
        REDIS[(Redis Cache)]
    end

    subgraph "Externos"
        EMAIL[Serviço de Email]
        PAYMENT[Gateway Pagamento]
    end

    RN --> RN_AUTH
    RN_AUTH --> RN_API
    RN_API --> HTTPS
    HTTPS --> NGINX
    NGINX --> DJANGO
    
    DJANGO --> MIDDLEWARE
    MIDDLEWARE --> PERMISSIONS
    PERMISSIONS --> F_USER
    PERMISSIONS --> F_TRANS
    PERMISSIONS --> F_SUB
    PERMISSIONS --> F_COMP
    PERMISSIONS --> F_REP
    
    F_USER --> SERIALIZERS
    F_TRANS --> SERIALIZERS
    F_SUB --> SERIALIZERS
    F_COMP --> SERIALIZERS
    F_REP --> SERIALIZERS
    
    SERIALIZERS --> POSTGRES
    DJANGO --> REDIS
    DJANGO --> EMAIL
    DJANGO --> PAYMENT
    
    RN_API --> RN_STORE

    style RN fill:#61DAFB,stroke:#333,stroke-width:2px
    style DJANGO fill:#092E20,stroke:#333,stroke-width:2px,color:#FFF
    style POSTGRES fill:#336791,stroke:#333,stroke-width:2px,color:#FFF
    style REDIS fill:#DC382D,stroke:#333,stroke-width:2px,color:#FFF
```

## Estrutura de Features (Django)

```mermaid
graph LR
    subgraph "Feature: usuarios"
        U_MODELS[models.py]
        U_VIEWS[views.py]
        U_SERIALIZERS[serializers.py]
        U_URLS[urls.py]
        U_TESTS[tests.py]
    end

    subgraph "Feature: transacoes"
        T_MODELS[models.py]
        T_VIEWS[views.py]
        T_SERIALIZERS[serializers.py]
        T_URLS[urls.py]
        T_TESTS[tests.py]
    end

    subgraph "Feature: assinaturas"
        S_MODELS[models.py]
        S_VIEWS[views.py]
        S_SERIALIZERS[serializers.py]
        S_URLS[urls.py]
        S_TESTS[tests.py]
    end

    subgraph "Core Django"
        SETTINGS[settings.py]
        MAIN_URLS[main urls.py]
        WSGI[wsgi.py]
    end

    MAIN_URLS --> U_URLS
    MAIN_URLS --> T_URLS
    MAIN_URLS --> S_URLS

    style U_MODELS fill:#e1f5fe
    style T_MODELS fill:#e1f5fe
    style S_MODELS fill:#e1f5fe
```

## Arquitetura React Native (MVC)

```mermaid
graph TB
    subgraph "View Layer"
        SCREENS[Screens/]
        COMPONENTS[Components/]
        NAVIGATION[Navigation/]
    end

    subgraph "Controller Layer"
        SERVICES[Services/]
        HOOKS[Custom Hooks/]
        API[API Clients/]
    end

    subgraph "Model Layer"
        CONTEXTS[Contexts/]
        REDUCERS[Reducers/]
        STORAGE[AsyncStorage/]
    end

    SCREENS --> HOOKS
    COMPONENTS --> HOOKS
    HOOKS --> SERVICES
    SERVICES --> API
    HOOKS --> CONTEXTS
    CONTEXTS --> REDUCERS
    CONTEXTS --> STORAGE
    NAVIGATION --> SCREENS

    style SCREENS fill:#e8f5e8
    style SERVICES fill:#fff3e0
    style CONTEXTS fill:#f3e5f5
```

## Fluxo de Autenticação

```mermaid
sequenceDiagram
    participant U as Usuário
    participant A as App RN
    participant API as Django API
    participant DB as PostgreSQL

    U->>A: Login (email, senha)
    A->>API: POST /api/token/
    API->>DB: Valida credenciais
    DB-->>API: Usuário válido
    API-->>A: JWT Tokens
    A->>A: Armazena tokens
    A-->>U: Redireciona para home

    Note over A,API: Requisições subsequentes
    A->>API: Requisição + JWT Header
    API->>API: Valida JWT
    API-->>A: Resposta autorizada
```

## Fluxo de Dados das Transações

```mermaid
flowchart TD
    A[Usuário cria transação] --> B{Empresa selecionada?}
    B -->|Não| C[Selecionar empresa]
    B -->|Sim| D[Formulário de transação]
    C --> D
    D --> E[Validar dados]
    E --> F{Dentro dos limites?}
    F -->|Não| G[Erro: Upgrade necessário]
    F -->|Sim| H[Salvar no banco]
    H --> I[Atualizar cache]
    I --> J[Notificar sucesso]
    G --> K[Redirecionar para planos]

    style A fill:#e1f5fe
    style H fill:#e8f5e8
    style G fill:#ffebee
```

## Camadas de Segurança

```mermaid
graph TD
    subgraph "Segurança em Camadas"
        L1[1. HTTPS/TLS]
        L2[2. Rate Limiting]
        L3[3. JWT Authentication]
        L4[4. Permission Classes]
        L5[5. Input Validation]
        L6[6. SQL Injection Protection]
        L7[7. CORS Policy]
    end

    CLIENT[Cliente] --> L1
    L1 --> L2
    L2 --> L3
    L3 --> L4
    L4 --> L5
    L5 --> L6
    L6 --> L7
    L7 --> API[Django API]

    style L1 fill:#ffcdd2
    style L3 fill:#f8bbd9
    style L4 fill:#e1bee7
    style L6 fill:#c8e6c9
```

## Deployment Architecture

```mermaid
graph TB
    subgraph "Produção"
        LB[Load Balancer]
        
        subgraph "App Servers"
            AS1[Django Server 1]
            AS2[Django Server 2]
        end
        
        subgraph "Database"
            MASTER[(PostgreSQL Master)]
            REPLICA[(PostgreSQL Replica)]
        end
        
        subgraph "Cache & Queue"
            REDIS_CACHE[(Redis Cache)]
            REDIS_QUEUE[(Redis Queue)]
        end
        
        subgraph "Storage"
            S3[AWS S3]
        end
    end

    USERS[Usuários] --> LB
    LB --> AS1
    LB --> AS2
    AS1 --> MASTER
    AS2 --> MASTER
    AS1 --> REPLICA
    AS2 --> REPLICA
    AS1 --> REDIS_CACHE
    AS2 --> REDIS_CACHE
    AS1 --> REDIS_QUEUE
    AS2 --> REDIS_QUEUE
    AS1 --> S3
    AS2 --> S3

    style LB fill:#bbdefb
    style MASTER fill:#c8e6c9
    style REPLICA fill:#dcedc8
```

## Monitoramento e Observabilidade

```mermaid
graph LR
    subgraph "Aplicação"
        APP[Django App]
        DB[(PostgreSQL)]
        CACHE[(Redis)]
    end

    subgraph "Monitoramento"
        METRICS[Prometheus]
        LOGS[ElasticSearch]
        TRACES[Jaeger]
        ALERTS[AlertManager]
    end

    subgraph "Visualização"
        GRAFANA[Grafana]
        KIBANA[Kibana]
    end

    APP --> METRICS
    APP --> LOGS
    APP --> TRACES
    DB --> METRICS
    CACHE --> METRICS
    
    METRICS --> GRAFANA
    METRICS --> ALERTS
    LOGS --> KIBANA
    TRACES --> GRAFANA

    style APP fill:#e1f5fe
    style METRICS fill:#fff3e0
    style GRAFANA fill:#e8f5e8
```
