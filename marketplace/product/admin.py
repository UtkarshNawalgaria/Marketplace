from django.contrib import admin

from marketplace.product.models import Category, Product, ProductMedia


@admin.register(ProductMedia)
class ProductMediaAdmin(admin.ModelAdmin):
    list_display = ("product",)
    fields = ("product", "image", "image_alt_text")


class ProductMediaInline(admin.TabularInline):
    model = ProductMedia
    fields = ("image_alt_text", "image")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ("name", "slug", "activated_at")
    fields = ("name", "slug", "background_image", "image_alt_text")
    readonly_fields = ("slug", "activated_at", "created_at", "updated_at")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ("name", "slug", "activated_at")
    fields = ("name", "sku", "category", "description")
    readonly_fields = ("activated_at", "created_at", "updated_at")
    inlines = [ProductMediaInline]
