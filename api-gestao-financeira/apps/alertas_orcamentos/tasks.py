from celery import shared_task
from django.utils import timezone
from .models import Alerta


@shared_task
def dispatch_alertas():
    """Varre alertas ativos por empresa e agenda envios conforme antecedência.
    Placeholder: apenas retorna um resumo do que seria processado.
    """
    hoje = timezone.localdate()
    ativos = Alerta.objects.filter(ativo=True)
    por_empresa = {}
    for alerta in ativos:
        por_empresa.setdefault(alerta.empresa_id, 0)
        por_empresa[alerta.empresa_id] += 1
    return {"data": str(hoje), "empresas": len(por_empresa), "alertas": sum(por_empresa.values())}
