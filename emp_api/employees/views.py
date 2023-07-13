from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework.views import APIView
from rest_framework import status
from django import forms
from django.views import View
from .models import Employee
import re
from .forms import EmpForm
from enum import Enum

class DepartmentChoices(Enum):
    HR = 'HR'
    DEVELOPER = 'Developer'
    SALES = 'Sales'
    MARKETING = 'Marketing'
    UIX = 'UI/UX'
    GAMING = 'Gaming'
    RISKANALYST = 'Risk Analyst'
    BA = 'BA'




class EmployeeAPI(APIView):
    # def get(self, request, id=None):
    #     try:
    #         if id:
    #             employee = Employee.objects.get(eid=id)
    #             data = {
    #                 'id': employee.eid,
    #                 'name': employee.ename,
    #                 'phone': employee.ephone,
    #                 'email': employee.eemail,
    #                 'department': employee.edepartment,
    #             }
    #         else:
    #             employees = Employee.objects.all()
    #             data = [{'id': emp.eid, 'name': emp.ename, 'phone': emp.ephone} for emp in employees]

    #         return JsonResponse({'data': data})
    #     except Employee.DoesNotExist:
    #         return JsonResponse({'error': 'Employee not found'}, status=404)
    #     except Exception as e:
    #         return JsonResponse({'error': str(e)}, status=500)


    #=========================================================================================


    def get(self, request, id=None):
        try:
            input_department = request.GET.get('input_department')

            if id:
                employee = Employee.objects.get(eid=id, edepartment=input_department)
                data = {
                    'id': employee.eid,
                    'name': employee.ename,
                    'phone': employee.ephone,
                    'email': employee.eemail,
                    'department': employee.edepartment,
                }
            else:
                if input_department:
                    department_list = [department.strip() for department in input_department.split(",") if department.strip()]
                    employees = Employee.objects.filter(edepartment__in=department_list)
                else:
                    employees = Employee.objects.all()

                data = [{'id': emp.eid, 'name': emp.ename, 'phone': emp.ephone, 'email': emp.eemail, 'department': emp.edepartment} for emp in employees]

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

            # print(eemail_list)

            # Validate each email address
            for email in eemail_list:
                validate_email(email)

            # Validate the mobile number
            pattern = r'^(?:\+91|0)?[6-9]\d{9}$'
            if not re.match(pattern, ephone):
                return JsonResponse({'error': 'Invalid phone number'}, status=400)
            
            # Validate department choice
            if edepartment not in [choice.value for choice in DepartmentChoices]:
                return JsonResponse({'error': 'Invalid department choice','1': 'HR','2': 'Developer','3': 'Sales','4': 'Marketing','5': 'UI/UX','6': 'Gaming','7': 'Risk Analyst','8': 'BA'}, status=400)

            employee = Employee.objects.create(eid=eid, ename=ename, ephone=ephone, eemail=eemail, edepartment=edepartment)

            return JsonResponse({'id': employee.eid, 'success': 'Employee created successfully'})
        
        except ValidationError as e:
            data = {'status':'error','error_code': 422, 'message': "['Enter a valid email address.']".format(e)}
            return JsonResponse(data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
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

            eemail_list = [email.strip() for email in employee.eemail.split(',')]
            # Validate each email address
            for email in eemail_list:
                validate_email(email)
            
             # Validate department choice
            if department not in [choice.value for choice in DepartmentChoices]:
                return JsonResponse({'error': 'Invalid department choice','1': 'HR','2': 'Developer','3': 'Sales','4': 'Marketing','5': 'UI/UX','6': 'Gaming','7': 'Risk Analyst','8': 'BA'}, status=400)


            return JsonResponse({'success': 'Employee updated successfully'})
        except Employee.DoesNotExist:
            return JsonResponse({'error': 'Employee not found'}, status=404)
        
        except ValidationError as e:
            data = {'status':'error','error_code': 422, 'message': "['Enter a valid email address.']".format(e)}
            return JsonResponse(data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
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
