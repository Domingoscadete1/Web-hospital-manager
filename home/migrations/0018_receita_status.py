# Generated by Django 5.0.3 on 2024-08-09 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_analise_preco'),
    ]

    operations = [
        migrations.AddField(
            model_name='receita',
            name='status',
            field=models.CharField(blank=True, choices=[('pendente', 'Pendente'), ('concluida', 'Concluída')], max_length=20, null=True),
        ),
    ]
