from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from django.db import transaction
from .models import Employee
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import EmployeeSerializer, CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    
@api_view(['POST'])
@permission_classes([AllowAny])
def register_employee(request):
    """
    Register a new employee
    """
    try:
        with transaction.atomic():  # ✅ This starts the transaction block
            data = request.data
            
            # Validate required fields
            if not data.get('username'):
                return Response({'error': 'Username is required'}, status=400)
            
            if not data.get('password'):
                return Response({'error': 'Password is required'}, status=400)
            
            # Check if user exists
            if User.objects.filter(username=data['username']).exists():
                return Response({'error': 'Username already exists'}, status=400)
            
            # Create user with is_active=True
            user = User.objects.create_user(
                username=data.get('username'),
                password=data.get('password'),
                email=data.get('email', ''),
                first_name=data.get('first_name', ''),
                last_name=data.get('last_name', ''),
                is_active=True  # ✅ Ensure user is active
            )
            
            # Create employee profile
            employee = Employee.objects.create(
                user=user,
                department=data.get('department', ''),
                position=data.get('position', ''),
                phone_number=data.get('phone_number', '')
            )
            
            return Response({
                'message': 'Employee registered successfully',
                'user_id': user.id,
                'username': user.username
            }, status=201)
        # ✅ The with statement automatically closes the transaction
        
    except Exception as e:
        print("Exception:", str(e))  # Debugging
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employee_profile(request):
    """
    Get current employee profile
    """
    try:
        employee = Employee.objects.get(user=request.user)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)
    except Employee.DoesNotExist:
        # Return basic user info if no employee profile exists
        return Response({
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'is_staff': request.user.is_staff,
                'is_superuser': request.user.is_superuser
            },
            'message': 'Employee profile not found'
        })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employee_list(request):
    """
    Get list of all employees (admin only)
    """
    if not request.user.is_staff:
        return Response({'error': 'Permission denied'}, status=403)
    
    employees = Employee.objects.all()
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data)