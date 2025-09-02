"""
URL configuration for analyticsproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core.views import index, contact, dashboard, chart_data, table_data, unique_data, filtered_data, filter_select_unique, language, get_hashtags
from core.views import get_hashtag_table
from overall.views import follower_chart, monthly_chart

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index, name='index'),
    path("contact/", contact, name='contact' ),
    path("dashboard/", dashboard, name ='dashboard'),
    path("language_page/", language, name='language_page'),
    path("api/chart_data/", chart_data, name='chart_data'),
    path("api/table_data/", table_data, name='table_data'),
    path('api/unique_data/', unique_data, name = 'unique_data'),
    path('api/filtered_data/', filtered_data, name = 'filitered_data'),
    path('api/filter_select/', filter_select_unique, name='filter_select'),
    path('api/follower_chart/', follower_chart, name='follower_chart'),
    path('api/monthly_chart/', monthly_chart, name='monthly_chart'),
    path('api/get_hashtags/', get_hashtags, name='get_hashtags'),
    path('api/get_hashtag_table/', get_hashtag_table, name='get_hashtag_table'),
]
