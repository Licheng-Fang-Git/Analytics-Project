from datetime import datetime
from django.shortcuts import render
from django.db.models import Avg
from .models import LinkedInPost
import pandas as pd
from django.http import HttpResponse, JsonResponse
from django import template
import json

import plotly.express as px

filter_df = pd.DataFrame(list(LinkedInPost.objects.values()))
# Create your views here.
def index(request):
    return render(request, 'core/index.html' )

def contact(request):
    return render(request, 'core/contact.html')

def dashboard(request):
    chart_data(request)
    return render(request, 'core/dashboard.html')

def multi_graph_page(request):
    return render(request, 'core/multigraph.html')

def chart_data(request):
    filter_by = request.GET.get('filter_by', 'day_of_week')
    # Query the data from the model
    data = LinkedInPost.objects.values()

    df = pd.DataFrame(list(data))
    df['impressions'] = pd.to_numeric(df['impressions'], errors='coerce')
    
    avg_impressions = df.groupby(filter_by)['impressions'].mean().round()
    if filter_by == 'day_of_week':
        days_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
        avg_impressions = avg_impressions.reindex(days_order).fillna(0)
    
    elif filter_by == 'month':
        months_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        avg_impressions = avg_impressions.reindex(months_order).fillna(0)
    
    
    # Order the days of the week
    
    # # Prepare data for Chart.js
    chart_data = {
        'labels': avg_impressions.index.tolist(),
        'data': avg_impressions.values.tolist(),
    }
    return JsonResponse(chart_data)


def table_data(request):
    filter_by = request.GET.get('filter_by', '')
    comma_idx = filter_by.find(',')
    all_posts = LinkedInPost.objects.values()
    df = pd.DataFrame(list(all_posts))
    print(filter_by)
    if filter_by != '' and "," in filter_by:
        chosen_x = filter_by[:comma_idx]
        label_x = filter_by[comma_idx+1:]
        
        if label_x == 'true':
            filtered_df = df[df[chosen_x] == True].copy()
        elif label_x == 'false':
            filtered_df = df[df[chosen_x] == False].copy()
        elif label_x == 'FnO':
            filtered_df = df[df[chosen_x] == 'F&O'].copy()
            print(filtered_df[chosen_x], filtered_df['post_title'])
        elif ':' in label_x:
            filtered_df = df[df[chosen_x] == datetime.strptime(label_x, "%H:%M:%S").time()].copy()
        else:
            try:
                filtered_df = df[df[chosen_x] == int(label_x)].copy()
            except:
                filtered_df = df[df[chosen_x] == label_x].copy()
    else:
        filtered_df = df.copy() 

    df_to_render = filtered_df[
        ['post_title','post_link', 'impressions', 'day_of_week', 'type_of_post', 'created_date']
        ].copy()
        
    table_data = df_to_render.to_json(orient='records')
    return JsonResponse(table_data, safe=False)

def unique_data(request):
    all_data = LinkedInPost.objects.values()
    df = pd.DataFrame(list(all_data))
    df = df.dropna(subset=['category'])
    
    data = {
        'year': df['year'].unique().tolist(),
        'month': df['month'].unique().tolist(),
        'day_of_week': df['day_of_week'].unique().tolist(),
        'time_interval' : df['time_of_posting'].unique().tolist(),
        'category' : df['category'].unique().tolist(),
        'sub_category' : df['sub_category'].unique().tolist(),
        'emoji' : df['emoji'].unique().tolist(),
        'type_post' : df['type_of_post'].unique().tolist()
    }
    
    return JsonResponse(data)

def filtered_data(request):
    global filter_df
    all_data = LinkedInPost.objects.values()
    df = pd.DataFrame(list(all_data))

    year = list(map(int, request.GET.getlist('year[]')))
    month = request.GET.getlist('month[]')
    day = request.GET.getlist('day_of_week[]')
    time = request.GET.getlist('time_interval[]')
    time = list(map(lambda s: datetime.strptime(s, "%H:%M:%S").time(), time))
    category = request.GET.getlist('category[]')
    sub_category = request.GET.getlist('sub_category[]')
    emoji = list(map(bool, request.GET.getlist('emoji[]')))
    type_post = request.GET.getlist('type_post[]')
    last_filtered = ""
    last_filtered_label = ""
    # Apply filters progressively (just like in Streamlit)
    if year:
        df = df[df['year'].isin(year)]
        last_filtered_label = "year"
        last_filtered = year
    if month:
        df = df[df['month'].isin(month)]
        last_filtered_label = "month"
        last_filtered = month
    if day:
        df = df[df['day_of_week'].isin(day)]
        last_filtered_label = "day_of_week"
        last_filtered = day
    if time:
        df = df[df['time_of_posting'].isin(time)]
        last_filtered_label = "time_of_posting"
        last_filtered = time
    if category:
        df = df[df['category'].isin(category)]
        last_filtered_label = "category"
        last_filtered = category
    if sub_category:
        df = df[df['sub_category'].isin(sub_category)]
        last_filtered_label = "sub_category"
        last_filtered = sub_category
    if emoji:
        df = df[df['emoji'].isin(emoji)]
        last_filtered_label = "emoji"
        last_filtered = emoji
    if type_post:
        df = df[df['type_of_post'].isin(type_post)]
        last_filtered_label = "type_of_post"
        last_filtered = type_post
    if last_filtered != "":
        df['impressions'] = pd.to_numeric(df['impressions'], errors='coerce')
        avg_impressions = df.groupby(last_filtered_label)['impressions'].mean().round()

        filter_chart_data = {
            'labels' : avg_impressions.index.tolist(),
            'data' : avg_impressions.values.tolist(),
            'x_label' : [last_filtered_label]
        }
        
    else:
        avg_impressions = df.groupby('year')['impressions'].mean().round()
        filter_chart_data = {
            'labels' : avg_impressions.index.tolist(),
            'data' : avg_impressions.values.tolist(),
            'x_label' : ['']
        }
    filter_df = df
        # Return filtered data
    return JsonResponse(filter_chart_data)

def filter_select_unique(request):
    global filter_df
    df = filter_df

    filter_select_data = {
        'year': df['year'].unique().tolist(),
        'month': df['month'].unique().tolist(),
        'day_of_week': df['day_of_week'].unique().tolist(),
        'time_interval' : df['time_of_posting'].unique().tolist(),
        'category' : df['category'].unique().tolist(),
        'sub_category' : df['sub_category'].unique().tolist(),
        'emoji' : df['emoji'].unique().tolist(),
        'type_post' : df['type_of_post'].unique().tolist()
    }

    return JsonResponse(filter_select_data)


    


