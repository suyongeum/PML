import nltk
import pandas as pd
from operator import add
import urllib.request
from bs4 import BeautifulSoup
import math
import random
import re
import time
import os

class FeatureExtraction :

    '''
    A class to extract features from data set: the words
    '''
    def __init__(self) :
        # Data reading from file and label the two columns: difficulty and word
        # trainingdata = pd.read_csv('data_panda.csv', encoding="shift-jis", header=None, names=('difficulty', 'word'),
        #                         keep_default_na=False)
        dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        base_features = pd.read_csv(os.path.join(dir_path, 'svm_model\\featureExtraction_for_training\\base_extracted_features.csv'), encoding="shift-jis", keep_default_na=False)
        self.feature_data = base_features

    def word_and_vowel_length(self):
        wordLength = []
        vowelRatio = []

        #for i in range(len(self.feature_data)):
        for word in self.feature_data['word']:
            wordLength.append(len(word))

            count = 0
            count = word.count('a')
            count += word.count('i')
            count += word.count('u')
            count += word.count('e')
            count += word.count('o')
            vowelRatio.append(count/len(word))

        self.feature_data["wlen"] = wordLength
        self.feature_data["vrlen"] = vowelRatio

    # C:\Users\adagio\AppData\Roaming\nltk_data\corpora
    # Basically we use Gutenberg corpus
    def word_couting(self):
        datasets = nltk.corpus.gutenberg.fileids()
        self.feature_data['freq_guten'] = 0

        # This routine takes a bit of time: 2 minutes in the desktop machine.
        total_freq = [0]*len(self.feature_data)
        for i in range(0, len(datasets)):
            fdist = nltk.FreqDist(nltk.Text(nltk.corpus.gutenberg.words(str(datasets[i]))))
            #print(str(datasets[i]))
            word_freq = []
            for w in self.feature_data['word']:
                word_freq.append(fdist[w])
            total_freq = list(map(add, total_freq, word_freq))
        self.feature_data['freq_guten'] = total_freq

    # tagging words
    def word_tagging(self):
        a = nltk.pos_tag(self.feature_data["word"])
        partOfSpeech = []

        #preparing category of simplified parts of speech
        noun = ('NN', 'NNS', 'NP', 'IN', 'CD', 'FW', 'CC', 'UH')
        adj  = ('JJ', 'JJR', 'JJS')
        verb = ('RP', 'VB', 'VBD', 'VBG', 'VBN', 'VBZ', 'VBP', 'VD', 'VDD', 'VDG', 'VDN', 'VDZ', 'VDP', 'VH', 'VHD', 'VHG', 'VHN', 'VHZ', 'VHP', 'VV', 'VVD', 'VVG', 'VVN', 'VVP', 'VVZ', 'POS')
        adv  = ('RB', 'RBR', 'RBS', 'WDT', 'DT', 'WP', 'MD', 'TO')

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
            if done == False:
                print(a[i][0] , '-' , a[i][1])
                partOfSpeech.append(10)
        #######################################################################################
        print(len(partOfSpeech))
        print(len(self.feature_data))
        self.feature_data["pos"] = partOfSpeech

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
        for word in ['happy']: # self.feature_data['word']:
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
            #print(word, '-', learning_level.text)
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

    # Basic features include
    # 1. word length
    # 2. vowel ratio to word
    # 3. freq_brown corpus
    # 4. freq_reuter corpus
    # 5. weblio (learning level)
    # 6. bing_log
    # 7. yahoo_log
    # 8. google_log

    features = FeatureExtraction()
    print(features.feature_data.head())

    # Let's add
    # 9. freq_gutenberg

    features.word_couting()
    print(features.feature_data.head())

    # Let's add
    # 10. Position of Speech

    features.word_tagging()
    print(features.feature_data.head())

    # Let's save it into total features...

    features.feature_data.to_csv('total_extracted_features.csv')

