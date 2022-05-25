from django.contrib.auth import get_user_model

from rest_framework.viewsets import ModelViewSet

from marketplace.product.mixins import StaffUserPermissionMixin
from marketplace.product.models import Category, Product
from marketplace.product.serializers import (
    CategorySerializer,
    ProductDetailSerializer,
    ProductListSerializer,
)

User = get_user_model()


class ProductViewSet(StaffUserPermissionMixin, ModelViewSet):
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

        return Product.active.all().prefetch_related("category")

    def get_serializer_class(self):

        if self.action == "list":
            return ProductListSerializer

        return ProductDetailSerializer


class CategoryViewSet(StaffUserPermissionMixin, ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
