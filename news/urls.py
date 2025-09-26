from django.urls import path
from news import views

urlpatterns = [
    path('', views.home, name='news-home'),
    path('post/detail/<int:id>', views.detail, name='detail'),
]
