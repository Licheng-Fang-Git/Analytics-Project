from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

# Create your views here.
def index(request):
    return render(request, "index.html")

def area_charts(request):
    return render(request, 'area_chart.html')

def hello_world(request):
    return HttpResponse("Hello world")

class HelloEthiopia(View):
    def get(self, request):
        return HttpResponse("Hello Ethiopia")
    


