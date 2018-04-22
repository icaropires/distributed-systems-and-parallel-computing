from django.contrib import admin
from django.conf.urls import url, include

urlpatterns = [
    url('^api/', include('api.urls')),
]
