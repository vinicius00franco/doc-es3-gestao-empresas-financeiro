# Diagramas de Sequência - Processamento de Notas Fiscais

Esta pasta contém os diagramas de sequência para o sistema de processamento automático de notas fiscais.

## Fluxo Principal

1. **upload-invoice.puml** - Upload e recebimento inicial da nota fiscal
2. **extract-data.puml** - Extração de dados (XML/OCR)
3. **analyze-and-categorize.puml** - Análise e categorização dos dados
4. **error-handling.puml** - Tratamento de erros e recuperação

## Funcionalidades Cobertas

- Upload de arquivos XML (NF-e) e PDF
- Extração automática de dados fiscais
- Criação automática de empresas/fornecedores
- Geração de transações financeiras
- Categorização automática de gastos
- Tratamento de erros e retry

## Dados Extraídos

- CNPJ emissor e destinatário
- Valores totais e impostos
- Itens/serviços detalhados
- Datas de emissão e vencimento
- Chave de acesso da NF-e
- Informações de contato

## Status de Processamento

- `uploaded` - Arquivo recebido
- `processing` - Em processamento
- `processed` - Dados extraídos
- `analyzed` - Análise concluída
- `failed` - Erro no processamento