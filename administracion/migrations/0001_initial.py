# Generated by Django 2.2.1 on 2023-06-15 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Operador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('ci', models.CharField(max_length=8)),
                ('u_name', models.CharField(max_length=30, unique=True)),
                ('password', models.TextField()),
                ('rol', models.CharField(choices=[('ADM', 'Administrador'), ('OPE', 'Operador')], max_length=3)),
            ],
        ),
    ]
