from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse

from PIL import Image

# Create your views here.

def cnn(request):
    return render(request, 'CNN/cnn.html')

def change(request):


    html = "hello word"

    return HttpResponse(html)

    #return render(request, html)
    #
    # response = {'image': image}
    #
    # return JsonResponse(response)