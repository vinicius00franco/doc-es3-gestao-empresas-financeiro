from rest_framework import serializers
from .models import Plano, Assinatura


class PlanoSerializer(serializers.ModelSerializer):
    eh_gratuito = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Plano
        fields = [
            'id', 'nome', 'descricao', 'preco', 'eh_gratuito',
            'limite_transacoes', 'limite_empresas', 'permite_relatorios',
            'permite_exportacao', 'permite_notas_fiscais'
        ]


class AssinaturaSerializer(serializers.ModelSerializer):
    plano = PlanoSerializer(read_only=True)
    pode_criar_transacao = serializers.BooleanField(read_only=True)
    pode_criar_empresa = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Assinatura
        fields = [
            'id', 'plano', 'status', 'data_inicio', 'data_fim',
            'valor_pago', 'pode_criar_transacao', 'pode_criar_empresa',
            'criado_em', 'atualizado_em'
        ]
        read_only_fields = [
            'id', 'data_inicio', 'data_fim', 'valor_pago',
            'criado_em', 'atualizado_em'
        ]


class UpgradeAssinaturaSerializer(serializers.Serializer):
    plano_id = serializers.IntegerField()
    
    def validate_plano_id(self, value):
        try:
            plano = Plano.objects.get(id=value, ativo=True)
            if plano.eh_gratuito:
                raise serializers.ValidationError("Não é possível fazer upgrade para plano gratuito.")
            return value
        except Plano.DoesNotExist:
            raise serializers.ValidationError("Plano não encontrado.")