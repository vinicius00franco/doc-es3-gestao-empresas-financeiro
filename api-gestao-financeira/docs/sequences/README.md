# Diagramas de Sequência - API Gestão Financeira

Este diretório contém os diagramas de sequência para todas as rotas da API de Gestão Financeira.

## Estrutura dos Diagramas

### Autenticação
- `auth_register.puml` - Registro de usuário (POST /auth/register/)
- `auth_login.puml` - Login (POST /auth/login/)
- `auth_refresh.puml` - Refresh token (POST /auth/refresh/)

### Usuários
- `users_profile.puml` - Perfil do usuário (GET/PUT /users/profile/)
- `usuarios_config_get_update.puml` - Configurações (GET/PUT /users/configuracao/)

### Transações
- `transacoes_crud.puml` - CRUD completo de transações
- `categorias_crud.puml` - CRUD completo de categorias
- `fornecedores_crud.puml` - CRUD completo de fornecedores

### Empresas
- `empresas_crud.puml` - CRUD de empresas e definição de empresa padrão

### Assinaturas
- `assinaturas_fluxo.puml` - Fluxo completo de planos e assinaturas

### Dashboard
- `dashboard_resumo.puml` - Resumo do dashboard

### Notas Fiscais
- `notas_fiscais_upload.puml` - Upload de notas fiscais
- `notas_fiscais_status_list.puml` - Status e listagem de notas fiscais

## Convenções

- **Actor**: Cliente (usuário da API)
- **Boundary**: API (camada de entrada)
- **Control**: Views/Controllers (lógica de negócio)
- **Entity**: Serializers/Models (entidades de dados)
- **Database**: DB (persistência)
- **Queue**: Celery Task (processamento assíncrono)

## Orientação

Todos os diagramas utilizam orientação horizontal (`left to right direction`) para melhor visualização.

## Como visualizar

Use qualquer ferramenta que suporte PlantUML:
- VS Code com extensão PlantUML
- IntelliJ IDEA
- Online: http://www.plantuml.com/plantuml/