from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import RegraAutomacao
from .serializers import RegraAutomacaoSerializer


class RegraListCreateView(generics.ListCreateAPIView):
    serializer_class = RegraAutomacaoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        empresa = getattr(self.request, 'tenant_empresa', None)
        qs = RegraAutomacao.objects.all()
        if empresa:
            qs = qs.filter(empresa=empresa)
        return qs.order_by('-criado_em')

    def perform_create(self, serializer):
        empresa = getattr(self.request, 'tenant_empresa', None)
        if empresa:
            serializer.save(empresa=empresa)
        else:
            serializer.save()


class RegraDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RegraAutomacaoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        empresa = getattr(self.request, 'tenant_empresa', None)
        qs = RegraAutomacao.objects.all()
        if empresa:
            qs = qs.filter(empresa=empresa)
        return qs


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def conciliar(request):
    """Simulação de conciliação: aplica regras e retorna estatísticas."""
    # Aqui poderíamos receber um payload de transações não conciliadas e aplicar regras condicao/acao
    # Simulação
    return Response({
        'itens_processados': 0,
        'itens_conciliados': 0,
        'mensagem': 'Simulação de conciliação executada.'
    })
