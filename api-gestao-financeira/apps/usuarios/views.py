from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from core.jwt_utils import CustomRefreshToken
from .models import Usuario
from .serializers import (
    UsuarioRegistroSerializer, 
    UsuarioLoginSerializer, 
    UsuarioSerializer,
    ConfiguracaoUsuarioSerializer
)


@api_view(['POST'])
@permission_classes([AllowAny])
def registro(request):
    serializer = UsuarioRegistroSerializer(data=request.data)
    if serializer.is_valid():
        usuario = serializer.save()
        return Response({
            'id': usuario.id,
            'nome': usuario.nome,
            'email': usuario.email,
            'criado_em': usuario.criado_em
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.throttling import UserRateThrottle

class LoginRateThrottle(UserRateThrottle):
    scope = 'login'

@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([LoginRateThrottle])
def login(request):
    serializer = UsuarioLoginSerializer(data=request.data)
    if serializer.is_valid():
        usuario = serializer.validated_data['usuario']
        empresa = serializer.validated_data['empresa']
        application_id = serializer.validated_data['application_id']
        
        refresh = CustomRefreshToken.for_user_with_tenant(usuario, application_id)
        
        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user': {
                'id': usuario.id,
                'nome': usuario.nome,
                'email': usuario.email
            },
            'application_id': application_id
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    try:
        refresh_token = request.data.get('refresh_token')
        token = RefreshToken(refresh_token)
        return Response({
            'access_token': str(token.access_token)
        })
    except Exception:
        return Response(
            {'error': 'Token inválido'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )


class PerfilView(generics.RetrieveUpdateAPIView):
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ConfiguracaoView(generics.RetrieveUpdateAPIView):
    serializer_class = ConfiguracaoUsuarioSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.configuracao