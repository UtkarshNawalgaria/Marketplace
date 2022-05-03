from rest_framework.permissions import DjangoModelPermissions, IsAdminUser


class StaffUserPermissionMixin:
    def get_permissions(self):
        """
        1. Any user can GET all the products.
        2. Only Staff user can UPDATE/DELETE any product
        """

        if self.action in ["list", "retrieve"]:
            permission_classes = []
        else:
            permission_classes = [IsAdminUser, DjangoModelPermissions]

        return [permission() for permission in permission_classes]
