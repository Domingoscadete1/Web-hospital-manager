# Generated by Django 5.0.3 on 2024-08-09 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_alter_receita_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='receita',
            name='codigo',
            field=models.ImageField(blank=True, null=True, upload_to='codigos_de_barras/'),
        ),
    ]
