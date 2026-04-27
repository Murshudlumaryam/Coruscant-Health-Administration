from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','first_name','last_name','role','is_approved','phone','date_of_birth','created_at']
        read_only_fields = ['id','created_at','is_approved']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    class Meta:
        model = User
        fields = ['username','email','password','first_name','last_name','role','phone']

    def validate_role(self, value):
        if value not in ('patient','doctor'):
            raise serializers.ValidationError("Role must be patient or doctor.")
        return value

    def create(self, validated_data):
        pwd = validated_data.pop('password')
        user = User(**validated_data, is_approved=False)
        user.set_password(pwd)
        user.save()
        return user
