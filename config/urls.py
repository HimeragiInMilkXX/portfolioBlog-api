from django.contrib import admin
from django.urls import path, include, re_path
from django.http import JsonResponse
from django.conf import settings
from django.views.static import serve
import os

def hello_api(request):
    data = {

        "message": "Hello from your nomo",
        "framework": "Django"

    }
    return JsonResponse(data)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/hello/", hello_api),
    path("api/", include("blog.urls")),
    path("api/", include("accounts.urls"))
]

if settings.DEBUG or os.environ.get("SERVE_MEDIA", "False").lower() == "true":
    urlpatterns += [
        re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    ]
