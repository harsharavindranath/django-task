from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework.authtoken.models import Token



@api_view(['POST'])
def user_registration(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def userlogin(request):
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key,'message': "login successfull"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# @api_view(['GET'])
# def employeehomepage(request,id):
#     if request.method == 'GET':
#         try:
#             employee = Employee.objects.get(pk=id)
#         except Employee.DoesNotExist:
#             return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = EmployeeHomepageSerializer(employee)
#         return Response(serializer.data)


@api_view(['GET','POST','PUT','PATCH','DELETE'])
def admin_homepage(request):
    if request.method == 'GET':
        employees = CustomUser.objects.filter(user_type='Employee')
        employee_serializer = EmployeeSerializer(employees, many=True)
        tasks = Task.objects.all()
        task_serializer = TaskSerializer(tasks, many=True)
        leads = CustomUser.objects.filter(user_type='Employee')
        lead_serializer = LeadSerializer(leads, many=True)
        data = {
        'employees': employee_serializer.data,
        'tasks': task_serializer.data,
        'leads': lead_serializer.data
        }
        return Response(data)
    elif request.method == 'POST':
        task_serializer = TaskSerializer(data=request.data)
        lead_serializer = LeadSerializer(data=request.data)
        employee_serializer = EmployeeSerializer(data=request.data)
        
        if task_serializer.is_valid():
            task_serializer.save()
            return Response(task_serializer.data, status=status.HTTP_201_CREATED)
        elif lead_serializer.is_valid():
            lead_serializer.save()
            return Response(lead_serializer.data, status=status.HTTP_201_CREATED)
        elif employee_serializer.is_valid():
            employee_serializer.save()
            return Response(employee_serializer.data, status=status.HTTP_201_CREATED)
        else:
            # If none of the serializers are valid, return error response
            return Response(
                {'error': 'Invalid data for creating task, lead, or employee.'},
                status=status.HTTP_400_BAD_REQUEST
            )