# Generated by Django 2.0.13 on 2019-07-17 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20190717_1436'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newuser',
            name='password1',
        ),
        migrations.RemoveField(
            model_name='newuser',
            name='password2',
        ),
    ]
