from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Alerta, OrcamentoMensal
from .serializers import AlertaSerializer, OrcamentoMensalSerializer


class AlertaListCreateView(generics.ListCreateAPIView):
    serializer_class = AlertaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        empresa = getattr(self.request, 'tenant_empresa', None)
        qs = Alerta.objects.all()
        if empresa:
            qs = qs.filter(empresa=empresa)
        return qs.order_by('-criado_em')

    def perform_create(self, serializer):
        empresa = getattr(self.request, 'tenant_empresa', None)
        if empresa:
            serializer.save(empresa=empresa)
        else:
            serializer.save()


class AlertaDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AlertaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        empresa = getattr(self.request, 'tenant_empresa', None)
        qs = Alerta.objects.all()
        if empresa:
            qs = qs.filter(empresa=empresa)
        return qs


class OrcamentoMensalListCreateView(generics.ListCreateAPIView):
    serializer_class = OrcamentoMensalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        empresa = getattr(self.request, 'tenant_empresa', None)
        qs = OrcamentoMensal.objects.all()
        if empresa:
            qs = qs.filter(empresa=empresa)
        return qs.order_by('-mes')

    def perform_create(self, serializer):
        empresa = getattr(self.request, 'tenant_empresa', None)
        if empresa:
            serializer.save(empresa=empresa)
        else:
            serializer.save()


class OrcamentoMensalDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrcamentoMensalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        empresa = getattr(self.request, 'tenant_empresa', None)
        qs = OrcamentoMensal.objects.all()
        if empresa:
            qs = qs.filter(empresa=empresa)
        return qs
