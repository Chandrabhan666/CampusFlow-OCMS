from django.urls import path

from .frontend_views import delete, detail, edit, index

urlpatterns = [
    path("", index, name="home"),
    path("courses/<int:id>/", detail, name="course-detail-page"),
    path("courses/<int:id>/edit/", edit, name="course-edit-page"),
    path("courses/<int:id>/delete/", delete, name="course-delete-page"),
]
