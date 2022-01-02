from django.contrib import admin

from marketplace.product.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ("name", "slug", "activated_at")
    fields = ("name",)
    readonly_fields = ("activated_at", "created_at", "updated_at")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ("name", "slug", "activated_at")
    fields = ("name", "category")
    readonly_fields = ("activated_at", "created_at", "updated_at")
