from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import User
from .models import Enrollment, LectureProgress
from .serializers import EnrollmentSerializer, LectureProgressSerializer


def _paginate(request, queryset, serializer_cls, page_size=10):
    paginator = PageNumberPagination()
    paginator.page_size = page_size
    page = paginator.paginate_queryset(queryset, request)
    serializer = serializer_cls(page, many=True)
    return paginator.get_paginated_response(serializer.data)


def _is_student_or_admin(user):
    return user.is_authenticated and user.role in {User.Role.STUDENT, User.Role.ADMIN}


def _owns_enrollment_or_admin(user, enrollment):
    return user.role == User.Role.ADMIN or enrollment.student_id == user.id


def _owns_progress_or_admin(user, progress):
    return user.role == User.Role.ADMIN or progress.enrollment.student_id == user.id


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def enrollment_list(request):
    if request.method == "GET":
        enrollments = Enrollment.objects.select_related("student", "course").all()

        if request.user.role != User.Role.ADMIN:
            enrollments = enrollments.filter(student=request.user)

        student = request.query_params.get("student")
        course = request.query_params.get("course")
        status_value = request.query_params.get("status")
        ordering = request.query_params.get("ordering")

        if student:
            enrollments = enrollments.filter(student_id=student)
        if course:
            enrollments = enrollments.filter(course_id=course)
        if status_value:
            enrollments = enrollments.filter(status=status_value)
        if ordering in {"enrolled_at", "-enrolled_at"}:
            enrollments = enrollments.order_by(ordering)

        return _paginate(request, enrollments, EnrollmentSerializer)

    if not _is_student_or_admin(request.user):
        return Response({"detail": "Only student/admin can create enrollments."}, status=403)

    serializer = EnrollmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def enrollment_detail(request, id):
    enrollment = get_object_or_404(Enrollment, id=id)

    if request.user.role != User.Role.ADMIN and enrollment.student_id != request.user.id:
        return Response({"detail": "Not allowed."}, status=403)

    if request.method == "GET":
        return Response(EnrollmentSerializer(enrollment).data)

    if not _owns_enrollment_or_admin(request.user, enrollment):
        return Response({"detail": "Not allowed."}, status=403)

    if request.method == "DELETE":
        enrollment.delete()
        return Response(status=204)

    partial = request.method == "PATCH"
    serializer = EnrollmentSerializer(enrollment, data=request.data, partial=partial)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def lecture_progress_list(request):
    if request.method == "GET":
        records = LectureProgress.objects.select_related("enrollment", "lecture").all()

        if request.user.role != User.Role.ADMIN:
            records = records.filter(enrollment__student=request.user)

        enrollment = request.query_params.get("enrollment")
        lecture = request.query_params.get("lecture")
        completed = request.query_params.get("completed")

        if enrollment:
            records = records.filter(enrollment_id=enrollment)
        if lecture:
            records = records.filter(lecture_id=lecture)
        if completed is not None:
            if completed.lower() in {"true", "1"}:
                records = records.filter(completed=True)
            elif completed.lower() in {"false", "0"}:
                records = records.filter(completed=False)

        return _paginate(request, records, LectureProgressSerializer)

    if not _is_student_or_admin(request.user):
        return Response({"detail": "Only student/admin can create progress records."}, status=403)

    serializer = LectureProgressSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def lecture_progress_detail(request, id):
    progress = get_object_or_404(LectureProgress, id=id)

    if request.user.role != User.Role.ADMIN and progress.enrollment.student_id != request.user.id:
        return Response({"detail": "Not allowed."}, status=403)

    if request.method == "GET":
        return Response(LectureProgressSerializer(progress).data)

    if not _owns_progress_or_admin(request.user, progress):
        return Response({"detail": "Not allowed."}, status=403)

    if request.method == "DELETE":
        progress.delete()
        return Response(status=204)

    partial = request.method == "PATCH"
    serializer = LectureProgressSerializer(progress, data=request.data, partial=partial)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)
