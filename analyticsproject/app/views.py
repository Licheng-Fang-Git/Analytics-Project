from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

# Create your views here.
def index(request):
    return render(request, "index.html")

def area_chart(request):
    return render(request, 'area_chart.html')

class HelloEthiopia(View):
    def get(self, request):
        return HttpResponse("Hello Ethiopia")
    


