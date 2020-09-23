from rest_framework.permissions import BasePermission

class IsOrganizer(BasePermission):
    message = "You must be the organizer."

    def has_object_permission(self, request, view, obj):
        if obj.organizer == request.user:
            return True
        else:
            return False