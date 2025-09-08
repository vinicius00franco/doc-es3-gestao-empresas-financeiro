# Requisitos - Assinaturas

Este documento descreve os requisitos funcionais e regras de negócio para os endpoints de planos e assinaturas.

## Endpoints

### GET /api/v1/planos/
**Descrição**: Lista planos disponíveis (público).

**Regras de Negócio**:
- Apenas planos ativos são retornados.
- Inclui informações de limites e permissões.
- Ordenado por preço crescente.
 - Campo `eh_gratuito` é derivado de `preco == 0` (propriedade no model).
 - Limites por plano, por exemplo: até 4 empresas no plano Profissional (definido por `limite_empresas`).

**Resposta de Sucesso**:
```json
[
  {
    "id": 1,
    "nome": "Grátis",
    "descricao": "Plano básico gratuito",
    "preco": 0.00,
    "eh_gratuito": true,
    "limite_transacoes": 100,
  "limite_empresas": 1,
    "permite_relatorios": false,
    "permite_exportacao": false,
    "permite_notas_fiscais": false
  },
  {
    "id": 2,
    "nome": "Profissional",
    "descricao": "Plano completo para profissionais",
    "preco": 29.90,
    "eh_gratuito": false,
    "limite_transacoes": 1000,
  "limite_empresas": 4,
    "permite_relatorios": true,
    "permite_exportacao": true,
    "permite_notas_fiscais": true
  }
]
```

### GET /api/v1/assinaturas/atual/
**Descrição**: Retorna assinatura atual do usuário.

**Regras de Negócio**:
- Cria assinatura gratuita automaticamente se não existir, usando o plano com `nome='Grátis'`.
- Inclui permissões calculadas baseadas no plano.
- Verifica se limites foram excedidos.

**Resposta de Sucesso**:
```json
{
  "id": 1,
  "plano": {
    "id": 2,
    "nome": "Profissional",
    "preco": 29.90
  },
  "status": "ativa",
  "data_inicio": "2025-01-01",
  "data_fim": "2025-02-01",
  "valor_pago": 29.90,
  "pode_criar_transacao": true,
  "pode_criar_empresa": true,
  "criado_em": "2025-01-01T00:00:00Z"
}
```

### POST /api/v1/assinaturas/upgrade/
**Descrição**: Inicia upgrade de plano.

**Regras de Negócio**:
- Simula integração com gateway de pagamento.
- Retorna URL de checkout e session_id.
- Não permite upgrade para plano gratuito.
- Plano deve estar ativo.

**Validações**:
- `plano_id`: Deve existir, ser ativo e não gratuito.

**Corpo da Requisição**:
```json
{
  "plano_id": 2
}
```

**Resposta de Sucesso**:
```json
{
  "payment_url": "https://payment-gateway.com/checkout/2",
  "session_id": "cs_1640995200",
  "plano": {
    "id": 2,
    "nome": "Profissional",
    "preco": 29.90
  }
}
```

### POST /api/v1/assinaturas/confirmar-pagamento/
**Descrição**: Confirma pagamento (webhook simulado).

**Regras de Negócio**:
- Atualiza assinatura com novo plano.
- Registra valor pago e ID da transação.
- Muda status para 'ativa'.
- Define data de início como hoje.
 - Segurança do webhook deve ser implementada em produção (ex.: assinatura HMAC); atualmente não há verificação.

**Validações**:
- `session_id`: Obrigatório.
- `plano_id`: Deve existir.
- `usuario_id`: Deve existir.

**Corpo da Requisição**:
```json
{
  "session_id": "cs_1640995200",
  "plano_id": 2,
  "usuario_id": 1
}
```

**Resposta de Sucesso**:
```json
{
  "message": "Pagamento confirmado com sucesso."
}
```

## Regras Específicas

1. **Assinatura Automática**: Usuários recebem plano gratuito automaticamente.
2. **Limites por Plano**: Transações, empresas e funcionalidades limitadas por plano.
3. **Período de Assinatura**: Geralmente mensal, renovado automaticamente.
4. **Status da Assinatura**: 'ativa', 'cancelada', 'inadimplente', 'expirada'.
5. **Upgrade/Downgrade**: Apenas upgrade permitido via endpoint específico.
6. **Integração de Pagamento**: Simulada, em produção seria gateway real.
7. **Auditoria**: Todas as mudanças de plano são registradas.
