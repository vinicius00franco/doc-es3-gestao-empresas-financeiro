# Infraestrutura - API Gestão Financeira

## 📁 Estrutura

```
infra/
├── nginx/                  # Configuração Nginx
│   ├── nginx.conf         # Load balancer config
│   └── Dockerfile         # Container Nginx
├── scripts/               # Scripts de deploy
│   └── start-prod.sh      # Inicialização produção
├── docker-compose.prod.yml # Orquestração produção
├── Dockerfile.prod        # Build otimizada
└── .env.prod             # Variáveis produção
```

## 🚀 Comandos

### Produção
```bash
# Da pasta raiz do projeto
docker-compose -f infra/docker-compose.prod.yml up --build

# Logs
docker-compose -f infra/docker-compose.prod.yml logs -f

# Parar
docker-compose -f infra/docker-compose.prod.yml down
```

### Desenvolvimento
```bash
# Da pasta raiz do projeto
docker-compose up --build
```