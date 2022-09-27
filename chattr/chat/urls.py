from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('channel/<int:channel_id>/', views.channel, name='channel'),
]
