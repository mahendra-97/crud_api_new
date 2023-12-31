# Generated by Django 4.1.5 on 2023-07-10 05:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0003_alter_employee_ephone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='eemail',
            field=models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator(message='Invalid email address.')], verbose_name='eemail'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='ephone',
            field=models.IntegerField(verbose_name='ephone'),
        ),
    ]
