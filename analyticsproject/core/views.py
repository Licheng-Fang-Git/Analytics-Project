from datetime import datetime
from django.shortcuts import render
from django.db.models import Avg
from .models import LinkedInPost
import pandas as pd
from django.http import JsonResponse
from django import template
import json
from django.template.response import TemplateResponse

# Create your views here.
def index(request):
    return render(request, 'core/index.html' )

def contact(request):
    return render(request, 'core/contact.html')

def dashboard(request):
    chart_data(request)
    return render(request, 'core/dashboard.html')

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

    print(df['time_of_posting'].head)
   
    if filter_by != '' and "," in filter_by:
        chosen_x = filter_by[:comma_idx]
        label_x = filter_by[comma_idx+1:]
        
        if label_x == 'true':
            filtered_df = df[df[chosen_x] == True].copy()
        elif label_x == 'false':
            filtered_df = df[df[chosen_x] == False].copy()
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
