from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Course(models.Model):
    class Level(models.TextChoices):
        BEGINNER = "Beginner", "Beginner"
        INTERMEDIATE = "Intermediate", "Intermediate"
        ADVANCED = "Advanced", "Advanced"

    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    level = models.CharField(max_length=20, choices=Level.choices)
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="courses")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="courses")
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules")
    title = models.CharField(max_length=255)
    order = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["course", "order"], name="unique_module_order_per_course"),
        ]
        ordering = ["order"]

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Lecture(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="lectures")
    title = models.CharField(max_length=255)
    video_url = models.TextField()
    notes = models.TextField(blank=True)
    order = models.IntegerField()
    duration = models.IntegerField(help_text="Duration in seconds")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["module", "order"], name="unique_lecture_order_per_module"),
        ]
        ordering = ["order"]

    def __str__(self):
        return f"{self.module.title} - {self.title}"
