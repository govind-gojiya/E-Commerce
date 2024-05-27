from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    # To make permissions just override the has_permission method
    def has_permission(self, request, view):
        # if request.method == 'GET': # Not to use this because it will block HEAD and OPTIONS request which is safe method so include it to
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)
    
class FullDjangoModelPermission(permissions.DjangoModelPermissions):
    def __init__(self) -> None:
        self.perms_map['GET'] = ['%(app_label)s.add_%(model_name)s']

class ViewCustomerHistoryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('store.view_history')