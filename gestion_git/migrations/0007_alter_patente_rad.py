# Generated by Django 4.0.4 on 2023-01-04 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_git', '0006_patente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patente',
            name='rad',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
