from rest_framework.permissions import IsAuthenticated
from .tenant import get_current_tenant


class TenantViewMixin:
    """Mixin para views que trabalham com dados multi-tenant"""
    
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Retorna queryset filtrado automaticamente pelo tenant atual"""
        queryset = super().get_queryset()
        
        # O TenantManager já filtra automaticamente por tenant_id
        # Mantemos o filtro por empresa para compatibilidade
        if hasattr(self.request, 'tenant_empresa') and self.request.tenant_empresa:
            if hasattr(queryset.model, 'empresa'):
                queryset = queryset.filter(empresa=self.request.tenant_empresa)
        
        return queryset
    
    def perform_create(self, serializer):
        """Garante que novos objetos sejam criados com a empresa do tenant atual"""
        if hasattr(self.request, 'tenant_empresa') and self.request.tenant_empresa:
            if hasattr(serializer.Meta.model, 'empresa'):
                serializer.save(empresa=self.request.tenant_empresa)
            else:
                serializer.save()
        else:
            serializer.save()