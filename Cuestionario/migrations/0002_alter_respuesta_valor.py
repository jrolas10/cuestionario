# Generated by Django 4.2.1 on 2023-11-23 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cuestionario', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='respuesta',
            name='valor',
            field=models.SmallIntegerField(),
        ),
    ]
