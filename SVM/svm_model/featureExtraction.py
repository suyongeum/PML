import nltk
import pandas as pd
from operator import add
import urllib.request
from bs4 import BeautifulSoup
import math
import random
import re
import time

class FeatureExtraction :

    feature_data = []

    '''
    A class to extract features from data set: the words
    '''
    def __init__(self) :
        # Data reading from file and label the two columns: difficulty and word
        trainingdata = pd.read_csv('data_panda.csv', encoding="shift-jis", header=None, names=('difficulty', 'word'),
                                keep_default_na=False)
        self.feature_data = trainingdata

    def word_and_vowel_length(self):
        wordLength = []
        vowelLength  = []

        #for i in range(len(self.feature_data)):
        for word in self.feature_data['word']:
            wordLength.append(len(word))

            count = 0
            count = word.count('a')
            count += word.count('i')
            count += word.count('u')
            count += word.count('e')
            count += word.count('o')
            vowelLength.append(count)

        self.feature_data["wlen"] = wordLength
        self.feature_data["vlen"] = vowelLength

    # C:\Users\adagio\AppData\Roaming\nltk_data\corpora
    # Basically we use Gutenberg corpus
    def word_couting(self):
        datasets = nltk.corpus.gutenberg.fileids()
        self.feature_data['freq'] = 0

        # This routine takes a bit of time: 2 minutes in the desktop machine.
        total_freq = [0]*len(self.feature_data)
        for i in range(0, len(datasets)):
            fdist = nltk.FreqDist(nltk.Text(nltk.corpus.gutenberg.words(str(datasets[i]))))
            print(str(datasets[i]))
            word_freq = []
            for w in self.feature_data['word']:
                word_freq.append(fdist[w])
            total_freq = list(map(add, total_freq, word_freq))
        self.feature_data['freq'] = total_freq

    # tagging words
    def word_tagging(self):
        a = nltk.pos_tag(self.feature_data["word"])
        partOfSpeech = []

        #preparing category of simplified parts of speech
        noun = ('NN', 'NNS', 'NP')
        adj  = ('JJ', 'JJR', 'JJS')
        verb = ('RP', 'VB', 'VBD', 'VBG', 'VBN', 'VBZ', 'VBP', 'VD', 'VDD', 'VDG', 'VDN', 'VDZ', 'VDP', 'VH', 'VHD', 'VHG', 'VHN', 'VHZ', 'VHP', 'VV', 'VVD', 'VVG', 'VVN', 'VVP', 'VVZ')
        adv  = ('RB', 'RBR', 'RBS')

        for i in range(len(self.feature_data)):
            tag = a[i][1]
            done =  False
            for n in noun :
                if n in tag :
                    partOfSpeech.append(1)
                    done = True
                    break

            for j in adj :
                if done == True:
                    break
                if j in tag :
                    partOfSpeech.append(3)
                    done = True
                    break

            for v in verb :
                if done == True:
                    break
                if v in tag :
                    partOfSpeech.append(5)
                    done = True
                    break
            for av in adv :
                if done == True:
                    break
                if av in tag :
                    partOfSpeech.append(7)
                    done = True
                    break
        #######################################################################################
        #print(len(partOfSpeech)) --------------------------------------------
        #self.feature_data["pos"] = partOfSpeech

    # scrapping bing - one request takes around 1 second. so 11999 seconds ...
    def scraping_bing(self):
        word_popularity_bing = []
        for word in self.feature_data['word']:
            req = urllib.request.Request('https://www.bing.com/search?q=' + word,
                                         headers={'User-Agent': 'Osaka University'})
            f = urllib.request.urlopen(req)
            bsObj = BeautifulSoup(f.read(), "html.parser")
            site_num_ori = bsObj.find('span', class_='sb_count').string
            site_num = int(site_num_ori.replace(',', '').replace(' 件の検索結果', ''))
            f.close()
            word_popularity_bing.append(math.log10(site_num))
        self.feature_data["bing_num"] = word_popularity_bing

    # scrapping yahoo - one request takes around 1 second. so 11999 seconds ...
    def scraping_yahoo(self):
        word_popularity_yahoo = []
        for word in self.feature_data['word']:
            num_str = str(random.randint(0, 500))
            req = urllib.request.Request('https://search.yahoo.co.jp/search?p=' + word,
                                         headers={'User-Agent': 'PracticalMachineLearning' + num_str})
            f = urllib.request.urlopen(req)
            bsObj = BeautifulSoup(f.read(), "html.parser")
            site_num_ori = str(bsObj.find('div', id='inf'))
            site_num_1 = re.sub(r'.*約', '', site_num_ori)
            site_num_2 = re.sub(r'件.*', '', site_num_1)
            site_num = int(site_num_2.replace(',', ''))
            f.close()
            word_popularity_yahoo.append(math.log10(site_num))
        self.feature_data["yahoo_num"] = word_popularity_yahoo

    # scrapping weblio - faster than yahoo or bing scraping... let's say 0.5 second?
    def scraping_weblio(self):
        word_difficulity_level_weblio = []
        for word in self.feature_data['word']:
            req = urllib.request.Request('https://ejje.weblio.jp/content/' + word,
                                         headers={'User-Agent': 'PracticalMachineLearning'})
            f = urllib.request.urlopen(req)
            bsObj = BeautifulSoup(f.read(), "html.parser")
            # metatags = bsObj.findAll('meta')
            # word_class_1 = re.sub(r'】.*【*.*', '', str(metatags[1]))
            # word_class = re.sub(r'.* 【', '', word_class_1)
            learning_level = bsObj.find('span', class_='learning-level-content')
            f.close()
            word_difficulity_level_weblio.append(learning_level.text)
            # print(word, '-', learning_level.text)
        self.feature_data["weblio_diff_lev"] = word_difficulity_level_weblio

    # scrapping google - it takes a bit of time ...
    def scraping_google(self):
        word_popularity_google = []
        for word in self.feature_data['word']:
            num_str = str(random.randint(0, 500))
            time.sleep(random.randint(1, 6))
            req = urllib.request.Request('https://www.google.com/search?q=' + word,
                                         headers={'User-Agent': 'PracticalMachineLearning' + num_str})
            f = urllib.request.urlopen(req)
            bsObj = BeautifulSoup(f.read(), "html.parser")
            site_num_ori = bsObj.find('div', id='resultStats').string
            site_num = int(site_num_ori.replace('約 ', '').replace(',', '').replace(' 件', ''))
            f.close()
            word_popularity_google.append(math.log10(site_num))
        self.feature_data["google_num"] = word_popularity_google

if __name__ == '__main__' :
    features = FeatureExtraction()

    # after calling init -  data loading
    #print(features.feature_data.head())

    # add word_length
    #print(features.word_and_vowel_length())
    #print(features.feature_data.head())

    # extract word column
    # print(features.word_couting())
    # print(features.feature_data.head())

    # tagging words
    print(features.word_tagging())
    print(features.feature_data.head())

    # scrapping bing
    # print(features.scraping_bing())
    # print(features.feature_data.head())

    # scrapping yahoo
    # print(features.scraping_yahoo())
    # print(features.feature_data.head())

    # scrapping weblio
    # print(features.scraping_weblio())
    # print(features.feature_data.head())

    # scrapping google
    # print(features.scraping_google())
    # print(features.feature_data.head())



#     def categorizingIntoSpeech(self) :
#         import treetaggerwrapper as ttw
#
#         # preparing category of simplified parts of speech
#         noun = ('NN', 'NNS', 'NP')
#         adj  = ('JJ', 'JJR', 'JJS')
#         verb = ('RP', 'VB', 'VBD', 'VBG', 'VBN', 'VBZ', 'VBP', 'VD', 'VDD', 'VDG', 'VDN', 'VDZ', 'VDP', 'VH', 'VHD', 'VHG', 'VHN', 'VHZ', 'VHP', 'VV', 'VVD', 'VVG', 'VVN', 'VVP', 'VVZ')
#         adv  = ('RB', 'RBR', 'RBS')
#
#         tagger   = ttw.TreeTagger(TAGLANG='en', TAGDIR='../')
#         tagnum   = np.zeros(len(self.test))
#
#         for i, t in zip(range(len(self.test)), self.test) :
#             tags = tagger.TagText(t[1])
#
#             for n in noun :
#                 if n in tags[0] :
#                     tagnum[i] = 1
#                     continue
#
#             for j in adj :
#                 if j in tags[0] :
#                     tagnum[i] = 3
#                     continue
#
#             for v in verb :
#                 if v in tags[0] :
#                     tagnum[i] = 5
#                     continue
#
#             for av in adv :
#                 if av in tags[0] :
#                     tagnum[i] = 7
#                     continue
#
#
#         return tagnum
#
#     def searchingWeblio(self) :
#         # close explanation is in WeblioLevel()
#         weblio = np.loadtxt('./level.csv')
#
#         return weblio
#
# class WeblioLevel() :
#     '''
#     A class for getting 'level' from Weblio
#     Weblio : https://ejje.weblio.jp/
#     '''
#     def __init__(self, start, file) :
#         from selenium import webdriver
#         from selenium.common.exceptions import TimeoutException
#         import csv, sys, io, time
#
#         # Loading dataset
#         f    = open('./test.csv', 'r')
#         t = csv.reader(f, delimiter=' ')
#         self.test = list(t)
#
#         # Picking only words as list
#         self.words = [t[1] for t in self.test]
#
#         self.pickingLevel(start, file)
#
#     def pickingLevel(self, start, file) :
#         # Using Chrome
#         driver = webdriver.Chrome()
#         # timeout deadline is 10 sec
#         driver.set_page_load_timeout(10)
#
#         for i, w in zip(range(len(self.words))[start:], self.words[start:]) :
#             print(w)
#             #return
#
#             # accessing Weblio
#             while True :
#                 page = 'https://ejje.weblio.jp/content/' + w
#                 print(page)
#                 try :
#                     # moving to the URL
#                     driver.get(page)
#                     break
#
#                 except TimeoutException :
#                     # if timeout, reload
#                     print('timeout')
#                     continue
#
#             # getting 'level' from HTML
#             try :
#                 html      = driver.find_element_by_class_name('learning-level-content').text
#                 level     = int(html)
#             except :
#                 # if not found
#                 print("level not found...")
#                 level     = 0
#
#             # saving level as s csv and update the csv everytime
#             paper  = np.loadtxt('./levels/level' + str(file) + '.csv')
#             result = np.hstack((paper, level))
#             np.savetxt('./levels/level' + str(file) + '.csv', result)
#
#             # process log
#             print("score : %d" % level)
#             print("Completed %d/%d" % (i, len(self.words)))
#
#         driver.close()
