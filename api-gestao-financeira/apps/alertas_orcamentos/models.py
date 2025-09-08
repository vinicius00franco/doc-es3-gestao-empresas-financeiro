from django.db import models
from apps.empresas.models import Empresa


class Alerta(models.Model):
    TIPO_CHOICES = [
        ('vencimento_nf', 'Vencimento NF'),
        ('vencimento_boleto', 'Vencimento Boleto'),
        ('orcamento', 'Orçamento'),
        ('caixa', 'Caixa'),
    ]
    CANAL_CHOICES = [
        ('email', 'E-mail'),
        ('push', 'Push'),
    ]
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='alertas')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    canal = models.CharField(max_length=10, choices=CANAL_CHOICES, default='email')
    antecedencia_dias = models.IntegerField(default=3)
    ativo = models.BooleanField(default=True)
    parametros = models.JSONField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'alertas'


class OrcamentoMensal(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='orcamentos')
    categoria_id = models.IntegerField()  # referência indireta para categoria
    mes = models.CharField(max_length=7)  # YYYY-MM
    valor_planejado = models.DecimalField(max_digits=12, decimal_places=2)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'orcamentos_mensais'
        unique_together = ['empresa', 'categoria_id', 'mes']
