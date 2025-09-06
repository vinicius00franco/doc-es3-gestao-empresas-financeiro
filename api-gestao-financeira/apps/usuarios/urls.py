from django.urls import path
from . import views

urlpatterns = [
    # Autenticação
    path('auth/register/', views.registro, name='registro'),
    path('auth/login/', views.login, name='login'),
    path('auth/refresh/', views.refresh_token, name='refresh_token'),
    
    # Perfil
    path('users/profile/', views.PerfilView.as_view(), name='perfil'),
    path('users/configuracao/', views.ConfiguracaoView.as_view(), name='configuracao'),
]