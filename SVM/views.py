from django.shortcuts import render
from django.http import JsonResponse
from PML.nlp.Lemmatiser import Lemmatiser
from PCA.models import Word
import re

from sklearn.externals import joblib
from SVM.svm_model.featureExtraction import FeatureExtraction

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
                estimated_difficulty = 1;
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

    # 5-1. Feature extraction and prediction
    featureModel = joblib.load('PML/pickled/features.sav')
    svmModel = joblib.load('PML/pickled/svm_len_vrlen_googlelog_pos_weblio_gutenfq.sav')

    not_found_ = []
    for item in not_found:

        print(item[0], item[1])

        word = item[0]
        difficulty = item[1]

        # feature extraction
        featureModel.run_prediction(word)
        f1 = featureModel.len
        f2 = featureModel.vrlen
        f3 = featureModel.google_log
        f4 = featureModel.pos
        f5 = featureModel.weblio
        f6 = featureModel.freq_guten

        # prediction
        difficulty = svmModel.predict([[f1, f2, f3, f4, f5, f6]])[0]
        not_found_.append([word, difficulty])

    response = {'not_found': not_found_, 'found': found}
    return JsonResponse(response)































