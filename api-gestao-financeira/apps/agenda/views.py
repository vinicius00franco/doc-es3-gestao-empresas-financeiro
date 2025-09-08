from datetime import date
from calendar import monthrange
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Agendamento, ProjecaoSaldo
from .serializers import AgendamentoSerializer, ProjecaoSaldoSerializer


class AgendamentoListCreateView(generics.ListCreateAPIView):
    serializer_class = AgendamentoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        empresa = getattr(self.request, 'tenant_empresa', None)
        qs = Agendamento.objects.all()
        if empresa:
            qs = qs.filter(empresa=empresa)
        # filtros opcionais
        data_inicio = self.request.query_params.get('data_inicio')
        data_fim = self.request.query_params.get('data_fim')
        if data_inicio:
            qs = qs.filter(data_vencimento__gte=data_inicio)
        if data_fim:
            qs = qs.filter(data_vencimento__lte=data_fim)
        tipo = self.request.query_params.get('tipo')
        if tipo:
            qs = qs.filter(tipo=tipo)
        return qs.order_by('data_vencimento')

    def perform_create(self, serializer):
        empresa = getattr(self.request, 'tenant_empresa', None)
        if empresa:
            serializer.save(empresa=empresa)
        else:
            serializer.save()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def saldo_diario(request):
    """Retorna saldo diário previsto para um mês (YYYY-MM). Simulação simples."""
    empresa = getattr(request, 'tenant_empresa', None)
    month = request.query_params.get('month')
    if not month:
        today = date.today()
        month = f"{today.year:04d}-{today.month:02d}"
    year, mon = map(int, month.split('-'))
    last_day = monthrange(year, mon)[1]

    # Simulação: saldo inicial 0 e somatório de agendamentos
    agqs = Agendamento.objects.all()
    if empresa:
        agqs = agqs.filter(empresa=empresa)
    agqs = agqs.filter(data_vencimento__gte=f"{month}-01", data_vencimento__lte=f"{month}-{last_day:02d}")

    dia_valores = {d: 0 for d in range(1, last_day + 1)}
    for ag in agqs:
        d = ag.data_vencimento.day
        dia_valores[d] += (ag.valor if ag.tipo == 'entrada' else -ag.valor)

    saldo = 0
    resposta = []
    for d in range(1, last_day + 1):
        saldo += dia_valores[d]
        resposta.append({
            'data': f"{year:04d}-{mon:02d}-{d:02d}",
            'saldo_previsto': f"{saldo:.2f}",
        })
    return Response(resposta)
