from rest_framework import serializers
from django.db import IntegrityError
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source="creator.username")

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "status",
            "duration",
            "creator",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "creator", "created_at", "updated_at"]

    def validate_duration(self, value):
        if value < 1:
            raise serializers.ValidationError("Duration must be at least 1 month.")
        
        return value
