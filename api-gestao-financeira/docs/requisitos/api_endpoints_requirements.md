# Requisitos da API - Gestão Financeira

Este documento descreve os requisitos funcionais e regras de negócio para cada endpoint da API de Gestão Financeira. A API é baseada em Django REST Framework e utiliza arquitetura multi-tenant, onde cada usuário pode gerenciar múltiplas empresas.

## Autenticação e Autorização

- **JWT Tokens**: A API utiliza tokens JWT para autenticação.
- **Multi-tenant**: Todos os recursos são filtrados pela empresa padrão do usuário.
- **Permissões**: Endpoints públicos (registro, login) não requerem autenticação. Outros requerem `IsAuthenticated`.

## Endpoints por Módulo

### 1. Autenticação (Usuarios)

#### POST /api/v1/auth/register/
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

**Resposta de Sucesso**:
```json
{
  "id": 1,
  "nome": "João Silva",
  "email": "joao@example.com",
  "criado_em": "2025-01-01T00:00:00Z"
}
```

#### POST /api/v1/auth/login/
**Descrição**: Autentica usuário e retorna tokens JWT.

**Regras de Negócio**:
- Rate limiting aplicado (throttle por usuário).
- Usuário deve estar ativo.
- Deve ter pelo menos uma empresa cadastrada.
- Retorna tokens customizados com tenant.

**Validações**:
- `email`: Obrigatório, formato válido.
- `senha`: Obrigatório.
- `application_id`: Obrigatório (string do tenant).

**Resposta de Sucesso**:
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "user": {"id": 1, "nome": "João", "email": "joao@example.com"},
  "application_id": "com.empresa1"
}
```

#### POST /api/v1/auth/refresh/
**Descrição**: Renova o token de acesso usando refresh token.

**Regras de Negócio**:
- Refresh token deve ser válido.
- Retorna novo access token.

**Validações**:
- `refresh_token`: Obrigatório, válido.

#### GET/PUT /api/v1/users/profile/
**Descrição**: Recupera ou atualiza o perfil do usuário autenticado.

**Regras de Negócio**:
- Apenas o próprio usuário pode acessar seu perfil.
- Campos read-only: id, criado_em, atualizado_em.

**Validações**:
- Autenticação obrigatória.

#### GET/PUT /api/v1/users/configuracao/
**Descrição**: Gerencia configurações do usuário.

**Regras de Negócio**:
- Configuração criada automaticamente no registro.
- Campos: tema, moeda, formato_data, fuso_horario, notificações.

**Validações**:
- Autenticação obrigatória.

### 2. Empresas

#### GET/POST /api/v1/empresas/
**Descrição**: Lista empresas do usuário ou cria nova empresa.

**Regras de Negócio**:
- Filtrado por usuário autenticado.
- CNPJ deve ser único por usuário.
- Uma empresa pode ser marcada como padrão.
- Sanitização de textos aplicada.

**Validações**:
- `cnpj`: Formato válido (14 dígitos), único por usuário.
- `razao_social`: Obrigatório, sanitizado.
- `nome_fantasia`: Opcional, sanitizado.
- `tipo_empresa`: Obrigatório.

#### GET/PUT/DELETE /api/v1/empresas/{pk}/
**Descrição**: Detalhes, atualização ou exclusão de empresa específica.

**Regras de Negócio**:
- Apenas empresas do usuário podem ser acessadas.
- Não pode excluir empresa padrão se for a única.

**Validações**:
- Empresa deve pertencer ao usuário.

#### POST /api/v1/empresas/{pk}/definir-padrao/
**Descrição**: Define empresa como padrão do usuário.

**Regras de Negócio**:
- Remove flag padrão das outras empresas.
- Apenas uma empresa pode ser padrão por usuário.

**Validações**:
- Empresa deve existir e pertencer ao usuário.

### 3. Transações

#### GET/POST /api/v1/transacoes/
**Descrição**: Lista ou cria transações filtradas por empresa padrão.

**Regras de Negócio**:
- Filtrado por empresa padrão do usuário.
- Filtros: tipo_transacao, status, categoria, data_inicio, data_fim.
- Busca por: descricao, observacoes, numero_documento.
- Ordenação por: data_transacao, valor, criado_em.

**Validações**:
- `categoria`: Deve pertencer à empresa do usuário.
- `fornecedor`: Deve pertencer à empresa do usuário.
- `descricao`: Sanitizada.
- `observacoes`: Sanitizada.
- `numero_documento`: Sanitizado.

#### GET/PUT/DELETE /api/v1/transacoes/{pk}/
**Descrição**: Detalhes, atualização ou exclusão de transação específica.

**Regras de Negócio**:
- Filtrado por empresa padrão.

#### GET/POST /api/v1/categorias/
**Descrição**: Lista ou cria categorias.

**Regras de Negócio**:
- Filtrado por empresa padrão.
- Apenas categorias ativas são listadas.
- Filtro opcional por tipo_transacao.
- Busca por nome e descricao.

**Validações**:
- Criadas na empresa padrão do usuário.

#### GET/PUT/DELETE /api/v1/categorias/{pk}/
**Descrição**: Gerencia categoria específica.

#### GET/POST /api/v1/fornecedores/
**Descrição**: Lista ou cria fornecedores.

**Regras de Negócio**:
- Filtrado por empresa padrão.
- Apenas fornecedores ativos.
- Busca por razao_social, nome_fantasia, cnpj.
- CNPJ único por empresa.

**Validações**:
- `cnpj`: Formato válido, único por empresa.
- Textos sanitizados.

#### GET/PUT/DELETE /api/v1/fornecedores/{pk}/
**Descrição**: Gerencia fornecedor específico.

### 4. Assinaturas

#### GET /api/v1/planos/
**Descrição**: Lista planos disponíveis (público).

**Regras de Negócio**:
- Apenas planos ativos são retornados.
- Inclui informações de limites e permissões.

#### GET /api/v1/assinaturas/atual/
**Descrição**: Retorna assinatura atual do usuário.

**Regras de Negócio**:
- Cria assinatura gratuita automaticamente se não existir.
- Inclui permissões calculadas (pode_criar_transacao, etc.).

#### POST /api/v1/assinaturas/upgrade/
**Descrição**: Inicia upgrade de plano.

**Regras de Negócio**:
- Simula integração com gateway de pagamento.
- Retorna URL de checkout e session_id.

**Validações**:
- `plano_id`: Deve existir e ser ativo (não gratuito).

#### POST /api/v1/assinaturas/confirmar-pagamento/
**Descrição**: Confirma pagamento (webhook simulado).

**Regras de Negócio**:
- Atualiza assinatura com novo plano.
- Registra valor pago e ID da transação.

### 5. Dashboard

#### GET /api/v1/dashboard/
**Descrição**: Retorna resumo financeiro e estatísticas.

**Regras de Negócio**:
- Filtrado por empresa padrão.
- Período padrão: últimos 30 dias.
- Parâmetros opcionais: data_inicio, data_fim.
- Inclui resumo financeiro, top categorias, processamento fiscal.

**Validações**:
- Usuário deve ter empresa padrão.

### 6. Notas Fiscais

#### POST /api/v1/invoices/upload/
**Descrição**: Faz upload de nota fiscal para processamento.

**Regras de Negócio**:
- Arquivo deve ser XML ou PDF.
- Tamanho máximo: 10MB.
- Processamento assíncrono (Celery).
- Cria fornecedor automaticamente se não existir.
- Cria transação vinculada.

**Validações**:
- `file`: Extensão permitida (.xml, .pdf), tamanho <= 10MB.
- `empresa_id`: Deve pertencer ao usuário.

#### GET/PUT /api/v1/invoices/{pk}/status/
**Descrição**: Consulta status do processamento da nota fiscal.

**Regras de Negócio**:
- Filtrado por empresa do usuário.

#### GET /api/v1/invoices/
**Descrição**: Lista notas fiscais do usuário.

**Regras de Negócio**:
- Filtrado por empresa do usuário.
- Ordenado por data de criação decrescente.
- Inclui fornecedor e transação relacionada.

## Regras Gerais de Negócio

1. **Multi-tenant**: Todos os recursos são isolados por empresa/usuário.
2. **Empresa Padrão**: Muitos endpoints requerem empresa padrão definida.
3. **Sanitização**: Textos são sanitizados para prevenir XSS.
4. **Validações**: CNPJ formatado e validado.
5. **Assinaturas**: Limites baseados no plano ativo.
6. **Processamento Assíncrono**: Upload de notas fiscais é processado em background.
7. **Rate Limiting**: Aplicado em endpoints de autenticação.
8. **Auditoria**: Campos de auditoria (criado_em, atualizado_em) em todas as entidades.

## Tratamento de Erros

- **400 Bad Request**: Validações falharam.
- **401 Unauthorized**: Token inválido ou expirado.
- **403 Forbidden**: Acesso negado (recurso não pertence ao usuário).
- **404 Not Found**: Recurso não encontrado.
- **429 Too Many Requests**: Rate limit excedido.
- **500 Internal Server Error**: Erro interno do servidor.

## Considerações de Segurança

- Autenticação JWT obrigatória para endpoints protegidos.
- Validação de ownership em todos os recursos.
- Sanitização de inputs para prevenir injeções.
- Rate limiting para prevenir abuso.
- Logs de auditoria para ações críticas.
