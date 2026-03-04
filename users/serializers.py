from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        
        fields = [
            "id",
            "username",
            "email",
            "full_name",
            "avatar",
            "password",
        ]
        
        read_only_fields = ["id"]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already registered.")
        
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already taken.")
        
        return value

    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                username=validated_data["username"],
                email=validated_data["email"],
                full_name=validated_data["full_name"],
                password=validated_data["password"],
                avatar=validated_data.get("avatar")
            )
            return user
        except IntegrityError:
            raise serializers.ValidationError("User could not be created.")
        
User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.USERNAME_FIELD

    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user

        avatar_url = None
        if user.avatar and hasattr(user.avatar, "url"):     # type: ignore
            avatar_url = user.avatar.url                    # type: ignore

        data["user"] = {                            # type: ignore
            "id": user.id,                          # type: ignore
            "username": user.username,              # type: ignore
            "email": user.email,                    # type: ignore
            "full_name": user.full_name,            # type: ignore
            "avatar": avatar_url,                   # type: ignore
        }

        return data