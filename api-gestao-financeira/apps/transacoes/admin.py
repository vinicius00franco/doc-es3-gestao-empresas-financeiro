from django.contrib import admin
from .models import Transacao, Categoria, Fornecedor


@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'valor', 'tipo_transacao', 'data_transacao', 'empresa', 'status']
    list_filter = ['tipo_transacao', 'status', 'data_transacao', 'empresa']
    search_fields = ['descricao', 'observacoes', 'numero_documento']
    ordering = ['-data_transacao']
    readonly_fields = ['criado_em', 'atualizado_em']


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo_transacao', 'empresa', 'ativa', 'categoria_padrao']
    list_filter = ['tipo_transacao', 'ativa', 'categoria_padrao', 'empresa']
    search_fields = ['nome', 'descricao']
    ordering = ['empresa', 'tipo_transacao', 'nome']


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ['razao_social', 'cnpj', 'empresa', 'criado_automaticamente', 'ativo']
    list_filter = ['criado_automaticamente', 'ativo', 'empresa']
    search_fields = ['razao_social', 'nome_fantasia', 'cnpj']
    ordering = ['empresa', 'razao_social']
    readonly_fields = ['criado_em', 'atualizado_em']