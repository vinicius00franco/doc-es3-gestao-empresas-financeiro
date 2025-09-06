#!/bin/bash

echo "🚀 Iniciando aplicação em modo produção..."

# Aplicar migrações
echo "📊 Aplicando migrações do banco de dados..."
python manage.py migrate --noinput

# Coletar arquivos estáticos
echo "📁 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Criar superusuário se não existir
echo "👤 Verificando superusuário..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superusuário criado: admin/admin123')
"

# Criar dados iniciais
echo "📋 Criando dados iniciais..."
python manage.py shell < setup.py

echo "✅ Aplicação pronta para produção!"

# Iniciar Daphne
exec daphne -b 0.0.0.0 -p 8000 core.asgi:application