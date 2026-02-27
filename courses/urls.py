from django.urls import path

from .views import (
    category_detail,
    category_list,
    course_detail,
    course_list,
    lecture_detail,
    lecture_list,
    module_detail,
    module_list,
    top_courses,
)

urlpatterns = [
    path("categories/", category_list, name="category-list"),
    path("categories/<int:id>/", category_detail, name="category-detail"),
    path("courses/top/", top_courses, name="course-top"),
    path("courses/", course_list, name="course-list"),
    path("courses/<int:id>/", course_detail, name="course-detail"),
    path("modules/", module_list, name="module-list"),
    path("modules/<int:id>/", module_detail, name="module-detail"),
    path("lectures/", lecture_list, name="lecture-list"),
    path("lectures/<int:id>/", lecture_detail, name="lecture-detail"),
]
