import os
import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.externals import joblib

class SVMmodel:

    '''
    A class to extract features from data set: the words
    '''

    def __init__(self):
        # feature reading from a file. It can be done from DB
        features = pd.read_csv('./featureExtraction_for_training/total_extracted_features.csv', keep_default_na=False)

        # labels and features (data)
        print (features.columns)
        self.features_for_model = ['len', 'vrlen', 'googlelog', 'pos', 'weblio', 'gutenfq']
        self.labels = features.loc[:, 'difficulty']
        self.features = features.loc[:, self.features_for_model]
        print (len(self.labels))

    def greedSearch(self):
        tuned_parameters = [
            {'C': [10], 'kernel': ['rbf'], 'gamma': [0.1]},
            #{'C': [1, 10, 100], 'kernel': ['rbf'], 'gamma': [1, 0.1, 0.01]},
            #{'C': [10, 100, 1000], 'kernel': ['poly'], 'degree': [5, 10, 15, 20], 'gamma': [0.1, 0.01, 0.001, 0.0001]},
            #{'C': [10, 100, 1000], 'kernel': ['sigmoid'], 'gamma': [0.1, 0.01, 0.001, 0.0001]}
        ]

        model = GridSearchCV(
            SVC(),  # Classifire
            tuned_parameters,  # parms set for optimize
            cv = 10,  # number of blocks for cross-validation
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

        name = 'svm'
        for feature in self.features_for_model:
            name = name + '_' + feature
        name = name + '.sav'

        joblib.dump(self.optimizedModel, os.path.join(dir_path, 'PML/pickled/'+ name))

    def predictSVM(self, given_features):
        print(self.optimizedModel.predict(given_features))

if __name__ == '__main__' :

    svmModel = SVMmodel()
    svmModel.greedSearch() # Parameter search and save the model
    svmModel.makeSVMpickle()  # Making SVM pickle




