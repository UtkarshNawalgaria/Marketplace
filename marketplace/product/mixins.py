from rest_framework.permissions import DjangoModelPermissions, IsAdminUser

from marketplace.product.permissions import IsStoreStaffAdminUser


class StaffUserPermissionMixin:
    def get_permissions(self):
        """
        1. Any user can GET all the products.
        2. Only Staff user can CREATE/UPDATE/DELETE any product
        """

        permission_classes = []

        if self.action not in ["list", "retrieve"]:
            permission_classes = [IsStoreStaffAdminUser]

        return [permission() for permission in permission_classes]
