from django.core.management.base import BaseCommand
from apps.assinaturas.models import Plano


class Command(BaseCommand):
    help = 'Cria planos padrão (Grátis e Profissional) com limites predefinidos.'

    def handle(self, *args, **options):
        gratis, _ = Plano.objects.get_or_create(
            nome='Grátis',
            defaults={
                'descricao': 'Plano básico gratuito',
                'preco': 0,
                'limite_transacoes': 100,
                'limite_empresas': 1,
                'permite_relatorios': False,
                'permite_exportacao': False,
                'permite_notas_fiscais': False,
                'ativo': True,
            }
        )
        prof, _ = Plano.objects.get_or_create(
            nome='Profissional',
            defaults={
                'descricao': 'Plano completo para profissionais',
                'preco': 29.90,
                'limite_transacoes': 1000,
                'limite_empresas': 4,
                'permite_relatorios': True,
                'permite_exportacao': True,
                'permite_notas_fiscais': True,
                'ativo': True,
            }
        )
        self.stdout.write(self.style.SUCCESS('Planos criados/atualizados com sucesso.'))
