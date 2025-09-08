from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({'status': 'healthy'})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health-check'),
    # django-prometheus expõe /metrics quando incluído na raiz
    path('', include('django_prometheus.urls')),
    # Também incluir explicitamente para garantir
    path('metrics/', include('django_prometheus.urls')),
    path('api/v1/', include('apps.usuarios.urls')),
    path('api/v1/empresas/', include('apps.empresas.urls')),
    path('api/v1/', include('apps.transacoes.urls')),
    path('api/v1/', include('apps.assinaturas.urls')),
    path('api/v1/dashboard/', include('apps.dashboard.urls')),
    path('api/v1/', include('apps.notas_fiscais.urls')),
    path('api/v1/', include('apps.agenda.urls')),
    path('api/v1/', include('apps.alertas_orcamentos.urls')),
    path('api/v1/', include('apps.automacoes.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)