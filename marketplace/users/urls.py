from django.urls import path

from marketplace.users.views import (
    user_detail_view,
    user_logout_view,
    user_redirect_view,
    user_signup_view,
    user_update_view,
)

app_name = "user"
urlpatterns = [
    path("signup/", view=user_signup_view, name="signup"),
    path("logout/", view=user_logout_view, name="logout"),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<int:id>/", view=user_detail_view, name="detail"),
]
