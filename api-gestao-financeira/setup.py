#!/usr/bin/env python
"""
Script de inicialização para criar dados básicos do sistema
Execute: python manage.py shell < setup.py
"""

from apps.assinaturas.models import Plano
from apps.transacoes.models import Categoria
from apps.empresas.models import Empresa
from django.contrib.auth import get_user_model

User = get_user_model()

print("🚀 Iniciando setup do sistema...")

# Criar planos de assinatura
print("📋 Criando planos de assinatura...")

plano_gratis, created = Plano.objects.get_or_create(
    nome='Grátis',
    defaults={
        'descricao': 'Plano básico gratuito com funcionalidades essenciais',
        'preco': 0.00,
        'limite_transacoes': 50,
        'limite_empresas': 1,
        'permite_relatorios': False,
        'permite_exportacao': False,
        'permite_notas_fiscais': False
    }
)

plano_pro, created = Plano.objects.get_or_create(
    nome='Pro',
    defaults={
        'descricao': 'Plano profissional completo com recursos avançados',
        'preco': 29.90,
        'limite_transacoes': None,  # Ilimitado
        'limite_empresas': 5,
        'permite_relatorios': True,
        'permite_exportacao': True,
        'permite_notas_fiscais': True
    }
)

print(f"✅ Planos criados: {plano_gratis.nome}, {plano_pro.nome}")

print("🎉 Setup concluído com sucesso!")
print("\n📝 Próximos passos:")
print("1. Criar um superusuário: python manage.py createsuperuser")
print("2. Acessar admin: http://localhost:8000/admin/")
print("3. Testar API: http://localhost:8000/api/v1/auth/register/")
print("\n📚 Documentação completa disponível no README.md")