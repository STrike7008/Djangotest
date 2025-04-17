from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path("", views.galery, name="gallery"),
    path('upload/', views.upload, name='upload_image'),
]
