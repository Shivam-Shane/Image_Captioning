"""
URL configuration for IC_django project.
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from IC_django import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('predictor/', views.predictor),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)