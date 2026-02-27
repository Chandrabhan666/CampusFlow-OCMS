from django.urls import path

from .views import enrollment_detail, enrollment_list, lecture_progress_detail, lecture_progress_list

urlpatterns = [
    path("enrollments/", enrollment_list, name="enrollment-list"),
    path("enrollments/<int:id>/", enrollment_detail, name="enrollment-detail"),
    path("lecture-progress/", lecture_progress_list, name="lecture-progress-list"),
    path("lecture-progress/<int:id>/", lecture_progress_detail, name="lecture-progress-detail"),
]
