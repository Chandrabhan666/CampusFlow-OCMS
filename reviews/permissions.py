from rest_framework.permissions import SAFE_METHODS, BasePermission

from accounts.models import User


class IsStudentOrAdminForWrite(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in {User.Role.STUDENT, User.Role.ADMIN}
        )


class IsReviewOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(
            request.user
            and request.user.is_authenticated
            and (obj.student_id == request.user.id or request.user.role == User.Role.ADMIN)
        )
