from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="firstapp-index"),
    path('class', views.HelloEthiopia.as_view())
]