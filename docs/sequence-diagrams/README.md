# Diagramas de Sequência - Sistema de Gestão Financeira

Esta pasta contém diagramas de sequência detalhados que mostram as interações entre os componentes do sistema ao longo do tempo.

## 📋 Estrutura de Pastas

### 🔐 Authentication
- **`jwt-login.puml`** — Fluxo completo de autenticação JWT
  - Login com email/senha
  - Geração de tokens (access + refresh)
  - Armazenamento seguro no app mobile
  - Tratamento de credenciais inválidas

### 👤 User Management
- **`password-reset.puml`** — Processo de recuperação de senha
  - Solicitação via email
  - Geração de token temporário
  - Validação e redefinição

### 💰 Transactions
- **`create-transaction.puml`** — Criação de nova transação
  - Carregamento de categorias
  - Validação de limites por plano
  - Persistência no banco de dados
  - Tratamento de limites excedidos

### 💳 Subscriptions
- **`plan-upgrade.puml`** — Processo de upgrade de plano
  - Seleção de novo plano
  - Integração com gateway de pagamento
  - Confirmação via webhook
  - Atualização de limites

- **`subscription-check.puml`** — Verificação de limites de assinatura
  - Validação antes de ações
  - Controle de acesso por plano
  - Sugestões de upgrade

## 🎨 Como Visualizar

### 1️⃣ **VS Code + PlantUML**
```bash
# 1. Instale a extensão PlantUML
# 2. Abra qualquer arquivo .puml
# 3. Ctrl+Shift+P → "PlantUML: Preview Current Diagram"
```

### 2️⃣ **Exportar Imagens**
```bash
# Via VS Code: Preview → Export → PNG/SVG
# Via comando (se tiver plantuml.jar):
java -jar plantuml.jar docs/sequence-diagrams/**/*.puml
```

## 🔧 Características dos Diagramas

### ✅ **Visual Profissional**
- **Tema moderno** com cores consistentes
- **Numeração automática** das interações
- **Cores distintas** para cada participante
- **Notas explicativas** em pontos importantes

### ✅ **Detalhamento Técnico**
- **Endpoints específicos** da API
- **Códigos de status HTTP** corretos
- **Tratamento de erros** completo
- **Validações de segurança** incluídas

### ✅ **Fluxos Realistas**
- **Cenários alternativos** (sucesso/erro)
- **Validações de negócio** representadas
- **Integrações externas** mapeadas
- **Estados de loading** considerados

## 📖 Guia de Leitura

### 🎯 **Participantes Padrão**
- **Usuário** (Actor) — Pessoa usando o app
- **App (React Native)** — Frontend mobile
- **API (Django REST)** — Backend servidor
- **Banco de Dados** — PostgreSQL

### 🔍 **Elementos Visuais**
- **Caixas coloridas** — Diferentes componentes
- **Setas numeradas** — Sequência de interações
- **Blocos alt/else** — Cenários condicionais
- **Notas laterais** — Explicações técnicas

### 📊 **Padrões de Fluxo**
1. **Ativação** — Componente processa requisição
2. **Validação** — Verificações de segurança/negócio
3. **Persistência** — Operações no banco
4. **Resposta** — Retorno para o usuário

## 🚀 Casos de Uso Cobertos

### 🔐 **Segurança**
- Autenticação JWT completa
- Refresh de tokens automático
- Validação de permissões
- Recuperação segura de senha

### 💼 **Negócio**
- Criação de transações com validações
- Controle de limites por plano
- Upgrade de assinaturas
- Integração com pagamentos

### 🎯 **UX/UI**
- Feedback visual de loading
- Tratamento de erros amigável
- Navegação condicional
- Estados de sucesso/erro

## 📝 Convenções Utilizadas

### 🎨 **Cores**
- **Verde claro** — Componentes frontend
- **Azul claro** — Componentes backend
- **Amarelo claro** — Banco de dados
- **Verde** — Fluxos de sucesso
- **Vermelho** — Fluxos de erro

### 🔢 **Numeração**
- **Automática** — Sequência cronológica
- **Contínua** — Através de todos os participantes
- **Reinicia** — A cada novo diagrama

### 📋 **Anotações**
- **Notas técnicas** — Detalhes de implementação
- **Regras de negócio** — Validações importantes
- **Considerações UX** — Aspectos de experiência

---
💡 **Dica:** Use estes diagramas como referência durante o desenvolvimento para garantir que todos os cenários estão cobertos.