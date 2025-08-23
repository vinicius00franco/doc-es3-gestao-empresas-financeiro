# Documentação - Sistema de Gestão Financeira

Documentação técnica completa do sistema de gestão financeira desenvolvido com Django REST Framework (backend) e React Native (frontend).

## 📋 Estrutura da Documentação

### 📊 **Diagramas Técnicos**
- **`diagrams/`** — Diagramas estruturais e de análise
  - IDEF0 (Níveis 0 e 1) — Análise funcional
  - DFD — Fluxo de dados detalhado
  - Use Case — Casos de uso completos
- **`sequence-diagrams/`** — Diagramas de sequência por módulo
  - Authentication — Fluxos de login/JWT
  - Transactions — Criação e validação
  - Subscriptions — Upgrades e limites
  - User Management — Recuperação de senha

### 📖 **Documentação Técnica**
- **`api-documentation.md`** — Especificação completa da API REST
- **`backend-documentation.md`** — Arquitetura Django e implementação
- **`frontend-documentation.md`** — Estrutura React Native e componentes
- **`architecture-diagrams.md`** — Diagramas de arquitetura (Mermaid)
- **`database-model.dbml`** — Modelo de dados e relacionamentos
- **`sequence-diagrams.md`** — Documentação dos fluxos de sequência

## 🎯 Stack Tecnológica

### 🔧 **Backend**
- **Django REST Framework** — API REST robusta
- **PostgreSQL** — Banco de dados relacional
- **JWT Authentication** — Autenticação segura
- **Docker** — Containerização

### 📱 **Frontend**
- **React Native** — App mobile multiplataforma
- **Context API** — Gerenciamento de estado
- **AsyncStorage** — Persistência local
- **Axios** — Cliente HTTP

### 🏗️ **Arquitetura**
- **Feature Folder** — Organização por funcionalidades
- **MVC Pattern** — Separação de responsabilidades
- **RESTful API** — Padrões de comunicação
- **JWT Tokens** — Segurança stateless

## 🚀 Funcionalidades Principais

### 👤 **Gestão de Usuários**
- Registro e autenticação
- Perfil de usuário
- Recuperação de senha
- Tokens JWT com refresh

### 🏢 **Gestão de Empresas**
- CRUD de empresas
- Múltiplas empresas por usuário
- Validação de dados

### 💰 **Gestão Financeira**
- Transações (entrada/saída)
- Categorização automática
- Filtros e busca
- Validações de negócio

### 💳 **Sistema de Assinaturas**
- Planos Grátis e Pro
- Limites por plano
- Gateway de pagamento
- Upgrade automático

### 📊 **Relatórios e Dashboard**
- Resumo financeiro
- Gráficos por categoria
- Filtros por período
- Exportação de dados

## 📖 Como Usar Esta Documentação

### 🎯 **Para Desenvolvedores**
1. **Comece com** `architecture-diagrams.md` — Visão geral
2. **Backend:** `backend-documentation.md` + `api-documentation.md`
3. **Frontend:** `frontend-documentation.md`
4. **Banco:** `database-model.dbml`

### 🔍 **Para Analistas**
1. **Requisitos:** `diagrams/use-case.puml`
2. **Processos:** `diagrams/idef0-*.puml`
3. **Dados:** `diagrams/dfd.puml`
4. **Fluxos:** `sequence-diagrams/`

### 🎨 **Para Designers**
1. **UX Flows:** `sequence-diagrams/`
2. **Componentes:** `frontend-documentation.md`
3. **Estados:** Diagramas de sequência

## 🔧 Ferramentas Necessárias

### 📊 **Para Visualizar Diagramas**
- **VS Code** + Extensão PlantUML
- **Extensão Mermaid** (para architecture-diagrams.md)
- **DBML Previewer** (para database-model.dbml)

### 🛠️ **Para Desenvolvimento**
- **Docker** + Docker Compose
- **Node.js** + React Native CLI
- **Python 3.11** + Django
- **PostgreSQL**

## 📋 Convenções e Padrões

### 🎨 **Diagramas**
- **PlantUML** — Sintaxe padrão para todos os diagramas
- **Cores consistentes** — Paleta profissional
- **Numeração sequencial** — Fácil referência
- **Notas explicativas** — Contexto técnico

### 📝 **Código**
- **Feature Folders** — Organização por funcionalidade
- **TypeScript** — Tipagem estática no frontend
- **REST Conventions** — Padrões HTTP corretos
- **JWT Security** — Autenticação stateless

### 📖 **Documentação**
- **Markdown** — Formato padrão
- **Exemplos práticos** — Código funcional
- **Estrutura consistente** — Fácil navegação
- **Links internos** — Referências cruzadas

## 🚀 Próximos Passos

### 🔄 **Para Implementação**
1. **Setup do ambiente** — Docker + dependências
2. **Backend primeiro** — API + banco de dados
3. **Frontend integrado** — App + API
4. **Testes e deploy** — Validação completa

### 📈 **Para Evolução**
1. **Novos módulos** — Seguir padrão de features
2. **Integrações** — APIs externas
3. **Performance** — Otimizações
4. **Segurança** — Auditorias regulares

## 📞 Suporte

### 🔍 **Encontrar Informações**
- **API:** Consulte `api-documentation.md`
- **Componentes:** Veja `frontend-documentation.md`
- **Fluxos:** Analise `sequence-diagrams/`
- **Dados:** Examine `database-model.dbml`

### 🛠️ **Resolver Problemas**
- **Erros de API:** Códigos em `api-documentation.md`
- **Fluxos quebrados:** Diagramas de sequência
- **Dados inconsistentes:** Modelo DBML
- **Componentes:** Frontend documentation

---

💡 **Dica:** Esta documentação é viva e deve ser atualizada conforme o sistema evolui. Mantenha sempre sincronizada com o código.