from django.shortcuts import render
from django.http import JsonResponse
from PML.nlp.Lemmatiser import Lemmatiser
from PCA.models import Word
import re
import dill
import time

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

    lemmas_ = list(set(lemmas))
    print(lemmas_)

    ########################################################################
    # 3. Get rid of special character
    # 4. Difficulty level check from DB
    found = []
    not_found = []
    for word in lemmas_:
        # DB check
        obj = Word.objects.filter(word=word)
        if obj.count() == 0:
            # if the word includes a special character or number
            # not consider it as a word
            if (re.search('[0-9]', word) == None)and(re.search('[a-z]', word) != None):
                # Need to create SVM function
                not_found.append([word, 0])
                # SVM is used to return an inferred difficulty.
        else:
            # if the word includes a special character or number
            # not consider it as a word
            # making [ [word, 1], [word, 3], ... ]
            found.append([obj.first().word, obj.first().difficulty])
            #print("found: ", word)
    ########################################################################
    # 5. If does not exist, classify using SVM result.

    # 5-1. Feature extraction and prediction
    start = time.clock()
    featureModel = dill.load(open(r"PML/pickled/features.dill", "rb"))
    #svmModel = joblib.load('PML/pickled/svm_len_vrlen_googlelog_pos_weblio_gutenfq.sav')
    #svmModel = joblib.load('PML/pickled/svm_len_vrlen_googlelog_pos_weblio.sav')
    svmModel = joblib.load('PML/pickled/svm_len_vrlen_googlelog_pos.sav')
    print("Loading time:", time.clock() - start)

    not_found_ = []
    for item in not_found:

        word = item[0]
        difficulty = item[1]

        print("------------------------------------------------")
        print("Not found word:", word)
        print("------------------------------------------------")

        # feature extraction
        start = time.clock()
        featureModel.run_prediction(word)
        print("feature extraction time:", time.clock() - start)

        f1 = featureModel.len
        f2 = featureModel.vrlen
        f3 = featureModel.google_log
        f4 = featureModel.pos
        f5 = featureModel.weblio
        f6 = featureModel.freq_guten

        print("len:", f1)
        print("vrlen: %.2f" % f2)
        print("google_log: %.2f" % f3)
        print("pos:", f4)
        print("weblio:", f5)
        print("freq_guten:", f6)

        # prediction
        start = time.clock()
        #difficulty = svmModel.predict([[f1, f2, f3, f4, f5, f6]])[0]
        #difficulty = svmModel.predict([[f1, f2, f3, f4])[0]
        difficulty = svmModel.predict([[f1, f2, f3, f4]])[0]
        print("svm running time:", time.clock() - start)
        print('----------------------------------------------')
        print("Difficulty Level is: ", difficulty)
        print('----------------------------------------------')

        not_found_.append([word, int(difficulty)])

    # if not found and not_found_:
    #     pass
    # else:

    response = {'not_found': not_found_, 'found': found}
    return JsonResponse(response)
































