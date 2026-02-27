from django.urls import path

from .views import me_view, register_user

urlpatterns = [
    path("register/", register_user, name="register"),
    path("me/", me_view, name="me"),
]
