from rest_framework import serializers
from versatileimagefield.serializers import VersatileImageFieldSerializer

from marketplace.product.models import Category, Product, ProductMedia


class ProductCategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        lookup_field="slug", view_name="api:category-detail"
    )

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "url",
        )


class CategorySerializer(ProductCategorySerializer):
    background_image = VersatileImageFieldSerializer(
        sizes=[("full", "url"), ("thumbnail", "thumbnail__100x100")]
    )

    class Meta(ProductCategorySerializer.Meta):
        fields = ProductCategorySerializer.Meta.fields + (
            "background_image",
            "image_alt_text",
        )


class ProductMediaSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[("full", "url"), ("thumbnail", "thumbnail__100x100")]
    )

    class Meta:
        model = ProductMedia
        fields = ("image", "image_alt_text")


class ProductSerializer(serializers.ModelSerializer):
    categories = ProductCategorySerializer(many=True, read_only=True)
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    url = serializers.HyperlinkedIdentityField(
        lookup_field="slug", view_name="api:product-detail"
    )
    media = ProductMediaSerializer(many=True, read_only=True)

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
            "media",
        )
