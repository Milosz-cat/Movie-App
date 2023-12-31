from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("base.urls")),
    path("", include("user_management.urls")),
    path("", include("list_management.urls")),
    path("", include("django_prometheus.urls")),
]
