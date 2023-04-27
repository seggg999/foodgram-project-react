from rest_framework import permissions


class IsAutherOrReadOnly(permissions.BasePermission):
    '''Права изменения доступны автору'''
    def has_object_permission(self, request, view, obj):
        return bool(request.method in permissions.SAFE_METHODS
                    or request.user == obj.author
                    )
