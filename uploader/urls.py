from django.urls import path

from . import views

urlpatterns = [
    path('', views.uploadChunk, name='uploadChunk'),
    # path("/api/o", views.home, name='home'),
    # path('<path:resource>', views.home, name='home'),
]