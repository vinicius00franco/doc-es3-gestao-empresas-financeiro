from django.db import models
from apps.empresas.models import Empresa
from apps.transacoes.models import Fornecedor, Transacao


class NotaFiscal(models.Model):
    STATUS_CHOICES = [
        ('uploaded', 'Enviado'),
        ('processing', 'Processando'),
        ('processed', 'Processado'),
        ('failed', 'Erro no Processamento'),
    ]
    
    TIPO_ARQUIVO_CHOICES = [
        ('XML', 'XML'),
        ('PDF', 'PDF'),
    ]

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='notas_fiscais')
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, null=True, blank=True)
    transacao = models.ForeignKey(Transacao, on_delete=models.SET_NULL, null=True, blank=True)
    
    arquivo_original = models.CharField(max_length=255)
    caminho_arquivo = models.FileField(upload_to='notas_fiscais/%Y/%m/')
    tipo_arquivo = models.CharField(max_length=5, choices=TIPO_ARQUIVO_CHOICES)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='uploaded')
    
    # Dados extraídos da NF-e
    chave_acesso = models.CharField(max_length=44, unique=True, null=True, blank=True)
    cnpj_emissor = models.CharField(max_length=18, blank=True)
    razao_social_emissor = models.CharField(max_length=255, blank=True)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    data_emissao = models.DateField(null=True, blank=True)
    dados_extraidos = models.JSONField(null=True, blank=True)
    
    erro_processamento = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    processado_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'notas_fiscais'
        verbose_name = 'Nota Fiscal'
        verbose_name_plural = 'Notas Fiscais'
        ordering = ['-criado_em']

    def __str__(self):
        return f"NF {self.arquivo_original} - {self.empresa.razao_social}"