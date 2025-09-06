from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
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


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = UsuarioLoginSerializer(data=request.data)
    if serializer.is_valid():
        usuario = serializer.validated_data['usuario']
        refresh = RefreshToken.for_user(usuario)
        
        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user': {
                'id': usuario.id,
                'nome': usuario.nome,
                'email': usuario.email
            }
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