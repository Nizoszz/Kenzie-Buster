from rest_framework import permissions
from rest_framework.views import Request, View
from movies.models import MovieOrder


class IsMovieOrder(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View,
                              obj: MovieOrder) -> bool:
        return True