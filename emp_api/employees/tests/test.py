# from django.test import TestCase
# from django.forms import ValidationError
# from django.urls import reverse
# from employees.models import Employee
# from employees.views import EmployeeAPI
# from rest_framework.test import APIClient
# from rest_framework import status


# class EmployeeTestCase(TestCase):
#     def setUp(self):
#         self.employee_data = {
#             'eid': 1,
#             'ename': 'John Doe',
#             'ephone': '9876543210',
#             'eemail': 'john@example.com, jane@example.com, jdoe@example.com',
#             'edepartment': 'Sales',
#         }

#     def test_create_employee(self):
#         response = self.client.post(reverse('Employee_api'), self.employee_data)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(Employee.objects.count(), 1)
#         employee = Employee.objects.first()
#         self.assertEqual(employee.eid, self.employee_data['eid'])
#         self.assertEqual(employee.ename, self.employee_data['ename'])
#         self.assertEqual(employee.ephone, self.employee_data['ephone'])
#         self.assertEqual(employee.eemail, self.employee_data['eemail'])
#         self.assertEqual(employee.edepartment, self.employee_data['edepartment'])

#     def test_update_employee_emails(self):
#         employee = Employee.objects.create(**self.employee_data)

#         update_data = {
#             'eid': employee.eid,
#             'eemail': 'john.doe@example.com, johndoe@example.com',
#         }

#         response = self.client.put(reverse('employee-detail-api', kwargs={'id': employee.eid}), update_data)
#         print(response.content)  # Print the response content for debugging
#         self.assertEqual(response.status_code, 200)
#         employee.refresh_from_db()
#         self.assertEqual(employee.eemail, update_data['eemail'])


#     def test_invalid_email_validation(self):
#         invalid_employee_data = {
#             'eid': 1,
#             'ename': 'John Doe',
#             'ephone': '9876543210',
#             'eemail': 'john.doe@example.com, invalid_email, johndoe@example.com',
#             'edepartment': 'Sales',
#         }

#         response = self.client.post(reverse('Employee_api'), invalid_employee_data)
#         self.assertEqual(response.status_code, 500)
#         self.assertEqual(Employee.objects.count(), 0)

