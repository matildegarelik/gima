# Generated by Django 4.0.4 on 2022-05-03 21:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_git', '0004_alter_planes_de_pago_adjudicacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planes_de_pago',
            name='adjudicacion',
            field=models.OneToOneField(blank=True, max_length=45, on_delete=django.db.models.deletion.PROTECT, to='gestion_git.adjudicacion'),
        ),
    ]
