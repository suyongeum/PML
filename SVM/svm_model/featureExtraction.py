import os
import nltk
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup
import math
import random
import dill
import re
import time
import difflib

class FeatureExtraction:

    # 'len', 'vrlen', 'weblio', 'google_log', 'freq_guten', 'pos'

    def __init__(self):
        self.len = 0
        self.vrlen = 0
        self.weblio = 0
        self.google_log = 0
        self.freq_guten = 0
        self.pos = 0
        self.close_word = ''
        self.features = pd.read_csv('./featureExtraction_for_training/total_extracted_features.csv', keep_default_na=False)
        self.words = self.features.loc[:, 'word']

    def run_prediction(self, word):
        # obtain features of the given word
        self.search_similar_word_v1(word)  # set self.close_word, self.close_word_index
        self.fvrlen(word)
        self.fweblio_mod(word)
        self.fgoogle_log_mod(word)
        self.ffreq_guten_mod(word)
        self.fpos_mod(word)

        # self.search_similar_word(word)  # set self.close_word, self.close_word_index
        # self.fvrlen(word)
        # self.fweblio(word)
        # self.fgoogle_log(word)
        # self.ffreq_guten(word)
        # self.fpos(word)

    def search_similar_word(self, word):
        min = 100
        index = 0
        for word_ in self.words:
            distance = nltk.edit_distance(word_, word)
            if distance < min:
                min = distance
                self.close_word = word_
                self.close_word_index = index
            index = index + 1
        print('search:', self.close_word)

    def search_similar_word_v1(self, word):
        found = difflib.get_close_matches(word, self.words)
        print("3 similar words:", found)
        if found:
            for i in found:
                if i[0] == word[0]:
                    self.close_word = i
                    break
            for i in found:
                if re.search(i, word+'[a-z]'):
                    self.close_word = i
                    break
            if not self.close_word:
                self.close_word = found[0]
        else:
            self.close_word = 'condolence'
        print('----------------------------------------------')
        print('original word:', word, '-- diff search:', self.close_word)
        print('----------------------------------------------')

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

        if learning_level:
            self.weblio = learning_level.text
        else:
            self.weblio = 'encouragement'

    def fweblio_mod(self, word):
        if (self.features).iloc[(self.words).tolist().index(self.close_word)]['weblio']:
            self.weblio = (self.features).iloc[(self.words).tolist().index(self.close_word)]['weblio']
        else:
            self.weblio = 'encouragement'

        #print("weblio:", self.weblio)

    def fgoogle_log(self, word):
        req = urllib.request.Request('https://www.google.com/search?q=' + word,
                                     headers={'User-Agent': 'PracticalMachineLearning' + str(random.randint(0, 500)),
                                              'Disallow': '/*data*$'})
        f = urllib.request.urlopen(req)
        bsObj = BeautifulSoup(f.read(), "html.parser")
        site_num_ori = bsObj.find('div', id='resultStats').string
        site_num = ''.join(re.findall(r'\d+', site_num_ori))
        f.close()
        self.google_log =math.log10(float(site_num))

    def fgoogle_log_mod(self, word):
        self.google_log = (self.features).iloc[(self.words).tolist().index(self.close_word)]['googlelog']
        self.google_log =math.log10(float(self.google_log))
        #print("google_log:", self.google_log)

    def ffreq_guten(self, word):
        datasets = nltk.corpus.gutenberg.fileids()
        total_freq = 0
        for i in range(0, len(datasets)):
            fdist = nltk.FreqDist(nltk.Text(nltk.corpus.gutenberg.words(str(datasets[i]))))
            total_freq = total_freq + fdist[word]
        self.freq_guten = total_freq

    def ffreq_guten_mod(self, word):
        self.freq_guten = (self.features).iloc[(self.words).tolist().index(self.close_word)]['gutenfq']
        #print("guten_frq:", self.freq_guten)

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

    def fpos_mod(self, word):
        self.pos = (self.features).iloc[(self.words).tolist().index(self.close_word)]['pos']
        #print("pos:", self.freq_guten)

    # def makeFeaturepickle(self):
    #     # save the model to disk
    #     dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    #     joblib.dump(self, os.path.join(dir_path, 'PML/pickled/features.sav'))

if __name__ == '__main__' :

    # Creation of a pickle
    svmFeatures = FeatureExtraction()
    dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    dill.settings['recurse'] = True # to access a member function
    dill.dump(svmFeatures, open(os.path.join(dir_path, 'PML\\pickled\\features.dill'), "wb"))

    # Testing
    word = 'reactively'

    start = time.clock()
    svmFeatures.search_similar_word_v1(word)
    print("------search similar word time v1:", time.clock() - start)

    start = time.clock()
    svmFeatures.fvrlen(word)
    print("------fvlen time:", time.clock() - start)

    start = time.clock()
    svmFeatures.fweblio_mod(word)
    print("------weblio time:", time.clock() - start)

    start = time.clock()
    svmFeatures.fgoogle_log_mod(word)
    print("------fgoodle time:", time.clock() - start)

    start = time.clock()
    svmFeatures.ffreq_guten_mod(word)
    print("------guten time:", time.clock() - start)

    start = time.clock()
    svmFeatures.fpos_mod(word)
    print("------pos time:", time.clock() - start)






































