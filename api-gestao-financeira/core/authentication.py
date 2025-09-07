from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from django.contrib.auth.models import AnonymousUser


class TenantJWTAuthentication(JWTAuthentication):
    """Autenticação JWT que valida application_id no token"""
    
    def get_user(self, validated_token):
        user = super().get_user(validated_token)
        
        # Verifica se o token contém application_id
        application_id = validated_token.get('application_id')
        if not application_id:
            raise InvalidToken('Token deve conter application_id')
        
        # Valida se usuário tem empresas cadastradas
        if hasattr(user, 'empresas'):
            if not user.empresas.exists():
                raise InvalidToken('Usuário não possui empresas cadastradas')
        
        return user