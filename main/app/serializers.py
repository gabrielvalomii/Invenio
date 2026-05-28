from rest_framework import serializers
from app.models import User
from django.contrib.auth.hashers import make_password, check_password
from validate_docbr import CNPJ as CNPJValidator


class UserSerializer(serializers.ModelSerializer):
    """Serializer para listar e atualizar usuários"""
    
    class Meta:
        model = User
        fields = ['id', 'nome', 'email', 'CNPJ']
        read_only_fields = ['id', 'CNPJ']


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer para criar usuários (cadastro)"""
    senha = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ['id', 'nome', 'email', 'senha', 'CNPJ']
        read_only_fields = ['id']
    
    def validate_CNPJ(self, value):
        """Valida CNPJ"""
        cnpj_validator = CNPJValidator()
        if not cnpj_validator.validate(value):
            raise serializers.ValidationError("CNPJ inválido.")
        return value
    
    def validate_email(self, value):
        """Verifica se email já existe"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email já cadastrado.")
        return value
    
    def validate(self, value):
        """Validação cruzada - verifica se CNPJ já existe"""
        if User.objects.filter(CNPJ=value).exists():
            raise serializers.ValidationError({"CNPJ": "CNPJ já cadastrado."})
        return value
    
    def create(self, validated_data):
        """Cria usuário com senha hashada"""
        validated_data['senha'] = make_password(validated_data['senha'])
        return super().create(validated_data)


class LoginSerializer(serializers.Serializer):
    """Serializer para login"""
    email = serializers.EmailField()
    senha = serializers.CharField(write_only=True)
    
    def validate(self, data):
        """Valida credenciais"""
        email = data.get('email')
        senha = data.get('senha')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Usuário não encontrado.")
        
        if not check_password(senha, user.senha):
            raise serializers.ValidationError("Senha incorreta.")
        
        # Adiciona o usuário aos dados validados
        data['user'] = user
        return data


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer para atualizar usuário"""
    senha = serializers.CharField(write_only=True, required=False, min_length=6)
    
    class Meta:
        model = User
        fields = ['nome', 'senha']
    
    def update(self, instance, validated_data):
        """Atualiza usuário, hasheando senha se fornecida"""
        if 'senha' in validated_data:
            validated_data['senha'] = make_password(validated_data['senha'])
        return super().update(instance, validated_data)