# Requisitos - Notas Fiscais

Este documento descreve os requisitos funcionais e regras de negócio para os endpoints de upload e processamento de notas fiscais.

## Endpoints

### POST /api/v1/invoices/upload/
**Descrição**: Faz upload de nota fiscal para processamento.

**Regras de Negócio**:
- Arquivo deve ser XML ou PDF.
- Tamanho máximo: 10MB.
- Processamento assíncrono via Celery.
- Cria fornecedor automaticamente se não existir.
- Cria transação vinculada automaticamente.
- Status inicial: 'uploaded'.
- (Backlog) Diferenciar NF de entrada (compras) e NF/NFS-e de saída (vendas/serviços) para gerar saídas e entradas.
- (Backlog) Regras de mapeamento automático para categoria/fornecedor/cliente por CNPJ/CFOP.

**Validações**:
- `file`: Extensão permitida (.xml, .pdf), tamanho <= 10MB.
- `empresa_id`: Deve pertencer ao usuário e estar ativa.

**Corpo da Requisição**:
```
Content-Type: multipart/form-data
file: <arquivo>
empresa_id: 1
```

**Resposta de Sucesso**:
```json
{
  "id": 1,
  "status": "uploaded",
  "arquivo_original": "nfe_001.xml",
  "empresa_id": 1,
  "criado_em": "2025-01-08T10:00:00Z"
}
```

### GET /api/v1/invoices/{pk}/status/
**Descrição**: Consulta status do processamento da nota fiscal.

**Regras de Negócio**:
- Filtrado por empresa do usuário.
- Status possíveis: 'uploaded', 'processing', 'processed', 'failed'.
- Inclui dados extraídos quando processado com sucesso.

**Resposta de Sucesso**:
```json
{
  "id": 1,
  "status": "processed",
  "dados_extraidos": {
    "cnpj_emissor": "12.345.678/0001-90",
    "razao_social": "ABC LTDA",
    "valor_total": "1500.00",
    "data_emissao": "2025-01-08"
  },
  "transacao": 123,
  "erro_processamento": null,
  "processado_em": "2025-01-08T10:05:00Z"
}
```

### GET /api/v1/invoices/
**Descrição**: Lista notas fiscais do usuário.

**Regras de Negócio**:
- Filtrado por empresa do usuário.
- Ordenado por data de criação decrescente.
- Inclui fornecedor e transação relacionada.
 - Paginação padrão (20 por página).

**Parâmetros de Query**:
- `status`: Filtrar por status
- `data_inicio`: Data inicial
- `data_fim`: Data final

**Resposta de Sucesso**:
```json
[
  {
    "id": 1,
    "arquivo_original": "nfe_001.xml",
    "tipo_arquivo": "XML",
    "status": "processed",
    "chave_acesso": "12345678901234567890123456789012345678901234",
    "cnpj_emissor": "12.345.678/0001-90",
    "razao_social_emissor": "ABC LTDA",
    "valor_total": "1500.00",
    "data_emissao": "2025-01-08",
    "fornecedor": {
      "id": 1,
      "razao_social": "ABC LTDA",
      "cnpj": "12.345.678/0001-90"
    },
  "transacao": 123,
    "erro_processamento": null,
    "criado_em": "2025-01-08T10:00:00Z",
    "processado_em": "2025-01-08T10:05:00Z"
  }
]
```

Observação: o campo `transacao` é um ID (inteiro) da transação relacionada; já `fornecedor` é retornado expandido.

## Processo de Upload e Processamento

### 1. Upload
1. Usuário faz upload do arquivo (XML/PDF)
2. Sistema valida arquivo e empresa
3. Cria registro de NotaFiscal com status 'uploaded'
4. Dispara tarefa assíncrona de processamento (na view; no serializer há comentário de como seria)

### 2. Processamento (Assíncrono)
1. Status muda para 'processing'
2. Extração de dados do arquivo (simulado no mock):
   - XML: Parsing direto
   - PDF: OCR + parsing (simulado)
3. Validação dos dados extraídos
4. Criação/atualização de fornecedor
5. Criação de transação vinculada
6. Status final: 'processed' ou 'failed'

### 3. Criação Automática de Recursos
- **Fornecedor**: Criado se CNPJ não existir para a empresa
- **Transação**: Sempre criada com categoria padrão de saída
- **Vinculação**: Nota fiscal vinculada à transação criada

## Regras Específicas

1. **Formatos Suportados**: Apenas XML e PDF.
2. **Limite de Tamanho**: 10MB por arquivo.
3. **Processamento Assíncrono**: Não bloqueia a resposta da API.
4. **Criação de Fornecedor**: Automática baseada nos dados da NF-e.
5. **Categoria Padrão**: Usada quando não há categoria específica.
6. **Validação de Empresa**: Arquivo só pode ser processado para empresas do usuário.
7. **Auditoria Completa**: Todos os passos são registrados com timestamps.
8. **Tratamento de Erros**: Falhas são registradas e podem ser consultadas.

## Campos Extraídos (XML)

- `chave_acesso`: Chave de acesso da NF-e
- `cnpj_emissor`: CNPJ do emitente
- `razao_social_emissor`: Razão social do emitente
- `valor_total`: Valor total da nota
- `data_emissao`: Data de emissão
- `numero_documento`: Número da nota

## Considerações Técnicas

1. **Armazenamento**: Arquivos salvos no sistema de arquivos ou cloud storage.
2. **Celery**: Processamento em background para não bloquear requests.
3. **Fallback**: Se processamento falhar, status 'failed' com mensagem de erro.
4. **Reprocessamento**: Possibilidade de reprocessar notas com falha.
5. **Limpeza**: Arquivos temporários removidos após processamento.
6. **Segurança**: Validação rigorosa de arquivos para prevenir uploads maliciosos.
7. **Tenant**: Enviar `application_id` no token ou `X-Application-ID`.
