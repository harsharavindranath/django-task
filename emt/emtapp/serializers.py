from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate



class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'user_type']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            user_type=validated_data['user_type']
        )
        return user
    


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                data['user'] = user
            else:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")

        return data


# class TaskSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Task
#         fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

  

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'start_date', 'end_date']


class EmployeeHomepageSerializer(serializers.Serializer):
    assigned_tasks = TaskSerializer(many=True)

    def to_representation(self, instance):
        return {
            'assigned_tasks': TaskSerializer(instance.assigned_tasks.all(), many=True).data
        }
  

class EmployeeSerializer(serializers.ModelSerializer):
    assigned_tasks = TaskSerializer(many=True)
    
    class Meta:
        model = CustomUser
        fields = ['id','username', 'email', 'assigned_tasks']

class AdminHomepageSerializer(serializers.Serializer):
    employees = EmployeeSerializer(many=True)

    def to_representation(self, instance):
        return {
            'employees': EmployeeSerializer(instance, many=True).data
        }
    
class LeadSerializer(serializers.ModelSerializer):
    assigned_tasks = TaskSerializer(many=True, read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id','username', 'email', 'assigned_tasks']