from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Employee

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)  # to set password on create

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name','password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # hash password
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # now writable

    class Meta:
        model = Employee
        fields = ['id', 'user', 'department', 'phone_number']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        employee = Employee.objects.create(user=user, **validated_data)
        return employee

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = UserSerializer(instance=instance.user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
