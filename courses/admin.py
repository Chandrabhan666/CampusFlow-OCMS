from django.contrib import admin

from .models import Category, Course, Lecture, Module


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    search_fields = ("name", "slug")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "instructor", "category", "level", "price", "is_published", "created_at")
    list_filter = ("level", "is_published", "category")
    search_fields = ("title", "description")


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order")
    list_filter = ("course",)


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ("title", "module", "order", "duration")
    list_filter = ("module",)
    search_fields = ("title",)
