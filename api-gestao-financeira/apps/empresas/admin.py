from django.contrib import admin
from .models import Empresa


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['razao_social', 'cnpj', 'usuario', 'tipo_empresa', 'ativa', 'empresa_padrao']
    list_filter = ['tipo_empresa', 'ativa', 'empresa_padrao', 'criado_em']
    search_fields = ['razao_social', 'nome_fantasia', 'cnpj', 'usuario__email']
    ordering = ['-criado_em']
    readonly_fields = ['criado_em', 'atualizado_em']