# Requisitos - Dashboard

Este documento descreve os requisitos funcionais e regras de negócio para o endpoint de dashboard e relatórios.

## Endpoints

### GET /api/v1/dashboard/
**Descrição**: Retorna resumo financeiro e estatísticas do usuário.

**Regras de Negócio**:
- Filtrado por empresa padrão do usuário.
- Período padrão: últimos 30 dias.
- Parâmetros opcionais: data_inicio, data_fim.
- Inclui resumo financeiro, top categorias, processamento fiscal.
- Apenas transações com status 'confirmada' são consideradas.
 - Valores retornados como strings com duas casas decimais.

**Parâmetros de Query**:
- `data_inicio`: Data inicial (formato YYYY-MM-DD)
- `data_fim`: Data final (formato YYYY-MM-DD)

**Validações**:
- Usuário deve ter empresa padrão definida.
- Datas devem ser válidas e data_fim >= data_inicio.
 - Datas são parseadas com tolerância; valores inválidos são ignorados.

**Resposta de Sucesso**:
```json
{
  "periodo": {
    "data_inicio": "2024-12-09",
    "data_fim": "2025-01-08"
  },
  "resumo": {
    "total_entradas": "15000.00",
    "total_saidas": "12000.00",
    "saldo": "3000.00",
    "transacoes_count": 45,
    "notas_fiscais_processadas": 12
  },
  "entradas_por_categoria": [
    {
      "categoria": "Vendas",
      "valor": "10000.00"
    },
    {
      "categoria": "Serviços",
      "valor": "5000.00"
    }
  ],
  "saidas_por_categoria": [
    {
      "categoria": "Fornecedores",
      "valor": "8000.00"
    },
    {
      "categoria": "Salários",
      "valor": "4000.00"
    }
  ],
  "processamento_fiscal": {
    "pendentes": 2,
    "processadas_mes": 12,
    "erro_processamento": 1
  }
}
```

## Regras Específicas

1. **Empresa Padrão Obrigatória**: Dashboard só funciona com empresa padrão definida.
2. **Status das Transações**: Apenas transações 'confirmadas' são incluídas nos cálculos.
3. **Período Dinâmico**: Padrão 30 dias, mas customizável via parâmetros.
4. **Limitação de Resultados**: Top 5 categorias por tipo para evitar resposta muito grande.
5. **Formatação de Valores**: Strings com duas casas decimais (sem símbolo de moeda).
6. **Processamento Fiscal**: Integração com módulo de notas fiscais (se disponível).
7. **Performance**: Cálculos otimizados com agregações do banco de dados.
8. **Cache**: Em produção, resultados poderiam ser cacheados por período.

## Cálculos Realizados

### Resumo Financeiro
- **Total Entradas**: Soma de todas as transações de entrada no período
- **Total Saídas**: Soma de todas as transações de saída no período
- **Saldo**: Entradas - Saídas
- **Contador de Transações**: Número total de transações no período

### Top Categorias
- **Entradas por Categoria**: Top 5 categorias de entrada por valor total
- **Saídas por Categoria**: Top 5 categorias de saída por valor total
- Agrupamento por nome da categoria
- Valores decrescentes

### Processamento Fiscal
- **Pendentes**: Notas fiscais aguardando processamento
- **Processadas no Mês**: Notas fiscais processadas com sucesso
- **Erro de Processamento**: Notas fiscais com falha no processamento

## Considerações Técnicas

1. **Filtros de Segurança**: Todas as consultas são filtradas por empresa do usuário.
2. **Validação de Datas**: Parsing seguro de datas com tratamento de erros.
3. **Limites de Período**: Não há limite rígido no código atual; considerar implementar se necessário.
4. **Formatação Consistente**: Valores sempre formatados da mesma forma.
5. **Fallback para Notas Fiscais**: Se o módulo não estiver disponível, retorna zeros.
