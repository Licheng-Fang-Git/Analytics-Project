from django.urls import path
from . import views

urlpatterns = [
    path("area", views.area_charts, name="app-area-chart"),
    path("index", views.index, name="index")
]