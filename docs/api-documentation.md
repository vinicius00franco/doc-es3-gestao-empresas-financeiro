# API Documentation - Gestão Financeira

Documentação completa da API REST do sistema de gestão financeira.

## Base URL
```
http://localhost:8000/api/v1/
```

## Autenticação

### JWT Authentication
Todas as rotas protegidas requerem um token JWT no header:
```
Authorization: Bearer <access_token>
```

### Endpoints de Autenticação

#### POST /auth/register/
Cadastro de novo usuário.

**Request Body:**
```json
{
  "nome": "João Silva",
  "email": "joao@email.com",
  "senha": "minhasenha123"
}
```

**Response (201):**
```json
{
  "id": 1,
  "nome": "João Silva",
  "email": "joao@email.com",
  "criado_em": "2025-08-21T10:00:00Z"
}
```

#### POST /auth/login/
Login do usuário.

**Request Body:**
```json
{
  "email": "joao@email.com",
  "senha": "minhasenha123"
}
```

**Response (200):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "nome": "João Silva",
    "email": "joao@email.com"
  }
}
```

#### POST /auth/refresh/
Renovar token de acesso.

**Request Body:**
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response (200):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### POST /auth/password-reset/
Solicitar recuperação de senha.

**Request Body:**
```json
{
  "email": "joao@email.com"
}
```

**Response (200):**
```json
{
  "message": "Se o email existir, você receberá instruções para redefinir sua senha."
}
```

## Usuários

#### GET /users/profile/
Buscar perfil do usuário autenticado.

**Headers:** `Authorization: Bearer <token>`

**Response (200):**
```json
{
  "id": 1,
  "nome": "João Silva",
  "email": "joao@email.com",
  "criado_em": "2025-08-21T10:00:00Z",
  "assinatura": {
    "plano": "Pro",
    "status": "ativa",
    "data_fim": "2025-09-21"
  }
}
```

#### PUT /users/profile/
Atualizar perfil do usuário.

**Request Body:**
```json
{
  "nome": "João Santos Silva",
  "email": "joao.santos@email.com"
}
```

**Response (200):**
```json
{
  "id": 1,
  "nome": "João Santos Silva",
  "email": "joao.santos@email.com",
  "atualizado_em": "2025-08-21T15:30:00Z"
}
```

## Empresas

#### GET /empresas/
Listar empresas do usuário.

**Response (200):**
```json
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "cnpj": "12.345.678/0001-90",
      "razao_social": "Empresa Silva LTDA",
      "nome_fantasia": "Silva Tech",
      "tipo_empresa": "LTDA",
      "ativa": true,
      "empresa_padrao": true
    },
    {
      "id": 2,
      "cnpj": "98.765.432/0001-10",
      "razao_social": "João Silva ME",
      "tipo_empresa": "ME",
      "ativa": true,
      "empresa_padrao": false
    }
  ]
}
```

#### POST /empresas/
Cadastrar nova empresa.

**Request Body:**
```json
{
  "cnpj": "11.222.333/0001-44",
  "razao_social": "Nova Empresa LTDA",
  "nome_fantasia": "Nova Tech",
  "tipo_empresa": "LTDA"
}
```

**Response (201):**
```json
{
  "id": 3,
  "cnpj": "11.222.333/0001-44",
  "razao_social": "Nova Empresa LTDA",
  "nome_fantasia": "Nova Tech",
  "tipo_empresa": "LTDA",
  "ativa": true,
  "empresa_padrao": false,
  "criado_em": "2025-08-21T16:00:00Z"
}
```

#### PUT /empresas/{id}/set-padrao/
Definir empresa como padrão.

**Response (200):**
```json
{
  "message": "Empresa definida como padrão com sucesso."
}
```

## Transações

#### GET /transacoes/
Listar transações da empresa ativa.

**Query Parameters:**
- `empresa_id`: ID da empresa (opcional, usa empresa padrão se não informado)
- `tipo`: `entrada` ou `saida`
- `categoria_id`: ID da categoria
- `data_inicio`: Data inicial (YYYY-MM-DD)
- `data_fim`: Data final (YYYY-MM-DD)
- `page`: Número da página
- `page_size`: Itens por página (padrão: 20)

**Response (200):**
```json
{
  "count": 150,
  "next": "http://localhost:8000/api/v1/transacoes/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "descricao": "Venda de produto X",
      "valor": "1500.00",
      "data_transacao": "2025-08-21",
      "tipo_transacao": "entrada",
      "status": "confirmada",
      "categoria": {
        "id": 1,
        "nome": "Vendas",
        "cor": "#4CAF50"
      },
      "forma_pagamento": "pix",
      "numero_documento": "NF-001",
      "criado_em": "2025-08-21T14:30:00Z"
    }
  ]
}
```

#### POST /transacoes/
Criar nova transação.

**Request Body:**
```json
{
  "empresa_id": 1,
  "descricao": "Pagamento fornecedor ABC",
  "valor": "800.50",
  "data_transacao": "2025-08-21",
  "tipo_transacao": "saida",
  "categoria_id": 4,
  "forma_pagamento": "transferencia",
  "numero_documento": "DOC-12345",
  "observacoes": "Pagamento à vista com desconto"
}
```

**Response (201):**
```json
{
  "id": 25,
  "empresa_id": 1,
  "descricao": "Pagamento fornecedor ABC",
  "valor": "800.50",
  "data_transacao": "2025-08-21",
  "tipo_transacao": "saida",
  "status": "confirmada",
  "categoria": {
    "id": 4,
    "nome": "Fornecedores",
    "cor": "#F44336"
  },
  "forma_pagamento": "transferencia",
  "numero_documento": "DOC-12345",
  "observacoes": "Pagamento à vista com desconto",
  "criado_em": "2025-08-21T16:45:00Z"
}
```

#### PUT /transacoes/{id}/
Atualizar transação.

**Request Body:**
```json
{
  "descricao": "Pagamento fornecedor ABC - Atualizado",
  "valor": "750.00",
  "observacoes": "Pagamento com desconto negociado"
}
```

#### DELETE /transacoes/{id}/
Excluir transação.

**Response (204):** No content

## Categorias

#### GET /categorias/
Listar categorias da empresa.

**Query Parameters:**
- `empresa_id`: ID da empresa
- `tipo_transacao`: `entrada`, `saida` ou `ambos`

**Response (200):**
```json
{
  "count": 7,
  "results": [
    {
      "id": 1,
      "nome": "Vendas",
      "descricao": "Receitas de vendas de produtos/serviços",
      "cor": "#4CAF50",
      "icone": "attach-money",
      "tipo_transacao": "entrada",
      "ativa": true,
      "categoria_padrao": true
    },
    {
      "id": 4,
      "nome": "Fornecedores",
      "descricao": "Pagamentos a fornecedores",
      "cor": "#F44336",
      "icone": "local-shipping",
      "tipo_transacao": "saida",
      "ativa": true,
      "categoria_padrao": false
    }
  ]
}
```

#### POST /categorias/
Criar nova categoria.

**Request Body:**
```json
{
  "empresa_id": 1,
  "nome": "Marketing",
  "descricao": "Gastos com marketing e publicidade",
  "cor": "#FF5722",
  "icone": "campaign",
  "tipo_transacao": "saida"
}
```

**Response (201):**
```json
{
  "id": 8,
  "nome": "Marketing",
  "descricao": "Gastos com marketing e publicidade",
  "cor": "#FF5722",
  "icone": "campaign",
  "tipo_transacao": "saida",
  "ativa": true,
  "categoria_padrao": false,
  "criado_em": "2025-08-21T17:00:00Z"
}
```

## Planos e Assinaturas

#### GET /planos/
Listar planos disponíveis.

**Response (200):**
```json
{
  "count": 3,
  "results": [
    {
      "id": 1,
      "nome": "Grátis",
      "descricao": "Plano básico para começar",
      "preco": "0.00",
      "limite_transacoes": 50,
      "limite_empresas": 1,
      "permite_relatorios": false,
      "permite_exportacao": false
    },
    {
      "id": 2,
      "nome": "Pro",
      "descricao": "Para pequenas empresas em crescimento",
      "preco": "29.90",
      "limite_transacoes": null,
      "limite_empresas": 5,
      "permite_relatorios": true,
      "permite_exportacao": true
    }
  ]
}
```

#### GET /assinaturas/atual/
Buscar assinatura atual do usuário.

**Response (200):**
```json
{
  "id": 1,
  "plano": {
    "id": 2,
    "nome": "Pro",
    "preco": "29.90"
  },
  "status": "ativa",
  "data_inicio": "2025-07-21",
  "data_fim": "2025-08-21",
  "uso_atual": {
    "transacoes_mes": 45,
    "empresas_cadastradas": 2
  }
}
```

#### POST /assinaturas/upgrade/
Fazer upgrade de plano.

**Request Body:**
```json
{
  "plano_id": 2
}
```

**Response (200):**
```json
{
  "payment_url": "https://payment-gateway.com/checkout/abc123",
  "session_id": "cs_12345"
}
```

## Relatórios

#### GET /relatorios/dashboard/
Dashboard financeiro resumido.

**Query Parameters:**
- `empresa_id`: ID da empresa
- `periodo`: `7d`, `30d`, `90d`, `1y` (padrão: 30d)

**Response (200):**
```json
{
  "periodo": "30d",
  "resumo": {
    "total_entradas": "15750.00",
    "total_saidas": "8920.50",
    "saldo": "6829.50",
    "transacoes_count": 47
  },
  "entradas_por_categoria": [
    {
      "categoria": "Vendas",
      "valor": "12500.00",
      "percentual": 79.4
    },
    {
      "categoria": "Serviços",
      "valor": "3250.00",
      "percentual": 20.6
    }
  ],
  "saidas_por_categoria": [
    {
      "categoria": "Fornecedores",
      "valor": "5200.00",
      "percentual": 58.3
    },
    {
      "categoria": "Salários",
      "valor": "2500.00",
      "percentual": 28.0
    }
  ],
  "fluxo_diario": [
    {
      "data": "2025-08-01",
      "entradas": "500.00",
      "saidas": "200.00"
    }
  ]
}
```

#### GET /relatorios/fluxo-caixa/
Relatório detalhado de fluxo de caixa.

**Query Parameters:**
- `empresa_id`: ID da empresa
- `data_inicio`: Data inicial (YYYY-MM-DD)
- `data_fim`: Data final (YYYY-MM-DD)
- `formato`: `json` ou `pdf`

**Response (200):**
```json
{
  "empresa": {
    "id": 1,
    "razao_social": "Empresa Silva LTDA"
  },
  "periodo": {
    "inicio": "2025-08-01",
    "fim": "2025-08-21"
  },
  "resumo": {
    "saldo_inicial": "5000.00",
    "total_entradas": "15750.00",
    "total_saidas": "8920.50",
    "saldo_final": "11829.50"
  },
  "transacoes": [
    {
      "data": "2025-08-21",
      "descricao": "Venda produto X",
      "categoria": "Vendas",
      "entrada": "1500.00",
      "saida": null,
      "saldo_acumulado": "11829.50"
    }
  ]
}
```

## Códigos de Erro

### 400 - Bad Request
```json
{
  "error": "validation_error",
  "message": "Dados inválidos",
  "details": {
    "valor": ["Este campo é obrigatório"],
    "email": ["Insira um endereço de email válido"]
  }
}
```

### 401 - Unauthorized
```json
{
  "error": "unauthorized",
  "message": "Token de autenticação inválido ou expirado"
}
```

### 403 - Forbidden
```json
{
  "error": "forbidden",
  "message": "Você atingiu o limite de transações do seu plano atual",
  "upgrade_required": true
}
```

### 404 - Not Found
```json
{
  "error": "not_found",
  "message": "Recurso não encontrado"
}
```

### 422 - Unprocessable Entity
```json
{
  "error": "business_rule_violation",
  "message": "Não é possível excluir categoria que possui transações vinculadas"
}
```

### 429 - Too Many Requests
```json
{
  "error": "rate_limit_exceeded",
  "message": "Muitas tentativas. Tente novamente em 60 segundos"
}
```

### 500 - Internal Server Error
```json
{
  "error": "internal_error",
  "message": "Erro interno do servidor. Nossa equipe foi notificada."
}
```

## Rate Limiting

- **Autenticação**: 5 tentativas por minuto por IP
- **APIs Gerais**: 1000 requisições por hora por usuário
- **Upload de Arquivos**: 10 uploads por minuto

## Versionamento

A API utiliza versionamento via URL:
- v1: `/api/v1/` (atual)
- Futuras versões: `/api/v2/`, `/api/v3/`, etc.

## Webhooks (Futuro)

Para integrações com gateways de pagamento:

#### POST /webhooks/payment-confirmed/
Confirmação de pagamento de assinatura.

## Paginação

Endpoints que retornam listas utilizam paginação:

```json
{
  "count": 150,
  "next": "http://localhost:8000/api/v1/transacoes/?page=3",
  "previous": "http://localhost:8000/api/v1/transacoes/?page=1",
  "results": []
}
```

## Filtros e Ordenação

Parâmetros comuns:
- `ordering`: Campo para ordenação (prefixo `-` para desc)
- `search`: Busca textual
- `limit`: Limite de resultados por página
