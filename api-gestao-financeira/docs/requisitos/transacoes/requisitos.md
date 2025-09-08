# Requisitos - Transações

Este documento descreve os requisitos funcionais e regras de negócio para os endpoints de transações, categorias e fornecedores.

## Endpoints de Transações

### GET/POST /api/v1/transacoes/
**Descrição**: Lista ou cria transações filtradas por empresa padrão.

**Regras de Negócio**:
- Filtrado por empresa padrão do usuário.
- Filtros: tipo_transacao, status, categoria, data_inicio, data_fim.
- Busca por: descricao, observacoes, numero_documento.
- Ordenação por: data_transacao, valor, criado_em.
- Status padrão: 'confirmada' para novas transações.
- Paginação padrão: 20 por página (`page`, `page_size`).

**Validações**:
- `categoria`: Deve pertencer à empresa do usuário.
- `fornecedor`: Deve pertencer à empresa do usuário (opcional).
- `descricao`: Obrigatório, sanitizado.
- `valor`: Obrigatório.
- `data_transacao`: Obrigatório. (Regra "não pode ser futura" não está implementada no código atual.)
- `tipo_transacao`: Obrigatório ('entrada' ou 'saida').
- `observacoes`: Opcional, sanitizado.
- `numero_documento`: Opcional, sanitizado.

**Corpo da Requisição (POST)**:
```json
{
  "descricao": "Pagamento fornecedor ABC",
  "valor": 1500.00,
  "data_transacao": "2025-01-15",
  "tipo_transacao": "saida",
  "status": "confirmada",
  "categoria": 1,
  "fornecedor": 1,
  "observacoes": "Pagamento mensal",
  "numero_documento": "NF-001",
  "forma_pagamento": "transferencia",
  "recorrente": false
}
```

**Resposta de Sucesso (GET)**:
```json
[
  {
    "id": 1,
    "descricao": "Pagamento fornecedor ABC",
    "valor": 1500.00,
    "valor_formatado": "R$ 1.500,00",
    "data_transacao": "2025-01-15",
    "tipo_transacao": "saida",
    "status": "confirmada",
    "categoria": 1,
    "categoria_nome": "Fornecedores",
    "fornecedor": 1,
    "fornecedor_nome": "ABC LTDA",
    "criado_em": "2025-01-15T10:00:00Z"
  }
]
```

### GET/PUT/DELETE /api/v1/transacoes/{pk}/
**Descrição**: Detalhes, atualização ou exclusão de transação específica.

**Regras de Negócio**:
- Filtrado por empresa padrão.
- Campos read-only: id, criado_em, atualizado_em.
Nota: A restrição "não pode alterar tipo_transacao" não está implementada no serializer/view; se necessária, deve ser adicionada.

## Endpoints de Categorias

### GET/POST /api/v1/categorias/
**Descrição**: Lista ou cria categorias.

**Regras de Negócio**:
- Filtrado por empresa padrão.
- Apenas categorias ativas são listadas por padrão.
- Filtro opcional por tipo_transacao.
- Busca por nome e descricao.
- Uma categoria pode ser padrão por tipo e empresa.
 - Paginação padrão: 20 por página.

**Validações**:
- `nome`: Obrigatório. (Unicidade é por `tenant_id`, empresa e nome — enforced em nível de model.)
- `tipo_transacao`: Obrigatório ('entrada' ou 'saida').
- `cor`: Opcional, formato hexadecimal.
- `descricao`: Opcional.

**Corpo da Requisição (POST)**:
```json
{
  "nome": "Alimentação",
  "descricao": "Despesas com alimentação",
  "cor": "#FF5733",
  "icone": "restaurant",
  "tipo_transacao": "saida",
  "ativa": true,
  "categoria_padrao": false
}
```

### GET/PUT/DELETE /api/v1/categorias/{pk}/
**Descrição**: Gerencia categoria específica.

**Regras de Negócio**:
- Não pode desativar categoria padrão se não houver outra ativa do mesmo tipo.

## Endpoints de Fornecedores

### GET/POST /api/v1/fornecedores/
**Descrição**: Lista ou cria fornecedores.

**Regras de Negócio**:
- Filtrado por empresa padrão.
- Apenas fornecedores ativos são listados.
- Busca por razao_social, nome_fantasia, cnpj.
- CNPJ único por empresa.
- Pode ser criado automaticamente pelo processamento de notas fiscais.
 - Paginação padrão: 20 por página.

**Validações**:
- `cnpj`: Formato válido (14 dígitos), unicidade por `tenant_id`, empresa e CNPJ.
- `razao_social`: Obrigatório, sanitizado.
- `nome_fantasia`: Opcional, sanitizado.
- `email`: Opcional, formato válido.
- `telefone`: Opcional.

**Corpo da Requisição (POST)**:
```json
{
  "cnpj": "12.345.678/0001-90",
  "razao_social": "ABC Fornecedores LTDA",
  "nome_fantasia": "ABC Corp",
  "email": "contato@abc.com",
  "telefone": "(11) 99999-9999",
  "endereco": "Rua ABC, 123",
  "ativa": true
}
```

### GET/PUT/DELETE /api/v1/fornecedores/{pk}/
**Descrição**: Gerencia fornecedor específico.

## Regras Específicas

1. **Isolamento por Empresa**: Todos os recursos são filtrados pela empresa padrão.
2. **Validações Cruzadas**: Categoria e fornecedor devem pertencer à mesma empresa.
3. **Sanitização**: Todos os campos de texto são sanitizados.
4. (Gap) Regra "data não pode ser futura" não está implementada — considere adicionar validação se for requisito.
5. **Status**: Transações podem ter status 'pendente', 'confirmada', 'cancelada'.
6. **Relacionamentos**: Transações podem não ter fornecedor (ex: salários).
