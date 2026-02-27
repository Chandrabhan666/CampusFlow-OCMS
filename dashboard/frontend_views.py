import time

from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect, render

from courses.models import Category, Course


def index(request):
    start = time.time()
    payload = cache.get("index_courses_payload")
    if not payload:
        source = "DB HIT"
        courses = list(
            Course.objects.select_related("category", "instructor")
            .filter(is_published=True)
            .order_by("-created_at")
            .values("id", "title", "level", "price", "description", "category__name", "instructor__full_name")
        )
        payload = {
            "courses": courses,
            "total_courses": Course.objects.count(),
            "published_courses": Course.objects.filter(is_published=True).count(),
            "total_categories": Category.objects.count(),
            "total_instructors": Course.objects.values("instructor").distinct().count(),
        }
        cache.set("index_courses_payload", payload, timeout=60)
    else:
        source = "CACHE HIT"

    duration_ms = (time.time() - start) * 1000
    return render(
        request,
        "courses/index.html",
        {
            "courses": payload["courses"],
            "source": source,
            "time": f"{duration_ms:.2f} ms",
            "total_courses": payload["total_courses"],
            "published_courses": payload["published_courses"],
            "total_categories": payload["total_categories"],
            "total_instructors": payload["total_instructors"],
        },
    )


def detail(request, id):
    item = get_object_or_404(
        Course.objects.select_related("category", "instructor").prefetch_related("modules__lectures"),
        id=id,
    )
    modules = item.modules.all().order_by("order")
    return render(request, "courses/detail.html", {"item": item, "modules": modules})


def edit(request, id):
    item = get_object_or_404(Course, id=id)
    if request.method == "POST":
        item.title = request.POST.get("title")
        item.description = request.POST.get("description")
        item.level = request.POST.get("level")
        item.price = request.POST.get("price")
        item.is_published = request.POST.get("is_published") == "on"
        item.save()
        cache.delete("index_courses_payload")
        return redirect("home")
    return render(request, "courses/edit.html", {"item": item})


def delete(request, id):
    item = get_object_or_404(Course, id=id)
    if request.method == "POST":
        item.delete()
        cache.delete("index_courses_payload")
        return redirect("home")
    return render(request, "courses/delete.html", {"item": item})
