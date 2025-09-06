from rest_framework import serializers
from .models import Empresa


class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = [
            'id', 'cnpj', 'razao_social', 'nome_fantasia', 
            'tipo_empresa', 'ativa', 'empresa_padrao', 
            'criado_em', 'atualizado_em'
        ]
        read_only_fields = ['id', 'criado_em', 'atualizado_em']

    def validate_cnpj(self, value):
        # Remove formatação do CNPJ
        cnpj = ''.join(filter(str.isdigit, value))
        
        if len(cnpj) != 14:
            raise serializers.ValidationError("CNPJ deve ter 14 dígitos.")
        
        # Formatar CNPJ
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}"

    def create(self, validated_data):
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)


class EmpresaResumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ['id', 'razao_social', 'nome_fantasia', 'ativa']