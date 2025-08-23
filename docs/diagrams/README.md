# Diagramas Profissionais - Sistema de Gestão Financeira

Esta pasta contém diagramas técnicos detalhados e profissionais do sistema:

## 📋 Arquivos Disponíveis

### 🏗️ Análise Estruturada (IDEF0)
- **`idef0-level0.puml`** — **Nível 0 (Contexto Geral)**
  - Visão macro do sistema com ICOM (Inputs, Controls, Outputs, Mechanisms)
  - Mostra o propósito geral e fronteiras do sistema

- **`idef0-level1.puml`** — **Nível 1 (Decomposição Funcional)**
  - Decomposição das 5 funções principais: A1-A5
  - Fluxos de dados entre processos internos
  - **NOVO:** A5 - Processar Notas Fiscais

### 👥 Análise de Requisitos
- **`use-case.puml`** — **Diagrama de Casos de Uso**
  - 22 casos de uso organizados por módulos funcionais
  - Relacionamentos entre atores (Usuário, Admin, Sistemas Externos)
  - Dependências e extensões entre casos de uso
  - **NOVO:** Módulo de Processamento Fiscal (UC16-UC19)

### 🔄 Análise de Dados
- **`dfd.puml`** — **Diagrama de Fluxo de Dados (Nível 1)**
  - 6 processos principais numerados (1.0 a 6.0)
  - 7 depósitos de dados (D1 a D7)
  - 35 fluxos de dados numerados e rotulados
  - Entidades externas claramente identificadas
  - **NOVO:** Processamento automático de notas fiscais

## 🎨 Como Visualizar

### 1️⃣ **VS Code + PlantUML (Recomendado)**
```bash
# 1. Abra qualquer arquivo .puml
# 2. Command Palette (Ctrl+Shift+P)
# 3. Digite: "PlantUML: Preview Current Diagram"
# 4. Ou clique direito → "Preview Current Diagram"
```

### 2️⃣ **Exportar para Imagem**
```bash
# Via VS Code: Na preview → botão "Export" → PNG/SVG
# Via linha de comando (se tiver plantuml.jar):
java -jar plantuml.jar docs/diagrams/*.puml
```

### 3️⃣ **Navegador (Markdown Preview Enhanced)**
```bash
# Se tiver a extensão instalada:
# Command Palette → "Markdown Preview Enhanced: Open Preview in Browser"
```

## 🔧 Recursos Profissionais Implementados

### ✅ **Layout Otimizado**
- **Sem sobreposições** — elementos bem espaçados
- **Cores organizadas** — paleta profissional consistente
- **Fontes legíveis** — texto preto para máximo contraste

### ✅ **Informações Detalhadas**
- **Rótulos descritivos** — cada fluxo/elemento nomeado
- **Numeração sequencial** — fácil referência
- **Notas explicativas** — regras de negócio importantes

### ✅ **Padrões da Indústria**
- **IDEF0** — metodologia padrão para modelagem funcional
- **DFD** — notação clássica Yourdon/DeMarco
- **UML** — casos de uso seguindo padrão OMG

## 📖 Guia de Leitura por Diagrama

### 🎯 **IDEF0 Level 0** (Contexto)
- **Foco:** Entender o propósito geral do sistema
- **Leia:** ICOM (setas entrando/saindo do processo A-0)

### 🔍 **IDEF0 Level 1** (Decomposição)
- **Foco:** Como o sistema se divide em 5 grandes funções
- **Leia:** Sequência A1→A2→A3→A4→A5 e fluxos internos

### 👤 **Use Case** (Requisitos)
- **Foco:** O que cada tipo de usuário pode fazer
- **Leia:** Agrupamentos por módulo funcional

### 📊 **DFD** (Fluxo de Dados)
- **Foco:** Como os dados se movem pelo sistema
- **Leia:** Sequência numerada 1→35 dos fluxos
- **NOVO:** Fluxos 28-35 para processamento de NF-e

## 🆕 Novas Funcionalidades (v2.0)

### 📄 **Processamento Automático de Notas Fiscais**
- **Upload:** Arquivos XML (NF-e) e PDF
- **Extração:** OCR para PDF, XML parser para NF-e
- **Integração:** Criação automática de fornecedores e transações
- **Validação:** Dados fiscais e conformidade

## 🚀 Próximos Passos

Para trabalhar com estes diagramas:

1. **Abra no VS Code** e use a preview da extensão PlantUML
2. **Edite conforme necessário** — sintaxe PlantUML é intuitiva
3. **Exporte imagens** para apresentações ou documentação
4. **Compartilhe via Git** — arquivos .puml são versionáveis

---
💡 **Dica:** Todos os diagramas usam `skinparam defaultFontColor #000000` para garantir texto legível.
