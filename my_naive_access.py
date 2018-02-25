import nltk
import random
import pickle
from nltk.tokenize import word_tokenize
import json


documents_f = open("pickled_algos/documents.pickle", "rb")
documents = pickle.load(documents_f)
documents_f.close()

word_features5k_f = open("pickled_algos/word_features5k.pickle", "rb")
word_features = pickle.load(word_features5k_f)
word_features5k_f.close()


def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features


featuresets = [(find_features(rev), category) for (rev, category) in documents]

random.shuffle(featuresets)

testing_set = featuresets[10000:]
training_set = featuresets[:10000]

open_file = open("pickled_algos/originalnaivebayes5k.pickle", "rb")
classifier = pickle.load(open_file)
open_file.close()

print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set)) * 100)
classifier.show_most_informative_features(15)


def sentiment(text):
    feats = find_features(text)

    return classifier.classify(feats)


'''
file_name = 'processed_tweets.json'

with open(file_name) as f_obj:
    tweets = json.load(f_obj)

for tweet in tweets:
    print(sentiment(tweet))
'''

print(sentiment("asad is handsome boy"))
print(sentiment("asad is selfish boy"))
