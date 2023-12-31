# Generated by Django 4.1.5 on 2023-07-10 08:43

from django.db import migrations, models
import employees.models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0006_alter_employee_eemail_alter_employee_ephone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='eemail',
            field=models.CharField(max_length=100, verbose_name='eemail'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='ephone',
            field=models.CharField(max_length=15, validators=[employees.models.validate_ephone], verbose_name='ephone'),
        ),
    ]
