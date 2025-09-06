from django.contrib import admin
from .models import NotaFiscal


@admin.register(NotaFiscal)
class NotaFiscalAdmin(admin.ModelAdmin):
    list_display = [
        'arquivo_original', 'empresa', 'status', 'razao_social_emissor', 
        'valor_total', 'criado_em'
    ]
    list_filter = ['status', 'tipo_arquivo', 'empresa', 'criado_em']
    search_fields = [
        'arquivo_original', 'chave_acesso', 'cnpj_emissor', 
        'razao_social_emissor'
    ]
    ordering = ['-criado_em']
    readonly_fields = ['criado_em', 'processado_em']