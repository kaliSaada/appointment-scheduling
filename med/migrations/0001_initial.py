# Generated by Django 2.1.2 on 2018-10-06 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Consulta',
            fields=[
                ('codigo', models.AutoField(primary_key=True, serialize=False)),
                ('user_codigo', models.CharField(max_length=10)),
                ('date', models.CharField(max_length=14)),
                ('hora', models.CharField(max_length=10)),
                ('comentario', models.CharField(max_length=200)),
            ],
        ),
    ]
