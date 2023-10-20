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
        "api/v1/schema/redoc/",
        SpectacularRedocView.as_view(url_name="doc"),
        name="redoc"
    ),

    path("__debug__/", include("debug_toolbar.urls")),

    path("admin/", admin.site.urls),

    path(
        "api/v1/team/", include(
            "team.urls", namespace="team"
        ),
    ),
    path(
        "api/v1/user/", include(
            "user.urls", namespace="user"
        ),
    ),
] + static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
)
