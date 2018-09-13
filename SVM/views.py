from django.shortcuts import render
from django.http import JsonResponse
from PML.nlp.Lemmatiser import Lemmatiser
from PCA.models import Word
import re
import random

from sklearn.externals import joblib

# Create your views here.

def svm(request):
    return render(request, 'SVM/svm.html')

def check(request):
    text = request.GET.get('text')

    ########################################################################
    # This is the part to verify the sentence

    # 1. Tokenize the sentence
    # 2. Recover the original form of each word
    # 3. Get rid of special character
    # 4. Difficulty level check from DB
    # 5. If does not exist, classify using SVM result.
    ########################################################################
    # 1. Tokenize the sentence
    # 2. Recover the original form of each word

    lemmatiser = Lemmatiser()
    lemmas = lemmatiser.lemmatise_sentence(text)
    print(lemmas)

    ########################################################################
    # 3. Get rid of special character
    # 4. Difficulty level check from DB
    found = []
    not_found = []
    for word in lemmas:
        # DB check
        obj = Word.objects.filter(word=word)
        if obj.count() == 0:
            # if the word includes a special character or number
            # not consider it as a word
            if re.match(r'^\w+$', word):
                # Need to create SVM function
                estimated_difficulty = random.randint(1,12) #SVM(word);
                not_found.append([word, estimated_difficulty])
                print("not found: ", word)
                # SVM is used to return an inferred difficulty.
        else:
            # if the word includes a special character or number
            # not consider it as a word
            if re.match(r'^\w+$', word):
                # making [ [word, 1], [word, 3], ... ]
                found.append([obj.first().word, obj.first().difficulty])
                print("found: ", word)
    ########################################################################
    # 5. If does not exist, classify using SVM result.
    # 5-1. Feature extraction

    svmModel = joblib.load('PML/pickled/svm.sav')
    print(svmModel.predict([[10.00,5.00,5.00,0.00,0.00,6.00]]))


    response = {'not_found': not_found, 'found': found}
    return JsonResponse(response)































