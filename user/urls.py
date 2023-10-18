from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user.views import UserView

app_name = "user"

router = DefaultRouter()

router.register("users", UserView)

urlpatterns = [
    path("", include(router.urls)),
]
