# Requisitos - Empresas

Este documento descreve os requisitos funcionais e regras de negócio para os endpoints de gerenciamento de empresas.

## Endpoints

### GET/POST /api/v1/empresas/
**Descrição**: Lista empresas do usuário ou cria nova empresa.

**Regras de Negócio**:
- Filtrado por usuário autenticado.
- CNPJ deve ser único por usuário.
- Uma empresa pode ser marcada como padrão.
- Sanitização de textos aplicada.
- Ao criar a primeira empresa do usuário, ela é marcada como padrão automaticamente (regra no model).
- Foco em PJ: somente CNPJ (não há suporte a PF/CPF).
- (Backlog) Campo `regime_tributario` para indicar, por exemplo, Simples Nacional, Lucro Presumido, Lucro Real.

**Validações**:
- `cnpj`: Formato válido (14 dígitos), único por usuário.
- `razao_social`: Obrigatório, sanitizado.
- `nome_fantasia`: Opcional, sanitizado.
- `tipo_empresa`: Obrigatório.

**Corpo da Requisição (POST)**:
```json
{
  "cnpj": "12.345.678/0001-90",
  "razao_social": "Empresa ABC LTDA",
  "nome_fantasia": "ABC Corp",
  "tipo_empresa": "LTDA",
  "ativa": true,
  "empresa_padrao": false
}
```

**Resposta de Sucesso (GET)**:
```json
[
  {
    "id": 1,
    "cnpj": "12.345.678/0001-90",
    "razao_social": "Empresa ABC LTDA",
    "nome_fantasia": "ABC Corp",
    "tipo_empresa": "LTDA",
    "ativa": true,
    "empresa_padrao": true,
    "criado_em": "2025-01-01T00:00:00Z",
    "atualizado_em": "2025-01-01T00:00:00Z"
  }
]
```

### GET/PUT/DELETE /api/v1/empresas/{pk}/
**Descrição**: Detalhes, atualização ou exclusão de empresa específica.

**Regras de Negócio**:
- Apenas empresas do usuário podem ser acessadas.
- Campos read-only: id, criado_em, atualizado_em.

Nota: As restrições de não excluir/desativar empresa padrão não estão explicitamente implementadas no código atual; se desejadas, considerar implementar validações antes de documentar como obrigatórias.

**Validações**:
- Empresa deve pertencer ao usuário.
- Não pode desativar empresa padrão se não houver outra ativa.

### POST /api/v1/empresas/{pk}/definir-padrao/
**Descrição**: Define empresa como padrão do usuário.

**Regras de Negócio**:
- Remove flag padrão das outras empresas (implementado na view/model).
- Apenas uma empresa pode ser padrão por usuário.

**Validações**:
- Empresa deve existir e pertencer ao usuário.
- Empresa deve estar ativa.

**Resposta de Sucesso**:
```json
{
  "message": "Empresa padrão definida com sucesso."
}
```

## Regras Específicas

1. **Empresa Padrão Automática**: Primeira empresa criada torna-se padrão automaticamente.
2. **CNPJ Único por Usuário**: Mesmo CNPJ pode existir para usuários diferentes.
3. (Opcional) Regras extras de exclusão/ativação podem ser definidas e implementadas se necessárias.
4. **Validação CNPJ**: Formatação automática e validação básica de formato (14 dígitos) no serializer.
5. **Sanitização**: Campos de texto sanitizados para prevenir XSS.
6. **Auditoria**: Timestamps de criação/atualização presentes.
