from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/', views.register_employee, name='register-employee'),
    path('auth/me/', views.get_current_employee, name='current-employee'),

    # Add these if you want employee list/detail endpoints
    path('employees/', views.employee_list, name='employee-list'),
    path('employees/<int:pk>/', views.employee_detail, name='employee-detail'),
]