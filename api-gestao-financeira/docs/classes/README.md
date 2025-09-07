# Diagramas de Classes - API Gestão Financeira

Este diretório contém os diagramas de classes completos para toda a arquitetura da API de Gestão Financeira.

## Estrutura dos Diagramas

### Arquitetura Completa por Módulo
- `usuarios_complete.puml` - Usuários: URLs, Views, Serializers, Models, Utils
- `empresas_complete.puml` - Empresas: URLs, Views, Serializers, Models, Utils
- `transacoes_complete.puml` - Transações: URLs, Views, Serializers, Models, Mixins, Utils
- `assinaturas_complete.puml` - Assinaturas: URLs, Views, Serializers, Models
- `notas_fiscais_complete.puml` - Notas Fiscais: URLs, Views, Serializers, Models, Tasks
- `dashboard_complete.puml` - Dashboard: URLs, Views, Models, Utils

### Arquitetura Geral
- `complete_architecture.puml` - Visão geral de toda a arquitetura
- `views_architecture.puml` - Arquitetura das views e mixins

## Características dos Diagramas

### Cobertura Completa
Cada diagrama inclui todas as classes relacionadas às rotas:
- **URLs**: Mapeamento de rotas para views
- **Views**: Controllers e funções de view
- **Serializers**: Validação e serialização de dados
- **Models**: Modelos de dados e relacionamentos
- **Mixins/Utils**: Classes auxiliares e utilitários
- **Tasks**: Processamento assíncrono (Celery)

### Multi-tenancy
Os modelos `Transacao`, `Categoria` e `Fornecedor` herdam de `TenantMixin` para suporte a multi-tenancy.

### Relacionamentos
- **Usuario** 1:N **Empresa** (um usuário pode ter várias empresas)
- **Usuario** 1:1 **ConfiguracaoUsuario** (configurações pessoais)
- **Usuario** 1:1 **Assinatura** (plano atual)
- **Empresa** 1:N **Transacao** (transações por empresa)
- **Empresa** 1:N **Categoria** (categorias por empresa)
- **Empresa** 1:N **Fornecedor** (fornecedores por empresa)

### Fluxo de Dados
Cada diagrama mostra o fluxo completo:
**URL → View → Serializer → Model**

## Orientação

Todos os diagramas utilizam orientação horizontal (`left to right direction`) para melhor visualização dos relacionamentos.

## Como visualizar

Use qualquer ferramenta que suporte PlantUML:
- VS Code com extensão PlantUML
- IntelliJ IDEA
- Online: http://www.plantuml.com/plantuml/