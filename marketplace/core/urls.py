from django.urls import path

from marketplace.core.views import customer_dashboard_view, seller_dashboard_view

app_name = "core"
urlpatterns = [
    path("seller/dashboard/", seller_dashboard_view, name="seller-dashboard"),
    path("customer/dashboard/", customer_dashboard_view, name="customer-dashboard"),
]
