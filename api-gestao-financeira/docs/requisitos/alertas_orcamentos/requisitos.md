# Alertas & Orçamentos – Requisitos (Backlog)

Status: Parcial (flags de notificação existem em Configuração do Usuário), demais não implementado

## Objetivo
Alertar sobre vencimentos (NF/boletos), controle mensal de gastos (orçamentos por categoria/centro de custo) e visão rápida da saúde da empresa.

## Modelos Propostos
- Alerta: tipo (vencimento_nf, vencimento_boleto, orcamento, caixa), canal (email, push), antecedencia_dias, ativo, parametros (JSON), empresa/usuario
- OrcamentoMensal: empresa, categoria, mes (YYYY-MM), valor_planejado, valor_real (calculado), status (abaixo, dentro, acima)

## Endpoints
- GET/POST /api/v1/alertas/ — Lista/Cria alertas
- GET/PUT/DELETE /api/v1/alertas/{id}/ — Gerencia alertas
- GET/POST /api/v1/orcamentos/ — Lista/Cria orçamentos mensais
- GET/PUT/DELETE /api/v1/orcamentos/{id}/ — Gerencia orçamentos
- Dashboard: incluir KPIs (atingimento de orçamento, tendência, burn rate)

## Regras de Negócio
- Disparo de alertas por Celery Beat considerando antecedência e status
- Orçamento por categoria soma transações confirmadas no mês
- Status do orçamento calculado dinamicamente (abaixo/dentro/acima)
- Multi-tenant e por empresa

## Considerações Técnicas
- Tarefas periódicas (Celery Beat) para varrer vencimentos e orçamentos
- Logs de envio e reentrega idempotente
