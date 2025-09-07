from django.db import models
from django.conf import settings
from apps.empresas.models import Empresa
from core.tenant import TenantMixin


class Categoria(TenantMixin):
    TIPO_TRANSACAO_CHOICES = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    ]

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='categorias')
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    cor = models.CharField(max_length=7, blank=True)  # Hex color
    icone = models.CharField(max_length=50, blank=True)
    tipo_transacao = models.CharField(max_length=10, choices=TIPO_TRANSACAO_CHOICES)
    ativa = models.BooleanField(default=True)
    categoria_padrao = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'categorias'
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        unique_together = ['tenant_id', 'empresa', 'nome']
        ordering = ['tipo_transacao', 'nome']
        indexes = [
            models.Index(fields=['tenant_id', 'empresa']),
            models.Index(fields=['tenant_id', 'tipo_transacao']),
        ]

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_transacao_display()})"


class Fornecedor(TenantMixin):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='fornecedores')
    cnpj = models.CharField(max_length=18)
    razao_social = models.CharField(max_length=255)
    nome_fantasia = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    endereco = models.TextField(blank=True)
    criado_automaticamente = models.BooleanField(default=False)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'fornecedores'
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'
        unique_together = ['tenant_id', 'empresa', 'cnpj']
        ordering = ['razao_social']
        indexes = [
            models.Index(fields=['tenant_id', 'empresa']),
            models.Index(fields=['tenant_id', 'ativo']),
        ]

    def __str__(self):
        return self.razao_social


class Transacao(TenantMixin):
    TIPO_TRANSACAO_CHOICES = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    ]
    
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]
    
    FORMA_PAGAMENTO_CHOICES = [
        ('dinheiro', 'Dinheiro'),
        ('pix', 'PIX'),
        ('cartao_credito', 'Cartão de Crédito'),
        ('cartao_debito', 'Cartão de Débito'),
        ('boleto', 'Boleto'),
        ('transferencia', 'Transferência'),
    ]

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='transacoes')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, null=True, blank=True)
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data_transacao = models.DateField()
    tipo_transacao = models.CharField(max_length=10, choices=TIPO_TRANSACAO_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='confirmada')
    observacoes = models.TextField(blank=True)
    numero_documento = models.CharField(max_length=100, blank=True)
    forma_pagamento = models.CharField(max_length=20, choices=FORMA_PAGAMENTO_CHOICES, blank=True)
    recorrente = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transacoes'
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'
        ordering = ['-data_transacao', '-criado_em']
        indexes = [
            models.Index(fields=['tenant_id', 'empresa']),
            models.Index(fields=['tenant_id', 'data_transacao']),
            models.Index(fields=['tenant_id', 'status']),
            models.Index(fields=['tenant_id', 'tipo_transacao']),
        ]

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor}"

    @property
    def valor_formatado(self):
        return f"R$ {self.valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')