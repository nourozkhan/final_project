import nltk

from nltk.sentiment.vader import SentimentIntensityAnalyzer

tweets = [
    'good ', 'intelligent','bed']

sid = SentimentIntensityAnalyzer()
for sentence in tweets:
    print(sentence)
    ss = sid.polarity_scores(sentence)
    for k in ss:
        print('{0}: {1}, '.format(k, ss[k]), end ='')
        print()

