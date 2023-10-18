from django.urls import path, include
from rest_framework.routers import DefaultRouter

from team.views import (
    TypeView,
    TeamView,
)

app_name = "team"

router = DefaultRouter()

router.register("types", TypeView)
router.register("team", TeamView)

urlpatterns = [
    path("", include(router.urls)),
]
