from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta
from apps.transacoes.models import Transacao, Categoria
from apps.notas_fiscais.models import NotaFiscal


def _parse_date_safely(date_str):
    """Parse date string safely"""
    try:
        return datetime.fromisoformat(date_str).date()
    except (ValueError, TypeError):
        return None


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_resumo(request):
    user = request.user
    empresa_padrao = user.empresas.filter(empresa_padrao=True).first()
    
    if not empresa_padrao:
        return Response({
            'error': 'Usuário deve ter uma empresa padrão'
        }, status=400)
    
    # Período padrão: últimos 30 dias
    data_fim = timezone.now().date()
    data_inicio = data_fim - timedelta(days=30)
    
    # Parâmetros de filtro opcionais com validação
    if request.GET.get('data_inicio'):
        parsed_date = _parse_date_safely(request.GET.get('data_inicio'))
        if parsed_date:
            data_inicio = parsed_date
    
    if request.GET.get('data_fim'):
        parsed_date = _parse_date_safely(request.GET.get('data_fim'))
        if parsed_date:
            data_fim = parsed_date
    
    # Transações no período
    transacoes = Transacao.objects.filter(
        empresa=empresa_padrao,
        data_transacao__gte=data_inicio,
        data_transacao__lte=data_fim,
        status='confirmada'
    )
    
    # Resumo financeiro
    entradas = transacoes.filter(tipo_transacao='entrada').aggregate(
        total=Sum('valor')
    )['total'] or 0
    
    saidas = transacoes.filter(tipo_transacao='saida').aggregate(
        total=Sum('valor')
    )['total'] or 0
    
    saldo = entradas - saidas
    
    # Contadores
    total_transacoes = transacoes.count()
    
    # Entradas por categoria
    entradas_por_categoria = transacoes.filter(
        tipo_transacao='entrada'
    ).values(
        'categoria__nome'
    ).annotate(
        valor=Sum('valor')
    ).order_by('-valor')[:5]
    
    # Saídas por categoria
    saidas_por_categoria = transacoes.filter(
        tipo_transacao='saida'
    ).values(
        'categoria__nome'
    ).annotate(
        valor=Sum('valor')
    ).order_by('-valor')[:5]
    
    # Notas fiscais (se existir a app)
    try:
        notas_fiscais_mes = NotaFiscal.objects.filter(
            empresa=empresa_padrao,
            criado_em__gte=data_inicio,
            criado_em__lte=data_fim
        )
        
        processamento_fiscal = {
            'pendentes': notas_fiscais_mes.filter(status='uploaded').count(),
            'processadas_mes': notas_fiscais_mes.filter(status='processed').count(),
            'erro_processamento': notas_fiscais_mes.filter(status='failed').count(),
        }
    except:
        processamento_fiscal = {
            'pendentes': 0,
            'processadas_mes': 0,
            'erro_processamento': 0,
        }
    
    return Response({
        'periodo': {
            'data_inicio': data_inicio,
            'data_fim': data_fim
        },
        'resumo': {
            'total_entradas': f"{entradas:.2f}",
            'total_saidas': f"{saidas:.2f}",
            'saldo': f"{saldo:.2f}",
            'transacoes_count': total_transacoes,
            'notas_fiscais_processadas': processamento_fiscal['processadas_mes']
        },
        'entradas_por_categoria': [
            {
                'categoria': item['categoria__nome'] or 'Sem categoria',
                'valor': f"{item['valor']:.2f}"
            }
            for item in entradas_por_categoria
        ],
        'saidas_por_categoria': [
            {
                'categoria': item['categoria__nome'] or 'Sem categoria',
                'valor': f"{item['valor']:.2f}"
            }
            for item in saidas_por_categoria
        ],
        'processamento_fiscal': processamento_fiscal
    })