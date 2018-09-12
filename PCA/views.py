from django.shortcuts import render
from . import forms
from sklearn.externals import joblib
import json

# Create your views here.

def pca(request):

    all = joblib.load('PML/pickled/pca_all.sav')
    js_data_all = json.dumps(all)

    return render(request, 'PCA/pca.html', {"js_data_all":js_data_all})

def predict(request):
    if request.method == 'POST':
        form =  forms.CreateWord(request.POST, request.FILES)
        if form.is_valid():
            #save it to db
            return redirect('index')
    else:
        form = forms.CreateWord()
    return render(request, 'PCA/predict.html', {'form': form});

