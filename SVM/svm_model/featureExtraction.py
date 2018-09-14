import os
import nltk
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup
import math
import random
from sklearn.externals import joblib

class FeatureExtraction:

    # 'len', 'vrlen', 'weblio', 'google_log', 'freq_guten', 'pos'

    def __init__(self):
        self.len = 0
        self.vrlen = 0
        self.weblio = 0
        self.google_log = 0
        self.freq_guten = 0
        self.pos = 0
        features = pd.read_csv('./featureExtraction_for_training/total_extracted_features.csv', keep_default_na=False)
        self.words = features.loc[:, 'word']
        self.guten_all = features.loc[:, 'gutenfq']

    def run_prediction(self, word):
        # obtain features of the given word
        self.fvrlen(word)
        self.fweblio(word)
        self.fgoogle_log(word)
        #self.ffreq_guten(word)
        self.ffreq_guten_mod(word)
        self.fpos(word)

    def fvrlen(self, word):
        self.len = len(word)
        count = 0
        count = word.count('a')
        count += word.count('i')
        count += word.count('u')
        count += word.count('e')
        count += word.count('o')
        self.vrlen = count / len(word)

    def fweblio(self, word):
        req = urllib.request.Request('https://ejje.weblio.jp/content/' + word,
                                     headers={'User-Agent': 'PracticalMachineLearning'})
        f = urllib.request.urlopen(req)
        bsObj = BeautifulSoup(f.read(), "html.parser")
        learning_level = bsObj.find('span', class_='learning-level-content')
        f.close()
        self.weblio = learning_level.text

    def fgoogle_log(self, word):
        req = urllib.request.Request('https://www.google.com/search?q=' + word,
                                     headers={'User-Agent': 'PracticalMachineLearning' + str(random.randint(0, 500))})
        f = urllib.request.urlopen(req)
        bsObj = BeautifulSoup(f.read(), "html.parser")
        site_num_ori = bsObj.find('div', id='resultStats').string
        site_num = int(site_num_ori.replace('約 ', '').replace(',', '').replace(' 件', ''))
        f.close()
        self.google_log =math.log10(site_num)

    def ffreq_guten(self, word):
        datasets = nltk.corpus.gutenberg.fileids()
        total_freq = 0
        for i in range(0, len(datasets)):
            fdist = nltk.FreqDist(nltk.Text(nltk.corpus.gutenberg.words(str(datasets[i]))))
            total_freq = total_freq + fdist[word]
        self.freq_guten = total_freq

    def ffreq_guten_mod(self, word):
        min=100
        for word_, guten_freq in zip(self.words, self.guten_all):
            distance = nltk.edit_distance(word_, word)
            if distance < min:
                min = distance
                close_word = word_
                self.freq_guten = guten_freq
        #print(close_word, self.freq_guten)

    def fpos(self, word):
        a = nltk.pos_tag([word])
        #preparing category of simplified parts of speech
        noun = ('NN', 'NNS', 'NP', 'IN', 'CD', 'FW', 'CC', 'UH')
        adj  = ('JJ', 'JJR', 'JJS')
        verb = ('RP', 'VB', 'VBD', 'VBG', 'VBN', 'VBZ', 'VBP', 'VD', 'VDD', 'VDG', 'VDN', 'VDZ', 'VDP', 'VH', 'VHD', 'VHG', 'VHN', 'VHZ', 'VHP', 'VV', 'VVD', 'VVG', 'VVN', 'VVP', 'VVZ', 'POS')
        adv  = ('RB', 'RBR', 'RBS', 'WDT', 'DT', 'WP', 'MD', 'TO')

        tag = a[0][1]

        for n in noun :
            if n in tag :
                self.pos = 1
                return
        for j in adj :
            if j in tag :
                self.pos = 3
                return
        for v in verb :
            if v in tag :
                self.pos = 5
                return
        for av in adv :
            if av in tag :
                self.pos = 7
                return
        self.pos = 10

    def makeFeaturepickle(self):
        # save the model to disk
        dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        joblib.dump(self, os.path.join(dir_path, 'PML/pickled/features.sav'))

if __name__ == '__main__' :

    svmFeatures = FeatureExtraction()
    svmFeatures.makeFeaturepickle()






































