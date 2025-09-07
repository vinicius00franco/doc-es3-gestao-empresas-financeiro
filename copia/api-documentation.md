# API Documentation - Gestão Financeira (MVP)

Documentação da API REST do sistema de gestão financeira - versão MVP.

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
  "criado_em": "2025-08-21T10:00:00Z"
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
[
  {
    "id": 1,
    "razao_social": "Empresa Silva LTDA",
    "nome_fantasia": "Silva Tech",
    "ativa": true
  }
]
```

#### POST /empresas/
Cadastrar nova empresa.

**Request Body:**
```json
{
  "razao_social": "Nova Empresa LTDA",
  "nome_fantasia": "Nova Tech"
}
```

**Response (201):**
```json
{
  "id": 2,
  "razao_social": "Nova Empresa LTDA",
  "nome_fantasia": "Nova Tech",
  "ativa": true,
  "criado_em": "2025-08-21T16:00:00Z"
}
```

## Transações

#### GET /transacoes/
Listar transações.

**Query Parameters:**
- `tipo`: `entrada` ou `saida`
- `data_inicio`: Data inicial (YYYY-MM-DD)
- `data_fim`: Data final (YYYY-MM-DD)

**Response (200):**
```json
[
  {
    "id": 1,
    "descricao": "Venda de produto X",
    "valor": "1500.00",
    "data_transacao": "2025-08-21",
    "tipo_transacao": "entrada",
    "categoria": {
      "id": 1,
      "nome": "Vendas"
    },
    "criado_em": "2025-08-21T14:30:00Z"
  }
]
```

#### POST /transacoes/
Criar nova transação.

**Request Body:**
```json
{
  "descricao": "Pagamento fornecedor ABC",
  "valor": "800.50",
  "data_transacao": "2025-08-21",
  "tipo_transacao": "saida",
  "categoria_id": 4
}
```

**Response (201):**
```json
{
  "id": 25,
  "descricao": "Pagamento fornecedor ABC",
  "valor": "800.50",
  "data_transacao": "2025-08-21",
  "tipo_transacao": "saida",
  "categoria": {
    "id": 4,
    "nome": "Fornecedores"
  },
  "criado_em": "2025-08-21T16:45:00Z"
}
```

#### PUT /transacoes/{id}/
Atualizar transação.

**Request Body:**
```json
{
  "descricao": "Pagamento fornecedor ABC - Atualizado",
  "valor": "750.00"
}
```

#### DELETE /transacoes/{id}/
Excluir transação.

**Response (204):** No content

## Categorias

#### GET /categorias/
Listar categorias.

**Response (200):**
```json
[
  {
    "id": 1,
    "nome": "Vendas",
    "tipo_transacao": "entrada"
  },
  {
    "id": 4,
    "nome": "Fornecedores",
    "tipo_transacao": "saida"
  }
]
```

#### POST /categorias/
Criar nova categoria.

**Request Body:**
```json
{
  "nome": "Marketing",
  "tipo_transacao": "saida"
}
```

**Response (201):**
```json
{
  "id": 8,
  "nome": "Marketing",
  "tipo_transacao": "saida",
  "criado_em": "2025-08-21T17:00:00Z"
}
```

## Assinaturas

#### GET /planos/
Listar planos disponíveis.

**Response (200):**
```json
[
  {
    "id": 1,
    "nome": "Grátis",
    "preco": "0.00",
    "limite_transacoes": 50
  },
  {
    "id": 2,
    "nome": "Pro",
    "preco": "29.90",
    "limite_transacoes": null
  }
]
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
  "data_fim": "2025-08-21"
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

## Notas Fiscais

#### POST /invoices/upload/
Upload de nota fiscal para processamento.

**Request:** Multipart form-data
```
file: arquivo XML ou PDF
empresa_id: ID da empresa
```

**Response (201):**
```json
{
  "id": 1,
  "status": "uploaded",
  "arquivo_original": "nfe_123.xml",
  "empresa_id": 1,
  "criado_em": "2025-08-21T10:00:00Z"
}
```

#### GET /invoices/{id}/status/
Verificar status do processamento.

**Response (200):**
```json
{
  "id": 1,
  "status": "processed",
  "dados_extraidos": {
    "cnpj_emissor": "12.345.678/0001-90",
    "razao_social": "Fornecedor ABC LTDA",
    "valor_total": "1500.00",
    "data_emissao": "2025-08-20"
  },
  "transacao_criada_id": 25
}
```

#### GET /invoices/
Listar notas fiscais processadas.

**Response (200):**
```json
[
  {
    "id": 1,
    "arquivo_original": "nfe_123.xml",
    "status": "processed",
    "fornecedor": "Fornecedor ABC LTDA",
    "valor_total": "1500.00",
    "processado_em": "2025-08-21T10:05:00Z"
  }
]
```

## Fornecedores

#### GET /fornecedores/
Listar fornecedores cadastrados.

**Response (200):**
```json
[
  {
    "id": 1,
    "cnpj": "12.345.678/0001-90",
    "razao_social": "Fornecedor ABC LTDA",
    "nome_fantasia": "ABC Tech",
    "criado_automaticamente": true,
    "total_transacoes": 5
  }
]
```

#### POST /fornecedores/
Cadastrar novo fornecedor.

**Request Body:**
```json
{
  "cnpj": "98.765.432/0001-10",
  "razao_social": "Novo Fornecedor LTDA",
  "nome_fantasia": "Novo Tech"
}
```

## Dashboard

#### GET /dashboard/
Resumo financeiro básico.

**Response (200):**
```json
{
  "resumo": {
    "total_entradas": "15750.00",
    "total_saidas": "8920.50",
    "saldo": "6829.50",
    "transacoes_count": 47,
    "notas_fiscais_processadas": 12
  },
  "entradas_por_categoria": [
    {
      "categoria": "Vendas",
      "valor": "12500.00"
    }
  ],
  "saidas_por_categoria": [
    {
      "categoria": "Fornecedores",
      "valor": "5200.00"
    }
  ],
  "processamento_fiscal": {
    "pendentes": 2,
    "processadas_mes": 8,
    "erro_processamento": 1
  }
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

### 404 - Not Found
```json
{
  "error": "not_found",
  "message": "Recurso não encontrado"
}
```

### 500 - Internal Server Error
```json
{
  "error": "internal_error",
  "message": "Erro interno do servidor"
}
```
