from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Empresa
from .serializers import EmpresaSerializer


class EmpresaListCreateView(generics.ListCreateAPIView):
    serializer_class = EmpresaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Empresa.objects.filter(usuario=self.request.user)


class EmpresaDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EmpresaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Empresa.objects.filter(usuario=self.request.user)


@api_view(['POST'])
def definir_empresa_padrao(request, pk):
    try:
        empresa = Empresa.objects.get(pk=pk, usuario=request.user)
        
        # Remove padrão das outras empresas
        Empresa.objects.filter(
            usuario=request.user, 
            empresa_padrao=True
        ).update(empresa_padrao=False)
        
        # Define como padrão
        empresa.empresa_padrao = True
        empresa.save()
        
        return Response({'message': 'Empresa padrão definida com sucesso.'})
    
    except Empresa.DoesNotExist:
        return Response(
            {'error': 'Empresa não encontrada.'}, 
            status=status.HTTP_404_NOT_FOUND
        )