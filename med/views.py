import json
from django.http import HttpResponse
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
from med.models import Consulta


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def index(request):
    return verifica_login(request, 'index.html')


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
            return redirect_index_mensagem(0, request, 'Cadastro realizado com sucesso.')
    else:
        return verifica_login(request, 'cadastro.html')


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
                return HttpResponseRedirect('home')
            except:
                return redirect_index_mensagem(1, request, 'Não foi possivel fazer o login.')
        else:
            return redirect_index_mensagem(1, request, 'Senha inválida!')
    except User.DoesNotExist:
        return redirect_index_mensagem(1, request, 'Usuário inválido!')


@csrf_exempt
@login_required
def sair(request):
    logout(request)
    return HttpResponseRedirect('/')


@csrf_exempt
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def adm(request):
    return render(request, 'adm.html')


@csrf_exempt
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def home(request):
    return render(request, 'home.html')


@csrf_exempt
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def agenda(request):
    evento = []
    if True:
        consultas = Consulta.objects.all().values('codigo', 'user_codigo', 'date', 'hora')
        for consulta in consultas:
            eventos = [{
                "title": "Consulta",
                "start": "%sT%s" % (consulta['date'], consulta['hora']),
            }]
            evento += eventos
        return HttpResponse(json.dumps(evento), content_type="application/json")
    else:
        return HttpResponse(json.dumps([
            {
                "title": "Cheio",
                "start": "2018-10-05",
                "end": "2018-10-05"
            },
            {
                "title": "Consulta",
                "start": "2018-10-05T10:30:00-05:00",
                "end": "2018-10-05T12:30:00"
            },
            {
                "title": "Consulta",
                "start": "2018-10-05T12:00:00"
            },
            {
                "title": "Consulta",
                "start": "2018-10-05T14:30:00"
            },
            {
                "title": "Consulta",
                "start": "2018-10-05T17:30:00"
            },
            {
                "title": "Consulta",
                "start": "2018-10-05T20:00:00"
            }
        ]), content_type="application/json")


@csrf_exempt
def consulta(request):
    if request.method == 'POST':
        data = request.POST['data']
        time = request.POST['time']
        comentario = request.POST['comentario']
        consulta = Consulta(user_codigo=request.user.id, date=data, hora=time, comentario=comentario)
        consulta.save()
        messages.success(request, 'Consulta marcada.')
        return redirect(home)
    else:
        messages.error(request, 'Não foi possivel marcar a consulta.')
        return redirect(index)


def redirect_index_mensagem(tipo=None, request=None, texto=None):
    if tipo == 0:
        messages.success(request, texto)
        return redirect(index)
    elif tipo == 1:
        messages.error(request, texto)
        return redirect(index)
    else:
        return redirect(index)


def verifica_login(request, pagina):
    if request.user.id is not None:
        return HttpResponseRedirect('home')
    else:
        return render(request, pagina)
