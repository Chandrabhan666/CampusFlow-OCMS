from django.conf import settings
from django.db import models

from courses.models import Course, Lecture


class Enrollment(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        COMPLETED = "COMPLETED", "Completed"

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["student", "course"], name="unique_student_course_enrollment"),
        ]
        ordering = ["-enrolled_at"]

    def __str__(self):
        return f"{self.student.email} -> {self.course.title}"


class LectureProgress(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name="lecture_progress")
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name="progress_records")
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Progress({self.enrollment_id}, {self.lecture_id})"
