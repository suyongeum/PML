import pandas as pd

trainingdata = pd.read_csv('data_panda.csv', encoding="shift-jis", header=None, names=('difficulty', 'word'),
                           keep_default_na=False)

data_one = pd.read_csv('feature_one.csv', encoding="shift-jis", keep_default_na=False)
data_two = pd.read_csv('feature_two.csv', keep_default_na=False)

print (trainingdata.head())
print (data_one.head())
print (data_two.head())

word_list = []
for i in  trainingdata['word']:
    word_list.append(i)

print(word_list)

data_two.word = data_two.word.astype("category")
data_two.word.cat.set_categories(word_list, inplace=True)
sorted_data_two = data_two.sort_values(["word"])

print ('before sorting')
print(data_two['word'].head())

print ('after sorting')
print(sorted_data_two['word'].head(10))

#########################################
# create a new features: trainingdata and sorted_data_two

# for i in range(0, len(trainingdata['word'])):
#     if trainingdata['word'][i] != sorted_data_two['word']:
#         print('differ')

new_features = trainingdata

new_features['len'] = data_one['length']
new_features['vrlen'] = data_one['vowel']/data_one['length']
new_features['freq_brown'] = data_one['hitBrown']
new_features['freq_reuter'] = data_one['hitReuter']
new_features['weblio'] = sorted_data_two['learning_level']
new_features['bing_log'] = sorted_data_two['site_num_log_bing']
new_features['yahoo_log'] = sorted_data_two['site_num_log_yahoo']
new_features['google_log'] = sorted_data_two['site_num_log_google']

new_features.to_csv('base_extracted_features.csv')

print(new_features.head())

# data_two_list = []
# for i in  data_two['word']:
#     data_two_list.append(i)
#
# index = 0
# for i in trainingdata['word']:
#     found = False
#     for j in data_two['word']:
#         if (i == j):
#             #print (index, ')', i, j)
#             word_list.remove(i)
#             data_two_list.remove(j)
#             found = True
#             break
#     if(found == False):
#         print(index, '-###############################################################)', i, ' --- ' ,j)
#     #print(index, ')', i, ' --- ', j)
#     index = index + 1
#
#
# print(word_list)
# print(data_two_list)





