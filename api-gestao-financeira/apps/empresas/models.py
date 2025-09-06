from django.db import models
from django.conf import settings


class Empresa(models.Model):
    TIPO_EMPRESA_CHOICES = [
        ('MEI', 'Microempreendedor Individual'),
        ('ME', 'Microempresa'),
        ('EPP', 'Empresa de Pequeno Porte'),
        ('LTDA', 'Sociedade Limitada'),
        ('SA', 'Sociedade Anônima'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='empresas')
    cnpj = models.CharField(max_length=18)
    razao_social = models.CharField(max_length=255)
    nome_fantasia = models.CharField(max_length=255, blank=True)
    tipo_empresa = models.CharField(max_length=10, choices=TIPO_EMPRESA_CHOICES)
    ativa = models.BooleanField(default=True)
    empresa_padrao = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'empresas'
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        unique_together = ['usuario', 'cnpj']
        ordering = ['-empresa_padrao', 'razao_social']

    def __str__(self):
        return self.razao_social

    def save(self, *args, **kwargs):
        # Se é a primeira empresa do usuário, torna padrão
        if not self.pk and not self.usuario.empresas.exists():
            self.empresa_padrao = True
        
        # Se está sendo marcada como padrão, remove das outras
        if self.empresa_padrao:
            Empresa.objects.filter(
                usuario=self.usuario, 
                empresa_padrao=True
            ).exclude(pk=self.pk).update(empresa_padrao=False)
        
        super().save(*args, **kwargs)