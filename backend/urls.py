from django.contrib import admin
from django.urls import include, path

from .api import api

urlpatterns = [
    path('', include('backend.expense.urls', namespace='expense')),
    path('admin/', admin.site.urls),
    path('api/v2/', api.urls),
]
