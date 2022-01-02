from django.urls import path

from marketplace.core.views import (
    customer_dashboard_view,
    seller_dashboard_view,
)

app_name = "core"
urlpatterns = [
    path("s/dashboard/", seller_dashboard_view, name="seller-dashboard"),
    path("c/dashboard/", customer_dashboard_view, name="customer-dashboard"),
]
