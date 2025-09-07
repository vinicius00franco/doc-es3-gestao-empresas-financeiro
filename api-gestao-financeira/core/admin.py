from django.contrib import admin
from .tenant import get_current_tenant, set_current_tenant


class TenantAdminMixin:
    """Mixin para admin que filtra por tenant"""
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(qs.model, 'tenant_id'):
            # No admin, mostra todos os dados se for superuser
            if request.user.is_superuser:
                return qs.model.all_objects.get_queryset()
            # Caso contrário, filtra pela empresa padrão do usuário
            empresa_padrao = request.user.empresas.filter(empresa_padrao=True).first()
            if empresa_padrao:
                return qs.model.all_objects.filter(tenant_id=str(empresa_padrao.id))
        return qs
    
    def save_model(self, request, obj, form, change):
        if hasattr(obj, 'tenant_id') and not obj.tenant_id:
            empresa_padrao = request.user.empresas.filter(empresa_padrao=True).first()
            if empresa_padrao:
                obj.tenant_id = str(empresa_padrao.id)
        super().save_model(request, obj, form, change)