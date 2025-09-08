from django.urls import path
from . import views

urlpatterns = [
    path('agendamentos/', views.AgendamentoListCreateView.as_view(), name='agendamento-list-create'),
    path('agenda/daily-balance/', views.saldo_diario, name='agenda-saldo-diario'),
]
