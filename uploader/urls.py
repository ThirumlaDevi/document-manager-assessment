from django.urls import path

from . import views

urlpatterns = [
    path('', views.uploadChunk, name='upload-chunk-view'),
    path("/<str:id>", views.get, name='get-chunk-by-id-view')
]