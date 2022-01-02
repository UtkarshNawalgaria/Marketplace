from django.db import models


class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class ActiveProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(activated_at__isnull=False)
