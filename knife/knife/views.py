from django.http import HttpResponse

def index(request):
    return HttpResponse('<a href="/knife/">Clike Me into Knife.</a>')