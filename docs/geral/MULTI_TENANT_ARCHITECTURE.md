# Arquitetura Multi-tenant (como implementada)

## Visão geral

O sistema é multi-tenant lógico: os dados são isolados por empresa (tenant) dentro do mesmo banco. O contexto do tenant é definido a partir do `application_id` informado no login e do vínculo do usuário com sua empresa padrão. O token JWT incorpora o contexto necessário para posterior identificação.

## Componentes na base de código

1) Autenticação JWT com Tenant
- Arquivo: `core/authentication.py` (TenantJWTAuthentication)
- Inclui/valida `application_id` no token e associa o usuário ao contexto de empresa

2) Middleware de Tenant
- Arquivo: `core/tenant_middleware.py`
- Após autenticação, resolve a empresa ativa do usuário e seta `request.tenant_empresa`
- Usado pelas views para filtrar QuerySets por empresa do tenant

3) Views/Serializers conscientes de tenant
- Ex.: Listagens usam `request.tenant_empresa` para filtrar
- `perform_create` injeta `empresa` no `serializer.save()` quando aplicável

4) Admin/Django Admin
- Admins usam mixins para limitar dados por empresa quando apropriado; superusers podem ver tudo

## Como o isolamento funciona

- Os modelos centrais (Transação, Categoria, Fornecedor, NotaFiscal, Agendamento, ProjecaoSaldo, Alerta, OrcamentoMensal) possuem FK para `Empresa`
- O middleware garante que as operações ocorram no escopo de `request.tenant_empresa`
- O token JWT contém `application_id` e a autenticação valida o uso correto

Observação: Não há `TenantMixin` genérico adicionando um campo `tenant_id` separado em todos os modelos nesta versão. O isolamento é obtido por FK de `empresa` + middleware + autenticação JWT.

## Fluxo (resumo)

1. Login: usuário envia `email`, `senha`, `application_id`
2. Emissão do JWT: payload inclui `application_id`
3. Requests seguintes: autenticação lê o token e o middleware define `request.tenant_empresa`
4. Views: filtram por `empresa` e ao criar registros preenchem `empresa=tenant`

Headers suportados
- Opcionalmente, `X-Application-ID` pode ser usado como fallback para identificar a aplicação (sujeito às políticas)

## Celery / Processos Periódicos por Tenant

- Tarefas periódicas (Celery Beat) disparam um dispatcher que itera empresas e agenda tarefas específicas por empresa (ex.: projeção de saldo)
- Exemplo: `apps.agenda.tasks.dispatch_gerar_projecao_saldo` agenda `gerar_projecao_saldo(empresa_id, YYYY-MM)` para cada empresa
- Alertas/Orçamentos: `apps.alertas_orcamentos.tasks.dispatch_alertas` varre alertas ativos por empresa

## Boas práticas e considerações

- Garantir que toda consulta sensível use `request.tenant_empresa`
- Validar pertencimento (categoria/fornecedor) à mesma empresa do usuário
- Auditoria e logs segregados por empresa quando aplicável
- Backups devem manter integridade referencial por `empresa_id`