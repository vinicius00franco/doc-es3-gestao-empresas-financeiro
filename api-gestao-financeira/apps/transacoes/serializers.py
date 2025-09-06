from rest_framework import serializers
from .models import Transacao, Categoria, Fornecedor
from apps.empresas.serializers import EmpresaResumoSerializer


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
        cnpj = ''.join(filter(str.isdigit, value))
        if len(cnpj) != 14:
            raise serializers.ValidationError("CNPJ deve ter 14 dígitos.")
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}"


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


class TransacaoResumoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)
    
    class Meta:
        model = Transacao
        fields = ['id', 'descricao', 'valor', 'data_transacao', 'tipo_transacao', 'categoria_nome']