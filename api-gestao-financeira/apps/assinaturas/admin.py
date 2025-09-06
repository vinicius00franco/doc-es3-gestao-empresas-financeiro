from django.contrib import admin
from .models import Plano, Assinatura


@admin.register(Plano)
class PlanoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'preco', 'limite_transacoes', 'limite_empresas', 'ativo']
    list_filter = ['ativo', 'permite_relatorios', 'permite_exportacao']
    search_fields = ['nome', 'descricao']
    ordering = ['preco']


@admin.register(Assinatura)
class AssinaturaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'plano', 'status', 'data_inicio', 'data_fim']
    list_filter = ['status', 'plano', 'data_inicio']
    search_fields = ['usuario__email', 'usuario__nome']
    ordering = ['-criado_em']
    readonly_fields = ['criado_em', 'atualizado_em']