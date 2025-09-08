from rest_framework import serializers
from .models import Empresa
from core.sanitizers import sanitize_text_input, validate_cnpj_format


class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = [
            'id', 'cnpj', 'razao_social', 'nome_fantasia', 
            'tipo_empresa', 'regime_tributario', 'ativa', 'empresa_padrao', 
            'criado_em', 'atualizado_em'
        ]
        read_only_fields = ['id', 'criado_em', 'atualizado_em']

    def validate_cnpj(self, value):
        if not validate_cnpj_format(value):
            raise serializers.ValidationError("CNPJ deve ter 14 dígitos.")
        cnpj = ''.join(filter(str.isdigit, value))
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}"
    
    def validate_razao_social(self, value):
        return sanitize_text_input(value)
    
    def validate_nome_fantasia(self, value):
        return sanitize_text_input(value) if value else value

    def create(self, validated_data):
        user = self.context['request'].user
        # Verifica limite de empresas pelo plano do usuário (se existir assinatura)
        try:
            assinatura = getattr(user, 'assinatura', None)
            if assinatura and not assinatura.pode_criar_empresa():
                raise serializers.ValidationError("Limite de empresas atingido pelo plano atual.")
        except Exception:
            # Se houver qualquer erro ao verificar, segue sem bloquear
            pass

        validated_data['usuario'] = user
        return super().create(validated_data)


class EmpresaResumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ['id', 'razao_social', 'nome_fantasia', 'ativa']