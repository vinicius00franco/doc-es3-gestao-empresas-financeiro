from django.core.management.base import BaseCommand
from django.db import transaction
from apps.transacoes.models import Transacao, Categoria, Fornecedor


class Command(BaseCommand):
    help = 'Migra dados existentes para incluir tenant_id baseado na empresa'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando migração para multi-tenant...')
        
        with transaction.atomic():
            # Migrar Categorias
            categorias_sem_tenant = Categoria.all_objects.filter(tenant_id__isnull=True)
            for categoria in categorias_sem_tenant:
                categoria.tenant_id = str(categoria.empresa.id)
                categoria.save(update_fields=['tenant_id'])
            
            self.stdout.write(f'Migradas {categorias_sem_tenant.count()} categorias')
            
            # Migrar Fornecedores
            fornecedores_sem_tenant = Fornecedor.all_objects.filter(tenant_id__isnull=True)
            for fornecedor in fornecedores_sem_tenant:
                fornecedor.tenant_id = str(fornecedor.empresa.id)
                fornecedor.save(update_fields=['tenant_id'])
            
            self.stdout.write(f'Migrados {fornecedores_sem_tenant.count()} fornecedores')
            
            # Migrar Transações
            transacoes_sem_tenant = Transacao.all_objects.filter(tenant_id__isnull=True)
            for transacao in transacoes_sem_tenant:
                transacao.tenant_id = str(transacao.empresa.id)
                transacao.save(update_fields=['tenant_id'])
            
            self.stdout.write(f'Migradas {transacoes_sem_tenant.count()} transações')
        
        self.stdout.write(self.style.SUCCESS('Migração concluída com sucesso!'))