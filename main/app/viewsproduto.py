from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.models import User
from models import Produto
from .serializersproduto import (
    ProdutoSerializer,
    ProdutoCreateSerializer,
    ProdutoUpdateSerializer
)

@api_view(['POST'])
def criar_produto(request):
    
    serializer = ProdutoCreateSerializer(data=request.data)
    if serializer.is_valid is True:
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
def update_produto(request, id):
    
    
    try:
        produto = Produto.objects.get(id=id)
    except Produto.DoesNotExist:
        return Response({"error": "Produto não encontrado."}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProdutoUpdateSerializer(data=request.data)
    if serializer.is_valid is True:
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_produto(request, id):
    try:
        produto = Produto.objects.get(id=id)
    except Produto.DoesNotExist:
        return Response({"error": "Produto não encontrado."}, status=status.HTTP_404_NOT_FOUND)
    
    produto.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
        
        