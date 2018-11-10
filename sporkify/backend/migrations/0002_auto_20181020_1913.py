# Generated by Django 2.1 on 2018-10-20 19:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shift',
            name='emp_ID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.Employee'),
        ),
        migrations.AlterField(
            model_name='shift',
            name='time_out',
            field=models.DateTimeField(null=True),
        ),
    ]