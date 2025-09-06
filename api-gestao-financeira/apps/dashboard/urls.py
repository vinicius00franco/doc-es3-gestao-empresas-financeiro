from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_resumo, name='dashboard-resumo'),
]