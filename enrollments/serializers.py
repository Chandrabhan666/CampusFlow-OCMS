from django.utils import timezone
from rest_framework import serializers

from .models import Enrollment, LectureProgress


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ["id", "student", "course", "status", "enrolled_at"]
        read_only_fields = ["id", "enrolled_at"]


class LectureProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureProgress
        fields = ["id", "enrollment", "lecture", "completed", "completed_at"]
        read_only_fields = ["id", "completed_at"]

    def update(self, instance, validated_data):
        completed = validated_data.get("completed", instance.completed)
        if completed and not instance.completed_at:
            validated_data["completed_at"] = timezone.now()
        elif not completed:
            validated_data["completed_at"] = None
        return super().update(instance, validated_data)
