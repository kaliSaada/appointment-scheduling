"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from med import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('login', views.logar, name="login"),
    path('sair', views.sair, name="sair"),
    path('cadastro', views.cadastro, name="cadastro"),
    path('home', views.home, name="home"),
    path('adm', views.adm, name="adm"),
    path('adm/painel', views.painel, name="adm/painel"),
    path('agenda', views.agenda, name="agenda"),
    path('consulta', views.consulta, name="consulta"),
    path('consulta/adicionar', views.adicionar_consulta, name="adicionar_consulta"),
    path('consulta/deletar', views.deletar_consulta, name="deletar_consulta"),
    path('consulta/alterar', views.alterar_consulta, name="alterar_consulta"),

]

