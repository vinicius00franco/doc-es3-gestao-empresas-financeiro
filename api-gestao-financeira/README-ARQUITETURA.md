# Arquitetura de Produção - API Gestão Financeira

## 🏗️ Visão Geral da Arquitetura

```
Internet → Nginx (Load Balancer) → 3x Daphne (Django API) → PostgreSQL
                ↓                                    ↓
         Static/Media Files                    Redis (Cache/Celery)
                                                     ↓
                                              Celery Workers
```

## 🔧 Componentes da Arquitetura

### 1. **Nginx - Proxy Reverso e Load Balancer**
- **Porta**: 80 (HTTP)
- **Função**: Distribui requisições entre 3 instâncias Django
- **Recursos**:
  - Serve arquivos estáticos e media
  - Headers de segurança
  - Timeouts e buffers otimizados
  - Health checks

### 2. **Django API - 3 Instâncias (web1, web2, web3)**
- **Servidor**: Daphne (ASGI)
- **Porta**: 8000 (interna)
- **Recursos**:
  - Processamento assíncrono
  - Health checks integrados
  - Auto-restart em falhas

### 3. **PostgreSQL - Banco de Dados**
- **Versão**: 15
- **Recursos**:
  - Dados persistentes
  - Health checks
  - Backup automático via volumes

### 4. **Redis - Cache e Message Broker**
- **Função**: Cache + Celery broker
- **Recursos**:
  - Cache de sessões
  - Filas de tarefas assíncronas

### 5. **Celery - Processamento Assíncrono**
- **Worker**: Processa tarefas em background
- **Beat**: Agendador de tarefas
- **Uso**: Processamento de notas fiscais

## 🚀 Como Executar

### Desenvolvimento
```bash
# Ambiente de desenvolvimento com hot reload
docker-compose up --build

# Acessar: http://localhost:8000
```

### Produção
```bash
# Ambiente de produção com load balancer
docker-compose -f docker-compose.prod.yml up --build

# Acessar: http://localhost (porta 80)
```

## 📊 Monitoramento e Health Checks

### Endpoints de Saúde
- **API**: `GET /health/` - Status da aplicação
- **Nginx**: `GET /health/` - Status do load balancer

### Health Checks Automáticos
- **PostgreSQL**: `pg_isready`
- **Redis**: `redis-cli ping`
- **Django**: `curl /health/`

## ⚡ Performance e Escalabilidade

### Load Balancing
- **3 instâncias Django** rodando simultaneamente
- **Distribuição automática** de carga pelo Nginx
- **Failover automático** em caso de falha

### Cache Strategy
- **Redis cache** para sessões e dados frequentes
- **Nginx cache** para arquivos estáticos
- **Browser cache** com headers otimizados

### Processamento Assíncrono
- **Celery workers** para tarefas pesadas
- **Filas Redis** para comunicação
- **Processamento de NF-e** em background

## 🔒 Segurança

### Headers de Segurança (Nginx)
- `X-Frame-Options: SAMEORIGIN`
- `X-Content-Type-Options: nosniff`
- `X-XSS-Protection: 1; mode=block`

### Django Security (Produção)
- `SECURE_BROWSER_XSS_FILTER = True`
- `SECURE_CONTENT_TYPE_NOSNIFF = True`
- `SECURE_HSTS_SECONDS = 31536000`
- `X_FRAME_OPTIONS = 'DENY'`

### Usuário Não-Root
- Containers rodam com usuário `django`
- Permissões mínimas necessárias

## 📁 Estrutura de Arquivos

```
api-gestao-financeira/
├── nginx/
│   ├── nginx.conf          # Configuração do Nginx
│   └── Dockerfile          # Container Nginx
├── scripts/
│   └── start-prod.sh       # Script de inicialização
├── docker-compose.yml      # Desenvolvimento
├── docker-compose.prod.yml # Produção
├── Dockerfile              # Desenvolvimento
├── Dockerfile.prod         # Produção otimizada
├── .env.local             # Variáveis desenvolvimento
└── .env.prod              # Variáveis produção
```

## 🔧 Comandos Úteis

### Logs
```bash
# Logs de todos os serviços
docker-compose -f docker-compose.prod.yml logs -f

# Logs específicos
docker-compose -f docker-compose.prod.yml logs -f nginx
docker-compose -f docker-compose.prod.yml logs -f web1
```

### Scaling
```bash
# Escalar para 5 instâncias Django
docker-compose -f docker-compose.prod.yml up --scale web1=2 --scale web2=2 --scale web3=1
```

### Manutenção
```bash
# Backup do banco
docker-compose -f docker-compose.prod.yml exec db pg_dump -U postgres gestao_financeira_prod > backup.sql

# Restaurar backup
docker-compose -f docker-compose.prod.yml exec -T db psql -U postgres gestao_financeira_prod < backup.sql
```

## 📈 Métricas e Monitoramento

### Recursos Recomendados
- **CPU**: 2-4 cores por instância Django
- **RAM**: 1-2GB por instância Django
- **Disco**: SSD para melhor performance do PostgreSQL

### Monitoramento Externo (Futuro)
- **Prometheus + Grafana** para métricas
- **ELK Stack** para logs centralizados
- **Sentry** para tracking de erros

## 🌐 Deploy em Produção

### Variáveis Importantes (.env.prod)
```env
SECRET_KEY=your-super-secret-production-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
POSTGRES_PASSWORD=your-secure-password
```

### SSL/HTTPS (Futuro)
- Adicionar certificado Let's Encrypt no Nginx
- Redirecionar HTTP → HTTPS
- Configurar HSTS headers

---

💡 **Esta arquitetura suporta milhares de usuários simultâneos e é facilmente escalável horizontalmente.**