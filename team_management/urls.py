"""
URL configuration for team_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
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
        "api/doc/",
        SpectacularAPIView.as_view(),
        name='doc'
    ),
    path(
        "api/doc/swagger/",
        SpectacularSwaggerView.as_view(url_name="doc"),
        name="swagger"
    ),
    path(
        "api/schema/redoc/",
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
