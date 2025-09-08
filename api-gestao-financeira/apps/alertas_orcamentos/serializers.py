from rest_framework import serializers
from .models import Alerta, OrcamentoMensal


class AlertaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alerta
        fields = ['id', 'tipo', 'canal', 'antecedencia_dias', 'ativo', 'parametros', 'criado_em']
        read_only_fields = ['id', 'criado_em']


class OrcamentoMensalSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrcamentoMensal
        fields = ['id', 'categoria_id', 'mes', 'valor_planejado', 'criado_em']
        read_only_fields = ['id', 'criado_em']
