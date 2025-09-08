from rest_framework import serializers
from django.utils import timezone
from .models import Transacao, Categoria, Fornecedor
from apps.empresas.serializers import EmpresaResumoSerializer
from core.sanitizers import sanitize_text_input, validate_cnpj_format


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = [
            'id', 'nome', 'descricao', 'cor', 'icone', 
            'tipo_transacao', 'ativa', 'categoria_padrao'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        # Pega a empresa padrão do usuário
        empresa_padrao = self.context['request'].user.empresas.filter(empresa_padrao=True).first()
        if not empresa_padrao:
            raise serializers.ValidationError("Usuário deve ter uma empresa padrão.")
        
        validated_data['empresa'] = empresa_padrao
        return super().create(validated_data)


class FornecedorSerializer(serializers.ModelSerializer):
    total_transacoes = serializers.SerializerMethodField()

    class Meta:
        model = Fornecedor
        fields = [
            'id', 'cnpj', 'razao_social', 'nome_fantasia', 
            'email', 'telefone', 'endereco', 'criado_automaticamente',
            'ativo', 'total_transacoes'
        ]
        read_only_fields = ['id', 'criado_automaticamente', 'total_transacoes']

    def get_total_transacoes(self, obj):
        return obj.transacao_set.count()

    def validate_cnpj(self, value):
        if not validate_cnpj_format(value):
            raise serializers.ValidationError("CNPJ deve ter 14 dígitos.")
        cnpj = ''.join(filter(str.isdigit, value))
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}"
    
    def validate_razao_social(self, value):
        return sanitize_text_input(value)
    
    def validate_nome_fantasia(self, value):
        return sanitize_text_input(value) if value else value
    
    def validate_endereco(self, value):
        return sanitize_text_input(value) if value else value


class TransacaoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)
    fornecedor_nome = serializers.CharField(source='fornecedor.razao_social', read_only=True)
    valor_formatado = serializers.CharField(read_only=True)

    class Meta:
        model = Transacao
        fields = [
            'id', 'descricao', 'valor', 'valor_formatado', 'data_transacao',
            'tipo_transacao', 'status', 'observacoes', 'numero_documento',
            'forma_pagamento', 'recorrente', 'categoria', 'categoria_nome',
            'fornecedor', 'fornecedor_nome', 'criado_em', 'atualizado_em'
        ]
        read_only_fields = ['id', 'criado_em', 'atualizado_em']

    def create(self, validated_data):
        # Pega a empresa padrão do usuário
        empresa_padrao = self.context['request'].user.empresas.filter(empresa_padrao=True).first()
        if not empresa_padrao:
            raise serializers.ValidationError("Usuário deve ter uma empresa padrão.")
        
        validated_data['empresa'] = empresa_padrao
        return super().create(validated_data)

    def validate(self, attrs):
        # Impedir alteração de tipo_transacao após criação
        if getattr(self, 'instance', None) is not None:
            novo_tipo = attrs.get('tipo_transacao')
            if novo_tipo and novo_tipo != self.instance.tipo_transacao:
                raise serializers.ValidationError({
                    'tipo_transacao': 'O tipo da transação não pode ser alterado após a criação.'
                })

        # Validar se categoria pertence à empresa do usuário
        if 'categoria' in attrs and attrs['categoria']:
            empresa_padrao = self.context['request'].user.empresas.filter(empresa_padrao=True).first()
            if attrs['categoria'].empresa != empresa_padrao:
                raise serializers.ValidationError("Categoria não pertence à empresa do usuário.")
        
        # Validar se fornecedor pertence à empresa do usuário
        if 'fornecedor' in attrs and attrs['fornecedor']:
            empresa_padrao = self.context['request'].user.empresas.filter(empresa_padrao=True).first()
            if attrs['fornecedor'].empresa != empresa_padrao:
                raise serializers.ValidationError("Fornecedor não pertence à empresa do usuário.")
        
        return attrs
    
    def validate_descricao(self, value):
        return sanitize_text_input(value)
    
    def validate_observacoes(self, value):
        return sanitize_text_input(value) if value else value
    
    def validate_numero_documento(self, value):
        return sanitize_text_input(value) if value else value

    def validate_data_transacao(self, value):
        hoje = timezone.now().date()
        if value and value > hoje:
            raise serializers.ValidationError('Data da transação não pode estar no futuro.')
        return value


class TransacaoResumoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)
    
    class Meta:
        model = Transacao
        fields = ['id', 'descricao', 'valor', 'data_transacao', 'tipo_transacao', 'categoria_nome']