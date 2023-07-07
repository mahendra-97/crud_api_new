# from django.core.validators import validate_email
from django.db import models
from django import forms

class Employee(models.Model):
    eid = models.AutoField('eid',primary_key=True)
    ename = models.CharField('ename',max_length=100)
    ephone = models.IntegerField('ephone')
    eemail = models.EmailField('eemail')
    edepartment = models.CharField('edepartment',max_length=20)


    def __str__(self):
        return self.name
