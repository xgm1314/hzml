# Generated by Django 4.1.7 on 2023-05-18 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0001_initial'),
        ('user', '0002_user_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='one_department',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to='department.department', verbose_name='一级部门'),
        ),
    ]
