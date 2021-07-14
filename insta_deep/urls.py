from django.urls import path

from . import views

app_name = 'insta_deep'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:keyword>/', views.insta_activate, name='insta_active')
]
