from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from foodsystem.reports_views import ReportsAPIView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('foodsystem.urls')),
    path(
    "api/reports/",
    ReportsAPIView.as_view(),
    name="reports"
),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)