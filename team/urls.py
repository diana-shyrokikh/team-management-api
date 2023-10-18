from django.urls import path, include
from rest_framework.routers import DefaultRouter

from team.views import (
    TypeView,
    TeamView,
    TaskView,
)

app_name = "team"

router = DefaultRouter()

router.register("types", TypeView)
router.register("teams", TeamView)
router.register("tasks", TaskView)

urlpatterns = [
    path("", include(router.urls)),
]
