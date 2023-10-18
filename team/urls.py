from django.urls import path, include
from rest_framework.routers import DefaultRouter

from team.views import TypeView

app_name = "team"

router = DefaultRouter()

router.register("types", TypeView)

urlpatterns = [
    path("", include(router.urls)),
]
