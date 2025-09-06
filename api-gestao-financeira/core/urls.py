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
    path('api/v1/', include('apps.usuarios.urls')),
    path('api/v1/empresas/', include('apps.empresas.urls')),
    path('api/v1/', include('apps.transacoes.urls')),
    path('api/v1/', include('apps.assinaturas.urls')),
    path('api/v1/dashboard/', include('apps.dashboard.urls')),
    path('api/v1/', include('apps.notas_fiscais.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)