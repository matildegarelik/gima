# Generated by Django 4.0.4 on 2023-01-04 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_git', '0005_planes_de_pago_facturado'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dominio', models.CharField(blank=True, max_length=10, null=True)),
                ('vigente', models.BooleanField()),
                ('titular', models.CharField(max_length=200)),
                ('cuit', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=200)),
                ('localidad', models.CharField(max_length=200)),
                ('provincia', models.CharField(max_length=200)),
                ('cpa', models.CharField(blank=True, max_length=10, null=True)),
                ('marca', models.CharField(blank=True, max_length=10, null=True)),
                ('modelo', models.CharField(blank=True, max_length=10, null=True)),
                ('rad', models.CharField(blank=True, max_length=10, null=True)),
                ('pje_tit', models.FloatField(blank=True, null=True)),
                ('fecha', models.DateField(blank=True, null=True)),
                ('seccion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestion_git.seccion')),
            ],
        ),
    ]