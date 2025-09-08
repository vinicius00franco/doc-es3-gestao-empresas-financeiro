from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import NotaFiscal
from .serializers import (
    NotaFiscalUploadSerializer,
    NotaFiscalSerializer,
    NotaFiscalStatusSerializer
)
from apps.transacoes.models import Fornecedor, Transacao, Categoria


@api_view(['POST'])
def upload_nota_fiscal(request):
    serializer = NotaFiscalUploadSerializer(
        data=request.data, 
        context={'request': request}
    )
    
    if serializer.is_valid():
        nota_fiscal = serializer.save()
        
        # Disparar processamento assíncrono
        from .tasks import processar_nota_fiscal
        processar_nota_fiscal.delay(nota_fiscal.id)
        
        return Response({
            'id': nota_fiscal.id,
            'status': nota_fiscal.status,
            'arquivo_original': nota_fiscal.arquivo_original,
            'empresa_id': nota_fiscal.empresa.id,
            'criado_em': nota_fiscal.criado_em
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def processar_nota_fiscal_mock(nota_fiscal):
    """
    Simulação do processamento de nota fiscal
    Em produção, seria feito com Celery + biblioteca de extração XML
    """
    try:
        nota_fiscal.status = 'processing'
        nota_fiscal.save()
        
        # Simular extração via serviço dedicado
        try:
            from .services import parse_nfe_xml
            conteudo = None
            try:
                if nota_fiscal.caminho_arquivo and hasattr(nota_fiscal.caminho_arquivo, 'file'):
                    conteudo = nota_fiscal.caminho_arquivo.file.read()
            except Exception:
                conteudo = None
            dados_mock = parse_nfe_xml(conteudo or b'')
        except Exception:
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
        
        # Buscar categoria padrão para saída
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
        
    except Exception as e:
        nota_fiscal.status = 'failed'
        nota_fiscal.erro_processamento = str(e)
        nota_fiscal.save()


class NotaFiscalStatusView(generics.RetrieveAPIView):
    serializer_class = NotaFiscalStatusSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return NotaFiscal.objects.filter(empresa__usuario=user)


class NotaFiscalListView(generics.ListAPIView):
    serializer_class = NotaFiscalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return NotaFiscal.objects.filter(
            empresa__usuario=user
        ).select_related('fornecedor', 'transacao').order_by('-criado_em')