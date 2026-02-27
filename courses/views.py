from django.core.cache import cache
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.cache import cache_page

from accounts.models import User
from .models import Category, Course, Lecture, Module
from .serializers import CategorySerializer, CourseSerializer, LectureSerializer, ModuleSerializer


def _is_instructor_or_admin(user):
    return user.is_authenticated and user.role in {User.Role.INSTRUCTOR, User.Role.ADMIN}


def _is_course_owner_or_admin(user, course):
    return user.is_authenticated and (course.instructor_id == user.id or user.role == User.Role.ADMIN)


def _paginate(request, queryset, serializer_cls, page_size=10):
    paginator = PageNumberPagination()
    paginator.page_size = page_size
    page = paginator.paginate_queryset(queryset, request)
    serializer = serializer_cls(page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(["GET", "POST"])
@cache_page(100)
@permission_classes([AllowAny])
def category_list(request):
    if request.method == "GET":
        categories = Category.objects.all().order_by("name")
        ordering = request.query_params.get("ordering")
        search = request.query_params.get("search")

        if ordering in {"name", "-name", "created_at", "-created_at"}:
            categories = categories.order_by(ordering)
        if search:
            categories = categories.filter(name__icontains=search)

        return _paginate(request, categories, CategorySerializer)

    if not _is_instructor_or_admin(request.user):
        return Response({"detail": "Only instructor/admin can create categories."}, status=403)

    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@cache_page(100)
@permission_classes([AllowAny])
def category_detail(request, id):
    category = get_object_or_404(Category, id=id)

    if request.method == "GET":
        return Response(CategorySerializer(category).data)

    if not _is_instructor_or_admin(request.user):
        return Response({"detail": "Only instructor/admin can modify categories."}, status=403)

    if request.method == "DELETE":
        category.delete()
        return Response(status=204)

    partial = request.method == "PATCH"
    serializer = CategorySerializer(category, data=request.data, partial=partial)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(["GET", "POST"])
@cache_page(100)
@permission_classes([AllowAny])
def course_list(request):
    if request.method == "GET":
        cache_key = f"course_list:{request.get_full_path()}"
        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        courses = Course.objects.select_related("instructor", "category").filter(is_published=True).order_by("-created_at")

        ordering = request.query_params.get("ordering")
        title = request.query_params.get("title")
        level = request.query_params.get("level")
        category = request.query_params.get("category")

        allowed_ordering = {"created_at", "-created_at", "price", "-price", "title", "-title"}
        if ordering in allowed_ordering:
            courses = courses.order_by(ordering)
        if title:
            courses = courses.filter(title__icontains=title)
        if level:
            courses = courses.filter(level=level)
        if category:
            courses = courses.filter(category_id=category)

        response = _paginate(request, courses, CourseSerializer)
        cache.set(cache_key, response.data, timeout=600)
        return response

    if not _is_instructor_or_admin(request.user):
        return Response({"detail": "Only instructor/admin can create courses."}, status=403)

    serializer = CourseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@cache_page(100)
@permission_classes([AllowAny])
def course_detail(request, id):
    course = get_object_or_404(Course, id=id)

    if request.method == "GET":
        if not course.is_published:
            return Response({"detail": "Course not found."}, status=404)
        return Response(CourseSerializer(course).data)

    if not _is_course_owner_or_admin(request.user, course):
        return Response({"detail": "Only course owner/admin can modify this course."}, status=403)

    if request.method == "DELETE":
        course.delete()
        return Response(status=204)

    partial = request.method == "PATCH"
    serializer = CourseSerializer(course, data=request.data, partial=partial)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(["GET"])
@cache_page(100)
@permission_classes([AllowAny])
def top_courses(request):
    cache_key = "top_courses"
    cached = cache.get(cache_key)
    if cached:
        return Response(cached)

    courses = (
        Course.objects.filter(is_published=True)
        .annotate(enrollments_count=Count("enrollments"))
        .order_by("-enrollments_count", "-created_at")[:10]
    )
    data = CourseSerializer(courses, many=True).data
    cache.set(cache_key, data, timeout=900)
    return Response(data)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def module_list(request):
    if request.method == "GET":
        modules = Module.objects.select_related("course").all()
        course = request.query_params.get("course")
        ordering = request.query_params.get("ordering")

        if course:
            modules = modules.filter(course_id=course)
        if ordering in {"order", "-order"}:
            modules = modules.order_by(ordering)

        return _paginate(request, modules, ModuleSerializer)

    if not _is_instructor_or_admin(request.user):
        return Response({"detail": "Only instructor/admin can create modules."}, status=403)

    serializer = ModuleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def module_detail(request, id):
    module = get_object_or_404(Module, id=id)

    if request.method == "GET":
        return Response(ModuleSerializer(module).data)

    if not _is_instructor_or_admin(request.user):
        return Response({"detail": "Only instructor/admin can modify modules."}, status=403)

    if request.method == "DELETE":
        module.delete()
        return Response(status=204)

    partial = request.method == "PATCH"
    serializer = ModuleSerializer(module, data=request.data, partial=partial)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def lecture_list(request):
    if request.method == "GET":
        lectures = Lecture.objects.select_related("module", "module__course").all()
        module = request.query_params.get("module")
        ordering = request.query_params.get("ordering")
        search = request.query_params.get("search")

        if module:
            lectures = lectures.filter(module_id=module)
        if ordering in {"order", "-order", "duration", "-duration"}:
            lectures = lectures.order_by(ordering)
        if search:
            lectures = lectures.filter(title__icontains=search)

        return _paginate(request, lectures, LectureSerializer)

    if not _is_instructor_or_admin(request.user):
        return Response({"detail": "Only instructor/admin can create lectures."}, status=403)

    serializer = LectureSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def lecture_detail(request, id):
    lecture = get_object_or_404(Lecture, id=id)

    if request.method == "GET":
        return Response(LectureSerializer(lecture).data)

    if not _is_instructor_or_admin(request.user):
        return Response({"detail": "Only instructor/admin can modify lectures."}, status=403)

    if request.method == "DELETE":
        lecture.delete()
        return Response(status=204)

    partial = request.method == "PATCH"
    serializer = LectureSerializer(lecture, data=request.data, partial=partial)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)
