# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Users(models.Model):
    codigo = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    usuario = models.CharField(max_length=40)
    senha = models.CharField(max_length=40)
    email = models.CharField(max_length=150)