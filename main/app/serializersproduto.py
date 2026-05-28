from rest_framework import serializers
from app.models import Produto
import enchant 


class ProdutoSerializer(serializers.ModelSerializer):
    """Serializer para listar e atualizar produtos"""
    
    class Meta:
        model = Produto
        fields = ['id', 'nome_produto', 'quantidade', 'valor']
        read_only_fields = ['id']
        
class ProdutoCreateSerializer(serializers.ModelSerializer):
    """Serializer para criar produtos"""
    
    class Meta:
        model = Produto
        fields = ['id', 'nome_produto', 'quantidade', 'valor']
        read_only_fields = ['id']
        
    def validate_quantidade(self, value):
        
        if value<0:
            raise serializers.ValidationError("Quantidade não pode ser negativa.")
        return value
    def validate_valor(self, value):
        if value< 5:
            raise serializers.ValidationError("Valor mínimo é R$5,00.")
        return value
    def validate_nome_produto(self,value):
        d = enchant.Dict("pt_BR")
        if not d.check(value):
            raise serializers.ValidationError("Nome do produto contém palavras inválidas.")
        return value
        return super().validate(validade_data)

class ProdutoUpdateSerializer(serializers.ModelSerializer):
    """Serializer para atualizar produtos"""
    
    class Meta:
        model = Produto
        fields = [ 'nome_produto', 'quantidade', 'valor']
        
    def validate_quantidade(self, value):
        if value<0:
            raise serializers.ValidationError("Quantidade não pode ser negativa.")
        return value
    def validate_valor(self, value):
        if value< 5:
            raise serializers.ValidationError("Valor mínimo é R$5,00.")
        return value
    def validate_nome_produto(self,value):
        d = enchant.Dict("pt_BR")
        if not d.check(value):
            raise serializers.ValidationError("Nome do produto contém palavras inválidas.")
        return value
    def update(self, instance, validated_data):
        """Permite atualização parcial (PATCH)"""
        if 'nome_produto' in validated_data and \
              'quantidade' in validated_data and \
                'valor' in validated_data:
            instance.nome_produto = validated_data.get('nome_produto', instance.nome_produto)
            instance.quantidade = validated_data.get('quantidade', instance.quantidade)
            instance.valor = validated_data.get('valor', instance.valor)
            instance.save()
        return instance
