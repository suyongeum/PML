import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.externals import joblib
from enum import Enum as enum

class SVMmodel:

    '''
    A class to extract features from data set: the words
    '''

    def __init__(self):
        # feature reading from a file. It can be done from DB
        dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        features = pd.read_csv(
            os.path.join(dir_path, 'SVM\\svm_model\\total_extracted_features.csv'),
            encoding="shift-jis", keep_default_na=False)

        # Standardization of data set - probably we do not need
        #ssc = StandardScaler()
        #ssc.fit(ch[:, 1:])
        # self.features  = ssc.transform(ch[:, 1:])

        # labels and features (data)
        self.labels = features.iloc[1:, 2]
        #           4       5          6             7            8          9           10          11             12         13
        #features['len', 'vrlen', 'freq_brown', 'freq_reuter', 'weblio', 'bing_log', 'yahoo_log', 'google_log', 'freq_guten','pos']

        print(features.iloc[0, :])

        self.features = features.iloc[1:, ['len', 'vrlen', 'weblio', 'google_log', 'freq_guten', 'pos']]
        #self.features = features.iloc[1:, ['len', 'vrlen', 'weblio', 'google_log', 'freq_guten', 'pos']]
        #self.features = features.iloc[1:, [4, 5, 8, 11, 12, 13]]

    def greedSearch(self):
        tuned_parameters = [
            {'C': [10], 'kernel': ['rbf'], 'gamma': [0.1]},
            #{'C': [1, 10, 100, 1000], 'kernel': ['rbf'], 'gamma': [1, 0.1, 0.01, 0.001, 0.0001]},
            #{'C': [10, 100, 1000], 'kernel': ['poly'], 'degree': [5, 10, 15, 20], 'gamma': [0.1, 0.01, 0.001, 0.0001]},
            #{'C': [10, 100, 1000], 'kernel': ['sigmoid'], 'gamma': [0.1, 0.01, 0.001, 0.0001]}
        ]

        model = GridSearchCV(
            SVC(),  # Classifire
            tuned_parameters,  # parms set for optimize
            cv = 10,  # number of cross-validation
            verbose = True,
            scoring = 'f1_weighted')  # evaluation func. for this model
        model.fit(self.features, self.labels)

        # parameter search
        print (model.best_params_)
        print (model.best_score_)
        print (model.best_estimator_) # actually this one returns a function which can be used to predict ...
        self.optimizedModel = model.best_estimator_

    def makeSVMpickle(self):
        # save the model to disk
        dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        joblib.dump(self.optimizedModel, os.path.join(dir_path, 'PML/pickled/svm.sav'))

    def predictSVM(self, given_features):
        print(self.optimizedModel.predict(given_features))

if __name__ == '__main__' :

    svmModel = SVMmodel()
    #svmModel.greedSearch() # Parameter search and save the model
    # svmModel.makeSVMpickle()  # Parameter search
    # svmModel.predictSVM([[10.00,5.00,5.00,0.00,0.00,6.00]])
    # print(svmModel.word_tagging())

