from django.contrib.auth import get_user_model

from rest_framework.viewsets import ModelViewSet

from marketplace.product.mixins import StaffUserPermissionMixin
from marketplace.product.models import Category, Product
from marketplace.product.serializers import CategorySerializer, ProductSerializer

User = get_user_model()


class ProductViewSet(ModelViewSet, StaffUserPermissionMixin):
    queryset = Product.active.all().prefetch_related("category")
    serializer_class = ProductSerializer
    lookup_field = "slug"

    def get_queryset(self):
        """
        Returns the list of products based on the following conditions

        1. If User is not a staff, only return Products that are active.
        2. If User is authenticated and is a staff, return all products.
        """

        # If user is admin, send all products
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return Product.objects.all().prefetch_related("category")

        return super().get_queryset()


class CategoryViewSet(ModelViewSet, StaffUserPermissionMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
