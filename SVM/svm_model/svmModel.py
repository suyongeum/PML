import os
import numpy as np

from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.externals import joblib

class SVMmodel:

    # Default parameters of the SVM model
    C = 1.
    kernel = 'rbf'
    gamma = 0.1
    n_split = 10

    '''
     A class to return a pickled SVM object
     '''
    def __init__(self) :
        # feature reading from a file. It can be done from DB
        ch = np.loadtxt('./character.csv', delimiter=',')

        # Standardization of data set
        ssc = StandardScaler()
        ssc.fit(ch[:, 1:])

        # labels and features (data)
        self.labels = ch[:, 0]
        self.features  = ssc.transform(ch[:, 1:])

    def greedSearch(self):
        pass

    def makeSVMpickle(self):
        model = SVC(C=self.C, kernel=self.kernel, gamma=self.gamma)
        model.fit(self.features, self.labels)
        #label = model.predict(self.features)

        # save the model to disk
        dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        joblib.dump(model, os.path.join(dir_path, 'PML/pickled/svm.sav'))


    # def runSVM(self):
    #     model = SVC(kernel='rbf', random_state=None)
    #     model.fit(x_train_std, t_train)
    #
    #     # training datas
    #     expectation  = model.predict(x_train_std)
    #     accuracy     = accuracy_score(t_train, expectation)
    #     print('Accuracy of Training： %.2f' % accuracy)
    #
    #     # test datas
    #     pred_test = model.predict(x_test_std)
    #     accuracy_test = accuracy_score(t_test, pred_test)
    #     print('Accuracy of Test： %.2f' % accuracy_test)


    # def crossValidation(self) :
    #     index information
    #     from 'character.csv'
    #     0: leng  1: vowel  2: conso  3: hitBr  4: hitRe  5: level of weblio
    #
    #     executing PCA
    #     pca    = PCA(n_components=2)
    #     tChara = pca.fit_transform(np.hstack((self.character[:, 1:3], self.character[:, 5:6])))
    #     #tChara = pca.fit_transform(self.character[:, 0:5])
    #
    #     print(pca.explained_variance_ratio_)
    #
    #     # splitting character into training and test
    #     # t = f(x)
    #     x_train, x_test, t_train, t_test = train_test_split(tChara, self.difficulty, test_size=0.3, random_state=None)


if __name__ == '__main__' :
    svmModel = SVMmodel()
    svmModel.makeSVMpickle();
    # print(svmModel.word_tagging())

