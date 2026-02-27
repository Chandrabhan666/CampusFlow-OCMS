from rest_framework import serializers


class DashboardStatsSerializer(serializers.Serializer):
    total_users = serializers.IntegerField()
    total_courses = serializers.IntegerField()
    total_enrollments = serializers.IntegerField()
    total_reviews = serializers.IntegerField()
    published_courses = serializers.IntegerField()
