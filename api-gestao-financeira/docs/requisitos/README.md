# Requisitos da API - Gestão Financeira

Este documento descreve os requisitos funcionais e regras de negócio para cada endpoint da API de Gestão Financeira. A API é baseada em Django REST Framework e utiliza arquitetura multi-tenant, onde cada usuário pode gerenciar múltiplas empresas.

## Escopo do Produto

- Foco em Pessoa Jurídica (PJ) — MEI, ME, EPP, LTDA, SA; sem suporte a Pessoas Físicas (sem CPF).
- Regime tributário deve ser considerado como metadado da empresa (ex.: Simples Nacional, Lucro Presumido, Lucro Real). [Backlog]
- Meta: mínima fricção operacional e máxima automação (evitar cadastros manuais sempre que possível).

## Autenticação, Tenant e Autorização

- **JWT Tokens**: A API utiliza tokens JWT para autenticação.
- **Multi-tenant (obrigatório)**: Requests autenticadas devem enviar o Application ID do tenant via um destes meios:
	- Claim `application_id` no JWT (retornado no login), ou
	- Cabeçalho `X-Application-ID: <application_id>`
	Caso não seja informado, o middleware retorna erro 400/401. O isolamento também considera a empresa do usuário.
- **Permissões**: Endpoints públicos (registro, login, planos) não requerem autenticação. Os demais requerem `IsAuthenticated` por padrão.

## Paginação e Filtros

- **Paginação**: Padrão DRF com `page` e `page_size`. Tamanho padrão: 20 itens por página.
- **Ordenação/Busca/Filtros**: Indicados por endpoint quando suportados.

## Estrutura da Documentação

A documentação está organizada por funcionalidades em pastas separadas:

- [`autenticacao/`](./autenticacao/) - Endpoints de autenticação e gerenciamento de usuários
- [`empresas/`](./empresas/) - Gerenciamento de empresas
- [`transacoes/`](./transacoes/) - Transações, categorias e fornecedores
- [`assinaturas/`](./assinaturas/) - Planos e assinaturas
- [`dashboard/`](./dashboard/) - Relatórios e estatísticas
- [`notas_fiscais/`](./notas_fiscais/) - Upload e processamento de notas fiscais
 - [Agenda/Calendário](./agenda/) - Projeção e saldo diário por recebíveis/pagamentos programados [Backlog]
 - [Alertas & Orçamentos](./alertas_orcamentos/) - Alertas de vencimentos e controle mensal de gastos [Backlog]
 - [Automação](./automacoes/) - Regras de automação (categorização, conciliação, importação bancária) [Backlog]

## Endpoints Gerais (Infra)

- `GET /health/` — Health check simples, retorna `{ "status": "healthy" }`.
- `GET /metrics/` — Métricas Prometheus (exposto também na raiz por `django_prometheus`).

## Regras Gerais de Negócio

1. **Multi-tenant**: Todos os recursos são isolados por empresa/usuário.
2. **Empresa Padrão**: Muitos endpoints requerem empresa padrão definida.
3. **Sanitização**: Textos são sanitizados para prevenir XSS.
4. **Validações**: CNPJ formatado e validado.
5. **Assinaturas**: Limites baseados no plano ativo.
6. **Processamento Assíncrono**: Upload de notas fiscais é processado em background.
7. **Rate Limiting**: Aplicado em endpoints de autenticação.
8. **Auditoria**: Campos de auditoria (criado_em, atualizado_em) em todas as entidades.

## Metas de Automação (Visão)

- Registro automático a partir de documentos formais (NF-e/NFS-e), com mínimo de intervenção.
- Regras de automação configuráveis (por CNPJ/descrição/CFOP) para categorização e fornecedores/clientes. [Backlog]
- Importação de extratos bancários e conciliação assistida. [Backlog]
- Alertas configuráveis (vencimentos, orçamento) e visão de saúde financeira em um clique. [Backlog]

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
