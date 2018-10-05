import json
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from med.models import Users


@api_view(["GET"])
def index(request):
    return render(request, 'index.html')


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'mensagem': 'Passe o login e a senha.'},
                        status=HTTP_200_OK)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'mensagem': 'Credenciais inválidas.'},
                        status=HTTP_200_OK)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)


@api_view(['GET', 'POST'])
def cadastro(request):
    if request.method == 'POST':
        try:
            user = Users(
                nome=request.data.get("nome"),
                usuario=request.data.get("usuario"),
                senha=request.data.get("senha"),
                email=request.data.get("email")
            )
            user.save()
        except:
            return Response({'mensagem': 'Dados inválidos'}, status=HTTP_200_OK)
    else:
        return render(request, 'cadastro.html')
