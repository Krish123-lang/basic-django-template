from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('post/create', views.create_post, name='post-create'),
    path('post/edit/<int:id>/', views.edit_post, name='post-edit'),
    path('post/delete/<int:id>/', views.delete_post, name='post-delete'),
]
