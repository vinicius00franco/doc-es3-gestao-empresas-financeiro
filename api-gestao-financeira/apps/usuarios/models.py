from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']

    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.nome


class ConfiguracaoUsuario(models.Model):
    TEMA_CHOICES = [
        ('claro', 'Claro'),
        ('escuro', 'Escuro'),
        ('auto', 'Automático'),
    ]
    
    FORMATO_DATA_CHOICES = [
        ('DD/MM/YYYY', 'DD/MM/YYYY'),
        ('MM/DD/YYYY', 'MM/DD/YYYY'),
        ('YYYY-MM-DD', 'YYYY-MM-DD'),
    ]

    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='configuracao')
    tema = models.CharField(max_length=10, choices=TEMA_CHOICES, default='auto')
    moeda = models.CharField(max_length=3, default='BRL')
    formato_data = models.CharField(max_length=10, choices=FORMATO_DATA_CHOICES, default='DD/MM/YYYY')
    fuso_horario = models.CharField(max_length=50, default='America/Sao_Paulo')
    notificacoes_email = models.BooleanField(default=True)
    notificacoes_push = models.BooleanField(default=True)
    backup_automatico = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'configuracoes_usuario'
        verbose_name = 'Configuração do Usuário'
        verbose_name_plural = 'Configurações dos Usuários'


class TokenRecuperacao(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    usado = models.BooleanField(default=False)
    expira_em = models.DateTimeField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tokens_recuperacao'
        verbose_name = 'Token de Recuperação'
        verbose_name_plural = 'Tokens de Recuperação'


class LogAtividade(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    acao = models.CharField(max_length=100)
    detalhes = models.JSONField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'logs_atividade'
        verbose_name = 'Log de Atividade'
        verbose_name_plural = 'Logs de Atividade'
        ordering = ['-criado_em']