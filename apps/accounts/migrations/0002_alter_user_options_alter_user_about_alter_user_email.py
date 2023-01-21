# Generated by Django 4.1.5 on 2023-01-20 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Юзер', 'verbose_name_plural': 'Юзери'},
        ),
        migrations.AlterField(
            model_name='user',
            name='about',
            field=models.TextField(blank=True, null=True, verbose_name='Про себе'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Електронна пошта'),
        ),
    ]