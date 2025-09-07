# Gestão Financeira API

## Deploy com Docker (Arquitetura Separada)

1. Criar rede compartilhada (uma vez):
```
docker network create production-network
```
2. Subir banco de dados:
```
docker compose -f docker-compose.db.yml up -d
```
3. Ajustar `.env` baseado em `.env.example`.
4. Subir aplicação e monitoramento:
```
docker compose -f docker-compose.app.yml up -d --build
```
5. Acessos:
- API: http://localhost
- Métricas Prometheus (/metrics): http://localhost/metrics
- Prometheus UI: http://localhost:9090
- Grafana: http://localhost:3000 (user: admin / senha: `GRAFANA_ADMIN_PASSWORD`)

Escalar aplicação (ex: 3 instâncias):
```
docker compose -f docker-compose.app.yml up -d --scale app=3
```

Recriar somente app (hot reload de imagem):
```
docker compose -f docker-compose.app.yml up -d --build app
```

## Observabilidade
- Métricas expostas via `django-prometheus` em `/metrics`.
- Prometheus coleta e Grafana visualiza.

## Estrutura Simplificada
- `docker-compose.db.yml`: somente PostgreSQL.
- `docker-compose.app.yml`: app, nginx, redis, celery worker, prometheus, grafana.
- `nginx/nginx.conf`: proxy + estáticos.
- `monitoring/prometheus.yml`: jobs de scrape.

## Próximos Passos (Opcional)
- Adicionar HTTPS (montar certificados em `nginx/certs`).
- Configurar dashboards no Grafana (importar dashboards Django/Prometheus).
- Adicionar alertas no Prometheus ou Alertmanager.
