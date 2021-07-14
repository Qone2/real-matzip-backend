from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('<str:file_name>/', views.image_show, name='insta_active'),
]
