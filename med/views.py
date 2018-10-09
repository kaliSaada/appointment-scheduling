import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from med.models import Consulta
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


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
            return redirect_mensagem(0, 'index', request, 'Cadastro realizado com sucesso.')
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
                return redirect_mensagem(1, 'index',request, 'Não foi possivel fazer o login.')
        else:
            return redirect_mensagem(1, 'index',request, 'Senha inválida!')
    except User.DoesNotExist:
        return redirect_mensagem(1, 'index',request, 'Usuário inválido!')


@csrf_exempt
def sair(request):
    logout(request)
    return HttpResponseRedirect('/')


@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
def adm(request):
    if request.method == 'POST' and request.POST['username'] == 'admin':
        try:
            usuario_aux = User.objects.get(username=request.POST['username'])
            usuario = authenticate(username=usuario_aux.username,
                                   password=request.POST["password"])
            if usuario is not None:
                try:
                    login(request, usuario)
                    return HttpResponseRedirect('adm/painel')
                except:
                    return redirect_mensagem(1, 'adm', request, 'Não foi possivel fazer o login.')
            else:
                return redirect_mensagem(1, 'adm', request, 'Senha inválida!')
        except User.DoesNotExist:
            return redirect_mensagem(1, 'adm', request, 'Usuário inválido!')
    else:
        return render(request, 'adm.html')


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def painel(request):
    return render(request, 'painel.html')


@csrf_exempt
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def home(request):
    return render(request, 'home.html')


@csrf_exempt
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def agenda(request):
    try:
        start = request.query_params['start']
        end = request.query_params['end']
    except:
        return HttpResponse(json.dumps({'Mensagem': 'Informe a data de inicio e a data final.'}),
                            content_type="application/json")
    eventos = []
    consultas = Consulta.objects.all().filter(date__range=(start, end)).values('codigo', 'user_codigo', 'date', 'hora')
    for consulta in consultas:
        evento = [{
            "id": "%s" % (consulta['user_codigo']),
            "title": "Consulta",
            "start": "%sT%s" % (consulta['date'], consulta['hora']),
        }]
        eventos += evento
    return HttpResponse(json.dumps(eventos), content_type="application/json")


@csrf_exempt
@api_view(["GET"])
def consulta(request):
        consultas = Consulta.objects.all().filter(user_codigo=request.user.id).\
            values('codigo', 'user_codigo', 'date', 'hora', 'comentario')
        consultas = list(consultas)
        return HttpResponse(json.dumps(consultas), content_type="application/json")


@csrf_exempt
def adicionar_consulta(request):
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


@csrf_exempt
def alterar_consulta(request):
    if request.method == 'POST':
        consulta = Consulta.objects.all().filter(codigo=request.POST['codigo_consulta']).\
            values('codigo', 'user_codigo', 'date', 'hora')
        consulta.date = request.POST['data']
        consulta.hora = request.POST['time']
        consulta.comentario = request.POST['comentario']
        consulta.save()
        messages.success(request, 'Consulta alterada.')
        return redirect(home)
    else:
        messages.error(request, 'Não foi possivel deletar a consulta.')
        return redirect(index)


@csrf_exempt
def deletar_consulta(request):
    if request.method == 'POST':
        codigo_consulta = request.POST['codigo_consulta']
        Consulta.objects.filter(codigo=codigo_consulta).delete()
        redirect_mensagem(1, 'home', request, 'Consulta deletada.')
        return redirect(home)
    else:
        messages.error(request, 'Não foi possivel alterar a consulta.')
        return redirect(index)


def redirect_mensagem(tipo=None, pagina=None, request=None, texto=None):
    if tipo == 0:
        messages.success(request, texto)
        return redirect(pagina)
    elif tipo == 1:
        messages.error(request, texto)
        return redirect(pagina)
    else:
        return redirect(pagina)


def verifica_login(request, pagina):
    if request.user.id is not None:
        return HttpResponseRedirect('home')
    else:
        return render(request, pagina)


def notificar(assunto, remetente, destinatarios):
    try:
        mensagem_html = render_to_string('email.html')
        assunto = u"%s" % assunto
        remetente = u'%s' % remetente
        msg = EmailMultiAlternatives(assunto, mensagem_html, remetente, destinatarios)
        msg = msg.attach_alternative(mensagem_html, "text/html")
        msg.send()
    except Exception as exception:
        return exception

