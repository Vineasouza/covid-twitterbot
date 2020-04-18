import tweepy
import settings
import requests
import datetime 
from bs4 import BeautifulSoup
from threading import Timer

CONSUMER_KEY = settings.ENV['CONSUMER_KEY']
CONSUMER_SECRET = settings.ENV['CONSUMER_SECRET']
ACCESS_KEY = settings.ENV['ACCESS_KEY']
ACCESS_SECRET = settings.ENV['ACCESS_SECRET']

# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# getting data
url = "https://www.worldometers.info/coronavirus/country/brazil/"
r = requests.get(url)
s = BeautifulSoup(r.text,"html.parser")
data = s.find_all("div",class_ = "maincounter-number")

#getting date
now = datetime.datetime.now()

# console log
#print(now.strftime("%Y-%m-%d %H:%M:%S") + "\nTotal Casos: "+ data[0].text.strip() + "\nTotal Mortes: " + data[1].text.strip () + "\nTotal Recuperados: " + data[2].text.strip())

# tweet stats
def tweet():
    #getting date
    now = datetime.datetime.now()

    api.update_status("--" + now.strftime("%Y-%m-%d %H:%M:%S") + "--" + "\nTotal Casos: "+ data[0].text.strip() + "\nTotal Mortes: " + data[1].text.strip () + "\nTotal Recuperados: " + data[2].text.strip())

    print("tweetado " + now.strftime("%Y-%m-%d %H:%M:%S"))

    Timer(1800.0, tweet).start()

Timer(1800.0, tweet).start()