from flask import Flask, Response
import os
import nltk
import random
import pickle
from twython import TwythonStreamer
import re
import json
from nltk.tokenize import word_tokenize

app = Flask(__name__)

headers = {
            'Cache-Control': 'no-cache',
            'Access-Control-Allow-Origin': '*'
        }

processed_tweets = []


@app.route('/')
def index():
    del processed_tweets[0:]

    return Response(
            processed_tweets,
           headers=headers
    )


@app.route('/test')
def test():
    print("testing")
    result = "positivity , 90.0 , negativity , 10.0 "
    return Response(
        result,
        headers=headers
    )


@app.route('/main')
def main():

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

    #print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set)) * 100)
    #classifier.show_most_informative_features(15)

    def sentiment(text):
        feats = find_features(text)

        return classifier.classify(feats)

    total_positive = 0
    total_negative = 0

    for tweet in processed_tweets:
        if sentiment(tweet) == 'pos':
            total_positive += 1
        else:
            total_negative += 1

    total_length = total_negative + total_positive
    positivity = (total_positive / total_length) * 100
    negativity = (total_negative / total_length) * 100

    result = "positivity , " + str(positivity) + " , negativity , " + str(negativity) + " "
    print(result)

    return Response(
        result,
        headers=headers
    )



@app.route('/sea/<user_input>')
def sea(user_input):


    def preprocess_word(word):
        # Remove punctuation
        word = word.strip('\'"?!,.():;')
        # Convert more than 2 letter repetitions to 2 letter
        # funnnnny --> funny
        word = re.sub(r'(.)\1+', r'\1\1', word)
        # Remove - & '
        word = re.sub(r'(-|\')', '', word)
        return word

    def is_valid_word(word):
        # Check if word begins with an alphabet
        return (re.search(r'^[a-zA-Z][a-z0-9A-Z\._]*$', word) is not None)

    def handle_emojis(tweet):
        # Smile -- :), : ), :-), (:, ( :, (-:, :')
        tweet = re.sub(r'(:\s?\)|:-\)|\(\s?:|\(-:|:\'\))', ' EMO_POS ', tweet)
        # Laugh -- :D, : D, :-D, xD, x-D, XD, X-D
        tweet = re.sub(r'(:\s?D|:-D|x-?D|X-?D)', ' EMO_POS ', tweet)
        # Love -- <3, :*
        tweet = re.sub(r'(<3|:\*)', ' EMO_POS ', tweet)
        # Wink -- ;-), ;), ;-D, ;D, (;,  (-;
        tweet = re.sub(r'(;-?\)|;-?D|\(-?;)', ' EMO_POS ', tweet)
        # Sad -- :-(, : (, :(, ):, )-:
        tweet = re.sub(r'(:\s?\(|:-\(|\)\s?:|\)-:)', ' EMO_NEG ', tweet)
        # Cry -- :,(, :'(, :"(
        tweet = re.sub(r'(:,\(|:\'\(|:"\()', ' EMO_NEG ', tweet)
        return tweet

    def preprocess_tweet(tweet):
        processed_tweet = []
        # Convert to lower case
        tweet = tweet.lower()
        # Replaces URLs with the word URL
        tweet = re.sub(r'((www\.[\S]+)|(https?://[\S]+))', ' URL ', tweet)
        # Replace @handle with the word USER_MENTION
        tweet = re.sub(r'@[\S]+', 'USER_MENTION', tweet)
        # Replaces #hashtag with hashtag
        tweet = re.sub(r'#(\S+)', r' \1 ', tweet)
        # Remove RT (retweet)
        tweet = re.sub(r'\brt\b', '', tweet)
        # Replace 2+ dots with space
        tweet = re.sub(r'\.{2,}', ' ', tweet)
        # Strip space, " and ' from tweet
        tweet = tweet.strip(' "\'')
        # Replace emojis with either EMO_POS or EMO_NEG
        tweet = handle_emojis(tweet)
        # Replace multiple spaces with a single space
        tweet = re.sub(r'\s+', ' ', tweet)

        words = word_tokenize(tweet)

        for word in words:
            word = preprocess_word(word)
            if is_valid_word(word):
                processed_tweet.append(word)

        return ' '.join(processed_tweet)

    #processed_tweets = []

    class MyStreamer(TwythonStreamer):
        """our own subclass of TwythonStreamer that specifies
        how to interact with the stream"""

        def on_success(self, data):
            """what do we do when twitter sends us data?
            here data will be a Python object representing a tweet"""

            # only want to collect English-language tweets
            if data['lang'] == 'en':
                tweet = data['text']
                processed_tweets.append(preprocess_tweet(tweet))

            # stop when we've collected enough
            if len(processed_tweets) >= 5:
                self.disconnect()

        def on_error(self, status_code, data):
            print(status_code, data)
            self.disconnect()

    stream = MyStreamer("nkm6QqtBlsAMarl65vofBHZSO", "Ud6bLeh7XUO6T3uqIvjUocdOQCsTUWs7yyNH9oLlsE43GEBtUH",
                        "776737130370433024-Muj5zw18tozpI2mpWx0DlzXQKucNXVZ",
                        "aQsUV6okJRqHGzP15Tdhnq9YbTw5vKIjzVdB5Xq5ULasY")

    # starts consuming public statuses that contain the keyword 'data'

    stream.statuses.filter(track=user_input)

    return Response(
        processed_tweets,
        headers=headers
    )


if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 3001)), debug=True)

