from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import User
from .models import Review
from .serializers import ReviewSerializer


def _paginate(request, queryset, serializer_cls, page_size=10):
    paginator = PageNumberPagination()
    paginator.page_size = page_size
    page = paginator.paginate_queryset(queryset, request)
    serializer = serializer_cls(page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def review_list(request):
    if request.method == "GET":
        reviews = Review.objects.select_related("student", "course").all()

        if request.user.role != User.Role.ADMIN:
            reviews = reviews.filter(student=request.user)

        student = request.query_params.get("student")
        course = request.query_params.get("course")
        rating = request.query_params.get("rating")
        ordering = request.query_params.get("ordering")
        search = request.query_params.get("search")

        if student:
            reviews = reviews.filter(student_id=student)
        if course:
            reviews = reviews.filter(course_id=course)
        if rating:
            reviews = reviews.filter(rating=rating)
        if search:
            reviews = reviews.filter(comment__icontains=search)
        if ordering in {"created_at", "-created_at", "rating", "-rating"}:
            reviews = reviews.order_by(ordering)

        return _paginate(request, reviews, ReviewSerializer)

    if request.user.role not in {User.Role.STUDENT, User.Role.ADMIN}:
        return Response({"detail": "Only student/admin can create reviews."}, status=403)

    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def review_detail(request, id):
    review = get_object_or_404(Review, id=id)

    if request.user.role != User.Role.ADMIN and review.student_id != request.user.id:
        return Response({"detail": "Not allowed."}, status=403)

    if request.method == "GET":
        return Response(ReviewSerializer(review).data)

    if request.method == "DELETE":
        review.delete()
        return Response(status=204)

    partial = request.method == "PATCH"
    serializer = ReviewSerializer(review, data=request.data, partial=partial)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)
