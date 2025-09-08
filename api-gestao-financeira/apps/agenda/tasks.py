from datetime import date
from calendar import monthrange
from celery import shared_task
from django.db import transaction
from django.utils import timezone
from apps.empresas.models import Empresa
from .models import Agendamento, ProjecaoSaldo


@shared_task
def gerar_projecao_saldo(empresa_id: int, month: str):
    """Simula geração de projeção de saldo para um mês (YYYY-MM)."""
    year, mon = map(int, month.split('-'))
    last_day = monthrange(year, mon)[1]

    agqs = Agendamento.objects.filter(empresa_id=empresa_id,
                                      data_vencimento__gte=f"{month}-01",
                                      data_vencimento__lte=f"{month}-{last_day:02d}")

    dia_valores = {d: 0 for d in range(1, last_day + 1)}
    for ag in agqs:
        d = ag.data_vencimento.day
        dia_valores[d] += (ag.valor if ag.tipo == 'entrada' else -ag.valor)

    saldo = 0
    with transaction.atomic():
        for d in range(1, last_day + 1):
            saldo += dia_valores[d]
            ProjecaoSaldo.objects.update_or_create(
                empresa_id=empresa_id,
                data=date(year, mon, d),
                defaults={'saldo_previsto': saldo}
            )


@shared_task
def dispatch_gerar_projecao_saldo():
    """Dispatcher sem argumentos para Celery Beat.
    Itera empresas e agenda gerar_projecao_saldo para o mês corrente (YYYY-MM).
    """
    today = timezone.localdate()
    month = f"{today.year:04d}-{today.month:02d}"
    empresa_ids = list(Empresa.objects.values_list('id', flat=True))
    for eid in empresa_ids:
        gerar_projecao_saldo.delay(eid, month)
    return {"mes": month, "empresas_agendadas": len(empresa_ids)}
