# Generated by Django 4.2.4 on 2023-08-19 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_remove_customuser_cpf_alter_customuser_cidade_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='cpf',
            field=models.CharField(blank=True, max_length=14, null=True, unique=True),
        ),
    ]