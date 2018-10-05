import json
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def index(request):
    return render(request, 'index.html')


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def logar(request):
    try:
        usuario_aux = User.objects.get(username=request.POST['username'])
        usuario = authenticate(username=usuario_aux.username,
                               password=request.POST["password"])
        if usuario is not None:
            try:
                login(request, usuario)
                return HttpResponseRedirect('adm')
            except:
                return render(request, 'index.html')
    except:
        messages.error(request, 'Usuário ou senha inválido!')
        return redirect(index)


@csrf_exempt
@login_required
def sair(request):
    logout(request)
    return HttpResponseRedirect('/')


@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
def cadastro(request):
    if request.method == 'POST':
        try:
            usuario_aux = User.objects.get(username=request.POST['username'])
            if usuario_aux:
                messages.error(request, 'Já temos esse usuário cadastrado.')
                return redirect(cadastro)
        except User.DoesNotExist:
            nome_usuario = request.POST['username']
            email = request.POST['email']
            senha = request.POST['password']
            novoUsuario = User.objects.create_user(username=nome_usuario, email=email, password=senha)
            novoUsuario.save()
            messages.success(request, 'Cadastro realizado com sucesso.')
            return redirect(index)
    else:
        return render(request, 'cadastro.html')


@csrf_exempt
@api_view(["GET"])
def adm(request):
    return render(request, 'adm.html')