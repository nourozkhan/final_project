
# Here's our data
dataset = [["good", "positive"], ["not good", "negative"], ["intellgent", "neutral"], ["smart", "positive"], ["ugly", "negative"], ["dirty", "negative"], ["honest", "positive"]]
#naive bayes algorithm
# We're trying to predict whether or not the new_tweet is positive or negative.
new_tweet = ["intellgent"]

def calc_y_probability(y_label, dataset):
  return len([d for d in dataset if d[1] == y_label]) / len(dataset)

def calc_word_probability_given_y(ran_label, y_label, dataset):
  return len([d for d in dataset if d[1] == y_label and d[0] == ran_label]) / len(dataset)

denominator = len([d for d in dataset if d[0] == new_tweet[0]]) / len(dataset)
# Plug all the values into our formula.  Multiply the class (y) probability, and the probability of the x-values occuring given that class.
prob_pos = (calc_y_probability("positive", dataset) * calc_word_probability_given_y(new_tweet[0], "positive", dataset)) / denominator

prob_neg = (calc_y_probability("negative", dataset) * calc_word_probability_given_y(new_tweet[0], "negative", dataset)) / denominator

prob_neu = (calc_y_probability("neutral", dataset) * calc_word_probability_given_y(new_tweet[0], "neutral", dataset)) / denominator

# Make a classification decision based on the probabilities.
classification = "positive"
if prob_neg > prob_pos:
  classification = "negative"

if prob_neu > prob_neg:
  classification = "neutral"
print("Final classification for new_tweet: {0}. positive: {1}. negative: {2}. neutral:{3}".format(classification, prob_pos, prob_neg, prob_neu))
