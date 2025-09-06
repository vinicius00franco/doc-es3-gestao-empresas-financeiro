from django.db import models
from django.conf import settings


class Plano(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    limite_transacoes = models.IntegerField(null=True, blank=True)  # null = ilimitado
    limite_empresas = models.IntegerField(default=1)
    permite_relatorios = models.BooleanField(default=False)
    permite_exportacao = models.BooleanField(default=False)
    permite_notas_fiscais = models.BooleanField(default=False)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'planos'
        verbose_name = 'Plano'
        verbose_name_plural = 'Planos'
        ordering = ['preco']

    def __str__(self):
        return self.nome

    @property
    def eh_gratuito(self):
        return self.preco == 0


class Assinatura(models.Model):
    STATUS_CHOICES = [
        ('ativa', 'Ativa'),
        ('cancelada', 'Cancelada'),
        ('inadimplente', 'Inadimplente'),
        ('expirada', 'Expirada'),
    ]

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='assinatura'
    )
    plano = models.ForeignKey(Plano, on_delete=models.PROTECT)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='ativa')
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    gateway_pagamento = models.CharField(max_length=50, blank=True)
    id_transacao_gateway = models.CharField(max_length=255, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'assinaturas'
        verbose_name = 'Assinatura'
        verbose_name_plural = 'Assinaturas'
        ordering = ['-criado_em']

    def __str__(self):
        return f"{self.usuario.nome} - {self.plano.nome}"

    def pode_criar_transacao(self):
        """Verifica se o usuário pode criar mais transações"""
        if self.status != 'ativa':
            return False
        
        if self.plano.limite_transacoes is None:  # Ilimitado
            return True
        
        # Conta transações do mês atual
        from django.utils import timezone
        from apps.transacoes.models import Transacao
        
        hoje = timezone.now().date()
        inicio_mes = hoje.replace(day=1)
        
        transacoes_mes = Transacao.objects.filter(
            empresa__usuario=self.usuario,
            data_transacao__gte=inicio_mes,
            data_transacao__lte=hoje
        ).count()
        
        return transacoes_mes < self.plano.limite_transacoes

    def pode_criar_empresa(self):
        """Verifica se o usuário pode criar mais empresas"""
        if self.status != 'ativa':
            return False
        
        empresas_count = self.usuario.empresas.filter(ativa=True).count()
        return empresas_count < self.plano.limite_empresas