# Documentação de Diagramas - API Gestão Financeira

Este diretório contém os diagramas de modelagem do sistema de gestão financeira, organizados por tipo e funcionalidade.

## Estrutura dos Diagramas

### 1. Diagrama de Caso de Uso (`use-case-diagram.puml`)
**Perspectiva:** Visão do Usuário / Comportamento Externo  
**Pergunta que Responde:** "Quais são as funcionalidades que o sistema oferece e quem pode usá-las?"

**Funcionalidades Mapeadas:**
- **Autenticação:** Login, registro, recuperação de senha, configurações
- **Gestão de Empresas:** CRUD de empresas, definição de empresa padrão
- **Gestão Financeira:** CRUD de transações, categorias e fornecedores
- **Processamento Fiscal:** Upload e processamento de notas fiscais
- **Assinaturas:** Contratação, alteração e cancelamento de planos
- **Dashboard:** Visualização de relatórios e exportação de dados

**Atores:**
- **Usuário:** Pessoa física que utiliza o sistema
- **Sistema de Pagamento:** Gateway externo para processamento de pagamentos
- **Receita Federal:** Sistema externo para validação de NF-e

### 2. Diagrama de Fluxo de Dados (`data-flow-diagram.puml`)
**Perspectiva:** Visão de Processamento / Fluxo de Informação  
**Pergunta que Responde:** "De onde vêm os dados, para onde vão e quais processos os transformam?"

**Processos Principais:**
1. **Autenticar Usuário** - Validação de credenciais e geração de tokens
2. **Gerenciar Empresas** - CRUD e validação de dados empresariais
3. **Processar Transações** - Criação, categorização e validação de transações
4. **Processar Notas Fiscais** - Upload, extração de dados e criação de transações
5. **Gerenciar Assinaturas** - Controle de planos e limites de uso
6. **Gerar Dashboard** - Agregação de dados para relatórios

**Depósitos de Dados:**
- D1: Usuários | D2: Empresas | D3: Transações | D4: Categorias
- D5: Fornecedores | D6: Notas Fiscais | D7: Assinaturas | D8: Planos | D9: Logs

### 3. Diagrama de Entidade-Relacionamento (`entity-relationship-diagram.puml`)
**Perspectiva:** Visão de Dados / Estrutura de Armazenamento  
**Pergunta que Responde:** "Quais informações o sistema precisa armazenar e como elas estão estruturadas e conectadas?"

**Entidades Principais:**
- **Usuario:** Dados de autenticação e perfil
- **Empresa:** Informações empresariais (CNPJ, razão social)
- **Transacao:** Movimentações financeiras
- **NotaFiscal:** Documentos fiscais processados
- **Assinatura/Plano:** Controle de acesso e limites

**Relacionamentos Chave:**
- Usuario 1:N Empresa (um usuário pode ter várias empresas)
- Empresa 1:N Transacao (uma empresa tem várias transações)
- NotaFiscal 1:1 Transacao (uma NF pode gerar uma transação)
- Usuario 1:1 Assinatura (controle de plano ativo)

### 4. Diagrama IDEF0 - Nível 0 (`idef0-level0.puml`)
**Perspectiva:** Visão Funcional / Análise de Processo de Negócio  
**Pergunta que Responde:** "Qual é a função principal do sistema e quais são seus ICOM?"

**Função Principal:** GERENCIAR FINANÇAS EMPRESARIAIS

**ICOM:**
- **Inputs:** Dados de usuários, empresas, transações, NF-e, fornecedores
- **Controls:** Legislação fiscal, regras de negócio, políticas de segurança
- **Outputs:** Relatórios, dashboard, dados categorizados, alertas
- **Mechanisms:** Django API, PostgreSQL, JWT, processador NF-e, Celery

### 5. Diagrama IDEF0 - Nível 1 (`idef0-level1.puml`)
**Perspectiva:** Decomposição Funcional Detalhada  
**Pergunta que Responde:** "Quais são as subfunções do sistema e como elas interagem?"

**Subfunções:**
- **A1:** Autenticar e Gerenciar Usuários
- **A2:** Gerenciar Empresas
- **A3:** Processar Transações
- **A4:** Processar Notas Fiscais
- **A5:** Controlar Assinaturas
- **A6:** Gerar Relatórios e Dashboard

## Como Visualizar os Diagramas

### Opção 1: PlantUML Online
1. Acesse [plantuml.com/plantuml](http://www.plantuml.com/plantuml)
2. Copie o conteúdo do arquivo `.puml` desejado
3. Cole no editor online para visualizar

### Opção 2: VS Code com Extensão PlantUML
1. Instale a extensão "PlantUML" no VS Code
2. Abra o arquivo `.puml`
3. Use `Ctrl+Shift+P` → "PlantUML: Preview Current Diagram"

### Opção 3: CLI PlantUML
```bash
# Instalar PlantUML
sudo apt-get install plantuml

# Gerar PNG
plantuml -tpng *.puml

# Gerar SVG
plantuml -tsvg *.puml
```

## Arquitetura Multi-tenant

O sistema implementa arquitetura multi-tenant onde:
- Cada usuário pode ter múltiplas empresas
- Dados são isolados por `tenant_id`
- Empresa padrão define o contexto principal
- Assinaturas controlam limites por usuário

## Fluxos Principais

### Fluxo de Processamento de NF-e
1. Upload do arquivo (XML/PDF)
2. Validação e extração de dados
3. Criação automática de fornecedor (se necessário)
4. Geração de transação baseada nos dados extraídos
5. Categorização automática

### Fluxo de Controle de Assinatura
1. Verificação de limites antes de operações
2. Bloqueio de funcionalidades premium
3. Integração com gateway de pagamento
4. Atualização automática de status

## Tecnologias Utilizadas

- **Backend:** Django REST Framework
- **Banco:** PostgreSQL com multi-tenancy
- **Autenticação:** JWT
- **Processamento Assíncrono:** Celery + Redis
- **Monitoramento:** Prometheus
- **Containerização:** Docker