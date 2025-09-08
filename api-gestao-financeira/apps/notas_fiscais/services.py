"""Serviços externos simulados (mocks fiéis ao esperado em produção)."""
from datetime import date


def parse_nfe_xml(file_bytes: bytes):
    """Simula parsing de XML da NF-e retornando campos essenciais.
    Em produção, usar biblioteca específica (ex.: nfelib) e validar schema.
    """
    # Simulação simples
    return {
        'chave_acesso': '12345678901234567890123456789012345678901234',
        'cnpj_emissor': '12.345.678/0001-90',
        'razao_social': 'Fornecedor ABC LTDA',
        'valor_total': '1500.00',
        'data_emissao': str(date.today()),
    }


def payment_gateway_create_checkout(plano_id: int):
    """Simula criação de sessão de checkout em gateway de pagamento."""
    return {
        'payment_url': f'https://payment-gateway.com/checkout/{plano_id}',
        'session_id': f'cs_{plano_id}_sim'
    }
