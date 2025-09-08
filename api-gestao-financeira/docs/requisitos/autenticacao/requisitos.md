# Requisitos - Autenticação

Este documento descreve os requisitos funcionais e regras de negócio para os endpoints de autenticação e gerenciamento de usuários.

## Endpoints

### POST /api/v1/auth/register/
**Descrição**: Registra um novo usuário no sistema.

**Regras de Negócio**:
- Email deve ser único no sistema.
- Senha deve atender aos critérios de validação do Django (comprimento mínimo, complexidade).
- Confirmação de senha deve coincidir.
- Cria automaticamente uma configuração padrão para o usuário.

**Validações**:
- `nome`: Obrigatório, sanitizado.
- `email`: Obrigatório, formato válido, único.
- `senha`: Obrigatório, validada por `validate_password`.
- `senha_confirmacao`: Deve coincidir com senha.

**Corpo da Requisição**:
```json
{
  "nome": "João Silva",
  "email": "joao@example.com",
  "senha": "MinhaSenha123!",
  "senha_confirmacao": "MinhaSenha123!"
}
```

**Resposta de Sucesso**:
```json
{
  "id": 1,
  "nome": "João Silva",
  "email": "joao@example.com",
  "criado_em": "2025-01-01T00:00:00Z"
}
```

### POST /api/v1/auth/login/
**Descrição**: Autentica usuário e retorna tokens JWT.

**Regras de Negócio**:
- Rate limiting aplicado (escopo `login`: 5/min conforme settings).
- Usuário deve estar ativo.
- Deve ter pelo menos uma empresa cadastrada.
- Retorna tokens customizados com tenant.

**Validações**:
- `email`: Obrigatório, formato válido.
- `senha`: Obrigatório.
- `application_id`: Obrigatório (string do tenant).

**Corpo da Requisição**:
```json
{
  "email": "joao@example.com",
  "senha": "MinhaSenha123!",
  "application_id": "com.empresa1"
}
```

**Resposta de Sucesso**:
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "user": {"id": 1, "nome": "João", "email": "joao@example.com"},
  "application_id": "com.empresa1"
}
```

### POST /api/v1/auth/refresh/
**Descrição**: Renova o token de acesso usando refresh token.

**Regras de Negócio**:
- Refresh token deve ser válido.
- Retorna novo access token.

**Validações**:
- `refresh_token`: Obrigatório, válido.

**Corpo da Requisição**:
```json
{
  "refresh_token": "eyJ..."
}
```

**Resposta de Sucesso**:
```json
{
  "access_token": "eyJ..."
}
```

### GET/PUT /api/v1/users/profile/
**Descrição**: Recupera ou atualiza o perfil do usuário autenticado.

**Regras de Negócio**:
- Apenas o próprio usuário pode acessar seu perfil.
- Campos read-only: id, criado_em, atualizado_em.

**Validações**:
- Autenticação obrigatória.
 - Enviar Application ID via claim no token ou cabeçalho `X-Application-ID`.

**Resposta de Sucesso (GET)**:
```json
{
  "id": 1,
  "nome": "João Silva",
  "email": "joao@example.com",
  "criado_em": "2025-01-01T00:00:00Z",
  "atualizado_em": "2025-01-01T00:00:00Z"
}
```

### GET/PUT /api/v1/users/configuracao/
**Descrição**: Gerencia configurações do usuário.

**Regras de Negócio**:
- Configuração criada automaticamente no registro.
- Campos: tema (`claro|escuro|auto`), moeda (padrão BRL), formato_data (ex.: DD/MM/YYYY), fuso_horario, notificações, backup_automatico.

**Validações**:
- Autenticação obrigatória.
 - Enviar Application ID via claim no token ou cabeçalho `X-Application-ID`.

**Resposta de Sucesso (GET)**:
```json
{
  "tema": "light",
  "moeda": "BRL",
  "formato_data": "DD/MM/YYYY",
  "fuso_horario": "America/Sao_Paulo",
  "notificacoes_email": true,
  "notificacoes_push": false,
  "backup_automatico": true
}
```

## Regras Específicas

1. **Rate Limiting**: Aplicado no endpoint de login para prevenir ataques de força bruta.
2. **Ativação de Conta**: Usuários são criados como ativos por padrão.
3. **Configuração Automática**: Criada automaticamente no registro com valores padrão.
4. **Tokens Customizados**: Incluem `application_id` para isolamento multi-tenant.
5. **Cabeçalho Tenant**: Alternativamente usar `X-Application-ID` em requests autenticadas.
