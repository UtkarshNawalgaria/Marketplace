import utils.decorators
from django.shortcuts import render


@utils.decorators.role_required("Customer")
def customer_dashboard_view(request):
    return render(request, "pages/customer.html", {})


@utils.decorators.role_required("Seller")
def seller_dashboard_view(request):
    return render(request, "pages/seller.html", {})
