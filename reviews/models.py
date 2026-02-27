from django.conf import settings
from django.db import models

from courses.models import Course


class Review(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["student", "course"], name="unique_student_course_review"),
            models.CheckConstraint(condition=models.Q(rating__gte=1) & models.Q(rating__lte=5), name="rating_between_1_and_5"),
        ]

    def __str__(self):
        return f"{self.student.email} rated {self.course.title}"
