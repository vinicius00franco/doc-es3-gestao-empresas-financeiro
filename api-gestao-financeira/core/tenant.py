from django.db import models
from django.core.exceptions import ValidationError
from threading import local

_thread_local = local()


class TenantManager(models.Manager):
    """Manager que filtra automaticamente por tenant"""
    
    def get_queryset(self):
        queryset = super().get_queryset()
        tenant_id = getattr(_thread_local, 'tenant_id', None)
        if tenant_id and hasattr(self.model, 'tenant_id'):
            return queryset.filter(tenant_id=tenant_id)
        return queryset


class TenantMixin(models.Model):
    """Mixin para adicionar tenant_id aos modelos"""
    
    tenant_id = models.CharField(max_length=50, db_index=True)
    
    objects = TenantManager()
    all_objects = models.Manager()  # Manager sem filtro de tenant
    
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        if not self.tenant_id:
            tenant_id = getattr(_thread_local, 'tenant_id', None)
            if not tenant_id:
                raise ValidationError("Tenant ID é obrigatório")
            self.tenant_id = tenant_id
        super().save(*args, **kwargs)


def set_current_tenant(tenant_id):
    """Define o tenant atual para a thread"""
    _thread_local.tenant_id = tenant_id


def get_current_tenant():
    """Obtém o tenant atual da thread"""
    return getattr(_thread_local, 'tenant_id', None)


def clear_current_tenant():
    """Limpa o tenant atual da thread"""
    if hasattr(_thread_local, 'tenant_id'):
        delattr(_thread_local, 'tenant_id')