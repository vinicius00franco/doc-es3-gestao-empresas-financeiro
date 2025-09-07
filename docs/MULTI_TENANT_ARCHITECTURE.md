# Arquitetura Multi-Tenant

## Visão Geral

Esta implementação utiliza uma arquitetura multi-tenant com backend único e particionamento de dados no mesmo banco/schema. Cada tenant é identificado pelo `application_id` enviado no login e incluído no token JWT.

## Componentes Principais

### 1. TenantMixin (`core/tenant.py`)
- Adiciona campo `tenant_id` aos modelos
- Manager personalizado que filtra automaticamente por tenant
- Thread-local storage para o tenant atual

### 2. TenantMiddleware (`core/tenant_middleware.py`)
- Identifica o tenant baseado na empresa padrão do usuário
- Define o tenant atual na thread
- Executa após autenticação

### 3. TenantViewMixin (`core/mixins.py`)
- Mixin para views que automatiza filtro por tenant
- Garante que novos objetos sejam criados no tenant correto

### 4. TenantAdminMixin (`core/admin.py`)
- Isolamento de dados no Django Admin
- Superusers podem ver todos os dados

## Modelos Atualizados

Os seguintes modelos agora herdam de `TenantMixin`:
- `Transacao`
- `Categoria` 
- `Fornecedor`

### Índices Adicionados
- `tenant_id + empresa`
- `tenant_id + data_transacao`
- `tenant_id + status`
- `tenant_id + tipo_transacao`

## Migração de Dados

Execute o comando para migrar dados existentes:

```bash
python manage.py migrate_to_tenant
```

## Funcionamento

1. **Login**: Usuário envia `email`, `senha` e `application_id`
2. **Token JWT**: Token inclui `application_id` no payload
3. **Identificação do Tenant**: Middleware extrai `application_id` do token ou cabeçalho `X-Application-ID`
4. **Validação**: Verifica se `application_id` corresponde a empresa do usuário
5. **Isolamento Automático**: Todas as consultas são filtradas por `tenant_id`
6. **Criação de Dados**: Novos registros recebem `tenant_id` automaticamente

## Exemplo de Uso

### Login
```json
{
  "email": "user@example.com",
  "senha": "password123",
  "application_id": "com.tenant1"
}
```

### Requisições Subsequentes
- **Opção 1**: Token JWT já contém `application_id`
- **Opção 2**: Cabeçalho `X-Application-ID: com.tenant1`

## Vantagens

- **Isolamento Completo**: Dados de diferentes tenants nunca se misturam
- **Performance**: Índices otimizados por tenant
- **Transparência**: Filtro automático, sem mudanças no código de negócio
- **Escalabilidade**: Mesmo banco/schema, particionamento lógico
- **Segurança**: Impossível acessar dados de outro tenant

## Considerações

- `application_id` deve ser enviado obrigatoriamente no login
- Token JWT contém `application_id` para identificação automática
- Fallback para cabeçalho `X-Application-ID` se necessário
- Erro 400/403 se `application_id` ausente ou inválido
- Cada usuário pode ter múltiplas empresas, mas apenas uma ativa por sessão
- Superusers no admin podem ver dados de todos os tenants
- Backup e restore mantêm isolamento por tenant