from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, ConfiguracaoUsuario, LogAtividade


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['email', 'nome', 'ativo', 'criado_em']
    list_filter = ['ativo', 'criado_em']
    search_fields = ['email', 'nome']
    ordering = ['-criado_em']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('nome',)}),
        ('Permissões', {'fields': ('ativo', 'is_staff', 'is_superuser')}),
        ('Datas Importantes', {'fields': ('last_login', 'criado_em', 'atualizado_em')}),
    )
    
    readonly_fields = ['criado_em', 'atualizado_em']


@admin.register(ConfiguracaoUsuario)
class ConfiguracaoUsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'tema', 'moeda', 'notificacoes_email']
    list_filter = ['tema', 'moeda', 'notificacoes_email']
    search_fields = ['usuario__email', 'usuario__nome']


@admin.register(LogAtividade)
class LogAtividadeAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'acao', 'ip_address', 'criado_em']
    list_filter = ['acao', 'criado_em']
    search_fields = ['usuario__email', 'acao']
    readonly_fields = ['criado_em']