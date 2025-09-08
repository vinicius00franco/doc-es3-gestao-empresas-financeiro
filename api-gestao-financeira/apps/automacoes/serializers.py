from rest_framework import serializers
from .models import RegraAutomacao


class RegraAutomacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegraAutomacao
        fields = ['id', 'nome', 'condicao', 'acao', 'ativo', 'criado_em']
        read_only_fields = ['id', 'criado_em']
