from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user.views import (
    UserView,
    UserMeView,
)

app_name = "user"

router = DefaultRouter()

router.register("users", UserView)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "me/",
        UserMeView.as_view(),
        name="user-me"
    ),
    path(
        "token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair"
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh"
    ),
]
