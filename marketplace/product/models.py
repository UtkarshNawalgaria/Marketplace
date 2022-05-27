from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

from django_extensions.db.fields import AutoSlugField
from rest_framework.exceptions import ValidationError
from versatileimagefield.fields import PPOIField, VersatileImageField

from marketplace.core.models import BaseModel
from marketplace.product.managers import ActiveProductManager, ProductManager

User = get_user_model()


class Category(BaseModel):
    def upload_path(instance, filename):
        return f"categories/{instance.id}/{filename}"

    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from="name", unique=True)
    activated_at = models.DateTimeField(null=True)

    ppoi = PPOIField("Image PPOI")
    background_image = VersatileImageField(
        upload_to=upload_path, ppoi_field="ppoi", null=True, blank=True
    )
    image_alt_text = models.CharField(max_length=128, null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):

        created = not self.pk
        self.slug = slugify(self.name)

        if created:
            if not self.created_by or (
                self.created_by and not self.created_by.is_staff
            ):
                raise ValidationError("Not allowed to create category.")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Category(name={self.name})"

    def active_products(self):
        return Product.active.filter(category=self)


class Product(BaseModel):

    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from="name", unique=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    category = models.ManyToManyField("Category", related_name="products")

    retail_price = models.DecimalField(
        verbose_name="Price", max_digits=10, decimal_places=2, default=0
    )
    sale_price = models.DecimalField(
        verbose_name="Sale Price",
        max_digits=10,
        decimal_places=2,
        default=0,
        null=True,
        blank=True,
    )

    activated_at = models.DateTimeField(null=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    objects = ProductManager()
    active = ActiveProductManager()

    def __str__(self):
        return f"Product(name={self.name}, sku={self.sku})"

    @property
    def categories(self):
        return self.category.all()

    def save(self, *args, **kwargs):

        created = not self.pk

        if created:
            if not self.created_by or (
                self.created_by and not self.created_by.is_staff
            ):
                raise ValidationError("Not allowed to create new product.")

        super().save(*args, **kwargs)


class ProductMedia(BaseModel):
    def upload_path(instance, filename):
        return f"products/{instance.product.id}/{filename}"

    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="media"
    )

    ppoi = PPOIField("Image PPOI")
    image = VersatileImageField(
        upload_to=upload_path, ppoi_field="ppoi", null=True, blank=True
    )
    image_alt_text = models.CharField(max_length=128, blank=True)

    class Meta:
        verbose_name = "Product Media"
        verbose_name_plural = "Product Media"


class ProductInventory(BaseModel):

    sku = models.CharField(max_length=100, unique=True)
    brand = models.CharField(max_length=100, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    in_stock = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    activated_at = models.DateTimeField(null=True)

    retail_price = models.DecimalField(max_digits=6, decimal_places=2)
    sale_price = models.DecimalField(max_digits=6, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)

    quantity = models.PositiveIntegerField()
    quantity_sold = models.PositiveIntegerField()
    sold_out_at = models.DateTimeField(null=True)

    class Meta:
        verbose_name_plural = "Product Inventory"

    def __str__(self):
        return f"Inventory - {self.product.name}"
