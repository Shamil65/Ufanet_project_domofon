from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('domofon/', include('domofon.urls')),
    path('', include('client.urls')),
]
