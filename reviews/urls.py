from django.urls import path

from .views import review_detail, review_list

urlpatterns = [
    path("", review_list, name="review-list"),
    path("<int:id>/", review_detail, name="review-detail"),
]
