# Automação – Requisitos (Backlog)

Status: Parcial (processamento de NF mock; criação automática de fornecedor/transação simulada)

## Objetivo
Reduzir cadastros manuais com regras automáticas de categorização, vinculação de fornecedor/cliente, importação bancária e conciliação.

## Regras de Automação
- Por CNPJ emissor/destinatário → categoria padrão
- Por descrição/CFOP/NCM → categoria
- Mapeamento de fornecedor/cliente baseado em NF
- Deduplicação de transações (hash por valor+data+doc)

## Integrações
- Importação de extratos bancários (OFX/CSV/API bancária) [Backlog]
- Conciliação assistida entre extrato e transações [Backlog]

## Endpoints
- GET/POST /api/v1/automacoes/regras/ — Lista/Cria regras
- GET/PUT/DELETE /api/v1/automacoes/regras/{id}/ — Gerencia regras
- POST /api/v1/automacoes/concilia — Executa conciliação assistida

## Considerações Técnicas
- Execução idempotente e logs de decisão (por que categorizou assim?)
- Testes de regressão para regras
- Prioridade e sobreposição de regras
- Multi-tenant por empresa
