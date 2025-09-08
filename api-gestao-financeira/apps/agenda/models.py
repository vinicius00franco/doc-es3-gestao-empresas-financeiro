from django.db import models
from apps.empresas.models import Empresa


class Agendamento(models.Model):
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    ]
    STATUS_CHOICES = [
        ('previsto', 'Previsto'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
    ]

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='agendamentos')
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data_vencimento = models.DateField()
    recorrencia = models.CharField(max_length=20, blank=True)  # ex.: mensal, semanal
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='previsto')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'agendamentos'
        ordering = ['-data_vencimento', '-criado_em']


class ProjecaoSaldo(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='projecoes_saldo')
    data = models.DateField()
    saldo_previsto = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'projecoes_saldo'
        unique_together = ['empresa', 'data']
        ordering = ['data']
