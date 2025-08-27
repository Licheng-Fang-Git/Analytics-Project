from django.shortcuts import render
from django.db.models import Avg
from .models import LinkedInPost
import pandas as pd
from django.http import JsonResponse

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

def create_tables(request):
    filter_by = request.GET.get('filter_by', '')
    comma_idx = filter_by.find(',')
    if filter_by != '':
        chosen_x = filter_by[:comma_idx]
        label_x = filter_by[comma_idx+1:]
        data = LinkedInPost.objects.values()
        df = pd.DataFrame(data)
        filtered_df = df[df[chosen_x] == int(label_x)].copy()
        print(filtered_df[chosen_x])
        

    table_data = {
        'data': [1,2,3]
    }
    return JsonResponse(table_data)
