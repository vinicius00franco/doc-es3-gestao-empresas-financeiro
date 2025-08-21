# Diagramas de Sequência - Gestão Financeira

> **AVISO**: Este arquivo foi reorganizado. Os diagramas agora estão organizados em pastas por funcionalidade.
> 
> **Nova localização**: `docs/sequence-diagrams/`

## Nova Estrutura

Os diagramas foram reorganizados em:

- **[authentication/](sequence-diagrams/authentication/)** - Autenticação JWT e autorização
- **[transactions/](sequence-diagrams/transactions/)** - Gestão de transações financeiras
- **[subscriptions/](sequence-diagrams/subscriptions/)** - Assinaturas e verificação de limites
- **[user-management/](sequence-diagrams/user-management/)** - Gestão de usuários e recuperação de senha

## Formatos Disponíveis

Cada diagrama está disponível em dois formatos:
- **PlantUML** (`.puml`) - Para ferramentas especializadas
- **Mermaid** (`.mmd`) - Para visualização no GitHub/GitLab

## Acesso Rápido

### Autenticação
- [Login JWT - PlantUML](sequence-diagrams/authentication/jwt-login.puml)
- [Login JWT - Mermaid](sequence-diagrams/authentication/jwt-login.mmd)

### Transações
- [Criar Transação - PlantUML](sequence-diagrams/transactions/create-transaction.puml)
- [Criar Transação - Mermaid](sequence-diagrams/transactions/create-transaction.mmd)

### Assinaturas
- [Verificação de Limites - PlantUML](sequence-diagrams/subscriptions/subscription-check.puml)
- [Verificação de Limites - Mermaid](sequence-diagrams/subscriptions/subscription-check.mmd)
- [Upgrade de Plano - PlantUML](sequence-diagrams/subscriptions/plan-upgrade.puml)
- [Upgrade de Plano - Mermaid](sequence-diagrams/subscriptions/plan-upgrade.mmd)

### Gestão de Usuários
- [Recuperação de Senha - PlantUML](sequence-diagrams/user-management/password-reset.puml)
- [Recuperação de Senha - Mermaid](sequence-diagrams/user-management/password-reset.mmd)

---

**Para mais detalhes, acesse**: [sequence-diagrams/README.md](sequence-diagrams/README.md)
