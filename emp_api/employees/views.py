from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework.views import APIView
from django import forms
from django.views import View
from .models import Employee
import re

from .forms import EmpForm

class EmployeeAPI(APIView):
    def get(self, request, id=None):
        try:
            if id:
                employee = Employee.objects.get(eid=id)
                data = {
                    'id': employee.eid,
                    'name': employee.ename,
                    'phone': employee.ephone,
                    'email': employee.eemail,
                    'department': employee.edepartment,
                }
            else:
                employees = Employee.objects.all()
                data = [{'id': emp.eid, 'name': emp.ename, 'phone': emp.ephone} for emp in employees]

            return JsonResponse({'data': data})
        except Employee.DoesNotExist:
            return JsonResponse({'error': 'Employee not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        

    def post(self, request):
        try:
            eid = request.POST.get('eid')
            ename = request.POST.get('ename')
            ephone = request.POST.get('ephone')
            eemail = request.POST.get('eemail')
            edepartment = request.POST.get('edepartment')

            # # Validate the Email
            # validate_email(eemail)

            # Split the email addresses by commas
            eemail_list = [email.strip() for email in eemail.split(',')]

            print(eemail_list)

            # Validate each email address
            for email in eemail_list:
                validate_email(email)

            # Validate the mobile number
            pattern = r'^(?:\+91|0)?[6-9]\d{9}$'
            if not re.match(pattern, ephone):
                return JsonResponse({'error': 'Invalid phone number'}, status=400)
            


            employee = Employee.objects.create(eid=eid, ename=ename, ephone=ephone, eemail=eemail, edepartment=edepartment)

            return JsonResponse({'id': employee.eid, 'success': 'Employee created successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        

    def put(self, request, id=None):
        try:
            name = request.POST.get('ename')
            phone = request.POST.get('ephone')
            email = request.POST.get('eemail')
            department = request.POST.get('edepartment')

            employee = Employee.objects.get(eid=id)
            employee.ename = name
            employee.ephone = phone
            employee.eemail = email
            employee.edepartment = department
            employee.save()

            return JsonResponse({'success': 'Employee updated successfully'})
        except Employee.DoesNotExist:
            return JsonResponse({'error': 'Employee not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def delete(self, request, id):
        try:
            employee = Employee.objects.get(eid=id)
            employee.delete()

            return JsonResponse({'success': 'Employee deleted successfully'})
        except Employee.DoesNotExist:
            return JsonResponse({'error': 'Employee not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
