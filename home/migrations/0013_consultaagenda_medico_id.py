# Generated by Django 5.0.3 on 2024-08-06 19:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_consulta_data_consulta_hora'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultaagenda',
            name='medico_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.medico'),
        ),
    ]
