from django.db import models
from django_extensions.db.fields import AutoSlugField

from marketplace.core.models import BaseModel
from marketplace.product.managers import ActiveProductManager, ProductManager


class Product(BaseModel):

    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from="name")
    description = models.TextField(max_length=500)
    activated_at = models.DateTimeField(null=True)
    category = models.ManyToManyField("Category", related_name="products")

    objects = ProductManager()
    active = ActiveProductManager()

    def __str__(self):
        return f"Product<name='{self.name}'>"

    @property
    def categories(self):
        return self.category.all()


class Category(BaseModel):

    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from="name")
    activated_at = models.DateTimeField(null=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"Category<name='{self.name}'>"

    def active_products(self):
        return Product.active.filter(category=self)


class ProductInventory(BaseModel):

    sku = models.CharField(max_length=10, unique=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    brand = models.CharField(max_length=50, null=True)

    activated_at = models.DateTimeField(null=True)
    is_default = models.BooleanField(default=False)
    in_stock = models.BooleanField(default=True)

    retail_price = models.DecimalField(max_digits=6, decimal_places=2)
    sale_price = models.DecimalField(max_digits=6, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)

    quantity = models.PositiveIntegerField()
    quantity_sold = models.PositiveIntegerField()
    last_sold_at = models.DateTimeField(null=True)

    class Meta:
        verbose_name_plural = "Product Inventory"

    def __str__(self):
        return f"Inventory - {self.product.name}"
