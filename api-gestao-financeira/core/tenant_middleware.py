from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from .tenant import set_current_tenant, clear_current_tenant


class TenantMiddleware(MiddlewareMixin):
    """Middleware para identificar tenant via JWT application_id ou cabeçalho"""
    
    def process_request(self, request):
        clear_current_tenant()
        tenant_id = None
        
        if request.user.is_authenticated:
            try:
                # 1. Tenta obter application_id do token JWT
                auth_header = request.META.get('HTTP_AUTHORIZATION')
                if auth_header and auth_header.startswith('Bearer '):
                    token = auth_header.split(' ')[1]
                    jwt_auth = JWTAuthentication()
                    validated_token = jwt_auth.get_validated_token(token)
                    tenant_id = validated_token.get('application_id')
                
                # 2. Se não encontrou no token, tenta o cabeçalho
                if not tenant_id:
                    tenant_id = request.META.get('HTTP_X_APPLICATION_ID')
                
                # 3. Se ainda não encontrou, retorna erro
                if not tenant_id:
                    return JsonResponse(
                        {'error': 'Application ID é obrigatório no token ou cabeçalho X-Application-ID'}, 
                        status=400
                    )
                
                # Para application_id string, valida se usuário tem empresas
                empresa = request.user.empresas.first()
                if not empresa:
                    return JsonResponse(
                        {'error': 'Usuário não possui empresas cadastradas'}, 
                        status=403
                    )
                
                # Usa application_id como tenant_id
                set_current_tenant(tenant_id)
                request.tenant_id = tenant_id
                request.application_id = tenant_id
                request.tenant_empresa = empresa
                
            except (InvalidToken, Exception):
                return JsonResponse(
                    {'error': 'Token inválido ou Application ID não encontrado'}, 
                    status=401
                )
    
    def process_response(self, request, response):
        clear_current_tenant()
        return response
    
    def process_exception(self, request, exception):
        clear_current_tenant()
        return None