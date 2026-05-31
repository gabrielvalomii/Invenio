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
        if 'quantidade' in validated_data:
            quantidade_a_substituir = validated_data['quantidade']
            if quantidade_a_substituir > 0:
                instance.quantidade = quantidade_a_substituir - instance.quantidade
            else:
                raise serializers.ValidationError("Quantidade deve ser maior que zero para atualização.")
        if 'valor' in validated_data:
            instance.valor = validated_data['valor']
        if 'nome_produto' in validated_data:
            instance.nome_produto = validated_data['nome_produto']
        instance.save()
        return instance
