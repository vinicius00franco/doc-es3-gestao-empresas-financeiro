from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from .models import Plano, Assinatura
from .serializers import PlanoSerializer, AssinaturaSerializer, UpgradeAssinaturaSerializer


class PlanoListView(generics.ListAPIView):
    queryset = Plano.objects.filter(ativo=True)
    serializer_class = PlanoSerializer
    permission_classes = [AllowAny]


class AssinaturaAtualView(generics.RetrieveAPIView):
    serializer_class = AssinaturaSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        assinatura, created = Assinatura.objects.get_or_create(
            usuario=self.request.user,
            defaults={
                'plano': Plano.objects.get(nome='Grátis'),
                'data_inicio': timezone.now().date(),
                'status': 'ativa'
            }
        )
        return assinatura


@api_view(['POST'])
def upgrade_assinatura(request):
    serializer = UpgradeAssinaturaSerializer(data=request.data)
    
    if serializer.is_valid():
        plano_id = serializer.validated_data['plano_id']
        plano = Plano.objects.get(id=plano_id)
        # Simular integração com gateway de pagamento via serviço dedicado
        from apps.notas_fiscais.services import payment_gateway_create_checkout
        checkout = payment_gateway_create_checkout(plano_id)
        payment_url = checkout['payment_url']
        session_id = checkout['session_id']

        return Response({
            'payment_url': payment_url,
            'session_id': session_id,
            'plano': PlanoSerializer(plano).data
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def confirmar_pagamento(request):
    """
    Endpoint para webhook do gateway de pagamento
    Em produção, seria protegido com assinatura do gateway
    """
    session_id = request.data.get('session_id')
    plano_id = request.data.get('plano_id')
    usuario_id = request.data.get('usuario_id')
    
    try:
        from apps.usuarios.models import Usuario
        usuario = Usuario.objects.get(id=usuario_id)
        plano = Plano.objects.get(id=plano_id)
        
        # Atualizar assinatura
        assinatura = usuario.assinatura
        assinatura.plano = plano
        assinatura.status = 'ativa'
        assinatura.data_inicio = timezone.now().date()
        assinatura.valor_pago = plano.preco
        assinatura.id_transacao_gateway = session_id
        assinatura.save()
        
        return Response({'message': 'Pagamento confirmado com sucesso.'})
    
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        )