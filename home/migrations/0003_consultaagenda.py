# Generated by Django 5.0.3 on 2024-07-30 20:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_consulta_tipo'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsultaAgenda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('especielidade', models.CharField(choices=[('Ginecologia', 'Ginecologia'), ('Cirugia', 'Cirugia'), ('Dermatologia', 'Dermatologia'), ('Odontologia', 'Odontolgia'), ('Oftamologia', 'Oftamologia'), ('Nutricao', 'Nutricao')], max_length=255)),
                ('status', models.CharField(choices=[('pendente', 'Pendente'), ('aceite', 'Aceite'), ('concluida', 'Concluída')], max_length=20)),
                ('consulta', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.consulta')),
                ('paciente_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.paciente')),
            ],
        ),
    ]
