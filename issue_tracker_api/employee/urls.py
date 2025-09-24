from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_employee, name='register-employee'),
    path('profile/', views.employee_profile, name='employee-profile'),
    path('employees/', views.employee_list, name='employee-list'),
]