from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.cache import cache_page

from courses.models import Course
from enrollments.models import Enrollment
from reviews.models import Review

from .serializers import DashboardStatsSerializer


@api_view(["GET"])
@cache_page(100)
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    if request.user.role != "ADMIN":
        return Response({"detail": "Only admins can access dashboard stats."}, status=403)

    cache_key = "dashboard_stats"
    cached = cache.get(cache_key)
    if cached:
        return Response(cached)

    User = get_user_model()
    data = {
        "total_users": User.objects.count(),
        "total_courses": Course.objects.count(),
        "total_enrollments": Enrollment.objects.count(),
        "total_reviews": Review.objects.count(),
        "published_courses": Course.objects.filter(is_published=True).count(),
    }

    payload = DashboardStatsSerializer(data).data
    cache.set(cache_key, payload, timeout=600)
    return Response(payload)
