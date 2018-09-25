from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
import os

from CNN.cnn_model.run_main import main as run_style

import CNN.cnn_model.style_transfer

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
        # Here we know the file

        content = './bssets/inputs/' + filename
        style   = './CNN/cnn_model/style/starry-night.jpg'
        output  = './bssets/outputs/output.jpg'

        cmd = 'python ./CNN/cnn_model/run_main.py --content ' + content +  ' --style ' + style + ' --output ' + output
        print(cmd)
        os.system(cmd)
        # print(returned_output)

        ###############################################################
        # Logic to display in the web


        file_url = fs.url(filename)
        print(file_url)
        response = {'image': file_url}
        return JsonResponse(response)
    else:
        image = ""
        response = {'image': image}
        return JsonResponse(response)
    ########################################################################


