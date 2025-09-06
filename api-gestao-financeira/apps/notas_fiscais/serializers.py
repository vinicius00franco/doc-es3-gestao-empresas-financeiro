from rest_framework import serializers
from .models import NotaFiscal
from apps.transacoes.serializers import FornecedorSerializer


class NotaFiscalUploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)
    empresa_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = NotaFiscal
        fields = ['file', 'empresa_id']

    def validate_file(self, value):
        # Validar extensão do arquivo
        allowed_extensions = ['.xml', '.pdf']
        file_extension = value.name.lower().split('.')[-1]
        
        if f'.{file_extension}' not in allowed_extensions:
            raise serializers.ValidationError(
                "Apenas arquivos XML e PDF são permitidos."
            )
        
        # Validar tamanho (máx 10MB)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError(
                "Arquivo muito grande. Máximo 10MB."
            )
        
        return value

    def validate_empresa_id(self, value):
        user = self.context['request'].user
        if not user.empresas.filter(id=value).exists():
            raise serializers.ValidationError(
                "Empresa não encontrada ou não pertence ao usuário."
            )
        return value

    def create(self, validated_data):
        file = validated_data.pop('file')
        empresa_id = validated_data.pop('empresa_id')
        
        from apps.empresas.models import Empresa
        empresa = Empresa.objects.get(id=empresa_id)
        
        # Determinar tipo do arquivo
        file_extension = file.name.lower().split('.')[-1]
        tipo_arquivo = 'XML' if file_extension == 'xml' else 'PDF'
        
        nota_fiscal = NotaFiscal.objects.create(
            empresa=empresa,
            arquivo_original=file.name,
            caminho_arquivo=file,
            tipo_arquivo=tipo_arquivo,
            status='uploaded'
        )
        
        # Aqui seria disparado o processamento assíncrono
        # processar_nota_fiscal.delay(nota_fiscal.id)
        
        return nota_fiscal


class NotaFiscalSerializer(serializers.ModelSerializer):
    fornecedor = FornecedorSerializer(read_only=True)
    
    class Meta:
        model = NotaFiscal
        fields = [
            'id', 'arquivo_original', 'tipo_arquivo', 'status',
            'chave_acesso', 'cnpj_emissor', 'razao_social_emissor',
            'valor_total', 'data_emissao', 'fornecedor', 'transacao',
            'erro_processamento', 'criado_em', 'processado_em'
        ]
        read_only_fields = [
            'id', 'chave_acesso', 'cnpj_emissor', 'razao_social_emissor',
            'valor_total', 'data_emissao', 'dados_extraidos',
            'criado_em', 'processado_em'
        ]


class NotaFiscalStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotaFiscal
        fields = [
            'id', 'status', 'dados_extraidos', 'transacao',
            'erro_processamento', 'processado_em'
        ]