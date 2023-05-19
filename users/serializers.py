from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(max_length=50, validators=[UniqueValidator(queryset=User.objects.all(), message="email already registered.")])
    password = serializers.CharField(max_length=50, write_only=True)
    username = serializers.CharField(max_length=50, validators=[UniqueValidator(queryset=User.objects.all(), message="username already taken.")])
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    birthdate = serializers.DateField(allow_null=True, default=None)
    is_employee = serializers.BooleanField(allow_null=True, default=False)
    is_superuser = serializers.BooleanField(allow_null=True, default=False)

    def create(self, validated_data: dict) -> User:
        return User.objects.create_user(**validated_data)
    
    def update(self, instance, validated_data: dict) -> User:
        password = validated_data.pop("password", None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50, write_only=True)
    password = serializers.CharField(max_length=50, write_only=True)