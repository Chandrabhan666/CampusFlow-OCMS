from django.contrib import admin

from .models import Enrollment, LectureProgress


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "status", "enrolled_at")
    list_filter = ("status",)
    search_fields = ("student__email", "course__title")


@admin.register(LectureProgress)
class LectureProgressAdmin(admin.ModelAdmin):
    list_display = ("enrollment", "lecture", "completed", "completed_at")
    list_filter = ("completed",)
