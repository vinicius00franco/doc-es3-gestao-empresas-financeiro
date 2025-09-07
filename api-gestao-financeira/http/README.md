# Testes HTTP da API Gestão Financeira

Esta pasta contém arquivos `.http` organizados por funcionalidade para testar todas as rotas da API.

## Como usar

1. **VS Code**: Instale a extensão "REST Client" e clique em "Send Request" acima de cada requisição
2. **IntelliJ/PyCharm**: Suporte nativo para arquivos `.http`
3. **Postman**: Importe os arquivos ou copie as requisições

## Arquivos disponíveis

- `auth.http` - Autenticação e usuários
- `empresas.http` - Gestão de empresas
- `transacoes.http` - Transações financeiras
- `categorias.http` - Categorias de transações
- `fornecedores.http` - Gestão de fornecedores
- `dashboard.http` - Dashboard e relatórios
- `notas-fiscais.http` - Upload e processamento de notas fiscais
- `assinaturas.http` - Gestão de assinaturas recorrentes
- `health.http` - Health check e métricas

## Variáveis

Substitua as seguintes variáveis pelos valores reais:

- `{{access_token}}` - Token JWT obtido no login
- `{{refresh_token}}` - Token de refresh obtido no login

## Fluxo recomendado

1. Execute o registro ou login em `auth.http`
2. Copie o `access_token` retornado
3. Substitua `{{access_token}}` nos outros arquivos
4. Teste as demais funcionalidades

## Exemplo de uso com variáveis

```http
### Login
POST http://localhost:8000/api/v1/auth/login/
Content-Type: application/json

{
  "email": "seu@email.com",
  "password": "suasenha"
}

### Usar o token retornado
GET http://localhost:8000/api/v1/empresas/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```