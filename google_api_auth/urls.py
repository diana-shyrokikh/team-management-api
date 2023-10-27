from django.urls import path

from google_api_auth.views import (
    GoogleLoginView,
    GoogleLoginRedirectView,
)


app_name = "google_api_auth"

urlpatterns = [
    path(
        "login/",
        GoogleLoginView.as_view(),
        name="callback-sdk"
    ),
    path(
        "",
        GoogleLoginRedirectView.as_view(),
        name="redirect-sdk"
    ),
]
