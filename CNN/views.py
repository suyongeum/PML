from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage

import requests
import json
import cv2

# Create your views here.

def cnn(request):
    return render(request, 'CNN/cnn.html')

def change(request):

    ########################################################################
    if request.method == 'POST' and request.FILES['origin']:
        myfile = request.FILES['origin']
        fs = FileSystemStorage('./bssets/inputs/') #defaults to   MEDIA_ROOT
        filename = fs.save(myfile.name, myfile)

        ###############################################################
        # # Here we know the file is in
        api_host = 'http://35.221.233.111:8000/'
        headers = {'Content-Type': 'image/jpeg'}
        img = cv2.imread('./bssets/inputs/'+ filename)
        _, img_encoded = cv2.imencode('.jpg', img)
        response = requests.post(api_host, data=img_encoded.tostring(), headers=headers)

        return JsonResponse(response)

    #     # content = './bssets/inputs/' + filename
    #     # style   = './CNN/cnn_model/style/starry-night.jpg'
    #     # output  = './bssets/outputs/output.jpg'
    #     # python_command = 'c:/users/adagio/Anaconda3/envs/tensorflow/python.exe'
    #     #
    #     # cmd = python_command + ' ./CNN/cnn_model/run_main.py --content ' + content +  ' --style ' + style + ' --output ' + output
    #     # print(cmd)
    #     # os.system(cmd)
    #     # print(returned_output)
    #
    #     ###############################################################
    #     # Logic to display in the web
    #
    #
    #     file_url = fs.url(filename)
    #     print(file_url)
    #     response = {'image': file_url}
    #     return JsonResponse(response)
    # else:
    #     image = ""
    #     response = {'image': image}
    #     return JsonResponse(response)
    # ########################################################################


