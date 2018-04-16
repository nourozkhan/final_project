from twython import TwythonStreamer
import json

# appending data to a global variable is pretty poor form
# but it makes the example much simpler
tweets = []


class MyStreamer(TwythonStreamer):
    """our own subclass of TwythonStreamer that specifies
    how to interact with the stream"""

    def on_success(self, data):
        """what do we do when twitter sends us data?
        here data will be a Python object representing a tweet"""

        # only want to collect English-language tweets
        if data['lang'] == 'en':
            #tweet = data.split(',"text":"')[1].split('","source')[0]
            tweet = data['text']
            tweets.append(tweet)
            #with open('tweetes.txt', 'a') as t_obj:
                #t_obj.write(tweet)

        # stop when we've collected enough
        if len(tweets) >= 100:
            self.disconnect()

    def on_error(self, status_code, data):
        print(status_code, data)
        self.disconnect()


stream = MyStreamer("Consumer Key", "Consumer Secret ",
                        "Access Token", "Access Token Secret")

# starts consuming public statuses that contain the keyword 'data'
stream.statuses.filter(track='donald trump')

#with open('tweets.json', 'w') as f_obj:
    #json.dump(tweets,f_obj)
for r_tweet in tweets:
    print(r_tweet)
