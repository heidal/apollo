from typing import List, Type, TypeVar

from rest_framework.permissions import BasePermission
from rest_framework.settings import api_settings

BasePermissionType = TypeVar("BasePermissionType", bound=BasePermission)


def get_default_permission_classes() -> List[BasePermissionType]:
    """
    Get a copy of the default permission classes.

    Accessing the default permission classes directly yields a mutable instance
    that is easy to break when we try adding new permissions to it.
    :return: List of permission classes
    """
    return api_settings.DEFAULT_PERMISSION_CLASSES.copy()
