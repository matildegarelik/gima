# Generated by Django 4.0.4 on 2022-12-05 11:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_git', '0003_userseccion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seccion',
            name='user',
        ),
    ]