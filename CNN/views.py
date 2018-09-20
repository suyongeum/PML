from django.shortcuts import render

# Create your views here.

def cnn(request):
    return render(request, 'CNN/cnn.html')