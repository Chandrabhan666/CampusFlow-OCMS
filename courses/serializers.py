from rest_framework import serializers

from .models import Category, Course, Lecture, Module


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "created_at"]
        read_only_fields = ["id", "created_at"]


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ["id", "module", "title", "video_url", "notes", "order", "duration"]
        read_only_fields = ["id"]


class ModuleSerializer(serializers.ModelSerializer):
    lectures = LectureSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ["id", "course", "title", "order", "lectures"]
        read_only_fields = ["id"]


class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "price",
            "level",
            "instructor",
            "category",
            "is_published",
            "created_at",
            "modules",
        ]
        read_only_fields = ["id", "created_at", "modules"]
