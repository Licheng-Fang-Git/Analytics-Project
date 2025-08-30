from django.shortcuts import render
from .models import Followers
import pandas as pd
from django.http import JsonResponse
from datetime import datetime

def follower_chart(request):
    data = Followers.objects.values()

    df = pd.DataFrame(list(data))

    follower_chart_data = {
        'dates' : df['date'].to_list(),
        'total_follower' : df['total_follower_count'].to_list()
    }

    return JsonResponse(follower_chart_data, safe=False)

def monthly_chart(request):
    data = Followers.objects.values()

    df = pd.DataFrame(list(data))
    df['date'] = pd.to_datetime(df['date'])
    df = df[df['date'] >= '2025-08-15']

    follower_chart_data = {
        'dates' : df['date'].to_list(),
        'follower' : df['follower_increase'].to_list()
    }

    return JsonResponse(follower_chart_data, safe=False)



