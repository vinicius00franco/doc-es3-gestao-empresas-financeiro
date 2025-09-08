# Agenda/Calendário – Requisitos (Backlog)

Status: Não implementado

## Objetivo
Prover visão de calendário com saldo diário projetado, baseado em recebíveis e pagamentos programados (contas a pagar/receber) e recorrências.

## Modelos Propostos
- Agendamento (pagar/receber): descricao, valor, data_vencimento, recorrencia (mensal, semanal, custom), tipo (entrada/saida), status (previsto, confirmado, cancelado), fornecedor/cliente opcional, empresa, categoria opcional
- ProjecaoSaldo (opcional/materializado): data, saldo_previsto, empresa

## Endpoints
- GET /api/v1/agenda/daily-balance?month=YYYY-MM — Saldo por dia do mês
- GET /api/v1/agendamentos/ — Lista previsões (paginado, filtros por período, tipo)
- POST /api/v1/agendamentos/ — Cria agendamento
- GET/PUT/DELETE /api/v1/agendamentos/{id}/ — Gerencia agendamento

## Regras de Negócio
- Eventos recorrentes devem ser expandidos no período consultado
- Saldo diário = saldo anterior + entradas previstas - saídas previstas (considerando confirmadas e previstas de acordo com filtro)
- Integração com transações: ao confirmar pagamento/recebimento, gerar/ligar uma Transacao
- Multi-tenant e por empresa (tenant + empresa do usuário)

## Considerações Técnicas
- Celery Beat para geração/expansão de recorrências e limpeza de projeções
- Indexação por data e empresa
- Possível cache por mês/empresa
