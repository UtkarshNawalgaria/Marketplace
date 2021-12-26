from django.shortcuts import render

from marketplace.utils.decorators import role_required


@role_required("Customer")
def customer_dashboard_view(request):
    return render(request, "pages/customer.html", {})


@role_required("Seller")
def seller_dashboard_view(request):
    return render(request, "pages/seller.html", {})
