from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
# from django.contrib.postgres.forms import SimpleArrayField

class EmpForm(forms.Form):
    eid = forms.IntegerField()
    ename = forms.CharField(required=True, min_length=1, max_length=50)
    ephone = forms.IntegerField(required=True)
    email = forms.EmailField(required=True)
    department = forms.CharField(required=True, min_length=1, max_length=100)

