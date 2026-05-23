from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Produto
from django.contrib.auth.hashers import make_password, check_password
import json
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render
from validate_docbr import CNPJ
from django.core.exceptions import ValidationError

@csrf_exempt
def usuario(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nome = data.get('nome')
            email = data.get('email')
            senha = data.get('senha')
            CNPJ = data.get('CNPJ')
            CNPJ_verificador = CNPJ()
            if not nome or not email or not senha or not CNPJ:
                return JsonResponse({'erros': 'Todos os campos são obrigatórios.'}, status=400)
            if not CNPJ_verificador.validate(CNPJ):
                return JsonResponse({'erros': 'CNPJ inválido.'}, status=400)
            if User.objects.filter(CNPJ=CNPJ, nome=nome, email=email).exists():
                return JsonResponse({'erros': 'algum dos campos já cadastrado.'}, status=400)
            senha_hash = make_password(senha)
            user = User.objects.create(
                nome = nome,
                email = email,
                senha = senha_hash,
                CNPJ = CNPJ
            )
            return JsonResponse({'message': 'Usuário criado com sucesso.', 'id':user.id, 'nome': user.nome, 'email': user.email, 'CNPJ': user.CNPJ}, status=201)
            return render (request, 'login.html')
        except Exception as e:
            return JsonResponse({'erros': str(e)}, status=400)
    return JsonResponse({'erros': 'Método não permitido.'}, status=405)
    return render (request, 'cadastro.html')

@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            senha = data.get('senha')
            if not email or not senha:
                return JsonResponse({'erros': 'Email e senha são obrigatórios.'}, status=400)
            user = User.objects.filter(email=email).first()
            if not user:
                return JsonResponse({'erros': 'Usuário não encontrado.'}, status=404)
            if not check_password(senha, user.senha):
                return JsonResponse({'erros': 'Senha incorreta.'}, status=400)
            
            request.session['user_id'] = user.id
            request.session['user_nome'] = user.nome
            
            return JsonResponse({'message': 'Login bem-sucedido.', 'id':user.id, 'nome': user.nome, 'email': user.email}, status=200)
            return render (request, 'home.html')
        except Exception as e:
            return JsonResponse({'erros': str(e)}, status=400)
    return JsonResponse({'erros': 'Método não permitido.'}, status=405)
    return render (request, 'login.html')        

@csrf_exempt
def logout(request):
    if request.method in ['POST', 'GET']:
        try:
            request.session.flush()
            return JsonResponse({'message': 'Logout bem-sucedido.'}, status=200)
            return render (request, 'login.html')
        except Exception as e:
            return JsonResponse({'erros': str(e)}, status=400)
        
        

@csrf_exempt
def editar_user(request, id):
    if request.method in ['PUT', 'PATCH', 'POST']:
        try:
            data = json.loads(request.body)
            user = User.objects.filter(id =id).first()
            if not user:
                return JsonResponse({'erros': 'Usuário não encontrado.'}, status=404)
            nome = data.get('nome')
            senha = data.get('senha')
            if nome:
                User.nome = nome
            if senha:
                User.senha = make_password(senha)
            user.save()
            return JsonResponse({'message': 'Usuário atualizado com sucesso.', 'id':user.id, 'nome': user.nome, 'email': user.email, 'CNPJ': user.CNPJ}, status=200)
        except Exception as e:
            return JsonResponse({'erros': str(e)},status=400)
    return JsonResponse({'erros': 'Método não permitido.'}, status=405)
    return render (request, 'login.html')

@csrf_exempt
def deletar_user(request, id):
    if request.method in ['DELETE', 'POST']:
        try:
            user = User.objects.filter(id=id).first()
            if not user:
                return JsonResponse({'erros': 'Usuário não encontrado.'}, status=404)
            user.delete()
            return JsonResponse({'message': 'Usuário deletado com sucesso.'}, status=200)
        except Exception as e:
            return JsonResponse({'erros': str(e)}, status=400)
    return JsonResponse({'erros': 'Método não permitido.'}, status=405)
    return render (request, 'cadastro.html')
    
        
@csrf_exempt
def produto(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nome_produto = data.get('nome_produto')
            quantidade = data.get('quantidade')
            valor = data.get('valor')
            if not nome_produto or not quantidade or not valor:
                return JsonResponse({'erros': 'Todos os campos são obrigatórios.'}, status=400)
            produto = Produto.objects.create(
                nome_produto = nome_produto,
                quantidade = quantidade,
                valor = valor
            )
            return JsonResponse ({'message': 'Produto criado com sucesso.', 'id':produto.id, 'nome_produto': produto.nome_produto, 'quantidade': produto.quantidade, 'valor': produto.valor}, status=201)
        except Exception as e:
            return JsonResponse({'erros': str(e)}, status=400)
    return JsonResponse({'erros': 'Método não permitido.'}, status=405)

@csrf_exempt
def editar_produto(request, id):
    if request.method in ['PUT', 'PATCH', 'POST']:
        try:
            data = json.loads(request.body)
            produto = Produto.objects.filter(id=id).first()
            if not produto:
                return JsonResponse({'erros': 'Produto não encontrado.'}, status=404)
            quantidade = data.get('quantidade')
            valor = data.get('valor')
            if quantidade > 0:
                Produto.quantidade -= quantidade
                return JsonResponse({'message': 'Produto atualizado com sucesso.', 'id':produto.id, 'nome_produto': produto.nome_produto, 'quantidade': produto.quantidade, 'valor': produto.valor}, status=200)
            if valor:
                Produto.valor = valor
                return JsonResponse({'message': 'Produto atualizado com sucesso.', 'id':produto.id, 'nome_produto': produto.nome_produto, 'quantidade': produto.quantidade, 'valor': produto.valor}, status=200)
            produto.save()
        except Exception as e:
            return JsonResponse({'erros': str(e)}, status=400)
    return JsonResponse({'erros': 'Método não permitido.'}, status=405)

@csrf_exempt
def deletar_produto(request, id):
    if request.method in ['DELETE', 'POST']:
        try:
            produto = Produto.objects.filter(id=id).first()
            if not produto:
                return JsonResponse({'erros': 'Produto não encontrado.'}, status=404)
            produto.delete()
            return JsonResponse({'message': 'Produto deletado com sucesso.'}, status=200)
        except Exception as e:
            return JsonResponse({'erros': str(e)}, status=400)
    return JsonResponse({'erros': 'Método não permitido.'}, status=405)

                
            
            
        