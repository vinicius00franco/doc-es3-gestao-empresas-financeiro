# Diagrama de Arquitetura - Gestão Financeira (MVP)

Este documento contém os diagramas de arquitetura do sistema - versão MVP.

## Arquitetura Geral do Sistema

```mermaid
graph TD
    subgraph "Ambiente Docker"
        subgraph "Backend (Django)"
            B1[Feature: Usuarios]
            B2[Feature: Transacoes]
            B3[Feature: Empresas]
            B4[Feature: Assinaturas]
            B5[Feature: Dashboard]
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

    subgraph "Backend Django"
        DJANGO[Django REST API]
        
        subgraph "Features"
            F_USER[usuarios/]
            F_TRANS[transacoes/]
            F_COMP[empresas/]
            F_DASH[dashboard/]
        end
        
        subgraph "Core"
            MIDDLEWARE[Auth Middleware]
            SERIALIZERS[Serializers]
        end
    end

    subgraph "Dados"
        POSTGRES[(PostgreSQL)]
    end

    subgraph "Externos"
        PAYMENT[Gateway Pagamento]
    end

    RN --> RN_AUTH
    RN_AUTH --> RN_API
    RN_API --> DJANGO
    
    DJANGO --> MIDDLEWARE
    MIDDLEWARE --> F_USER
    MIDDLEWARE --> F_TRANS
    MIDDLEWARE --> F_COMP
    MIDDLEWARE --> F_DASH
    
    F_USER --> SERIALIZERS
    F_TRANS --> SERIALIZERS
    F_COMP --> SERIALIZERS
    F_DASH --> SERIALIZERS
    
    SERIALIZERS --> POSTGRES
    DJANGO --> PAYMENT
    
    RN_API --> RN_STORE

    style RN fill:#61DAFB,stroke:#333,stroke-width:2px
    style DJANGO fill:#092E20,stroke:#333,stroke-width:2px,color:#FFF
    style POSTGRES fill:#336791,stroke:#333,stroke-width:2px,color:#FFF
```

## Estrutura de Features (Django)

```mermaid
graph LR
    subgraph "Feature: usuarios"
        U_MODELS[models.py]
        U_VIEWS[views.py]
        U_SERIALIZERS[serializers.py]
        U_URLS[urls.py]
    end

    subgraph "Feature: transacoes"
        T_MODELS[models.py]
        T_VIEWS[views.py]
        T_SERIALIZERS[serializers.py]
        T_URLS[urls.py]
    end

    subgraph "Feature: empresas"
        E_MODELS[models.py]
        E_VIEWS[views.py]
        E_SERIALIZERS[serializers.py]
        E_URLS[urls.py]
    end

    subgraph "Core Django"
        SETTINGS[settings.py]
        MAIN_URLS[main urls.py]
        WSGI[wsgi.py]
    end

    MAIN_URLS --> U_URLS
    MAIN_URLS --> T_URLS
    MAIN_URLS --> E_URLS

    style U_MODELS fill:#e1f5fe
    style T_MODELS fill:#e1f5fe
    style E_MODELS fill:#e1f5fe
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
    A[Usuário cria transação] --> B[Formulário de transação]
    B --> C[Validar dados]
    C --> D[Salvar no banco]
    D --> E[Notificar sucesso]

    style A fill:#e1f5fe
    style D fill:#e8f5e8
```

## Camadas de Segurança

```mermaid
graph TD
    subgraph "Segurança Completa"
        L1[1. JWT Authentication]
        L2[2. Plan Permissions]
        L3[3. Input Validation]
        L4[4. SQL Injection Protection]
        L5[5. CORS Policy]
    end

    CLIENT[Cliente] --> L1
    L1 --> L2
    L2 --> L3
    L3 --> L4
    L4 --> L5
    L5 --> API[Django API]

    style L1 fill:#f8bbd9
    style L2 fill:#ffcdd2
    style L3 fill:#e1bee7
    style L4 fill:#c8e6c9
```

## Deployment Simples

```mermaid
graph TB
    subgraph "Ambiente Docker"
        APP[Django App]
        DB[(PostgreSQL)]
    end

    USERS[Usuários] --> APP
    APP --> DB

    style APP fill:#bbdefb
    style DB fill:#c8e6c9
```
