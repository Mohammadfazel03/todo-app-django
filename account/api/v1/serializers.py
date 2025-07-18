from rest_framework import serializers
from django.contrib.auth.password_validation import get_default_password_validators, validate_password

from account.models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2')

    def validate_password(self, password):
        validators = get_default_password_validators()
        validate_password(password=password, password_validators=validators)
        return password

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Passwords must match'})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False
        )

        return user


class UserEmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs['email'])
            attrs['user'] = user
        except User.DoesNotExist:
            raise serializers.ValidationError({'email': 'This email is not registered'})
        return attrs


class PasswordSerializer(serializers.Serializer):
    password2 = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate_password(self, password):
        validators = get_default_password_validators()
        validate_password(password=password, password_validators=validators)
        return password

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Passwords must match'})
        return attrs
