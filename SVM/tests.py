import django
django.setup()

from PML.nlp.Lemmatiser import Lemmatiser
from PCA.models import Word

lemmatiser = Lemmatiser()

# Create your tests here.

# Given text below
text = "hello words how are you suyong"

# # 1. Tokenize the sentence
# # 2. Recover the original form of each word
lemmas = lemmatiser.lemmatise_sentence(text)
print(lemmas)

# # 3. Difficulty level check from DB
print(Word.objects.count())



# 4. If does not exist, classify using SVM result.


