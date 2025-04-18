from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("post/<slug:title>/", views.post, name="post"),
    path("category/<str:name>/", views.category, name="category"),
    path("search/", views.search, name="search"),
    path("create-post/", views.create_post, name="create_post"),
    path('login/', LoginView.as_view(), name='blog_login'),
    # path('logout/', LogoutView.as_view(), name='blog_logout'),
    path('logout/', views.custom_logout, name='blog_logout'),
    path('accounts/profile/', views.user_profile, name='user_profile'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('my-posts/', views.my_posts, name='my_posts'),
    path('delete-post/<slug:slug>/', views.delete_post, name='delete_post'),
    path('register/', views.register, name='register'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
]
