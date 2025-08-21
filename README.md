# Gestão Financeira Simplificada (v2)

Aplicação para gestão financeira com backend em Django REST Framework, frontend mobile em React Native e ambiente com Docker.

## Stack principal
- Backend: Django REST Framework (Python)
- Frontend: React Native
- Banco: PostgreSQL
- Autenticação: JWT
- Containerização: Docker / Docker Compose

## Setup rápido
```bash
git clone <repo-url>
cd es3
docker-compose up --build
# Backend: http://localhost:8000
```

## Estrutura (resumida)
- gestao_financeira/ — backend (apps por feature: usuarios, empresas, transacoes, assinaturas, relatorios)
- mobile_app/ — frontend React Native
- docs/ — documentação e diagramas (PlantUML, Mermaid, DBML)

## Documentação
Consulte a pasta `docs/` para API, arquitetura e diagramas de sequência.

## Extensões VS Code (principais instaladas)
- ms-python.python, ms-python.vscode-pylance, ms-toolsai.jupyter
- jebbs.plantuml, bierner.markdown-mermaid, rizkykurniawan.dbml-previewer
- github.copilot, github.copilot-chat, humao.rest-client
- ritwickdey.liveserver, foxundermoon.shell-format, vscode-icons-team.vscode-icons

## Observações
Leia os arquivos em `docs/` para detalhes de API e modelagem. Ajuste variáveis de ambiente antes do deploy.

---
Versão: 2.0 — Agosto 2025
