from django.shortcuts import render

# Create your views here.
def index(request):
    '''这是主页的视图'''
    return render(request,'index.html')