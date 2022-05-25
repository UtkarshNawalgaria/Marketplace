from rest_framework.routers import DefaultRouter

from marketplace.product.views import CategoryViewSet, ProductViewSet
from marketplace.users.views import UserViewSet

app_name = "api"
router = DefaultRouter()

router.register("users", UserViewSet)
router.register("category", CategoryViewSet)
router.register("products", ProductViewSet, basename="product")


urlpatterns = router.urls
