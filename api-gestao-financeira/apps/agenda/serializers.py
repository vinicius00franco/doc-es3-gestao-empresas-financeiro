from rest_framework import serializers
from .models import Agendamento, ProjecaoSaldo


class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = ['id', 'descricao', 'valor', 'data_vencimento', 'recorrencia', 'tipo', 'status', 'criado_em', 'atualizado_em']
        read_only_fields = ['id', 'criado_em', 'atualizado_em']


class ProjecaoSaldoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjecaoSaldo
        fields = ['data', 'saldo_previsto']
