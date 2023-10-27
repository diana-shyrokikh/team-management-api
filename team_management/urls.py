"""
URL configuration for team_management project.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from rest_framework.routers import DefaultRouter

from team.views import (
    TypeView,
    TaskView,
    TeamView,
)
from user.views import UserView

router = DefaultRouter()

router.register("types", TypeView)
router.register("teams", TeamView)
router.register("tasks", TaskView)
router.register("users", UserView)

urlpatterns = [
    path(
        "api/v1/doc/",
        SpectacularAPIView.as_view(),
        name='doc'
    ),
    path(
        "api/v1/doc/swagger/",
        SpectacularSwaggerView.as_view(url_name="doc"),
        name="swagger"
    ),
    path(
        "api/v1/doc/redoc/",
        SpectacularRedocView.as_view(url_name="doc"),
        name="redoc"
    ),

    path(
        "__debug__/",
        include("debug_toolbar.urls")
    ),

    path("admin/", admin.site.urls),

    path(
        "api/v1/team-management/",
        include(router.urls),
    ),
    path(
        "api/v1/team-management/users/", include(
            "user.urls", namespace="user"
        ),
    ),
] + static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
)
