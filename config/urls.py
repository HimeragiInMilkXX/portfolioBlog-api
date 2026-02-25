from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static

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

if settings.DEBUG:
    urlpatterns += static( settings.MEDIA_URL, document_root=settings.MEDIA_ROOT )
