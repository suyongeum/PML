import csv
import numpy as np

from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

class SVMmodel :
    def __init__(self) :
        ch = np.loadtxt('./character.csv', delimiter=',')
        self.difficulty = ch[:, 0]
        self.character  = ch[:, 1:]

        self.crossValidation()

    def crossValidation(self) :

        # index information
        # from 'character.csv'
        # 0: leng  1: vowel  2: conso  3: hitBr  4: hitRe  5: level of weblio
        # from 'oldCharacter.csv'
        # 0: leng  1: hit Brown  2: hit Reuters  3-17: categories in Brown  18: parts of speech  19: length  20: vowels  21: consonants

        # executing PCA
        pca    = PCA(n_components=2)
        tChara = pca.fit_transform(np.hstack((self.character[:, 1:3], self.character[:, 5:6])))
        #tChara = pca.fit_transform(self.character[:, 0:5])

        print(pca.explained_variance_ratio_)

        # splitting character into training and test
        # t = f(x)
        x_train, x_test, t_train, t_test = train_test_split(tChara, self.difficulty, test_size=0.3, random_state=None)

        # defining SVM
        ssc = StandardScaler()
        ssc.fit(x_train)
        x_train_std = ssc.transform(x_train)
        x_test_std  = ssc.transform(x_test)

        model = SVC(kernel='rbf', random_state=None)
        model.fit(x_train_std, t_train)

        # training datas
        expectation  = model.predict(x_train_std)
        accuracy     = accuracy_score(t_train, expectation)
        print('Accuracy of Training： %.2f' % accuracy)

        # test datas
        pred_test = model.predict(x_test_std)
        accuracy_test = accuracy_score(t_test, pred_test)
        print('Accuracy of Test： %.2f' % accuracy_test)

if __name__ == '__main__' :
    SVMmodel()
