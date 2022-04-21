from django.forms import ModelForm
from django.utils import timezone

from marketplace.product.models import Category


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = "name"

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.activated_at = timezone.now()
        instance.save()

        return instance
