from rest_framework import serializers

from marketplace.product.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        lookup_field="slug", view_name="api:category-detail"
    )

    class Meta:
        model = Category
        fields = ("id", "name", "url")


class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    url = serializers.HyperlinkedIdentityField(
        lookup_field="slug", view_name="api:product-detail"
    )

    class Meta:
        model = Product
        fields = (
            "url",
            "name",
            "sku",
            "slug",
            "description",
            "created_by",
            "categories",
        )
