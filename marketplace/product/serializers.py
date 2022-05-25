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
            "slug",
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


class ProductListMediaSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[("full", "url"), ("thumbnail", "thumbnail__250x250")]
    )

    class Meta:
        model = ProductMedia
        fields = ("image", "image_alt_text")


class ProductDetailMediaSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(sizes=[("full", "url")])

    class Meta:
        model = ProductMedia
        fields = ("image", "image_alt_text")


class AbstractProductSerializer(serializers.ModelSerializer):
    categories = ProductCategorySerializer(many=True)
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


class ProductListSerializer(AbstractProductSerializer):
    media = ProductListMediaSerializer(many=True, read_only=True)

    class Meta(AbstractProductSerializer.Meta):
        fields = AbstractProductSerializer.Meta.fields + ("media",)


class ProductDetailSerializer(AbstractProductSerializer):
    media = ProductDetailMediaSerializer(many=True, read_only=True)

    class Meta(AbstractProductSerializer.Meta):
        fields = AbstractProductSerializer.Meta.fields + ("media",)

    def create(self, validated_data):
        categories = validated_data.pop("categories")
        category_models = []

        # Create new category or get the already saved category
        for category in categories:
            if not category:
                continue

            cat_name = category.get("name").lower()
            category_objs = Category.objects.filter(name__iexact=cat_name)

            if category_objs.exists():
                category_models.append(category_objs.first())
            else:
                # Create new category
                new_category = Category.objects.create(
                    name=category.get("name"),
                    created_by=validated_data.get("created_by"),
                )
                category_models.append(new_category)

        # create new product instance with the required categories
        new_product = Product.objects.create(**validated_data)
        new_product.category.add(*category_models)

        return new_product
