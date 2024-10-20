from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken




USER = get_user_model()

class UserSerializerWithToken(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = USER
        fields = ["username", "token"]
        
    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class UserCreateSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = USER
        fields = ["username", "email", "password1", "password2"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password2(self, value):
        if value != self.initial_data["password1"]:
            raise serializers.ValidationError("Passwords must match")
        return value

    def validate_email(self, value):
        if USER.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")

        return value
    
    def validate_username(self, value):
        if USER.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")

        return value


    def create(self, validated_data):
        password1 = validated_data.pop("password1")
        email = validated_data["email"]
        username = validated_data["username"]

        user = USER.objects.create_user(
            username=username,
            email=email
        )
        user.set_password(password1)
        user.save()

        return user