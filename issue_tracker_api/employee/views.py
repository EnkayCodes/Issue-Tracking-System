from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .models import Employee
from .serializers import EmployeeSerializer, UserSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register_employee(request):
    """
    Register a new employee
    """
    try:
        data = request.data
        
        # Validate required fields
        required_fields = ['username', 'email', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if not data.get(field):
                return Response(
                    {'error': f'{field} is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Check if user already exists
        if User.objects.filter(username=data['username']).exists():
            return Response(
                {'error': 'Username already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(email=data['email']).exists():
            return Response(
                {'error': 'Email already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create User
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        
        # Create Employee profile
        employee = Employee.objects.create(
            user=user,
            department=data.get('department', 'General'),
            position=data.get('position', 'Employee'),
            phone_number=data.get('phone_number', ''),
            hire_date=data.get('hire_date')  # You might want to set this automatically
        )
        
        # Return success response
        return Response({
            'message': 'Employee registered successfully',
            'user_id': user.id,
            'employee_id': employee.id
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_current_employee(request):
    """
    Get current employee profile
    """
    try:
        employee = Employee.objects.get(user=request.user)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)
    except Employee.DoesNotExist:
        return Response(
            {'error': 'Employee profile not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
        
        
@api_view(['GET'])
def employee_list(request):
    """
    Get list of all employees (admin only)
    """
    if not request.user.is_staff:
        return Response(
            {'error': 'Permission denied'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    employees = Employee.objects.all()
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def employee_detail(request, pk):
    """
    Get specific employee details
    """
    try:
        employee = Employee.objects.get(pk=pk)
        
        # Users can only see their own profile unless they're admin
        if not request.user.is_staff and employee.user != request.user:
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)
    except Employee.DoesNotExist:
        return Response(
            {'error': 'Employee not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )