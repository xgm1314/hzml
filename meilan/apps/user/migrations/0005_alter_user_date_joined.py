# Generated by Django 4.1.7 on 2023-05-22 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_user_one_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(null=True, verbose_name='入职日期'),
        ),
    ]
