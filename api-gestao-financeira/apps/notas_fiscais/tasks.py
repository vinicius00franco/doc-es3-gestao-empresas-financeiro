from celery import shared_task
from django.utils import timezone
from .models import NotaFiscal
from apps.transacoes.models import Fornecedor, Transacao, Categoria


@shared_task
def processar_nota_fiscal(nota_fiscal_id):
    """
    Task assíncrona para processar nota fiscal
    """
    try:
        nota_fiscal = NotaFiscal.objects.get(id=nota_fiscal_id)
        nota_fiscal.status = 'processing'
        nota_fiscal.save()
        
        # Simular processamento (substituir por lógica real)
        dados_mock = {
            'cnpj_emissor': '12.345.678/0001-90',
            'razao_social': 'Fornecedor ABC LTDA',
            'valor_total': '1500.00',
            'data_emissao': '2025-01-20'
        }
        
        # Criar ou buscar fornecedor
        fornecedor, created = Fornecedor.objects.get_or_create(
            empresa=nota_fiscal.empresa,
            cnpj=dados_mock['cnpj_emissor'],
            defaults={
                'razao_social': dados_mock['razao_social'],
                'criado_automaticamente': True
            }
        )
        
        # Buscar categoria padrão
        categoria_padrao = Categoria.objects.filter(
            empresa=nota_fiscal.empresa,
            tipo_transacao='saida',
            categoria_padrao=True
        ).first()
        
        # Criar transação
        transacao = Transacao.objects.create(
            empresa=nota_fiscal.empresa,
            categoria=categoria_padrao,
            fornecedor=fornecedor,
            descricao=f"NF-e {dados_mock['razao_social']}",
            valor=dados_mock['valor_total'],
            data_transacao=dados_mock['data_emissao'],
            tipo_transacao='saida',
            numero_documento=nota_fiscal.arquivo_original
        )
        
        # Atualizar nota fiscal
        nota_fiscal.fornecedor = fornecedor
        nota_fiscal.transacao = transacao
        nota_fiscal.cnpj_emissor = dados_mock['cnpj_emissor']
        nota_fiscal.razao_social_emissor = dados_mock['razao_social']
        nota_fiscal.valor_total = dados_mock['valor_total']
        nota_fiscal.data_emissao = dados_mock['data_emissao']
        nota_fiscal.dados_extraidos = dados_mock
        nota_fiscal.status = 'processed'
        nota_fiscal.processado_em = timezone.now()
        nota_fiscal.save()
        
        return f"Nota fiscal {nota_fiscal_id} processada com sucesso"
        
    except Exception as e:
        nota_fiscal.status = 'failed'
        nota_fiscal.erro_processamento = str(e)
        nota_fiscal.save()
        raise