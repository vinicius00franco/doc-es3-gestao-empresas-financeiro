from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import Usuario, ConfiguracaoUsuario


class UsuarioRegistroSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True, validators=[validate_password])
    senha_confirmacao = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'senha', 'senha_confirmacao']

    def validate(self, attrs):
        if attrs['senha'] != attrs['senha_confirmacao']:
            raise serializers.ValidationError("As senhas não coincidem.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('senha_confirmacao')
        usuario = Usuario.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            nome=validated_data['nome'],
            password=validated_data['senha']
        )
        ConfiguracaoUsuario.objects.create(usuario=usuario)
        return usuario


class UsuarioLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    senha = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        senha = attrs.get('senha')

        if email and senha:
            usuario = authenticate(username=email, password=senha)
            if not usuario:
                raise serializers.ValidationError('Credenciais inválidas.')
            if not usuario.ativo:
                raise serializers.ValidationError('Conta desativada.')
            attrs['usuario'] = usuario
        return attrs


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'email', 'criado_em', 'atualizado_em']
        read_only_fields = ['id', 'criado_em', 'atualizado_em']


class ConfiguracaoUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracaoUsuario
        fields = [
            'tema', 'moeda', 'formato_data', 'fuso_horario',
            'notificacoes_email', 'notificacoes_push', 'backup_automatico'
        ]