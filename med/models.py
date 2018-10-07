# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Consulta(models.Model):
    codigo = models.AutoField(primary_key=True)
    user_codigo = models.CharField(max_length=10)
    date = models.CharField(max_length=14)
    hora = models.CharField(max_length=10)
    comentario = models.CharField(max_length=200)