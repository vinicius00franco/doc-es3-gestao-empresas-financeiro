from django.db import models
from apps.empresas.models import Empresa


class RegraAutomacao(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='regras_automacao')
    nome = models.CharField(max_length=100)
    condicao = models.JSONField()  # ex.: {"cnpj": "..", "descricao_contains": ".."}
    acao = models.JSONField()      # ex.: {"categoria_id": 1}
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'regras_automacao'
