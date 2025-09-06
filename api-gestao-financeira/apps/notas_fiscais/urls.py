from django.urls import path
from . import views

urlpatterns = [
    # Notas Fiscais
    path('invoices/upload/', views.upload_nota_fiscal, name='upload-nota-fiscal'),
    path('invoices/<int:pk>/status/', views.NotaFiscalStatusView.as_view(), name='nota-fiscal-status'),
    path('invoices/', views.NotaFiscalListView.as_view(), name='nota-fiscal-list'),
]