from django.test import TestCase
from django.forms import ValidationError
# from django.core.exceptions import ValidationError
from django.urls import reverse
from employees.models import Employee
from rest_framework.test import APIClient
from rest_framework import status

class EmployeeTest(TestCase):
    def test_valid_email(self):
        employee = Employee(
            eid=1,
            ename='John Doe',
            ephone='9876543210',
            eemail='john@example.com, jane@example.com',
            edepartment='Sales'
        )
        self.assertEqual(employee.clean_fields(), None)

    def test_invalid_email(self):
        employee = Employee(
            eid=1,
            ename='John Doe',
            ephone='9876543210',
            eemail='john',
            edepartment='Sales'
        )
        employee.full_clean()

        
class EmployeeTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.emp1 = Employee.objects.create(
            eid='2',
            ename='Mahendra',
            ephone='1234567890',
            eemail='mahendra@example',
            edepartment='Development'
        )
        self.emp2 = Employee.objects.create(
            eid='3',
            ename='Stanley',
            ephone='9879863210',
            eemail='stan@example',
            edepartment='Data Engineering'
        )

    def test_get_all_employees(self):
        response = self.client.get('/employees')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"data": [{"id": 2, "name": "Mahendra", "phone": "1234567890"}, {"id": 3, "name": "Stanley", "phone": "9879863210"}]} )

    def test_invalid_get_all_employees(self):
        # get API response
        response = self.client.get('/employee')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_employees(self):
        input_data = {
            'ename': 'John Doe',
            'ephone': '9876543210',
            'eemail': 'john@example.com',
            'edepartment': 'Sales'
        }
        response = self.client.post('/employees', input_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        output_response = {"id": 4, "success": "Employee created successfully"}
        self.assertEqual(response.json(), output_response)

    def test_invalid_email_address(self):
        data = {'ename':'John Doe', 
                'ephone':'1234567890', 
                'eemail':'invalid_mail',
                'edepartment':'Sales'}
        response = self.client.post('/employees', data)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(response.json(),{"status": "error", "error_code": 422, "message": "['Enter a valid email address.']"})
   
    def test_post_without_phone_employee(self):
        # create a new Employee without pass mobile key
        input_data = {'ename':'John Doe', 
                    'eemail':'john@example.com',
                    'edepartment':'Sales'}
        response = self.client.post('/employees', input_data )
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_post_with_null_phone_employee(self):
        # create a new Employee without pass mobile key
        input_data = {'ename':'John Doe', 
                      'ephone':'',
                    'eemail':'john@example.com',
                    'edepartment':'Sales'}
        response = self.client.post('/employees', input_data )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_post_wrong_mobile_employee(self):
        # create a new Employee with wronge format mobile number
        input_data = {'ename':'John Doe', 
                    'eemail':'john@example.com',
                    'ephone':'1234567',
                    'edepartment':'Sales'}
        response = self.client.post('/employees', input_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class EmployeePutTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.employee_data = Employee.objects.create(ename= 'Jonny', ephone= '1234567987', eemail= 'jonny@gmail.com', edepartment= 'IT')
        # self.employee2 = Employee.objects.create(ename= 'Jon', ephone= '1234567988', eemail= 'jon@gmail.com', edepartment= 'IT')
        # self.response = ('/employees', self.employee_data)
        self.employee = Employee.objects.get()
        # self.employee2= Employee.objects.get()


    def test_put_student(self):
        # update an existing Employee
        new_data = {
                    'eid':self.employee.eid,
                    'ename': 'Mahendra', 
                    'ephone': '9874563210', 
                    'eemail': 'mahendrasonawane@gmail.com', 
                    'edepartment': 'Gaming'}
        # response = self.client.put(f'/employees/<eid={self.employee.eid}>', new_data)
        response = self.client.put(f'/employees/{self.employee.eid}', new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
      
    def test_put_invalid_email_address(self):
        new_data = {'eid':self.employee.eid, 'ename': 'John', 'ephone': '9874563211', 'eemail': 'invalid_email', 'edepartment': 'IT'}
        response = self.client.put(f'/employees/{self.employee.eid}', new_data)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(response.json(),{"status": "error", "error_code": 422, "message": "['Enter a valid email address.']"})

    def test_delete_employee(self):
        # delete an existing employee
        response = self.client.delete(f'/employees/{self.employee.eid}')
        # print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Employee.objects.count(), 0)

    def test_invalid_delete_student(self):
        # delete an existing employee
        response = self.client.delete(f'/employees/{self.employee.eid}')
        response = self.client.delete(f'/employees/{self.employee.eid}')
        # print(response.content)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Employee.objects.count(), 0)
        output_response = {"error": "Employee not found"}
        self.assertEqual(response.json(), output_response)


