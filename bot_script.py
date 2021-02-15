#!/usr/bin/python
'''
USE AT YOUR OWN PERIL <3
fill in your API keys before running the script
written in Python3 by Judith van Stegeren, @jd7h
'''

#import twitter #for docs, see https://python-twitter.readthedocs.io/en/latest/twitter.html
import nltk
nltk.download('averaged_perceptron_tagger')
import tweepy
import logging
#from config import create_api
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

'''
before running the script, do this:
1. create a virtual environment
$ python3 -m venv venv
$ source venv/bin/activate
2. install the dependencies
$ pip install python-twitter
3. obtain API keys from twitter
4. fill them in in the script below
'''

def twitter_demo():
    # connect to api with apikeys
    # if you don't have apikeys, go to apps.twitter.com
    tknzr = nltk.tokenize.TweetTokenizer()
    myString = "This is a cooool #dummysmiley: :-) :-P <3"
    
    print(tknzr.tokenize(myString))

def check_mentions(api, keywords, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
        #logger.info(f"Text is {tweet.text}")
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        if any(keyword in tweet.text.lower() for keyword in keywords):
            logger.info(f"Answering to {tweet.user.name}")
            print(str(tweet.text))
            text = tweet.text[8:]
            tknzr = nltk.tokenize.TweetTokenizer()
            tokens = tknzr.tokenize(text)
            print(f"after tokenize {tokens}")
            
            print(nltk.pos_tag(tokens))

            SA = nltk.sentiment.vader.SentimentIntensityAnalyzer()
            SA.polarity_scores(text)
            print(SA)

            



            #if not tweet.user.following:
            #    tweet.user.follow()
            try:
                api.update_status(
    
                    status= "@%s Hello!" % (tweet.user.screen_name),
                    in_reply_to_status_id=tweet.id,
                )
            except tweepy.TweepError as e:
                print(e.reason)
    return new_since_id

def main():
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler("i43i0N9plzAa7wf4huwpxsvcN", "V7yAapEx33sxfR3HKTYYQVWlWdZA3acVVDynkXPau39BdK4V0M")
    auth.set_access_token("1360611491611869184-0OfpGHTFo9JYA3ZIaqJIKMNFdmPzve", "r45sGkAn1Y6c4GZZjbuxnmBbEVJB2DolDXapNab2ZVfL4")

    # Create API object
    api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)
    #api = create_api()
    since_id = 1
    while True:
        since_id = check_mentions(api, ["help", "support"], since_id)
        logger.info("Waiting...")
        time.sleep(30)

if __name__ == "__main__":
    main()

