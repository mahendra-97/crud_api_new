from django.urls import path
from .views import EmployeeAPI

urlpatterns = [
    path('employees', EmployeeAPI.as_view(), name='Employee_api'),
    path('employees/<id>', EmployeeAPI.as_view(), name='employee-detail-api'),
]