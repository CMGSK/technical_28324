from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('input.urls')),
    path('input/', include('input.urls')), # TODO: Clean this
    path('result/', include('input.urls')),
    path("admin/", admin.site.urls),
]
