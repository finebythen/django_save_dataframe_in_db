from django.urls import path
from . import views


urlpatterns = [
    path('', views.main, name="Main"),
    path('list/', views.overview, name="Overview"),
]
